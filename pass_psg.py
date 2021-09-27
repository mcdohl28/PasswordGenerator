"""
    The module creates a UI and runs a random generated password at 10 secs interval.
"""
import os
import logging
from logging import handlers
import random
import time
import PySimpleGUI as sg
import pyperclip


# Check for path exist.
if not os.path.exists('log'):
    os.makedirs('log')

logger = logging.getLogger('password-generator-app')
logger.setLevel(logging.DEBUG)

# Define log format
formatter = logging.Formatter('[%(asctime)s] - %(levelname)s - %(message)s')

# Setting log file location, when to rotate the log and number of files to keep.
logHandler = handlers.TimedRotatingFileHandler('log/pass-psg.log',
                                               when='midnight',
                                               interval=1,
                                               backupCount=7)
logHandler.setLevel(logging.DEBUG)

# Set our logHandler's formatter
logHandler.setFormatter(formatter)
logger.addHandler(logHandler)

CONST_TIMER = 10

sg.theme("Dark2")

# ---- Define the column layout ----
input_column = [
    [
        sg.Text('Random 16 character password: '),
        sg.InputText(key="-TEXTBOX-", disabled=True),
        sg.Text('', key="-TEXT-"),
        sg.Button("copy", key="-COPY-"),
     ]
]

timer_column = [
    [
        sg.ProgressBar(1000, orientation='h', size=(20, 20), key='progressbar')
    ]
]

# ---- full layout -----
layout = [
    input_column
]

# create the window
window = sg.Window("Password Generator Demo", layout, margins=(100, 50), finalize=True)

secs = CONST_TIMER
progress_count = 0


def generate_password():
    """
    The function returns a random generated password.
    :return: a random password
    """

    lower = "abcdefghijklmnopqrstuvwxyz"
    upper = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    numbers = "0123456789"
    symbols = "[]{}()*;/,_-"
    combination = lower + upper + numbers + symbols
    length = 16
    password = "".join(random.sample(combination, length))
    logger.debug("[+] Generated Password:" + password)
    return password


# create an event loop
while True:
    event, values = window.read(timeout=CONST_TIMER)
    # End program if user closes window or

    # presses the certain button for certain event.
    if event in ("Exit", sg.WIN_CLOSED):
        logger.info("[+] event[-exit-] is triggered.")
        break
    if event == "-GENERATE-":
        logger.info("[+] event[-generate-] is triggered.")
        generated_password = generate_password()
        window['-TEXTBOX-'].update(generated_password)
        logger.info("[+] event[-generate-] ended.")
    if event == "-COPY-":
        logger.info("[+] event[-copy-] is triggered.")
        copied_text = window.Element('-TEXTBOX-').get()
        pyperclip.copy(copied_text)
        logger.info("[+] event[-copy-] Text value copied.")
        logger.info("[+] event[-copy-] ended.")
    if event == sg.TIMEOUT_KEY:
        if secs == CONST_TIMER:
            generated_password = generate_password()
            window['-TEXTBOX-'].update(generated_password)
        time.sleep(1)
        secs = secs-1
        window['-TEXT-'].update(secs)
        if secs == 0:
            secs = CONST_TIMER
        continue

window.close()
