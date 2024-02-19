from firecore._init import start_training
from pydantic import BaseModel


class Config(BaseModel):
    max_epochs: int = 100

    class Train(BaseModel):
        batch_size: int = 128

    train: Train = Train()

    class Val(BaseModel):
        batch_size: int = 256

    val: Val = Val()





def main():
    with start_training(Config) as ctx:
        print(ctx.config)


if __name__ == "__main__":
    main()
