import torch
from torch import nn, Tensor
import torch.nn.functional as F
from loguru import logger
import rich
import typed_args as ta
from pathlib import Path
from firecore.config.evaluate import evaluate_config
from firecore.config.lazy import instantiate
from firecore.config import _types


@ta.dataclass
class Args(ta.TypedArgs):
    no_cuda: bool = ta.add_argument("--no-cuda", action="store_true")
    no_mps: bool = ta.add_argument("--no-mps", action="store_true")
    dry_run: bool = ta.add_argument("--dry-run", action="store_true")
    seed: int = ta.add_argument("--seed", default=1)
    log_interval: int = ta.add_argument("--log-interval", default=10)
    save_model: bool = ta.add_argument("--save-model", action="store_true")

    config: Path = ta.add_argument("-c", "--config", type=Path, required=True)


def train(
    args: Args,
    model: nn.Module,
    device: torch.device,
    train_loader,
    optimizer,
    epoch: int,
):
    model.train()
    for batch_idx, (data, target) in enumerate(train_loader):
        data, target = data.to(device), target.to(device)
        optimizer.zero_grad()
        output = model(data)
        loss = F.nll_loss(output, target)
        loss.backward()
        optimizer.step()
        if batch_idx % args.log_interval == 0:
            logger.info(
                "Train Epoch: {} [{}/{} ({:.0f}%)]\tLoss: {:.6f}".format(
                    epoch,
                    batch_idx * len(data),
                    len(train_loader.dataset),
                    100.0 * batch_idx / len(train_loader),
                    loss.item(),
                )
            )
            if args.dry_run:
                break


def test(model: nn.Module, device: torch.device, test_loader):
    model.eval()
    test_loss = 0
    correct = 0
    with torch.no_grad():
        for data, target in test_loader:
            data, target = data.to(device), target.to(device)
            output = model(data)
            test_loss += F.nll_loss(
                output, target, reduction="sum"
            ).item()  # sum up batch loss
            pred = output.argmax(
                dim=1, keepdim=True
            )  # get the index of the max log-probability
            correct += pred.eq(target.view_as(pred)).sum().item()

    test_loss /= len(test_loader.dataset)

    logger.info(
        "\nTest set: Average loss: {:.4f}, Accuracy: {}/{} ({:.0f}%)\n".format(
            test_loss,
            correct,
            len(test_loader.dataset),
            100.0 * correct / len(test_loader.dataset),
        )
    )


def main():
    logger.disable("firecore._config")
    args = Args.parse_args()
    rich.print(args)

    use_cuda = not args.no_cuda and torch.cuda.is_available()
    use_mps = not args.no_mps and torch.backends.mps.is_available()

    torch.manual_seed(args.seed)

    if use_cuda:
        device = torch.device("cuda")
    elif use_mps:
        device = torch.device("mps")
    else:
        device = torch.device("cpu")

    logger.info("device: {}", device)

    # train_kwargs = {
    #     "batch_size": config.train.batch_size,
    # }
    # test_kwargs = {"batch_size": config.test.batch_size}
    # if use_cuda:
    #     cuda_kwargs = {"num_workers": 1, "pin_memory": True, "shuffle": True}
    #     train_kwargs.update(cuda_kwargs)
    #     test_kwargs.update(cuda_kwargs)

    # transform = transforms.Compose(
    #     [transforms.ToTensor(), transforms.Normalize((0.1307,), (0.3081,))]
    # )
    # dataset1 = datasets.MNIST("/tmp", train=True, download=True, transform=transform)
    # dataset2 = datasets.MNIST("/tmp", train=False, transform=transform)
    # train_loader = DataLoader(dataset1, **train_kwargs)
    # test_loader = DataLoader(dataset2, **test_kwargs)

    # model = Net().to(device)
    # if config.opt == OptimizerType.adadelta:
    #     optimizer = optim.Adadelta(model.parameters(), **config.adadelta.model_dump())
    # else:
    #     raise Exception()

    # if config.sche == SchedulerType.step_lr:
    #     scheduler = optim.lr_scheduler.StepLR(
    #         optimizer, step_size=1, **config.step_lr.model_dump()
    #     )
    # else:
    #     raise Exception()

    config: _types.Config = evaluate_config(str(args.config))
    rich.print(config)

    # rich.print(components)

    model = instantiate(config["model"]).to(device)
    params = instantiate(config["params"])(model)
    optimizer = instantiate(config["optimizer"])(params)
    scheduler = instantiate(config["lr_scheduler"])(optimizer)
    epochs = config["strategy"]["max_epochs"]
    train_loader = instantiate(config["train"]["loader"])
    test_loader = instantiate(config["val"]["loader"])

    for epoch in range(1, epochs + 1):
        train(args, model, device, train_loader, optimizer, epoch)
        test(model, device, test_loader)

        scheduler.step()

    if args.save_model:
        output_path = "/tmp/mnist_cnn.pt"
        logger.info("save model: {}", output_path)
        torch.save(model.state_dict(), output_path)


if __name__ == "__main__":
    main()
