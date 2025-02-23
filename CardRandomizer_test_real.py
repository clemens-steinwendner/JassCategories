import random
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
import numpy as np
import tkinter as tk
from tkinter import simpledialog, messagebox
import os
from github_sync import GitHubSync

#config:

allowed_categories = ["Ei", "Ro", "Se", "Si", "Oa", "Uu", "Soa", "Suu", "Sch"]

name_cat = ["Eichle", "Rose", "Schelle", "Schilte", "Obe abe", "Une ufe", "Slalom obe abe", "Slalom une ufe", "Schiebe!"]

# GitHub configuration
GITHUB_TOKEN = None  # Will be prompted
GITHUB_REPO = "JassCategories"  # Just the repository name without username

#tkinter init:

class CategorizationApp:
    def __init__(self, master):
        self.master = master
        master.title("Jass Trump Kategorisierung")

        # Get GitHub token and username if not set
        global GITHUB_TOKEN
        if not GITHUB_TOKEN:
            token = simpledialog.askstring("GitHub Setup", "Please enter your GitHub token:", parent=master)
            if not token:
                messagebox.showerror("Error", "GitHub token is required!")
                master.destroy()
                return
            GITHUB_TOKEN = token
        
        self.username = simpledialog.askstring("Username", "Please enter your username:", parent=master)
        if not self.username:
            messagebox.showerror("Error", "Username is required!")
            master.destroy()
            return

        # Initialize GitHub sync
        try:
            self.github_sync = GitHubSync(GITHUB_TOKEN, GITHUB_REPO)
        except Exception as e:
            messagebox.showerror("GitHub Error", f"Failed to initialize GitHub: {str(e)}")
            master.destroy()
            return

        self.counter = 0

        self.counter_label = tk.Label(master, text = f"Images analyzed: {self.counter}", font = ("Arial", 20))
        self.counter_label.pack()

        self.reward_label = tk.Label(master, text = "", font = ("Comic Sans MS", 30))
        self.reward_label.pack()

        self.fig = plt.Figure(figsize=(9, 3))
        self.axes = self.fig.subplots(1, 9)

        self.canvas = FigureCanvasTkAgg(self.fig, master = master)
        self.canvas.get_tk_widget().pack(side = tk.TOP, fill = tk.BOTH, expand = True)

        self.buttons_frame = tk.Frame(master)
        self.buttons_frame.pack(pady=10)

        for i, cat in enumerate(allowed_categories):
            btn = tk.Button(self.buttons_frame, text=name_cat[i],
                            command=lambda cat=cat: self.process_category(cat),
                            font=("Arial", 12))
            btn.pack(side=tk.LEFT, padx=5)

        self.label = tk.Label(master, 
                              text = "Enter Category:",
                              font = ("Arial", 14))
        self.label.pack(pady = (10,0))

        self.entry = tk.Entry(master, font=("Arial", 14))
        self.entry.pack(fill=tk.X, padx = 10, pady = 5)
        self.entry.focus_set()
        self.entry.bind('<Return>', lambda event: self.process_input())

        self.submit_button = tk.Button(master, text = "Submit", command = self.process_input, font = ("Arial", 14))
        self.submit_button.pack(pady=(0, 10))


        self.cards = []
        self.update_images()



# get 9 random numbers/cards: 
# image display:



#user input / ansagen

    def update_images(self):
        

        if self.counter == 10:
            self.reward_label.config(text = "Good job, you labeled 10 Trümpfe, now work harder!!!!")
        elif self.counter == 20:
            self.reward_label.config(text = "FASTER FASTER FASTER")
        elif self.counter == 50:
            self.reward_label.config(text = "Alright, looks like you could become the skibid labeller...")
        elif self.counter == 100:
            self.reward_label.config(text = "100... They talked about you in the prophecies...")
        elif self.counter >= 200:
            self.reward_label.config(text = "You're him... You're the legendary skibidi sigma labeller")
        else:
            self.reward_label.config(text = "")

        #Display images first
        self.cards = random.sample(range(0,36), 9)
        self.cards.sort()


        for ax in self.axes:
            ax.clear()
            ax.axis("off")


        #fig, axes = plt.subplots(1, len(cards), figsize=(len(cards)*3, 3))

        for ax, ind in zip(self.axes, self.cards):
            try:
                img = mpimg.imread(f'images3/img_{ind}.jpg')
                ax.imshow(img)
            except FileNotFoundError:
                ax.text(0.5, 0.5, f"Missing image {ind}")                
                continue

        self.canvas.draw()

        #fig.canvas.manager.set_window_title('Deine Hand:')
        #plt.tight_layout()
        #plt.show()

    # Next Step: get user input

    def process_category(self, category):
        """
        Write the current set of card indices and the category
        to GitHub and update the images.
        """
        try:
            self.github_sync.add_categorization(self.cards, category, self.username)
            print("Data cached for GitHub sync")
        except Exception as e:
            messagebox.showerror("Error saving data", str(e))
            return

        self.counter += 1
        self.counter_label.config(text = f"Images analyzed: {self.counter}")
        
        # Clear the entry and update images for the next round.
        self.entry.delete(0, tk.END)
        self.update_images()

    def process_input(self):
        user_input = self.entry.get().strip()

        if user_input is None:
            print("You dummy baka, input something")
            return

        if user_input.lower() == "skip":
            self.entry.delete(0, tk.END)
            self.update_images()
            return

        if user_input not in allowed_categories:
            messagebox.showerror(
                "Invalid Input",
                "Enter a valid category"
            )
            return
        
        try:
            self.github_sync.add_categorization(self.cards, user_input, self.username)
            print("Data cached for GitHub sync")
        except Exception as e:
            messagebox.showerror("Error saving data", str(e))
            return

        self.counter += 1
        self.counter_label.config(text = f"Images analyzed: {self.counter}")
        
        self.entry.delete(0, tk.END)
        self.update_images()

    def on_closing(self):
        """Handle window closing - force sync any remaining data"""
        try:
            if hasattr(self, 'github_sync'):
                self.github_sync.force_sync()
        finally:
            self.master.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = CategorizationApp(root)
    if hasattr(app, 'github_sync'):  # Only set up closing handler if GitHub sync was initialized
        root.protocol("WM_DELETE_WINDOW", app.on_closing)  # Handle window closing
    root.mainloop()
    