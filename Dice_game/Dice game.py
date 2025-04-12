#GCSE Computer Science NEA project code for June 2020 Series
#Kuba Kane

import time
import random

print("Welcome to this two-player dice game created by Kuba Kane!")
print("Please note that this game requires both players to register.")
enter = input("Press enter to begin.")
print()

#Authenitcation

global player
player = ""

playerOne = ""
playerTwo = ""

def newUser():
    global username
    print("Please create a username and password below.")
    time.sleep(1)
    username = input("Username: ")
    password = input("Password: ")
    
    exist = True
    try:
        f=open(username+".txt")
        f.close
    except FileNotFoundError:
        exist = False

    if exist == False:
        file = open(username+".txt", "w")
        file.write(username+":"+password)
        file.close
        print("Thanks for registering! ")
        
        
    else:
        while exist == True:
            print("Username already exists")
            again=input("Try again? (y/n): ")
            while again != "y" and again != "n":
                print("Please enter only 'y' or 'n'")
                again=input("Try again? (y/n): ")
            if again == "y":
                if player == "1":
                    print()
                    displayMenu()
                    break
                elif player == "2":
                    print()
                    displayMenu2()
                    break
            else:
                print("Exiting game")
                quit()

                    

def oldUser():
    global username1
    print("Please login below")
    username1 = input("Username: ")
    password1 = input("Password: ")
    
    exist1 = True
    try:
        f=open(username1+".txt")
        f.close
    except FileNotFoundError:
        exist1 = False

    if exist1 == True:
        file1 = open(username1+".txt", "r")
        data=file1.readline()
        file1.close()
        if (username1+":"+password1) == data:
            print("Login successful")
        else:
            print("Login unsuccessful")
            while exist1 == True:
                again2 = input("Try again? (y/n): ")
                while again2 != "y" and again1 != "n":
                    print("Please enter only 'y' or 'n'")
                    again2=input("Try again? (y/n): ")
                if again2 == "y":
                    if player == "1":
                        print()
                        displayMenu()
                        break
                    elif player == "2":
                        print()
                        displayMenu2()
                        break
                else:
                    print("Exiting game")
                    quit()
    else:
        while exist1 == False:
            print("User doesn't exist.")
            again1 = input("Try again? (y/n): ")
            while again1 != "y" and again1 != "n":
                print("Please enter only 'y' or 'n'")
                again1=input("Try again? (y/n): ")
            if again1 == "y":
                if player == "1":
                    print()
                    displayMenu()
                    break
                elif player == "2":
                    print()
                    displayMenu2()
                    break
            else:
                print("Exiting game")
                quit()

            
def displayMenu():
    global playerOne
    global player
    player = "1"
    print("-----------PLAYER ONE------------")
    print("Do you already have an account?")
    print("Press y for yes, n for no, or q to quit")
    status = input("")
    print()
    while status != "y" and status != "n" and status != "q":
        print("Invalid input - You must only press y, n or q")
        print("Do you already have an account?")
        status = input("")
        print()

    if status == "n":
        newUser()
        playerOne = username
    elif status == "y":
        oldUser()
        playerOne = username1
    elif status == "q":
        print("Exiting game.")
        quit()


def displayMenu2():
    global playerTwo
    global player
    player = "2"
    print()
    print("-----------PLAYER TWO------------")
    print("Do you already have an account?")
    print("Press y for yes, n for no, or q to quit")
    status = input("")
    print()
    while status != "y" and status != "n" and status != "q":
        print("Invalid input - You must only press y, n or q")
        print("Do you already have an account?")
        status = input("")
        print()

    if status == "n":
        newUser()
        playerTwo = username
    elif status == "y":
        oldUser()
        playerTwo = username1
    elif status == "q":
        print("Exiting game.")
        quit()

displayMenu()
displayMenu2()

if playerOne == playerTwo:
    while playerOne == playerTwo:
        print()
        print("Sorry, two seperate users must log in.")
        print("The second player must log in again.")
        playerTwoAgain = input("Do you want to continue? - Note that not doing so will end the game - (y/n): ")
        while playerTwoAgain != "y" and playerTwoAgain != "n":
            print()
            print("You must only enter y or n.")
            playerTwoAgain = input("Do you want to continue or quit? (y/n): ")
        if playerTwoAgain == "y":
            print()
            print("-----------PLAYER TWO------------")
            print("Do you already have an account?")
            print("Press y for yes, n for no, or q to quit")
            status = input("")
            print()
            while status != "y" and status != "n" and status != "q":
                print("Invalid input - You must only press y, n or q")
                print("Do you already have an account?")
                status = input("")
                print()
                
            if status == "n":
                newUser()
                playerTwo = username
                break
            elif status == "y":
                oldUser()
                playerTwo = username1
                break
            elif status == "q":
                print("Exiting game.")
                quit()
        else:
            print("Exiting game.")
            quit()
    

#Dice roll

print()
print()
print("Both players are now successfully logged in!")
rules = input("Do you want to see the game rules? (y/n): ")

while rules != "y" and rules != "n":
    print()
    print("You must only enter y or n")
    rules = input("Do you want to see the game rules? (y/n): ")
    
if rules == "y":
    print()
    time.sleep(2)
    print("GAME RULES")
    print("1. Each player gets to roll two dice each, in the 5 rounds")
    print("2. If you roll a double, you can roll a third die")
    print("3. If your total score for the round is an even number, 10 points are added to your score")
    print("4. If your total score for the round is an odd number, 5 points are deducted from your score")
    print("5. A player cannot have a score below 0")
    print("5. The player with the highest score at the end of the 5 rounds wins")
    print("6. If both players have the same score at the end of the 5 rounds, they each roll 1 die until the highest point wins")
    print()
    end = input("Press enter to continue the game")


def diceRoll():
    for x in range(6):
        rollOne = random.randint(1,6)
    return rollOne

def rollScore():
    rollOneInput = input("Press enter to roll the first die")
    rollOne = diceRoll()
    print("You rolled a",rollOne, "!")
    rollTwoInput = input("Press enter to roll the second die")
    rollTwo = diceRoll()
    print("You rolled a",rollTwo, "!")
    score = rollOne + rollTwo
    if rollOne == rollTwo:
        print()
        print("You've rolled a double! You get to roll one extra die!")
        rollThreeInput = input("Press enter to roll the die")
        rollThree = diceRoll()
        print("You rolled a", rollThree)
        score = score + rollThree
        
    if score % 2 == 0:
        score = score+10
    else:
        score = score-5

    if score < 0:
        score = 0
    return score
    

    
time.sleep(1.5)

roundScore = 0
roundScore2 = 0
playerOneScore = 0
playerTwoScore = 0

for x in range(1,6):
    print()
    print("ROUND", x)
    print()
    
    print(playerOne+ ", its your turn!")
    roundScore = rollScore()
    playerOneScore = playerOneScore + roundScore 
    time.sleep(1.5)
    print("Your total score for this round, "+playerOne+", is...",roundScore)
    time.sleep(2)

    print()
    print(playerTwo+ ", you're up!")
    roundScore2 = rollScore()
    playerTwoScore = playerTwoScore + roundScore2 
    time.sleep(1.5)
    print("Your total score for this round, "+playerTwo+", is...",roundScore2)
    time.sleep(2)
    
    x=x+1

#Calculating winner, or, if its a tie, finding the winner by rolling one die

winner = ""

if playerOneScore == playerTwoScore:
    print()
    print("You tied! You both scored", playerOneScore)
    print("For a tie-breaker, both players must roll a dice again.")
    time.sleep(1.5)
    
    print()
    print(playerOne+ ", its your turn!")
    roll = input("Press enter to roll the first die")
    rollTie = diceRoll()
    print("You rolled a",rollTie, "!")
    
    print()
    print(playerTwo+ ", its your turn now!")
    roll = input("Press enter to roll the first die")
    rollTie2 = diceRoll()
    print("You rolled a",rollTie2, "!")
    while rollTie == rollTie2:
        print("You tied again! Have another go...")
        print()
        print(playerOne+ ", its your turn!")
        roll = input("Press enter to roll the first die")
        rollTie = diceRoll()
        print("You rolled a",rollTie, "!")
    
        print()
        print(playerTwo+ ", its your turn now!")
        roll = input("Press enter to roll the first die")
        rollTie2 = diceRoll()
        print("You rolled a",rollTie2, "!")
    if rollTie > rollTie2:
        print()
        print(playerOne+" wins!")
        winner = playerOne
        winnerScore = playerOneScore
    else:
        print()
        print(playerTwo+" wins!")
        winner = playerTwo
        winnerScore = playerTwoScore
elif playerOneScore > playerTwoScore:
    print()
    print(playerOne+" wins with a total score of",playerOneScore,"while "+playerTwo+" had a total score of",playerTwoScore)
    winner = playerOne
    winnerScore = playerOneScore
elif playerTwoScore > playerOneScore:
    print()
    print(playerTwo+" wins with a total score of",playerTwoScore,"while "+playerOne+" had a total score of",playerOneScore)
    winner = playerTwo
    winnerScore = playerTwoScore
        

#leaderboard


x = 0
Name = ""
Score = ""

text_file = open("leaderboard.txt","a")

def write_in_file(x,y):
    global text_file
    text_file.write(x+" | "+y)
    text_file.write("\n")
    text_file.close()
    text_file = open("leaderboard.txt", "a")

Name = winner
Score = str(winnerScore)
write_in_file(Name, Score)


leaderboardOption = input("Do you want to see the leaderboard of winners? (y/n)")


while leaderboardOption != "y" and leaderboardOption != "n":
    print()
    print("You must only enter y or n")
    leaderboardOption = input("Do you want to see the leaderboard of winners? (y/n)")

if leaderboardOption == "y":
    print("Ok, this is the leaderboard...")
    time.sleep(2)
    print()
    text_file = open("leaderboard.txt", "r")
    print(text_file.read())
    text_file.close()
else:
    print("Ok.")

time.sleep(2)
print("Thanks for playing this dice game made by Kuba Kane. Hope you enjoyed playing it :)")







