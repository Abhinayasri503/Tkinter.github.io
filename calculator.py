import tkinter as tk
import math

# ================= WINDOW =================
root = tk.Tk()
root.title("Scientific Calculator")
root.geometry("380x650")
root.configure(bg="#121212")
root.resizable(False, False)

# ================= VARIABLES =================
expression = ""
memory = 0
mode = tk.StringVar(value="DEG")
display = tk.StringVar()

# ================= SAFE FUNCTIONS =================
def sin(x): return math.sin(math.radians(x)) if mode.get() == "DEG" else math.sin(x)
def cos(x): return math.cos(math.radians(x)) if mode.get() == "DEG" else math.cos(x)
def tan(x): return math.tan(math.radians(x)) if mode.get() == "DEG" else math.tan(x)

allowed = {
    "sin": sin,
    "cos": cos,
    "tan": tan,
    "sqrt": math.sqrt,
    "log": math.log10,
    "ln": math.log,
    "pi": math.pi,
    "e": math.e,
    "pow": pow,
    "factorial": math.factorial
}

# ================= CORE FUNCTIONS =================
def press(val):
    global expression
    expression += str(val)
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
        result = eval(expression, {"__builtins__": None}, allowed)
        display.set(result)
        expression = str(result)
    except:
        display.set("Error")
        expression = ""

# ================= MODE =================
def toggle_mode():
    mode.set("RAD" if mode.get() == "DEG" else "DEG")

# ================= MEMORY =================
def mem_clear():
    global memory
    memory = 0

def mem_add():
    global memory
    memory += float(display.get() or 0)

def mem_sub():
    global memory
    memory -= float(display.get() or 0)

def mem_recall():
    press(memory)

# ================= DISPLAY =================
entry = tk.Entry(
    root, textvariable=display,
    font=("Consolas", 24),
    bg="#000", fg="#00ffcc",
    justify="right", bd=0
)
entry.pack(fill="x", padx=12, pady=20, ipady=15)

tk.Button(root, textvariable=mode, command=toggle_mode,
          bg="#333", fg="white", bd=0).pack(pady=5)

# ================= BUTTONS =================
frame = tk.Frame(root, bg="#121212")
frame.pack()

def btn(text, cmd, r, c, color="#2a2a2a"):
    tk.Button(
        frame, text=text, command=cmd,
        font=("Arial", 12),
        width=6, height=2,
        bg=color, fg="white", bd=0
    ).grid(row=r, column=c, padx=6, pady=6)

buttons = [
    ("MC", mem_clear), ("MR", mem_recall), ("M+", mem_add), ("M-", mem_sub),
    ("C", clear, "#dc3545"), ("⌫", backspace, "#ffc107"),
    ("(", lambda: press("(")), (")", lambda: press(")")),

    ("sin", lambda: press("sin(")), ("cos", lambda: press("cos(")),
    ("tan", lambda: press("tan(")), ("/", lambda: press("/")),

    ("7", lambda: press(7)), ("8", lambda: press(8)),
    ("9", lambda: press(9)), ("*", lambda: press("*")),

    ("4", lambda: press(4)), ("5", lambda: press(5)),
    ("6", lambda: press(6)), ("-", lambda: press("-")),

    ("1", lambda: press(1)), ("2", lambda: press(2)),
    ("3", lambda: press(3)), ("+", lambda: press("+")),

    ("0", lambda: press(0)), (".", lambda: press(".")),
    ("π", lambda: press("pi")), ("=", calculate, "#00adb5"),

    ("√", lambda: press("sqrt(")), ("x²", lambda: press("**2")),
    ("xʸ", lambda: press("**")), ("!", lambda: press("factorial(")),

    ("log", lambda: press("log(")), ("ln", lambda: press("ln(")),
    ("e", lambda: press("e")), ("%", lambda: press("/100"))
]

r = c = 0
for b in buttons:
    if len(b) == 3:
        btn(b[0], b[1], r, c, b[2])
    else:
        btn(b[0], b[1], r, c)
    c += 1
    if c == 4:
        c = 0
        r += 1

# ================= KEYBOARD =================
def key_input(e):
    if e.char in "0123456789.+-*/()":
        press(e.char)
    elif e.keysym == "Return":
        calculate()
    elif e.keysym == "BackSpace":
        backspace()
    elif e.keysym == "Escape":
        clear()

root.bind("<Key>", key_input)

# ================= RUN =================
root.mainloop()
