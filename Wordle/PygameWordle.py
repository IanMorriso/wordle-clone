import random

class ScrabbleDict:
    def __init__(self, size, filename):
        self.size = size
        self.words = {}
        with open(filename) as txtfile:
            for line in txtfile:
                for word in line.strip().split('#'):
                    if len(word) == size:
                        self.words[word] = True

    def check(self, word):
        return word in self.words

    def getSize(self):
        return len(self.words)

    def selectWord(self, index):
        return list(self.words.keys())[index]

    def getWordSize(self):
        return self.size

class Game:
    def __init__(self, size, dict):
        self.size = size
        self.dict = dict
        self.word = "probe"#self.getWord()
        self.guesses = []
        self.correctGuess = False

    def getWord(self):
        index = random.randint(0, self.dict.getSize() - 1)
        return self.dict.selectWord(index)
    
    def inputValidator(self, guess):
        print(self.guesses)
        if not self.dict.check(guess.lower()):
            print(guess + " is not a recognized word")
            return guess + " is not a recognized word"

        elif any(g[0] == guess for g in self.guesses):
            print(guess + " was already entered")
            return guess + " was already entered"

        else:
            #self.guesses.append(guess)
            return ""

    def play(self):
        pass  # This method will not be used in Pygame version

    def match(self, guess):
        result = []
        for i in range(self.size):
            if guess[i] == self.word[i]:
                result.append('green')
            elif guess[i] in self.word:
                result.append('orange')
            else:
                result.append('red')
        if guess == self.word:
            self.correctGuess = True
        return result

    def add_guess(self, guess):
        print("guess added ", len(self.guesses))
        self.guesses.append(guess)

    def is_correct_guess(self):
        return self.correctGuess

    def get_guesses(self):
        return self.guesses