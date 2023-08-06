""" Base module of the Spectra lexer core package. Contains the most fundamental components. Don't touch anything... """

import argparse
from functools import partial
from typing import ClassVar, Hashable, List

from spectra_lexer.engine import Engine
from spectra_lexer.utils import nop


def pipe(key:Hashable, next_key:Hashable=None, **cmd_kwargs) -> callable:
    """ Decorator for component engine command flow. """
    def base_decorator(func:callable) -> callable:
        """ Call the command and pipe its return value to another command. """
        func.cmd = (key, next_key, cmd_kwargs)
        return func
    return base_decorator


# All command decorators currently do the same thing.
on = respond_to = fork = pipe


class Component:
    """
    Base class for any component that sends and receives commands from the Spectra engine.
    It is the root class of the Spectra lexer object hierarchy, being subclassed directly
    or indirectly by nearly every important (externally-visible) piece of the program.
    As such, it cannot depend on anything except core helpers and pure utility functions.
    """

    # Standard identifier for a component's function, usable in many ways (e.g. config page title).
    ROLE: ClassVar[str] = "UNDEFINED"

    _cmd_attr_list: ClassVar[List[tuple]] = []  # Default class command parameter list; meant to be copied.
    engine_call: callable = nop  # Default engine callback is a no-op (useful for testing individual components).

    def __init_subclass__(cls) -> None:
        """ Make a list of commands this component class handles with methods that handle each one.
            Each engine-callable method (class attribute) has its command info saved on an attribute.
            Save each of these to a list. Combine it with the parent's command list to make a new child list.
            This new combined list covers the full inheritance tree. Parent commands execute first. """
        cmd_list = [(attr, *func.cmd) for attr, func in vars(cls).items() if hasattr(func, "cmd")]
        cls._cmd_attr_list = cmd_list + cls._cmd_attr_list

    def engine_connect(self, cb:callable) -> None:
        """ Set the callback used for engine calls by this component. """
        self.engine_call = cb

    def engine_commands(self) -> List[tuple]:
        """ Bind all class command functions to the instance and return the raw (key, (func, ...)) command tuples.
            Each command has a main callable followed by optional instructions on what to execute next. """
        return [(key, (getattr(self, attr), *params)) for (attr, key, *params) in self._cmd_attr_list]


class Gateway(Component):
    """ Central constructor/container for components. All commands issued to children go through here first. """

    components: List[Component]  # List of all child components. Should not change after initialization.

    def engine_connect(self, cb:callable) -> None:
        """ All child components must be able to call the engine independently. """
        for c in self.components:
            c.engine_call = cb

    def engine_commands(self) -> List[tuple]:
        """ Any command serviced by a child component should be forwarded here by the engine. """
        cmds = [cmd for c in self.components for cmd in c.engine_commands()]
        return [(key, (partial(self.engine_call, func), *params)) for (key, (func, *params)) in cmds]


class Application(Engine):
    """ Runnable component setup for an engine that serves as a base for an entire application. """

    components: List[Component]  # List of all connected components. Should not change after initialization.

    def __init__(self, *cls_iter:type):
        """ Assemble child components from constructors and initialize the engine. """
        super().__init__()
        # Create all necessary components in order from base to derived classes.
        self.components = [cls() for cls in cls_iter]
        # Add (key, (func, ...)) command tuples and set callbacks for all child components.
        for c in self.components:
            for (key, cmd) in c.engine_commands():
                self.setdefault(key, []).append(cmd)
            c.engine_connect(self.call)

    def start(self, **opts) -> None:
        """ Send the start signal with options from command line arguments parsed from sys.argv,
            followed by keyword options given directly by subclasses or by main(). """
        # Suppress defaults for unused options so that they don't override the ones from subclasses with None.
        parser = argparse.ArgumentParser(argument_default=argparse.SUPPRESS)
        for c in opts:
            parser.add_argument('--' + c)
        # Command-line options must be added with update() to enforce precedence and eliminate duplicates.
        opts.update(vars(parser.parse_args()))
        self.call("start", **opts)
