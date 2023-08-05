"""
Entrypoint for Transformer when used as a library.
"""
import warnings
from pathlib import Path
from typing import Sequence, Union, Iterable, TextIO, Iterator, TypeVar

from transformer.locust import locustfile, locustfile_lines
from transformer.plugins import sanitize_headers
from transformer.plugins.contracts import OnTaskSequence
from transformer.scenario import Scenario

DEFAULT_PLUGINS = (sanitize_headers.plugin,)


def transform(
    scenarios_path: Union[str, Path],
    plugins: Sequence[OnTaskSequence] = (),
    with_default_plugins: bool = True,
) -> str:
    """
    This function is deprecated and will be removed in a future version.
    Do not rely on it.
    Reason: It only accepts one scenario path at a time, and requires plugins
    to be already resolved (and therefore that users use
    transformer.plugins.resolve, which is kind of low-level). Both dumps & dump
    lift these constraints and have a more familiar naming
    (see json.dump/s, etc.).
    Deprecated since: v1.0.2.
    """
    warnings.warn(DeprecationWarning("transform: use dump or dumps instead"))
    if with_default_plugins:
        plugins = (*DEFAULT_PLUGINS, *plugins)
    return locustfile([Scenario.from_path(Path(scenarios_path), plugins)])


LaxPath = Union[str, Path]
PluginName = str


def dumps(
    scenario_paths: Iterable[LaxPath],
    plugins: Sequence[PluginName] = (),
    with_default_plugins: bool = True,
) -> str:
    """
    Transforms the provided scenarios using the provided plugins, and returns
    the resulting locustfile code as a string.

    See also: dump

    :param scenario_paths: paths to scenario files (HAR) or directories
    :param plugins: names of plugins to use
    :param with_default_plugins: whether the default plugins should be used in
        addition to those provided (recommended: True)
    """
    return "\n".join(_dump_as_lines(scenario_paths, plugins, with_default_plugins))


def dump(
    file: TextIO,
    scenario_paths: Iterable[LaxPath],
    plugins: Sequence[PluginName] = (),
    with_default_plugins: bool = True,
) -> None:
    """
    Transforms the provided scenarios using the provided plugins, and writes
    the resulting locustfile code in the provided file.

    See also: dumps

    :param file: an object with a `writelines` method (as specified by
        io.TextIOBase), e.g. `sys.stdout` or the result of `open`.
    :param scenario_paths: paths to scenario files (HAR) or directories.
    :param plugins: names of plugins to use.
    :param with_default_plugins: whether the default plugins should be used in
        addition to those provided (recommended: True).
    """
    file.writelines(
        intersperse("\n", _dump_as_lines(scenario_paths, plugins, with_default_plugins))
    )


def _dump_as_lines(
    scenario_paths: Iterable[LaxPath],
    plugins: Sequence[PluginName],
    with_default_plugins: bool,
) -> Iterator[str]:
    if with_default_plugins:
        plugins = (*DEFAULT_PLUGINS, *plugins)
    yield from locustfile_lines(
        [Scenario.from_path(path, plugins) for path in scenario_paths]
    )


T = TypeVar("T")


def intersperse(delim: T, iterable: Iterable[T]) -> Iterator[T]:
    """
    >>> list(intersperse(",", "a"))
    ['a']
    >>> list(intersperse(",", ""))
    []
    >>> list(intersperse(",", "abc"))
    ['a', ',', 'b', ',', 'c']
    >>> list(intersperse(",", ["a", "b", "c"]))
    ['a', ',', 'b', ',', 'c']
    """
    it = iter(iterable)
    try:
        yield next(it)
    except StopIteration:
        return
    for x in it:
        yield delim
        yield x
