import customtkinter as tk
from customtkinter import filedialog
import os
import pdf_recognizer as pdf
from model import Model

class QuestionAnswerApp:
    def __init__(self, master):
        #tk.set_appearance_mode("Dark")
        # Question Entry Frame

        self.question_frame = tk.CTkFrame(master, corner_radius=10)
        self.question_frame.pack(pady=10)

        self.question_label = tk.CTkLabel(self.question_frame, text="Введите вопрос:")
        self.question_label.pack()

        self.question_entry = tk.CTkEntry(self.question_frame, height=20, width=600)
        self.question_entry.pack(fill=tk.X, padx=10, pady=10, expand=True)

        self.answer_button = tk.CTkButton(self.question_frame, text="Получить ответ", command=self.get_answer)
        self.answer_button.pack(pady=10)

        # Answer Display Frame
        self.answer_frame = tk.CTkFrame(master, corner_radius=10)
        self.answer_frame.pack(pady=10)

        self.answer_text = tk.CTkTextbox(self.answer_frame, height=200, width=620)
        self.answer_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Load Button Frame
        self.load_button_frame = tk.CTkFrame(master, corner_radius=10)
        self.load_button_frame.pack(pady=10)

        self.load_button = tk.CTkButton(self.load_button_frame, text="Загрузить PDF", command=self.load_pdf)
        self.load_button.pack(side=tk.LEFT)

        # Filename Label Frame
        self.filename_frame = tk.CTkFrame(master, corner_radius=10)
        self.filename_frame.pack(pady=10)

        self.filename_label = tk.CTkLabel(self.filename_frame, text="Выбранный файл: ")
        self.filename_label.pack(side=tk.LEFT, fill=tk.X, expand=True)

    def load_pdf(self):
        # Открытие диалогового окна для выбора файла
        selected_file = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])

        # Проверка, выбран ли файл
        if selected_file:
            # Обновление метки с именем файла
            self.filename_label.configure(text=f"Выбранный файл: {os.path.basename(selected_file)}")
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

