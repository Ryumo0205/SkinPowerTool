#!/usr/bin/env python
# -*-coding:utf-8 -*-


from modules.ui import UI
import maya.cmds as cmds

import modules.ui
import modules.information


# Force reload the modules to avoid using old instances when UI is called multiple times
import importlib
importlib.reload(modules.ui)
importlib.reload(modules.information)


if __name__ == "__main__":
    ui = UI()
    ui.show_ui()
    # Multiple scriptJobs using the same event might interfere with each other causing incorrect info updates
    info_listening = cmds.scriptJob(
        event=["SelectionChanged", ui.update_ui], protected=True, parent=ui.main_window)


else:
    pass
