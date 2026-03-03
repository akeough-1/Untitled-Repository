from PySide6.QtWidgets import QApplication, QMainWindow, QInputDialog, QMessageBox, QFrame,QWidget, QVBoxLayout, QGridLayout, QLabel, QListWidget, QLineEdit, QPushButton, QCheckBox
from PySide6.QtCore import Qt, Signal, Slot

import pandas as pd
import random as rand
import openpyxl

class QSearchBar(QLineEdit):
    queryUpdated = Signal(list)

    def __init__(self, item_list:list):
        super().__init__()

        self.complete_list = item_list
        self.query_list = item_list

        self.textChanged.connect(self.text_search)
    
    def clear(self):
        super().clear()
        self.text_search()

    def text_search(self):
        # ignore casing
        text = self.text().casefold() # -> lowercase str

        if text:
            # create new list
            query_list = []
            # index every item in existing list
            for format_item_name in self.complete_list:              
                # ignore casing
                item_name = format_item_name.casefold()
                # initialize boolean
                match = False
                # index for every letter in item name
                for item_index in range(len(item_name)):
                    text_index = 0
                    # check if series of letters match beginning at starting letter
                    while item_name[item_index+text_index] == text[text_index]:
                        # if we successfully matched the entire text prompt
                        if text_index == len(text)-1:
                            match = True
                            break

                        elif item_index+text_index == len(item_name)-1:
                            break
                        # go to next letter in text prompt
                        text_index = text_index+1

                    # check if the item matches search
                    if match == True:
                        # add to new list of items
                        query_list = query_list + [format_item_name]
                        break
        
            self.query_list = query_list
        
        else:
            self.query_list = self.complete_list

        self.queryUpdated.emit(self.query_list)

class FilePathWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("App Info")
        container = QWidget()
        layout = QGridLayout(container)
        
        self.setCentralWidget(container)

        self.instructions = QLabel("Enter File Path:")
        layout.addWidget(self.instructions,0,0)

        self.line_edit = QLineEdit()
        layout.addWidget(self.line_edit,1,0,1,2)

        self.accept_button = QPushButton("Enter")
        self.accept_button.clicked.connect(self.verify_file_path)
        layout.addWidget(self.accept_button,2,0)

        self.clear_button = QPushButton("Clear")
        self.clear_button.clicked.connect(lambda: self.line_edit.clear())
        layout.addWidget(self.clear_button,0,1)

        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.clicked.connect(lambda: self.close())
        layout.addWidget(self.cancel_button,2,1)

    def verify_file_path(self):
        path_text = self.line_edit.text() # ->str
        try:
            file_path = ""
            for letter in path_text:
                # Convert backslash from app.windows "copy path" command to forward slash that python uses
                if letter == "\\":
                    file_path = file_path + "/"
                # Ignore quotation marks
                elif letter != "\"":
                    file_path = file_path + letter

            pd.read_excel(file_path)

            app_info = pd.DataFrame({"File Path":[file_path]})
            app_info.to_csv("App Info.csv",index=None)

            app.window = MainWindow()
            app.window.show()
            self.close()

        except FileNotFoundError:
            self.instructions.setText("File Not Found. Try Again:")

class DuplicateFrame(QFrame):
    def __init__(self, file_path:str):
        super().__init__()

        layout = QVBoxLayout(self)

        self.non_dupe_label = QLabel("Non-Duplicateable Items:")
        layout.addWidget(self.non_dupe_label)

        self.active_campaign = None

        # This excel sheet cannot change during program operation
        items_df = pd.read_excel(file_path,sheet_name='Magic Items List',header=None)
        self.disabled_items = items_df.iloc[:,0].tolist()
        self.all_items = tuple(self.disabled_items)
        self.enabled_items = []

        self.search_bar = QSearchBar(item_list=list(self.all_items))
        self.search_bar.queryUpdated.connect(self.search)
        layout.addWidget(self.search_bar)

        self.clear_button = QPushButton("clear")
        self.clear_button.clicked.connect(lambda: self.search_bar.clear())
        layout.addWidget(self.clear_button)

        self.non_dupe_items = QListWidget()
        layout.addWidget(self.non_dupe_items)

        self.enable_button = QPushButton("Enable Duplicate")
        self.enable_button.clicked.connect(self.enable_duplicate)
        layout.addWidget(self.enable_button)

        self.dupe_label = QLabel("Duplicateable Items:")
        layout.addWidget(self.dupe_label)

        self.dupe_items = QListWidget()
        layout.addWidget(self.dupe_items)

        self.disable_button = QPushButton("Disable Duplicate")
        self.disable_button.clicked.connect(self.disable_duplicate)
        layout.addWidget(self.disable_button)

        self.refresh()

    def refresh(self):
        self.disabled_items.sort()
        self.non_dupe_items.clear()
        self.non_dupe_items.addItems(self.disabled_items)
    
        self.enabled_items.sort()
        self.dupe_items.clear()
        self.dupe_items.addItems(self.enabled_items)

        if self.active_campaign:
            app_info = pd.read_csv("App Info.csv")
            column_data = self.enabled_items
            if len(column_data) > len(app_info):
                app_info = app_info.reindex(range(len(column_data)))
            elif len(column_data) < len(app_info):
                diff = len(app_info) - len(column_data)
                column_data = column_data + [None for i in range(diff)]

            app_info[self.active_campaign] = column_data
            app_info = app_info.dropna(how='all')
            app_info.to_csv("App Info.csv",index=None)

        self.search_bar.complete_list = self.disabled_items
        self.search_bar.text_search()

    @Slot(str)
    def update_campaign(self,campaign_name:str):
        if campaign_name:
            self.active_campaign = campaign_name
            app_info = pd.read_csv("App Info.csv")

            self.disabled_items = list(self.all_items)
            self.enabled_items = app_info[campaign_name].dropna().tolist()
            for item in self.enabled_items:
                self.disabled_items.remove(item)

        else:
            self.active_campaign = None
            self.disabled_items = list(self.all_items)
            self.enabled_items = []

        self.refresh()

    @Slot(list)
    def search(self,query_items:list):
        self.non_dupe_items.clear()
        self.non_dupe_items.addItems(query_items)

    def enable_duplicate(self):
        if self.non_dupe_items.currentItem():
            item_name = self.non_dupe_items.currentItem().text()
            self.enabled_items.append(item_name)
            self.disabled_items.remove(item_name)

            self.refresh()

    def disable_duplicate(self):
        if self.dupe_items.currentItem():
            item_name = self.dupe_items.currentItem().text()
            self.disabled_items.append(item_name)
            self.enabled_items.remove(item_name)

            self.refresh()

class CampaignFrame(QFrame):
    campaignUpdated = Signal(str)

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)

        self.selection_label = QLabel("Select a Campaign")
        layout.addWidget(self.selection_label)

        self.campaign_select = QListWidget()
        self.campaign_select.itemClicked.connect(self.select_campaign)
        layout.addWidget(self.campaign_select)

        self.create_button = QPushButton("create new")
        self.create_button.clicked.connect(self.create_new_campaign)
        layout.addWidget(self.create_button)

        self.delete_button = QPushButton("delete")
        self.delete_button.clicked.connect(self.delete_campaign)
        layout.addWidget(self.delete_button)

        self.refresh()
        self.campaign_select.setCurrentRow(0)
        self.select_campaign()

    def refresh(self):
        app_info = pd.read_csv("App Info.csv")
        self.campaign_list = app_info.columns[1:].to_list()

        self.selection_label.setText("Select a Campaign")
        self.campaign_select.clear()
        self.campaign_select.addItems(self.campaign_list)

    def select_campaign(self):
        selection = self.campaign_select.currentItem()
        if selection:
            selection = selection.text()
            self.campaign = selection
            self.selection_label.setText(selection)
            self.campaignUpdated.emit(selection)

    def create_new_campaign(self):
        text, ok = QInputDialog.getText(self,"New Campaign","Enter the new campaign name:")
        if ok:
            name = text
            app_info = pd.read_csv("App Info.csv")
            app_info.insert(loc=1, column=name, value=None)
            app_info.to_csv("App Info.csv",index=None)

            self.campaign_list.insert(0,name)
            self.campaign_select.insertItem(0,name)
            self.campaign_select.setCurrentRow(0)
            self.select_campaign()

    def delete_campaign(self):
        reply = QMessageBox.question(self,"Delete Campaign","Are you sure you want to delete this campaign? It will be removed forever.",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            app_info = pd.read_csv("App Info.csv")
            selection = self.campaign_select.currentItem()
            self.campaign_select.takeItem(self.campaign_select.row(selection))
            app_info.drop(selection.text(),axis=1,inplace=True)
            app_info.to_csv("App Info.csv",index=None)

            self.campaignUpdated.emit(None)
            self.refresh()



class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        app_info = pd.read_csv("App Info.csv")
        self.file_path = app_info.loc[0,"File Path"]

        self.setWindowTitle("Loot Generator")
        container = QWidget()
        layout = QVBoxLayout(container)

        self.setCentralWidget(container)

        self.duplicates_checkbox = QCheckBox("Allow Duplicates?")
        self.duplicates_checkbox.toggled.connect(self.toggle_duplicate_frame)
        layout.addWidget(self.duplicates_checkbox)

        # Duplicate Item Container
        self.duplicate_frame = DuplicateFrame(self.file_path)
        layout.addWidget(self.duplicate_frame)

        #Campaign Selection Container
        self.campaign_frame = CampaignFrame()
        self.campaign_frame.campaignUpdated.connect(self.duplicate_frame.update_campaign)
        self.campaign_frame.select_campaign()
        layout.addWidget(self.campaign_frame)

    def toggle_duplicate_frame(self):
        if self.duplicates_checkbox.isChecked():
            self.duplicate_frame.setEnabled(False)
        else:
            self.duplicate_frame.setEnabled(True)





# Ok start the code sequence here
app = QApplication()
try:
    app_info = pd.read_csv("App Info.csv")
    pd.read_excel(app_info.loc[0,"File Path"])
    app.window = MainWindow()
    app.window.show()

except (FileNotFoundError,KeyError,ValueError):
    app.window = FilePathWindow()
    app.window.show()
    # This creates a new App Info file in place of whatever exists
    

app.exec()