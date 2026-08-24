import customtkinter as ctk
from tkinter import messagebox
import re

ctk.set_appearance_mode("Light")
ctk.set_default_color_theme("blue")

EMAIL_RE = r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"

PASSWORD_RE = (
    r"^(?=.*[A-Z])"
    r"(?=.*[a-z])"
    r"(?=.*\d)"
    r"(?=.*[!@#$%^&*()_+\-=\[\]{};':\"\\|,.<>/?])"
    r".{8,16}$"
)

class Validator:
    @staticmethod
    def email_verification(email):
        return re.fullmatch(EMAIL_RE, email) is not None

    @staticmethod
    def password_verification(password):
        return re.fullmatch(PASSWORD_RE, password) is not None


class BasePage:
    def __init__(self, root):
        self.root = root

        self.root.title("Calmora - Login Page")
        self.root.geometry("900x650")
        self.root.resizable(False, False)
        self.root.configure(fg_color="#FFF8F3")


class LoginPage(BasePage):
    def __init__(self, root):
        super().__init__(root)

        self.password_visible = False
        self.ui()

    def ui(self):
        frame = ctk.CTkFrame(
            self.root,
            width=500,
            height=500,
            corner_radius=20,
            fg_color="#FFFFFF"
        )

        frame.place(
            relx=0.5,
            rely=0.5,
            anchor="center"
        )

        frame.pack_propagate(False)

        ctk.CTkLabel(
            frame,
            text="Welcome Back",
            font=("Helvetica", 36, "bold"),
            text_color="#000000"
        ).pack(pady=(40, 10))

        ctk.CTkLabel(
            frame,
            text="Don't have an account? Sign Up",
            font=("Helvetica", 18),
            text_color="gray30"
        ).pack(pady=(0, 30))

        ctk.CTkLabel(
            frame,
            text="Email Address",
            font=("Helvetica", 18),
            text_color="#000000"
        ).pack()

        self.email_entry = ctk.CTkEntry(
            frame,
            placeholder_text="Enter your email address",
            width=400,
            height=40
        )

        self.email_entry.pack(pady=10)

        ctk.CTkLabel(
            frame,
            text="Password",
            font=("Helvetica", 18),
            text_color="#000000"
        ).pack()

        self.password_entry = ctk.CTkEntry(
            frame,
            placeholder_text="Enter your password",
            width=400,
            height=40,
            show="*"
        )

        self.password_entry.pack(pady=10)

        ctk.CTkButton(
            frame,
            text="Show Password",
            command=self.toggle_password,
            width=180,
            height=35,
            fg_color="#4F6D7A",
            hover_color="#3A5562"
        ).pack(pady=15)

        self.login_button = ctk.CTkButton(
            frame,
            text="Login",
            command=self.login,
            width=250,
            height=45,
            fg_color="#FC7F9C",
            hover_color="#F65C84",
            text_color="#FFFFFF",
            corner_radius=10
        )

        self.login_button.pack(pady=20)
        self.root.bind("<Return>", lambda event: self.login())

    def toggle_password(self):
        self.password_visible = not self.password_visible

        if self.password_visible:
            self.password_entry.configure(show="")
        else:
            self.password_entry.configure(show="*")

    def login(self):
        email = self.email_entry.get().strip()
        password = self.password_entry.get()

        if email == "":
            messagebox.showerror(
                "Error",
                "Please enter your email address."
            )
            return

        if not Validator.email_verification(email):
            messagebox.showerror(
                "Error",
                "Please enter a valid email address."
            )
            return

        if password == "":
            messagebox.showerror(
                "Error",
                "Please enter your password."
            )
            return

        if not Validator.password_verification(password):
            messagebox.showerror(
                "Error",
                "Password must contain:\n"
                "- 1 uppercase letter\n"
                "- 1 lowercase letter\n"
                "- 1 number\n"
                "- 1 special character\n"
                "- 8 to 16 characters"
            )
            return

        messagebox.showinfo(
            "Success",
            "Login Successful!"
        )


root = ctk.CTk()
LoginPage(root)
root.mainloop()