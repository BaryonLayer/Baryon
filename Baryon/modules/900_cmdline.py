"""
Module for modifying the executable to be launched
"""

import os
from pathlib import Path

from modules import BaryonModule
from modules import ModuleReturn
from modules import ToolType

from modules import proton_index


class Cmdline(BaryonModule):
    @staticmethod
    def module_run(pre_command: list, command: list, command_args: list, tool_type=ToolType.OTHER,
                   verb=None, is_scriptevaluator=None, **kwargs) -> ModuleReturn:
        if not is_scriptevaluator and any(cmd in os.environ for cmd in ["BARYON_EXEC", "BARYON_CMDLINE"]):
            __exec = os.environ.get("BARYON_EXEC", None)
            __args = os.environ.get("BARYON_ARGS", None)

            if os.environ.get("BARYON_DIR", None) is not None:
                path_dir = Path(os.environ.get("BARYON_DIR")).expanduser()
                if path_dir.exists():
                    os.chdir(path_dir)
                elif os.environ.get("BARYON_CMDLINE", None) is not None:
                    path_cmdline = Path(os.environ.get("BARYON_CMDLINE")).expanduser()
                    if path_cmdline.exists():
                        os.chdir(path_cmdline.parent)

            if not __exec:
                __cmdline = os.environ.get("BARYON_CMDLINE").split(";")
                __exec = __cmdline[0]
                if len(__cmdline) > 1:
                    __args = ";".join(__cmdline[1:]).split(" ")

            if tool_type == ToolType.PROTON and proton_index(command) >= 0:
                p_index = proton_index(command)
                command[p_index + 2] = __exec
            else:
                command.clear()
                command.append(__exec)

            if __args:
                command_args.clear()
                command_args.append(__args)
        return ModuleReturn.SKIP

    @staticmethod
    def post_execute(pre_command: list, command: list, command_args: list, **kwargs):
        return 0


def priority():
    return 900


def get_module() -> BaryonModule:
    return Cmdline()
