import tkinter as tk
import tkinter.messagebox
from tkinter import *
from PIL import Image, ImageTk
import os
import random
import json
import subprocess

class RobotPortrait:
    def __init__(self, root):
        self.root = root
        self.root.title("Robot Portrait Generator")
        #self.root.geometry("2000x1000")
        self.root.configure(bg="#eefbfb")

        # To keep user's choices
        self.selected_features = []
        self.selected_portraits = []
        self.current_portraits = []
        self.history = []  #if we want to come back

        # Save test portraits
        self.image_folder = "data_sample"
        self.all_images = [f for f in os.listdir(self.image_folder) if f.endswith(".jpg")]

        # Scrollbar
        self.canvas = tk.Canvas(self.root, bg="#eefbfb")

        self.scrollbar = tk.Scrollbar(self.root, orient=VERTICAL, command=self.canvas.yview)
        self.scrollbar.pack(side=RIGHT, fill=Y)
        self.canvas.config(yscrollcommand=self.scrollbar.set)

        self.scrollable_frame = tk.Frame(self.canvas, bg="#eefbfb")
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        self.scrollable_frame.bind(
            "<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        self.create_widgets()

    def create_widgets(self):
        # create all widgets
        self.main_page_widg()
    
    def main_page_widg(self):
        self.title_label = tk.Label(self.root, text="Welcome to your Robot Portrait Generator", font=("Baskerville", 24), bg="#eefbfb", fg="#722f37")
        self.title_label.pack(pady=20)

        self.start_button = tk.Button(self.root, text="Start", command=self.portrait_generator, font=("Baskerville", 15))
        self.start_button.pack(pady=20)
        
    def portrait_generator(self):
        # Remove home page widgets
        self.title_label.pack_forget()
        self.start_button.pack_forget()
        
        # Title with instruction
        self.label_instruction = tk.Label(self.root, text="Choose the 4 most look-alike portraits by clinking on it.", font=("Baskerville", 12), bg="#eefbfb", fg="#722f37")
        self.label_instruction.pack(pady=10)

        # Elements choosen by the user
        self.frame_choices = tk.Frame(self.root, bg="#eefbfb")
        self.frame_choices.pack()

        self.choices = ["Male", "Pale-skin", "Eyeglasses", "Gray Hair", "Blond Hair", "Black Hair", "Brown Hair", "Bald", "Straight Hair", "Wavy Hair", "No Beard", "Mustache", "Goatee"]	#simple liste test
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
        self.label_selected = tk.Label(self.root, text="More accurate portrait :", font=("Arial", 12), bg="#eefbfb", fg="#722f37")
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
        
        self.frame_right = tk.Frame(self.root, bg="#eefbfb")  # New frame for right alignment
        self.frame_right.pack(side=tk.RIGHT, padx=20)

        self.btn_final_choice = tk.Button(self.frame_right, text="My Final Choice", command=self.final_choice, state=tk.DISABLED, bg="#0F0616", fg="white", font=("Baskerville", 10, "bold"))
        self.btn_final_choice.pack(side=tk.RIGHT, padx=10)

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
            
        try:
            result = subprocess.run(["python3", "firstGen.py", "user_choices.json"], capture_output=True, text=True)

            if result.returncode != 0:
                print (f"Error while generating images. stderr: {result.stderr}")
                tk.messagebox.showerror("Error", f"Error while generating images: {result.stderr}")
                return
        
            print(result.stdout)
            
            image_names = result.stdout.strip()[1:-1].split(", ")
            
            image_paths = [f"{img_name.strip()[1:-1]}" for img_name in image_names]
            
            print(image_paths)
            
            self.display_images(image_paths)
        
        except Exception as e:
            print(f"An exception occurred: {e}")
            tk.messagebox.showerror("Exception", f"An error occurred: {e}")
        
        finally:
            
            pass

    def display_images(self, image_paths):
        for widget in self.frame_portraits.winfo_children():
            widget.destroy()
        
            self.portrait_buttons = []

        for i, img_name in enumerate(image_paths):
            img = Image.open(os.path.join(self.image_folder, img_name)).resize((128, 128))
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
        if len(self.selected_portraits) == 1:
            self.btn_final_choice.config(state=tk.NORMAL)

        # 1st portrait chosen is the best one
        img_path = os.path.join(self.image_folder, self.selected_portraits[0])
        img = Image.open(img_path)
        img_resized=img.resize((128,128))
        img_tk = ImageTk.PhotoImage(img_resized)
        self.canvas_selected.create_image(64, 64, image=img_tk)
        self.canvas_selected.image = img_tk

    def final_choice(self):
        self.history.append(self.selected_portraits.copy())
        
        for widget in self.root.winfo_children():
            widget.destroy()
            
        final_message=tk.Label(self.root, text="Your final chosen portrait!", font=("Baskerville", 24), bg="#eefbfb", fg="#722f37")
        final_message.pack(pady=20)
        
        final_portrait_path = os.path.join(self.image_folder, self.selected_portraits[0])
        img = Image.open(final_portrait_path).resize((300, 300))
        img_tk = ImageTk.PhotoImage(img)

        final_portrait_label = tk.Label(self.root, image=img_tk)
        final_portrait_label.image = img_tk
        final_portrait_label.pack(pady=20)

        ending_message = tk.Label(self.root, text="Thank you for using the Robot Portrait Generator!", font=("Baskerville", 18), bg="#eefbfb", fg="#722f37")
        ending_message.pack(pady=10)

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

