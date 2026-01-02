import tkinter as tk
import math

# ---------- Main Window ----------
root = tk.Tk()
root.title("Advanced Scientific Calculator")

# Mobile-style centered window
width, height = 360, 640
x = (root.winfo_screenwidth() - width) // 2
y = (root.winfo_screenheight() - height) // 2
root.geometry(f"{width}x{height}+{x}+{y}")
root.configure(bg="#121212")
root.resizable(False, False)

# ---------- Variables ----------
expression = ""
display = tk.StringVar()
mode = tk.StringVar(value="DEG")  # DEG or RAD

# ---------- Core Functions ----------
def press(value):
    global expression
    expression += str(value)
    display.set(expression)


def clear():
    global expression
    expression = ""
    display.set("")


def backspace():
    global expression
    expression = expression[:-1]
    display.set(expression)


def calculate():
    global expression
    try:
        result = eval(expression)
        display.set(result)
        expression = str(result)
    except:
        display.set("Error")
        expression = ""

# ---------- Degree / Radian ----------
def toggle_mode():
    if mode.get() == "DEG":
        mode.set("RAD")
    else:
        mode.set("DEG")


def apply_trig(func):
    global expression
    try:
        value = float(expression)
        if mode.get() == "DEG":
            value = math.radians(value)
        result = func(value)
        display.set(result)
        expression = str(result)
    except:
        display.set("Error")
        expression = ""

# ---------- Math Operations ----------
def sqrt(): apply_math(math.sqrt)
def square(): apply_math(lambda x: x * x)
def log10(): apply_math(math.log10)
def ln(): apply_math(math.log)
def factorial(): apply_math(lambda x: math.factorial(int(x)))
def percentage(): apply_math(lambda x: x / 100)


def apply_math(func):
    global expression
    try:
        result = func(float(expression))
        display.set(result)
        expression = str(result)
    except:
        display.set("Error")
        expression = ""

# ---------- Keyboard Support with Highlight ----------
def key_input(event):
    key = event.char
    if key in '0123456789.+-*/':
        press(key)
    elif event.keysym == 'Return':
        calculate()
    elif event.keysym == 'BackSpace':
        backspace()
    elif event.keysym == 'Escape':
        clear()

root.bind('<Key>', key_input)

# ---------- Display ----------
entry = tk.Entry(
    root, textvariable=display,
    font=("Consolas", 22),
    bg="#000000", fg="#00ffcc",
    insertbackground="white",
    bd=0, justify="right"
)
entry.pack(fill="x", padx=12, pady=20, ipady=14)

# ---------- Mode Button ----------
mode_btn = tk.Button(
    root, textvariable=mode,
    font=("Arial", 11),
    bg="#333", fg="white",
    bd=0, command=toggle_mode
)
mode_btn.pack(pady=4)

# ---------- Button Factory ----------
def create_button(text, cmd, r, c, bg="#2a2a2a"):
    btn = tk.Button(
        btn_frame, text=text,
        width=6, height=2,
        font=("Arial", 12),
        bg=bg, fg="white",
        activebackground="#00adb5",
        bd=0, command=cmd
    )
    btn.grid(row=r, column=c, padx=6, pady=6)
    return btn

# ---------- Buttons Layout ----------
btn_frame = tk.Frame(root, bg="#121212")
btn_frame.pack()

buttons = [
    ("C", clear, "#d9534f"), ("⌫", backspace, "#f0ad4e"), ("π", lambda: press(math.pi), "#6f42c1"), ("e", lambda: press(math.e), "#6f42c1"),
    ("sin", lambda: apply_trig(math.sin), "#6f42c1"), ("cos", lambda: apply_trig(math.cos), "#6f42c1"), ("tan", lambda: apply_trig(math.tan), "#6f42c1"), ("/", lambda: press('/'), "#5bc0de"),
    ("ln", ln, "#6f42c1"), ("log", log10, "#6f42c1"), ("x!", factorial, "#6f42c1"), ("", lambda: press(''), "#5bc0de"),
    ("7", lambda: press(7), "#2a2a2a"), ("8", lambda: press(8), "#2a2a2a"), ("9", lambda: press(9), "#2a2a2a"), ("-", lambda: press('-'), "#5bc0de"),
    ("4", lambda: press(4), "#2a2a2a"), ("5", lambda: press(5), "#2a2a2a"), ("6", lambda: press(6), "#2a2a2a"), ("+", lambda: press('+'), "#5bc0de"),
    ("1", lambda: press(1), "#2a2a2a"), ("2", lambda: press(2), "#2a2a2a"), ("3", lambda: press(3), "#2a2a2a"), ("=", calculate, "#00adb5"),
    ("0", lambda: press(0), "#2a2a2a"), (".", lambda: press('.'), "#2a2a2a"), ("√", sqrt, "#6f42c1"), ("x²", square, "#6f42c1")
]

row = col = 0
for text, cmd, color in buttons:
    create_button(text, cmd, row, col, color)
    col += 1
    if col > 3:
        col = 0
        row += 1

# ---------- Run ----------
root.mainloop()