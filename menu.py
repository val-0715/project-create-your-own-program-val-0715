print("Welcome to the Flashcard CLI!",
"\n1. Create a flashcard",
"\n2. Review flashcards",
"\n3. Delete Flashcards",
"\n4. Exit",
"\nPlease select an option (1, 2, 3, or 4)")
input_option = input("Option: ")

if input_option == "1":
    import storage
    from storage import create_flashcards
    create_flashcards()
elif input_option == "2":
    import flashcards_cli
elif input_option == "3":
    import storage
    from storage import delete_flashcards
    delete_flashcards()

elif input_option == "4":
    print("Goodbye!")
else:
    print("Invalid option, please try again.")