from builtins import ord
import sys
import customtkinter as ctk
from tkinter import messagebox
import re
import pycountry
import phonenumbers
import urllib.request
from io import BytesIO
from PIL import Image, ImageTk
from tkcalendar import DateEntry
from datetime import date



class MacSafeDateEntry(DateEntry):
    """DateEntry workaround for tkcalendar focus issues on macOS."""

    def _on_focus_out_cal(self, event):
        if sys.platform != "darwin":
            return super()._on_focus_out_cal(event)

        # On macOS, Tk can report a FocusOut immediately after the calendar
        # opens. Keep it open while the pointer is over the date field or
        # calendar, and only close it when focus really moves elsewhere.
        if not self._top_cal.winfo_ismapped():
            return

        try:
            pointer_x, pointer_y = self._top_cal.winfo_pointerxy()

            cal_x = self._top_cal.winfo_rootx()
            cal_y = self._top_cal.winfo_rooty()
            cal_w = self._top_cal.winfo_width()
            cal_h = self._top_cal.winfo_height()

            entry_x = self.winfo_rootx()
            entry_y = self.winfo_rooty()
            entry_w = self.winfo_width()
            entry_h = self.winfo_height()

            over_calendar = (
                cal_x <= pointer_x <= cal_x + cal_w
                and cal_y <= pointer_y <= cal_y + cal_h
            )
            over_entry = (
                entry_x <= pointer_x <= entry_x + entry_w
                and entry_y <= pointer_y <= entry_y + entry_h
            )

            if over_calendar or over_entry:
                self.after_idle(self._calendar.focus_force)
                return
        except Exception:
            # Avoid closing the popup because of a transient macOS focus event.
            return

        self._top_cal.withdraw()
        self.state(["!pressed"])


class Validator:
    EMAIL = r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"
    PASSWORD = r"^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[!@#$%^&*]).{8,16}$"

    @staticmethod
    def email(value):
        return re.fullmatch(Validator.EMAIL, value) is not None

    @staticmethod
    def password(value):
        return re.fullmatch(Validator.PASSWORD, value) is not None


class SignUpPage:
    BG = "#FFF8F3"
    PINK = "#FC7F9C"
    HOVER = "#F65C84"

    def __init__(self, root):
        self.root = root
        self.root.title("Calmora - Sign Up")
        self.root.geometry("900x750")
        self.root.resizable(False, False)
        self.root.configure(fg_color=self.BG)

        self.password_visible = False
        self.confirm_visible = False
        self.countries = self.get_countries()
        self.flag_cache = {}
        self.country_popup = None
        self.create_ui()

    def get_countries(self):
        data = []

        for country in pycountry.countries:
            code = country.alpha_2
            dial = phonenumbers.country_code_for_region(code)

            if dial:
                data.append((country.name, code, dial))

        return sorted(data, key=lambda x: x[0])

    def get_flag(self, code, size=22):
        code = code.upper()

        if code in self.flag_cache:
            return self.flag_cache[code]

        points = "-".join(f"{ord(c) + 127397:x}" for c in code)
        url = (
            "https://cdn.jsdelivr.net/gh/twitter/twemoji@latest/"
            f"assets/72x72/{points}.png"
        )

        try:
            data = urllib.request.urlopen(url, timeout=5).read()
            image = Image.open(BytesIO(data)).convert("RGBA")
            image.thumbnail((size, size))
            photo = ImageTk.PhotoImage(image)
            self.flag_cache[code] = photo
            return photo
        except Exception:
            return None

    def create_ui(self):
        card = ctk.CTkFrame(
            self.root, width=620, height=700,
            corner_radius=20, fg_color="white"
        )
        card.place(relx=.5, rely=.5, anchor="center")
        card.pack_propagate(False)

        ctk.CTkLabel(
            card, text="Create Your Account",
            font=("Helvetica", 30, "bold")
        ).pack(pady=(25, 2))

        ctk.CTkLabel(
            card, text="Create your account to get started",
            font=("Helvetica", 15), text_color="gray30"
        ).pack(pady=(0, 15))

        self.username = self.add_entry(
            card, "Username", "Enter Username", 400
        )

        row = ctk.CTkFrame(card, fg_color="transparent")
        row.pack(pady=5)
        self.first = self.add_entry(
            row, "First Name", "Enter First Name", 185, "left"
        )
        self.last = self.add_entry(
            row, "Last Name", "Enter Last Name", 185, "right"
        )

        row = ctk.CTkFrame(card, fg_color="transparent")
        row.pack(pady=5)
        self.email = self.add_entry(
            row, "Email Address", "Example@gmail.com", 185, "left"
        )
        self.add_phone(row)

        row = ctk.CTkFrame(card, fg_color="transparent")
        row.pack(pady=5)
        dob_box = ctk.CTkFrame(row, fg_color="transparent")
        dob_box.pack(side="left")

        ctk.CTkLabel(
            dob_box, text="Date of Birth"
        ).pack(anchor="w")

        self.dob = MacSafeDateEntry(
            dob_box,
            width=20,
            date_pattern="dd/mm/yyyy",
            maxdate=date.today()
        )
        self.dob.pack(pady=3, ipady=7)

        gender = ctk.CTkFrame(row, fg_color="transparent")
        gender.pack(side="right", padx=(20, 0))
        ctk.CTkLabel(gender, text="Gender").pack(anchor="w")

        self.gender = ctk.CTkComboBox(
            gender,
            values=["Man","Woman","Non-binary","Genderfluid","Genderqueer","Agender","Bigender","Demiboy","Demigirl","Questioning","Two-Spirit","Another gender / Self-describe","Prefer not to say"],
            width=185, height=40
        )
        self.gender.set("Select Gender")
        self.gender.pack(pady=3)

        row = ctk.CTkFrame(card, fg_color="transparent")
        row.pack(pady=5)

        self.password = self.add_password(
            row, "Enter Password",
            "Minimum 8 characters", False
        )
        self.confirm = self.add_password(
            row, "Confirm Password",
            "Confirm Password", True
        )

        ctk.CTkButton(
            card, text="SIGN UP", command=self.signup,
            width=400, height=42,
            fg_color=self.PINK, hover_color=self.HOVER
        ).pack(pady=18)

    def add_entry(self, parent, label, placeholder, width, side=None):
        box = ctk.CTkFrame(parent, fg_color="transparent")

        if side:
            box.pack(
                side=side,
                padx=(0 if side == "left" else 20, 0)
            )
        else:
            box.pack()

        ctk.CTkLabel(box, text=label).pack(anchor="w")

        entry = ctk.CTkEntry(
            box,
            placeholder_text=placeholder,
            width=width,
            height=40
        )
        entry.pack(pady=3)
        return entry

    def add_password(self, parent, label, placeholder, right):
        box = ctk.CTkFrame(parent, fg_color="transparent")
        box.pack(
            side="right" if right else "left",
            padx=(20 if right else 0, 0)
        )

        ctk.CTkLabel(box, text=label).pack(anchor="w")

        entry = ctk.CTkEntry(
            box,
            placeholder_text=placeholder,
            width=185,
            height=40,
            show="*"
        )
        entry.pack(pady=3)

        button = ctk.CTkButton(
            box,
            text="Show",
            width=45,
            height=22,
            fg_color="transparent",
            text_color="#4F6D7A",
            hover_color="#F3E5E5",
            command=lambda: self.toggle(
                entry, button, right
            )
        )
        button.place(relx=.98, rely=.72, anchor="e")
        return entry


    def add_phone(self, parent):
        box = ctk.CTkFrame(parent, fg_color="transparent")
        box.pack(side="right", padx=(20, 0))

        ctk.CTkLabel(
            box, text="Phone Number"
        ).pack(anchor="w")

        phone_row = ctk.CTkFrame(
            box, fg_color="transparent"
        )
        phone_row.pack(pady=3)

        self.flag_label = ctk.CTkLabel(
            phone_row,
            text="",
            width=32,
            height=40
        )
        self.flag_label.pack(side="left")

        self.country_button = ctk.CTkButton(
            phone_row,
            text="United Arab Emirates (+971)",
            width=105,
            height=40,
            fg_color="#F3F3F3",
            hover_color="#E8E8E8",
            text_color="#333333",
            anchor="w",
            command=self.open_country_list
        )
        self.country_button.pack(side="left")

        self.phone = ctk.CTkEntry(
            box,
            placeholder_text="Phone Number",
            width=185,
            height=40
        )
        self.phone.pack(pady=(2, 0))

        self.selected_region = "UAE"
        self.selected_code = 971
        self.set_country("United Arab Emirates", "UAW", 971)

    def set_country(self, name, code, dial):
        self.selected_region = code
        self.selected_code = dial
        self.country_button.configure(
            text=f"{name} (+{dial})"
        )

        image = self.get_flag(code, 22)

        if image:
            self.flag_label.configure(
                image=image,
                text=""
            )
            self.flag_label.image = image
        else:
            self.flag_label.configure(
                image=None,
                text=code
            )

    def open_country_list(self):
        if self.country_popup is not None:
            self.close_country_list()
            return

        self.country_popup = ctk.CTkToplevel(self.root)
        self.country_popup.title("Select Country")
        self.country_popup.geometry("320x430")
        self.country_popup.resizable(False, False)
        self.country_popup.configure(fg_color="white")
        self.country_popup.transient(self.root)
        self.country_popup.grab_set()

        ctk.CTkLabel(
            self.country_popup,
            text="Select Country Code",
            font=("Helvetica", 15, "bold")
        ).pack(pady=(12, 7))

        search = ctk.CTkEntry(
            self.country_popup,
            placeholder_text="Search country..."
        )
        search.pack(fill="x", padx=12, pady=(0, 8))

        scroll = ctk.CTkScrollableFrame(
            self.country_popup,
            width=285,
            height=335,
            fg_color="#FAFAFA"
        )
        scroll.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        def populate(event=None):
            for widget in scroll.winfo_children():
                widget.destroy()

            query = search.get().lower().strip()

            for name, code, dial in self.countries:
                if query and query not in name.lower() and query not in code.lower() and query not in str(dial):
                    continue

                row = ctk.CTkFrame(
                    scroll,
                    height=42,
                    fg_color="transparent"
                )
                row.pack(fill="x", pady=2)

                image = self.get_flag(code, 20)

                if image:
                    label = ctk.CTkLabel(
                        row,
                        text="",
                        image=image,
                        width=30
                    )
                    label.image = image
                else:
                    label = ctk.CTkLabel(
                        row,
                        text=code,
                        width=30
                    )

                label.pack(side="left", padx=(5, 4))

                button = ctk.CTkButton(
                    row,
                    text=f"{name}  +{dial}",
                    anchor="w",
                    height=36,
                    fg_color="transparent",
                    hover_color="#FFE7ED",
                    text_color="#333333",
                    command=lambda n=name, c=code, d=dial:
                        self.choose_country(n, c, d)
                )
                button.pack(side="left", fill="x", expand=True)

        search.bind("<KeyRelease>", populate)
        populate()

        self.country_popup.protocol(
            "WM_DELETE_WINDOW",
            self.close_country_list
        )

    def choose_country(self, name, code, dial):
        self.set_country(name, code, dial)
        self.close_country_list()

    def close_country_list(self):
        if self.country_popup:
            self.country_popup.grab_release()
            self.country_popup.destroy()
            self.country_popup = None


    def toggle(self, entry, button, confirm):
        if confirm:
            self.confirm_visible = not self.confirm_visible
            visible = self.confirm_visible
        else:
            self.password_visible = not self.password_visible
            visible = self.password_visible

        entry.configure(show="" if visible else "*")
        button.configure(text="Hide" if visible else "Show")


    def signup(self):
        email = self.email.get().strip()
        password = self.password.get()
        confirm = self.confirm.get()
        phone = self.phone.get().strip()

        if not email or not password or not confirm:
            messagebox.showerror(
                "Error",
                "Please fill all required fields."
            )
            return

        if not Validator.email(email):
            messagebox.showerror(
                "Error",
                "Enter a valid email address."
            )
            return

        if not Validator.password(password):
            messagebox.showerror(
                "Error",
                "Password must contain uppercase, lowercase, "
                "number, special character and 8-16 characters."
            )
            return

        if password != confirm:
            messagebox.showerror(
                "Error",
                "Passwords do not match."
            )
            return

        try:
            number = phonenumbers.parse(
                "+" + str(self.selected_code) + phone,
                self.selected_region
            )

            if not phonenumbers.is_valid_number(number):
                raise ValueError

        except Exception:
            messagebox.showerror(
                "Error",
                "Enter a valid phone number."
            )
            return

        messagebox.showinfo(
            "Success",
            "Account created successfully!"
        )


if __name__ == "__main__":
    root = ctk.CTk()
    SignUpPage(root)
    root.mainloop()
