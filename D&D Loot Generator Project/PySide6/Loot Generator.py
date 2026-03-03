from PySide6.QtWidgets import QApplication, QMainWindow, QInputDialog, QMessageBox, QFrame,QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QLabel, QListWidget, QLineEdit, QPushButton, QCheckBox, QComboBox
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

            app_info = pd.DataFrame({"File Path":[file_path],"Enabled Duplicates":[None]})
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

        # This excel sheet cannot change during program operation
        items_df = pd.read_excel(file_path,sheet_name='Magic Items List',header=None)
        self.all_items = tuple(items_df.iloc[:,0].tolist())
        
        app_info = pd.read_csv("App Info.csv")
        self.enabled_items = app_info["Enabled Duplicates"].dropna().tolist()
        self.disabled_items = list(self.all_items)
        for item in self.enabled_items:
            self.disabled_items.remove(item)

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

        app_info = pd.read_csv("App Info.csv")
        column_data = self.enabled_items.copy()
        if len(column_data) > len(app_info):
            app_info = app_info.reindex(range(len(column_data)))
        elif len(column_data) < len(app_info):
            diff = len(app_info) - len(column_data)
            column_data = column_data + [None for i in range(diff)]

        app_info["Enabled Duplicates"] = column_data
        app_info = app_info.dropna(how='all')
        app_info.to_csv("App Info.csv",index=None)

        self.search_bar.complete_list = self.disabled_items
        self.search_bar.text_search()

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
        self.campaign_list = app_info.columns[2:].to_list()

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
            app_info.insert(loc=2, column=name, value=None)
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

class LootFrame(QFrame):
    def __init__(self,file_path:str):
        super().__init__()

        self.file_path = file_path
        self.active_campaign = None

        layout = QVBoxLayout(self)

        self.cr_label = QLabel("Select CR:")
        layout.addWidget(self.cr_label)

        self.cr_combobox = QComboBox()
        cr_list = [str(i) for i in range(16)] + ["17+"]
        self.cr_combobox.addItems(cr_list)
        layout.addWidget(self.cr_combobox)

        self.enc_label = QLabel("Select Encounter Type:")
        layout.addWidget(self.enc_label)

        self.enc_combobox = QComboBox()
        self.enc_combobox.addItems(["Individual","Hoard"])
        layout.addWidget(self.enc_combobox)

        self.run_button = QPushButton("Generate")
        self.run_button.clicked.connect(self.generate_loot)
        layout.addWidget(self.run_button)

        self.money_display = QListWidget()
        layout.addWidget(self.money_display)
        
        self.item_display = QListWidget()
        layout.addWidget(self.item_display)

    def refresh(self):
        self.money_display.clear()
        self.item_display.clear()

    @Slot(str)
    def update_campaign(self,active_campaign:str):
        self.active_campaign = active_campaign

    def generate_loot(self):
        def dice(amount:int,sides:int):
            roll = 0
            for i in range(0,amount):
                die = rand.randint(1,sides)
                roll = roll + die
            return(roll)
        
        def string_finder(string:str,char:str):
            for pos in range(len(string)):
                if string[pos] == char:
                    return(pos)
                elif pos == len(string):
                    return(False)
                
        def range_finder(roll_result:int,table:pd.DataFrame,column_index:int,start_index:int,end_index:int):
            odds_list = table.iloc[start_index:end_index,column_index].tolist()
            for row in range(len(odds_list)):
                odds = str(odds_list[row])
                hyphen_loc = string_finder(odds,'-')
                
                if hyphen_loc == None:
                    low = int(odds)
                    high = low
                else:
                    low = int(odds[0:hyphen_loc])
                    high = int(odds[hyphen_loc+1:len(odds)])

                if low <= roll_result <= high:
                    return row
                
        self.refresh()

        CR = self.cr_combobox.currentText()
        if CR == '17+':
            CR = 17
        else:
            CR = int(CR)

        enc = self.enc_combobox.currentText()

        money_list = []
        if enc == 'Individual':
            # Obtain individual encounter tables from Excel sheet
            indv_tables = pd.read_excel(self.file_path,sheet_name='Individual Treasure Tables')

            # Find indicies where all values are empty (these separate the tables on the excel sheet)
            sep = indv_tables[indv_tables.isnull().all(axis=1)].index.tolist()

            # Determine the range of indicies to pull from the table based the encounter's Challenge Rating
            if 0 <= CR <= 4:
                start = 0
                end = sep[0]
            elif 5 <= CR <= 10:
                start = sep[0]+1
                end = sep[1]
            elif 11 <= CR <= 16:
                start = sep[1]+1
                end = sep[2]
            else:
                start = sep[2]+1
                end = len(indv_tables)

            # Extract appropriate indicies from encounter table
            loot_table = indv_tables.iloc[start:end].reset_index(drop=True)

            # Roll a d100 to determine the row of the loot table to use
            loot_roll = dice(1,100)
            loot_index = range_finder(loot_roll,loot_table,0,0,len(loot_table))

            # Drop empty cells from loot table
            coin_table = loot_table.loc[loot_index,'cp':].dropna()
            for coin in coin_table:
                # Find location of 'd' and ' ' within the string
                d_loc = string_finder(coin,'d')
                space_loc = string_finder(coin,' ')

                # Extract the amount of dice to roll
                amt = int(coin[0:d_loc])

                # If there is no ' ' in the string (no multiplier)
                if space_loc == None:
                    # Extract the size of dice to roll
                    sides = int(coin[d_loc+1:])
                    value = dice(amt,sides)
                # If the string has a multiplier attatched
                else:
                    sides = int(coin[d_loc+1:space_loc])
                    mult = int((coin[space_loc+3:]))
                    value = dice(amt,sides)*mult
                
                # Extract the denomination of coin from loot table
                denom = coin_table.index[coin_table==coin][0] # for some reason this creates a list with the string and type so just pull the first part
                
                money_list.append(str(value) + str(denom))
                self.money_display.addItems(money_list)

        elif enc == "Hoard":
            # Import Excel sheet containing treasure hoard data
            hoard_tables = pd.read_excel(self.file_path,sheet_name='Treasure Hoard Tables',header=None)

            # Find indicies where all values are empty (these separate the tables on the excel sheet)
            sep = hoard_tables[hoard_tables.isnull().all(axis=1)].index.tolist()

            # Determine which table to use based on Challenge Rating
            if 0 <= CR <= 4:
                loot_table = hoard_tables.iloc[0:sep[0]]
            elif 5 <= CR <= 10:
                loot_table = hoard_tables.iloc[sep[0]+1:sep[1]]
            elif 11 <= CR <= 16:
                loot_table = hoard_tables.iloc[sep[1]+1:sep[2]]
            else:
                loot_table = hoard_tables.iloc[sep[2]+1:len(hoard_tables)]

            # Set table to base index values
            loot_table = loot_table.reset_index(drop=True)

            for coin_index in loot_table.iloc[1:2,1:].dropna(axis=1):
                coins = loot_table.iloc[1,coin_index]
                # Find location of 'd' and ' ' within the string
                d_loc = string_finder(coins,'d')
                space_loc = string_finder(coins,' ')

                # Extract the amount of dice to roll
                amt = int(coins[0:d_loc])

                # If there is no ' ' in the string (no multiplier)
                if space_loc == None:
                    # Extract the size of dice to roll
                    sides = int(coins[d_loc+1:])
                    value = dice(amt,sides)
                # If the string has a multiplier attatched
                else:
                    sides = int(coins[d_loc+1:space_loc])
                    mult = int((coins[space_loc+3:]))
                    value = dice(amt,sides)*mult
                
                # Extract the denomination of coin from loot table
                denom = loot_table.iloc[0,coin_index] # for some reason this creates a list with the string and type so just pull the first part
                
                money_list.append(str(value) + str(denom))

            items_table = loot_table.iloc[3:len(loot_table),0:2].reset_index(drop=True)
            loot_roll = dice(1,100)
            treasure_index = range_finder(loot_roll,items_table,0,0,len(items_table))

            # Isolate the gems/art objects column
            valuables = items_table.iloc[treasure_index,1]

            # There's a chance that the space is empty in this case so check for that
            if pd.isna(valuables) == False:

                # Find the location of "d" and the first space
                d_loc = string_finder(valuables,'d')
                space_loc = string_finder(valuables,' ')

                # Read the number and type of dice and the type of valuables
                amt = int(valuables[0:d_loc])
                sides = int(valuables[d_loc+1:space_loc])
                val_type = valuables[space_loc+1:len(valuables)]

                # Roll the number of gems or art objects in the hoard
                val_amt = dice(amt,sides)
                object_string = str(val_amt) +"-"+ str(val_type)
                money_list.append(object_string)
            
            self.money_display.addItems(money_list)

            # Constrain loot table to just the magic items section
            magic_table = loot_table.iloc[3:,2:].reset_index(drop=True)

            # Obtain the Magic Item Tables from the Excel file
            magic_items = pd.read_excel(self.file_path,sheet_name='Magic Item Tables',index_col=0)

            # Preallocate a list to put the items into
            items = []
            repeat_items = []

            # Prepare the duplicate items
            app_info = pd.read_csv("App Info.csv")
            if self.active_campaign:
                previous_items = app_info[self.active_campaign].dropna().to_list()
            else:
                previous_items = []
            
            enabled_dupes = app_info["Enabled Duplicates"].to_list()

            # For each column that magic items could be in
            for column in range(4):
                
                # Extract instructions for which table to use
                description = magic_table.iloc[treasure_index,column]

                # Detect if the index contains information or not
                NaN = magic_table.iloc[treasure_index].notna()
                
                # Only try to do something if there's something there :)
                if NaN.iloc[column] == 1:
                    # Check if just one roll ("Roll once")
                    if description[5] == 'o':
                        number_items = 1
                    
                    # Determine the number of items for each column
                    else:
                        d_loc = string_finder(description,'d')
                        t_loc = string_finder(description,'t')

                        amt = int(description[5:d_loc])
                        sides = int(description[d_loc+1:t_loc-1])
                        number_items = dice(amt,sides)
                    
                    # The particular table is at the end of the string so just index this
                    table = description[len(description)-1]
                    # Obtain the letter magic item table
                    crnt_magic_table = magic_items.loc[table].reset_index(drop=True)
                    
                    # Repeat for the number of items rolled
                    for item_count in range(number_items):
                        local_dupe = False
                        item_roll = dice(1,100) 
                        # Identify the particular item from the magic item table
                        item_index = range_finder(item_roll,crnt_magic_table,0,0,len(crnt_magic_table))
                        # Get item from table at determined index
                        item = crnt_magic_table.loc[item_index,'Name']

                        if item in enabled_dupes:
                            # Duplicate item check to display as x2 or x3 etc
                            for check in items:
                                # Check if the list index already has a multiplier
                                x_loc = string_finder(check,'x')
                                
                                # Function returns None if the character is not present
                                try:
                                    # Determine the current count based on the number after the x
                                    crnt_count = int(check[x_loc+1:])
                                    # Reset to the string without the multiplier & space
                                    base_string = check[:x_loc-1]
                                except (ValueError,TypeError):
                                    crnt_count = 1
                                    base_string = check

                                # Check if the rolled item is the same as the index
                                if item == base_string:
                                    crnt_count = crnt_count+1
                                    # Replace the item in it's place in the list
                                    items[items.index(check)] = base_string + ' x' + str(crnt_count)
                                    # Not necessary to append to the list if this is the case
                                    local_dupe = True

                            # Only need to append list if item was not replaced
                            if local_dupe == False:
                                repeat_items.append(item)

                        # If the item should be ignored
                        elif item in previous_items:
                            # Reset the index as if this roll never happened
                            item_count = item_count - 1

                        # Normal item roll
                        else:
                            items.append(item)


            # Display every item in the list
            self.item_display.addItems(items + repeat_items)

            if self.active_campaign:
                column_data = previous_items + items
                if len(column_data) > len(app_info):
                    app_info = app_info.reindex(range(len(column_data)))
                elif len(column_data) < len(app_info):
                    diff = len(app_info) - len(column_data)
                    column_data = column_data + [None for i in range(diff)]

                app_info[self.active_campaign] = column_data
                app_info = app_info.dropna(how='all')
                app_info.to_csv("App Info.csv",index=None)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        app_info = pd.read_csv("App Info.csv")
        self.file_path = app_info.loc[0,"File Path"]

        self.setWindowTitle("Loot Generator")
        container = QWidget()
        layout = QHBoxLayout(container)

        self.setCentralWidget(container)

        left_stack = QVBoxLayout()

        self.duplicates_checkbox = QCheckBox("Allow Duplicates?")
        self.duplicates_checkbox.toggled.connect(self.toggle_duplicate_frame)
        left_stack.addWidget(self.duplicates_checkbox)

        # Duplicate Item Container
        self.duplicate_frame = DuplicateFrame(self.file_path)
        left_stack.addWidget(self.duplicate_frame)

        layout.addLayout(left_stack)

        # Campaign Selection Container
        self.campaign_frame = CampaignFrame()
        layout.addWidget(self.campaign_frame)

        # Code Execution Container
        self.loot_frame = LootFrame(self.file_path)
        layout.addWidget(self.loot_frame)

        self.campaign_frame.campaignUpdated.connect(self.loot_frame.update_campaign)
        self.campaign_frame.select_campaign()

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