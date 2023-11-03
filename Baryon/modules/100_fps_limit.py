import os

from modules import BaryonModule
from modules import ModuleReturn


class FPSLimit(BaryonModule):
    @staticmethod
    def module_run(pre_command: list, command: list, command_args: list, **kwargs) -> ModuleReturn:
        __fps = os.environ.get("BARYON_FPS", None)
        if __fps:
            os.environ["MANGOHUD_CONFIG"] = (
                "read_cfg,"
                f"fps_limit={__fps}"
            )

        return ModuleReturn.NEXT

    @staticmethod
    def post_execute(pre_command: list, command: list, command_args: list, **kwargs):
        return 0


def priority():
    return 100


def get_module() -> BaryonModule:
    return FPSLimit()
