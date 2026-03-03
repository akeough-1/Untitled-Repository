import pandas as pd
import numpy as np
import openpyxl

def string_finder(string:str,char:str):
    for pos in range(len(string)):
        if string[pos] == char:
            return(pos)
        elif pos == len(string):
            return(False)

indv_tables = pd.read_excel('C:/Users/Anderson/Documents/DnD_data.xlsx',sheet_name='Individual Treasure Tables')
new_tables = indv_tables.copy()

new_tables.rename(columns={"d100":"low"},inplace=True)
new_tables.insert(1,"high",np.nan)

insert_index = [i for i in range(3,16,3)]
label_list = ["_amt","_size","_mult"]

for coin_num in range(0,5):
    coin_name = indv_tables.columns[1+coin_num]

    for label_num in range(0,3):
        label = label_list[label_num]
        column_num = insert_index[coin_num]+label_num

        new_tables.insert(column_num,coin_name+label,np.nan)

    loot_column = indv_tables.loc[:,coin_name].tolist()
    for loot_index in range(len(loot_column)):
        loot_dice = loot_column[loot_index]
        if pd.notna(loot_dice)==True:
            d_loc = string_finder(loot_dice,'d')
            x_loc = string_finder(loot_dice,'x')

            amt = loot_dice[0:d_loc]

            if x_loc:
                size = loot_dice[d_loc+1:x_loc-1]
                mult = loot_dice[x_loc+1:]

            else:
                size = loot_dice[d_loc+1:]
                mult = 1

            dice_info = [amt,size,mult]
            for label_num in range(0,3):
                new_tables.loc[loot_index,coin_name+label_list[label_num]] = dice_info[label_num]

    del new_tables[coin_name]


indv_tables.to_csv("C:/Users/Anderson/OneDrive/Documents/Python/tables/Individual Tables",index=False)



magic_item_list = pd.read_excel('C:/Users/Anderson/Documents/DnD_data.xlsx',sheet_name='Magic Items List')
magic_item_list.to_csv("C:/Users/Anderson/OneDrive/Documents/Python/tables/Magic Item List",index=False,header=False)



magic_item_tables = pd.read_excel('C:/Users/Anderson/Documents/DnD_data.xlsx',sheet_name='Magic Item Tables',index_col=0)

magic_item_tables.rename(columns={"d100":"low"},inplace=True)
magic_item_tables.insert(1,"high",np.nan)

tables_sep = sep = magic_item_tables[magic_item_tables.isnull().all(axis=1)].index.tolist()
magic_item_tables.drop(tables_sep)

for index in magic_item_tables.index:
    dice_range = magic_item_tables.loc[index,"low"]
    if pd.notna(dice_range)==True:
        hyphen_loc = string_finder(dice_range,'-')
        if hyphen_loc:
            low = dice_range[0:hyphen_loc]
            high = dice_range[hyphen_loc+1:]

            magic_item_tables.loc[index,"low"] = low
            magic_item_tables.loc[index,"high"] = high
        
        else:
            magic_item_tables.loc[index,"low"] = dice_range
            magic_item_tables.loc[index,"high"] = dice_range

magic_item_tables.to_csv("C:/Users/Anderson/OneDrive/Documents/Python/tables/Magic Item Tables")



hoard_tables = pd.read_excel('C:/Users/Anderson/Documents/DnD_data.xlsx',sheet_name='Treasure Hoard Tables',header=None)
