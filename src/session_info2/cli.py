# SPDX-License-Identifier: MPL-2.0
"""CLI."""

from __future__ import annotations

import sys
from argparse import ArgumentParser, Namespace
from argparse import BooleanOptionalAction as Ba
from types import ModuleType
from typing import Literal, get_args
from unittest.mock import patch

from . import _repr, session_info

Format = Literal["text", "markdown", "html", "json"]


class Args(Namespace):
    """CLI arguments."""

    packages: list[str]
    os: bool
    cpu: bool
    gpu: bool
    dependencies: bool
    format: Format

    @classmethod
    def parser(cls) -> ArgumentParser:
        """Return argument parser."""
        parser = ArgumentParser()
        parser.add_argument("packages", nargs="*", help="packages to import")
        parser.add_argument(
            "--os", default=True, action=Ba, help="include OS name and version"
        )
        parser.add_argument(
            "--cpu", default=True, action=Ba, help="include number of CPU cores"
        )
        parser.add_argument(
            "--gpu",
            default=False,
            action=Ba,
            help="include information per supported GPU (disabled by default)",
        )
        parser.add_argument(
            "--dependencies", default=True, action=Ba, help="include dependencies"
        )
        parser.add_argument(
            "-f",
            "--format",
            default="text",
            choices=get_args(Format),
            help="output format",
        )
        return parser

    @classmethod
    def parse(cls, args: list[str] | None = None) -> Args:
        """Parse CLI arguments."""
        return cls.parser().parse_args(args, cls())


def main(args_: list[str] | None = None, /) -> None:
    """Run CLI."""
    args = Args.parse(args_)

    modules = {name: __import__(name) for name in args.packages}

    with patch.dict(sys.modules, __main__=type("__main__", (ModuleType,), modules)):
        si = session_info(
            os=args.os, cpu=args.cpu, gpu=args.gpu, dependencies=args.dependencies
        )

    match args.format:
        case "text":
            print(si)
        case "markdown":
            print(_repr.repr_markdown(si))
        case "html":
            print(_repr.repr_html(si))
        case "json":
            print(_repr.repr_json(si))
        case _:
            raise AssertionError
