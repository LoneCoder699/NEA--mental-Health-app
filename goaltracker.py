import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
from datetime import datetime,date,timedelta
import json
from pathlib import Path
from tkcalendar import DateEntry

DATA_FILE = Path.home()/'goal_tracking_data.json'
BG = "#f5f5f5"
PANEL = "#dedede"
SIDEBAR = "#1E1E1E"
DARK = "#111111"
BLACK = "#000000"
WHITE = "#ffffff"
GRAY = "#777777"
GRID = "#8c8c8c"

class GoalTrackingPage(ctk.CTk):
    def __init__(self):
        ctk.set_appearance_mode('light')
        ctk.set_default_color_theme('blue')
        self.title("Goal Tracking")
        self.geometry("1280x760")
        self.minsize(1050,650)
        self.configure(fg_color = BG)
        self.sidebar_expanded = True
        self.tasks = []
        self.week = [1,2,3,4,5,6,7]
        self.next_id = 1
        self.load_data()
        self.build_ui()
        self.refresh_all()
        self.bind('<Control-n>', lambda e: self.open_task_popup())
        self.bind('<Control-s>', lambda e: self.save_data())
        self.bind('<Escape>', lambda e: self.close_task_popup())

    def load_data(self):
        if DATA_FILE.exists():
            try:
                data = json.loads(DATA_FILE.read_text(encoding='utf-8'))
                self.tasks = data.get("task",[])
                self.week = data.get("week",[0]*7)
                if not isinstance(self.tasks,list):
                    self.tasks = []
                if len(self.week) != 7:
                    self.week = [0]*7
                self.next_id = max([int(t.get('id',0)) for t in self.tasks]+[0])+1
                return
            except Exception:
                pass

        today = date.today().isoformat()
        self.tasks = [{'id':1,'name':'task name', 'deadline': today,'notes':'abc','recurring':False, 'completed': True},
                      {'id':2,'name':'task name', 'deadline': today,'notes':'abc','recurring':False, 'completed': True},
                      {'id':3,'name':'task name', 'deadline': today,'notes':'abc','recurring':False, 'completed': False},
                      {'id':4,'name':'task name', 'deadline': today,'notes':'abc','recurring':False, 'completed': False},
                      {'id':5,'name':'task name', 'deadline': today,'notes':'abc','recurring':False, 'completed': False}
                      ]
        
        self.next_id = 6

    def save_data(self):
        try:
            DATA_FILE.write_text(json.dumps({'task':self.tasks,'week':self.week},indent = True),encoding = 'utf-8')
        except Exception as e:
            messagebox.showerror('Save Error',str(e))

    def build_ui(self):
        self.grid_columnconfigure(0,weight = 0)
        self.grid_columnconfigure(1,weight = 1)
        self.grid_rowconfigure(0,weight = 1)
        self.build_navbar()
        self.main = ctk.CTkFrame(self, fg_color = BG, corner_radius = 0)
        self.main.grid(row = 0, column = 1, sticky = 'nsew')
        self.main.grid_columnconfigure(0,weight = 1)
        self.main.grid_rowconfigure(2,weight = 1)
        self.build_header()
        self.build_summary()
        self.build_bottom()

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


    def build_header(self):
        self.header = ctk.CTkFrame(self.main, fg_color = BG, height = 50)
        self.header.grid(row = 0, column = 0, sticky = 'ew', padx = 16, pady = (8,0))
        self.header.grid_columnconfigure(0,weight = 1)
        self.header_title = ctk.CTkLabel(self.header,text = "Goal Tracking",font = ("Arial",20),text_color=DARK)
        self.header_title.grid(row = 0, column = 0, sticky = 'w')
        self.header_date = ctk.CTkLabel(self.header,text = date.today().strftime('%A, %d %B %Y'),font = ("Arial",10),text_color=DARK)
        self.header_date.grid(row = 0, column = 1, padx = 12)
        self.add_task_button = ctk.CTkButton(self.header,text = "+ Add Task",command=self.open_task_popup)
        self.add_task_button.grid(row = 0, column = 2)

    
    def build_summary(self):
        top = ctk.CTkFrame(self.main, fg_color = 'transparent')
        top.grid(row = 1, column = 0, padx = 16, pady = 8, sticky = 'ew')
        top.grid_columnconfigure(0,weight = 1)
        top.grid_columnconfigure(1,weight = 1)
        top.grid_columnconfigure(2,weight = 2)
        completion = ctk.CTkFrame(top,fg_color = PANEL, height = 145)
        completion.grid(row = 0, column = 0, padx = (0,6), sticky = 'nsew')
        completion.grid_propagate(False)
        self.c_label = ctk.CTkLabel(completion,text = 'CURRENT TASK COMPLETION', text_color = DARK, font = ('Arial', 10,'bold'))
        self.c_label.pack(anchor = 'nw', padx = 12,pady = (9,0))
        self.pie_canvas = tk.Canvas(completion,bg = PANEL,highlightthickness= 1, height = 105)
        self.pie_canvas.pack(fill = 'both', expand = True, padx = 4)
        self.pie_canvas.bind('<Configure>', lambda e: self.draw_pie())
        streak = ctk.CTkFrame(top,fg_color = PANEL, height = 145)
        streak.grid(row = 0, column = 1, padx = 6, sticky = 'nsew')
        streak.grid_propagate(False)
        self.streak_label = ctk.CTkLabel(streak,text = 'STREAK', text_color = DARK, font = ("Arial", 10, 'bold'))
        self.streak_label.pack(anchor = 'nw', padx = 12, pady = (9,0))
        self.day_label = ctk.CTkLabel(streak, text = 'Day\n25', text_color = DARK)
        self.streak_icon = ctk.CTkLabel(streak, text="♨", text_color = DARK, font = ('Arial', 37))
        self.streak_icon.pack()
        chart = ctk.CTkFrame(top,fg_color = PANEL, height = 145)
        chart.grid(row = 0, column = 2, padx = (6,0), sticky = 'nsew')
        chart.grid_propagate(False)
        chart_label = ctk.CTkLabel(chart,text = 'WEEKLY TASK COMPLETION', text_color = DARK, font = ("Arial", 10, 'bold'))
        chart_label.pack(anchor = 'nw', padx = 12, pady = (9,0))
        self.bar_canvas = tk.Canvas(chart, bg = PANEL, highlightthickness=1, height = 105)
        self.bar_canvas.pack(fill = 'both', expand = True, padx = 5)
        self.bar_canvas.bind('<Configure>', lambda e: self.draw_bars())

    def build_botton(self):
        bottom = ctk.CTkFrame(self.main, fg_color = PANEL)
        bottom.grid(row = 2, column = 0, padx = 16, pady = (0,14), sticky = 'nsew')
        bottom.grid_columnconfigure(0,weight = 1)
        bottom.grid_columnconfigure(1,weight = 1)
        bottom.grid_columnconfigure(2,weight = 2)
        self.build_todo(bottom)
        self.build_schedule(bottom)

    def build_todo(self, parent):
        panel = ctk.CtkFrame(parent, fg_color = PANEL)
        panel.grid(row = 0,column = 0, padx = (0,6), sticky = 'nsew')
        panel.grid_rowconfigure(1,weight = 1)
        panel.grid_columnconfigure(0,weight = 1)
        header = ctk.CTkFrame(panel, fg_color = PANEL, height = 45)
        header.grid(row = 0, column = 0, sticky = 'ew')
        header_label = ctk.CTkLabel(header, text = 'TO-DO LIST', text_color = DARK, font = ('Arial', 11,'bold'))
        header_label.grid(row = 0, column = 0, padx = 14, pady = 12, sticky = 'w')
        self.count_label = ctk.CTkLabel(header, text = '', text_color = GRAY, font = ("Arial", 9))
        self.count_label.grid(row = 0, column = 1, padx = 12)
        self.todo_scroll = ctk.CTkScrollableFrame(panel, fg_color = PANEL)
        self.todo_scroll.grid(row = 1, column = 0, padx = 7, pady = (0,7), sticky = 'nsew')
        self.todo_scroll.grid_columnconfigure(0,weight = 1)

    def build_schedule(self, parent):
        panel = ctk.CtkFrame(parent, fg_color = PANEL)
        panel.grid(row = 0,column = 1, padx = (6,0), sticky = 'nsew')
        panel.grid_rowconfigure(1,weight = 1)
        panel.grid_columnconfigure(0,weight = 1)
        action_bar = ctk.CTkFrame(panel, fg_color = PANEL, height = 45)
        action_bar.grid(row = 0, column = 0, padx = 0, sticky = 'ew')
        action_bar.grid_columnconfigure(0, weight = 1)
        new_task_label = ctk.CTklabel(action_bar, text = 'Create New Task', text_color = DARK, font = ("Arial", 11))
        new_task_label.grid(row = 0, column = 0, padx = 14, pady = 10, sticky = 'w')
        create_button = ctk.CTkButton(action_bar, text = 'CREATE', width = 108, height = 30, fg_color = BLACK, hover_color = GRAY, text_color = WHITE, font = ('Arial', 10), command = self.opem_task_popup)
        create_button.grid(row = 0, column = 1, padx = 8)
        self.schedule_frame = ctk.CTkFrame(panel, fg_color = "#EEEEEE")
        self.schedule_frame.grid(row = 1, column = 0, padx = 8, pady = (0,8), sticky = 'nsew')
        self.schedule_frame.grid_columnconfigure(tuple(range(7)), weight = 1)
        self.schedule_frame.grid_rowconfigure(tuple(range(1,7)), weight = 1)
        self.schedule_header = ["Mon","Tue","Wed","Thu","Fri","Sat","Sun"]
        self.schedule_cells = {}
        self.draw_schedule()
        edit_label = ctk.CTkLabel(panel, text = 'Double click- A task or an empty schedule cell to edit or create', text_color = '#666666', font = ("Arial", 9))
        edit_label.grid(row = 2, column = 0, pady = (0,7))

    def draw_schedule(self):
        for child in self.schedule_frame.winfo_children():
            child.destroy()
        self.schedule_cells.clear()
        monday = date.today()-timedelta(days = date.today().weekday())
        for col, day_name in enumerate(self.schedule_header):
            header = ctk.CTkLabel(self.schedule_frame, text = day_name, fg_color = '#EEEEEE', text_color = DARK, fomt = ("Arial",10,'bold'), height = 27)
            header.grid(row = 0, column = col, padx = (1,0), pady = (1,0), sticky = 'nsew')
        for col in range(7):
            target_date = monday+timedelta(days = col)
            tasks = [e for e in self.tasks if self.task_matches_day(e,target_date)]
            for row in range(1,7):
                task = tasks[row-1] if row-1 < len(tasks) else None
                cell = ctk.CTkFrame(self.schedule_frame, fg_color = WHITE if task is None else DARK, border_width = 1,  border_color = GRID)
                cell.grid(row = row, column = col, padx = (1,0), pady = (1,0), sticky = 'nsew')
                self.schedule_cells[(col,row)] = cell
                if task:
                    label = ctk.CTkLabel(cell,text = self.short_task_name(task['name']), text_color = WHITE, font = ('Arial',8), wraplength=90)
                    for widget in cell,label:
                        widget.bind("<DoubleButton-1>",lambda e, tid = task['id']:self.open_task_popup(task_id=tid))
                else:
                    hint = ctk.CTkLabel(cell,text="", text_color = "#777777", font = ("Arial",8))
                    hint.pack(fill='both', expand = True)
                    for widget in (cell,hint):
                        widget.bind("<DoubleButton-1>",lambda e,d=target_date:self.open_task_popup(fill_date=d))


    def task_matches_day(self, task, target_date):
        try:
            task_date = datetime.strptime(task.get('Deadline', ''),'%Y-%m-%d').date()
            return task_date == target_date
        except Exception:
            return False


    def short_task_name(self,name):    
        if len(name) <= 16:
            return name
        return name[:14]+'...'


    def refresh_tasks(self):
        for child in self.todo_scroll.winfo_children():
            child.destroy()
        completed = sum(bool(t.get('completed')) for t in self.tasks)
        self.count_label.configure(text = f"{completed}/{len(self.tasks)} completed")
        for row, task in enumerate(self.tasks):
            self.make_task_row(task,row)


    def make_task_row(self, task, row):
        card = ctk.CTkFrame(self.todo_scroll, fg_color = DARK, height = 47)
        card.grid(row = row, column = 0, padx = 2, padx = 4, sticky = 'ew')
        card.grid_propagate(False)
        card.grid_columnconfigure(1, weight = 1)
        complete_button = ctk.CTkButton(card,text = '✓' if task.get('completed') else '', width = 31, height = 31, corner_radius = 16, fg_color = '#DDDDDD', hover_color = '#BBBBBB', text_color = DARK, font = ("Arial", 15, 'bold'), command = lambda tid = task['id']:self.toggle_task(id))
        complete_button.grid(row = 0,column = 0, padx = 7, pady = 8)
        name_label = ctk.CTkLabel(card, text = task.get('name','Task Name'), text_color = GRAY if task.get('completed') else WHITE, font = ("Arial", 10, 'bold'), anchor = 'w')
        name_label.grid(row = 0, column = 1, padx=6, sticky = 'ew')
        delete_button = ctk.CTkButton(card, text = 'X', width = 32, height = 32, fg_color = DARK, hover_color = GRAY, text_color = WHITE, font = ("Arial", 14, 'bold'), command = lambda tid = task['id']: self.delete_task(tid))
        delete_button.grid(row = 0, column = 2, padx = 4)
        name_label.bind('<Double-Button-1>', lambda e, tid = task['id']: self.open_task_popup(task_id = tid))
        card.bind('<Double-Button-1>', lambda e, tid = task['id']: self.open_task_popup(task_id = tid))

    def toggle_task(self, task_id):
        for task in self.tasks:
            if task['id'] == task_id:
                task['completed'] = not bool(task.get('completed'))
                today_index = date.today().weekday()
                if task['completed']:
                    self.week[today_index]+=1
                elif self.week['today_index'] >0:
                    self.week['today_index'] -=1
                break

        self.save_data()
        self.refresh_all()


    def delete_tasks(self, task_id):
        task = next((t for t in self.tasks if t.get('id') == task_id), None)
        if not task:
            return
        answer = messagebox.askyesno('Delete Task',f"Delete '{task.get('name','Task Name')}'?")
        if not answer:
            return
        self.tasks = [t for t in self.tasks if t.get('id')!=task_id]
        self.save_data()
        self.refresh_all()


    def open_task_popup(self,task_id = None, prefill_date = None):
        if hasattr(self,'task_popup') and self.task_popup.winfo_exists():
            self.task_popup.lift()
            self.task_popup.focus_force
            return
        self.task_popup = ctk.CTkToplevel(self)
        self.task_popup.title('Edit Task' if task_id is not None else 'Create New Task')
        self.task_popup.geometry('440x500')
        self.task_popup.resizable(False,False)
        self.task_popup.configure(fg_color = PANEL)
        self.task_popup.transient(self)
        self.task_popup.grab_set()
        self.task_popup.protocol('WM_DELETE_WINDOW', self.close_task_popup)
        self.update_idletasks()
        x = self.winfo_rootx()+(self.winfo_width()-440)//2
        y = self.winfo_rooty()+(self.winfo_height()-500)//2
        self.task_popup.geometry(f"+{max(x,0)}+{max(y,0)}")
        edit_task = ctk.CTkLabel(self.task_popup,text = 'Edit Task' if task_id is not None else 'Create New Task', text_color = DARK,font = ("Arial",17,'bold'))
        form = ctk.CTkFrame(self.task_popup, fg_color = WHITE, corner_radius=2)
        form.pack(fill = 'both', expand = True, padx = 18, pady = (0,18))
        form.grid_columnconfigure(0,weight = 1)
        task_name = ctk.CTkLabel(form,text = 'Task Name', text_color = DARK, font = ("Arial",11,'bold'))
        task_name.grid(row = 0, column = 0, padx = 18, pady = (18,5, stick = 'w'))
        self.task_entry = ctk.CTkEntry(form, height = 38, corner_radius = 2, border_width = 1, fg_color = WHITE, text_color = DARK, placeholder_text='Enter Task Name')
        self.task_entry.grid(row = 1, column = 0, padx = 18, sticky = 'ew')
        deadline_label = ctk.CTkLabel(form, text = 'Deadline', text_color = DARK, font = ('Arial',11,'bold'))
        deadline_label.grid(row = 2, column = 0, padx = 18, pady = (13,5), sticky = 'w')
        self.popup_deadline = DateEntry(form, width = 20, date_pattern = 'dd/mm/yyyy', bg = DARK, fg_color = WHITE, border_width = 1)
        self.popup_deadline.grid(row = 3, column = 0, padx = 18, sticky = 'w')
        self.popup_recurring = tk.BooleanVar(value = False)
        recur_task = ctk.CTkCheckBox(form, text = 'Recurring Task', variable = self.popup_recurring, text_color = DARK, hover_color=GRAY,checkbox_width=20, checkbox_height=20)
        recur_task.grid(row = 4, column = 0, padx = 18, pady = 13, sticky = 'w')
        notes_label = ctk.CTkLabel(form, text = 'Notes', text_color = DARK, font = ("Arial", 11, 'bold'))
        notes_label.grid(row = 5, column = 0, padx = 18, pady = (2,5), sticky = 'w')
        self.popup_notes = ctk.CTkTextbox(form, height = 85)