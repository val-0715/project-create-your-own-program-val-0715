import json
import classes 
from classes import ques_var, ans_var
def collect_input():

    try:
        with open('flashinfo.json', 'r') as jsonfiles:
            data = json.load(jsonfiles)
            new_flashcard = data + lists
    except FileNotFoundError:
        with open('flashinfo.json', 'w') as f:
            json.dump(new_flashcard, f, indent = 2)
            print("success!")
    with open('flashinfo.json', 'w') as f:
            json.dump(new_flashcard, f, indent = 2)
            print("success!")

#with open('flashinfo.json', 'r') as jsonfiles:
 #       data = jsonfiles.read()
  #      data_converter = json.loads(data)
   #     id = data_converter[-1]["ID"] if data_converter else 0
    #    id += 1
id = 2

flashcards = {
    "Questions": ques_var,
    "Answers": ans_var,
    "ID": id
}
lists = ([flashcards])
collect_input()