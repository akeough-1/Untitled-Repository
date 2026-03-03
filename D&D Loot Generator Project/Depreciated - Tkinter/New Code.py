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
        odds = odds_list[row]
        hyphen_loc = string_finder(odds,'-')
        
        if hyphen_loc == None:
            low = int(odds)
            high = low
        else:
            low = int(odds[0:hyphen_loc])
            high = int(odds[hyphen_loc+1:len(odds)])

        if low <= roll_result <= high:
            return row

# for now just randomize challenge rating
CR = rand.randint(1,20)

enc = 'indv'

if enc == 'indv':
    # Obtain individual encounter tables from Excel sheet
    indv_tables = pd.read_excel('C:/Users/Anderson/Documents/DnD_data.xlsx',sheet_name='Individual Treasure Tables')

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
    elif CR > 16:
        start = sep[2]+1
        end = len(indv_tables)
    else:
        print("Error: Please enter a positive CR.")

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
        print(value,denom)

if enc == "hoard":
    # Import Excel sheet containing treasure hoard data
    hoard_tables = pd.read_excel('C:/Users/Anderson/Documents/DnD_data.xlsx',sheet_name='Treasure Hoard Tables',header=None)

    # Find indicies where all values are empty (these separate the tables on the excel sheet)
    sep = hoard_tables[hoard_tables.isnull().all(axis=1)].index.tolist()

    # Determine which table to use based on Challenge Rating
    if 0 <= CR <= 4:
        loot_table = hoard_tables.iloc[0:sep[0]]
    elif 5 <= CR <= 10:
        loot_table = hoard_tables.iloc[sep[0]+1:sep[1]]
    elif 11 <= CR <= 16:
        loot_table = hoard_tables.iloc[sep[1]+1:sep[2]]
    elif CR > 16:
        loot_table = hoard_tables.iloc[sep[2]+1:len(hoard_tables)]
    else:
        print("Error: Please enter a positive CR.")

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
        print(val_amt,val_type)

    # Constrain loot table to just the magic items section
    magic_table = loot_table.iloc[3:,2:].reset_index(drop=True)

    # Grab the row according to the index already determined by the gems/art objects
    magic_row = magic_table.iloc[treasure_index,:]

    # Obtain the Magic Item Tables from the Excel file
    magic_items = pd.read_excel('C:/Users/Anderson/Documents/DnD_data.xlsx',sheet_name='Magic Item Tables',index_col=0)

    # Preallocate a list to put the items into
    items = []
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
            for i in range(number_items):
                dupe = False
                item_roll = dice(1,100) 
                # Identify the particular item from the magic item table
                item_index = range_finder(item_roll,crnt_magic_table,0,0,len(crnt_magic_table))
                # Get item from table at determined index
                item = crnt_magic_table.loc[item_index,'Name']

                # Duplicate item check to display as x2 or x3 etc
                for check in items:
                    # Check if the list index already has a multiplier
                    x_loc = string_finder(check,'x')
                    
                    # Function returns None if the character is not present
                    if x_loc != None:
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
                        dupe = True
                # Only need to append list if item was not replaced
                if dupe == False:
                    items.append(item)

    # Display every item in the list
    for item in items:
        print(item)