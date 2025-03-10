from tkinter import *
from random import choice
import pandas as pd

unknown_words = []
known_words = []
current_card = {}

# ----------------Word Selection------------------
def next_word():
    global known_words
    global unknown_words
    print(len(unknown_words))
    global current_card, flip_timer
    window.after_cancel(flip_timer)
    current_card = choice(unknown_words)
    flip_timer = window.after(3000, func=card_flip)

# ------------------------------------------------
def known():
    global current_card
    unknown_words.remove(current_card)
    known_words.append(current_card)
    save_words()
    next_word()
    canvas.itemconfig(canvas_image, image=front_image)
    canvas.itemconfig(card_title, text="French", fill="black")
    canvas.itemconfig(card_word, text=current_card["French"], fill="black")



def card_flip():
    canvas.itemconfig(canvas_image, image=back_image)
    canvas.itemconfig(card_title, text="English", fill="white")
    canvas.itemconfig(card_word, text = current_card["English"], fill="white")


def unknown():
    next_word()
    canvas.itemconfig(canvas_image, image=front_image)
    canvas.itemconfig(card_title, text="French")
    canvas.itemconfig(card_word, text=current_card["French"])

def setup():
    global unknown_words
    try:
        data = pd.read_csv("data/words_to_learn.csv")
    except FileNotFoundError:
        data = pd.read_csv("data/french_words.csv")
    unknown_words = data.to_dict(orient="records")
    next_word()
    canvas.itemconfig(card_title, text="French")
    canvas.itemconfig(card_word, text=current_card["French"])

def save_words():
    df = pd.DataFrame(unknown_words)
    df.to_csv("data/words_to_learn.csv", index=False)

# -----------------UI Setup------------------------
BACKGROUND_COLOR = "#B1DDC6"

window = Tk()
window.title("flashy")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

canvas = Canvas(height=526, width=800)
front_image = PhotoImage(file="images/card_front.png")
back_image = PhotoImage(file="images/card_back.png")

canvas_image = canvas.create_image(400, 263, image=front_image)
card_title = canvas.create_text(400, 150, text="", font=("Ariel", 40, "italic"))
card_word = canvas.create_text(400, 263, text="", font=("Ariel", 60, "bold"))
canvas.config(bg=BACKGROUND_COLOR, highlightthickness=0)
canvas.grid(row=0, column=0, columnspan=2)



check_image = PhotoImage(file="images/right.png")
known_button = Button(image=check_image, command=known)
known_button.grid(row=1, column=1)
known_button.config(bg=BACKGROUND_COLOR,highlightthickness=0)

cross_image = PhotoImage(file="images/wrong.png")
unknown_button = Button(image=cross_image, command=unknown)
unknown_button.grid(row=1, column=0)
unknown_button.config(bg=BACKGROUND_COLOR,highlightthickness=0)

flip_timer = window.after(3000, func=card_flip)
setup()
window.mainloop()