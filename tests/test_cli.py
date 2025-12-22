# SPDX-License-Identifier: MPL-2.0
"""Test the Command Line Interface."""

from __future__ import annotations

from typing import TYPE_CHECKING

from session_info2.cli import main

if TYPE_CHECKING:
    import pytest


def test_cli(capsys: pytest.CaptureFixture[str]) -> None:
    main(["pytest"])

    out, err = capsys.readouterr()

    assert not err
    assert "pytest" in out
    assert "session-info2" in out
    assert out.index("pytest") < out.index("---") < out.index("session-info2")
