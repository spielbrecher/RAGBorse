import tkinter as tk
from tkinter import filedialog
import os
import pdf_recognizer as pdf
from model import Model

class QuestionAnswerApp:
    def __init__(self, master):
        master.title("Отчеты")

        # Frame for question entry
        self.question_frame = tk.Frame(master)
        self.question_frame.pack(pady=10)

        self.question_label = tk.Label(self.question_frame, text="Введите вопрос:")
        self.question_label.pack()

        self.question_entry = tk.Entry(self.question_frame, width=50)
        self.question_entry.pack(fill=tk.X, pady=10, expand=True)  # Растянуто по ширине

        self.answer_button = tk.Button(self.question_frame, text="Получить ответ", command=self.get_answer)
        self.answer_button.pack()

        # Frame for answer display
        self.answer_frame = tk.Frame(master)
        self.answer_frame.pack(pady=10)

        self.answer_text = tk.Text(self.answer_frame, height=10, width=50)
        self.answer_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Frame for buttons and file label
        self.button_frame = tk.Frame(master)
        self.button_frame.pack(pady=10)

        self.load_button = tk.Button(self.button_frame, text="Загрузить PDF", command=self.load_pdf)
        self.load_button.pack(side=tk.LEFT)


        # Label for displaying selected PDF filename (at the bottom)
        self.filename_frame = tk.Frame(master)
        self.filename_frame.pack(pady=10)
        self.filename_label = tk.Label(self.filename_frame, text="Выбранный файл: ")
        self.filename_label.pack(side=tk.LEFT, fill=tk.X, expand=True)  # Растянуто по ширине

    def load_pdf(self):
        # Открытие диалогового окна для выбора файла
        selected_file = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])

        # Проверка, выбран ли файл
        if selected_file:
            # Обновление метки с именем файла
            self.filename_label.config(text=f"Выбранный файл: {os.path.basename(selected_file)}")
            self.result = pdf.start(os.path.basename(selected_file))
            # Create Model
            self.gigachat_model = Model()
            self.gigachat_model.setReport(self.result)
            self.gigachat_model.transform()
            self.gigachat_model.create_embeddings()


    def get_answer(self):
        # Getting the question
        s = self.question_entry.get()
        self.question_entry.delete(0, tk.END)
        ans = self.gigachat_model.getAnswer(s)
        # Insert the new text into answer_text, keeping the existing content
        self.answer_text.delete(1.0, tk.END)
        self.answer_text.insert(tk.END, ans['result'])

