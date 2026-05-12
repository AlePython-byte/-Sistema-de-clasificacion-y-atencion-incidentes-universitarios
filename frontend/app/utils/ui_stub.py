"""Provides a `ui` object that wraps NiceGUI when available.
If NiceGUI is not installed, exposes a minimal dummy `ui` to allow static analysis
and simple test runs without raising import errors. This helps keep files free
of unresolved-import errors in editors and CI while remaining transparent when
the real package is installed.
"""
from typing import Any, Callable

try:
    from nicegui import ui as _real_ui  # type: ignore
except Exception:
    class _DummyContext:
        def __init__(self, *args, **kwargs):
            pass

        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc, tb):
            return False

        def classes(self, *args, **kwargs):
            return self

        def style(self, *args, **kwargs):
            return self

        def add(self, *args, **kwargs):
            return None

    class _DummyInput:
        def __init__(self, *args, **kwargs):
            self.value = ''

    class _DummyUI:
        def link(self, *args, **kwargs):
            return None

        def row(self, *args, **kwargs):
            return _DummyContext()

        def column(self, *args, **kwargs):
            return _DummyContext()

        def card(self, *args, **kwargs):
            return _DummyContext()

        def label(self, *args, **kwargs):
            return None

        def h1(self, *args, **kwargs):
            return None

        def h3(self, *args, **kwargs):
            return None

        def table(self, *args, **kwargs):
            return None

        def input(self, *args, **kwargs):
            return _DummyInput()

        def textarea(self, *args, **kwargs):
            return _DummyInput()

        def button(self, *args, **kwargs):
            return None

        def notify(self, *args, **kwargs):
            return None

        def title(self, *args, **kwargs):
            return None

        def page(self, *args, **kwargs):
            def decorator(f: Callable[..., Any]):
                return f
            return decorator

        def run(self, *args, **kwargs):
            return None

    _real_ui = _DummyUI()

ui = _real_ui
