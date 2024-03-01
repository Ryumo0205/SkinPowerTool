#!/usr/bin/env python
# -*-coding:utf-8 -*-
from modules.edit import edit
from modules.information import info
import modules.edit
import modules.information
import importlib
import maya.cmds as cmds
import os
import webbrowser

importlib.reload(modules.edit)


ui_relative_path = __file__
main_path = os.path.dirname(ui_relative_path)
parent_directory = os.path.dirname(main_path)
print("----main path---- : ", parent_directory)


class UI ():

    def __init__(self):



        self.ui_file = parent_directory + r"\skinPowerTool.ui"
        self.window_name = "SkinPowerTool_Main"
        self.main_window = None  

    
        self.edit_targets = None

    
        self.AlljointsName_list = None
        self.jointsName_list = None
        self.weights_list = None

    
        self.pushButton_grow = None
        self.pushButton_shrink = None
        self.pushButton_plus = None
        self.pushButton_minus = None
        self.pushButton_0 = None
        self.pushButton_dot25 = None
        self.pushButton_dot5 = None
        self.pushButton_dot75 = None
        self.pushButton_1 = None
        self.pushButton_floatUp = None
        self.pushButton_floatDown = None
        self.pushButton_append = None
        self.pushButton_search = None
        self.pushButton_copy = None
        self.pushButton_paste = None
        self.pushButton_smooth = None
        self.pushButton_mirror = None
        self.pushButton_prune = None
        self.pushButton_round = None
        self.pushButton_set = None
        self.pushButton_Donate = None

        # 字串視窗
        self.text_search = None
        self.text_doublespin = None
        self.text_prune = None
        self.text_round = None

    def close_ui(self, window_name):
        """
        Closes a specified Maya UI window and forcibly terminates any associated script jobs.

        This function checks if a window with the given name exists. If it does, 
        the function will search for Maya script jobs that contain the window name.
        It then forcibly terminates those script jobs to ensure there are no leftover processes 
        after closing the window.
        Finally, it uses the deleteUI command to delete the window.

        Parameters:
        window_name : str
            The name of the window to be closed.
        """

        if cmds.window(window_name, exists=True):
            print("Closing window: {}".format(window_name))

            script_jobs = cmds.scriptJob(listJobs=True)
            for job in script_jobs:
                if window_name in job:
                    job_num = int(job.split(":")[0])
                    cmds.scriptJob(kill=job_num, force=True)

            cmds.deleteUI(window_name, window=True)
            print("UI deleted")

        else:
            print("No window named '{}' found to close.".format(window_name))

    def create_main_window(self):
       

        self.main_window = cmds.loadUI(uiFile=self.ui_file)


        self.AlljointsName_list = cmds.textScrollList(
            self.main_window + r"|AlljointsName_list", edit=True)
        self.jointsName_list = cmds.textScrollList(
            self.main_window + r"|jointsName_list", edit=True)
        self.weights_list = cmds.textScrollList(
            self.main_window + r"|weights_list", edit=True)


        self.pushButton_grow = cmds.button(
            self.main_window + r"|pushButton_grow", edit=True, command=self.select_grow)
        self.pushButton_shrink = cmds.button(
            self.main_window + r"|pushButton_shrink", edit=True, command=self.select_shrink)
        self.pushButton_plus = cmds.button(
            self.main_window + r"|pushButton_plus", edit=True, command=self.weight_plus_btn)
        self.pushButton_minus = cmds.button(
            self.main_window + r"|pushButton_minus", edit=True, command=self.weight_minus_btn)
        self.pushButton_0 = cmds.button(
            self.main_window + r"|pushButton_0", edit=True, command=self.weight_0_btn)
        self.pushButton_dot25 = cmds.button(
            self.main_window + r"|pushButton_dot25", edit=True, command=self.weight_dot25_btn)
        self.pushButton_dot5 = cmds.button(
            self.main_window + r"|pushButton_dot5", edit=True, command=self.weight_dot5_btn)
        self.pushButton_dot75 = cmds.button(
            self.main_window + r"|pushButton_dot75", edit=True, command=self.weight_dot75_btn)
        self.pushButton_1 = cmds.button(
            self.main_window + r"|pushButton_1", edit=True, command=self.weight_1_btn)
        self.pushButton_floatUp = cmds.button(
            self.main_window + r"|pushButton_floatUp", edit=True, command=self.set_float_up)
        self.pushButton_floatDown = cmds.button(
            self.main_window + r"|pushButton_floatDown", edit=True, command=self.set_float_down)
        self.pushButton_append = cmds.button(
            self.main_window + r"|pushButton_append", edit=True, command=self.append_btn)
        self.pushButton_search = cmds.button(
            self.main_window + r"|pushButton_search", edit=True, command=self.search_btn)
        self.pushButton_copy = cmds.button(
            self.main_window + r"|pushButton_copy", edit=True, command=self.weight_copy_btn)
        self.pushButton_paste = cmds.button(
            self.main_window + r"|pushButton_paste", edit=True, command=self.weight_paste_btn)
        self.pushButton_smooth = cmds.button(
            self.main_window + r"|pushButton_smooth", edit=True, command=self.weight_smooth_btn)
        self.pushButton_mirror = cmds.button(
            self.main_window + r"|pushButton_mirror", edit=True, command=self.mirror_btn)
        self.pushButton_prune = cmds.button(
            self.main_window + r"|pushButton_prune", edit=True, command=self.prune_btn)
        self.pushButton_round = cmds.button(
            self.main_window + r"|pushButton_round", edit=True, command=self.round_btn)
        self.pushButton_set = cmds.button(
            self.main_window + r"|pushButton_set", edit=True, command=self.weight_set_btn)
        self.pushButton_Donate = cmds.button(
            self.main_window + r"|pushButton_Donate", edit=True, command=self.donate_page_btn)

        
        self.text_search = cmds.textField(
            self.main_window + r"|text_search", edit=True, placeholderText="Search Influencies",changeCommand=self.search_btn)
        # cmds.textField(self.text_search, edit=True, changeCommand=self.search_btn)
        
        self.text_doublespin = cmds.textField(
            self.main_window + r"|text_doublespin", edit=True, text="0.01")
        self.text_prune = cmds.textField(
            self.main_window + r"|text_prune", edit=True, text="0.01")
        self.text_round = cmds.textField(
            self.main_window + r"|text_round", edit=True, text="2")

        self.window = cmds.showWindow(self.main_window)

    def show_ui(self):
        
        self.close_ui(self.window_name)
        self.create_main_window()

        if self.main_window is not None:
            print("Showing window: {}".format(self.main_window))
            cmds.showWindow(self.main_window)
        else:
            print("Failed to create main window.")

    def update_ui(self):
        """
        更新 UI 介面。

        執行作業包含：
        1. 重新獲取最新資訊。
        2. 清空並更新所有關節名稱列表。
        3. 檢查並更新選定關節名稱列表。
        4. 清空並更新權重列表。
        最後，在控制檯列印 "ui update !" 表示更新完畢。
        """
        
        if info.update_info() == False:
            cmds.textScrollList(self.AlljointsName_list,
                              edit=True, removeAll=True)
            cmds.textScrollList(self.jointsName_list, edit=True, removeAll=True)
            cmds.textScrollList(self.weights_list, edit=True, removeAll=True)
            cmds.warning("get info failed")
            return
        else:

            # If the list has content, do not update to avoid overwriting search results
            if cmds.textScrollList(self.AlljointsName_list, query=True, allItems=True) == None:
                print("list updated")

                cmds.textScrollList(self.AlljointsName_list,
                                  edit=True, removeAll=True)
                cmds.textScrollList(self.AlljointsName_list,
                                  edit=True, append=info.all_influences)
            else:
                print("list no updated")
                print(cmds.textScrollList(self.AlljointsName_list, query=True, allItems=True))
                pass

            # if the UI already contains the same list; if so, pass, otherwise update
            check_temp = cmds.textScrollList(
                self.jointsName_list, query=True, allItems=True)
            if check_temp == info.display_inf_list:
                print("list elements is same, no update.")
                pass
            else:
                print("list updated")
                cmds.textScrollList(self.jointsName_list,
                                  edit=True, removeAll=True)
                cmds.textScrollList(self.jointsName_list,
                                  edit=True, append=info.display_inf_list)

            cmds.textScrollList(self.weights_list, edit=True, removeAll=True)
            cmds.textScrollList(self.weights_list, edit=True,
                              append=info.display_weights_list)


    def weight_plus_btn(self, ignoreInputs):
        """
        Increase the weight value of the selected joint.
        """

        self.edit_targets = []  

        # Query the current weight value and convert it to float
        get_text = cmds.textField(self.text_doublespin, query=True, text=True)
        get_number = float(get_text)

        # Fetch the selected influence name
        self.edit_targets = cmds.textScrollList(
            self.jointsName_list, query=True, selectItem=True)

        # Operate on the weight
        edit.weight_plus((self.edit_targets[0], get_number))

        # Update UI and reselect the object to avoid deselection
        self.update_ui()
        cmds.textScrollList(self.jointsName_list, edit=True,
                        selectItem=self.edit_targets[0])

        print(self.edit_targets, " + ", get_number)

    def weight_minus_btn(self, ignoreInputs):
        """
         Decrease the weight value of the selected joint.
        """

        self.edit_targets = [] 

        # Query the current weight value and convert it to float
        get_text = cmds.textField(self.text_doublespin, query=True, text=True)
        get_number = float(get_text)

        # Fetch the selected influence name
        self.edit_targets = cmds.textScrollList(
            self.jointsName_list, query=True, selectItem=True)

        # Operate on the weight (here by subtracting get_number)
        edit.weight_minus((self.edit_targets[0], get_number))

        # Update UI and reselect the object to avoid deselection
        self.update_ui()
        cmds.textScrollList(self.jointsName_list, edit=True,
                          selectItem=self.edit_targets[0])

        print(self.edit_targets, " - ", get_number)

    def _set_weight(self, value=float):
        self.edit_targets = []  

        # Fetch the selected influence name
        self.edit_targets = cmds.textScrollList(
            self.jointsName_list, query=True, selectItem=True)

        # Set the weight to 0
        edit.weight_set((self.edit_targets[0], value))

        # Update UI and reselect the object to avoid deselection
        self.update_ui()
        cmds.textScrollList(self.jointsName_list, edit=True,
                          selectItem=self.edit_targets[0])

        print(self.edit_targets, " set ", value)
    
    def weight_0_btn(self, ignoreInputs):

        self._set_weight(0.0)

    def weight_dot25_btn(self, ignoreInputs):
        
        self._set_weight(0.25)

    def weight_dot5_btn(self, ignoreInputs):
        
        self._set_weight(0.5)

    def weight_dot75_btn(self, ignoreInputs):
        
        self._set_weight(0.75)

    def weight_1_btn(self, ignoreInputs):
        
        self._set_weight(1.0)

    def weight_set_btn(self, ignoreInputs):

        # Query the current weight value and convert it to a float
        get_text = cmds.textField(self.text_doublespin, query=True, text=True)
        get_number = float(get_text)

        self._set_weight(get_number)

    def set_float_up(self, ignoreInputs):

        get_string = cmds.textField(self.text_doublespin, query=True, text=True)
        now_float = float(get_string)

        if now_float > 0.9999:
            cmds.textField(self.text_doublespin, edit=True, text="1.0")
            cmds.warning("weight must be 0 ~ 1 .")
        else:
            final_float = round(now_float + 0.01, 2)
            to_string = str(final_float)
            cmds.textField(self.text_doublespin, edit=True, text=to_string)
            print("float +", 0.1)

    def set_float_down(self, ignoreInputs):

        get_string = cmds.textField(self.text_doublespin, query=True, text=True)
        now_float = float(get_string)

        if now_float < 0.0001:
            cmds.textField(self.text_doublespin, edit=True, text="0.0")
            cmds.warning("weight must be 0 ~ 1 .")
        else:
            final_float = round(now_float - 0.01, 2)
            to_string = str(final_float)
            cmds.textField(self.text_doublespin, edit=True, text=to_string)
            print("float -", 0.1)

    def select_grow(self, ignoreInputs):
        cmds.GrowPolygonSelectionRegion()

    def select_shrink(self, ignoreInputs):
        cmds.ShrinkPolygonSelectionRegion()

    def weight_smooth_btn(self, ignoreInputs):
        edit.weight_smooth()
        self.update_ui()

    def weight_copy_btn(self, ignoreInputs):

        edit.weight_copy()

    def weight_paste_btn(self, ignoreInputs):

        edit.weight_paste()
        self.update_ui()

    def search_btn(self, ignoreInputs):

        
        get_string = cmds.textField(self.text_search, query=True, text=True)
        result = info.search_joints(get_string)

        cmds.textScrollList(self.AlljointsName_list, edit=True, removeAll=True)
        cmds.textScrollList(self.AlljointsName_list, edit=True, append=result)

    def append_btn(self, ignoreInputs):

        other_joint = cmds.textScrollList(
            self.AlljointsName_list, query=True, selectItem=True)
        now_list = cmds.textScrollList(
            self.jointsName_list, query=True, allItems=True)
        switch = False

        for joint in now_list:

            if other_joint[0] == joint:
                cmds.warning("the joint is already .")
                switch = False
                break
            else:
                switch = True

        if switch == True:
            
            cmds.textScrollList(self.jointsName_list,
                              edit=True, append=other_joint)

    def mirror_btn(self, ignoreInputs):

        edit.weight_mirror()
        self.update_ui()

    def prune_btn(self, ignoreInputs):

        get_string = cmds.textField(self.text_prune, query=True, text=True)
        to_float = float(get_string)

        edit.prune_weight(to_float)
        self.update_ui()

    def round_btn(self, ignoreInputs):

        get_num = cmds.textField(self.text_round, query=True, text=True)
        edit.round_weight(get_num)
        self.update_ui()


    def donate_page_btn(self, ignoreInputs):
        
        def _open_donation_site(*args):
            donation_url = r"https://sigenchang.bobaboba.me"
            webbrowser.open(donation_url)
                
        image_path = parent_directory + r"\BobaMe.png"
        
        donate_window_name = "donate_page"
        window_size = (600, 374)
        
        if cmds.window(donate_window_name, exists=True):
            cmds.deleteUI(donate_window_name, window=True)
            
        cmds.window(donate_window_name)
        donate_window = cmds.window(donate_window_name, edit=True, title="Donate Me !", widthHeight=window_size)
        
        cmds.columnLayout(adjustableColumn=True)
        bobame_btn = cmds.button(label="Give me a Boba !", backgroundColor=[0.933,0.843,0.761], command=_open_donation_site)
        cmds.image(image=image_path)
        
        cmds.showWindow(donate_window)
        
if __name__ == "__main__":
    ui = UI()
    ui.show_ui()
    ui.donate_page_btn()
    
else :
    pass