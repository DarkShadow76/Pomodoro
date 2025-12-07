from tkinter import *
import math
from pydub import AudioSegment
from pydub.playback import play

# ---------------------------- CONSTANTS ------------------------------- #
PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
FONT_NAME = "fixed"
WORK_MIN = 0.5
SHORT_BREAK_MIN = 0.3
LONG_BREAK_MIN = 0.2
reps = 0
timer = None

# ---------------------------- SOUND SETUP ------------------------------- #
ALARM_SOUND = None

try:
    ALARM_SOUND = AudioSegment.from_wav("Hey_listen.wav")
except Exception as e:
    print("Error loading sound file:", e)

# ---------------------------- SOUND PLAYER ------------------------------- #
def play_alarm():
    if ALARM_SOUND:
        play(ALARM_SOUND)
    else: 
        window.bell()

# ---------------------------- TIMER RESET ------------------------------- #


def reset_timer():
    window.after_cancel(timer)
    canvas.itemconfig(timer_text, text="00:00")
    title_label.config(text="Timer")
    check_marks.config(text="")
    global reps
    reps = 0


# ---------------------------- TIMER MECHANISM ------------------------------- #


def start_timer():
    global reps
    reps += 1

    work_sec = WORK_MIN * 60
    short_break_sec = SHORT_BREAK_MIN * 60
    long_break_sec = LONG_BREAK_MIN * 60

    if reps % 8 == 0:
        count_down(long_break_sec)
        title_label.config(text="Long Break", fg=RED)
        check_marks.config(text=f"Session: {reps}/8")
    elif reps % 2 == 0:
        count_down(short_break_sec)
        title_label.config(text="Break", fg=PINK)
        check_marks.config(text=f"Session: {reps}/2")
    else:
        count_down(work_sec)
        title_label.config(text="Work", fg=GREEN)


# ---------------------------- COUNTDOWN MECHANISM ------------------------------- #


def count_down(count):
    count_min = math.floor(count / 60)
    count_sec = count % 60

    if count_sec < 10:
        count_sec = f"0{count_sec}"

    canvas.itemconfig(timer_text, text=f"{count_min}:{count_sec}")
    if count > 0:
        global timer
        timer = window.after(1000, count_down, count - 1)
    else:
        start_timer()
        marks = ""
        work_session = math.floor(reps / 2)
        for _ in range(work_session):
            marks += "✔"
        check_marks.config(text=marks)

        play_alarm()

# ---------------------------- UI SETUP ------------------------------- #


window = Tk()
window.title("Pomodoro")
window.config(
    padx=20,
    pady=20,
    bg=YELLOW,
)
window.after(
    1000,
)
##window.geometry("450x450")

window.resizable(False, False)

title_label = Label(text="Timer", fg=GREEN, bg=YELLOW, font=(FONT_NAME, 35, "bold"))
title_label.grid(column=1, row=0)

##title_label.pack(pady=50)

tomato_img = PhotoImage(file="tomato.png")

fg = GREEN

canvas = Canvas(width=200, height=224, bg=YELLOW, highlightthickness=0)

canvas.create_image(100, 112, image=tomato_img)
timer_text = canvas.create_text(
    100, 130, text="00:00", fill="white", font=(FONT_NAME, 35, "bold")
)
canvas.grid(column=1, row=1)

start_button = Button(
    text="Start",
    highlightthickness=0,
    command=start_timer,
    font=(FONT_NAME, 50)
    )
start_button.grid(column=0, row=2)

reset_button = Button(
    text="Reset",
    highlightthickness=0,
    command=reset_timer,
    font=(FONT_NAME, 50)
    )
reset_button.grid(column=2, row=2)

check_marks = Label(fg=GREEN, bg=YELLOW,font=(FONT_NAME, 30))
check_marks.grid(column=1, row=3)

#count_down(0)
start_timer()

import tkinter.font as tkFont

available_fonts = tkFont.families()
print("--- Available Font Families ---")
print(available_fonts)

window.mainloop()
