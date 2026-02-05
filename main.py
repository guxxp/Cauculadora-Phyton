import tkinter as tk
from tkinter import font
import math

class ModernCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Antigravity Calculator")
        self.root.geometry("350x550")
        self.root.configure(bg="#1e1e1e")
        self.root.resizable(False, False)

        self.expression = ""
        self.display_text = tk.StringVar()
        self.display_text.set("0")

        self.create_widgets()

    def create_widgets(self):
        # Display Area
        display_frame = tk.Frame(self.root, bg="#1e1e1e", height=150)
        display_frame.pack(expand=True, fill="both")

        # Previous expression (smaller)
        self.prev_label = tk.Label(
            display_frame, 
            text="", 
            font=("Inter", 12), 
            bg="#1e1e1e", 
            fg="#888888", 
            anchor="e"
        )
        self.prev_label.pack(expand=True, fill="both", padx=20, pady=(20, 0))

        # Current display
        display_label = tk.Label(
            display_frame, 
            textvariable=self.display_text, 
            font=("Inter", 36, "bold"), 
            bg="#1e1e1e", 
            fg="#ffffff", 
            anchor="e"
        )
        display_label.pack(expand=True, fill="both", padx=20, pady=(0, 20))

        # Buttons Area
        buttons_frame = tk.Frame(self.root, bg="#1e1e1e")
        buttons_frame.pack(expand=True, fill="both", padx=10, pady=10)

        buttons = [
            ('C', 0, 0, "#a5a5a5", "#000000"), ('±', 0, 1, "#a5a5a5", "#000000"), ('%', 0, 2, "#a5a5a5", "#000000"), ('÷', 0, 3, "#ff9500", "#ffffff"),
            ('7', 1, 0, "#333333", "#ffffff"), ('8', 1, 1, "#333333", "#ffffff"), ('9', 1, 2, "#333333", "#ffffff"), ('×', 1, 3, "#ff9500", "#ffffff"),
            ('4', 2, 0, "#333333", "#ffffff"), ('5', 2, 1, "#333333", "#ffffff"), ('6', 2, 2, "#333333", "#ffffff"), ('-', 2, 3, "#ff9500", "#ffffff"),
            ('1', 3, 0, "#333333", "#ffffff"), ('2', 3, 1, "#333333", "#ffffff"), ('3', 3, 2, "#333333", "#ffffff"), ('+', 3, 3, "#ff9500", "#ffffff"),
            ('0', 4, 0, "#333333", "#ffffff", 2), ('.', 4, 2, "#333333", "#ffffff"), ('=', 4, 3, "#ff9500", "#ffffff"),
        ]

        self.button_widgets = {}
        for btn_info in buttons:
            text = btn_info[0]
            row = btn_info[1]
            col = btn_info[2]
            bg_color = btn_info[3]
            fg_color = btn_info[4]
            colspan = btn_info[5] if len(btn_info) > 5 else 1

            btn = tk.Button(
                buttons_frame, 
                text=text, 
                font=("Segoe UI", 18, "bold"), 
                bg=bg_color, 
                fg=fg_color, 
                borderwidth=0, 
                highlightthickness=0,
                activebackground=self.get_active_color(bg_color),
                activeforeground=fg_color,
                cursor="hand2",
                command=lambda t=text: self.on_button_click(t)
            )
            btn.grid(row=row, column=col, columnspan=colspan, sticky="nsew", padx=2, pady=2)
            
            # Bind hover events
            btn.bind("<Enter>", lambda e, b=btn, c=bg_color: self.on_enter(b, c))
            btn.bind("<Leave>", lambda e, b=btn, c=bg_color: self.on_leave(b, c))
            self.button_widgets[text] = btn

        # Configure grid weights
        for i in range(5):
            buttons_frame.grid_rowconfigure(i, weight=1)
        for i in range(4):
            buttons_frame.grid_columnconfigure(i, weight=1)

    def get_active_color(self, hex_color):
        if hex_color == "#333333": return "#4a4a4a"
        if hex_color == "#ff9500": return "#ffae42"
        if hex_color == "#a5a5a5": return "#c7c7c7"
        return hex_color

    def on_enter(self, btn, color):
        btn.config(bg=self.get_active_color(color))

    def on_leave(self, btn, color):
        btn.config(bg=color)

    def on_button_click(self, char):
        if char == 'C':
            self.expression = ""
            self.display_text.set("0")
            self.prev_label.config(text="")
        elif char == '=':
            try:
                # Replace visual operators with python ones
                calc_expr = self.expression.replace('×', '*').replace('÷', '/')
                # Basic sanitation/safety
                if not all(c in "0123456789+-*/. " for c in calc_expr):
                    # Check for safety, but we control the buttons so it's mostly fine
                    pass
                
                result = eval(calc_expr)
                # Format result: remove .0 if it's an integer
                if isinstance(result, float) and result.is_integer():
                    result = int(result)
                
                result_str = str(result)
                self.prev_label.config(text=self.expression + " =")
                self.display_text.set(result_str)
                self.expression = result_str
            except ZeroDivisionError:
                self.display_text.set("Div by 0")
                self.expression = ""
            except Exception:
                self.display_text.set("Error")
                self.expression = ""
        elif char == '±':
            if self.expression:
                if self.expression.startswith('-'):
                    self.expression = self.expression[1:]
                else:
                    self.expression = '-' + self.expression
                self.display_text.set(self.expression)
        elif char == '%':
            if self.expression:
                try:
                    result = float(eval(self.expression.replace('×', '*').replace('÷', '/'))) / 100
                    self.display_text.set(str(result))
                    self.expression = str(result)
                except Exception:
                    self.display_text.set("Error")
                    self.expression = ""
        else:
            # Prevent leading zeros
            if self.expression == "0" and char not in "+-×÷.":
                self.expression = char
            else:
                self.expression += char
            self.display_text.set(self.expression)


if __name__ == "__main__":
    root = tk.Tk()
    app = ModernCalculator(root)
    root.mainloop()
