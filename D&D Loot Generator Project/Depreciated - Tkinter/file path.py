import tkinter as tk
from tkinter import ttk
import pandas as pd
import random as rand
import openpyxl

# Function to simulate rolling dice
def dice(amount:int,sides:int):
    roll = 0
    for i in range(0,amount):
        die = rand.randint(1,sides)
        roll = roll + die
    return(roll)

# Function to find a specific character in a string
# Returns location or None if that character is not in the string
def string_finder(string:str,char:str):
    for pos in range(len(string)):
        if string[pos] == char:
            return(pos)
        elif pos == len(string):
            return(False)  

# Function to find the row index of a die roll within a table of ranges
# Returns column index within given column constraints    
def range_finder(roll_result:int,table_name:str,column_index:int,start_index:int,end_index:int):
    odds_list = table_name.iloc[start_index:end_index,column_index].tolist()
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

def center_screen(window,window_width:int,window_height:int):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width // 2) - (window_width // 2)
    y = (screen_height // 2) - (window_height // 2)
    window_geometry = f"{window_width}x{window_height}+{x}+{y}"
    return window_geometry

# Check to make sure everything is normal with the data files/first-time setup
try:
    app_info = pd.read_csv("App Info.csv")
    pd.read_excel(app_info.loc[0,"File Path"])

except (FileNotFoundError,KeyError,ValueError):
    # Create a new window with a text prompt
    get_path = tk.Tk()
    get_path.title("Locate Data")
    get_path.geometry(center_screen(get_path,210,50))

    # Save the user input in the txt file
    def insert_path(event=None):
        text = path_entry.get()
        # Build a new string for the file path letter by letter
        file_path = ""
        for letter in text:
            # Convert backslash from windows "copy path" command to forward slash that python uses
            if letter == "\\":
                file_path = file_path + "/"
            # Ignore quotation marks
            elif letter != "\"":
                file_path = file_path + letter
        
        # Check to make sure input works
        try:
            pd.read_excel(file_path)
            app_info = pd.DataFrame({"File Path":[file_path]})
            app_info.to_csv("App Info.csv",index=None)
            # Close window when successful
            get_path.destroy()
            
        except FileNotFoundError:
            instruct.config(text="File name not found. Try again, stupid.")

    get_path.rowconfigure(0,weight=1)
    get_path.columnconfigure(0,weight=1)
   
    center = tk.Frame(get_path)
    center.grid(row=0,column=0)

    instructions = "Enter the file path of the item tables."
    instruct = ttk.Label(center,text=instructions)
    instruct.grid(row=0,column=0,columnspan=2)

    path_entry = ttk.Entry(center)
    path_entry.grid(row=1,column=0,padx=3)
    path_entry.bind("<Return>",insert_path)

    insert_btn = ttk.Button(center,text="Insert",command=insert_path)
    insert_btn.grid(row=1,column=1)

    get_path.mainloop()

# Access the overall campaign data and file path for the item tables
app_info = pd.read_csv("App Info.csv")
file_path = app_info.loc[0,"File Path"]





magic_items = pd.read_excel(file_path,sheet_name='Magic Items List',header=None)
items = magic_items.iloc[:,0].tolist()

# Generate the window with primary functionality
main_window = tk.Tk()
main_window.title("Loot Generator")
main_window.geometry(center_screen(main_window,800,500))
main_window.bind("<Escape>",lambda event=None: main_window.destroy())



# Frame for Campaign Selection
camp_frame = tk.Frame(main_window)
camp_frame.grid(row=0,column=1)

# Get a list of the current campaigns
camp_list = app_info.columns[:0:-1].to_list()

# Function to open a new window to create a new campaign :)
def new_campaign(event=None):
    crnt_camp = tk.Tk()
    crnt_camp.title("New Campaign")
    crnt_camp.geometry(center_screen(crnt_camp,210,50))
    crnt_camp.bind("<Escape>",lambda event=None: crnt_camp.destroy())

    def create_camp(event=None):
        new_name = name_entry.get()
        if new_name:
            app_info[new_name] = None
            app_info.to_csv("App Info.csv",index=None)
            camp_select.insert(0,new_name)
            crnt_camp.destroy()

    instruct = ttk.Label(crnt_camp,text="Enter a new campaign name:")
    instruct.grid(row=0,column=0,columnspan=2,sticky='w',padx=3)

    name_entry = ttk.Entry(crnt_camp)
    name_entry.grid(row=1,column=0,padx=3)
    name_entry.bind("<Return>",create_camp)

    name_btn = ttk.Button(crnt_camp,text="Create",command=create_camp)
    name_btn.grid(row=1,column=1)

def delete_campaign(event=None):
    delete_index = camp_select.curselection()
    if delete_index:
        delete_name = camp_select.get(delete_index)
        app_info.drop(delete_name,axis=1,inplace=True)
        app_info.to_csv("App Info.csv",index=None)
        camp_select.delete(delete_index)

def select_campaign():
    if camp_select.curselection():
        # Set as a global variable so we can access wherever (OMG so illegal :O)
        global crnt_camp
        crnt_camp = camp_select.get(camp_select.curselection())
        return(crnt_camp)
    else:
        money_display.config(text="Select a Campaign")

# Label to display selected campaign name
camp_display = ttk.Label(camp_frame,text="Select a Campaign:")
camp_display.grid(row=1,column=0,columnspan=2)

# Selection box for current campaigns
camp_select = tk.Listbox(camp_frame,selectmode='single')
camp_select.grid(row=2,column=0,columnspan=2)
camp_select.bind("<ButtonRelease-1>",lambda event=None: camp_display.config(text=select_campaign()))
for i in range(0,len(camp_list)):
    camp_select.insert(i,camp_list[i])

# Button to create a new campaign
camp_new = ttk.Button(camp_frame,text="Create New",command=new_campaign)
camp_new.grid(row=3,column=0)

# Button to delete a campaign
camp_delete = ttk.Button(camp_frame,text="Delete",command=delete_campaign)
camp_delete.grid(row=3,column=1)

# Frame for duplicate item manipulation
dupe_frame = tk.Frame(main_window)
dupe_frame.grid(row=1,column=0)

# Function to gray out duplicate frame when that setting isn't selected
def disable_dupe_frame():
    if enable_dupe.get():
        state = 'normal'
        back_color = 'white'
        font_color = 'black'
    else:
        state = 'disabled'
        back_color = "#f0f0f0"
        font_color = "#a3a3a3"

    entry.config(state=state,background=back_color)
    item_list.config(bg=back_color,fg=font_color)
    display.config(foreground=font_color)
    enable_button.config(state=state)
    enabled_items.config(bg=back_color,fg=font_color)
    disable_btn.config(state=state)
    save_checkbox.config(state=state)

# Allows standard ctrl+bksp text deletion
def ctrl_bksp(event=None):
    text = entry.get()
    if text:
        text = text[::-1]
        for pos in range(len(text)):
            if text[pos] == " ":
                break
        index = len(text)-pos
        entry.delete(index,tk.END)

# Search in list for string input from user
def text_search(event=None):
    # ignore casing
    text = entry.get().casefold()

    if text:
        # create new list
        new_items = []
        # index every item in existing list
        for caps_item in items:
            # do not put item in the search box if it is already excluded
            excluded = False
            for excl_index in range(enabled_items.size()):
                if caps_item == enabled_items.get(excl_index):
                    excluded = True
                    break

            if excluded == False:
                # ignore casing
                item = caps_item.casefold()
                # initialize boolean
                match = False
                # index for every letter in item name
                for item_index in range(len(item)):
                    text_index = 0
                    # check if series of letters match beginning at starting letter
                    while item[item_index+text_index] == text[text_index]:
                        # if we successfully matched the entire text prompt
                        if text_index == len(text)-1:
                            match = True
                            break

                        elif item_index+text_index == len(item)-1:
                            break
                        # go to next letter in text prompt
                        text_index = text_index+1

                    # check if the item matches search
                    if match == True:
                        # add to new list of items
                        new_items = new_items + [caps_item]
                        break


        item_list.delete(0,tk.END)
        for item in new_items:
            item_list.insert(tk.END,item)

    # If the input field is empty, don't try to find a match just display everything
    else:
        item_list.delete(0,tk.END)
        for item in items:
            item_list.insert(tk.END,item)

# When an item is selected from list
def select_item(event=None):
    item_index = item_list.curselection()
    text_display = item_list.get(item_index)
    display.config(text=text_display)

# Moving an item to the exclusion list
def enable_item(event=None):
    if item_list.curselection():
        item_index = item_list.curselection()
        item_name = item_list.get(item_index)
        item_list.delete(item_index)
        enabled_items.insert(tk.END,item_name)

def disable_item(event=None):
    if enabled_items.curselection():
        item_index = enabled_items.curselection()
        enabled_items.delete(item_index)
        text_search()

# Text Entry for search
entry = ttk.Entry(dupe_frame)
entry.grid(row=1,column=0,columnspan=2,sticky='ew')
entry.bind("<Control-BackSpace>",ctrl_bksp)
entry.bind("<KeyRelease>",text_search)

# List of all of the magic items
item_list = tk.Listbox(dupe_frame,selectmode="single")
item_list.grid(row=2,column=0,columnspan=2,sticky='nesw')
item_list.bind("<ButtonRelease-1>",select_item)
for item in items:
    item_list.insert(tk.END,item)

# Scrollbar
scroll = ttk.Scrollbar(dupe_frame)
scroll.grid(row=2,column=2,sticky='ns')
#item_list.config(yscrollcommand = scroll.set)
#scroll.config(command = item_list.yview)

# Item Selection Display
display = ttk.Label(dupe_frame,text="Select an Item",width=50)
display.grid(row=3,column=0,sticky='ew')

# Select Enable Button
enable_button = ttk.Button(dupe_frame,text="Enable",command=enable_item)
enable_button.grid(row=3,column=1,sticky='e')

# List of Enabled Items
enabled_items = tk.Listbox(dupe_frame,selectmode="multiple")
enabled_items.grid(row=2,column=3,sticky='nesw')

# Button to Disable Items
disable_btn = ttk.Button(dupe_frame,text="Disable",command=disable_item)
disable_btn.grid(row=3,column=3,sticky='e')

# Checkbox to Enable or Disable Duplicate Item Settings
enable_dupe = tk.BooleanVar()
dupe_checkbox = ttk.Checkbutton(dupe_frame,text="Prevent Duplicate Items?",variable=enable_dupe,command=disable_dupe_frame)
dupe_checkbox.grid(row=0,column=0)

# Checkbox to Enable or Disable storing item information
enable_save = tk.BooleanVar()
save_checkbox = ttk.Checkbutton(dupe_frame,text="Save Items?",variable=enable_save)
save_checkbox.grid(row=0,column=1)

# Run function so frame is disabled by default
disable_dupe_frame()



# Frame for generating items
loot_frame = tk.Frame(main_window)
loot_frame.grid(row=0,column=0)

def loot_generator(from_csv):

    CR = cr_select.get()
    if CR == '17+':
        CR = 17
    else:
        CR = int(CR)

    enc = enc_select.get()

    if enc == 'Individual':
        money_string = None

        # Obtain individual encounter tables from Excel sheet
        indv_tables = pd.read_excel(file_path,sheet_name='Individual Treasure Tables')

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
            
            # Put coins into string
            if money_string == None:
                money_string = str(value) + str(denom)
            else:
                money_string = money_string + ", " + str(value) + str(denom)
            
            money_display.config(text=money_string)
            magic_display.config(text="")


    elif enc == "Hoard":
        money_string = None
        magic_string = None
        #crnt_camp = camp_select.get(camp_select.curselection())

        # Import Excel sheet containing treasure hoard data
        hoard_tables = pd.read_excel(file_path,sheet_name='Treasure Hoard Tables',header=None)

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
            
            # Put coins into string
            if money_string == None:
                money_string = str(value) + str(denom)
            else:
                money_string = money_string + ", " + str(value) + str(denom)

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
            money_string = money_string + ", " + str(val_amt) +"-"+ str(val_type)

        # Constrain loot table to just the magic items section
        magic_table = loot_table.iloc[3:,2:].reset_index(drop=True)

        # Obtain the Magic Item Tables from the Excel file
        magic_items = pd.read_excel(file_path,sheet_name='Magic Item Tables',index_col=0)

        # Preallocate a list to put the items into
        items = []

        # Prepare the duplicate items
        previous_items = from_csv.loc[:,crnt_camp].to_list()
        enabled_dupes = enabled_items.get(0,tk.END)

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

                    if enable_dupe == True or item in enabled_dupes:
                        # Duplicate item check to display as x2 or x3 etc
                        for check in items:
                            # Check if the list index already has a multiplier
                            x_loc = string_finder(check,'x')
                            
                            # Function returns None if the character is not present
                            if x_loc != None and check[x_loc-1] == ' ' and check[x_loc+1] == ' ':
                                # Determine the current count based on the number after the x
                                crnt_count = int(check[x_loc+1:])
                                # Reset to the string without the multiplier & space
                                base_string = check[:x_loc-1]

                            else:
                                crnt_count = 1
                                base_string = check

                            # Check if the rolled item is the same as the index
                            if item == base_string:
                                # Update the count by one
                                crnt_count = crnt_count+1
                                # Replace the item in it's place in the list
                                items[items.index(check)] = base_string + ' x' + str(crnt_count)
                                # Not necessary to append to the list if this is the case
                                local_dupe = True
                        # Only need to append list if item was not replaced
                        if local_dupe == False:
                            items.append(item)

                    # If the item should be ignored
                    elif item in previous_items:
                        # Reset the index as if this roll never happened
                        item_count = item_count - 1

                    # Normal item roll
                    else:
                        items.append(item)
                        previous_items.append(item)


        # Display every item in the list
        for item in items:
            if magic_string == None:
                magic_string = str(item)              
            else:
                magic_string = magic_string + ", " + str(item)
        money_display.config(text=money_string)
        magic_display.config(text=magic_string)

        new_column = pd.concat([from_csv.loc[:,crnt_camp].dropna(ignore_index=True),pd.Series(items)],ignore_index=True)
        if len(new_column) > len(from_csv):
            new_csv = from_csv.reindex(range(len(new_column)))

        elif len (new_column) < len(from_csv):
            new_column = new_column.reindex(range(len(from_csv)))
            new_csv = from_csv

        else:
            new_csv = from_csv

        new_csv[crnt_camp] = new_column

        # Update main document
        new_csv.to_csv("App Info.csv",index=None)



# Box to select challenge rating
cr_lbl = ttk.Label(loot_frame,text="Select CR:")
cr_lbl.grid(row=0,column=0)
cr_options = [i for i in range(17)]+['17+']
cr_select = ttk.Combobox(loot_frame,values=cr_options,width=5,)
cr_select.current(0)
cr_select.grid(row=0,column=1)

# Box to select encounter type
enc_lbl = ttk.Label(loot_frame,text="Select Encounter Type:")
enc_lbl.grid(row=0,column=2)
enc_options = ['Individual','Hoard']
enc_select = ttk.Combobox(loot_frame,values=enc_options,width=10)
enc_select.current(0)
enc_select.grid(row=0,column=3)

# Button to activate loot generator function
loot_btn = ttk.Button(loot_frame,text="Generate",command=lambda: loot_generator(app_info))
loot_btn.grid(row=0,column=4)
main_window.bind('<Return>',loot_generator)

# Display money
money_display = ttk.Label(loot_frame,text="Click \"Generate\" to get loot")
money_display.grid(row=1,column=0,columnspan=5)

# Display magic itemds
magic_display = ttk.Label(loot_frame)
magic_display.grid(row=2,column=0,columnspan=5)



main_window.mainloop()