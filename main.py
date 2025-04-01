import json
import utils
import random
from os import path
class Hangman:
    def __init__(self, word:str, total_points, guesses = None) -> None:
        if guesses == None:
            guesses = set()
        self.user_end = False
        self.target_word = word
        self.used_guesses = guesses
        self.points = total_points
        self.formatting_tools = utils.Formatting()
    def checkForEnd(self): #uses self.word, self.guesses, self.points
        # print(f"word: {sorted(set(self.word))}, guesses used: {sorted(self.guesses)}")
        if self.user_end:
            return True, "Q"
        elif self.points <= 0:
            return True, "L" #loss
        elif  set(sorted(self.target_word)) <= set(sorted(self.used_guesses)): #note: Not scalable
            return True,"W"
        else:
            return False,"-"
    def processGuess(self, guess:str): #uses guess, self.guesses, self.word, self.points
        if len(guess) == 1:
            if guess in self.used_guesses: # is a in {...}
                self.used_guesses.add(guess) 
                self.points -= 10
                print(f"Total points: {self.points}")
                return "Already used letter, loose 10 points"
            elif guess not in self.target_word:
                self.used_guesses.add(guess) 
                self.points -= 10
                print(f"Total points: {self.points}")
                return "Wrong choice, loose 10 points"    
            else:
                self.used_guesses.add(guess)
                self.points += 10
                print(f"Total points: {self.points}")
                return "Correct Choice, gain 10 points!"
        elif guess == "QUIT":
            self.user_end = True
            return "Exiting game"

        else:
            if self.target_word == guess:
                for letter in guess: self.used_guesses.add(letter)
                self.points += 10
                return "Correct Choice, gain 10 points!"
            else:
                self.points -= 10
                print(f"Total lives left: {self.points}")
                return "Wrong choice, loose 10 points"
    def renderWord(self): # uses self.word, self.guesses
        display = ""
        for char in self.target_word: # could be simplified to collection
            if char in self.used_guesses:
                display += f" {char} "
            else:
                display += " _ "
        display = self.formatting_tools.colors(display,"green")
        display += self.formatting_tools.colors("\nletters guessed: ","cyan")

        for used_letter in sorted(self.used_guesses):
            if used_letter in self.target_word:
                display += self.formatting_tools.colors(used_letter,"cyan")
            else:
                display += self.formatting_tools.colors(used_letter,"red") #sort guesses taken alpahbetically, convert into a string. Also render it in a different color
            display += " "       
        return display
#Software SCHOOL/Stream 2/Hangman Stream 2/all_words_info.json
def use_data(filename:str,relative_path:str|None = None,state:str|None = None,data = None): #loads and acceses database
    """
    Loads and accesses JSON database files with specified access mode.
    Args:
        filename (str): Name of the file to access
        relative_path (str, optional): Relative path to the file location. Defaults to empty string
        state (str, optional): File access mode. Defaults to "r" (read mode)
            Possible modes:
            - "r": Read (default)
            - "w": Write
            - "a": Append
            - "x": Create
            - "r+": Read and write
            - "w+": Write and read
            - "a+": Append and read
    Returns:
        dict or None: Returns JSON data as dictionary if successful, None if file not found
    Raises:
        FileNotFoundError: If specified file cannot be found at given path
    """
    if relative_path == None:
        relative_path = ""
    if state == None:
        state = "r"
    target_file_path = path.join(path.dirname(__file__),relative_path,filename)
    try:
        if state in ["w","a","x"]:
            with open(target_file_path, state) as file:
                json.dump(data, file, indent=4)
                return 
        else:
            with open(target_file_path, state) as file:
                game_data = json.load(file)
    except FileNotFoundError:
        print(f"File {filename} not found")
        return None
    return game_data

def load_game_state():
    saved_data = use_data("save_file.json")
    blank_game = False
    
    if saved_data:
        # Convert guesses to a set if it exists, otherwise create empty set
        guesses = set(saved_data["guesses"]) if saved_data.get("guesses") else set()
        word =str(saved_data["word"])
        points = saved_data["points"]

        # Check if any essential data is missing
        if points == '' or word == None:
            print("save file is empty")
            blank_game = True
    else:
        print("save file can not be found, creating new save file")
        use_data("save_file.json", state="x",data = {"word": "", "points": 0, "guesses": []})
        blank_game = True

    if blank_game:
        print("Starting new game")    
        word, points = chooseDif()
        guesses = set()
    
    return Hangman(word, int(points), guesses)
def save_game_state(game:Hangman):
    save_data = {
        "word": game.target_word,
        "points": game.points,
        "guesses": list(game.used_guesses)
    }
    use_data("save_file.json", state="w", data=save_data)

def chooseDif(): # uses loaded data
    game_data= use_data("all_words_info.json")
    if game_data == None:
        print("Exiting program")
        raise SystemExit
    all_words = game_data['all_words']
    difficulty_info = game_data['difficulties']
    options = []
    for difficulty in difficulty_info.values():
        options.extend(difficulty["shortcuts"])
    while True:
        user_choosen_difficulty = input("Choose a difficulty: ").lower()
        if user_choosen_difficulty in options:
            if user_choosen_difficulty in difficulty_info["easy"]["shortcuts"]:
                final_difficulty = "easy"
            elif user_choosen_difficulty in difficulty_info["medium"]["shortcuts"]:
                final_difficulty = "medium"
            elif user_choosen_difficulty in difficulty_info["hard"]["shortcuts"]:
                final_difficulty = "hard"
            else:
                print("Invalid Difficulty, try again. ")
                continue
            break
        else:
            print("Invalid Difficulty, try again. ")
    return (random.choice(all_words[final_difficulty]), difficulty_info[final_difficulty]["points"])
def write_new_words(new_word:str):
    if new_word.lower() == "quit":
        print("Exiting edit list mode ")
        return True # Function ends in a way the user intends
    if new_word == None or not new_word.isalpha(): # If the input had symbols/digits, or if it was just nothing, then break the function
        print("Enter a valid value")
        return False # Indicates that the function was not succesful
    with open('Software SCHOOL/Stream 2/Hangman Stream 2/Word Lists/all_words_info.json','r') as word_file:
        word_file_info = json.load(word_file)
    difficulty_lengths = {}
    for difficulty in word_file_info["difficulties"].keys():
        difficulty_lengths[difficulty] = word_file_info["difficulties"][difficulty]['word_length'][1] 

    valid_word = False
    if len(new_word)<word_file_info["difficulties"]["easy"]['word_length'][0]: #break if the suggested word is too small for the first difficulty
        print("Enter a word with the correct length")
        return False 
    
    difficulty_of_word = None
    for difficulty, length_of_word in difficulty_lengths.items():
        if len(new_word) < length_of_word:
            difficulty_of_word = difficulty
            if new_word not in word_file_info['all_words'][difficulty]:
                word_file_info['all_words'][difficulty].append(new_word)
            else:
                print("Word entered already exists ")
                return False 
            break
    if difficulty_of_word == None: # length of word is out of bounds --> break the function
        print("Enter a word with the correct length")
        return False
    with open('Software SCHOOL/Stream 2/Hangman Stream 2/Word Lists/all_words_info.json','w') as overwrite_file:
        json.dump(word_file_info, overwrite_file, indent=4) #overwrite the file with the updated word list
    print(f"\'{new_word}\' has been added into the {difficulty_of_word} list!\n")
    word_file_info = None
    return True # function is executed normally
end_game = False
print(f"""
=============================================
                HANGMAN GAME
=============================================

HOW TO PLAY:
-----------
* START: Type "start" or "s" to begin a new game
* LOAD:  Type "load" or "l" to continue a saved game
* UPDATE: Type "update" or "u" to add new words
* QUIT:  Type "QUIT" to exit at any point

DIFFICULTY LEVELS:
----------------
Easy, Medium, or Hard - each with different word 
lengths and starting points.

GAMEPLAY RULES:
-------------
* Guess one letter at a time or the full word
* CORRECT guess: +10 points
* INCORRECT guess: -10 points
* REPEATED guess: -10 points
* Type "QUIT" during a game to exit

WINNING & LOSING:
---------------
* WIN: Successfully guess the complete word
* LOSE: Your points reach zero

Games are automatically saved after each guess.
Green letters = correct guesses, Red letters = incorrect

Type "start", "load", "update" to begin...
======================================================
""")
while True:
    while True:
        game_state = input("Start a game, update word list, or load a new save file? ").lower()
        if game_state in ["start","update","load","s","u","l"]:
            if game_state in ['start','s']:
                word, maxPoints = chooseDif()
                currentGame = Hangman(word, maxPoints)
                break
            elif game_state in ["update", "u"]:
                while True:
                    if write_new_words(input("Add a new word (type QUIT to exit edit mode):  ")):
                        break
            elif game_state in ["load","l"]:
                print("Loading save file . . .")
                currentGame=load_game_state()
                break
        elif game_state.lower() in ["quit","q"]:
            end_game = True
            break
    if end_game:
        print("Exiting program.")
        break
    # This point is ONLY reached if the user has chosen to start a new game, or loaded a new one
    print(currentGame.renderWord())
    while True:
        print(currentGame.processGuess(input("guess: ")))
        save_game_state(currentGame)
        isEnd = currentGame.checkForEnd()
        if isEnd[0] == True:
            if isEnd[1] == "W":
                print(currentGame.formatting_tools.colors(f"You Won, the word was {currentGame.target_word}! \nYou had a total of {currentGame.points}", "green"))
            elif isEnd[1] == "L":
                print(currentGame.formatting_tools.colors((f"You Lost, the word was {currentGame.target_word}! \nYou had a total of {currentGame.points}"),"red"))
            elif isEnd[1] == "Q":
                raise SystemExit
            # TODO: render the word at the very end
            break
        print(currentGame.renderWord())
    save_game_state(Hangman("","",set())) #reset the save file
    if input("Would you like to play again? (y/n) ").lower() in ["y","yes","t"]:
        print("Starting a new game! \n\n")
    else:
        print("Thanks for playing! \nExiting Program.")
        break