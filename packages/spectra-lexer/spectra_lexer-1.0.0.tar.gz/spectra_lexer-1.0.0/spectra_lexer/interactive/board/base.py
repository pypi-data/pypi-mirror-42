""" Module for generating steno board diagram elements and descriptions. """

from typing import Dict, List, Tuple

from spectra_lexer import Component, on, pipe
from spectra_lexer.config import CFGOption
from spectra_lexer.interactive.board.matcher import ElementMatcher
from spectra_lexer.rules import RuleFlags, StenoRule


class BoardRenderer(Component):
    """ Creates graphics and description strings for the board diagram. """

    ROLE = "board"
    show_compound: bool = CFGOption(True, "Compound Key Labels", "Show special labels for compound keys and numbers")

    _matcher: ElementMatcher  # Generates the list of element IDs for each stroke of a rule.

    def __init__(self) -> None:
        """ Set up the matcher with an empty rule dictionary. """
        super().__init__()
        self._matcher = ElementMatcher()

    @on("new_rules")
    def set_rules(self, rules_dict:Dict[str,StenoRule]) -> None:
        """ Set up the generator with the rule dictionary. """
        self._matcher.set_rules(rules_dict)

    @pipe("new_svg", "new_board_setup")
    def set_elements(self, xml_dict:dict) -> Tuple[str, List[str]]:
        """ Load the generator with each graphical element that has a specific rule.
            Send the raw SVG text data along with all usable element IDs to the GUI. """
        self._matcher.set_rule_elements(xml_dict["ids"])
        return xml_dict["raw"], self._matcher.get_all_ids()

    @pipe("new_lexer_result", "new_board_info")
    def get_info(self, rule:StenoRule) -> Tuple[List[List[str]], str]:
        """ Generate board diagram elements from a steno rule and send them along with the description. """
        keys, letters, flags, desc, rulemap = rule
        raw_keys = keys.rtfcre
        if RuleFlags.GENERATED in flags:
            # If this is a lexer-generated rule (usually the root at the top), just display the description.
            description = desc
        elif not rulemap:
            # Base rules (i.e. leaf nodes) display their keys to the left of their descriptions.
            description = "{}: {}".format(raw_keys, desc)
        else:
            # Derived rules (i.e. non-leaf nodes) show the complete mapping of keys to letters in their description.
            description = "{} → {}: {}".format(raw_keys, letters, desc)
        # Create the list of element ID lists (one list for each stroke), with or without the special rule elements.
        if self._matcher:
            elements = self._matcher.get_element_ids(rule, self.show_compound)
        else:
            elements = []
        return elements, description

    @pipe("new_graph_selection", "new_board_info")
    def get_selection_info(self, rule:StenoRule) -> Tuple[List[List[str]],str]:
        """ The task is identical whether the rule is from a new lexer result or a user graph selection. """
        return self.get_info(rule)
