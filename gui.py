import tkinter as tk
from tkinter import filedialog, messagebox
import os
import threading
from main import main as run_main

def run_analysis(input_path, output_path, status_label):
    try:
        run_main(input_path, output_path)
        status_label.config(text="Аналіз завершено успішно.")
    except Exception as e:
        status_label.config(text="Помилка")
        messagebox.showerror("Помилка", str(e))

def browse_input(entry):
    path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    if path:
        entry.delete(0, tk.END)
        entry.insert(0, path)

def browse_input_folder(entry):
    path = filedialog.askdirectory()
    if path:
        entry.delete(0, tk.END)
        entry.insert(0, path)

def browse_output(entry):
    path = filedialog.askdirectory()
    if path:
        entry.delete(0, tk.END)
        entry.insert(0, path)

def start_gui():
    window = tk.Tk()
    window.title("Phonetic Analyzer")

    tk.Label(window, text="Файл або папка з текстами:").grid(row=0, column=0, sticky="w")
    input_entry = tk.Entry(window, width=60)
    input_entry.grid(row=0, column=1)
    tk.Button(window, text="Огляд (файл)", command=lambda: browse_input(input_entry)).grid(row=0, column=2)
    tk.Button(window, text="Огляд (папка)", command=lambda: browse_input_folder(input_entry)).grid(row=0, column=3)

    tk.Label(window, text="АБО введіть текст нижче:").grid(row=1, column=0, sticky="nw", pady=(10,0))
    text_box = tk.Text(window, height=10, width=70)
    text_box.grid(row=1, column=1, columnspan=3, pady=(10, 0))

    tk.Label(window, text="Папка для збереження результатів:").grid(row=2, column=0, sticky="w", pady=(10,0))
    output_entry = tk.Entry(window, width=60)
    output_entry.grid(row=2, column=1, pady=(10,0))
    tk.Button(window, text="Огляд", command=lambda: browse_output(output_entry)).grid(row=2, column=2, pady=(10,0))

    status_label = tk.Label(window, text="", fg="blue")
    status_label.grid(row=4, column=0, columnspan=4, pady=10)

    def on_start():
        input_path = input_entry.get().strip()
        manual_text = text_box.get("1.0", tk.END).strip()
        output_path = output_entry.get().strip()

        if not os.path.exists(output_path):
            os.makedirs(output_path)

        if manual_text:
            # Зберегти введений текст у тимчасовий файл
            manual_file_path = os.path.join(output_path, "manual_input.txt")
            with open(manual_file_path, "w", encoding="utf-8") as f:
                f.write(manual_text)
            input_path_final = manual_file_path
        elif os.path.exists(input_path):
            input_path_final = input_path
        else:
            messagebox.showerror("Помилка", "Не вказано вхідний текст або шлях до файлу/папки.")
            return

        status_label.config(text="Аналіз виконується...")
        thread = threading.Thread(target=run_analysis, args=(input_path_final, output_path, status_label))
        thread.start()

    tk.Button(window, text="Старт", command=on_start).grid(row=3, column=1, pady=10)

    window.mainloop()

if __name__ == "__main__":
    start_gui()
