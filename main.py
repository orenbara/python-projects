import turtle
import pandas
"""List as many U.S states as you can, type exit to finish game and get csv of missing states"""

NUMBER_OF_STATES = 50

# Define Map
screen = turtle.Screen()
screen.title("U.S States Game Oren's Version")
image = "map.gif"
screen.addshape(image)
turtle.shape(image)
screen.setup(725, 491)

# Get counties data from csv
states_df = pandas.read_csv("50_states.csv")
state_series = states_df.state
states_list = states_df.state.to_list()
user_guess_list = []
cancel_pressed = False
while len(user_guess_list) < NUMBER_OF_STATES:
    answer_state = screen.textinput(title=f"{len(user_guess_list)}/{NUMBER_OF_STATES} States Guessed", prompt="What's another state's "
                                                                                              "name?")
    if answer_state is None:
        cancel_pressed = True
        break
    answer_state = answer_state.title()
    if answer_state in states_list and answer_state not in user_guess_list and answer_state != "Exit":
        state_data = states_df[state_series == answer_state]
        # Get coordinates from data
        x = int(state_data.x)
        y = int(state_data.y)
        user_guess_list.append(answer_state)

        # Move state on map
        map_state = turtle.Turtle()
        map_state.penup()
        map_state.hideturtle()
        map_state.goto(x, y)
        map_state.write(f'{answer_state}')
    elif answer_state in user_guess_list:
        print(f"Already Guessed {answer_state}")
    elif answer_state == "Exit":
        user_name = screen.textinput(title="Missing States", prompt="New CSV with missing states wil be generated, What's your name?")
        missing_states = []
        for state in states_list:
            if state not in user_guess_list:
                missing_states.append(state)
        missing_states_df = pandas.DataFrame(missing_states)
        missing_states_df.to_csv(f"{user_name}.csv")
        break

if not cancel_pressed:
    # Winning message
    message = turtle.Turtle()
    message.penup()
    message.hideturtle()
    message.goto(-70, 0)
    message.write("You Won!!!!!!!!!!", font=('Arial', 20, 'normal'))
else:
    message = turtle.Turtle()
    message.penup()
    message.hideturtle()
    message.goto(-120, 0)
    message.write("You chose to cancel", font=('Arial', 20, 'normal'))
screen.mainloop()