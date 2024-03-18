import tkinter as tk

#Creating a blank dictionary
registration = {}

def register(username, password):

  #array of "special" characters for passwords
  characters = [",", ".", ":", "!", "?", "(", ")" ]

  #checks for the needed requirements for the password
  if len(password) < 8:
    failed_registration = tk.Label(register_frame, text="Registration Failed - Password too short!", font=("Arial", 12)).pack()
    return

  if not any(i.isupper() for i in password):
    failed_registration = tk.Label(register_frame, text="Registration Failed - No capital letters in password", font=("Arial", 12)).pack()
    return

  if not any(i in characters for i in password):
    failed_registration = tk.Label(register_frame, text="Registration Failed - No special characters, such as ,.:!?(), in password!", font=("Arial", 12)).pack()
    return

  #checks if another user already has the same username
  if username in registration:
    failed_registration = tk.Label(register_frame, text="Username is already taken - Please try again!", font=("Arial", 12)).pack()
  else:
    #assigns the password to the username
    registration[username] = password
    successful_registration = tk.Label(register_frame, text="Registration Successful", font=("Arial", 12)).pack()

def login(username, password):

  #checks if the credentials the user has entered are valid
  if username not in registration or registration[username] != password:
    failed_login = tk.Label(login_frame, text="Login Failed - Please try again!", font=("Arial", 12)).pack()
  else:
    successful_login = tk.Label(login_frame, text="Login Successful", font=("Arial", 12)).pack()

def change_to_login():
  #deletes the main frame and switches it to the login frame
  main_frame.pack_forget()
  login_frame.pack()

def change_to_register():
  #deletes the main frame and switches it to the register frame
  main_frame.pack_forget()
  register_frame.pack()

def change_from_l_to_r():
  #deletes the login frame and switches it to the register frame
  login_frame.pack_forget()
  register_frame.pack()

def change_from_r_to_l():
  #deletes the register frame and switches it to the login frame
  register_frame.pack_forget()
  login_frame.pack()

#creates a blank window called "Welcome Screen"
window = tk.Tk()
window.title("Welcome Screen")
window.geometry("500x500")
window.resizable(True, True)

#creates a new frame called "main_frame" within the window
main_frame = tk.Frame(window)
main_frame.pack()

title_label = tk.Label(main_frame, text="Welcome to Chess AI", font=("Arial", 18), padx=50, pady=20).pack()

empty_label = tk.Label(main_frame, text=" ", padx=10, pady=5).pack()

question_label = tk.Label(main_frame, text="Are you logged into the system?", font=("Arial", 14), padx=50, pady=20).pack()

left_space = tk.Label(main_frame, text=" ").pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
right_space = tk.Label(main_frame, text=" ").pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

yes_button = tk.Button(main_frame, text="Yes", font=("Arial", 12), padx=20, pady=10, command=change_to_login)
yes_button.pack(side=tk.LEFT)

no_button = tk.Button(main_frame, text="No", font=("Arial", 12), padx=20, pady=10, command=change_to_register)
no_button.pack(side=tk.LEFT)

#creates a new frame called "login_frame" within the window
login_frame = tk.Frame(window)
existing_username_label = tk.Label(login_frame, text="Username: ", font=("Arial", 12)).pack()
existing_username_entry = tk.Entry(login_frame)
existing_username_entry.pack()
empty_label1 = tk.Label(login_frame, text=" ", padx=10, pady=5).pack()
existing_password_label = tk.Label(login_frame, text="Password: ", font=("Arial", 12)).pack()
existing_password_entry = tk.Entry(login_frame, show="*")
existing_password_entry.pack()
empty_label2 = tk.Label(login_frame, text=" ", padx=10, pady=10).pack()
login_button = tk.Button(login_frame, text="Login", font=("Arial", 12), padx=20, pady=10, command=lambda: login(existing_username_entry.get(), existing_password_entry.get())).pack()
emptylabel3 = tk.Label(login_frame, text=" ", padx=10, pady=30).pack()
switch_to_r_label = tk.Label(login_frame, text="Forgot to register?", font=("Arial", 8)).pack()
switch_to_r_button = tk.Button(login_frame, text="Register", font=("Arial", 8), command=change_from_l_to_r).pack()

#creates a new frame called "register_frame" within the window
register_frame = tk.Frame(window)
new_username_label = tk.Label(register_frame, text="Username: ", font=("Arial", 12)).pack()
new_username_entry = tk.Entry(register_frame)
new_username_entry.pack()
empty_label4 = tk.Label(register_frame, text=" ", padx=10, pady=5).pack()
new_password_label = tk.Label(register_frame, text="Password: ", font=("Arial", 12)).pack()
new_password_entry = tk.Entry(register_frame, show="*")
new_password_entry.pack()
empty_label5 = tk.Label(register_frame, text=" ", padx=10, pady=10).pack()
register_button = tk.Button(register_frame, text="Register", font=("Arial", 12), padx=20, pady=10, command=lambda: register(new_username_entry.get(), new_password_entry.get())).pack()
emptylabel6 = tk.Label(register_frame, text=" ", padx=10, pady=30).pack()
switch_to_l_label = tk.Label(register_frame, text="Have you already logged in?", font=("Arial", 8)).pack()
switch_to_l_button = tk.Button(register_frame, text="Login", font=("Arial", 8), command=change_from_r_to_l).pack()

#calls the window
window.mainloop()
