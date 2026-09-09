import customtkinter as ctk
from PIL import Image
import pycountry
import phonenumbers
from datetime import date

ctk.set_appearance_mode("Light")
ctk.set_default_color_theme("blue")

class Profile():
    def __init__(self, root):
        self.root = root
        self.root.title("Calmora - Profile Page")
        self.root.geometry("1280x800")
        self.root.minsize(1000,700)
        self.selected_avatar = "🐱"
        self.profile_image = None
        self.password_visible = False
        self.create_ui()

    def create_ui(self):
        self.root.configure(fg_color = '#FDF9F3')
        container = ctk.CTkFrame(self.root, fg_color = '#FFFFFF')
        container.pack(fill = 'both', expand = True, padx = 35, pady = (45,25))
        container.grid_columnconfigure(1, weight = 1)
        container.grid_rowconfigure(0, weight = 1)
        self.create_sidebar_left(container)
        self.create_profile_area(container)

    def create_sidebar_left(self, parent):
        self.left_expanded = True
        self.collapse_width = 65
        self.left_sidebar = ctk.CTkFrame(parent, width = 265, fg_color = 'transparent')
        left_sidebar = self.left_sidebar
        left_sidebar.pack(side = 'left', fill = 'y')
        left_sidebar.pack_propagate = False
        self.top_left = ctk.CTkFrame(left_sidebar, height = 150, fg_color = '#FFFFFF')
        self.top_left.pack(fill = 'x', padx = 5, pady = (10,20))
        self.top_left.pack_propagate(False)
        self.logo = ctk.CTkLabel(self.top_left, text = 'Logo', width = 160, height = 70, fg_color = '#FFFFFF', text_color = '#4F6D7A', font = ("Arial", 13))
        self.logo.pack(side = 'left', fill = 'both', expand = True, padx = (0,10))
        self.toggle_left = ctk.CTkButton(self.top_left, text = '<', width = 45, height = 70, fg_color = '#FC7F9C', hover_color = '#F65C84', text_color = '#FFFFFF', font = ("Arial", 23), command = self.left_toggle)
        self.toggle_left.pack(side = 'right')
        self.menu_left = ctk.CTkFrame(left_sidebar, fg_color = 'transparent')
        self.menu_left.pack(fill = 'both', expand = True, padx = 3)
        self.left_buttons = []
        menu_items = [("Mental Health Survey",self.open_mhs), ("AI Chatbot",self.open_chatbot),("Appointment Booking",self.open_ab),("Journaling",self.open_j),("Mood Tracking",self.open_mt),("Goal Tracking",self.open_gt),("News / Blogs",self.open_nb),("Resources",self.open_rcs)]
        for text,command in menu_items:
            sep = ctk.CTkFrame(self.menu_left, height = 10, fg_color = '#FDF9F3')
            sep.pack(fill = 'x')
            button = ctk.CTkButton(self.menu_left, text = text, height = 48, fg_color = '#FC7F9C', text_color = '#FFFFFF', hover_color = "#F65C84", font = ("Arial", 13), anchor = 'center', command = command)
            button.pack(fill ='x')
            self.left_buttons.append((button,text))

    def left_toggle(self):
        if self.left_expanded:
            self.left_sidebar.configure(width = self.collapse_width)
            self.logo.pack_forget()
            self.toggle_left.configure(text = '>')
            for button,text in self.left_buttons:
                button.configure(text = '')
            self.left_expanded = False

        else:
            self.left_sidebar.configure(width = 265)
            self.logo.pack(side = 'left', fill = 'both', expand = True, padx = (0,10))
            self.toggle_left.configure(text = '<')
            for button,text in self.left_buttons:
                button.configure(text = text)
            self.left_expanded = True


    def open_mhs(self):
        print('Mental Health Survey Selected')

    def open_chatbot(self):
            print('AI Chatbot Selected')

    def open_ab(self):
            print('Appointment Booking Selected')

    def open_j(self):
            print('Journaling Selected')

    def open_mt(self):
            print('Mood Tracking Selected')

    def open_gt(self):
            print('Goal Tracking Selected')

    def open_nb(self):
            print('News / Blogs Selected')

    def open_rcs(self):
            print('Resources Selected')



    def create_sidebar_right(self):
        self.sidebar_open = True
        self.sidebar = ctk.CTkFrame(self,width = 90, height = self.winfo_height(), fg_color = '#FDF9F3')
        self.sidebar.place(relx = 1,rely = 0, anchor = 'ne', width = 90, height = self.winfo_height())
        close = ctk.CTkLabel(self.sidebar, text = 'V', font = ('Arial', 28, 'bold'), text_color = '#FFFFFF',fg_color = '#FC7F9C')
        close.pack(pady= (30,40))
        home_button = ctk.CTkButton(self.sidebar, text = '⌂', width = 55, height = 50, fg_color = '#FC7F9C', text_color = '#FFFFFF', hover_color = '#F65C84', font = ('Arial', 28), command = self.return_home)
        home_button.pack(pady = 10)
        profile_button = ctk.CTkButton(self.sidebar, text = '⛭', width = 55, height = 50, fg_color = '#FC7F9C', text_color = '#FFFFFF', hover_color = '#F65C84', font = ('Arial', 28), command = self.return_profile)
        profile_button.pack(pady = 10)
        self.after(100, lambda: self.sidebar.configure(height = self.winfo_height()))

        def toggle_sidebar(self):
            if self.sidebar_open:
                self.animate_sidebar_close()
            else:
                self.animate_sidebar_open()

        def animate_sidebar_open(self, height = 0):
            max_height = self.winfo_height()
            if max_height <= 1:
                self.after(50,lambda: self.animate_sidebar_open(height))
                return
            if height < max_height:
                height += 25
                if height > max_height:
                    height = max_height
                self.sidebar.configure(height = height, width = 90)
                self.after(10,lambda: self.animate_sidebar_open(height))
            else:
                self.sidebar_open = True

        def animate_sidebar_close(self, height = None):
            max_height = self.winfo_height()
            if max_height <= 1:
                return
            if height is None:
                height = max_height

            if height > 0:
                height -= 25
                if height < 0:
                    height = 0
                width = int(90*(height/max_height))
                if width < 1:
                    width = 1
                self.sidebar.configure(width = width, height = height)
                self.after(10,lambda: self.animate_sidebar_close(height))

            else:
                self.sidebar.configure(width = 1, height = 1)
                self.sidebar_open()

    def profile_area(self):
        self.main = ctk.CTkFrame(self, fg_color = "#FFFFFF")
        self.main.pack(side = 'left', fill = 'both', expand = True)

        top_bar = ctk.CTkFrame(self.main, fg_color ="#F65C84", height = 90)
        top_bar.pack(fill = 'x')
        top_bar.pack_propagate(False)
        title = ctk.CTkLabel(top_bar, text = "Profile", font = ("Arial", 25, 'bold'), text_color = '#FFFFFF')
        title.pack(side = 'left', padx = 35)
        content = ctk.CTkFrame(self.main, fg_color = "#FFFFFF")
        content.pack(fill = 'both', expand = True, padx = 40, pady = 30)
        profile_card = ctk.CTkFrame(content, fg_color = "#FFFFFF", corner_radius = 15)
        profile_card.pack(fill = 'x', pady = (0,25))
        image_frame = ctk.CTkFrame(profile_card, fg_color = 'transparent')
        image_frame.pack(pady = 25)
        self.avatar_label = ctk.CTkLabel(image_frame, text = self.selected_avatar, font = ("Segoe UI Emoji", 80), width = 150, height = 150)
        self.avatar_label.pack()
        self.avatar_preview = ctk.CTkLabel(image_frame, text = self.selected_avatar, font = ("Segoe UI Emoji", 25))
        self.avatar_preview.pack(pady = (5,0))
        button_frame = ctk.CTkFrame(profile_card, fg_color = 'transparent')
        button_frame.pack(pady = (0,25))
        upload_button = ctk.CTkButton(button_frame, text = 'Upload profile picture', width = 190, height = 40, fg_color = "#000000", text_color = "#FFFFFF", hover_color = "#333333", command = self.upload_picture)
        upload_button.pack(side='left', padx = 8)
        avatar_button = ctk.CTkButton(button_frame, text = 'Choose Pet Avatar', width = 170, height = 40, fg_color = '#000000', hover_color = "#333333", text_color = "#FFFFFF", command = self.open_avatar_window)
        avatar_button.pack(side='left', padx = 8)

    


    
