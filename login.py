import tkinter as tk
from MVIS import main_window
import ttkbootstrap as ttk

def open_main_window():
    main_window()

def message_box(message, callback):
    message_box = tk.Toplevel(login_window)
    message_box.title("Message")
    
    # Increase the size by adjusting width and height
    message_box.geometry("400x200")
    
    # You can add other widgets to customize the content of the message box
    label = ttk.Label(message_box, text=message, padding=10)
    label.pack()

    # OK button with callback
    ok_button = ttk.Button(message_box, text="OK", command=lambda: callback(message_box))
    ok_button.pack()

def validate_login():
    username = entry_username.get()
    password = entry_password.get()

    # Check if the username and password are valid (replace this with your authentication logic)
    if username == "user" and password == "password":
        def open_main_after_ok(message_box):
            message_box.destroy()  # Close the message box
            login_window.destroy()  # Close the login window
            open_main_window()  # Open the main window

        message_box("Login Successful, Welcome, {}".format(username), open_main_after_ok)
    else:
        message_box("Login Failed, Invalid username or password", lambda _: None)

# Create the login window
login_window = ttk.Window(themename="superhero")
login_window.title("Login Window")

# Center the window on the screen
window_width = 400
window_height = 400
screen_width = login_window.winfo_screenwidth()
screen_height = login_window.winfo_screenheight()
x_position = (screen_width - window_width) // 2
y_position = (screen_height - window_height) // 2

login_window.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

# Create and place widgets in the login window
frame = ttk.Frame(login_window, padding="20")
frame.grid(row=0, column=0, padx=70, pady=70, sticky=(tk.W, tk.E, tk.N, tk.S))

# Center the labels and entry widgets
frame.columnconfigure(0, weight=1)
frame.columnconfigure(1, weight=1)

label_username = ttk.Label(frame, text="Username:")
label_username.grid(row=0, column=0, padx=10, pady=10, sticky=tk.W)

entry_username = ttk.Entry(frame)
entry_username.grid(row=0, column=1, padx=10, pady=10, sticky=tk.E)

label_password = ttk.Label(frame, text="Password:")
label_password.grid(row=1, column=0, padx=10, pady=10, sticky=tk.W)

entry_password = ttk.Entry(frame, show="*")  # show="*" to hide the password
entry_password.grid(row=1, column=1, padx=10, pady=10, sticky=tk.E)

button_login = ttk.Button(frame, text="Login", command=validate_login)
button_login.grid(row=2, column=0, columnspan=2, pady=10)

# Run the main loop for the login window
login_window.mainloop()
