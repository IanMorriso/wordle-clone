# CMPUT 175 Assignment 2
# Author: Ian Morrison
# This program runs our created Wordle game by importing classes from our Wordle175.py file.

from Wordle175 import ScrabbleDict, Game

def main():

    destination = "scrabble5.txt"
    targetFile = open(destination, 'r')
    size = 5

    dict = ScrabbleDict(size, destination)

    game = Game(size, dict)

    game.play()

main()