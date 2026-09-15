import customtkinter as ctk
from PIL import Image
from tkcalendar import DateEntry
from datetime import date
import phonenumbers
import pycountry
from tkinter import filedialog, messagebox

BG = "#F4F4F4"
SIDEBAR = "#1E1E1E"
WHITE = "#FFFFFF"
BLACK = "#050505"
GRAY = "#C8C8C8"
LIGHT_GRAY = "#D3D3D3"
TEXT = "#242424"

class SettingsPage(ctk.CTkFrame):

    def __init__(self, parent, main=None):

        super().__init__(
            parent,
            fg_color=BG
        )

        self.parent = parent
        self.main_controller = main if main is not None else parent

        self.profile_image = None
        self.profile_image_path = None

        self.selected_avatar = "🐱"

        self.selected_country = "IN"
        self.selected_country_name = "India"
        self.selected_calling_code = 91
        self.country_popup = None
        self.home_menu = None
        self.settings_menu = None
        self.password_visible = False
        self.confirm_visible = False
        self.create_left_navbar()
        self.create_sidebar()        
        self.create_profile_area()

    def create_left_navbar(self):

        self.left_nav_expanded = True

        self.left_nav_width = 260
        self.left_nav_collapsed_width = 65

        self.left_navbar = ctk.CTkFrame(
            self,
            width=self.left_nav_width,
            fg_color=GRAY,
            corner_radius=0
        )

        self.left_navbar.pack(
            side="left",
            fill="y"
        )

        self.left_navbar.pack_propagate(False)

        self.left_nav_top = ctk.CTkFrame(
            self.left_navbar,
            height=100,
            fg_color="transparent"
        )

        self.left_nav_top.pack(
            fill="x",
            padx=5,
            pady=(10, 20)
        )

        self.left_nav_top.pack_propagate(False)

        # Logo
        self.left_logo = ctk.CTkLabel(
            self.left_nav_top,
            text="Logo",
            width=160,
            height=70,
            fg_color=SIDEBAR,
            text_color=WHITE,
            font=("Arial", 13),
            corner_radius=0
        )

        self.left_logo.pack(
            side="left",
            fill="both",
            expand=True,
            padx=(0, 10)
        )

        self.left_toggle = ctk.CTkButton(
            self.left_nav_top,
            text="<",
            width=45,
            height=70,
            fg_color=SIDEBAR,
            hover_color="#333333",
            text_color=WHITE,
            font=("Arial", 24),
            corner_radius=0,
            command=self.toggle_left_navbar
        )

        self.left_toggle.pack(
            side="right"
        )

        
        self.left_menu_frame = ctk.CTkFrame(
            self.left_navbar,
            fg_color="transparent"
        )

        self.left_menu_frame.pack(
            fill="both",
            expand=True,
            padx=3
        )

        self.left_nav_buttons = []

        menu_items = [
            ("Mental health survey", self.open_mental_health_survey),
            ("AI ChatBot", self.open_ai_chatbot),
            ("Appointment Booking", self.open_appointment_booking),
            ("Journaling", self.open_journaling),
            ("Mood Tracking", self.open_mood_tracking),
            ("Goal Tracking", self.open_goal_tracking),
            ("News/ Blogs", self.open_news_blogs),
            ("Resources", self.open_resources)
        ]

        for text, command in menu_items:

            separator = ctk.CTkFrame(
                self.left_menu_frame,
                height=10,
                fg_color=GRAY,
                corner_radius=0
            )

            separator.pack(
                fill="x"
            )

            button = ctk.CTkButton(
                self.left_menu_frame,
                text=text,
                height=48,
                fg_color=SIDEBAR,
                hover_color="#333333",
                text_color="#D0D0D0",
                font=("Arial", 14),
                corner_radius=0,
                anchor="center",
                command=command
            )

            button.pack(
                fill="x"
            )

            self.left_nav_buttons.append(
                (button, text)
            )

    def toggle_left_navbar(self):

        if self.left_nav_expanded:

            self.left_navbar.configure(
                width=self.left_nav_collapsed_width
            )

            self.left_logo.pack_forget()

            self.left_toggle.configure(
                text=">"
            )

            for button, text in self.left_nav_buttons:

                button.configure(
                    text=""
                )

            self.left_nav_expanded = False

        else:

            self.left_navbar.configure(
                width=self.left_nav_width
            )

            self.left_logo.pack(
                side="left",
                fill="both",
                expand=True,
                padx=(0, 10)
            )

            self.left_toggle.configure(
                text="<"
            )

            for button, text in self.left_nav_buttons:

                button.configure(
                    text=text
                )

            self.left_nav_expanded = True

    def open_mental_health_survey(self):
        print("Mental Health Survey selected")

    def open_ai_chatbot(self):
        print("AI ChatBot selected")

    def open_appointment_booking(self):
        print("Appointment Booking selected")

    def open_journaling(self):
        print("Journaling selected")

    def open_mood_tracking(self):
        print("Mood Tracking selected")

    def open_goal_tracking(self):
        print("Goal Tracking selected")

    def open_news_blogs(self):
        print("News / Blogs selected")

    def open_resources(self):
        print("Resources selected")
    
    def create_sidebar(self):
        self.sidebar_open = True
        self.sidebar = ctk.CTkFrame(
            self,
            width=90,
            fg_color=SIDEBAR,
            corner_radius=0
        )
        self.sidebar.place(
            relx=1,
            rely=0,
            anchor="ne"
        )

        self.sidebar.pack_propagate(False)

        self.sidebar_toggle = ctk.CTkButton(
            self.sidebar,
            text=">",
            width=55,
            height=40,
            fg_color="transparent",
            hover_color="#333333",
            text_color=WHITE,
            font=("Arial", 22),
            corner_radius=0,
            command=self.toggle_sidebar
        )

        self.sidebar_toggle.pack(
            pady=(15, 20)
        )
    
        logo = ctk.CTkLabel(
            self.sidebar,
            text="C",
            font=("Arial", 32, "bold"),
            text_color=WHITE
        )

        logo.pack(
            pady=(0, 35)
        )

        home_button = ctk.CTkButton(
            self.sidebar,
            text="⌂",
            width=55,
            height=50,
            fg_color="transparent",
            hover_color="#333333",
            text_color=WHITE,
            font=("Arial", 28),
            command=self.go_home
        )

        home_button.pack(
            pady=10
        )

        profile_button = ctk.CTkButton(
            self.sidebar,
            text="◉",
            width=55,
            height=50,
            fg_color="transparent",
            hover_color="#333333",
            text_color=WHITE,
            font=("Arial", 24),
            command=self.open_profile
        )

        profile_button.pack(
            pady=10
        )

        spacer = ctk.CTkFrame(
            self.sidebar,
            fg_color="transparent"
        )

        spacer.pack(
            expand=True,
            fill="both"
        )

        self.after(
            100,
            self.set_sidebar_height
        )

    def set_sidebar_height(self):

        height = self.winfo_height()

        if height > 1:

            self.sidebar.configure(
                height=height
            )

    def toggle_sidebar(self):

        if self.sidebar_open:

            self.animate_sidebar_close()

        else:

            self.animate_sidebar_open()

    def animate_sidebar_open(self, height=0):

        max_height = self.winfo_height()

        if max_height <= 1:

            self.after(
                50,
                lambda: self.animate_sidebar_open(height)
            )

            return

        if height < max_height:

            height += 25

            if height > max_height:
                height = max_height

            self.sidebar.configure(
                height=height,
                width=90
            )

            self.after(
                10,
                lambda: self.animate_sidebar_open(height)
            )

        else:

            self.sidebar_open = True

            self.sidebar_toggle.configure(
                text=">"
            )

    def animate_sidebar_close(self, height=None):

        max_height = self.winfo_height()

        if max_height <= 1:
            return

        if height is None:
            height = max_height

        if height > 0:

            height -= 25

            if height < 0:
                height = 0

            self.sidebar.configure(
                height=height,
                width=90
            )

            self.after(
                10,
                lambda: self.animate_sidebar_close(height)
            )

        else:

            self.sidebar.configure(
                width=90,
                height=1
            )

            self.sidebar_open = False

            self.sidebar_toggle.configure(
                text="<"
            )    
    def create_profile_area(self):
        self.main = ctk.CTkFrame(
            self,
            fg_color=BG,
            corner_radius=0
        )
        self.main.pack(
            side="left",
            fill="both",
            expand=True
        )
        top_bar = ctk.CTkFrame(
            self.main,
            fg_color=WHITE,
            height=80,
            corner_radius=0
        )

        top_bar.pack(
            fill="x"
        )

        top_bar.pack_propagate(False)

        title = ctk.CTkLabel(
            top_bar,
            text="Settings",
            font=("Arial", 26, "bold"),
            text_color=BLACK
        )

        title.pack(
            side="left",
            padx=35
        )
        right_buttons = ctk.CTkFrame(
            top_bar,
            fg_color="transparent"
        )

        right_buttons.pack(
            side="right",
            padx=25
        )
        home_container = ctk.CTkFrame(
            right_buttons,
            fg_color="transparent"
        )
        home_container.pack(
            side="left",
            padx=8
        )
        self.home_button = ctk.CTkButton(
            home_container,
            text="⌂",
            width=45,
            height=40,
            fg_color="transparent",
            hover_color=LIGHT_GRAY,
            text_color=BLACK,
            font=("Arial", 25),
            command=self.toggle_home_menu
        )
        self.home_button.pack()
        self.home_menu = ctk.CTkFrame(
            home_container,
            width=180,
            fg_color=WHITE,
            corner_radius=10,
            border_width=1,
            border_color=LIGHT_GRAY
        )
        self.create_home_menu()
        settings_container = ctk.CTkFrame(
            right_buttons,
            fg_color="transparent"
        )
        settings_container.pack(
            side="left",
            padx=8
        )
        self.settings_top_button = ctk.CTkButton(
            settings_container,
            text="⚙",
            width=45,
            height=40,
            fg_color="transparent",
            hover_color=LIGHT_GRAY,
            text_color=BLACK,
            font=("Arial", 24),
            command=self.toggle_settings_menu
        )
        self.settings_top_button.pack()
        self.settings_menu = ctk.CTkFrame(
            settings_container,
            width=190,
            fg_color=WHITE,
            corner_radius=10,
            border_width=1,
            border_color=LIGHT_GRAY
        )
        self.create_settings_menu()
        content = ctk.CTkScrollableFrame(
            self.main,
            fg_color=BG,
            corner_radius=0
        )
        content.pack(
            fill="both",
            expand=True,
            padx=40,
            pady=30
        )
        profile_card = ctk.CTkFrame(
            content,
            fg_color=WHITE,
            corner_radius=15)
        profile_card.pack(
            fill="x",
            pady=(0, 25)
        )
        image_frame = ctk.CTkFrame(
            profile_card,
            fg_color="transparent"
        )
        image_frame.pack(
            pady=25
        )
        self.avatar_label = ctk.CTkLabel(
            image_frame,
            text=self.selected_avatar,
            font=("Segoe UI Emoji", 80),
            width=150,
            height=150
        )
        self.avatar_label.pack()
        self.pet_avatar_preview = ctk.CTkLabel(
            image_frame,
            text=self.selected_avatar,
            font=("Segoe UI Emoji", 30)
        )
        self.pet_avatar_preview.pack(
            pady=(5, 0))
        button_frame = ctk.CTkFrame(
            profile_card,
            fg_color="transparent"
        )
        button_frame.pack(
            pady=(0, 25)
        )
        upload_button = ctk.CTkButton(
            button_frame,
            text="Upload Profile Picture",
            width=190,
            height=40,
            fg_color=BLACK,
            hover_color="#333333",
            text_color=WHITE,
            command=self.upload_profile_picture
        )
        upload_button.pack(
            side="left",
            padx=8
        )
        avatar_button = ctk.CTkButton(
            button_frame,
            text="Choose Pet Avatar",
            width=170,
            height=40,
            fg_color="#E8E8E8",
            hover_color="#D5D5D5",
            text_color=BLACK,
            command=self.open_pet_avatar_window
        )
        avatar_button.pack(
            side="left",
            padx=8
        )
        remove_button = ctk.CTkButton(
            button_frame,
            text="Remove Picture",
            width=150,
            height=40,
            fg_color="#E8E8E8",
            hover_color="#D5D5D5",
            text_color=BLACK,
            command=self.remove_profile_picture
        )
        remove_button.pack(
            side="left",
            padx=8)

        details_card = ctk.CTkFrame(
            content,
            fg_color = WHITE,
            corner_radius = 15,
        )
        details_card.pack(
            fill = 'x',
            pady = (0,25)
        )

        heading = ctk.CTkLabel(
            details_card,
            text = 'Personal Details',
            font = ("Arial",20,"bold"),
            text_color = BLACK
            )
        heading.pack(
            anchor = 'w', 
            padx = 30, 
            pady = (25,20)
        )

        fields = ctk.CTkFrame(
            details_card,
            fg_color = 'transparent'
            )
        fields.pack(
            fill = 'x',
            padx = 30,
            pady = (0,30)
        )

        fields.grid_columnconfigure(
            0,
            weight = 1
        )
        fields.grid_columnconfigure(
            1,
            weight = 1
        )

        first_label = ctk.CTkLabel(
            fields,
            text = 'First name',
            font = ("Arial", 13),
            text_color = TEXT
        )
        first_label.grid(
            row = 0,
            column = 0,
            sticky = 'w',
            pady = (0,5),
            padx = (0,15)
        )
        self.first_name_entry = ctk.CTkEntry(
            fields,
            height = 40,
            placeholder_text="Enter First Name"
        )
        self.first_name_entry.grid(
            row = 1,
            column = 0,
            sticky = 'ew',
            pady = (0,15),
            padx = (0,20)
        )

        last_label = ctk.CTkLabel(
            fields,
            text = 'Last name',
            font = ("Arial", 13),
            text_color = TEXT
                )
        last_label.grid(
            row = 0,
            column = 1,
            sticky = 'w',
            pady = (0,5),
            padx = (0,15)
        )
        self.last_name_entry = ctk.CTkEntry(
            fields,
            height = 40,
            placeholder_text="Enter Last Name"
        )
        self.last_name_entry.grid(
            row = 1,
            column = 1,
            sticky = 'ew',
            pady = (0,20),
            padx = (15,0)
            )

        phone_label = ctk.CTkLabel(
            fields,
            text = "Phone Number",
            font = ("Arial", 30),
            text_color = TEXT
        )
        phone_label.grid(
            row = 2, 
            column = 0, 
            sticky = 'w', 
            padx = (0,15),
            pady = (0,5)
            )
        phone_frame = ctk.CTkFrame(
            fields, 
            fg_color = 'transparent'
            )
        phone_frame.grid(
            row = 3, 
            column = 0, 
            sticky = 'ew', 
            padx = (0,15),
            pady = (0,20)
        )
        phone_frame.grid_columnconfigure(1,
            weight = 1)

        self.country_button = ctk.CTkButton(
            phone_frame,
            text = 'UAE +971   V',
            width = 110,
            height = 40,
            fg_color = WHITE,
            hovor_color = GRAY,
            text_color = BLACK,
            command = self.open_country_picker()
        )
        self.country_button.grid(
            row = 0,
            column = 0,
            padx = (0,5)
        )

        self.phone_entry = ctk.CTkEntry(
            phone_frame,
            height = 40,
            placeholder_text= "Phone Number"
        )
        self.phone_entry.grid(
            row = 0,
            column = 1,
            sticky = 'ew'
            )
        self.phone_entry.bind(
            "<KeyRelease>",
            self.validate_phonenumber
        )

        self.phone_status = ctk.CTkLabel(
            phone_frame,
            text = '',
            font = ("Arial", 11),
            text_color = 'red'
        )
        self.phone_status.grid(
            row = 1,
            column = 1,
            sticky = 'w'
        )
        dob_label = ctk.CTkLabel(
            fields,
            text = 'Date Of Birth',
            font = ("Arial", 13),
            text_color = TEXT
        )
        dob_label.grid(
            row = 2,
            column = 1,
            sticky = 'w',
            padx = (15,0),
            pady = (0,5)
        )
        self.dob_picker = DateEntry(
            fields,
            width = 25,
            background = WHITE,
            fg_color = GRAY,
            borderwidth = 1,
            date_pattern = "dd/mm/yyyy",
            maxdate = date.today(),
            font = ("Arial", 13)
        )
        self.dob_picker.grid(
            row = 3,
            column = 1,
            sticky = 'ew',
            padx = (15,0),
            pady = (0,20)
        )

        email_label = ctk.CTkLabel(
            fields,
            text = 'Email',
            font = ('Arial',13),
            text_color = TEXT
        )
        email_label.grid(
            row = 4,
            column = 0,
            sticky = 'w',
            padx = (0,15),
            pady = (0,5)
        )
        self.email_entry = ctk.CTkEntry(
            fields,
            height = 40, 
            placeholder_text= "Enter Email"
        )
        self.email_entry.grid(
            row = 5,
            column = 0,
            sticky = 'ew',
            padx = (0,15)
        )

        password_label = ctk.CTkLabel(
            fields,
            text = "Password",
            font = ("Arial",13),
            text_color = TEXT
        )
        password_label.grid(
            row = 4,
            column = 1,
            sticky = 'w',
            padx = (15,0),
            pady = (0,5)
            )
        password_frame = ctk.CTkFrame(
            fields,
            fg_color = 'transparent'
        )   
        password_frame.grid(
            row = 5,
            column = 1,
            sticky = 'ew',
            padx = (15,0)
        )
        password_frame.grid_columnconfigure(
            0,
            weight = 1
        )
        self.password_entry = ctk.CTkEntry(
            password_frame,
            height = 40,
            placeholder_text = "Enter Password",
            show = "*"
        )
        self.password_entry.grid(
            row = 0,
            column = 0,
            sticky = 'ew'
        )
        self.password_button = ctk.CTkButton(
            password_frame,
            text = 'Show',
            width = 55,
            height = 32,
            fg_color = 'transparent',
            hover_color = GRAY,
            text_color = BLACK,
            commad = self.toggle_password
        )
        self.password_button.grid(row = 0, column = 1, padx = 5)
        confirm_label = ctk.CTkLabel(
            fields,
            text = "Confirm Password",
            font = ("Arial",13),
            text_color = TEXT
        )
        confirm_label.grid(
            row = 6,
            column = 0,
            sticky = 'w',
            padx = (0,15),
            pady = (20,5)
        )
        confirm_frame = ctk.CTkFrame(
            fields,
            fg_color = 'transparent')
        confirm_frame.grid(
            row = 7,
            column = 0,
            sticky = 'ew',
            padx = (0,15)
        )
        confirm_frame.grid_columnconfigure(
            0,
            weight = 1
        )
        self.confirm_entry = ctk.CTkEntry(
            confirm_frame,
            height = 40,
            placeholder_text = "Confirm Password",
            show = "*"
        )
        self.confirm_entry.grid(
            row = 0,
            column = 0,
            sticky = 'ew'
        )
        self.confirm_button = ctk.CTkButton(
            confirm_frame,
            text = 'Show',
            width = 55,
            height = 32,
            fg_color = 'transparent',
            hover_color = GRAY,
            text_color = BLACK,
            command = self.toggle_confirm
        )
        self.confirm_button.grid(
            row = 0,
            column = 1,
            padx = 5
        )
        save_button = ctk.CTkButton(
            content,
            text = "Save Changes",
            width = 150,
            height = 40,
            fg_color = BLACK,
            hover_color = "#333333",
            text_color = WHITE,
            command = self.save_profile
        )
        save_button.pack(
            pady = (0,30)
        )
    def create_home_menu(self):
            home_title = ctk.CTkLabel(
                self.home_menu,
                text = "Home",
                font = ("Arial",14,"bold"),
                text_color = BLACK
            )
            home_title.pack(
                anchor = 'w',
                padx = 15,
                pady = (12,8)
            )
            home_button = ctk.CTkButton(
                self.home_menu,
                text = "⌂ Home",
                height = 35,
                fg_color = 'transparent',
                hover_color = GRAY,
                text_color = BLACK,
                font = ("Arial",13),
                anchor = 'w',
                command = self.go_home
            )
            home_button.pack(
                fill = 'x',
                padx = 5
            )
            dashboard_button = ctk.CTkButton(
                self.home_menu,
                text = "📊 Dashboard",
                height = 35,
                fg_color = 'transparent',
                hover_color = GRAY,
                text_color = BLACK,
                font = ("Arial",13),
                anchor = 'w',
                command = self.go_dashboard
            )
            dashboard_button.pack(
                fill = 'x',
                padx = 5
            )
            profile = ctk.CTkButton(
                self.home_menu,
                text = "👤 Profile",
                height = 35,
                fg_color = 'transparent',
                hover_color = GRAY,
                text_color = BLACK,
                font = ("Arial",13),
                anchor = 'w',
                command = self.open_profile
            )
            profile.pack(
                fill = 'x',
                padx = 5
            )

    def create_settings_menu(self):
            settings_title = ctk.CTkLabel(
                self.settings_menu,
                text = "Settings",
                font = ("Arial",14,"bold"),
                text_color = BLACK
            )
            settings_title.pack(
                anchor = 'w',
                padx = 15,
                pady = (12,8)
            )
            settings_button = ctk.CTkButton(
                self.settings_menu,
                text = "⚙ Settings",
                height = 35,
                fg_color = 'transparent',
                hover_color = GRAY,
                text_color = BLACK,
                font = ("Arial",13),
                anchor = 'w',
                command = self.open_profile
            )
            settings_button.pack(
                fill = 'x',
                padx = 5
            )
            logout_button = ctk.CTkButton(
                self.settings_menu,
                text = "🚪 Logout",
                height = 35,
                fg_color = 'transparent',
                hover_color = GRAY,
                text_color = BLACK,
                font = ("Arial",13),
                anchor = 'w',
                command = self.logout
            )
            logout_button.pack(
                fill = 'x',
                padx = 5,
                pady = (0,8)
            )

    def toggle_home_menu(self):
            if self.home_menu.winfo_ismapped():
                self.home_menu.pack_forget()
            if self.settings_menu.winfo_ismapped():
                self.settings_menu.pack_forget()
            else:
                self.home_menu.pack(
                    fill = 'x',
                    pady = (5,0)
                )

    def toggle_settings_menu(self):
            if self.settings_menu.winfo_ismapped():
                self.settings_menu.pack_forget()
            if self.home_menu.winfo_ismapped():
                self.home_menu.pack_forget()
            else:
                self.settings_menu.pack(
                    fill = 'x',
                    pady = (5,0)
                )

    def close_dropdowns(self):
            if self.home_menu.winfo_ismapped():
                self.home_menu.pack_forget()
            if self.settings_menu.winfo_ismapped():
                self.settings_menu.pack_forget()

    def go_home(self):
            self.close_dropdowns()
            print("Navigating to Home Page")

    def go_dashboard(self):
            self.close_dropdowns()
            print("Navigating to Dashboard Page")

    def open_profile(self):
            self.close_dropdowns()
            print("Navigating to Profile Page")

    def logout(self):
            self.close_dropdowns()
            print("Logging out...")

    def country_flag(self, country_code):
            return "".join(chr(ord(char) + 127397) for char in country_code.upper())

    def get_countires(self):
            countries = []
            for country in pycountry.countries:
                country_code = country.alpha_2
                name = country.name
                try:
                    calling_code = phonenumbers.country_code_for_region(country_code)

                except Exception:
                    continue
                if  calling_code == 0:
                    continue
                countries.append((country_code, name, calling_code))
            countries.sort(key=lambda x: x[1])
            return countries

    def open_country_picker(self):
            if self.country_popup is not None:
                try:
                    self.country_popup.destroy()
                except:
                    pass
                return
            self.country_popup = ctk.CTkToplevel(self)
            self.country_popup.title("Select Country")
            self.country_popup.geometry("400x500")
            self.country_popup.grab_set()
            search_entry = ctk.CTkEntry(
                self.country_popup,
                placeholder_text="Search country",
                height = 40,
                text_color=BLACK
            )
            search_entry.pack(
                side="left",
                padx=20,
                pady = 20
            )
            scroll_frame = ctk.CTkScrollableFrame(
                self.country_popup,
                fg_color=WHITE,
            )
            scroll_frame.pack(
                fill="both",
                expand=True,
                padx=10,
                pady=(0,10)
            )

            countries = self.get_countires()
            def display_countries(search = ''):
                for widget in scroll_frame.winfo_children():
                    widget.destroy()
                for country_code, name, calling_code in countries:
                    if search.lower() in name.lower() or search.lower() in country_code.lower() or search in str(calling_code):
                        flag = self.country_flag(country_code)
                        button = ctk.CTkButton(
                            scroll_frame,
                            text=f"{flag} {name} +{calling_code}",
                            height=40,
                            fg_color="transparent",
                            hover_color=LIGHT_GRAY,
                            text_color=BLACK,
                            font=("Arial", 13),
                            anchor="w",
                            command=lambda c=country_code, n=name, cc=calling_code: self.select_country(c, n, cc)
                        )
                        button.pack(
                            fill="x",
                            padx=10,
                            pady=(0, 5)
                        )
            search_entry.bind(
                "<KeyRelease>",
                lambda event: display_countries(search_entry.get())
            )
            display_countries()

    def select_country(self, country_code, name, calling_code):
            self.selected_country = country_code
            self.selected_country_name = name
            self.selected_calling_code = calling_code
            flag = self.country_flag(country_code)
            self.country_button.configure(
                text=f"{self.country_flag(country_code)} {name} +{calling_code} ▼"
            )
            if self.country_popup is not None:
                try:
                    self.country_popup.destroy()
                except:
                    pass
                self.country_popup = None
            self.validate_phonenumber()

    def validate_phonenumber(self, event = None):
            phone_number = self.phone_entry.get().strip()
            if not phone_number:
                self.phone_status.configure(
                    text = ''
                )
                return False

            try:
                parsed_number = phonenumbers.parse(f"+{self.selected_calling_code}{phone_number}", None)
                if phonenumbers.is_valid_number(parsed_number):
                    self.phone_status.configure(
                        text = 'Valid phone number ✓',
                        text_color = 'green'
                    )
                    return True
                else:
                    self.phone_status.configure(
                        text = 'Invalid phone number ✗',
                        text_color = 'red'
                    )
                    return False
            except Exception:
                self.phone_status.configure(
                    text = 'Invalid phone number ✗',
                    text_color = 'red'
                )
                return False

    def toggle_password(self):
            self.password_visible = not self.password_visible
            if self.password_visible:
                self.password_entry.configure(
                    show = ""
                )
                self.password_button.configure(
                    text = "Hide"
                )
            else:
                self.password_entry.configure(
                    show = "*"
                )
                self.password_button.configure(
                    text = "Show"
                )

    def toggle_confirm(self):
            self.confirm_visible = not self.confirm_visible
            if self.confirm_visible:
                self.confirm_entry.configure(
                    show = ""
                )
                self.confirm_button.configure(
                    text = "Hide"
                )
            else:
                self.confirm_entry.configure(
                    show = "*"
                )
                self.confirm_button.configure(
                    text = "Show"
                )

    def open_pet_avatar_window(self):
            avatar_window = ctk.CTkToplevel(self)
            avatar_window.title("Choose Pet Avatar")
            avatar_window.geometry("500x450")
            avatar_window.configure(
                fg_color=WHITE
            )
            avatar_window.grab_set()
            title = ctk.CTkLabel(
                avatar_window,
                text="Choose Your Pet Avatar",
                font=("Arial", 22, "bold"),
                text_color=BLACK
            )
            title.pack(
                pady=25
            )
            avatar_frame = ctk.CTkFrame(
                avatar_window,
                fg_color="transparent"
            )
            avatar_frame.pack(
                padx=20,
                pady=10
            )
            avatars = ["🐶", "🐱", "🐰", "🦊", "🐻", "🐼", "🐨", "🐯", "🦁", "🐮", "🐭", "🐵"]
            row = 0
            col = 0
            for e in avatars:
                avatar_button = ctk.CTkButton(
                    avatar_frame,
                    text=e,
                    width=80,
                    height=70,
                    fg_color="#E8E8E8",
                    hover_color="#D5D5D5",
                    text_color=BLACK,
                    font=("Segoe UI Emoji", 30),
                    command=lambda e=e: self.select_pet_avatar(e, avatar_window)
                )
                avatar_button.grid(
                    row=row,
                    column=col,
                    padx=10,
                    pady=10
                )
                col += 1
                if col > 3:
                    col = 0
                    row += 1

    def set_pet_avatar(self, avatar, window):
            self.selected_avatar = avatar
            self.avatar_label.configure(
                text=avatar
            )
            if self.profile_image is None:
                self.avatar_label.configure(
                    text=avatar,
                    image = None,
                    font = ("Segoe UI Emoji", 80)
            )
            window.destroy()

    def upload_profile_picture(self):
            file_path = filedialog.askopenfilename(
                title="Select Profile Picture",
                filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.gif;*.webp")]
            )
            if not file_path:
                return
            try:
                image = Image.open(file_path)
                image = image.convert("RGBA")
                image.thumbnail((150, 150), Image.ANTIALIAS)
                self.profile_image = ctk.CTkImage(
                    light_image=image,
                    dark_image=image,
                    size=(150, 150)
                )
                self.profile_image_path = file_path
                self.avatar_label.configure(
                    image=self.profile_image,
                    text=""
                )

            except Exception as e:
                messagebox.showerror(
                    "Error",
                    f"Failed to load image: {e}"
                )

    def remove_profile_picture(self):
            self.profile_image = None
            self.profile_image_path = None
            self.avatar_label.configure(
                image=None,
                text=self.selected_avatar,
                font=("Segoe UI Emoji", 80)
            )

    def save_profile(self):
            first_name = self.first_name_entry.get().strip()
            last_name = self.last_name_entry.get().strip()
            phone_number = self.phone_entry.get().strip()
            dob = self.dob_picker.get_date()
            email = self.email_entry.get().strip()
            password = self.password_entry.get().strip()
            confirm_password = self.confirm_entry.get().strip()

            if not first_name:
                print("First name is required.")
                messagebox.showerror(
                    "Error",
                    "First name is required."
                )
                return
            if not last_name:
                print("Last name is required.")
                messagebox.showerror(
                    "Error",
                    "Last name is required."
                )
                return
            if not phone_number:
                print("Phone number is required.")
                messagebox.showerror(
                    "Error",
                    "Phone number is required."
                )
                return
            if not email:
                print("Email is required.")
                messagebox.showerror(
                    "Error",
                    "Email is required."
                )
                return
            dob = self.dob_picker.get()
            if not dob:
                print("Date of birth is required.")
                messagebox.showerror(
                    "Error",
                    "Date of birth is required."
                )
                return
            if not password:
                print("Password is required.")
                messagebox.showerror(
                    "Error",
                    "Password is required."
                )
                return
            if not confirm_password:
                print("Confirm password is required.")
                messagebox.showerror(
                    "Error",
                    "Confirm password is required."
                )
                return

            if password != confirm_password:
                print("Passwords do not match.")
                messagebox.showerror(
                    "Error",
                    "Passwords do not match."
                )
                return

            if not self.validate_phonenumber():
                print("Please enter a valid phone number.")
                messagebox.showerror(
                    "Error",
                    "Please enter a valid phone number."
                )
                return

            print("Profile saved successfully!")
            print(f"First Name: {first_name}")
            print(f"Last Name: {last_name}")
            print(f"Phone Number: +{self.selected_calling_code}+{phone_number}")
            print(f"Country: {self.selected_country_name} ({self.selected_country})")
            print(f"Date of Birth: {dob}")
            print(f"Email: {email}")
            print(f"Pet Avatar: {self.selected_avatar}")
            print(f"Profile Picture Path: {self.profile_image_path if self.profile_image_path else 'No profile picture uploaded.'}")

if __name__ == "__main__":
    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("blue")
    root = ctk.CTk()
    root.geometry("1200x750")
    root.minsize(900, 600)
    root.title("Calmora - Settings")
    app = SettingsPage(root)
    app.pack(fill="both", expand=True)
    root.mainloop()