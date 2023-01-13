import rjsonnet
from typing import Optional, Union, List, Dict, Tuple, Callable, overload
import warnings


warnings.warn("don't use this module, use `rjsonnet` instead")

ImportCallback = Callable[[str, str], Tuple[str, Optional[str]]]


@overload
def evaluate_file(
    filename: str,
    jpathdir: Optional[Union[str, List[str]]] = None,
    max_stack: int = 500,
    gc_min_objects: int = 1000,
    gc_growth_trigger: float = 2.0,
    ext_vars: Dict[str, str] = {},
    ext_codes: Dict[str, str] = {},
    tla_vars: Dict[str, str] = {},
    tla_codes: Dict[str, str] = {},
    max_trace: int = 20,
    import_callback: Optional[ImportCallback] = None,
    native_callbacks: Dict[str, Tuple[str, Callable]] = {},
) -> str: ...


def evaluate_file(
    filename: str,
    **kwargs,
) -> str:
    """eval file
    Args:
        filename: jsonnet file
    """
    return rjsonnet.evaluate_file(filename, **kwargs)


@overload
def evaluate_snippet(
    filename: str,
    snippet: str,
    jpathdir: Optional[Union[str, List[str]]] = None,
    max_stack: int = 500,
    gc_min_objects: int = 1000,
    gc_growth_trigger: float = 2.0,
    ext_vars: Dict[str, str] = {},
    ext_codes: Dict[str, str] = {},
    tla_vars: Dict[str, str] = {},
    tla_codes: Dict[str, str] = {},
    max_trace: int = 20,
    import_callback: Optional[ImportCallback] = None,
    native_callbacks: Dict[str, Tuple[str, Callable]] = {},
) -> str: ...


def evaluate_snippet(
    filename: str,
    snippet: str,
    **kwargs,
) -> str:
    """eval snippet
    Args:
        filename: fake name for snippet
        expr: the snippet
    """
    return rjsonnet.evaluate_snippet(filename, snippet, **kwargs)
