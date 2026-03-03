import pandas as pd
import random as rand
items = pd.read_csv('C:/Users/Anderson/Documents/DnD_Items.csv')

# Filter items where "Cost" is not NaN
nonmagic = items[items["Cost"].notna()]

# Filter items that don't have a loot table value
magic = items[items["d100"].notna()]


#Treasure_Table = input("Enter I for Individual or H for Hoard: ")
#Cr = int(input("Enter Challenge Rating: "))
Treasure_Table = "I"
Cr = 1


# definitely need a function to roll dice
def dice(amount,sides):
    roll = 0
    for i in range(0,amount):
        die = rand.randint(1,sides)
        roll = roll + die
    return(roll)

# Individual Treasure Tables (Just money in Rules as Written)
if Treasure_Table == "I":

    def indv_table(table):
        d100_roll = dice(1,100)
        for low , high , (amount , sides , multiplier , coin) , (amount2 , sides2 , multiplier2 , coin2) in table:
            if low <= d100_roll <= high:
                treasure = [dice(amount,sides)*multiplier + dice(amount2,sides2)*multiplier2, coin , coin2] #come back to this lol
                break
        return(treasure)

    if 0 <= Cr <= 4:
        loot_table = [
            #(bounds , (# of dice , number of sides , multiplier , denomination) , (secondary))
            (1  , 30 , (5 , 6 ,  1 , "cp") , (0 , 0 ,  0 , "  ")),
            (31 , 60 , (4 , 6 ,  1 , "sp") , (0 , 0 ,  0 , "  ")),
            (61 , 70 , (6 , 6 ,  5 , "sp") , (0 , 0 ,  0 , "  ")), #normally ep but that's gross
            (71 , 95 , (3 , 6 ,  1 , "gp") , (0 , 0 ,  0 , "  ")),
            (96 , 100, (1 , 6 ,  1 , "pp") , (0 , 0 ,  0 , "  "))
        ]
    elif 5 <= Cr <= 10:
        loot_table = [
            #(bounds , (# of dice , number of sides , multiplier , denomination) , (secondary))
            (1  , 30 , (4 , 6 , 100, "cp") , (1 , 6 , 50 , "sp")),
            (31 , 60 , (6 , 6 , 10 , "sp") , (2 , 6 , 10 , "gp")),
            (61 , 70 , (3 , 6 , 50 , "sp") , (2 , 6 , 10 , "gp")),
            (71 , 95 , (3 , 6 , 10 , "gp") , (0 , 0 ,  0 , "  ")),
            (96 , 100, (2 , 6 , 10 , "gp") , (3 , 6 ,  0 , "pp"))
         ]
    elif 11 <= Cr <= 16:
        loot_table = [
            #(bounds , (# of dice , number of sides , multiplier , denomination) , (secondary))
            (1  , 20 , (4 , 6 , 100, "sp") , (1 , 6 , 100, "gp")),
            (21 , 35 , (1 , 6 , 500, "sp") , ())
        ]
    else:
        loot_table = [

        ]
        
    treasure = indv_table(loot_table)

print(treasure)

        



# create a function to sort items with the DataFrame rules once you know what you need because it's really annoying

# ur gonna need to make a sheet containing all of the spells lol get rekt