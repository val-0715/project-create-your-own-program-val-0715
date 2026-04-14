class Flashcard:
    def __init__(self, question, answer):
        self.question = question
        self.answer = answer

    def display_question(self, question):
        return self.question

    def display_answer(self, answer):
        return self.answer

question_input = Flashcard(input("Enter your question: "), "  ")
answer_input = Flashcard("  ", input("Enter your answer: "))

    
ques_var = question_input.display_question(question_input)
ans_var = answer_input.display_answer(answer_input)

