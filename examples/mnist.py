import torch
from torch import nn, Tensor
import torch.nn.functional as F
from pydantic import BaseModel
import enum
from firecore._init import prepare_parser, load_or_parse_config
from loguru import logger
import rich
from torchvision import datasets, transforms
from torch.utils.data import DataLoader
from torch import optim


class Train(BaseModel):
    batch_size: int = 64


class Test(BaseModel):
    batch_size: int = 1000


class OptimizerType(enum.Enum):
    adadelta = enum.auto()


class Adadelta(BaseModel):
    lr: float = 1.0


class SchedulerType(enum.Enum):
    step_lr = enum.auto()


class StepLr(BaseModel):
    gamma: float = 0.7


class Config(BaseModel):
    train: Train = Train()
    test: Test = Test()
    epochs: int = 14
    opt: OptimizerType = OptimizerType.adadelta
    adadelta: Adadelta = Adadelta()
    sche: SchedulerType = SchedulerType.step_lr
    step_lr: StepLr = StepLr()

    no_cuda: bool = False
    no_mps: bool = False
    dry_run: bool = False
    seed: int = 1
    log_interval: int = 10
    save_model: bool = False


class Net(nn.Module):
    def __init__(self):
        super(Net, self).__init__()
        self.conv1 = nn.Conv2d(1, 32, 3, 1)
        self.conv2 = nn.Conv2d(32, 64, 3, 1)
        self.dropout1 = nn.Dropout(0.25)
        self.dropout2 = nn.Dropout(0.5)
        self.fc1 = nn.Linear(9216, 128)
        self.fc2 = nn.Linear(128, 10)

    def forward(self, x):
        x = self.conv1(x)
        x = F.relu(x)
        x = self.conv2(x)
        x = F.relu(x)
        x = F.max_pool2d(x, 2)
        x = self.dropout1(x)
        x = torch.flatten(x, 1)
        x = self.fc1(x)
        x = F.relu(x)
        x = self.dropout2(x)
        x = self.fc2(x)
        output = F.log_softmax(x, dim=1)
        return output


def train(
    args: Config,
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
    parser = prepare_parser(Config)
    ns = parser.parse_args()
    config = load_or_parse_config(ns, Config)
    rich.print(config)

    use_cuda = not config.no_cuda and torch.cuda.is_available()
    use_mps = not config.no_mps and torch.backends.mps.is_available()

    torch.manual_seed(config.seed)

    if use_cuda:
        device = torch.device("cuda")
    elif use_mps:
        device = torch.device("mps")
    else:
        device = torch.device("cpu")

    logger.info('device: {}', device)

    train_kwargs = {
        "batch_size": config.train.batch_size,
    }
    test_kwargs = {"batch_size": config.test.batch_size}
    if use_cuda:
        cuda_kwargs = {"num_workers": 1, "pin_memory": True, "shuffle": True}
        train_kwargs.update(cuda_kwargs)
        test_kwargs.update(cuda_kwargs)

    transform = transforms.Compose(
        [transforms.ToTensor(), transforms.Normalize((0.1307,), (0.3081,))]
    )
    dataset1 = datasets.MNIST("/tmp", train=True, download=True, transform=transform)
    dataset2 = datasets.MNIST("/tmp", train=False, transform=transform)
    train_loader = DataLoader(dataset1, **train_kwargs)
    test_loader = DataLoader(dataset2, **test_kwargs)

    model = Net().to(device)
    if config.opt == OptimizerType.adadelta:
        optimizer = optim.Adadelta(model.parameters(), **config.adadelta.model_dump())
    else:
        raise Exception()

    if config.sche == SchedulerType.step_lr:
        scheduler = optim.lr_scheduler.StepLR(
            optimizer, step_size=1, **config.step_lr.model_dump()
        )
    else:
        raise Exception()

    for epoch in range(1, config.epochs + 1):
        train(config, model, device, train_loader, optimizer, epoch)
        test(model, device, test_loader)

        if config.sche == SchedulerType.step_lr:
            scheduler.step()

    if config.save_model:
        output_path = "/tmp/mnist_cnn.pt"
        logger.info("save model: {}", output_path)
        torch.save(model.state_dict(), output_path)


if __name__ == "__main__":
    main()
