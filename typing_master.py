import random
import json
import time
import sys

# Constants
WORD_LIST_FILE = 'word_categories.json'  # Change to your word categories file
LEADERBOARD_FILE = 'leaderboard.json'  # Change to your leaderboard file

# Function to load words from a JSON file
def load_words_from_json(filename):
    with open(filename, 'r') as file:
        word_data = json.load(file)
    return word_data

# Function to update and sort the leaderboard
def update_leaderboard(username, wpm):
    leaderboard = []

    try:
        with open(LEADERBOARD_FILE, 'r') as file:
            leaderboard = json.load(file)
    except FileNotFoundError:
        pass

    leaderboard.append({'username': username, 'wpm': wpm})
    leaderboard.sort(key=lambda x: x['wpm'], reverse=True)

    with open(LEADERBOARD_FILE, 'w') as file:
        json.dump(leaderboard, file, indent=4)

# Function to show the leaderboard
def show_leaderboard():
    try:
        with open(LEADERBOARD_FILE, 'r') as file:
            leaderboard = json.load(file)
            print("Leaderboard:")
            for i, entry in enumerate(leaderboard, start=1):
                print(f"{i}. {entry['username']}: {entry['wpm']} WPM")
    except FileNotFoundError:
        print("Leaderboard is empty.")

# Function to conduct the typing test
def start_typing_test(username, category, words):
    print(f"Category: {category}")
    print("Type the following words. Press 'Ctrl + Q' to quit.")
    input("Press Enter to start...")

    start_time = time.time()
    words_typed = 0

    for word in words:
        print(word)
        user_input = input()
        if user_input == 'Ctrl+Q':
            print("Typing test aborted.")
            break
        words_typed += 1

    end_time = time.time()
    elapsed_time = end_time - start_time
    wpm = int(words_typed / (elapsed_time / 60))

    print(f"Words Typed: {words_typed}")
    print(f"Time Taken: {elapsed_time:.2f} seconds")
    print(f"Words Per Minute (WPM): {wpm}")

    update_leaderboard(username, wpm)

# Main game logic
def main():
    print("Welcome to the Typing Test Application!")

    username = input("Enter your username: ")

    while True:
        print("\nOptions:")
        print("1. Start Typing Test")
        print("2. Show Leaderboard")
        print("3. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            word_data = load_words_from_json(WORD_LIST_FILE)
            categories = list(word_data.keys())

            print("Select a category:")
            for i, category in enumerate(categories, start=1):
                print(f"{i}. {category}")

            category_choice = input("Enter the category number: ")

            if category_choice.isdigit() and 1 <= int(category_choice) <= len(categories):
                category = categories[int(category_choice) - 1]
                words = word_data[category]
                random.shuffle(words)

                start_typing_test(username, category, words)
            else:
                print("Invalid category choice. Please try again.")

        elif choice == '2':
            show_leaderboard()

        elif choice == '3':
            sys.exit()

if __name__ == "__main__":
    main()
