#!/usr/bin/env python

import random
from tkinter import *

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

affirmative = ["y", "yes", "si", "yup", "yep", "yeah", "yea", "ya"]
negative = ["n", "no", "nope", "nah", "na"]
draw = ["d", "draw", "dr"]
restart = ["r", "re", "restart"]
end = ["e", "end", "exit"]
options = ["o", "opt", "options"]
history = ["h", "hist", "history"]
drawHistory = []
playerHistory = {}

inProgress = False

counter = 0

def main():

	global cards, used, counter, inProgress

	if not inProgress:
		playerList = setup()
	inProgress = True
	numPlayers = len(playerList)
	currPlayer = 0

	while (True):
		currPlayer = playerList[counter]
		
		#expand program with multiple actions: draw, restart, end, view history, etc
		print("Choose and action: [D]raw, View [H]istory, [R]estart, [O]ptions, or [E]xit")
		action = input()
		action = action.lower()
		if action in draw:
			drawCard(currPlayer, numPlayers)

		elif action in history:
			viewHistory()

		elif action in restart:
			restartGame()

		elif action in options:
			viewOptions()

		elif action in end:
			endGame()

		elif action == "fe":
			endGame("x")

		else: continue

		# #current working draw only version
		# print("Draw a card? (y or n) ")
		# answer = input()
		# if answer.lower() in affirmative: 
		# 	drawCard(currPlayer, numPlayers)

		# if (len(cards) == 0): 
		# 	print("Would you like to reshuffle the deck? ")
		# 	reshuffle = input()
		# 	if reshuffle.lower() in affirmative:
		# 		cards = used
		# 		used = []
		# 		showStats(len(cards),len(used))
		# 	if reshuffle.lower() in negative: break

		# if answer.lower() in negative: break

def showStats(cards, used):
	print("\tRemaining cards: " + str(cards))
	print("\tUsed cards: " + str(used))
	print("--------------------------------")

def setup(): 
	playerList = []
	while (True):
		print("How many players for this game? ")
		players = input()
		if (int(players) < 1 or int(players) > 4 or players.isalpha()):
			print("Invalid number of players")
		else: 
			players = int(players)
			break

	playersNamed = False
	while (not playersNamed):
		print("Would you like to name the players?")
		namePlayers = input()
		if namePlayers.lower() in affirmative:
			for x in range(players):
				correctName = "n"
				while correctName in negative:
					print("What would you like to call Player " + str(x+1) + "?")
					playerName = input()
					print("Is '" + playerName + "' correct?")
					correctName = input()
					if correctName in affirmative:
						print("Player" + str(x+1) + " name set to '" + playerName + "'")
						playerList.append(playerName)
						print(playerName + " added to game")
			playersNamed = True

		if namePlayers.lower() in negative:
			for x in range(players):
				playerNum = x+1
				playerList.append("Player"+str(playerNum))
				print("Player"+str(playerNum)+" added to game")
			playersNamed = True
	print("--------------------------------")

	return playerList

def drawCard(currPlayer, numPlayers):
	global cards, used, counter

	card = random.choice(cards)
	print(currPlayer+"'s card: " + card.upper())
	if (counter < numPlayers-1):
		counter += 1
	else:
		counter = 0		
	cards.remove(card)
	used.append(card)
	drawHistory.append(currPlayer + ": " + card)
	if currPlayer in playerHistory:
		playerHistory[currPlayer] = playerHistory[currPlayer] + ", " + card
	else:
		playerHistory[currPlayer] = card
	showStats(len(cards),len(used))
	return card

def viewHistory():
	#global used, playerHistory
	print("[I]ndividual players, or [F]ull history. ")
	opt = input().lower()
	if opt == "i":
		for player in playerHistory:
			print(player + ": " + playerHistory[player])
	if opt == "f":
		count = 1
		for card in used:
			print("Card " + str(count) + ": " + card)
			count += 1

def viewOptions():
	print("No options at this time")

def restartGame():
	if verify():
		global inProgress
		for card in used:
			cards.append(card)
		inProgress = False
		main()

def endGame(force):
	if force == "x":
		quit()
	if verify():
		print("Thanks for playing!")
		quit()

def verify():
	print("Are you sure?")
	ans = input()
	if ans in affirmative:
		return True

if __name__ == "__main__":
    main()	
