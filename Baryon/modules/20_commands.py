"""
Module for modifying the executable to be launched
"""

import os
import subprocess

from modules import BaryonModule
from modules import ModuleReturn
from modules import ToolType


class Commands(BaryonModule):
    """
    module that runs commands before and after startup compatibility tool
    """

    @staticmethod
    def module_run(pre_command: list, command: list, command_args: list, tool_type=ToolType.OTHER,
                   verb=None, is_scriptevaluator=None, **kwargs) -> ModuleReturn:
        start_command = os.environ.get("BARYON_START", None)
        if not is_scriptevaluator and start_command:
            subprocess.Popen(start_command, shell=True)
        return ModuleReturn.NEXT

    @staticmethod
    def post_execute(pre_command: list, command: list, command_args: list, is_scriptevaluator=None, **kwargs):
        end_command = os.environ.get("BARYON_END", None)
        if not is_scriptevaluator and end_command:
            subprocess.run(end_command, shell=True)
        return 0


def priority():
    return 20


def get_module() -> BaryonModule:
    return Commands()
