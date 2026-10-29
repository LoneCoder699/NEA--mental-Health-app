import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
from datetime import datetime, date, timedelta
import json
from pathlib import Path
from collections import deque
from tkcalendar import DateEntry

DATA_FILE = Path.home() / "goal_tracking_data.json"

BG = "#f5f5f5"
PANEL = "#dedede"
SIDEBAR = "#1E1E1E"
DARK = "#111111"
BLACK = "#000000"
WHITE = "#ffffff"
GRAY = "#777777"
GRID = "#8c8c8c"
LIGHT_GRAY = "#eeeeee"

class GoalTrackingPage(ctk.CTk):

    def __init__(self):


        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")

        super().__init__()

        self.title("Goal Tracking")
        self.geometry("1280x760")
        self.minsize(1050, 650)

        self.configure(fg_color=BG)

        self.tasks = []

        self.week = [0] * 7

        self.next_id = 1

        self.goal_queue = deque()

        self.completion_dates = []

        self.load_data()

        self.build_ui()

        self.refresh_all()

        self.bind(
            "<Control-n>",
            lambda e: self.open_task_popup()
        )

        self.bind(
            "<Control-s>",
            lambda e: self.save_data()
        )

        self.bind(
            "<Escape>",
            lambda e: self.close_task_popup()
        )
    
    
    def load_data(self):

        if DATA_FILE.exists():

            try:

                data = json.loads(
                    DATA_FILE.read_text(
                        encoding="utf-8"
                    )
                )

                self.tasks = data.get(
                    "tasks",
                    data.get("task", [])
                )

                self.week = data.get(
                    "week",
                    [0] * 7
                )

                self.completion_dates = data.get(
                    "completion_dates",
                    []
                )

                if not isinstance(self.tasks, list):
                    self.tasks = []

                if (
                    not isinstance(self.week, list)
                    or len(self.week) != 7
                ):
                    self.week = [0] * 7

                if not isinstance(
                    self.completion_dates,
                    list
                ):
                    self.completion_dates = []

                self.next_id = (
                    max(
                        [
                            int(
                                task.get(
                                    "id",
                                    0
                                )
                            )
                            for task in self.tasks
                        ]
                        + [0]
                    )
                    + 1
                )

                saved_queue = data.get(
                    "goal_queue"
                )

                if isinstance(
                    saved_queue,
                    list
                ):

                    self.goal_queue = deque(
                        int(task_id)
                        for task_id in saved_queue
                        if (
                            self.find_task(task_id)
                            is not None
                            and not self.find_task(
                                task_id
                            ).get(
                                "completed",
                                False
                            )
                        )
                    )

                else:

                    self.goal_queue = deque(
                        task["id"]
                        for task in self.tasks
                        if not task.get(
                            "completed",
                            False
                        )
                    )

                return

            except Exception:
                pass

        today = date.today().isoformat()

        self.tasks = [

            {
                "id": 1,
                "name": "Complete assignment",
                "deadline": today,
                "notes": "Finish today's assignment.",
                "recurring": False,
                "completed": True,
            },

            {
                "id": 2,
                "name": "Read for 30 minutes",
                "deadline": today,
                "notes": "Read a book or study material.",
                "recurring": False,
                "completed": True,
            },

            {
                "id": 3,
                "name": "Exercise",
                "deadline": today,
                "notes": "Complete a short workout.",
                "recurring": False,
                "completed": False,
            },

            {
                "id": 4,
                "name": "Study Python",
                "deadline": today,
                "notes": "Practice Python programming.",
                "recurring": False,
                "completed": False,
            },

            {
                "id": 5,
                "name": "Journal",
                "deadline": today,
                "notes": "Write today's journal entry.",
                "recurring": False,
                "completed": False,
            },
        ]

        self.next_id = 6

        self.goal_queue = deque(
            [3, 4, 5]
        )

        self.week = [
            2,
            4,
            3,
            5,
            3,
            6,
            4
        ]

        self.completion_dates = [
            date.today().isoformat()
        ]


    def save_data(self):

        try:

            DATA_FILE.write_text(
                json.dumps(
                    {
                        "tasks": self.tasks,
                        "week": self.week,
                        "goal_queue": list(
                            self.goal_queue
                        ),
                        "completion_dates":
                            self.completion_dates,
                    },
                    indent=2,
                ),
                encoding="utf-8",
            )

        except Exception as e:

            messagebox.showerror(
                "Save Error",
                str(e)
            )


    def find_task(self, task_id):

        return next(
            (
                task
                for task in self.tasks
                if task.get("id") == task_id
            ),
            None,
        )


    def enqueue_goal(self, task_id):

        task = self.find_task(task_id)

        if task is None:
            return

        if task.get(
            "completed",
            False
        ):
            return

        if task_id not in self.goal_queue:

            self.goal_queue.append(
                task_id
            )

        self.save_data()

        self.refresh_queue()
        self.refresh_tasks()


    def execute_next_goal(self):

        while self.goal_queue:

            task_id = self.goal_queue.popleft()

            task = self.find_task(
                task_id
            )

            if task is None:
                continue

            if task.get(
                "completed",
                False
            ):
                continue

            task["completed"] = True

            today_index = date.today().weekday()

            self.week[
                today_index
            ] += 1

            today_string = (
                date.today().isoformat()
            )

            if today_string not in self.completion_dates:

                self.completion_dates.append(
                    today_string
                )

            self.save_data()

            self.refresh_all()

            messagebox.showinfo(
                "Goal Executed",
                f"Completed:\n\n{task.get('name', 'Goal')}",
                parent=self,
            )

            return

        messagebox.showinfo(
            "Queue Empty",
            "There are no pending goals in the queue.",
            parent=self,
        )


    def clear_queue(self):

        if not self.goal_queue:

            messagebox.showinfo(
                "Queue Empty",
                "The goal queue is already empty.",
                parent=self,
            )

            return

        answer = messagebox.askyesno(
            "Clear Queue",
            "Remove all pending goals from the queue?\n\n"
            "The goals themselves will NOT be deleted.",
            parent=self,
        )

        if answer:

            self.goal_queue.clear()

            self.save_data()

            self.refresh_all()

   
    def calculate_streak(self):

        if not self.completion_dates:
            return 0

        try:

            completed_days = {
                datetime.strptime(
                    d,
                    "%Y-%m-%d"
                ).date()
                for d in self.completion_dates
            }

        except Exception:

            return 0

        current = date.today()

        if current not in completed_days:

            current -= timedelta(
                days=1
            )

        streak = 0

        while current in completed_days:

            streak += 1

            current -= timedelta(
                days=1
            )

        return streak

   
    def build_ui(self):

        self.grid_columnconfigure(
            0,
            weight=0
        )

        self.grid_columnconfigure(
            1,
            weight=1
        )

        self.grid_rowconfigure(
            0,
            weight=1
        )

        self.build_navbar()

        self.main = ctk.CTkFrame(
            self,
            fg_color=BG,
            corner_radius=0
        )

        self.main.grid(
            row=0,
            column=1,
            sticky="nsew"
        )

        self.main.grid_columnconfigure(
            0,
            weight=1
        )

        self.main.grid_rowconfigure(
            2,
            weight=1
        )

        self.build_header()

        self.build_summary()

        self.build_bottom()

        self.create_sidebar()

   
    def build_navbar(self):

        self.create_left_navbar()

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

    def go_home(self):
        self.close_dropdowns()
        print("Navigating to Home Page")

    def open_profile(self):
        self.close_dropdowns()
        print("Navigating to Profile Page")
    
    def logout(self):
        self.close_dropdowns()
        print("Logging out...")


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


    def build_header(self):

        self.header = ctk.CTkFrame(
            self.main,
            fg_color=BG,
            height=50
        )

        self.header.grid(
            row=0,
            column=0,
            sticky="ew",
            padx=16,
            pady=(8, 0)
        )

        self.header.grid_columnconfigure(
            0,
            weight=1
        )

        self.header_title = ctk.CTkLabel(
            self.header,
            text="Goal Tracking",
            font=("Arial", 20),
            text_color=DARK,
        )

        self.header_title.grid(
            row=0,
            column=0,
            sticky="w"
        )

        self.header_date = ctk.CTkLabel(
            self.header,
            text=date.today().strftime(
                "%A, %d %B %Y"
            ),
            font=("Arial", 10),
            text_color=DARK,
        )

        self.header_date.grid(
            row=0,
            column=1,
            padx=12
        )

        self.add_task_button = ctk.CTkButton(
            self.header,
            text="+ Add Goal",
            command=self.open_task_popup,
            fg_color=DARK,
            text_color=WHITE
        )

        self.add_task_button.grid(
            row=0,
            column=2
        )


    def build_summary(self):

        top = ctk.CTkFrame(
            self.main,
            fg_color="transparent"
        )

        top.grid(
            row=1,
            column=0,
            padx=16,
            pady=8,
            sticky="ew"
        )

        top.grid_columnconfigure(
            0,
            weight=1
        )

        top.grid_columnconfigure(
            1,
            weight=1
        )

        top.grid_columnconfigure(
            2,
            weight=2
        )
        completion = ctk.CTkFrame(
            top,
            fg_color=PANEL,
            height=145
        )

        completion.grid(
            row=0,
            column=0,
            padx=(0, 6),
            sticky="nsew"
        )

        completion.grid_propagate(
            False
        )

        ctk.CTkLabel(
            completion,
            text="CURRENT GOAL COMPLETION",
            text_color=DARK,
            font=("Arial", 10, "bold"),
        ).pack(
            anchor="nw",
            padx=12,
            pady=(9, 0)
        )

        self.pie_canvas = tk.Canvas(
            completion,
            bg=PANEL,
            highlightthickness=0,
            height=105,
        )

        self.pie_canvas.pack(
            fill="both",
            expand=True,
            padx=4
        )

        self.pie_canvas.bind(
            "<Configure>",
            lambda e: self.draw_pie()
        )

        streak = ctk.CTkFrame(
            top,
            fg_color=PANEL,
            height=145
        )

        streak.grid(
            row=0,
            column=1,
            padx=6,
            sticky="nsew"
        )

        streak.grid_propagate(
            False
        )

        ctk.CTkLabel(
            streak,
            text="STREAK",
            text_color=DARK,
            font=("Arial", 10, "bold"),
        ).pack(
            anchor="nw",
            padx=12,
            pady=(9, 0)
        )

        self.streak_day_label = ctk.CTkLabel(
            streak,
            text="Day\n0",
            text_color=DARK,
            font=("Arial", 14, "bold"),
        )

        self.streak_day_label.pack(
            pady=(7, 0)
        )

        self.streak_icon = ctk.CTkLabel(
            streak,
            text="♨",
            text_color=DARK,
            font=("Arial", 36),
        )

        self.streak_icon.pack()

        chart = ctk.CTkFrame(
            top,
            fg_color=PANEL,
            height=145
        )

        chart.grid(
            row=0,
            column=2,
            padx=(6, 0),
            sticky="nsew"
        )

        chart.grid_propagate(
            False
        )

        ctk.CTkLabel(
            chart,
            text="WEEKLY GOAL COMPLETION",
            text_color=DARK,
            font=("Arial", 10, "bold"),
        ).pack(
            anchor="nw",
            padx=12,
            pady=(9, 0)
        )

        self.bar_canvas = tk.Canvas(
            chart,
            bg=PANEL,
            highlightthickness=0,
            height=105,
        )

        self.bar_canvas.pack(
            fill="both",
            expand=True,
            padx=5
        )

        self.bar_canvas.bind(
            "<Configure>",
            lambda e: self.draw_bars()
        )

   
    def build_bottom(self):

        bottom = ctk.CTkFrame(
            self.main,
            fg_color=PANEL
        )

        bottom.grid(
            row=2,
            column=0,
            padx=16,
            pady=(0, 14),
            sticky="nsew"
        )

        bottom.grid_columnconfigure(
            0,
            weight=1
        )

        bottom.grid_columnconfigure(
            1,
            weight=1
        )

        bottom.grid_rowconfigure(
            0,
            weight=1
        )

        self.build_todo(
            bottom
        )

        self.build_schedule(
            bottom
        )

   
    def build_todo(self, parent):

        panel = ctk.CTkFrame(
            parent,
            fg_color=PANEL
        )

        panel.grid(
            row=0,
            column=0,
            padx=(0, 6),
            sticky="nsew"
        )

        panel.grid_rowconfigure(
            1,
            weight=1
        )

        panel.grid_columnconfigure(
            0,
            weight=1
        )

        header = ctk.CTkFrame(
            panel,
            fg_color=PANEL,
            height=45
        )

        header.grid(
            row=0,
            column=0,
            sticky="ew"
        )

        header.grid_columnconfigure(
            0,
            weight=1
        )

        ctk.CTkLabel(
            header,
            text="TO-DO LIST",
            text_color=DARK,
            font=("Arial", 11, "bold"),
        ).grid(
            row=0,
            column=0,
            padx=14,
            pady=12,
            sticky="w"
        )

        self.count_label = ctk.CTkLabel(
            header,
            text="",
            text_color=GRAY,
            font=("Arial", 9)
        )

        self.count_label.grid(
            row=0,
            column=1,
            padx=12
        )

        self.todo_scroll = ctk.CTkScrollableFrame(
            panel,
            fg_color=PANEL
        )

        self.todo_scroll.grid(
            row=1,
            column=0,
            padx=7,
            pady=(0, 7),
            sticky="nsew"
        )

        self.todo_scroll.grid_columnconfigure(
            0,
            weight=1
        )

        queue_bar = ctk.CTkFrame(
            panel,
            fg_color=PANEL
        )

        queue_bar.grid(
            row=2,
            column=0,
            padx=7,
            pady=(0, 7),
            sticky="ew"
        )

        queue_bar.grid_columnconfigure(
            0,
            weight=1
        )

        ctk.CTkButton(
            queue_bar,
            text="EXECUTE NEXT GOAL",
            height=34,
            fg_color=DARK,
            hover_color=GRAY,
            text_color=WHITE,
            command=self.execute_next_goal,
        ).grid(
            row=0,
            column=0,
            padx=(0, 4),
            sticky="ew"
        )

        ctk.CTkButton(
            queue_bar,
            text="CLEAR QUEUE",
            width=110,
            height=34,
            fg_color=GRAY,
            hover_color=WHITE,
            text_color=BLACK,
            command=self.clear_queue,
        ).grid(
            row=0,
            column=1,
            padx=(4, 0)
        )

        self.queue_status_label = ctk.CTkLabel(
            panel,
            text="Queue: 0 goals waiting",
            text_color=GRAY,
            font=("Arial", 9)
        )

        self.queue_status_label.grid(
            row=3,
            column=0,
            pady=(0, 7)
        )

   
    def build_schedule(self, parent):

        panel = ctk.CTkFrame(
            parent,
            fg_color=PANEL
        )

        panel.grid(
            row=0,
            column=1,
            padx=(6, 0),
            sticky="nsew"
        )

        panel.grid_rowconfigure(
            1,
            weight=1
        )

        panel.grid_columnconfigure(
            0,
            weight=1
        )

        action_bar = ctk.CTkFrame(
            panel,
            fg_color=PANEL,
            height=45
        )

        action_bar.grid(
            row=0,
            column=0,
            padx=0,
            sticky="ew"
        )

        action_bar.grid_columnconfigure(
            0,
            weight=1
        )

        ctk.CTkLabel(
            action_bar,
            text="Create New Goal",
            text_color=DARK,
            font=("Arial", 11),
        ).grid(
            row=0,
            column=0,
            padx=14,
            pady=10,
            sticky="w"
        )

        ctk.CTkButton(
            action_bar,
            text="CREATE",
            width=108,
            height=30,
            fg_color=BLACK,
            hover_color=GRAY,
            text_color=WHITE,
            font=("Arial", 10),
            command=self.open_task_popup,
        ).grid(
            row=0,
            column=1,
            padx=8
        )

        self.schedule_frame = ctk.CTkFrame(
            panel,
            fg_color=LIGHT_GRAY
        )

        self.schedule_frame.grid(
            row=1,
            column=0,
            padx=8,
            pady=(0, 8),
            sticky="nsew"
        )

        for col in range(7):

            self.schedule_frame.grid_columnconfigure(
                col,
                weight=1
            )

        for row in range(1, 7):

            self.schedule_frame.grid_rowconfigure(
                row,
                weight=1
            )

        self.schedule_header = [
            "Mon",
            "Tue",
            "Wed",
            "Thu",
            "Fri",
            "Sat",
            "Sun"
        ]

        self.schedule_cells = {}

        self.draw_schedule()

        ctk.CTkLabel(
            panel,
            text="Double-click a goal or empty schedule cell to edit/create",
            text_color="#666666",
            font=("Arial", 9),
        ).grid(
            row=2,
            column=0,
            pady=(0, 7)
        )

   
    def draw_schedule(self):

        for child in self.schedule_frame.winfo_children():

            child.destroy()

        self.schedule_cells.clear()

        monday = (
            date.today()
            - timedelta(
                days=date.today().weekday()
            )
        )

        for col, day_name in enumerate(
            self.schedule_header
        ):

            header = ctk.CTkLabel(
                self.schedule_frame,
                text=day_name,
                fg_color=LIGHT_GRAY,
                text_color=DARK,
                font=("Arial", 10, "bold"),
                height=27,
            )

            header.grid(
                row=0,
                column=col,
                padx=(1, 0),
                pady=(1, 0),
                sticky="nsew"
            )

        for col in range(7):

            target_date = (
                monday
                + timedelta(days=col)
            )

            tasks = [
                task
                for task in self.tasks
                if self.task_matches_day(
                    task,
                    target_date
                )
            ]

            for row in range(1, 7):

                task = (
                    tasks[row - 1]
                    if row - 1 < len(tasks)
                    else None
                )

                cell = ctk.CTkFrame(
                    self.schedule_frame,
                    fg_color=(
                        WHITE
                        if task is None
                        else DARK
                    ),
                    border_width=1,
                    border_color=GRID,
                )

                cell.grid(
                    row=row,
                    column=col,
                    padx=(1, 0),
                    pady=(1, 0),
                    sticky="nsew"
                )

                self.schedule_cells[
                    (col, row)
                ] = cell

                if task:

                    label = ctk.CTkLabel(
                        cell,
                        text=self.short_task_name(
                            task["name"]
                        ),
                        text_color=WHITE,
                        font=("Arial", 8),
                        wraplength=90,
                    )

                    label.pack(
                        fill="both",
                        expand=True
                    )

                    for widget in (
                        cell,
                        label
                    ):

                        widget.bind(
                            "<Double-Button-1>",
                            lambda e,
                            tid=task["id"]:
                            self.open_task_popup(
                                task_id=tid
                            )
                        )

                else:

                    hint = ctk.CTkLabel(
                        cell,
                        text="",
                        text_color="#777777",
                        font=("Arial", 8),
                    )

                    hint.pack(
                        fill="both",
                        expand=True
                    )

                    for widget in (
                        cell,
                        hint
                    ):

                        widget.bind(
                            "<Double-Button-1>",
                            lambda e,
                            d=target_date:
                            self.open_task_popup(
                                prefill_date=d
                            )
                        )


    def task_matches_day(
        self,
        task,
        target_date
    ):

        try:

            task_date = datetime.strptime(
                task.get(
                    "deadline",
                    ""
                ),
                "%Y-%m-%d"
            ).date()

            return task_date == target_date

        except Exception:

            return False


    def short_task_name(
        self,
        name
    ):

        if len(name) <= 16:
            return name

        return name[:14] + "..."

   
    def refresh_tasks(self):

        for child in (
            self.todo_scroll.winfo_children()
        ):

            child.destroy()

        completed = sum(
            bool(
                task.get(
                    "completed"
                )
            )
            for task in self.tasks
        )

        self.count_label.configure(
            text=(
                f"{completed}/"
                f"{len(self.tasks)} "
                f"completed"
            )
        )

        for row, task in enumerate(
            self.tasks
        ):

            self.make_task_row(
                task,
                row
            )


    def make_task_row(
        self,
        task,
        row
    ):

        card = ctk.CTkFrame(
            self.todo_scroll,
            fg_color=DARK,
            height=47
        )

        card.grid(
            row=row,
            column=0,
            padx=4,
            pady=2,
            sticky="ew"
        )

        card.grid_propagate(
            False
        )

        card.grid_columnconfigure(
            1,
            weight=1
        )

        complete_button = ctk.CTkButton(
            card,
            text=(
                "✓"
                if task.get("completed")
                else ""
            ),
            width=31,
            height=31,
            corner_radius=16,
            fg_color="#DDDDDD",
            hover_color="#BBBBBB",
            text_color=DARK,
            font=("Arial", 15, "bold"),
            command=lambda tid=task["id"]:
            self.toggle_task(tid),
        )

        complete_button.grid(
            row=0,
            column=0,
            padx=7,
            pady=8
        )

        name_label = ctk.CTkLabel(
            card,
            text=task.get(
                "name",
                "Goal Name"
            ),
            text_color=(
                GRAY
                if task.get("completed")
                else WHITE
            ),
            font=("Arial", 10, "bold"),
            anchor="w",
        )

        name_label.grid(
            row=0,
            column=1,
            padx=6,
            sticky="ew"
        )

        is_queued = (
            task["id"]
            in self.goal_queue
        )

        queue_button = ctk.CTkButton(
            card,
            text=(
                "✓Q"
                if is_queued
                else "Q"
            ),
            width=38,
            height=30,
            fg_color=(
                "#555555"
                if is_queued
                else GRAY
            ),
            hover_color=WHITE,
            text_color=(
                DARK
                if is_queued
                else WHITE
            ),
            command=lambda tid=task["id"]:
            self.enqueue_goal(tid),
        )

        queue_button.grid(
            row=0,
            column=2,
            padx=2
        )

        delete_button = ctk.CTkButton(
            card,
            text="X",
            width=32,
            height=32,
            fg_color=DARK,
            hover_color=GRAY,
            text_color=WHITE,
            font=("Arial", 14, "bold"),
            command=lambda tid=task["id"]:
            self.delete_task(tid),
        )

        delete_button.grid(
            row=0,
            column=3,
            padx=4
        )

        name_label.bind(
            "<Double-Button-1>",
            lambda e,
            tid=task["id"]:
            self.open_task_popup(
                task_id=tid
            ),
        )

        card.bind(
            "<Double-Button-1>",
            lambda e,
            tid=task["id"]:
            self.open_task_popup(
                task_id=tid
            ),
        )

   
    def refresh_queue(self):

        queue_ids = list(
            self.goal_queue
        )

        count = len(queue_ids)

        self.queue_status_label.configure(
            text=(
                f"Queue: "
                f"{count} "
                f"goals waiting"
            )
        )

   
    def toggle_task(
        self,
        task_id
    ):

        task = self.find_task(
            task_id
        )

        if not task:
            return

        old_state = bool(
            task.get(
                "completed"
            )
        )

        task["completed"] = not old_state

        if task["completed"]:

            self.goal_queue = deque(
                tid
                for tid in self.goal_queue
                if tid != task_id
            )

            today_index = (
                date.today().weekday()
            )

            self.week[
                today_index
            ] += 1

            today_string = (
                date.today().isoformat()
            )

            if (
                today_string
                not in self.completion_dates
            ):

                self.completion_dates.append(
                    today_string
                )

        else:

            if task_id not in self.goal_queue:

                self.goal_queue.append(
                    task_id
                )

        self.save_data()

        self.refresh_all()


    def delete_task(
        self,
        task_id
    ):

        task = self.find_task(
            task_id
        )

        if not task:
            return

        answer = messagebox.askyesno(
            "Delete Goal",
            (
                f"Delete "
                f"'{task.get('name', 'Goal')}'?"
            ),
            parent=self,
        )

        if not answer:
            return

        self.tasks = [
            task
            for task in self.tasks
            if task.get("id") != task_id
        ]

        self.goal_queue = deque(
            tid
            for tid in self.goal_queue
            if tid != task_id
        )

        self.save_data()

        self.refresh_all()

   
    def open_task_popup(
        self,
        task_id=None,
        prefill_date=None
    ):

        if (
            hasattr(
                self,
                "task_popup"
            )
            and self.task_popup.winfo_exists()
        ):

            self.task_popup.lift()

            self.task_popup.focus_force()

            return

        self.task_popup = ctk.CTkToplevel(
            self
        )

        self.task_popup.title(
            "Edit Goal"
            if task_id is not None
            else "Create New Goal"
        )

        self.task_popup.geometry(
            "440x500"
        )

        self.task_popup.resizable(
            False,
            False
        )

        self.task_popup.configure(
            fg_color=PANEL
        )

        self.task_popup.transient(
            self
        )

        self.task_popup.grab_set()

        self.task_popup.protocol(
            "WM_DELETE_WINDOW",
            self.close_task_popup
        )

        self.update_idletasks()

        x = (
            self.winfo_rootx()
            + (
                self.winfo_width()
                - 440
            )
            // 2
        )

        y = (
            self.winfo_rooty()
            + (
                self.winfo_height()
                - 500
            )
            // 2
        )

        self.task_popup.geometry(
            f"+{max(x, 0)}+{max(y, 0)}"
        )

        ctk.CTkLabel(
            self.task_popup,
            text=(
                "Edit Goal"
                if task_id is not None
                else "Create New Goal"
            ),
            text_color=DARK,
            font=("Arial", 17, "bold"),
        ).pack(
            anchor="w",
            padx=18,
            pady=12
        )

        form = ctk.CTkFrame(
            self.task_popup,
            fg_color=WHITE,
            corner_radius=2,
        )

        form.pack(
            fill="both",
            expand=True,
            padx=18,
            pady=(0, 18)
        )

        form.grid_columnconfigure(
            0,
            weight=1
        )

        ctk.CTkLabel(
            form,
            text="Goal Name",
            text_color=DARK,
            font=("Arial", 11, "bold"),
        ).grid(
            row=0,
            column=0,
            padx=18,
            pady=(18, 5),
            sticky="w"
        )

        self.task_entry = ctk.CTkEntry(
            form,
            height=38,
            corner_radius=2,
            border_width=1,
            fg_color=WHITE,
            text_color=DARK,
            placeholder_text="Enter Goal Name",
        )

        self.task_entry.grid(
            row=1,
            column=0,
            padx=18,
            sticky="ew"
        )

        ctk.CTkLabel(
            form,
            text="Deadline",
            text_color=DARK,
            font=("Arial", 11, "bold"),
        ).grid(
            row=2,
            column=0,
            padx=18,
            pady=(13, 5),
            sticky="w"
        )

        self.popup_deadline = DateEntry(
            form,
            width=20,
            date_pattern="dd/mm/yyyy",
            background=DARK,
            foreground=WHITE,
        )

        self.popup_deadline.grid(
            row=3,
            column=0,
            padx=18,
            sticky="w"
        )

        self.popup_recurring = tk.BooleanVar(
            value=False
        )

        ctk.CTkCheckBox(
            form,
            text="Recurring Goal",
            variable=self.popup_recurring,
            text_color=DARK,
            checkbox_width=20,
            checkbox_height=20,
            hover_color=GRAY,
        ).grid(
            row=4,
            column=0,
            padx=18,
            pady=13,
            sticky="w"
        )

        ctk.CTkLabel(
            form,
            text="Notes",
            text_color=DARK,
            font=("Arial", 11, "bold"),
        ).grid(
            row=5,
            column=0,
            padx=18,
            pady=(2, 5),
            sticky="w"
        )

        self.popup_notes = ctk.CTkTextbox(
            form,
            height=85,
            corner_radius=2,
            border_width=1,
            border_color=BLACK,
            fg_color=WHITE,
            text_color=DARK,
        )

        self.popup_notes.grid(
            row=6,
            column=0,
            padx=18,
            pady=(0, 12),
            sticky="ew"
        )

        button_frame = ctk.CTkFrame(
            form,
            fg_color=WHITE
        )

        button_frame.grid(
            row=7,
            column=0,
            padx=18,
            pady=(0, 18),
            sticky="ew"
        )

        button_frame.grid_columnconfigure(
            0,
            weight=1
        )

        button_frame.grid_columnconfigure(
            1,
            weight=1
        )

        ctk.CTkButton(
            button_frame,
            text="CANCEL",
            height=38,
            corner_radius=2,
            fg_color=GRAY,
            hover_color=WHITE,
            text_color=BLACK,
            command=self.close_task_popup,
        ).grid(
            row=0,
            column=0,
            padx=(0, 4),
            sticky="ew"
        )

        ctk.CTkButton(
            button_frame,
            text=(
                "UPDATE"
                if task_id is not None
                else "CREATE"
            ),
            height=38,
            corner_radius=2,
            fg_color=GRAY,
            hover_color=WHITE,
            text_color=BLACK,
            command=lambda:
            self.save_task_popup(
                task_id
            ),
        ).grid(
            row=0,
            column=1,
            padx=(4, 0),
            sticky="ew"
        )

        if task_id is not None:

            task = self.find_task(
                task_id
            )

            if task:

                self.task_entry.insert(
                    0,
                    task.get(
                        "name",
                        ""
                    )
                )

                self.set_popup_deadline(
                    task.get(
                        "deadline",
                        date.today().isoformat()
                    )
                )

                self.popup_recurring.set(
                    bool(
                        task.get(
                            "recurring",
                            False
                        )
                    )
                )

                self.popup_notes.insert(
                    "1.0",
                    task.get(
                        "notes",
                        ""
                    )
                )

        else:

            self.set_popup_deadline(
                (
                    prefill_date
                    or date.today()
                ).isoformat()
            )

        self.task_entry.focus_set()


    def set_popup_deadline(
        self,
        iso_value
    ):

        try:

            d = datetime.strptime(
                iso_value,
                "%Y-%m-%d"
            ).date()

        except Exception:

            d = date.today()

        self.popup_deadline.set_date(
            d
        )


    def get_popup_deadline(self):

        return self.popup_deadline.get_date().isoformat()


    def save_task_popup(
        self,
        task_id=None
    ):

        name = (
            self.task_entry
            .get()
            .strip()
        )

        if not name:

            messagebox.showwarning(
                "Missing Goal Name",
                "Please enter a goal name.",
                parent=self.task_popup,
            )

            self.task_entry.focus_set()

            return

        deadline = (
            self.get_popup_deadline()
        )

        notes = (
            self.popup_notes
            .get(
                "1.0",
                "end"
            )
            .strip()
        )

        recurring = bool(
            self.popup_recurring.get()
        )

        if task_id is None:

            new_id = self.next_id

            self.tasks.append(
                {
                    "id": new_id,
                    "name": name,
                    "deadline": deadline,
                    "notes": notes,
                    "recurring": recurring,
                    "completed": False,
                }
            )

            self.next_id += 1

            self.goal_queue.append(
                new_id
            )

        else:

            task = self.find_task(
                task_id
            )

            if task:

                task.update(
                    {
                        "name": name,
                        "deadline": deadline,
                        "notes": notes,
                        "recurring": recurring,
                    }
                )

                if not task.get(
                    "completed",
                    False
                ):

                    if task_id not in self.goal_queue:

                        self.goal_queue.append(
                            task_id
                        )

        self.save_data()

        self.close_task_popup()

        self.refresh_all()


    def close_task_popup(self):

        if hasattr(
            self,
            "task_popup"
        ):

            try:

                if self.task_popup.winfo_exists():

                    self.task_popup.grab_release()

                    self.task_popup.destroy()

            except Exception:

                pass

   
    def draw_pie(self):

        c = self.pie_canvas

        c.delete("all")

        w = max(
            c.winfo_width(),
            180
        )

        h = max(
            c.winfo_height(),
            80
        )

        total = len(
            self.tasks
        )

        completed = sum(
            bool(
                task.get(
                    "completed"
                )
            )
            for task in self.tasks
        )

        percent = (
            completed
            / total
            * 100
            if total
            else 0
        )

        size = min(
            90,
            h - 10
        )

        x0 = max(
            10,
            (w - size) / 2
        )

        y0 = (
            h - size
        ) / 2

        x1 = x0 + size

        y1 = y0 + size

        c.create_oval(
            x0,
            y0,
            x1,
            y1,
            outline=GRAY,
            width=10
        )

        if total:

            c.create_arc(
                x0,
                y0,
                x1,
                y1,
                start=90,
                extent=(
                    -360
                    * completed
                    / total
                ),
                style="arc",
                outline=DARK,
                width=10,
            )

        cx = (
            x0 + x1
        ) / 2

        cy = (
            y0 + y1
        ) / 2

        c.create_text(
            cx,
            cy - 3,
            text=f"{percent:.0f}%",
            fill=DARK,
            font=(
                "Arial",
                16,
                "bold"
            ),
        )

        c.create_text(
            cx,
            cy + 18,
            text=(
                f"{completed}/"
                f"{total}"
            ),
            fill=GRAY,
            font=(
                "Arial",
                8
            ),
        )

   
    def draw_bars(self):

        c = self.bar_canvas

        c.delete("all")

        w = max(
            c.winfo_width(),
            280
        )

        h = max(
            c.winfo_height(),
            90
        )

        left = 20
        right = 10
        top = 5
        bottom = 20

        chart_h = max(
            20,
            h - top - bottom
        )

        chart_w = max(
            50,
            w - left - right
        )

        max_value = max(
            max(self.week),
            1
        )

        for i in range(
            max_value + 1
        ):

            y = (
                top
                + chart_h
                - (
                    i
                    / max_value
                )
                * chart_h
            )

            c.create_line(
                left,
                y,
                w - right,
                y,
                fill="#b5b5b5"
            )

        days = [
            "Mon",
            "Tue",
            "Wed",
            "Thu",
            "Fri",
            "Sat",
            "Sun"
        ]

        slot = (
            chart_w / 7
        )

        bar_width = (
            slot * 0.56
        )

        for i, value in enumerate(
            self.week
        ):

            center = (
                left
                + slot * i
                + slot / 2
            )

            x0 = (
                center
                - bar_width / 2
            )

            x1 = (
                center
                + bar_width / 2
            )

            y1 = (
                top
                + chart_h
            )

            y0 = (
                y1
                - (
                    value
                    / max_value
                )
                * chart_h
            )

            if value == 0:

                y0 = y1 - 2

            c.create_rectangle(
                x0,
                y0,
                x1,
                y1,
                fill="#444444",
                outline="#222222",
            )

            c.create_text(
                center,
                y0 - 7,
                text=str(value),
                fill=DARK,
                font=(
                    "Arial",
                    7
                )
            )

            c.create_text(
                center,
                h - 10,
                text=days[i],
                fill=DARK,
                font=(
                    "Arial",
                    8
                ),
            )

   
    def refresh_all(self):

        self.refresh_tasks()

        self.refresh_queue()

        self.draw_schedule()

        self.draw_pie()

        self.draw_bars()

        streak = self.calculate_streak()

        self.streak_day_label.configure(
            text=f"Day\n{streak}"
        )

if __name__ == "__main__":

    app = GoalTrackingPage()

    app.mainloop()
