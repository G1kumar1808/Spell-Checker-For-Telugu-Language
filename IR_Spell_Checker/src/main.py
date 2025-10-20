from spell_checker import SpellChecker

def process_sentence(sentence, checker):
    """
    A helper function to process a single sentence and print the results.
    """
    print(f"\n--- Checking ---")
    print(f"Original: {sentence}")
    
    results = checker.check_document(sentence)
    
    corrected_doc = sentence
    if results['corrections']:
        print("Found Misspelled Words:")
        for misspelled, details in results['corrections'].items():
            best_guess = details['best_guess']
            print(f"  - '{misspelled}':")
            print(f"    Best Guess: '{best_guess}'")
            print(f"    Candidates (Possibilities): {details['candidates']}")
            corrected_doc = corrected_doc.replace(misspelled, best_guess)
        print(f"Corrected Document: {corrected_doc}")
    else:
        print("No misspelled words found.")

def run_predefined_test_cases(checker):
    """
    Runs the 5 built-in test cases.
    """
    print("\n--- Running Pre-defined Test Cases ---")
    
    # Test Case 1: విజ్ఞానం (Science) misspelled as విగానం
    text1 = "విగానం రంగంలో భారతదేశం ముందుకు వెళుతోంది."
    
    # Test Case 2: పుస్తకం (Book) misspelled as పుసతకం and కంప్యూటర్ (Computer) as కంపూటర్
    text2 = "నేను ఒక కొత్త పుసతకం కొన్నాను, అది కంపూటర్ గురించి."
    
    # Test Case 3: భాష (Language) misspelled as బష and ప్రభుత్వం (Government) as ప్రబుత్వం
    text3 = "తెలుగు మన మాతృ బష మరియు మన ప్రబుత్వం దీనిని ప్రోత్సహిస్తుంది."
    
    # Test Case 4: విద్యార్థులు (Students) misspelled as విద్యాతులు
    text4 = "విద్యాతులు పరీక్షలకు సిద్ధమవుతున్నారు."

    # Test Case 5: ఆరోగ్యం (Health) misspelled as అరోగ్యం
    text5 = "అందరూ తమ అరోగ్యం జాగ్రత్తగా చూసుకోవాలి."

    test_documents = [text1, text2, text3, text4, text5]

    for i, doc in enumerate(test_documents, 1):
        process_sentence(doc, checker)
        print("-" * 20) # Separator

    print("\n--- Test Cases Complete ---\n")

def run_interactive_mode(checker):
    """
    Starts an interactive loop for the user to input sentences.
    """
    print("\n--- Interactive Mode ---")
    print("Type a Telugu sentence and press Enter.")
    print("Type 'exit' or 'quit' to return to the main menu.")

    while True:
        user_input = input("\nEnter sentence: ")

        if user_input.lower() in ['exit', 'quit']:
            print("Returning to main menu...")
            break
        
        if user_input:
            process_sentence(user_input, checker)
        else:
            print("You didn't type anything. Try again.")
    print("\n") # Add a space before showing menu again

def main_menu():
    """
    Displays the main menu and handles user choices.
    """
    # 1. Loads the Telugu index from the hard drive into RAM.
    print("Please wait, loading Telugu spell checker index...")
    telugu_checker = SpellChecker('src/te_word_counts.json')
    
    if not telugu_checker.WORDS:
        print("Could not load index. Please run '1_build_index.py'. Exiting.")
        return

    print("Index loaded successfully!")

    # 2. Start the main menu loop
    while True:
        print("========================================")
        print("   Telugu Spell Checker Main Menu   ")
        print("========================================")
        print("  1. Run Pre-defined Test Cases")
        print("  2. Enter Interactive Mode (Give Input)")
        print("  3. Exit")
        print("========================================")
        
        choice = input("Please enter your choice (1, 2, or 3): ")

        if choice == '1':
            run_predefined_test_cases(telugu_checker)
        elif choice == '2':
            run_interactive_mode(telugu_checker)
        elif choice == '3':
            print("\nExiting spell checker. Goodbye! 👋")
            break
        else:
            print("\nInvalid choice. Please press 1, 2, or 3 and then Enter.\n")

if __name__ == '__main__':
    main_menu()