# Cmput 175 Assignemnt 2
# Author: Ian Morrison
# This program 'cleans' the corrupted file provided, then translates and writes it to a file as data for our wordle dictionary

def main():
    """
    This runs our cleaning program for which we take the 'corrupted' file and translate it into usable data for our
    dictionary.
    :return: None
    """
    fileName = "word5Dict.txt"
    destination = "scrabble5.txt"
    targetFile = open(destination, 'w')
    size = 5

    content = readFile(fileName)
    writeFile(targetFile, content)

def readFile(read):
    """
    This function reads information from target file and returns it in a list. We read the file and strip any whitespace
    on each line, along with any trailing '#'. Then we join each word with a '\n' so we can easily write it to a file
    later on.
    :param read: (str) This is the file name to read
    :return: content: (list) This is a list of words from the file
    """
    content = []
    words = []
    char = '#'

    with open(read) as file:
        for line in file:
            line = line.strip()
            line = line.rstrip('#')
            words = line.split('#')
            if '\n' in words:
                words.remove('\n')
            content += words
        content = '\n'.join(content)


    return content


def writeFile(file, content):
    """
    This function writes information from a list to a target file
    :param file: (str) - This is the file name to write to
    :param content: (list) - This contains all the information to write to target file
    :return: None
    """

    file.writelines(content)
    file.close()


main()