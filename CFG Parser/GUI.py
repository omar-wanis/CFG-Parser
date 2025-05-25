import customtkinter as ctk
from CFGParser import CFG
from tkinter import messagebox
from time import time

class CFGParserGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("CFG Parser (using DFS & BFS)")
        self.create_widgets()
        # self.root.iconbitmap("vi.jpg")

    def create_widgets(self):
        self.grammar_label = ctk.CTkLabel(self.root, text="Enter your Grammer Rules: (ex: S -> 0S1 | 0S0 | 0 | 1)")
        self.grammar_label.pack(pady=(20, 10), anchor="w")

        self.grammar_text = ctk.CTkTextbox(self.root, width=500, height=100)
        self.grammar_text.pack(padx=20, pady=10)

        button_frame = ctk.CTkFrame(self.root)
        button_frame.pack(pady=10)
        self.epsilon_button = ctk.CTkButton(button_frame, text="Insert ε", command=self.insert_epsilon)
        self.epsilon_button.pack(side="left", padx=5)
        self.finish_button = ctk.CTkButton(button_frame, text="Finish Grammar Entry", command=self.finish_grammar)
        self.finish_button.pack(side="left", padx=5)

        self.string_label = ctk.CTkLabel(self.root, text="String to parse:")
        self.string_label.pack(pady=10)

        self.string_entry = ctk.CTkEntry(self.root, width=300)
        self.string_entry.pack()

        self.output_text = ctk.CTkTextbox(self.root, width=500, height=200, state="disabled")
        self.output_text.pack(pady=10)

        self.parse_button_DFS = ctk.CTkButton(self.root, text="Parse String with DFS", corner_radius=25, fg_color="transparent", border_color="#0A1631", border_width=2, command=self.parse_stringDFS, state="disabled")
        self.parse_button_DFS.pack(pady=10)
        self.parse_button_BFS = ctk.CTkButton(self.root, text="Parse String with BFS", corner_radius=25, fg_color="transparent", border_color="#0A1631", border_width=2, command=self.parse_stringBFS, state="disabled")
        self.parse_button_BFS.pack(pady=10)

    def finish_grammar(self):
        self.output_text.configure(state="normal")
        self.output_text.delete("1.0", "end")
        
        # Prepare the grammar from the input text
        lines = self.grammar_text.get("1.0", "end").strip().split('\n')
        has_rules = False
        
        # Initialize CFG object
        # self.parser = CFG(terminals={'0', '1', 'λ'}, start_variable='S')
        rules = {}
        Terminals = []
        NullChar = ""
        for line in lines:
            rule_input = line.strip()
            if not rule_input:
                continue
            if '->' not in rule_input:
                self.output_text.insert("end", "❗ Invalid rule format: " + rule_input + "\n")
                continue
            left, right = rule_input.split("->")
            left = left.strip()
            right = right.strip()
            print(f"left : {left} & right : {right}")
            if not left or not right:
                self.output_text.insert("end", "❗ Both sides must not be empty: " + rule_input + "\n")
                continue
            if not left.isupper():
                self.output_text.insert("end", "❗ Left side must be uppercase: " + rule_input + "\n")
                continue
            
            # Add productions to the grammar
            productions = [prod.strip() for prod in right.split('|')]
            print(f"Productions : {productions}")
            if not all(productions):
                self.output_text.insert("end", "❗ All productions must be non-empty: " + rule_input + "\n")
                continue
            rules[left] = productions
            print(f"rule[{left}] : {rules[left]}")
            for prod in productions:
                try:
                    # Add each rule to the CFG object
                    has_rules = True
                    for c in prod:
                        if c.islower() or c in ['λ', 'ε']:
                            NullChar = c
                            Terminals.append(c)
            
                except Exception as e:
                    self.output_text.insert("end", "❗ Error: " + str(e) + "\n")
        
        if not has_rules:
            self.output_text.insert("end", "❗ Please enter at least one valid rule.\n")
            self.parse_button.configure(state="disabled")
            self.grammar_finished = False
            return
        self.parser = CFG(terminals=Terminals,rules=rules,null_character=NullChar)
        # Validate the CFG grammar
        self.output_text.insert("end", "Grammar entry complete.\n")
        self.grammar_finished = True
        # self.output_text.configure(state="disabled")
        self.parse_button_DFS.configure(state="normal")
        self.parse_button_BFS.configure(state="normal")



    def parse_stringBFS(self):
        if not self.grammar_finished:
            messagebox.showwarning("Grammar not finished", "Please finish grammar entry first.")
            return
        target = self.string_entry.get().strip()
        self.output_text.configure(state="normal")
        self.output_text.delete("1.0", "end")

        if not target:
            self.output_text.insert("end", "❗ Please enter a non-empty string.\n")
            self.output_text.configure(state="disabled")
            return

        try:
            self.parser.rules(None)
            start = time()
            result, node = self.parser.BFS(target)
            end = time()
            if result:
                self.output_text.insert("end", f"✅ The string '{target}' is accepted by the grammar.\n\nDerivation Path:\n")
                self.output_text.insert("end", self.parser.Derivation_Path(node))
                self.output_text.insert("end", f"\nTime took with BFS : {end-start}")
            else:
                self.output_text.insert("end", f"❌ The string '{target}' is NOT accepted by the grammar.\n")
        except Exception as e:
            self.output_text.insert("end", f"❗ Error during parsing: {str(e)}\n")

        self.output_text.configure(state="disabled")
    
    def parse_stringDFS(self):
        if not self.grammar_finished:
            messagebox.showwarning("Grammar not finished", "Please finish grammar entry first.")
            return
        target = self.string_entry.get().strip()
        self.output_text.configure(state="normal")
        self.output_text.delete("1.0", "end")

        if not target:
            self.output_text.insert("end", "❗ Please enter a non-empty string.\n")
            self.output_text.configure(state="disabled")
            return

        try:
            self.parser.rules(None)
            start = time()
            result, node = self.parser.DFS(target,None,self.parser._start_variable)
            end = time()
            if result:
                self.output_text.insert("end", f"✅ The string '{target}' is accepted by the grammar.\n\nDerivation Path:\n")
                self.output_text.insert("end", self.parser.Derivation_Path(node))
                self.output_text.insert("end", f"\nTime took with DFS : {end-start}")
                
            else:
                self.output_text.insert("end", f"❌ The string '{target}' is NOT accepted by the grammar.\n")
        except Exception as e:
            self.output_text.insert("end", f"❗ Error during parsing: {str(e)}\n")

        self.output_text.configure(state="disabled")

    def insert_epsilon(self):
        self.grammar_text.insert("insert", "ε")

def boom():
    ctk.set_appearance_mode("system")
    ctk.set_default_color_theme("dark-blue")
    root = ctk.CTk()
    root.geometry("500x650")
    root.resizable(False, False)
    app = CFGParserGUI(root)
    root.mainloop()

boom()
