import json

def reading_data():
    try:
        with open('flashinfo.json', 'r') as f:
            data = json.load(f)
            return data

    except FileNotFoundError:
        data = [{
        "Questions":"pratice",
        "Answers":"flashcard" ,
        "ID": 0
        }]

        with open('flashinfo.json', 'w') as f:
            json.dump(data, f, indent = 2)

def flashcards():
    import classes 
    from classes import ques_var, ans_var


    with open('flashinfo.json', 'r') as f:
            data_converter = json.load(f)
            num = data_converter[-1]["ID"] if data_converter else 0
            num += 1
            

            
    flashcards = {
        "Questions": ques_var,
        "Answers": ans_var,
        "ID": num
    }
    lists = ([flashcards])
    
    new_flashcard = data_converter + lists

    return new_flashcard

def create_flashcards():
    flash_var = flashcards()
    with open('flashinfo.json', 'w') as f:
            json.dump(flash_var, f, indent = 2)
            print("success!")

def delete_flashcards():
    d = reading_data()
    usr_input = int(input("Choose ID number to delete flashcard: "))
    data = [card for card in d if card.get('ID') != usr_input]

    with open('flashinfo.json', "w") as f:
        json.dump(data, f, indent = 2)
    

    
reading_data()
#flashcards()
#create_flashcards()
#delete_flashcards()