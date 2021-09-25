import PySimpleGUI as sg
import pyperclip
import random


def generate_password():
    lower = "abcdefghijklmnopqrstuvwxyz"
    upper = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    numbers = "0123456789"
    symbols = "[]{}()*;/,_-"
    all = lower + upper + numbers + symbols
    length = 16
    password = "".join(random.sample(all, length))
    print("Generated Password:" + password)
    return password


sg.theme("DarkBlue")
input_columns = [
    [
        sg.Button("Generate password", key="-GENERATE-"),
        sg.InputText(key="-TEXTBOX-"),
        sg.Button("copy", key="-COPY-"),
     ]
]

# ---- full layout -----
layout = [
    input_columns
]

# create the window
window = sg.Window("Password Generator Demo", layout, margins=(100, 50))

# create an event loop
while True:
    event, values = window.read()
    # End program if user closes window or
    # presses the OK button
    if event == "Exit" or event == sg.WIN_CLOSED:
        print("event[-exit-] is triggered.")
        break
    if event == "-GENERATE-":
        print("event[-generate-] is triggered.")
        generated_password = generate_password()
        window.Element('-TEXTBOX-').update(generated_password)
        print("event[-generate-] ended.")
    if event == "-COPY-":
        print("event[-copy-] is triggered.")
        copied_text = window.Element('-TEXTBOX-').get()
        pyperclip.copy(copied_text)
        print("event[-copy-] Text value copied.")
        print("event[-copy-] ended.")

window.close()
