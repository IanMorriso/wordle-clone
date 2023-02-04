# Author: Ian Morrison
# Class: CMPUT 175
# This program imports our Scrabble Dictionary from our wordle assignment and provides the user with possible words.

from Wordle175 import ScrabbleDict

def main():
    """
    This method runs our hint generator  and returns nothing.
    :return: None
    """

    wordSize = 5
    fileName = 'scrabble5.txt'
    wordle = ScrabbleDict(wordSize, fileName)

    # Creates a template and wildcards based on user input, then displays hints based on those parameters
    template, letters = createTemplate(wordle)
    print(wordle.getMaskedWord(template))
    print(wordle.getConstrainedWords(template, letters))

    # Generates and displays statistics in regards to letter occurrence
    statistics, totalWords = getStatistics(wordle)
    displayStats(statistics, totalWords)

def createTemplate(wordle):
    """
    This method creates a template for which the program will search through our game dictionary to find matching words.
    The user must provide letters in positions where they know correct letters are placed, and wildcards '*' where
    there are missing letters.
    :param wordle: (ScrabbleDict) - Our custom dictionary class with game attributes.
    :return: tempalte (str) - A template for which to search matching words
             letters (list) - A list of user provided wildcard letters
    """

    valid = False
    print("To generate a hint, please enter 'Green' letters in their corresponding positions, and '*' as a wild card wherever there is a missing letter.")

    # Continues to prompt user for valid input. Catches expected errors
    while not valid:
        try:
            template = validateTemplate(wordle)
            letters = createWildCards(wordle, template)
        except Exception as e:
            print(e.args)
        else:
            valid = True

    letters = list(letters.lower())
    return template, letters

def validateTemplate(wordle):
    """
    This method validates our user's template for letters and wildcards '*', length and size by checking each character
    in the template.
    :param wordle: (ScrabbleDict) - Our custom dictionary class with game attributes.
    :return: template (str) - Validate user template
    """
    wildCard = '*'
    size = wordle.getWordSize()
    validCharacters = 'abcdefghijklmnopqrstuvwxyz*'
    template = input("Please enter a word template: ").lower()

    # Checks for length and valid characters
    if len(template) != wordle.getWordSize():
        raise Exception("Error. Incorrect word size.")
    elif wildCard not in template:
        raise Exception("Error. No wild cards in template.")
    for i in range(len(template)):
        if template[i] not in validCharacters:
            raise Exception("Error. Invalid characters.")

    return template

def createWildCards(wordle, template):
    """
    This method generates wildcards for the template by prompting the user for letter characters. The user can opt to
    input no letters, some, or all letters for the amount of wildcards in the template.
    :param wordle: (ScrabbleDict) - Our custom dictionary class with game attributes.
    :param template: (str) - User provided template
    :return: letters: (str) - Validated user chosen wildcards
    """

    count = template.count('*')
    valid = False
    letters = ''

    while not valid:

        # Prompts user for input for however many wildcards are in the template
        for i in range(count):
            try:
                letter = validateLetter()
            except Exception as e:
                i = i - 1
                print(e.args)
            else:
                letters = letters + letter

        valid = True

    return letters

def validateLetter():
    """
    This method validates the users input for wildcard values. Valid inputs are None and/or letter characters.
    :return: letter (str) - Validated wildcard value
    """
    letter = input("Please enter a letter to use as a wild card: ").lower()

    if len(letter)>1:
        raise Exception("Error. Please enter only one letter.")

    # Checks user input for letter or None value
    elif letter.isalpha() or letter != None:
        return letter

    else:
        raise Exception("Error. Please enter a letter.")

def getStatistics(wordle):
    """
    This method counts each occurrence of letters A through Z in our wordle dictionary, and well as the total letter in
    the dictionary. We do this by converting each letters A and Z into their ord() values so we can easily loop through
    the alphabetical range and count their occurrences and assign key/value pairs.
    Returns a dictionary of each letter and occurrence as key value pairs
    :param wordle: (ScrabbleDict) - Our custom dictionary class with game attributes.
    :return: statistics: (dict) - Dictionary of each letter and occurrence as key value pairs
             total: (int) - Total number of letters in our dictionary
    """
    total = 0
    words = wordle.words
    statistics = {}

    # This code block loops through the alphabet and assigns keys for each letter
    for i in range(ord('a'), ord('z')+1):
        value = 0
        key = chr(i)
        # This code block loops through each word in our dictionary and counts its occurrences and totals them
        for word in words:
            value += word.count(key)

        total += value
        statistics[key] = value

    return statistics, total

def displayStats(statistics, total):
    """
    This method displays formatted statistics for each letter and the percent likely-hood of its occurrence, along with
    a histogram with a '*' representing every rounded percent chance of it occurring.
    :param statistics: Dictionary of each letter and occurrence as key value pairs
    :param total: (int) - Total number of letters in our dictionary
    :return: None
    """

    char = '*'
    # Loops through key/value pairs in our statistics dictionary
    for key, value in statistics.items():
        percent = (value/total)*100
        rounded = round(percent)
        # Prints our formatted statistics
        print("{0}: {1:>4} {2:>6.2f}% {3}".format(key.upper(), value, percent, rounded*char))


main()