import json
import classes 
from classes import lists, flashcards
def collect_input():
    with open('flashinfo.json', 'r') as jsonfiles:
        data = json.load(jsonfiles)
        new_flashcard = data + lists

    with open('flashinfo.json', 'w') as f:
        json.dump(new_flashcard, f, indent = 2)
        print("success!")
collect_input()