class Flashcard:
    def __init__(self, question, answer):
        self.question = question
        self.answer = answer

    def display_question(self, question):
        return self.question

    def display_answer(self, answer):
        return self.answer

import json

question_input = Flashcard(input("Enter your question: "), "  ")
answer_input = Flashcard("  ", input("Enter your answer: "))

    
ques_var = question_input.display_question(question_input)
ans_var = answer_input.display_answer(answer_input)

with open('flashinfo.json', 'r') as jsonfiles:
        data = jsonfiles.read()
        data_converter = json.loads(data)
        id = data_converter[-1]["ID"] if data_converter else 0
        id += 1
        

flashcards = {
    "Questions": ques_var,
    "Answers": ans_var,
    "ID": id
}
lists = ([flashcards])