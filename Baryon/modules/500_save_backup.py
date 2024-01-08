import os
import shutil
import threading
import filecmp
from pathlib import Path

from modules import BaryonModule
from modules import ModuleReturn


class BackupThread(threading.Thread):
    def __init__(self, location, timeout=1, copies=15):
        super().__init__(daemon=True)
        self.location = location
        self.timeout = timeout
        self.copies = copies
        self.alive = threading.Event()

    def mask(self, copy_number):
        return str(self.location) + " bck" + str(copy_number)

    @staticmethod
    def remove_path(path):
        if Path(path).exists():
            if Path(path).is_dir():
                shutil.rmtree(path)
            else:
                Path(path).unlink()

    def move_path(self, path_from, path_to):
        if Path(path_from).exists():
            if Path(path_to).exists():
                self.remove_path(path_to)
            shutil.move(path_from, path_to)

    def copy_path(self, path_from, path_to):
        if Path(path_from).exists():
            if Path(path_to).exists():
                self.remove_path(path_to)
            if Path(path_from).is_dir():
                shutil.copytree(path_from, path_to)
            else:
                shutil.copy(path_from, path_to)

    @staticmethod
    def check_path(path_one, path_two) -> bool:
        # True is the same, False is different
        if not Path(path_two).exists():
            return False
        if Path(path_one).is_dir() and Path(path_two).is_dir():
            def is_same_directories(dir_cmp) -> bool:
                if dir_cmp.diff_files or dir_cmp.left_only or dir_cmp.right_only:
                    return False
                for sub_dir in dir_cmp.subdirs.values():
                    if not is_same_directories(sub_dir):
                        return False
                return True

            _dir_cmp = filecmp.dircmp(path_one, path_two)
            return is_same_directories(_dir_cmp)
        if Path(path_one).is_file() and Path(path_two).is_file():
            return filecmp.cmp(path_one, path_two)
        return False

    def make_copy(self):
        if self.copies < 0:
            return
        if self.check_path(self.location, self.mask(1)):
            return

        for i in range(self.copies, 1, -1):
            self.move_path(self.mask(i - 1), self.mask(i))
        self.copy_path(self.location, self.mask(1))

    def run(self):
        self.alive.wait(self.timeout)
        while not self.alive.is_set():
            self.make_copy()
            self.alive.wait(self.timeout)

    def stop(self):
        self.alive.set()


class SaveBackup(BaryonModule):
    """
    Module what allow start Thread to back up saves
    """

    def __init__(self):
        self.thread = None
        self.alive = True

    def module_run(self, pre_command: list, command: list, command_args: list, is_scriptevaluator=False,
                   **kwargs) -> ModuleReturn:
        if "BARYON_BACKUP_LOCATION" in os.environ and os.environ["BARYON_BACKUP_LOCATION"]:
            path = os.environ["BARYON_BACKUP_LOCATION"]
            if "%USERPROFILE%" in path:
                compat_data_path = os.environ.get("STEAM_COMPAT_DATA_PATH", "")
                userprofile = Path(compat_data_path) / "pfx/drive_c/users/steamuser/"
                path = path.replace("%USERPROFILE%", str(userprofile))
            backup_location = Path(path).expanduser()
            print("Baryon backup started. Backup location {}".format(backup_location))
            if backup_location.exists():
                self.thread = BackupThread(backup_location)
                self.thread.start()
        return ModuleReturn.NEXT

    def post_execute(self, pre_command: list, command: list, command_args: list, **kwargs):
        if self.thread is not None and isinstance(self.thread, BackupThread):
            self.thread.stop()
        return 0


def priority():
    return 500


def get_module() -> BaryonModule:
    return SaveBackup()
