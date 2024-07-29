import os
import subprocess
import tkinter as tk
from tkinter import filedialog, messagebox, font

def create_csproj_file(base_directory, output_directory, module_file, protections_preset):
    csproj_content = f"""<?xml version="1.0" encoding="utf-8" ?>
<Project>
  <BaseDirectory>{base_directory}</BaseDirectory>
  <OutputDirectory>{output_directory}</OutputDirectory>
  <Modules>
    <Module file="{module_file}" />
  </Modules>
  <Protections>
    <preset>{protections_preset}</preset>
  </Protections>
</Project>
"""
    project_file_path = os.path.join(output_directory, 'project.csproj')
    with open(project_file_path, 'w') as file:
        file.write(csproj_content)
    return project_file_path

def open_csproj_config_window():
    config_window = tk.Toplevel(root)
    config_window.title("Config .csproj")
    config_window.geometry("450x350")
    config_window.configure(bg="black")

    def browse_base_directory():
        directory = filedialog.askdirectory()
        base_directory_entry.delete(0, tk.END)
        base_directory_entry.insert(0, directory)

    def browse_output_directory():
        directory = filedialog.askdirectory()
        output_directory_entry.delete(0, tk.END)
        output_directory_entry.insert(0, directory)

    def browse_module_file():
        file = filedialog.askopenfilename(filetypes=[("DLL Files", "*.dll")])
        module_file_entry.delete(0, tk.END)
        module_file_entry.insert(0, file)

    tk.Label(config_window, text="Base Directory:", fg="red", bg="black", font=label_font).pack(padx=10, pady=5, anchor="w")
    base_directory_frame = tk.Frame(config_window, bg="black")
    base_directory_frame.pack(padx=10, pady=5, fill="x")
    base_directory_entry = tk.Entry(base_directory_frame, width=30, bg="white", fg="black", font=entry_font)
    base_directory_entry.pack(side="left", fill="x", expand=True)
    tk.Button(base_directory_frame, text="Browse", command=browse_base_directory, bg="white", fg="black", font=button_font).pack(side="right")

    tk.Label(config_window, text="Output Directory:", fg="red", bg="black", font=label_font).pack(padx=10, pady=5, anchor="w")
    output_directory_frame = tk.Frame(config_window, bg="black")
    output_directory_frame.pack(padx=10, pady=5, fill="x")
    output_directory_entry = tk.Entry(output_directory_frame, width=30, bg="white", fg="black", font=entry_font)
    output_directory_entry.pack(side="left", fill="x", expand=True)
    tk.Button(output_directory_frame, text="Browse", command=browse_output_directory, bg="white", fg="black", font=button_font).pack(side="right")

    tk.Label(config_window, text="Module File:", fg="red", bg="black", font=label_font).pack(padx=10, pady=5, anchor="w")
    module_file_frame = tk.Frame(config_window, bg="black")
    module_file_frame.pack(padx=10, pady=5, fill="x")
    module_file_entry = tk.Entry(module_file_frame, width=30, bg="white", fg="black", font=entry_font)
    module_file_entry.pack(side="left", fill="x", expand=True)
    tk.Button(module_file_frame, text="Browse", command=browse_module_file, bg="white", fg="black", font=button_font).pack(side="right")

    tk.Label(config_window, text="Protections Preset:", fg="red", bg="black", font=label_font).pack(padx=10, pady=5, anchor="w")
    protections_preset_var = tk.StringVar(config_window)
    protections_preset_var.set("normal")  # default value
    protections_preset_menu = tk.OptionMenu(config_window, protections_preset_var, "none", "minimum", "normal", "aggressive", "maximum")
    protections_preset_menu.config(bg="white", fg="black", font=button_font)
    protections_preset_menu["menu"].config(bg="white", fg="black", font=button_font)
    protections_preset_menu.pack(padx=10, pady=5)

    def save_and_close():
        base_directory = base_directory_entry.get()
        output_directory = output_directory_entry.get()
        module_file = module_file_entry.get()
        protections_preset = protections_preset_var.get()

        if not base_directory or not output_directory or not module_file:
            messagebox.showerror("Error", "Please fill in all fields.")
            return

        project_file_path = create_csproj_file(base_directory, output_directory, module_file, protections_preset)
        config_window.destroy()
        entry_file_path.delete(0, tk.END)
        entry_file_path.insert(0, project_file_path)

    save_button = tk.Button(config_window, text="Save", command=save_and_close, bg="white", fg="black", font=button_font)
    save_button.pack(pady=20)

def obfuscate():
    file_path = entry_file_path.get()
    save_path = entry_save_path.get()
    iterations = entry_iterations.get()
    language = language_var.get()
    
    if not file_path:
        messagebox.showerror("Error", "Please select a file.")
        return
    
    if not save_path:
        messagebox.showerror("Error", "Please select a save directory.")
        return
    
    if not iterations.isdigit() or int(iterations) <= 0:
        messagebox.showerror("Error", "Number of iterations must be a positive integer.")
        return
    
    if language == "C#":
        if not file_path.endswith(".csproj"):
            messagebox.showerror("Error", "The selected file is not a .csproj file.")
            return
        
        command = f"Confuser.CLI.exe -n {file_path}"
    
    else:
        if language == "Python":
            command = f"pyarmor obfuscate --entry {file_path} --output {save_path}"
        elif language == "C":
            command = f"iwwerc {file_path} {save_path}.c"
        elif language == "C++":
            command = f"iwwerc {file_path} {save_path}.cpp"
        elif language == "Java":
            command = f"proguard @config.pro -injars {file_path} -outjars {save_path}.jar"
        else:
            messagebox.showerror("Error", "Unsupported language.")
            return

    # Open the obfuscating window
    obfuscating_window = tk.Toplevel(root)
    obfuscating_window.title("Obfuscating...")
    obfuscating_window.geometry("400x300")
    obfuscating_window.configure(bg="black")

    log_text = tk.Text(obfuscating_window, wrap="word", bg="black", fg="white", font=entry_font)
    log_text.pack(expand=True, fill="both", padx=10, pady=10)
    log_text.insert(tk.END, "Starting obfuscation...\n")
    obfuscating_window.update()

    try:
        for i in range(int(iterations)):
            subprocess.run(command, shell=True, check=True)
            log_text.insert(tk.END, f"Iteration {i + 1} complete\n")
            obfuscating_window.update()

        messagebox.showinfo("Success", "Obfuscation completed successfully.")
        log_text.insert(tk.END, "Obfuscation completed successfully.\n")
        obfuscating_window.update()
    
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Error", f"Command failed with error: {e}")
        log_text.insert(tk.END, f"Error: {e}\n")
        obfuscating_window.update()
    
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred during obfuscation: {e}")
        log_text.insert(tk.END, f"Error: {e}\n")
        obfuscating_window.update()
    
    finally:
        obfuscating_window.after(3000, obfuscating_window.destroy)

def select_file():
    file_path = filedialog.askopenfilename(filetypes=[("All Files", "*.*")])
    entry_file_path.delete(0, tk.END)
    entry_file_path.insert(0, file_path)

def select_save_directory():
    save_path = filedialog.askdirectory()
    entry_save_path.delete(0, tk.END)
    entry_save_path.insert(0, save_path)

def update_config_button_visibility(*args):
    if language_var.get() == "C#":
        config_button.grid(row=1, column=4, padx=10, pady=10)
    else:
        config_button.grid_forget()

# GUI setup
root = tk.Tk()
root.title("OBFCODE")
root.configure(bg="black")

# Fonts
title_font = font.Font(family="Helvetica", size=18, weight="bold")
label_font = font.Font(family="Helvetica", size=12)
entry_font = font.Font(family="Helvetica", size=10)
button_font = font.Font(family="Helvetica", size=10, weight="bold")

# Title
title_label = tk.Label(root, text="OBFCODE", fg="red", bg="black", font=title_font)
title_label.grid(row=0, column=0, columnspan=5, padx=10, pady=20)

# File path section
tk.Label(root, text="Select file:".upper(), fg="red", bg="black", font=label_font).grid(row=1, column=0, padx=10, pady=10, sticky="e")
entry_file_path = tk.Entry(root, width=50, bg="white", fg="black", font=entry_font)
entry_file_path.grid(row=1, column=1, padx=10, pady=10, columnspan=2, sticky="w")
tk.Button(root, text="Browse", command=select_file, bg="white", fg="black", font=button_font).grid(row=1, column=3, padx=10, pady=10)

# Save directory section
tk.Label(root, text="Save to:".upper(), fg="red", bg="black", font=label_font).grid(row=2, column=0, padx=10, pady=10, sticky="e")
entry_save_path = tk.Entry(root, width=50, bg="white", fg="black", font=entry_font)
entry_save_path.grid(row=2, column=1, padx=10, pady=10, columnspan=2, sticky="w")
tk.Button(root, text="Browse", command=select_save_directory, bg="white", fg="black", font=button_font).grid(row=2, column=3, padx=10, pady=10)

# Iterations and Language section
tk.Label(root, text="Repeat:".upper(), fg="red", bg="black", font=label_font).grid(row=3, column=0, padx=10, pady=10, sticky="e")
entry_iterations = tk.Entry(root, width=10, bg="white", fg="black", font=entry_font)
entry_iterations.grid(row=3, column=1, padx=10, pady=10, sticky="w")

tk.Label(root, text="Language:".upper(), fg="red", bg="black", font=label_font).grid(row=3, column=1, padx=10, pady=10, sticky="e")
language_var = tk.StringVar(root)
language_var.set("Python")  # default value
language_menu = tk.OptionMenu(root, language_var, "Python", "C", "C++", "C#", "Java")
language_menu.config(bg="white", fg="black", font=button_font)
language_menu["menu"].config(bg="white", fg="black", font=button_font)
language_menu.grid(row=3, column=2, padx=10, pady=10, sticky="w")
language_var.trace("w", update_config_button_visibility)

# Config .csproj button
config_button = tk.Button(root, text="Config .csproj", command=open_csproj_config_window, bg="white", fg="black", font=button_font)
config_button.grid(row=1, column=4, padx=10, pady=10)
config_button.grid_forget()  # Initially hidden

# Obfuscate button
tk.Button(root, text="Obfuscate".upper(), command=obfuscate, bg="white", fg="red", font=button_font, bd=2, relief="groove").grid(row=4, column=1, columnspan=2, padx=10, pady=20)

# Run the GUI
root.mainloop()
