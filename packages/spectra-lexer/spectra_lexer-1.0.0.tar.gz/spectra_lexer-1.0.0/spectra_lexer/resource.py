from functools import partialmethod
from typing import Sequence

from spectra_lexer import Component, fork, pipe
from spectra_lexer.utils import merge


class ResourceManager(Component):
    """ Base class for conversion, parsing, and other file operations on specific resource types. """

    files: Sequence[str] = ()  # Input filenames overridden by subclass default parameters or the command line.

    def __init_subclass__(cls) -> None:
        """ Create command decorators for each subclass based on its role/resource type. """
        s = cls.ROLE
        cls.start = pipe("start", s + "_load")(partialmethod(cls.start))
        cls.load = fork(s + "_load", "new_" + s)(partialmethod(cls.load))
        cls.save = pipe(s + "_save", "file_save")(partialmethod(cls.save))
        cls.dialog = pipe(s + "_dialog", "new_dialog_info")(partialmethod(cls.dialog))
        super().__init_subclass__()

    def start(self, **opts) -> Sequence[str]:
        """ If there is a command line option for this component, even if empty, attempt to load its resource.
            If the option is not empty (or otherwise evaluates True), save it over the default first. """
        file = opts.get(self.ROLE)
        if file is not None:
            if file:
                self.files = [file]
            return ()

    def load(self, filenames:Sequence[str]=()) -> dict:
        """ Load and merge resources from disk. If no filenames are given by the command,
            load the one from defaults or the command line. """
        dicts = self.engine_call("file_load", *(filenames or self.files))
        return self.parse(merge(dicts))

    def parse(self, d:dict) -> dict:
        """ Optional parse function to convert from raw disk format. May simply return the argument unchanged. """
        return d

    def save(self, filename:str, obj:object) -> tuple:
        """ Parse an object into raw form using reference data from the parser, then save it.
            If no save filename is given, use the first/only default file (if there's none, an IndexError is fine.) """
        return (filename or self.files[0]), self.inv_parse(obj)

    def inv_parse(self, obj:object) -> object:
        """ Optional parse function to convert to raw disk format. May simply return the argument unchanged. """
        return obj

    def dialog(self) -> tuple:
        """ Get all valid file extensions for this data type and send them with the role to a new GUI file dialog. """
        return self.ROLE, self.engine_call("file_get_supported_exts")
