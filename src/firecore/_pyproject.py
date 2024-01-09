import msgspec


class FirecoreConfig(msgspec.Struct):
    """
    Add all firecore related config here
    """

    work_dir: str = "works"


class Tool(msgspec.Struct):
    firecore: FirecoreConfig


class PyProject(msgspec.Struct):
    tool: Tool


if __name__ == "__main__":
    cfg = msgspec.toml.decode(open("pyproject.toml", "r").read(), type=PyProject)
    print(cfg.tool.firecore)
