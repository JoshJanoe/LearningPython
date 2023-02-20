#!python

import random
from tkinter import *

def main():

	cards = ["red", "red", "red", "red", "red", "red",
			"orange", "orange", "orange", "orange", "orange", "orange", 
			"yellow", "yellow", "yellow", "yellow", "yellow", "yellow", 
			"green", "green", "green", "green", "green", "green", 
			"blue", "blue", "blue", "blue", "blue", "blue", 
			"purple", "purple", "purple", "purple", "purple", "purple", 
			"double red", "double red", "double red", "double red",
			"double orange", "double orange", "double orange",  
			"double yellow", "double yellow", "double yellow", "double yellow",
			"double green", "double green", "double green", 
			"double blue", "double blue", "double blue", "double blue",  
			"double purple", "double purple", "double purple", "double purple", 
			"peppermint", "gumdrop", "ice-cream cone", "chocolate", "lollipop"]
	used = []

	affirmative = ["y", "yes", "si", "yup", "yep", "yeah", "yea"]
	negative = ["n", "no", "nope", "nah"]

	players = 0

	playerList = []
	drawHistory = []
	playerHistory = {}

	currPlayer = 0

	while (True):
		print("How many players for this game? ")
		players = int(input())
		if (players < 1 or players > 4):
			print("Invalid number of players")
		else: break

	
		playerNum = x+1
		playerList.append("Player"+str(playerNum))
		print("Player"+str(playerNum)+" added")

	#THIS SECTION INCOMPLETE. 
	#NEED LOOP FOR NEGATIVE REPLY TO CORRECT NAME QUESTION?
	# print("Would you like to name the players?")
	# namePlayers = input()
	# if namePlayers.lower() in affirmative:
	# 	for x in range(players):
	# 		print("What would you like to call Player 1?")
	# 		playerName = input()
	# 		print("Is " + playerName + " correct?")
	# 		correctName = input()
	# 		if correctName in affirmative:
	# 			print("Player" + x + " name set to " + playerName)
	# 			playerList[x] = playerName
	# 			continue

	while (True):
		print("Draw a card? (y or n) ")
		answer = input()
		if answer.lower() in affirmative: 
			card = random.choice(cards)
			print(playerList[currPlayer]+"\'s card: " + card.upper())
			if (currPlayer < len(playerList)-1):
				currPlayer += 1
			else:
				currPlayer = 0		
			cards.remove(card)
			used.append(card)
			showStats(len(cards),len(used))

		if (len(cards) == 0): 
			print("Would you like to reshuffle the deck? ")
			reshuffle = input()
			if reshuffle.lower() in affirmative:
				cards = used
				used = []
				showStats(len(cards),len(used))
			if reshuffle.lower() in negative: break

		if answer.lower() in negative: break

	print("Thanks for playing!")	

def showStats(cards, used):
	print("\tRemaining cards: " + str(cards))
	print("\tUsed cards: " + str(used))
	print("--------------------------------")

if __name__ == "__main__":
    main()	
