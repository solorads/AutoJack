import customtkinter as ctk
import inflect
import pyautogui as pg
import pydirectinput as pd
import time
from CTkMessagebox import CTkMessagebox
from pynput.keyboard import Listener, Key
import threading
import webbrowser  # To open the URL when clicked

# Initialize inflect engine
p = inflect.engine()

# Global flag for stopping the script
should_stop = False

# Create UI
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

app = ctk.CTk()
app.geometry("400x500")
app.title("Grammar & Hell Jacks")

# --- Widgets ---
label_title = ctk.CTkLabel(app, text="Jack Automation", font=("Arial", 22))
label_title.pack(pady=10)

entry_num = ctk.CTkEntry(app, placeholder_text="How many jacks?", width=200)
entry_num.pack(pady=10)

mode_dropdown = ctk.CTkOptionMenu(app, values=["Grammar Jacks", "Hell Jacks"])
mode_dropdown.set("Grammar Jacks")
mode_dropdown.pack(pady=10)

entry_custom = ctk.CTkEntry(app, placeholder_text="Hell Jack prefix (e.g., O)", width=200)
entry_custom.pack(pady=10)

# Option checkboxes
exclam_var = ctk.BooleanVar()
exclam_check = ctk.CTkCheckBox(app, text="Add exclamation (!)", variable=exclam_var)
exclam_check.pack(pady=(5, 2))

# Spacer
spacer = ctk.CTkLabel(app, text="")
spacer.pack(pady=(0, 2))

case_var = ctk.BooleanVar()
case_check = ctk.CTkCheckBox(app, text="Use lowercase", variable=case_var)
case_check.pack(pady=(2, 5))

# Delay slider
delay_slider = ctk.CTkSlider(app, from_=0.1, to=2, number_of_steps=19, width=200)
delay_slider.set(1)
delay_slider.pack(pady=10)
ctk.CTkLabel(app, text="Delay per message (seconds)").pack()

# --- Script ---
def start_script():
    global should_stop
    should_stop = False  # Reset the stop flag before starting

    try:
        # Validate input for number of jacks
        count = entry_num.get()
        if not count.isdigit() or int(count) <= 0:
            CTkMessagebox(title="Invalid Input", message="Please enter a valid number greater than 0.", icon="cancel")
            return
        
        count = int(count)
        
        mode = mode_dropdown.get()
        prefix = entry_custom.get().strip()
        use_lower = case_var.get()
        use_exclam = exclam_var.get()
        delay = delay_slider.get()

        msgbox = CTkMessagebox(title="Ready?", message="Switch to Roblox and click Begin.",
                               icon="info", option_1="Begin", option_2="Cancel")
        if msgbox.get() != "Begin":
            return

        for i in range(1, count + 1):
            if should_stop:
                print("Script stopped.")
                return  # Stop the script if the flag is set

            word = p.number_to_words(i)

            # Convert case
            word = word.lower() if use_lower else word.upper()

            # Add exclamation if selected
            if use_exclam:
                word += "!"

            if mode == "Grammar Jacks":
                time.sleep(delay)
                pd.press('/')
                pg.typewrite(word)
                pd.press('enter')
                pd.press('space')

            elif mode == "Hell Jacks":
                # Remove non-alphabetic characters
                cleaned_word = ''.join(c for c in word if c.isalpha())
                for letter in cleaned_word:
                    if should_stop:
                        print("Script stopped.")
                        return  # Stop the script if the flag is set

                    msg = f"{prefix} {letter}" if prefix else letter
                    time.sleep(delay)
                    pd.press('/')
                    pg.typewrite(msg)
                    pd.press('enter')
                    pd.press('space')

        CTkMessagebox(title="Done", message="Jack script finished!", icon="check")

    except Exception as e:
        CTkMessagebox(title="Error", message=f"Something went wrong:\n{e}", icon="cancel")

# Start Button
start_btn = ctk.CTkButton(app, text="Start", command=lambda: threading.Thread(target=start_script).start())
start_btn.pack(pady=30)

# --- Keybinding Logic ---
def on_press(key):
    global should_stop
    try:
        if key.char == 'j':  # Start the script when 'J' is pressed
            print("Starting script...")
            threading.Thread(target=start_script).start()  # Start the script in a new thread

        elif key.char == 'n':  # Stop the script when 'N' is pressed
            should_stop = True  # Set the stop flag
            print("Stopping script...")
    except AttributeError:
        pass  # Handle special keys like shift, etc.

# Start listening for key events in a non-blocking way
listener = Listener(on_press=on_press)
listener.start()

# --- URL Label ---
def open_url(event):
    webbrowser.open("https://solorads.site")  # Open the URL when the label is clicked

url_label = ctk.CTkLabel(app, text="made by solorads", font=("Arial", 23, "underline"), fg_color="transparent")
url_label.pack(pady=20)
url_label.bind("<Button-1>", open_url)  # Bind left mouse click to open URL

app.mainloop()
