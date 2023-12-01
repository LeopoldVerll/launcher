import sys

from PyQt5.QtWidgets import QApplication

from Updater_Module.gui import SimpleMessageBox
from Updater_Module.main import updater


def run_updater(repo_owner, repo_name, current_version, asset_name):
    if not sys.stdin.isatty():
        app = QApplication(sys.argv)
        window = SimpleMessageBox()
        window.show()

    # if not sys.stdin.isatty():
    #     sys.exit(app.exec_())

    return updater(repo_owner, repo_name, current_version, asset_name)
