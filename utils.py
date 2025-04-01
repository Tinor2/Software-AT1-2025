class Formatting():
    def __init__(self) -> None:
        pass
    def colors(self, text = None, color = None): # Allow for changing the colors of a text. Takes an input of a certain string, and then a color. The default color is plain
        if text == None: text = ""
        if color == None: color = "plain"
        color = color.lower()
        startingEscape = "\033[" # Uses tags that indicate different colors to change the color
        endingEscape = "\033[0m"
        options = {"plain":"37m", # Linking different colors with their corrosponding tags
                "red":"31m", 
                "green":"32m",
                "yellow":"33m",
                "blue":"34m",
                "magenta":"35m", 
                "cyan":"36m"}
        if color in options:    
            colorToken = options[color] # find the tag based on the input 
        else: 
            colorToken = options["plain"] # If there is any misspellings, it will just show it to be plain
        text = startingEscape + colorToken + text + endingEscape # add in the tags
        return text
    def italicize(self, text = None) -> str:
        return f"\033[3m{text}\033[0m"
    
