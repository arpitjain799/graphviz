"""Execute rendering subprocesses and open files in viewer."""

import typing

from .. import copying
from .common import ENGINES, FORMATS, RENDERERS, FORMATTERS, RequiredArgumentError
from .graphviz import version
from .rendering import (DOT_BINARY,
                        render,
                        pipe, pipe_string, pipe_lines, pipe_lines_string)
from .running import run_check, ExecutableNotFound
from .unflattening import unflatten
from .viewing import view, View

__all__ = ['DOT_BINARY', 'UNFLATTEN_BINARY',
           'ENGINES', 'FORMATS', 'RENDERERS', 'FORMATTERS',
           'RequiredArgumentError',
           'render', 'pipe', 'pipe_string', 'pipe_lines', 'pipe_lines_string',
           'unflatten',
           'Graphviz',
           'version', 'view',
           'View',
           'ExecutableNotFound']


class Graphviz(copying.Copy):
    """Graphiz default engine/format."""

    _engine = 'dot'

    _format = 'pdf'

    _renderer = None

    _formatter = None

    @staticmethod
    def _pipe_lines(*args, **kwargs):
        """Simplify mocking ``pipe_lines``."""
        return pipe_lines(*args, **kwargs)

    @staticmethod
    def _pipe_lines_string(*args, **kwargs):
        return pipe_lines_string(*args, **kwargs)

    @staticmethod
    def _render(*args, **kwargs):
        """Simplify mocking ``render``."""
        return render(*args, **kwargs)

    @staticmethod
    def _unflatten(*args, **kwargs):
        return unflatten(*args, **kwargs)

    def __init__(self, format=None, engine=None, *,
                 renderer: typing.Optional[str] = None,
                 formatter: typing.Optional[str] = None,
                 **kwargs):
        super().__init__(**kwargs)

        if format is not None:
            self.format = format

        if engine is not None:
            self.engine = engine

        self.renderer = renderer

        self.formatter = formatter

    def _copy_kwargs(self, **kwargs):
        """Return the kwargs to create a copy of the instance."""
        attr_kw = [('_engine', 'engine'), ('_format', 'format'),
                   ('_renderer', 'renderer'), ('_formatter', 'formatter')]
        ns = self.__dict__
        for attr, kw in attr_kw:
            assert kw not in kwargs
            if attr in ns:
                kwargs[kw] = ns[attr]
        return super()._copy_kwargs(**kwargs)

    @property
    def engine(self) -> str:
        """The layout engine used for rendering
            (``'dot'``, ``'neato'``, ...)."""
        return self._engine

    @engine.setter
    def engine(self, engine: str) -> None:
        engine = engine.lower()
        if engine not in ENGINES:
            raise ValueError(f'unknown engine: {engine!r}')
        self._engine = engine

    @property
    def format(self) -> str:
        """The output format used for rendering
            (``'pdf'``, ``'png'``, ...)."""
        return self._format

    @format.setter
    def format(self, format: str) -> None:
        format = format.lower()
        if format not in FORMATS:
            raise ValueError(f'unknown format: {format!r}')
        self._format = format

    @property
    def renderer(self) -> typing.Optional[str]:
        """The output renderer used for rendering
            (``'cairo'``, ``'gd'``, ...)."""
        return self._renderer

    @renderer.setter
    def renderer(self, renderer: typing.Optional[str]) -> None:
        if renderer is None:
            self.__dict__.pop('_renderer', None)
        else:
           renderer = renderer.lower()
           if renderer not in RENDERERS:
               raise ValueError(f'unknown renderer: {renderer!r}')
           self._renderer = renderer

    @property
    def formatter(self) -> typing.Optional[str]:
        """The output formatter used for rendering
            (``'cairo'``, ``'gd'``, ...)."""
        return self._formatter

    @formatter.setter
    def formatter(self, formatter: typing.Optional[str]) -> None:
        if formatter is None:
            self.__dict__.pop('_formatter', None)
        else:
            formatter = formatter.lower()
            if formatter not in FORMATTERS:
                 raise ValueError(f'unknown formatter: {formatter!r}')
            self._formatter = formatter

    def _get_backend_kwargs(self, *,
                            format: typing.Optional[str] = None,
                            renderer: typing.Optional[str] = None,
                            formatter: typing.Optional[str] = None,
                            **kwargs):
        if format is None:
            format = self._format

        if renderer is None:
            renderer = self._renderer

        if formatter is None:
            formatter = self._formatter

        kwargs.update(format=format, renderer=renderer, formatter=formatter)

        return kwargs

    _get_pipe_kwargs = _get_render_kwargs = _get_backend_kwargs
