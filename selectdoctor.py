import customtkinter as ctk
import os
try:
    from PIL import Image
except ImportError:
    Image = None

ctk.set_appearance_mode('light')

DARK = "#111111"
BLACK = "#000000"
WHITE = "#ffffff"
GRAY = "#777777"
LIGHT_GRAY = "#eeeeee"
HOVER = "#333333"

DOCTORS= [{'name':'Dr.Bob','info':'MBBS, 10 years exp','rating':'4.67/5', 'image':'doc1.jpeg'},
          {'name':'Dr.Bill','info':'MBBS, 6.7 years exp','rating':'3.8/5', 'image':'doc2.jpeg'},
          {'name':'Dr.Phil','info':'MBBS, 5 years exp','rating':'4/5', 'image':'doc3.jpeg'},
          {'name':'Dr.Will','info':'MBBS, 18 years exp','rating':'5/5', 'image':'doc4.jpeg'}
          ]

class Select_Doctor_Page(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title('Select Doctor')
        self.geometry('1100x720')
        self.minsize(820,560)
        self.columnconfigure(1,weight = 1)
        self.rowconfigure(0, weight = 1)
        self.images = []
        self.create_left_navbar()
        self.build_ui()

    def create_left_navbar(self):

        self.left_nav_expanded = True

        self.left_nav_width = 260

        self.left_nav_collapsed_width = 65

        self.left_navbar = ctk.CTkFrame(
            self,
            width=self.left_nav_width,
            fg_color=GRAY,
            corner_radius=0,
        )

        self.left_navbar.grid(
            row=0,
            column=0,
            sticky="ns"
        )

        self.left_navbar.grid_propagate(
            False
        )

        self.left_nav_top = ctk.CTkFrame(
            self.left_navbar,
            height=100,
            fg_color="transparent",
        )

        self.left_nav_top.pack(
            fill="x",
            padx=5,
            pady=(10, 20)
        )

        self.left_nav_top.pack_propagate(
            False
        )

        self.left_logo = ctk.CTkLabel(
            self.left_nav_top,
            text="Logo",
            width=160,
            height=70,
            fg_color=SIDEBAR,
            text_color=WHITE,
            font=("Arial", 13),
            corner_radius=0,
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
            command=self.toggle_left_navbar,
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

            (
                "Mental health survey",
                self.open_mental_health_survey
            ),

            (
                "AI ChatBot",
                self.open_ai_chatbot
            ),

            (
                "Appointment Booking",
                self.open_appointment_booking
            ),

            (
                "Journaling",
                self.open_journaling
            ),

            (
                "Mood Tracking",
                self.open_mood_tracking
            ),

            (
                "Goal Tracking",
                self.open_goal_tracking
            ),

            (
                "News/ Blogs",
                self.open_news_blogs
            ),

            (
                "Resources",
                self.open_resources
            ),
        ]

        for text, command in menu_items:

            separator = ctk.CTkFrame(
                self.left_menu_frame,
                height=10,
                fg_color=GRAY,
                corner_radius=0,
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
                command=command,
            )

            button.pack(
                fill="x"
            )

            self.left_nav_buttons.append(
                (button, text)
            )

    def go_home(self):
        self.close_dropdowns()
        print("Navigating to Home Page")

    def open_profile(self):
        self.close_dropdowns()
        print("Navigating to Profile Page")
    
    def logout(self):
        self.close_dropdowns()
        print("Logging out...")

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

    def build_ui(self):
        self.page = ctk.CTkFrame(self,fg_color = WHITE)
        self.page.grid(row = 0, column = 1, sticky = 'nsew')
        self.page.columnconfigure(0,weight = 1)
        self.page.rowconfigure(2, weight = 1)
        select_label = ctk.CTkLabel(self.page, text = 'Select Doctor', font = ('Arial', 45, 'bold'))
        select_label.grid(row = 0, column = 0, pady = (20,0))
        description_label = ctk.CTkLabel(self.page, text = 'Description', font = ('Arial', 45, 'bold'))
        description_label.grid(row = 1, column = 0, pady = (8,20))
        scroll = ctk.CTkScrollableFrame(self.page, fg_color = 'transparent')
        scroll.grid(row = 2, column = 0, sticky = 'nsew', pady = (60,20))
        scroll.columnconfigure(0,weight = 1)
        for i,doc in enumerate(DOCTORS):
            self.doc_card(scroll,doc,i)

    def doc_card(self,parent,doc,row):
        card = ctk.CTkFrame(parent,fg_color = 'transparent')
        card.grid(row = row, column = 0, sticky = 'ew', padx = 40, pady = (0,25))
        card.columnconfigure(1, weight = 1)
        image_box = ctk.CTkFrame(card,width = 115, height = 110, fg_color = LIGHT_GRAY)
        image_box.grid(row= 0, column = 0, padx = (0,45), sticky = 'n')
        image_box.grid_propagate(False)
        image_box.pack_propagate(False)
        image = None
        path = os.path.join(os.path.dirname(os.path.abspath(__file__)),doctor['image'])
        if Image and os.path.exists(path):
            try:
                image = ctk.CTkImage(Image.open(path),size = (115,110))
                self.images.append(image)
            except Exception:
                image = None

            if image:
                image_label = ctk.CTkLabel(image_box,image=image, text='')
                image_label.pack(fill = 'both', expand = True)
            else:
                image_label = ctk.CTkLabel(image_box, text='image', text_color = BLACK, font = ("Arial",20))
                image_label.pack(expand = True)

            info = ctk.CTkFrame(card,height = 110, fg_color = LIGHT_GRAY)
            info.grid(row=0,column =1, sticky ='ew')
            info.pack_propagate(False)
            for text in (doc['name'],doc['info'],doc['rating']):
                allinfo_label = ctk.CTkLabel(info,text = text, font = ("Arial", 14), text_color = 'black', anchor = 'w')
                allinfo_label.pack(fill = 'x', padx = 15)

            book_button = ctk.CTkButton(info, text = "BOOK NOW", width = 160, height = 30, fg_color = BLACK, hover_color=HOVER, text_color = WHITE, font = ("Arial", 14), command = lambda: self.book(doc))
            book_button.pack(anchor = 'w', padx = 15, pady = (4,0))

    def book(self,doc):
        messagebox.showinfo('all info', f'Doctor: {doc['name']}')

if __name__ == '__main__':
    Select_Doctor_Page().mainloop()
                


