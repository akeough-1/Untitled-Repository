import random as rand
sides = 6
amount = 5

roll = 0
for i in range(0,amount):
    die = rand.randint(1,sides)
    print("roll:",die)
    roll = roll + die

print("total:",roll)