"""
This functions are originally located at `Catalyst. Reproducible and fast DL & RL`_

Some methods were formatted and simplified.

.. _`Catalyst. Reproducible and fast DL & RL`:
    https://github.com/catalyst-team/catalyst
"""

import os

import argparse
import copy
import json
import yaml
from pydoc import locate

from typing import List, Any, Type, Optional, Dict
from collections import OrderedDict
from .types import Storage


class OrderedLoader(yaml.Loader):
    pass


def construct_mapping(loader, node):
    loader.flatten_mapping(node)
    return OrderedDict(loader.construct_pairs(node))


OrderedLoader.add_constructor(
    yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, construct_mapping
)


def type_from_str(dtype: str) -> Type:
    """Returns type by giving string
    Args:
        dtype (str): string representation of type
    Returns:
        (Type): type
    Examples:
        >>> type_from_str("str")
        str
        >>> type_from_str("int")
        int
        >>> type(type_from_str("int"))
        type
    """
    return locate(dtype)


def argparser(**argparser_kwargs) -> argparse.ArgumentParser:
    """Creates typical argument parser with ``--config`` argument
    Args:
        **argparser_kwargs: Arguments for ``ArgumentParser.__init__``, optional.
            See more at `Argparse docs`_
    Returns:
        (ArgumentParser): parser with ``--config`` argument

    .. _`Argparse docs`:
        https://docs.python.org/3/library/argparse.html#argumentparser-objects
    """
    argparser_kwargs = argparser_kwargs
    parser_ = argparse.ArgumentParser(**argparser_kwargs)

    parser_.add_argument(
        "-C", "--config",
        type=str,
        required=True,
        help="Path to a config file (YAML or JSON)",
        metavar="PATH"
    )
    return parser_


def load_config(config_path: str, ordered: bool = False) -> Storage:
    """Loads config by giving path. Supports YAML and JSON files.
    Args:
        config_path (str): path to config file (YAML or JSON)
        ordered (bool): decide if the config should be loaded as ``OrderedDict``
    Returns:
        (Storage): Config
    Raises:
        Exception: if path ``config_path`` doesn't exists or file format is not YAML or JSON
    """
    if not os.path.exists(config_path):
        raise Exception(f"Path '{config_path}' doesn't exist!")

    with open(config_path, "r") as stream:
        if config_path.endswith("json"):
            object_pairs_hook = OrderedDict if ordered else None
            config = json.load(stream, object_pairs_hook=object_pairs_hook)

        elif config_path.endswith("yml"):
            loader = OrderedLoader if ordered else yaml.Loader
            config = yaml.load(stream, loader)
        else:
            raise Exception("Unknown file format")

    return config


def parse_content(value: str) -> Any:
    """Parses strings ``value:dtype`` into typed value
    Args:
        value (str): string with form ``value:dtype`` or ``value``
    Returns:
        (Any): value of type ``dtype``, if ``dtype`` wasn't specified value will be parsed as string
    Examples:
        >>> parse_content("True:bool")
        True # type is bool
        >>> parse_content("True:str")
        "True" # type is str
        >>> parse_content("True")
        "True" # type is str
        >>> parse_content("some str")
        "some str" # type is str
        >>> parse_content("1:int")
        1 # type is int
        >>> parse_content("1:float")
        1.0 # type is float
    """
    content = value.rsplit(":", 1)
    if len(content) == 1:
        value_content, value_type = content[0], "str"
    else:
        value_content, value_type = content

    result = value_content
    value_type = type_from_str(value_type)
    if value_type is not None:
        result = value_type(value_content)

    return result


def update_config_from_args(config: Storage, args: List[str]) -> Storage:
    """Updates configuration file with list of arguments
    Args:
        config (Storage): configuration dict
        args (List[str]): list of arguments with form ``--key:dtype:value:dtype``
    Returns:
        (Storage): updated config
    """
    updated_config = copy.deepcopy(config)

    for argument in args:
        names, value = argument.split("=")
        names = names.lstrip("-").strip("/")

        value = parse_content(value)
        names = [parse_content(name) for name in names.split("/")]

        # safe_set(updated_config, *names, value=value)
        config_ = updated_config
        # TODO: change to `safe_set`
        for name in names[:-1]:
            if name not in config_:
                config_[name] = {}

            config_ = config_[name]

        config_[names[-1]] = value

    return updated_config


def load_config_from_args(
        arguments: Optional[List[str]] = None,
        argparser_kwargs:  Optional[Dict] = None
) -> Storage:
    """Parses command line arguments, loads config and updates it with unknown args
    Args:
        arguments (List[str], optional): arguments to parse, if None uses command line arguments
        argparser_kwargs (dict, optional): arguments for ``ArgumentParser.__init__``.
    Returns:
        (Storage): config dict with updated values from unknown args
    Examples:
        >>> load_config_from_args("-C examples/config.json --verbose=True:bool --paths/jsons/0:int=uno".split())
    """
    argparser_kwargs = argparser_kwargs or {}
    args, uargs = argparser(**argparser_kwargs).parse_known_args(args=arguments)
    config = load_config(args.config, ordered=False)
    return update_config_from_args(config, uargs)
