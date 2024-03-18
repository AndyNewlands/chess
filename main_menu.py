import tkinter as tk

def rapid():
    game_type.pack_forget()
    rapid_button.pack_forget()
    bullet_button.pack_forget()
    blitz_button.pack_forget()
    game_length = tk.Label(main_frame, text="What do you want the timer to show?", font=("Arial",11))
    game_length.pack()
    ten_min_button = tk.Button(main_frame, text="10 minutes", font=("Arial", 10), command=lambda : [set_opponent_rapid(game_length, ten_min_button, thirty_min_button), ispressed("10")])
    ten_min_button.pack()
    thirty_min_button = tk.Button(main_frame, text="30 minutes", font=("Arial", 10), command=lambda : [set_opponent_rapid(game_length, ten_min_button, thirty_min_button), ispressed("30")])
    thirty_min_button.pack()

def bullet():
    game_type.pack_forget()
    rapid_button.pack_forget()
    bullet_button.pack_forget()
    blitz_button.pack_forget()
    game_length = tk.Label(main_frame, text="What do you want the timer to show?", font=("Arial",11))
    game_length.pack()
    one_min_button = tk.Button(main_frame, text="1 minute", font=("Arial", 10), command=lambda : [set_opponent_bullet(game_length, one_min_button, two_min_button), ispressed("1")])
    one_min_button.pack()
    two_min_button = tk.Button(main_frame, text="2 minutes", font=("Arial", 10), command=lambda : [set_opponent_bullet(game_length, one_min_button, two_min_button), ispressed("2")])
    two_min_button.pack()

def blitz():
    game_type.pack_forget()
    rapid_button.pack_forget()
    bullet_button.pack_forget()
    blitz_button.pack_forget()
    game_length = tk.Label(main_frame, text="What do you want the timer to show?", font=("Arial",11))
    game_length.pack()
    three_min_button = tk.Button(main_frame, text="3 minutes", font=("Arial", 10), command=lambda : [set_opponent_blitz(game_length, three_min_button, five_min_button), ispressed("3")])
    three_min_button.pack()
    five_min_button = tk.Button(main_frame, text="5 minutes", font=("Arial", 10), command=lambda : [set_opponent_blitz(game_length, three_min_button, five_min_button), ispressed("5")])
    five_min_button.pack()

def ispressed(timer):
    return timer

def addsettings():
    main_frame.pack_forget()
    addsettings_frame.pack()

def details():
    main_frame.pack_forget()
    details_frame.pack()
    #username_label = tk.Label(main_frame, text=("Username", username), font=("Arial", 10)).pack()

def addset_to_menu():
    addsettings_frame.pack_forget()
    main_frame.pack()

def details_to_menu():
    details_frame.pack_forget()
    main_frame.pack()

def set_opponent_rapid(length, ten_button, thirty_button):
    length.pack_forget()
    ten_button.pack_forget()
    thirty_button.pack_forget()
    opponent_label = tk.Label(main_frame, text="Select AI Bot: ", font=("Arial", 10)).pack()

def set_opponent_bullet(length, one_button, two_button):
    length.pack_forget()
    one_button.pack_forget()
    two_button.pack_forget()
    opponent_label = tk.Label(main_frame, text="Select AI Bot: ", font=("Arial", 10)).pack()

def set_opponent_blitz(length, three_button, five_button):
    length.pack_forget()
    three_button.pack_forget()
    five_button.pack_forget()
    opponent_label = tk.Label(main_frame, text="Select AI Bot: ", font=("Arial", 10)).pack()

window = tk.Tk()
window.title("Main menu")
window.geometry("500x500")
window.resizable(True, True)

main_frame = tk.Frame(window)
main_frame.pack()

game_type = tk.Label(main_frame, text="What type of chess game do you want to play?", font=("Arial", 11))
game_type.pack()
rapid_button = tk.Button(main_frame, text="Rapid", font=("Arial", 10), command=rapid)
rapid_button.pack()
bullet_button = tk.Button(main_frame, text="Bullet", font=("Arial", 10), command=bullet)
bullet_button.pack()
blitz_button = tk.Button(main_frame, text="Blitz", font=("Arial", 10), command=blitz)
blitz_button.pack()

play_button = tk.Button(main_frame, text="Play", font=("Arial", 10)).pack(side='bottom')
additional_settings = tk.Button(main_frame, text="Additional Settings", font=("Arial", 10), command=addsettings).pack(side='bottom')
account_details = tk.Button(main_frame, text="Account Details", font=("Arial", 10), command=details).pack(side='bottom')

addsettings_frame = tk.Frame(window)
change_style = tk.Label(addsettings_frame, text="Change the style of the pieces", font=("Arial",10)).pack()
change_chessboard = tk.Label(addsettings_frame, text="Change the style of the chessboard", font=("Arial",10)).pack()
return_to_menu = tk.Button(addsettings_frame, text="Return to main menu", font=("Arial",10), command=addset_to_menu).pack()

details_frame = tk.Frame(window)

window.mainloop()
