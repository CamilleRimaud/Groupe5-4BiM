import tkinter as tk
import tkinter.messagebox
from tkinter import *
from PIL import Image, ImageTk
import os
import random
import json

class RobotPortrait:
    def __init__(self, root):
        self.root = root
        self.root.title("Robot Portrait Generator")
        self.root.configure(bg="#eefbfb")

        # To keep user's choices
        self.selected_features = []
        self.selected_portraits = []
        self.current_portraits = []
        self.history = []  #if we want to come back

        # Save test portraits
        self.image_folder = "images"
        self.all_images = [f for f in os.listdir(self.image_folder) if f.endswith(".jpg")] #plutôt flou comme fonction j'avoue ^^'

        self.create_widgets()

    def create_widgets(self):
        # Title with instruction
        self.label_instruction = tk.Label(self.root, text="Choose the 4 most look-alike portraits by clinking on it.", font=("Baskerville", 12), bg="#eefbfb", fg="#722f37")
        self.label_instruction.pack(pady=10)

        # Elements choosen by the user
        self.frame_choices = tk.Frame(self.root, bg="#eefbfb")
        self.frame_choices.pack()

        self.choices = ["Cheveux courts", "Cheveux longs", "Barbe", "Lunettes", "Sourcils épais", "Visage rond"]	#simple liste test
        self.check_vars = {choices: tk.IntVar() for choices in self.choices}   #plutôt flou

        for choices in self.choices:
            chk = tk.Checkbutton(self.frame_choices, text=choices, variable=self.check_vars[choices], bg="#f0f0f5")
            chk.pack(side=tk.LEFT, padx=5)

        # Generator button
        self.btn_gen = tk.Button(self.root, text="Generate !", command=self.generate_portraits, bg="#26619c", fg="#faebd7", font=("Baskerville", 10, "bold"))
        self.btn_gen.pack(pady=10)

        # Portraits zone
        self.frame_portraits = tk.Frame(self.root, bg="#eefbfb")
        self.frame_portraits.pack()

        # Best choice zone
        self.label_selected = tk.Label(self.root, text="Portrait le plus proche :", font=("Arial", 12), bg="#eefbfb", fg="#722f37")
        self.label_selected.pack()
        
        self.canvas_selected = tk.Canvas(self.root, width=128, height=128, bg="#d9f6f6")
        self.canvas_selected.pack(pady=10)

        # Buttons to move on
        self.frame_btn = tk.Frame(self.root, bg="#f0f0f0")
        self.frame_btn.pack(pady=10)
        
        self.btn_back = tk.Button(self.frame_btn, text="Return looooser !", command=self.previous_step, state=tk.DISABLED, bg="#623a00", fg="white", font=("Baskerville", 10, "bold"))
        self.btn_back.pack(side=tk.LEFT, padx=10)
        
        self.btn_next = tk.Button(self.frame_btn, text="Thank you, Next !", command=self.next_step, state=tk.DISABLED, bg="#401740", fg="white", font=("Baskerville", 10, "bold"))
        self.btn_next.pack(side=tk.RIGHT, padx=10)

    def generate_portraits(self):
        " Generate 12 portraits "
        self.selected_features = [feature for feature, var in self.check_vars.items() if var.get()]
        if not self.selected_features:
            tk.messagebox.showwarning(title="Warning !!", message="Choose at least 1 feature.")
            return

        #Save choices in a file
        self.save_choices()

        # Stock
        self.history.append(self.current_portraits.copy())
        self.selected_portraits = []

        # Delete old portraits
        for widget in self.frame_portraits.winfo_children():
            widget.destroy()

        # random selection
        self.current_portraits = random.sample(self.all_images, min(12, len(self.all_images)))
        self.portrait_buttons = []

        for i, img_name in enumerate(self.current_portraits):
            img_path = os.path.join(self.image_folder, img_name)
            img = Image.open(img_path).resize((128, 128))
            img_tk = ImageTk.PhotoImage(img)

            btn = tk.Button(self.frame_portraits, image=img_tk, command=lambda p=img_name: self.select_portrait(p))
            btn.image = img_tk
            btn.grid(row=i // 4, column=i % 4, padx=5, pady=5)
            self.portrait_buttons.append(btn)

    def select_portrait(self, portrait):
        if len(self.selected_portraits) < 4:
            self.selected_portraits.append(portrait)
        if len(self.selected_portraits) == 4:
            self.btn_next.config(state=tk.NORMAL)
        print(f"Selected portraits: {len(self.selected_portraits)}")  # Debugging line
        if len(self.selected_portraits) > 4:
            messagebox.showwarning("Warning !!", "You have to only select 4 portraits.")
            return

        # 1st portrait chosen is the best one
        img_path = os.path.join(self.image_folder, self.selected_portraits[0])
        img = Image.open(img_path).resize((128, 128))
        img_tk = ImageTk.PhotoImage(img)
        self.canvas_selected.create_image(128, 128, image=img_tk)
        self.canvas_selected.image = img_tk

    def next_step(self):
        "Next step with 12 new portraits"

        self.history.append(self.selected_portraits.copy())
        self.selected_portraits = []
        self.btn_next.config(state=tk.DISABLED)
        self.btn_back.config(state=tk.NORMAL)
        self.generate_portraits()

    def previous_step(self):
        "Return step"
        if self.history:
            self.current_portraits = self.history.pop()
            self.generate_portraits()
        if not self.history:
            self.btn_back.config(state=tk.DISABLED)

    def save_choices(self):   #in a json file
        with open('user_choices.json', 'w') as file:
            json.dump(self.selected_features, file)
        print("Choices saved")
        
    def load_choices(self):    #from a json file
        if os.path.exists('user_choices.json'):
            with open('user_choices.json', 'r') as file:
                self.selected_features = json.load(file)
            print("Choices loaded")
        else:
            print("No such file found")

if __name__ == "__main__":
    root = tk.Tk()
    app = RobotPortrait(root)
    root.mainloop()

