#pip install rich
from rich.table import Table
from rich.console import Console
import json

console = Console()
table = Table(title="Flashcards")
table.add_column("ID", style="magenta")
table.add_column("Question", style="green")
table.add_column("Answer", style="yellow")

con = Console()
tab = Table(title="Flashcards")
tab.add_column("ID", style="magenta")
tab.add_column("Question", style="green")
tab.add_column("Answer", style="yellow")


def display_flashcards():
      table.add_row(str(d["ID"]), d["Questions"], "Answer?")
      console.print(table)
      if input("Answer: ") == d["Answers"]:
            print("Correct!")              

def display_correct_answers():
      tab.add_row(str(d["ID"]), d["Questions"], d["Answers"])
      con.print(tab)                                          

with open('flashinfo.json') as f:
      data = json.load(f)

      for d in data:
            display_flashcards()
            display_correct_answers()
