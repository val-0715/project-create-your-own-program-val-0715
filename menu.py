print("Welcome to the Flashcard CLI!",
"\n1. Create a flashcard",
"\n2. Review flashcards",
"\n3. Exit",
"\nPlease select an option (1, 2, or 3)")
input_option = input("Option: ")

if input_option == "1":
    import storage
elif input_option == "2":
    import flashcards_cli
elif input_option == "3":
    print("Goodbye!")
else:
    print("Invalid option, please try again.")