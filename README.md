# Bash Editor

Bash Editor is a simple graphical user interface application written in Python using Tkinter. It allows users to load, edit, save, and run Bash scripts. The main purpose of this application is to provide an easy way to run multiple terminal commands as a Bash file without having to save it as a file. Bash Editor also supports handling `sudo` commands by prompting the user for a password.

## Features

- **Load and Save Files:** Load existing Bash scripts and save your edits.
- **Clear Editor:** Clear the current content of the editor.
- **Run Scripts:** Execute Bash scripts directly from the editor.
- **Resizable Layout:** Adjust the height of the editor and output textboxes by dragging the border between them.
- **Sudo Password Handling:** Prompt for a password when running scripts with `sudo`.

## Requirements

- Python 3.x
- Tkinter (usually included with Python installations)
- `subprocess` module (standard library)

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/bash-editor.git
    cd bash-editor
    ```
2. Run the application:
    ```bash
    python main.py
    ```

## Usage

1. **Load a Script:** Click the "Load" button to open a file dialog and select a Bash script to load into the editor.
2. **Edit the Script:** Make changes directly in the editable textbox.
3. **Save the Script:** Click the "Save" button to open a file dialog and save your changes to a file.
4. **Clear the Editor:** Click the "Clear" button to remove all content from the editor.
5. **Run the Script:** Click the "Run" button to execute the script. Output will be displayed in the bottom textbox. If the script contains `sudo` commands, you will be prompted for a password once. It is not necessary to save the script before running it.


## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
