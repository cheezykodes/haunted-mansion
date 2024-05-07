import tkinter as tk
from tkinter import messagebox
import json
import os
#from hanted_mansion_book import book

import json

with open(os.path.join(os.getcwd(), 'hanted_mansion.json'), 'r') as file:
    json_data = json.load(file)

book = json.loads(json_data)

DEBUG = False

class InteractiveBookGUI:
    def __init__(self):
        # Initialize the main window
        self.root = tk.Tk()
        self.root.title("Interactive Book App")
        self.root.geometry("800x300")

        self.data = book
        self.curr_anchor = book['start_anchor']
        self.valid_user_input = []
        self.post_node_texts = []
        self.next_anchors = []
        self.user_input = None
        self.next_anchor = None


        # Create GUI elements for introduction view -----------------------------------------------------------
        self.intro_frame = tk.Frame(self.root)
        self.intro_frame.pack(pady=10)

        self.intro_label = tk.Label(self.intro_frame, text="Welcome to the Interactive Book App!\nThis time: \"Haunted Mansion!\"\n\n")
        self.intro_label.pack()

        self.start_button = tk.Button(self.intro_frame, text="Start Reading", command=self.show_node)
        self.start_button.pack(side='bottom', pady=12)

        # Create GUI elements for node view -----------------------------------------------------------
        self.node_frame = tk.Frame(self.root)
        self.node_frame.pack(pady=10)

        self.node_text = tk.Text(self.node_frame, wrap='word', height=12)
        self.node_text.pack(expand=True, fill='both')

        self.user_input_frame = tk.Frame(self.node_frame)
        self.user_input_frame.pack(side='bottom', pady=5)

        self.answer_entry = tk.Entry(self.user_input_frame)
        self.answer_entry.pack(side=tk.LEFT)

        self.send_button = tk.Button(self.user_input_frame, text="Next", command=self.check_answer)
        self.send_button.pack(side=tk.RIGHT)


        # Create GUI elements for post-node view -----------------------------------------------------------
        self.post_node_frame = tk.Frame(self.root)
        self.post_node_frame.pack(pady=10)

        self.post_node_text = tk.Text(self.post_node_frame, wrap='word', height=12)
        self.post_node_text.pack(expand=True, fill='both')

        self.next_button = tk.Button(self.post_node_frame, text="Continue", command=self.do_continue)
        self.next_button.pack()

        # Create GUI elements for end view -----------------------------------------------------------
        self.end_frame = tk.Frame(self.root)
        self.end_frame.pack(pady=10)

        self.end_label = tk.Label(self.end_frame, text="The End")
        self.end_label.pack()

        self.quit_button = tk.Button(self.end_frame, text="Quit", command=self.root.quit)
        self.quit_button.pack()
        # ---------------------------------------------------------------------------------------------

        self.node_frame.pack_forget()
        self.end_frame.pack_forget()
        self.post_node_frame.pack_forget()
        self.intro_frame.pack()

        self.root.mainloop()

    def show_node(self):
        self.end_frame.pack_forget()
        self.post_node_frame.pack_forget()
        self.intro_frame.pack_forget() # Hide the intro frame
        self.node_frame.pack() # Display the node frame

        # Get the intro text for the current node
        intro_text = self.data['content'][self.curr_anchor]['intro']
        if DEBUG:
            print(f'Node Intro: {intro_text}')

        self.node_text.delete('1.0', 'end')
        self.node_text.insert('1.0', intro_text + '\n')
        # Inset the options
        self.node_text.insert('end', f"\n")
        if self.data['content'][self.curr_anchor]['question']:
            self.node_text.insert('end', f"{self.data['content'][self.curr_anchor]['question']}\n\n")
        self.valid_user_input, self.post_node_texts, self.next_anchors = [], [], []
        self.user_input, self.next_anchor = None, None
        #  (1, '(1) Yes, I open the door', 'You enter the living room', 'turn2.1'), # user input, option, respond, link
        for idx, option, next_text, next_anchor in self.data['content'][self.curr_anchor]['answer']:
            self.valid_user_input.append(str(idx))
            self.post_node_texts.append(next_text)
            self.next_anchors.append(next_anchor)
            self.node_text.insert('end', f"{option}\n")

        # self.options_list = tk.Listbox(self.node_frame, height=3)
        self.answer_entry.focus()

        self.node_text.pack(expand=False, fill='both', side='top', padx=20, pady=20) # Adjust size of Text widget

    def do_continue(self):
        self.curr_anchor = self.next_anchor

        if DEBUG:
            print(f"self.curr_anchor: {self.curr_anchor}")
        if len(self.next_anchors):
            self.show_node()
        else:
            self.the_end()

    def show_answer(self, text: str):
        # Display the current question
        self.end_frame.pack_forget()
        self.intro_frame.pack_forget() # Hide the intro frame
        self.node_frame.pack_forget() # Display the node frame
        self.post_node_frame.pack()

        if DEBUG:
            print(f'Post-Node Intro: {text}')

        self.post_node_text.delete('1.0', 'end')
        self.post_node_text.insert('end', text + '\n')


    def check_answer(self):
        # Check the answer provided by the user
        answer = self.answer_entry.get().lower()

        if DEBUG:
            print('answer in self.valid_user_input', answer in self.valid_user_input)
            print(f'Next anchor: {self.next_anchor}')

        if len(self.valid_user_input) == 0:
            self.the_end()

        if not answer:
            return

        if answer in self.valid_user_input:
            self.next_anchor = self.next_anchors[self.valid_user_input.index(answer)]
            self.user_input = answer
            text =self.post_node_texts[self.valid_user_input.index(answer)]
            self.answer_entry.delete(0, tk.END)
            self.show_answer(text)
        return

    def the_end(self):
        messagebox.showinfo("This is it!", f"THE END!")
        self.root.destroy()


if __name__ == "__main__":
    book = InteractiveBookGUI()