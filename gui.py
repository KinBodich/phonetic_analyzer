import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import os
import threading
from main import main as run_main  # тепер очікує log_callback

def run_analysis(input_path, output_path, status_label, console_text):
    """
    Викликає run_main з log_callback, який вставляє повідомлення у console_text.
    """
    def log_to_console(msg):
        console_text.configure(state="normal")
        console_text.insert(tk.END, msg + "\n")
        console_text.see(tk.END)
        console_text.configure(state="disabled")

    try:
        run_main(input_path, output_path, log_callback=log_to_console)
        status_label.config(text="Аналіз завершено успішно.")
    except Exception as e:
        status_label.config(text="Помилка")
        messagebox.showerror("Помилка", str(e))

def browse_input_file(entry):
    path = filedialog.askopenfilename(
        filetypes=[("Text files", "*.txt")],
        initialdir=os.getcwd()
    )
    if path:
        entry.delete(0, tk.END)
        entry.insert(0, path)

def browse_input_folder(entry):
    path = filedialog.askdirectory(initialdir=os.getcwd())
    if path:
        entry.delete(0, tk.END)
        entry.insert(0, path)

def browse_output_folder(entry):
    path = filedialog.askdirectory(initialdir=os.getcwd())
    if path:
        entry.delete(0, tk.END)
        entry.insert(0, path)

def start_gui():
    window = tk.Tk()
    window.title("Автом. фонетичний розбір")
    window.geometry("700x550")

    tk.Label(window, text="Вхідний файл або папка:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
    input_entry = tk.Entry(window, width=50)
    input_entry.grid(row=0, column=1, padx=5, pady=5)

    btn_frame = tk.Frame(window)
    btn_frame.grid(row=0, column=2, padx=5)
    tk.Button(btn_frame, text="Вибрати файл", command=lambda: browse_input_file(input_entry)).pack(side="left", padx=2)
    tk.Button(btn_frame, text="Вибрати папку", command=lambda: browse_input_folder(input_entry)).pack(side="left", padx=2)

    tk.Label(window, text="Вихідна папка:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
    output_entry = tk.Entry(window, width=50)
    output_entry.grid(row=1, column=1, padx=5, pady=5)
    tk.Button(window, text="Вибрати папку", command=lambda: browse_output_folder(output_entry)).grid(row=1, column=2, padx=5)

    status_label = tk.Label(window, text="")
    status_label.grid(row=2, column=0, columnspan=3, sticky="w", padx=5)

    console_text = scrolledtext.ScrolledText(window, width=80, height=25, state="disabled")
    console_text.grid(row=3, column=0, columnspan=3, padx=5, pady=5)

    def on_start():
        input_path_val = input_entry.get().strip()
        output_path_val = output_entry.get().strip()

        if not input_path_val or not output_path_val:
            messagebox.showerror("Помилка", "Не вказано вхідний файл/папку або вихідну папку.")
            return
        if not os.path.exists(input_path_val):
            messagebox.showerror("Помилка", "Вказаний вхідний шлях не існує.")
            return
        if not os.path.isdir(output_path_val):
            messagebox.showerror("Помилка", "Вказана вихідна папка не існує.")
            return

        console_text.configure(state="normal")
        console_text.delete("1.0", tk.END)
        console_text.configure(state="disabled")

        status_label.config(text="Аналіз виконується...")
        thread = threading.Thread(
            target=run_analysis,
            args=(input_path_val, output_path_val, status_label, console_text)
        )
        thread.start()

    tk.Button(window, text="Старт", command=on_start).grid(row=4, column=1, pady=10)

    window.mainloop()

if __name__ == "__main__":
    start_gui()
