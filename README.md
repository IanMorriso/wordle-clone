# wordle-clone

* Wordle Clone

Wordle Clone is a fully functioning version of the popular word puzzle game, "Wordle", built in Python.

In Wordle Clone, you will need to guess a 5-letter word, within 5 attempts to win!

Features:
If you incorrectly guess the 5-letter word, the terminal will display which letters were incorrect.
* If a letter in the guessed word was in the correct place, it will show up in the **Green** list.
* If a letter in the guessed word is in the target word, but in the incorrect position, it will show up in the **ORANGE** list.
* If any letter in the guessed word is not in the target word, it will show up in the **RED** list.
* **Note:** If there are more that one of the same letter in the word, each letter will have a sequential number assicated with it, beginning from the first occurance, to the last.


I have also implimented a 'hint.py' file, which is designed to be run in conjuction with the main game when you feel stuck.
* For each missing letter in your guessed word, input an '*'. This acts as a **wild card**, and will be filled in with any possible letters that can make up a valid word.
* For each letter in the correct position, input it into the template.
* Any blank spaces or empty inputs will defalt to a **wild card**
* Based on your input, the terminal will siplay a list of every word that could fit within your word template, thus providing you with many possible answers.
* **Note:** This file will also display a histogram of the likelyhood of each letter occuring, based on the number of times it occurs in words in the provided dictionary.


The default words the game uses are located in **scrabble5.txt**. However, this can be changed by entering a new 'targetFile' and 'size' found in 'main.py'.


The file 'clean.py' was created to clean a mock-corrupted dictionary '.txt' file, and output the words to a new '.txt' file that the program can now use.

