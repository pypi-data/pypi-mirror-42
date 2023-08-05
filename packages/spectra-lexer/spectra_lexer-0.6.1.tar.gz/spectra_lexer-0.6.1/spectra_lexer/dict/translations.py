import json
from typing import List

from spectra_lexer.dict import ResourceManager

# Plover's app user dir and config filename. Dictionaries are located in the same directory.
_PLOVER_USER_DIR: str = "~plover/"
_PLOVER_CFG_FILENAME: str = "plover.cfg"


class TranslationsManager(ResourceManager):
    """ Translation parser for the Spectra program. The structures are just string dicts
        that require no extra processing after conversion to/from JSON. """

    ROLE = "dict_translations"

    @property
    def files(self) -> List[str]:
        """ Attempt to find the local Plover user directory and, if found, decode all dictionary files
            in the correct priority order (reverse of normal, since earlier keys overwrite later ones). """
        try:
            cfg_dict = self.engine_call("file_load", _PLOVER_USER_DIR + _PLOVER_CFG_FILENAME)[0]
            dict_section = cfg_dict['System: English Stenotype']['dictionaries']
            # The section we need is read as a string, but it must be decoded as a JSON array.
            return [_PLOVER_USER_DIR + e['path'] for e in reversed(json.loads(dict_section))]
        except OSError:
            # Catch-all for file loading errors. Just assume the required files aren't there and move on.
            pass
        except KeyError:
            print("Could not find dictionaries in plover.cfg.")
        except json.decoder.JSONDecodeError:
            print("Problem decoding JSON in plover.cfg.")
        return []
