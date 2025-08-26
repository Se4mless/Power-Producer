import os
import sys
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox, font

import winshell  # pip install pywin32 or winshell

start_dir = os.path.dirname(os.path.abspath(__file__))  # script folder

APP_NAME = "PDCR"
TARGET_DIR = os.path.expandvars(r"%LOCALAPPDATA%\Programs\PDCR")  # global per-user folder

def install(selected_path=None):
    """Install PDCR to a safe folder and copy all resources"""
    pdcr_src = os.path.join(start_dir, APP_NAME)

    # Destination folder: either user selected or default
    dest_folder = selected_path if selected_path else TARGET_DIR
    os.makedirs(dest_folder, exist_ok=True)

    # Copy PDCR folder
    pdcr_dest = os.path.join(dest_folder, APP_NAME)
    if os.path.exists(pdcr_dest):
        shutil.rmtree(pdcr_dest)
    shutil.copytree(pdcr_src, pdcr_dest)

    # Copy the running exe/script
    exe_path = getattr(sys, 'frozen', False) and sys.executable or sys.argv[0]
    shutil.copy2(exe_path, os.path.join(dest_folder, os.path.basename(exe_path)))

    # Create a Start Menu shortcut
    shortcut_path = os.path.join(winshell.start_menu(), f"{APP_NAME}.lnk")
    with winshell.shortcut(shortcut_path) as link:
        link.path = os.path.join(dest_folder, os.path.basename(exe_path))
        link.working_directory = dest_folder

class InstallerWizard(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(f"{APP_NAME} Setup Wizard")
        self.geometry("450x250")
        self.configure(bg="#f0f0f0")
        self.steps = [self.step_welcome, self.step_options, self.step_install]
        self.current_step = 0
        self.heading_font = font.Font(family="Arial", size=16, weight="bold")
        self.content_frame = tk.Frame(self, bg="#f0f0f0")
        self.content_frame.pack(expand=True, fill="both", padx=20, pady=20)
        self.button_frame = tk.Frame(self, bg="#f0f0f0")
        self.button_frame.pack(fill="x", pady=(0,10))
        self.selected_folder_var = tk.StringVar(value="")
        self.show_step()

    def show_step(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        for widget in self.button_frame.winfo_children():
            widget.destroy()
        self.steps[self.current_step]()

    def step_welcome(self):
        tk.Label(self.content_frame, text=f"Welcome to {APP_NAME} Installer", font=self.heading_font, bg="#f0f0f0").pack(pady=30)
        tk.Label(self.content_frame, text="This wizard will guide you through installation.", bg="#f0f0f0").pack(pady=10)
        tk.Button(self.button_frame, text="Next", width=10, command=self.next_step, bg="#4CAF50", fg="white").pack(side="right", padx=10)

    def step_options(self):
        tk.Label(self.content_frame, text="Step 2: Choose Installation Folder", font=self.heading_font, bg="#f0f0f0").pack(pady=20)

        folder_frame = tk.Frame(self.content_frame, bg="#f0f0f0")
        folder_frame.pack(pady=(10,5), fill="x")

        folder_entry = tk.Entry(folder_frame, textvariable=self.selected_folder_var, state="readonly", width=50, readonlybackground="white")
        folder_entry.pack(side="left", padx=(0,5), expand=True, fill="x")

        tk.Button(folder_frame, text="Select Folder", command=self.select_folder, bg="#2196F3", fg="white").pack(side="right")
        tk.Button(self.button_frame, text="Back", width=10, command=self.prev_step, bg="#f44336", fg="white").pack(side="left", padx=10)
        tk.Button(self.button_frame, text="Next", width=10, command=self.next_step, bg="#4CAF50", fg="white").pack(side="right", padx=10)

    def select_folder(self):
        folder_path = filedialog.askdirectory(title="Select a folder", initialdir=os.path.expanduser("~"))
        if folder_path:
            self.selected_folder_var.set(folder_path)

    def step_install(self):
        tk.Label(self.content_frame, text="Ready to Install", font=self.heading_font, bg="#f0f0f0").pack(pady=20)
        tk.Label(self.content_frame, text="Click Install to complete the setup.", bg="#f0f0f0").pack(pady=10)
        tk.Button(self.button_frame, text="Back", width=10, command=self.prev_step, bg="#f44336", fg="white").pack(side="left", padx=10)
        tk.Button(self.button_frame, text="Install", width=10, command=self.run_install, bg="#4CAF50", fg="white").pack(side="right", padx=10)

    def next_step(self):
        if self.current_step < len(self.steps) - 1:
            self.current_step += 1
            self.show_step()

    def prev_step(self):
        if self.current_step > 0:
            self.current_step -= 1
            self.show_step()

    def run_install(self):
        install(self.selected_folder_var.get() or TARGET_DIR)
        messagebox.showinfo("Installer", f"{APP_NAME} installation complete!\nYou can launch it from Start Menu.")
        self.destroy()

if __name__ == "__main__":
    app = InstallerWizard()
    app.mainloop()
