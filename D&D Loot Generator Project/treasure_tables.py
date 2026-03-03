import pandas as pd
import random as rand
import openpyxl

# Function to simulate rolling dice
def dice(amount,sides):
    roll = 0
    for i in range(0,amount):
        die = rand.randint(1,sides)
        roll = roll + die
    return(roll)

# Function to find a specific character in a string
# Returns location or False if that character is not in the string
def string_finder(string,char):
    for pos in range(len(string)):
        if string[pos] == char:
            return(pos)
        elif pos == len(string):
            return(False)

# Get challenge rating and type of encounter from user
CR = int(input("Enter Challenge Rating: "))
enc = input("Choose treasure type: I (individual) or H (hoard) ")

if enc == 'I':
    # Import Excel sheet containing individual table data
    indv_tables = pd.read_excel('C:/Users/Anderson/Documents/DnD_data.xlsx',sheet_name='Individual Treasure Tables') #make this a one time input?

    # Find indicies where all values are empty (these separate the tables on the excel sheet)
    sep = indv_tables[indv_tables.isnull().all(axis=1)].index.tolist()

    # Determine which table to use based on Challenge Rating
    if 0 <= CR <= 4:
        loot_table = indv_tables.iloc[0:sep[0]]
    elif 5 <= CR <= 10:
        loot_table = indv_tables.iloc[sep[0]+1:sep[1]]
    elif 11 <= CR <= 16:
        loot_table = indv_tables.iloc[sep[1]+1:sep[2]]
    elif CR > 16:
        loot_table = indv_tables.iloc[sep[2]+1:len(indv_tables)]
    else:
        print("Error: Please enter a positive CR.")

    # Set table to base index values
    loot_table = loot_table.reset_index(drop=True)

    # Roll a d100 to determine which row of table to use
    loot_roll = dice(1,100)
    print("roll:",loot_roll)

    # Search loot table for row that matches d100 roll
    for loot_row in range(len(loot_table)):
        # Access the column with the odds in it
        odds = loot_table.loc[loot_row,'d100']

        # Find index where hyphen is located - this separates low value from high value
        hyphen_loc = string_finder(odds,'-')

        # Extract the low and high dice values from the d100 column
        low = int(odds[0:hyphen_loc]) #the end of the slice is exclusive, so if hyphen_loc == 1: low = just the first index
        high = int(odds[hyphen_loc+1:len(odds)])
        
        # Finally determine if roll was inside range for a given row
        if low <= loot_roll <= high:
            treasure_index = loot_row
            break

    # Limit the data to the columns with dice in them
    money_table = loot_table.loc[loot_row,['cp','sp','ep','gp','pp']].dropna()

    # Configure data into a list
    coins = [money_table.iloc[i]+'a'+money_table.index[i] for i in range(0,len(money_table))]

    # Break each value into its denominational components (may just be one)
    for coin in coins:
        # Find location of 'd' within each string
        d_loc = string_finder(coin,'d')

        # Extract the amount of dice to be rolled
        amt = int(coin[0:d_loc])

        # Use the location of the space (if it exists) to extract the # of sides and multiplier
        space_loc = string_finder(coin,' ')
        a_loc = string_finder(coin,'a')
        if space_loc == None: #func string_finder returns False if that character does not exist
            sides = int(coin[d_loc+1:a_loc])
            mult = 1
        else:
            sides = int(coin[d_loc+1:space_loc])
            mult = int(coin[space_loc+3:a_loc])

        # Roll the amount of each denomination that appears
        money = dice(amt,sides)*mult
        
        # extract the name of the coin (cp,sp,etc) from the string
        coin_name = coin[a_loc+1:len(coin)]

        # display loot for each type of coin
        print(str(money)+' '+coin_name)

elif enc == 'H':
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

    # remove columns from first two rows that do not have coins in them
    money_table = loot_table.iloc[0:2,1:len(loot_table)].dropna(axis=1)

    # create a list for each type of coin with the dice and name with an arbitrary character (~) to separate them
    coins = [money_table.iloc[1,i]+'~'+money_table.iloc[0,i] for i in range(0,len(money_table.iloc[0,:]))]

    # loop for each different type of coin in table
    for coin in coins:
        # extract amount of dice from indicies before 'd'
        d_loc = string_finder(coin,'d')
        amt = int(coin[0:d_loc])
        
        # find indicies for ' ' and '~' in string
        space_loc = string_finder(coin,' ')
        name_loc = string_finder(coin,'~')

        # check if there is a multiplier to use (default in treasure hoard but someone could edit it out for some reason)
        if space_loc == None: #func string_finder returns False if that character does not exist
            sides = int(coin[d_loc+1:name_loc])
            mult = 1
        else:
            sides = int(coin[d_loc+1:space_loc])
            mult = int(coin[space_loc+3:name_loc])

        # roll the dice to recieve your prize!
        money = dice(amt,sides)*mult

        # extract the name of the coin (cp,sp,etc) from the string
        coin_name = coin[name_loc+1:len(coin)]

        # display loot for each type of coin
        print(str(money)+' '+coin_name)

    items_table = loot_table.iloc[3:len(loot_table),0:2].reset_index(drop=True)

    # Roll a d100 to determine which row of table to use
    loot_roll = dice(1,100)

    # Search loot table for row that matches d100 roll
    for loot_row in range(len(items_table)):
        # Access the column with the odds in it
        odds = items_table.iloc[loot_row,0]

        # Find index where hyphen is located - this separates low value from high value
        hyphen_loc = string_finder(odds,'-')

        # If the range is a single value, then just check if it matches the roll
        if hyphen_loc == None:
            if loot_roll == int(odds):
                treasure_index = loot_row
                break

        else:
            # Extract the low and high dice values from the d100 column
            low = int(odds[0:hyphen_loc]) #the end of the slice is exclusive, so if hyphen_loc == 1 then low = just the first index
            high = int(odds[hyphen_loc+1:len(odds)])
            
            # Finally determine if roll was inside range for a given row
            if low <= loot_roll <= high:
                treasure_index = loot_row
                break

    # Isolate the gems/art objects column
    valuables = items_table.iloc[treasure_index,1]

    # Find the location of "d" and the first space
    d_loc = string_finder(valuables,'d')
    space_loc = string_finder(valuables,' ')

    # Read the number and type of dice and the type of valuables
    amt = int(valuables[0:d_loc])
    sides = int(valuables[d_loc+1:space_loc])
    val_type = valuables[space_loc+1:len(valuables)]

    # Roll the number of gems or art objects in the hoard
    amt = dice(amt,sides)
    print(amt,val_type)

    magic_table = loot_table.iloc[3:,2:].reset_index(drop=True)
    magic_row = magic_table.iloc[treasure_index,:]
    magic_items = pd.read_excel('C:/Users/Anderson/Documents/DnD_data.xlsx',sheet_name='Magic Item Tables',index_col=0)

    for column in range(4):
        description = magic_table.iloc[treasure_index,column]
        NaN = magic_table.iloc[treasure_index].notna()
        if NaN.iloc[column] == 1:
            if description[5] == 'o':
                number_items = 1
            
            else:
                d_loc = string_finder(description,'d')
                t_loc = string_finder(description,'t')

                amt = int(description[5:d_loc])
                sides = int(description[d_loc+1:t_loc-1])
                number_items = dice(amt,sides)
            
            table = description[len(description)-1]
            crnt_magic_table = magic_items.loc[table].reset_index(drop=True)
            
            
            for i in range(number_items):
                item_roll = dice(1,100)  

                for row in range(len(crnt_magic_table)):
                    odds = crnt_magic_table.loc[row,'d100']
                    
                    hyphen_loc = string_finder(odds,'-')

                    if hyphen_loc == None:
                        low = int(odds)
                        high = int(odds)

                    else:
                        low = int(odds[0:hyphen_loc])
                        high = int(odds[hyphen_loc+1:len(odds)])

                    if low <= item_roll <= high:
                        item_index = row
                        break
                
                item = crnt_magic_table.loc[item_index,'Name']
                print(item)


else:
    print("Enter I or H stupid it's literally not hard at all")