import sqlite3
import time

# Connect to SQLite database
conn = sqlite3.connect('users.db')
cursor = conn.cursor()

# Create users table if not exists
cursor.execute('''CREATE TABLE IF NOT EXISTS users
                  (id INTEGER PRIMARY KEY AUTOINCREMENT,
                   username TEXT UNIQUE,
                   password TEXT)''')
conn.commit()


# Define the quiz questions
questions = [
    {
        "question": "What is the output of '2 + 3 * 5'?",
        "options": ["10", "25", "17", "None of the above"],
        "answer": "17"
    },
    {
        "question": "Which data type is mutable in Python?",
        "options": ["int", "float", "tuple", "list"],
        "answer": "list"
    },
    {
        "question": "What is the keyword to define a function in Python?",
        "options": ["def", "function", "define", "func"],
        "answer": "def"
    },
    {
        "question": "What is the result of '10 % 3'?",
        "options": ["3", "1", "0", "10"],
        "answer": "1"
    },
    {
        "question": "Which of the following is not a Python built-in function?",
        "options": ["print()", "len()", "random()", "range()"],
        "answer": "random()"
    },
    {
        "question": "What is the output of 'print(bool(0))'?",
        "options": ["True", "False", "0", "1"],
        "answer": "False"
    },
    {
        "question": "How do you comment out multiple lines of code in Python?",
        "options": ["# Comment", "/* Comment */", "''' Comment '''", "// Comment"],
        "answer": "''' Comment '''"
    },
    {
        "question": "What does the 'pass' statement do in Python?",
        "options": ["Stops the execution of the program", "Does nothing", "Raises an exception", "Prints 'pass' to the console"],
        "answer": "Does nothing"
    },
    {
        "question": "What method is used to remove an item from a list in Python?",
        "options": [".delete()", ".remove()", ".pop()", ".discard()"],
        "answer": ".remove()"
    },
    {
        "question": "What is the result of '10 == '10' in Python?",
        "options": ["True", "False", "Error", "None"],
        "answer": "False"
    }
    # Add more questions here...
]

# Function to authenticate the user
def login():
    username = "beamlak"
    password = "abcdef123"
    cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    user = cursor.fetchone()
    if user:
        return username
    else:
        print("Invalid username or password.")
# Function to register a new user
def register():
    username = "beamlak"  # Set the username manually
    password = "abcdefg123"  # Set the password manually
    cursor.execute("SELECT * FROM users WHERE username=?", (username,))
    existing_user = cursor.fetchone()
    if existing_user:
        print("Username already exists. Please choose a different username.")
    else:
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        print("Registration successful! You can now login.")

# Function to display questions and collect answers
def run_quiz(username):
    score = 0
    total_questions = len(questions)
    start_time = time.time()

    print("\n--- Python Quiz - Welcome, {}! ---\n".format(username))
    for i, q in enumerate(questions, 1):
        print("Question {}: {}".format(i, q['question']))
        print("Options:")
        for idx, option in enumerate(q['options'], 1):
            print("{}. {}".format(idx, option))
        while True:
            try:
                user_choice = int(input("Enter your choice (1-4): "))
                if 1 <= user_choice <= 4:
                    break
                else:
                    print("Please enter a valid option (1-4)")
            except ValueError:
                print("Please enter a valid option (1-4)")

        selected_option = q['options'][user_choice - 1]
        if selected_option == q['answer']:
            print("Correct!")
            score += 1
        else:
            print("Wrong! The correct answer is: {}".format(q['answer']))
    end_time = time.time()
    total_time = round(end_time - start_time, 2)

    print("\n--- Quiz Completed! ---\n")
    print("Your score: {}/{}".format(score, total_questions))
    print("Total time taken: {} seconds".format(total_time))

# Main function to run the quiz
if __name__ == "__main__":
    print("\n--- User Registration ---")
    register()

    print("\n--- User Login ---")
    username = login()
    run_quiz(username)

# Close the database connection
conn.close()
