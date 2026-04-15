import json
import os
from flask import Flask, redirect, render_template_string, request, url_for

import classes
import storage

DATA_FILE = 'flashinfo.json'
app = Flask(__name__)

BASE_HTML = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Flashcards App</title>
    <style>
        body {
            margin: 0;
            font-family: Arial, sans-serif;
            background: linear-gradient(135deg, #0b0c10 0%, #1f2833 40%, #45a29e 100%);
            color: #edf2f4;
        }
        .page {
            max-width: 860px;
            margin: 0 auto;
            padding: 24px;
        }
        .header {
            text-align: center;
            margin-bottom: 32px;
        }
        .header h1 {
            margin: 0;
            color: #66fcf1;
            font-size: 36px;
        }
        .subtitle {
            color: #c5c6c7;
            font-size: 16px;
            margin-top: 8px;
        }
        .menu-grid {
            display: grid;
            gap: 16px;
            grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
        }
        .panel {
            background: rgba(255, 255, 255, 0.08);
            border: 1px solid rgba(102, 252, 241, 0.4);
            border-radius: 18px;
            padding: 28px;
            box-shadow: 0 18px 40px rgba(0, 0, 0, 0.15);
        }
        .button {
            display: inline-block;
            margin-top: 12px;
            padding: 14px 22px;
            background: #66fcf1;
            color: #0b0c10;
            border: none;
            border-radius: 12px;
            text-decoration: none;
            font-weight: bold;
            cursor: pointer;
        }
        .button:hover {
            background: #45a29e;
            color: #f8f9fa;
        }
        .card {
            background: #0b0c10;
            border-radius: 24px;
            border: 3px solid #66fcf1;
            padding: 32px;
            margin: 24px 0;
            box-shadow: inset 0 0 30px rgba(102, 252, 241, 0.12);
        }
        .card-title {
            margin: 0 0 16px;
            color: #0b0c10;
            font-size: 22px;
        }
        .card-text {
            color: #0b0c10;
            font-size: 20px;
            line-height: 1.5;
        }
        .input-row {
            margin-top: 18px;
        }
        label {
            display: block;
            margin-bottom: 10px;
            color: #c5c6c7;
            font-weight: bold;
        }
        input[type='text'], input[type='number'] {
            width: 100%;
            padding: 12px 14px;
            border-radius: 12px;
            border: 1px solid #66fcf1;
            background: #f8f9fa;
            color: #0b0c10;
            font-size: 14px;
        }
        .message {
            margin-top: 18px;
            padding: 14px 18px;
            border-radius: 14px;
            background: rgba(102, 252, 241, 0.16);
            color: #edf2f4;
        }
        .nav-row {
            display: flex;
            gap: 12px;
            flex-wrap: wrap;
            margin-top: 22px;
        }
    </style>
</head>
<body>
    <div class="page">
        <div class="header">
            <h1>Flashcards App</h1>
            <div class="subtitle">Review, create, and delete flashcards using your app data.</div>
        </div>
        {{ content|safe }}
    </div>
</body>
</html>
'''

MENU_HTML = '''
<div class="menu-grid">
    <div class="panel">
        <h2>1. Create a flashcard</h2>
        <p>Add a question and answer pair to your flashcard database.</p>
        <a class="button" href="{{ url_for('create') }}">Go to Create</a>
    </div>
    <div class="panel">
        <h2>2. Review flashcards</h2>
        <p>See one flashcard at a time and flip it after answering.</p>
        <a class="button" href="{{ url_for('review') }}">Go to Review</a>
    </div>
    <div class="panel">
        <h2>3. Delete flashcards</h2>
        <p>Browse cards and remove one by its ID number.</p>
        <a class="button" href="{{ url_for('delete') }}">Go to Delete</a>
    </div>
</div>
'''

CREATE_HTML = '''
<div class="panel">
    <h2>Create a New Flashcard</h2>
    <form method="post">
        <div class="input-row">
            <label for="question">Enter question</label>
            <input id="question" name="question" type="text" value="{{ question|default('') }}" />
        </div>
        <div class="input-row">
            <label for="answer">Enter answer</label>
            <input id="answer" name="answer" type="text" value="{{ answer|default('') }}" />
        </div>
        <button class="button" type="submit">Create flashcard</button>
        <a class="button" href="{{ url_for('menu') }}">Back to menu</a>
    </form>
    {% if message %}
    <div class="message">{{ message }}</div>
    {% endif %}
</div>

        <a class="button" href="{{ url_for('menu') }}">Back to menu</a>
    {% else %}
        <div class="card">
            <h3 class="card-title">Flashcard ID: {{ card['ID'] }}</h3>
            <p class="card-text">{{ text }}</p>
        </div>
        {% if not show_back %}
            <form method="post">
                <div class="input-row">
                    <label for="user_answer">Your answer</label>
                    <input id="user_answer" name="user_answer" type="text" />
                </div>
                <input type="hidden" name="idx" value="{{ idx }}" />
                <button class="button" type="submit">Submit answer</button>
                <a class="button" href="{{ url_for('menu') }}">Back to menu</a>
            </form>
        {% else %}
            <div class="message">{{ message }}</div>
            <div class="nav-row">
                <a class="button" href="{{ url_for('review', idx=idx + 1) }}">Next card</a>
                <a class="button" href="{{ url_for('menu') }}">Back to menu</a>
            </div>
        {% endif %}
    {% endif %}
</div>

        <a class="button" href="{{ url_for('menu') }}">Back to menu</a>
    {% else %}
        <div class="card">
            <h3 class="card-title">ID: {{ card['ID'] }}</h3>
            <p class="card-text"><strong>Question:</strong> {{ card['Questions'] }}</p>
            <p class="card-text"><strong>Answer:</strong> {{ card['Answers'] }}</p>
        </div>
        <div class="nav-row">
            <a class="button" href="{{ url_for('delete', idx=prev_idx) }}">Previous card</a>
            <a class="button" href="{{ url_for('delete', idx=next_idx) }}">Next card</a>
        </div>
        <form method="post">
            <div class="input-row">
                <label for="delete_id">Please enter the flashcard's ID number you want discarded</label>
                <input id="delete_id" name="delete_id" type="text" value="{{ delete_id|default('') }}" />
            </div>
            <input type="hidden" name="idx" value="{{ idx }}" />
            <button class="button" type="submit">Delete by ID</button>
            <a class="button" href="{{ url_for('menu') }}">Back to menu</a>
        </form>
        {% if message %}
        <div class="message">{{ message }}</div>
        {% endif %}
    {% endif %}
</div>
'''


def load_flashcards():
    if not os.path.exists(DATA_FILE):
        data = storage.reading_data()
        return data if data is not None else []

    with open(DATA_FILE, 'r') as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []


def save_flashcards(cards):
    with open(DATA_FILE, 'w') as f:
        json.dump(cards, f, indent=2)


def create_flashcard(question, answer):
    question = question.strip()
    answer = answer.strip()
    if not question or not answer:
        return False

    classes.ques_var = question
    classes.ans_var = answer
    storage.create_flashcards()
    return True


def delete_flashcard_by_id(card_id):
    cards = load_flashcards()
    remaining = [card for card in cards if card.get('ID') != card_id]
    if len(remaining) == len(cards):
        return False

    save_flashcards(remaining)
    return True


def get_card_by_index(index):
    cards = load_flashcards()
    if not cards:
        return None, 0, 0
    length = len(cards)
    index = index % length
    return cards[index], index, length


@app.route('/')
def menu():
    return render_template_string(BASE_HTML, content=render_template_string(MENU_HTML))


@app.route('/create', methods=['GET', 'POST'])
def create():
    message = ''
    question_value = ''
    answer_value = ''
    if request.method == 'POST':
        question_value = request.form.get('question', '')
        answer_value = request.form.get('answer', '')
        if create_flashcard(question_value, answer_value):
            message = 'Flashcard created successfully.'
            question_value = ''
            answer_value = ''
        else:
            message = 'Please enter both a question and an answer.'

    return render_template_string(
        BASE_HTML,
        content=render_template_string(
            CREATE_HTML,
            message=message,
            question=question_value,
            answer=answer_value,
        ),
    )


@app.route('/review', methods=['GET', 'POST'])
def review():
    idx = 0
    try:
        idx = int(request.values.get('idx', 0))
    except ValueError:
        idx = 0

    card, idx, total = get_card_by_index(idx)
    show_back = False
    answer_text = card.get('Questions', '') if card else ''
    message = ''

    if request.method == 'POST' and card:
        user_answer = request.form.get('user_answer', '').strip()
        correct_answer = card.get('Answers', '')
        show_back = True
        answer_text = f'Answer: {correct_answer}'
        if user_answer.lower() == correct_answer.lower():
            message = 'Correct!'
        else:
            message = 'Incorrect. Correct answer is shown above.'

    return render_template_string(
        BASE_HTML,
        content=render_template_string(
            REVIEW_HTML,
            card=card,
            idx=idx,
            text=answer_text,
            show_back=show_back,
            message=message,
        ),
    )


@app.route('/delete', methods=['GET', 'POST'])
def delete():
    idx = 0
    try:
        idx = int(request.values.get('idx', 0))
    except ValueError:
        idx = 0

    card, idx, total = get_card_by_index(idx)
    message = ''
    delete_id_value = ''

    if request.method == 'POST':
        delete_id_value = request.form.get('delete_id', '').strip()
        if delete_id_value.isdigit():
            card_id = int(delete_id_value)
            if delete_flashcard_by_id(card_id):
                message = f'Flashcard ID {card_id} deleted successfully.'
                card, idx, total = get_card_by_index(idx)
            else:
                message = f'No flashcard with ID {card_id} found.'
        else:
            message = 'Please enter a valid numeric flashcard ID.'

    prev_idx = (idx - 1) if total > 0 else 0
    next_idx = (idx + 1) if total > 0 else 0

    return render_template_string(
        BASE_HTML,
        content=render_template_string(
            DELETE_HTML,
            card=card,
            idx=idx,
            prev_idx=prev_idx,
            next_idx=next_idx,
            delete_id=delete_id_value,
            message=message,
        ),
    )


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
