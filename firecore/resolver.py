from .import_utils import require
from typing import Dict, Any, List
from firecore.logging import get_logger
import functools

logger = get_logger(__name__)

KEY_CALL = '_call'
KEY_PARTIAL = '_partial'


def resolve(cfg: Any, **extra_kwargs):
    """
    _0, _1 should be args
    _call should be require name
    others are kwargs
    """

    if isinstance(cfg, dict):
        if KEY_CALL in cfg:
            return _resolve_object(cfg, **extra_kwargs)
        elif KEY_PARTIAL in cfg:
            return _resolve_partial(cfg, **extra_kwargs)
        else:
            return _resolve_dict(cfg, **extra_kwargs)
    elif isinstance(cfg, list):
        return _resolve_list(cfg, **extra_kwargs)
    elif isinstance(cfg, str):
        return _resolve_string(cfg, **extra_kwargs)
    else:
        return cfg


def _resolve_dict(cfg: Dict[str, Any], **extra_kwargs) -> Dict[str, Any]:
    return {k: resolve(v, **extra_kwargs) for k, v in cfg.items()}


def _resolve_object(cfg: Dict[str, Any], **extra_kwargs) -> Any:
    call_name = cfg[KEY_CALL]
    args, kwargs = _resolve_args_kwargs(KEY_CALL, cfg, **extra_kwargs)
    return require(call_name)(*args, **kwargs)


def _resolve_partial(cfg: Dict[str, Any], **extra_kwargs) -> functools.partial:
    call_name = cfg[KEY_PARTIAL]
    args, kwargs = _resolve_args_kwargs(KEY_PARTIAL, cfg, **extra_kwargs)
    return functools.partial(require(call_name), *args, **kwargs)


def _resolve_list(cfg: List[Any], **extra_kwargs) -> List[Any]:
    return [resolve(x, **extra_kwargs) for x in cfg]


def _resolve_args_kwargs(key: str, cfg: Dict[str, Any], **extra_kwargs):
    call_name = cfg[key]

    args = {}
    arg_idx = 0
    while True:
        arg_name = '_{}'.format(arg_idx)
        if arg_name in cfg:
            args[arg_name] = cfg[arg_name]
            arg_idx += 1
        else:
            break

    kwargs = {k: v for k, v in cfg.items() if k != key and k not in args}

    logger.debug(
        'Start resolving object',
        name=call_name,
        args=list(args.values()), kwargs=kwargs
    )
    args_resolved = _resolve_list(args.values(), **extra_kwargs)
    kwargs_resolved = _resolve_dict(kwargs, **extra_kwargs)
    return args_resolved, kwargs_resolved


def _resolve_string(cfg: str, **kwargs):
    if cfg.startswith('$'):
        key = cfg[1:]
        return kwargs[key]
    else:
        return cfg
