import tkinter as tk
import subprocess
from tkinter import scrolledtext, filedialog

class TextEditorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Bash Editor")
        self.root.geometry("800x600")  # Set a default size for the window

        self.remember_password = tk.BooleanVar(value=False)
        self.stored_password = None

        # Create a frame to hold the buttons
        button_frame = tk.Frame(root)
        button_frame.pack(fill=tk.X)

        # Create "Load" button
        load_button = tk.Button(button_frame, text="Load", command=self.load_file)
        load_button.pack(side=tk.LEFT, padx=5, pady=5)

        # Create "Save" button
        save_button = tk.Button(button_frame, text="Save", command=self.save_file)
        save_button.pack(side=tk.LEFT, padx=5, pady=5)

        # Create "Clear" button
        clear_button = tk.Button(button_frame, text="Clear", command=self.clear_editor)
        clear_button.pack(side=tk.LEFT, padx=5, pady=5)

        # Create "Run" button
        run_button = tk.Button(button_frame, text="Run", command=self.run_code)
        run_button.pack(side=tk.LEFT, padx=5, pady=5)

        # Create a PanedWindow to hold the textboxes
        self.paned_window = tk.PanedWindow(root, orient=tk.VERTICAL)
        self.paned_window.pack(fill=tk.BOTH, expand=True)

        # Create an editable multiline textbox
        self.editable_textbox = scrolledtext.ScrolledText(self.paned_window, wrap=tk.WORD)
        self.paned_window.add(self.editable_textbox)

        # Create a read-only multiline textbox
        self.readonly_textbox = scrolledtext.ScrolledText(self.paned_window, wrap=tk.WORD, state=tk.DISABLED)
        self.paned_window.add(self.readonly_textbox)

    def load_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Bash files", "*.sh")])
        if file_path:
            try:
                with open(file_path, "r") as file:
                    content = file.read()
                    self.editable_textbox.delete("1.0", tk.END)
                    self.editable_textbox.insert(tk.END, content)
            except FileNotFoundError:
                print("File not found.")

    def save_file(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".sh", filetypes=[("Bash files", "*.sh")])
        if file_path:
            content = self.editable_textbox.get("1.0", tk.END)
            with open(file_path, "w") as file:
                file.write(content)

    def run_code(self):
        code = self.editable_textbox.get("1.0", tk.END).strip()
        if not code:
            self.display_output("No code to run.")
            return

        if not code.startswith("#!"):
            code = "#!/bin/bash\n" + code
            self.editable_textbox.delete("1.0", tk.END)
            self.editable_textbox.insert(tk.END, code)

        if "sudo" in code:
            if not self.remember_password.get() or self.stored_password is None:
                self.stored_password = self.prompt_password()
            
            if self.stored_password is None:
                self.display_output("No password provided.")
                return

            if not self.verify_sudo_password():
                self.display_output("Incorrect password.")
                return

            lines = code.split('\n')
            for i, line in enumerate(lines):
                if "sudo" in line:
                    lines[i] = f'echo "{self.stored_password}" | sudo -S {line}'
            code = "\n".join(lines)

        try:
            output = subprocess.check_output(["bash", "-c", code], stderr=subprocess.STDOUT, universal_newlines=True)
        except subprocess.CalledProcessError as e:
            output = e.output

        self.display_output(output)

    def clear_editor(self):
        self.editable_textbox.delete("1.0", tk.END)

    def clear_output(self):
        self.readonly_textbox.config(state=tk.NORMAL)
        self.readonly_textbox.delete("1.0", tk.END)
        self.readonly_textbox.config(state=tk.DISABLED)

    def display_output(self, output):
        self.readonly_textbox.config(state=tk.NORMAL)
        self.readonly_textbox.delete("1.0", tk.END)
        self.readonly_textbox.insert(tk.END, output)
        self.readonly_textbox.config(state=tk.DISABLED)

    def prompt_password(self):
        password_dialog = tk.Toplevel(self.root)
        password_dialog.title("Password")

        tk.Label(password_dialog, text="Enter your password:").pack(padx=10, pady=10)

        password_entry = tk.Entry(password_dialog, show='*')
        password_entry.pack(padx=5, pady=5)

        remember_check = tk.Checkbutton(password_dialog, text="Remember password", variable=self.remember_password)
        remember_check.pack(padx=5, pady=5)

        def on_ok():
            self.stored_password = password_entry.get()
            password_dialog.destroy()

        ok_button = tk.Button(password_dialog, text="OK", command=on_ok)
        ok_button.pack(padx=10, pady=10)

        self.root.wait_window(password_dialog)
        return self.stored_password

    def verify_sudo_password(self):
        try:
            result = subprocess.run(['sudo', '-S', 'echo', 'test'], input=self.stored_password + '\n',
                                    stderr=subprocess.PIPE, stdout=subprocess.PIPE, universal_newlines=True)
            return result.returncode == 0
        except Exception:
            return False

if __name__ == "__main__":
    root = tk.Tk()
    app = TextEditorApp(root)
    root.mainloop()
