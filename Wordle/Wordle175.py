# CMPUT 175 Assignment 2
# Author: Ian Morrison
# This program contains our ADT's so we can operate our Wordle game.
# ScrabbleDict contains our methods related to creating the dictionary, as well as
# selecting words out of the dictionary.
# Game is where Wordle is played, and runs until the correct word is guessed or
# until 5 guesses are completed.

import random

class ScrabbleDict:
    """
    ScrabbleDict contains our methods related to creating the dictionary, as well as
    selecting words out of the dictionary. It is initialized based off of a given word size and filename
    to source our words.

    ATTRIBUTES:
        self.size: (int) - length of words in dictionary
        self.words: (dict) - Dictionary of words used in game

    METHODS:
        check(): Checks if provided word is in dictionary
        getSize(): Gets the total number of words in the dictionary
        selectWord(): Selects word at given index
        getWordSize(): Gets the size of words in the dictionary
        getMaskedWord(): Gets a list of words that follow a user provided template
        getConstrainedWords(): Gets a list of words that follow a user provided template and contain provided
                               wildcard letters
    """
    def __init__(self, size, filename):
        """
        This function initializes our dictionary of words to be used in our Wordle game by reading words
        from a provided file and creating a dictionary for them.
        :param size: (int) - Length of word for our Wordle game
        :param filename: (str) - Filename of the file containing the words for our Wordle game
        """

        self.size = size

        self.words = {}
        txtfile = open(filename)

        for line in txtfile:
            key = line[:self.size]
            value = line
            self.words[key] = value.strip()


    def check(self, word):
        """
        This function checks to see if a chosen word is in our dictionary. Returns True if the word
        is in our dictionary and false otherwise.
        :param word: (str) - Word to check in dictionary
        :return: True if word is in dictionary, False otherwise
        """
        if word in self.words.keys():
            return True
        else:
            return False

    def getSize(self):
        """
        This function returns the total number of words in the dictionary
        :return: Total (int) - Total number of words in dictionary
        """
        return len(self.words)

    def getWords(self, letter):
        """
        This function searches for all words in the dictionary that begin with selected
        letter and returns them as a list
        :param letter: (string) - Letter to search words beginning with
        :return: sortedWords (list) - List of words beginning with selected letter
        """
        sortedWords = []
        for key in self.words:
            char = key[0]
            if char == letter:
                sortedWords.append(key)
        return sortedWords

    def selectWord(self, index):
        """
        This function selects the word at a given index
        :param index: (int) - Random integer used to select word from our dictionary.
        :return:
        """

        keyList = list(self.words)
        word = keyList[index]

        return word


    def getWordSize(self):
        """
        This is a getter function and returns the length of words stored in the dictionary
        :return: self.size (int) - Length of words used in dictionary
        """
        return self.size

    def getMaskedWord(self, template):
        """
        This function searches through our dictionary for words that have matching letters in the positions
        provided by the user provided template and returns them as a list
        :param template: (str) - This is our user provided template for which we search our dictionary for matching
         words. Returns a list of words matching our template.
        :return: words : (list) - This is a list of words that match our template
        """

        words = []
        match = True

        # This searches all words in our dictionary and finds words that match our given template
        for key in self.words:
            for i in range(len(key)):

                # If the template does not have a '*', we check to see if the character matches any words in our dictionary.
                if template[i]!= '*':

                    # If any character does not match, match is set to false
                    if template.lower()[i] != key[i]:
                        match = False

            # If our template matches a word, we add it to our list of words.
            if match == True:
                words.append(key)
            match = True

        return words

    def getConstrainedWords(self, template, letters):
        """
        This function gets a list of constrained words from our word dictionary using the parameters of the user
        provided template and letters.
        Constrained words must include all uses of letters provided in place of wild cards in the template. If there
        are less letters than there are wild cards, other letters will take their place.
        :param template: (str) - User validated template to search for possible hint words
        :param letters: (str) - User validated letters to fill in for template wildcards
        :return: constrainedWords: (list) - List of all potential words given template and letters
        """
        constrainedWords = []
        words = self.getMaskedWord(template)

        # Here we loop through all words in our given template
        for word in words:
            match = True
            wildcards = letters.copy()
            wildcardCount = template.count('*')

            # This loop checks each letter in the template for a '*'.
            # If there is a wildcard and the word has a letter from letters in the same location as the wild card,
            # we remove the letter from the pool.
            for i in range(len(template)):
                if template[i] == '*':
                    if word[i] in str(wildcards):
                        wildcards.remove(word[i])
                        wildcardCount -= 1

                    # If the letter does not match, the word won't meet our conditions
                    else:
                        match = False

            # If we run out of letters before wild cards, the word will be appended.
            if wildcardCount > 0 and len(wildcards) == 0:
                match = True

            if match == True:
                constrainedWords.append(word)

        return constrainedWords

class Game():
    """
    This class handles the operation of our Wordle game. The game finishes after 5 unsuccessful guesses, or when
    the correct word is guessed.

    ATTRIBUTES:
        self.continueGame: (bool) - State of game
        self.correctGuess: (bool) - State of current guess
        self.size: (int) - Size of words in dictionary
        self.guesses: (list) - List of previous guesses
        self.dict: (ScrabbleDict) - Custom dictionary of words and methods used for our game

    METHODS:
        getWord(): Generates a random number between 0 and max words in dictionary, then selects that word at the given
                   index of the dictionary
        play(): Plays the Wordle game by selecting a random word. The user has 5 guesses to select the correct word,
                otherwise, they lose.
        getInput(): Prompts user for guess word.
        inputValidation(): Validates user's guess word for correct characters and length
        match(): Determines whether user's guess is a match, otherwise, sorts letters from guess into green for correct
                 letter and placement, orange for correct letter, or red for incorrect letter.
        findDuplicates(): Searches guess word for duplicate letters. If duplicates found, it assigns ascending numbers
                          to the letters in order of appearance in the word.
        checkContinue(): Checks to see if any of the end game conditions are met (correct guess, or 5 attempts).
    """

    def __init__(self, size, dict):
        """
        This function initializes our Game class with the word size and dictionary provided.
        :param size:
        :param file:
        """

        self.continueGame = True
        self.correctGuess = False
        self.attemptCount = 1
        self.size = size
        self.guesses = []
        self.dict = dict

    def getWord(self):
        """
        This method finds the word in our dictionary with user provided index by converting our dictionary into a list.
        Returns a (str) word.
        :return: word (str) - Word at the given index
        """

        max = self.dict.getSize()
        number = random.randint(0, max)
        word = self.dict.selectWord(number)

        return word

    def play(self):
        """
        This method controls the playing of our game. It keeps track of previous guesses, selects our random word, and
        continues the game until the correct word has been guess or until 5 incorrect guesses have been inputted.
        :return: None
        """

        word = self.getWord()
        guessList = []

        # Continues the game while condition is true
        while self.continueGame:

            # Gets our guess from the user, checks it and adds to attempt count
            guess = self.getInput(self.attemptCount)
            outcome = self.match(guess.lower(), word)
            self.attemptCount += 1

            # Checks our game status, then appends our guesses if needed
            self.continueGame = self.checkContinue(self.attemptCount)
            guessList.append(outcome)

            # Prints our previous guesses
            for i in guessList:
                print(i)

        if not self.correctGuess:
            print("Sorry you lose. The Word is " + word.upper())


    def getInput(self, attempt):
        """
        This function prompts user for word guess and returns a validated input
        :param attempt: (int) - Attempt number
        :return: input: (str) - Validated user input
        """

        valid = False
        while not valid:
            guess = input("Attempt " + str(attempt) + ": Please enter a " + str(self.size) + "-letter word:")
            guess = guess.lower()
            valid = self.inputValidator(guess)

        return guess


    def inputValidator(self, guess):
        """
        This function validates user input for correct length and whether-or-not the word is in our dictionary
        :param guess: (str) - User's guess to validate
        :return: Returns True if guess is valid, False otherwise
        """
        guess = guess.upper()
        if len(guess) > self.size:
            print(guess + " is too long")
            return False

        elif len(guess) < self.size:
            print(guess + " is too short")
            return False

        elif not self.dict.check(guess.lower()):
            print(guess + " is not a recognized word")
            return False

        elif guess in self.guesses:
            print(guess + " was already entered")

        else:
            return True

    def match(self, guess, answer):
        """
        This method analyzes our user's guess. We check for correct guess and letters in correct position by comparing
        the guess and answer directly. We check for correct letters in incorrect position by checking if the letter is
        in the word, but not in the same position. We check for incorrect letters by comparing each letter to see if
        it is in the answer. Returns formatted outcome.
        :param guess:
        :param answer:
        :return:
        """

        index = 0
        green = []
        orange = []
        red = []
        chars = []

        print(answer, guess)
        # Checks if the guess is correct
        if guess.lower() == answer.lower():
            print("Found in " + str(self.attemptCount) + " attempts. Well done. The word is " + answer.upper())
            self.correctGuess = True

        for char in answer:
            chars.append(char.upper())

        # Finds duplicate letters in guess
        guessLetters = self.findDuplicates(guess)

        # This code block checks for correct/incorrect letters as well as correct/incorrect positions, then appends them
        # in appropriate lists
        index = 0
        for letter in guessLetters:
            letter = letter.upper()
            if letter[:1] == chars[index]:
                green.append(letter)
            if letter[:1] in chars and letter[:1] != chars[index]:
                orange.append(letter)
            if letter[:1] not in chars:
                red.append(letter)


            index += 1

        outcome = "{0} Green={1} Orange={2} Red={3}".format(guess.upper(), green, orange, red)
        return outcome

    def findDuplicates(self, guess):
        """
        This method finds duplicate letters in a users guess by counting each occurrence of a letter in the guess. If a
        letter appears more than once, ascending numbers beginning with 1 are added to the string value of the letter,
        with each occurrence of the given letter a higher number.
        :param guess:
        :return:
        """
        index = 0
        guessLetters = []

        # Creates a list of characters in the user's guess
        for char in guess:
            guessLetters.append(char)


        for i in guessLetters:
            base = 1  # Starts off the base occurrence of a letter as 1
            if guessLetters.count(i) > 1:
                for c in guessLetters:
                    # Loops through each letter in the guess, looking for each occurrence of a letter that occurs more
                    # than once, then adds the number of times it has occured so far to the letter
                    if i == c:
                        count = i + str(base % (guess.count(i)+1))
                        guessLetters[index] = count
                        base += 1
                    index += 1
                index = 0

        return guessLetters

    def checkContinue(self, attempts):
        """
        This method checks the state of the game and whether it should continue or not. If the attempts go over 5 or
        the correct answer has been guessed, this will return False, otherwise it returns True.
        :param attempts:
        :return:
        """

        if attempts > 5 or self.correctGuess:
            return False
        else:
            return True

if __name__ == "__main__":
    wordle = ScrabbleDict(5, "scrabble5.txt")

    letters = ['i']
    template = "T**ER"
    print(wordle.check('board'))
    print(wordle.getSize())
    print(wordle.getWords('b'))
    print(wordle.getWordSize())