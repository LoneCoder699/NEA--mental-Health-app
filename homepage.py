import customtkinter as ctk

ctk.set_appearance_mode("Light")
ctk.set_default_color_theme("blue")

class Home:
    def __init__(self,root):
        self.root = root
        self.root.title('Calmora')
        self.root.geometry("1100x700")
        self.root.minsize(900,600)
        self.ui()

    def ui(self):
        self.root.configure(fg_color = "#FDF9F3")
        header = ctk.CTkFrame(self.root,height = 75,fg_color = 'white', corner_radius= 0)
        header.pack(fill='x')
        header.pack_propagate(False)
        ctk.CTkLabel(header,text = "Calmora", font = ("Helvetica", 28, "bold"), text_color="#000000").pack(padx = 40, pady = 20)
        main = ctk.CTkScrollableFrame(self.root, fg_color = 'transparent')
        main.pack(fill = 'both', expand = True, padx = 45, pady = 35)
        ctk.CTkLabel(main, text = 'Good to see you 🌸', font =("Georgia", 34, "bold"), text_color = "#000000").pack(anchor = 'w')
        ctk.CTkLabel(main, text = "Take a breath, let's look at yourself today", font =("Times New Roman", 20)).pack(anchor = 'w', pady = (5,25))
        feel = ctk.CTkFrame(main, height = 350, corner_radius = 22, fg_color = "#FFFFFF")
        feel.pack(fill = 'x', pady = (0,25))
        feel.pack_propagate(False)

        ctk.CTkLabel(feel, text = "Negative Feelings", font = ("Arial",22,'bold'), text_color = '#000000').pack(anchor = 'w', padx = 25, pady = (20,12))
        ctk.CTkLabel(feel, text = "It's okay to have them, you're not alone 💙", font = ("Arial",16,'bold'), text_color = '#000000').pack(anchor = 'w', padx = 25, pady = (20,12))
        neg = ctk.CTkFrame(feel, fg_color = 'transparent')
        neg.pack(anchor = 'w', padx = 20)
        for text in ['Scared 😨','Numb 😶', 'Sad ☹️', 'Low 😕', 'Anxious 😥', 'Overwhelmed 🥵', 'Lonely 😞', 'Angry 😡', 'Hopeless 😔']:
            ctk.CTkButton(neg, text = text, width = 105, height = 35, corner_radius=18,fg_color = "#FFFDFA", text_color = '#FC7F9C', hover_color = '#FFC1DC').pack(side = 'left', padx = 5)

        ctk.CTkLabel(feel, text = "Positive Feelings", font = ("Arial",22,'bold'), text_color = '#000000').pack(anchor = 'w', padx = 25, pady = (20,12))
        ctk.CTkLabel(feel, text = "Celebrate them too", font = ("Arial",16,'bold'), text_color = '#000000').pack(anchor = 'w', padx = 25, pady = (20,12))
        pos = ctk.CTkFrame(feel, fg_color = 'transparent')
        pos.pack(anchor = 'w', padx = 20)
        for text in ["Happy 😊", "Relieved 😌", "Calm 😇", "Hopeful 🌤️", "Grateful 🙏", "Content 🙂", "Excited 🤩", "Proud 😎", "Motivated 💪"]:
            ctk.CTkButton(pos, text = text, width = 105, height = 35, corner_radius=18,fg_color = '#FFFDFA', text_color = '#FC7F9C', hover_color = '#FFC1DC').pack(side = 'left', padx = 5)

        cards = ctk.CTkFrame(main, fg_color = 'transparent')
        cards.pack(fill = 'both', expand = True)
        self.card(cards, '😥', 'Anxious', "Persistent worry, restlessness, rapid heartbeat, difficulty concentrating, sleep disturbances, and muscle tension.\nSELF-CARE TIPS\n• Deep breathing exercises\n• Limit caffeine intake\n• Grounding techniques (5-4-3-2-1)").grid(row=0, column=0, padx=8, pady=8, sticky='nsew')
        self.card(cards, '🥵', 'Stress', "Overwhelm, irritability, headaches, difficulty focusing, and feeling out of control.\nSELF-CARE TIPS\n• Progressive muscle relaxation\n• Time management strategies\n• Mindfulness practices").grid(row=0, column=1, padx=8, pady=8, sticky='nsew')
        self.card(cards, '😶', 'Burnout', "Emotional exhaustion, detachment from work, reduced sense of accomplishment, and cynicism.\nSELF-CARE TIPS\n• Set firm boundaries\n• Take regular breaks\n• Reconnect with meaningful activities").grid(row=0, column=2, padx=8, pady=8, sticky='nsew')
        self.card(cards, '☹️', 'Depression', "Persistent sadness, loss of interest, fatigue, changes in sleep and appetite, and feelings of worthlessness.\nSELF-CARE TIPS\n• Regular physical activity\n• Social connection\n• Consistent sleep schedule").grid(row=1, column=0, padx=8, pady=8, sticky='nsew')
        self.card(cards, '😞', 'Loneliness', "Feeling disconnected, isolated, or unsupported even when other people are around.\nSELF-CARE TIPS\n• Reach out to someone you trust\n• Join shared activities or groups\n• Spend time around supportive people").grid(row=1, column=1, padx=8, pady=8, sticky='nsew')
        self.card(cards, '😡', 'Anger', "Strong frustration, irritability, tension, impatience, or difficulty calming down after something upsetting.\nSELF-CARE TIPS\n• Take a short break from the situation\n• Use slow breathing techniques\n• Express feelings calmly").grid(row=1, column=2, padx=8, pady=8, sticky='nsew')
        cards.grid_columnconfigure((0,1,2),weight = 1)
        cards.grid_rowconfigure((0,1),weight = 1)
        ctk.CTkLabel(main,text = "You don't have to do everything today.One small step is enough. 💪", font = ("Arial", 14),text_color= '#808080', wraplength = 250, justify = 'left').pack(pady = (18,25))

    def card(self, parent, icon, title, text):
        frame = ctk.CTkFrame(parent, corner_radius = 20, fg_color = '#FFFFFF')
        ctk.CTkLabel(frame,text = icon, font = ("Arial", 30)).pack(anchor = 'w', padx = 22, pady = (20,8))
        ctk.CTkLabel(frame,text = title, font = ("Arial", 20, 'bold'), text_color = '#2A0F23').pack(anchor = 'w', pady = (20,8))
        ctk.CTkLabel(frame,text = text, font = ("Arial", 14), text_color = '#FC7F9C', wraplength = 250, justify = 'left').pack(anchor = 'w', padx = 30, pady = (20,20))
        return frame

root = ctk.CTk()
Home(root)
root.mainloop()

        



