from tkinter import *
import random
import json
import os

settings_dir = "settings"
jsonpath = "settings/settings.json"

default_json = {
    "MODE": "LOCAL"
}

def create_files():
    if not os.path.exists(jsonpath):
        os.mkdir(settings_dir)

        data_w = json.dumps(default_json, indent=4)
        with open(jsonpath, "w") as f:
            f.write(data_w)
        

def main():
    bgcolor = "#854bf7"

    window = Tk()

    window.geometry("420x420")
    window.title("HTO().games")
    window.config(background=bgcolor)

    label = Label(window, 
                  text="Welcome!", 
                  font=("Arial", 40, "bold"), 
                  fg="black", bg=bgcolor)
    label.pack()

    def disable_ttt():
        button_ttt.config(state=DISABLED)
        tic_tac_toe()
    
    button_ttt = Button(window,
                        text="Tic Tac Toe",
                        command=disable_ttt,
                        font=("Comic Sans", 20),
                        fg="white",
                        bg=bgcolor,
                        activeforeground="black",
                        activebackground=bgcolor,)
    button_ttt.pack()

    def enabler():
        button_ttt.config(state=ACTIVE)

    button_enabler = Button(window,
                            text="Enable all buttons",
                            command=enabler,
                            font=("Comic Sans", 20),
                            fg="white",
                            bg=bgcolor,
                            activebackground=bgcolor,
                            activeforeground="black")
    button_enabler.pack()

    window.mainloop()

def tic_tac_toe():

    def read_mode():

        with open(jsonpath, "r") as f:
            data = json.load(f)

        return data 
    
    data = read_mode()
    data_mode = data["MODE"]

    bgcolor = "#E5E80B"
    window_ttt = Tk()

    window_ttt.geometry("800x800")
    window_ttt.title("Tic Tac Toe")
    window_ttt.config(background=bgcolor)

    players = ["X", "O"]
    player = random.choice(players)
    
    buttons = [["" for _ in range(3)] for _ in range(3)]

    
    label_t = Label(window_ttt,
                  text=f"It is {player}'s turn", 
                  font=("Comic Sans", 20),
                  fg="black",
                  bg=bgcolor)
    label_t.pack(side="top")

    label_tmode = Label(window_ttt,
                        text=f"MODE: {data_mode}",
                        font=("Comic Sans", 20),
                        fg="black",
                        bg=bgcolor)
    label_tmode.pack(side="top")

    
    def change_mode():
        
        with open(jsonpath, "r") as f:
            data = json.load(f)

        with open(jsonpath, "w") as f:

            if data["MODE"] == "LOCAL":
                data["MODE"] = "COMPUTER"
                json.dump(data, f, indent=4)
                label_tmode.config(text=f"MODE: {data['MODE']}")
            
            elif data["MODE"] == "COMPUTER":
                data["MODE"] = "LOCAL"
                json.dump(data, f, indent=4)
                label_tmode.config(text=f"MODE: {data['MODE']}")
            
            else:
                json.dumps(default_json)
                label_tmode.config(text=f"MODE: {data['MODE']}")
        

    change_mode_button = Button(window_ttt,
                                text="Change mode",
                                font=("Comic Sans", 20),
                                command=change_mode)
    change_mode_button.pack(side="top")
    
    def newgame():
       nonlocal player
       create_buttons()
       label_t.config(text=f"It is {player}'s turn")

    reset_button = Button(window_ttt,
                          text="Restart game",
                          font=("Comic Sans", 20),
                          command=newgame)
    reset_button.pack(side="top")

    frame = Frame(window_ttt)
    frame.pack()

    def make_move(row, column):
        nonlocal player

        data = read_mode()
        data_mode = data["MODE"]

        def check_winner_or_tie(player):

            if check_winner(buttons):
                label_t.config(text=(f"{player} has won the game"))
                return True
            
            elif not empty_spaces(buttons):
                label_t.config(text=("It is a tie"))
                return True
            
            return False

        if buttons[row][column]["text"] == "" and not check_winner(buttons):
            buttons[row][column]["text"] = player

            if data_mode == "COMPUTER":
                computer = players.copy()
                computer.remove(player)
                computer = computer[0]

                if check_winner_or_tie(player):
                    return

                for row in range(3):
                    for column in range(3):
                        if buttons[row][column]["text"] == "":
                            buttons[row][column]["text"] = computer
                            if check_winner_or_tie(computer):
                                return
                            return

            if check_winner_or_tie(player):
                return

            player = players[1] if player == players[0] else players[0]
            label_t.config(text=(f"It is {player}'s turn"))

    def create_buttons(): 
        for row in range(3):
            for column in range(3):
                buttons[row][column] = Button(frame, 
                                            text="",
                                            font=("Comic Sans", 40),
                                            width=5,
                                            height=2,
                                            command=lambda row=row, column=column: make_move(row, column))
                buttons[row][column].grid(row=row, column=column)
    
    create_buttons()

    def check_winner(buttons):
        for row in range(3):
            if buttons[row][0]["text"] == buttons[row][1]["text"] == buttons[row][2]["text"] != "":
                buttons[row][0].config(bg="green")
                buttons[row][1].config(bg="green")
                buttons[row][2].config(bg="green")
                return True
            
        for column in range(3):
            if buttons[0][column]["text"] == buttons[1][column]["text"] == buttons[2][column]["text"] != "":
                buttons[0][column].config(bg="green")
                buttons[1][column].config(bg="green")
                buttons[2][column].config(bg="green")
                return True
            
        if buttons[0][0]["text"] == buttons[1][1]["text"] == buttons[2][2]["text"] != "":
            buttons[0][0].config(bg="green")
            buttons[1][1].config(bg="green")
            buttons[2][2].config(bg="green")
            return True
        
        elif buttons[0][2]["text"] == buttons[1][1]["text"] == buttons[2][0]["text"] != "":
            buttons[0][2].config(bg="green")
            buttons[1][1].config(bg="green")
            buttons[2][0].config(bg="green")
            return True
        
        elif not empty_spaces(buttons):
            for row in range(3):
                for column in range(3):
                    buttons[row][column].config(bg="orange")
            return False
            
    def empty_spaces(buttons):
        spaces = 9
        for row in range(3):
            for column in range(3):
                if buttons[row][column]["text"] != "":
                    spaces -= 1
        return spaces > 0

    window_ttt.mainloop()

if __name__ == "__main__":
    create_files()
    main()
