"""
Module for modifying the executable to be launched
"""

import os

from modules import BaryonModule
from modules import ModuleReturn
from modules import ToolType
from modules import proton_index


class ProtonAlwaysRun(BaryonModule):
    """
    Allows you to bypass the restriction that a prefix does not run a game while another program is running in it.
    """

    @staticmethod
    def module_run(pre_command: list, command: list, command_args: list, tool_type=ToolType.OTHER,
                   verb=None, is_scriptevaluator=None, **kwargs) -> ModuleReturn:
        p_index = proton_index(command)

        if bool(int(os.environ.get("BARYON_ALWAYSRUN", 0))) and tool_type == ToolType.PROTON and p_index >= 0:
            command[p_index + 1] = "run"

        return ModuleReturn.NEXT

    @staticmethod
    def post_execute(pre_command: list, command: list, command_args: list, **kwargs):
        return 0


def priority():
    return 10


def get_module() -> BaryonModule:
    return ProtonAlwaysRun()
