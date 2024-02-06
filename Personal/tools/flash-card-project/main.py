from tkinter import *
import pandas
import random


BACKGROUND_COLOR = "#B1DDC6"


# Flips the card to the other language
def flip_card():
    canvas.itemconfig(title, text="עברית", fill="white")
    canvas.itemconfig(word, text=random_card["עברית"], fill="white")
    canvas.itemconfig(current_image, image=card_back_img)

# Generates new random card
def new_word():
    global random_card, timer
    window.after_cancel(timer)
    random_card = random.choice(list_of_dicts)
    canvas.itemconfig(title, text="English", fill="black")
    canvas.itemconfig(word, text=random_card["English"], fill="black")
    canvas.itemconfig(current_image, image=front_image)
    timer = window.after(3000, flip_card)

def know_word():
    list_of_dicts.remove(random_card)
    new_word()
    new_data = pandas.DataFrame(list_of_dicts)
    new_data.to_csv("data/words_to_learn.csv", index=False)



# ---------------------------- UI SETUP ------------------------------- #


window = Tk()
window.title("Flesh Cards Game")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)
timer = window.after(3000, flip_card)


canvas = Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
front_image = PhotoImage(file="images/card_front.png")
current_image = canvas.create_image(400, 263, image=front_image)
canvas.grid(row=0, column=0, columnspan=2)

title = canvas.create_text(400, 100, text="Title", font=("Ariel", 40, "italic"))
word = canvas.create_text(400, 250, text="Word", font=("Ariel", 50, "bold"))

img_right = PhotoImage(file="images/right.png")
button_right = Button(image=img_right, highlightthickness=0, command=know_word)
button_right.grid(row=1, column=0)

img_wrong = PhotoImage(file="images/wrong.png")
button_wrong = Button(image=img_wrong, highlightthickness=0, command=new_word)
button_wrong.grid(row=1, column=1)

# For flipping:
card_back_img = PhotoImage(file="images/card_back.png")

# ----------------------------  Words ------------------------------- #

try:
    df = pandas.read_csv(filepath_or_buffer="data/words_to_learn.csv")
except FileNotFoundError:
    origin_df = pandas.read_csv(filepath_or_buffer="data/words.csv")
    list_of_dicts = origin_df.to_dict(orient="records")
else:
    list_of_dicts = df.to_dict(orient="records")



# Define first English Word
random_card = random.choice(list_of_dicts)
canvas.itemconfig(title, text="English")
canvas.itemconfig(word, text=random_card["English"])

window.mainloop()
