import random
import tkinter as tk

# Game word list with hints
words_with_hints = {
    'PYTHON': 'A snake? Nah, it’s a programming language that bites bugs!',
    'HANGMAN': 'The name of this game – hope you guessed it right!',
    'SPAGHETTI': 'Pasta that gets tangled like life – especially on Mondays.',
    'COWBOY': 'Someone who rides horses and says "Yeehaw!" before every meal.',
    'PIZZA': 'A cheesy masterpiece that solves 99 percent of life’s problems.',
    'PILLOW': 'Your loyal companion during midnight overthinking sessions.',
    'CLOUD': 'Fluffy stuff in the sky that just refuses to rain when you need it.',
    'CUPCAKE': 'A cake that fits in your hand – dreams do come true!',
    'TURTLE': 'A creature that’s slow but always wins the snack race.',
    'UNICORN': 'A horse that upgraded itself with a sparkly horn.',
    'BANANA': 'A fruit that makes you slip... literally.',
    'BROOM': 'The device that helps sweep problems under the rug.',
    'SNEEZE': 'The sudden explosion from your nose. Achoo!',
    'PIRATE': 'A person who always marks their treasure with an "X".',
    'BEE': 'A tiny creature with a big job and a bigger attitude!',
    'BUBBLE': 'Fun to pop, gone too soon – just like weekends.',
    'BED': 'Where all your greatest ideas are born... and forgotten.',
    'PINEAPPLE': 'The fruit that sparks endless pizza debates.',
    'SANDWICH': 'A meal stuck between two slices of indecision.',
    'PENGUIN': 'A bird that can’t fly but rocks a tuxedo like no one else.',
    'SPOON': 'What you need when forks just can’t handle the pressure.',
    'MONKEY': 'A creature that throws tantrums... and sometimes bananas.'
}


# Function to select a random word and its hint
def select_word():
    word, hint = random.choice(list(words_with_hints.items()))
    return word, hint

# Function to update the display of the word (correct guesses or blanks)
def update_display_word():
    display_word = ' '.join([letter if letter in correct_guesses else '_' for letter in word_to_guess])
    word_label.config(text=display_word)
    if '_' not in display_word:
        result_label.config(text="Congratulations! You won!", fg="green")
        disable_buttons()

# Function to handle player guesses
def handle_guess(letter):
    global attempts_remaining
    if letter in correct_guesses or letter in incorrect_guesses:
        result_label.config(text=f"You already guessed '{letter}'!", fg="orange")
        return
    
    if letter in word_to_guess:
        correct_guesses.add(letter)
        result_label.config(text=f"Good guess! '{letter}' is in the word.", fg="green")
    else:
        incorrect_guesses.add(letter)
        attempts_remaining -= 1
        result_label.config(text=f"'{letter}' is not in the word.", fg="red")
        draw_hangman(attempts_remaining)
    
    attempts_label.config(text=f"Attempts remaining: {attempts_remaining}")
    incorrect_label.config(text=f"Incorrect guesses: {', '.join(incorrect_guesses)}")
    update_display_word()

    if attempts_remaining == 0:
        result_label.config(text=f"Game Over! The word was '{word_to_guess}'.", fg="red")
        disable_buttons()

# Function to disable all buttons when the game ends
def disable_buttons():
    for button in letter_buttons.values():
        button.config(state="disabled")

# Function to reset the game
def reset_game():
    global word_to_guess, hint, correct_guesses, incorrect_guesses, attempts_remaining
    word_to_guess, hint = select_word()
    correct_guesses.clear()
    incorrect_guesses.clear()
    attempts_remaining = 6
    
    result_label.config(text="")
    attempts_label.config(text=f"Attempts remaining: {attempts_remaining}")
    incorrect_label.config(text="Incorrect guesses: ")
    hint_label.config(text=f"Hint: {hint}")
    
    for button in letter_buttons.values():
        button.config(state="normal")
    
    canvas.delete("hangman")  # Clear the hangman drawing
    update_display_word()

# Function to draw the hangman on the canvas based on remaining attempts
def draw_hangman(attempts):
    canvas.delete("hangman")
    if attempts <= 5:
        canvas.create_line(20, 180, 120, 180, tags="hangman", fill="white", width=3)  # Base
    if attempts <= 4:
        canvas.create_line(70, 180, 70, 20, tags="hangman", fill="white", width=3)    # Pole
    if attempts <= 3:
        canvas.create_line(70, 20, 130, 20, tags="hangman", fill="white", width=3)    # Top beam
    if attempts <= 2:
        canvas.create_line(130, 20, 130, 40, tags="hangman", fill="white", width=3)   # Rope
    if attempts <= 1:
        canvas.create_oval(110, 40, 150, 80, tags="hangman", outline="white", width=3)  # Head
    if attempts == 0:
        canvas.create_line(130, 80, 130, 130, tags="hangman", fill="white", width=3)  # Body
        canvas.create_line(130, 90, 110, 110, tags="hangman", fill="white", width=3)  # Left arm
        canvas.create_line(130, 90, 150, 110, tags="hangman", fill="white", width=3)  # Right arm
        canvas.create_line(130, 130, 110, 160, tags="hangman", fill="white", width=3) # Left leg
        canvas.create_line(130, 130, 150, 160, tags="hangman", fill="white", width=3) # Right leg

# Initialize game variables
correct_guesses = set()
incorrect_guesses = set()
attempts_remaining = 6

# Set up the Tkinter window
window = tk.Tk()
window.title("Hangman Game")
window.geometry("500x700")
window.config(bg="black")

# Create canvas for drawing the hangman
canvas = tk.Canvas(window, width=300, height=300, bg="black", highlightthickness=0)
canvas.pack(pady=10)

# Display the word with blanks and correct guesses
word_label = tk.Label(window, text="", font=("Helvetica", 24), fg="white", bg="black")
word_label.pack(pady=10)

# Display hint for the word
hint_label = tk.Label(window, text="", font=("Helvetica", 16), fg="orange", bg="black")
hint_label.pack(pady=5)

# Display remaining attempts
attempts_label = tk.Label(window, text=f"Attempts remaining: {attempts_remaining}", font=("Helvetica", 16), fg="white", bg="black")
attempts_label.pack(pady=5)

# Display incorrect guesses
incorrect_label = tk.Label(window, text="Incorrect guesses: ", font=("Helvetica", 16), fg="white", bg="black")
incorrect_label.pack(pady=5)

# Display game result (win/lose)
result_label = tk.Label(window, text="", font=("Helvetica", 24), fg="orange", bg="black")
result_label.pack(pady=5)

# Create frame for letter buttons
button_frame = tk.Frame(window, bg="black")
button_frame.pack(pady=5)

# Create letter buttons
letter_buttons = {}
for index, letter in enumerate("ABCDEFGHIJKLMNOPQRSTUVWXYZ"):
    button = tk.Button(button_frame, text=letter, font=("Helvetica", 14), width=3, height=1, 
                       command=lambda l=letter: handle_guess(l), bg="grey", fg="white")
    button.grid(row=index // 13, column=index % 13, padx=5, pady=5)
    letter_buttons[letter] = button

# Reset button to start a new game
reset_button = tk.Button(window, text="New Game", font=("Helvetica", 10), command=reset_game, bg="orange", fg="black")
reset_button.pack(pady=5)

# Initialize the game
word_to_guess, hint = select_word()
update_display_word()
hint_label.config(text=f"Hint: {hint}")

# Run the Tkinter main loop
window.mainloop()
