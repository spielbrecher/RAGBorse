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
        self.question_frame.pack(padx=10, pady=10)

        self.question_label = tk.CTkLabel(self.question_frame, text="Введите вопрос:")
        self.question_label.pack()

        self.question_entry = tk.CTkEntry(self.question_frame, height=20, width=600)
        self.question_entry.pack(fill=tk.X, padx=10, pady=10, expand=True)

        self.answer_button = tk.CTkButton(self.question_frame, text="Получить ответ", command=self.get_answer)
        self.answer_button.pack(padx=10, pady=10)

        # Answer Display Frame
        self.answer_frame = tk.CTkFrame(master, corner_radius=10)
        self.answer_frame.pack(padx=10, pady=10)

        self.answer_text = tk.CTkTextbox(self.answer_frame, height=140, width=620)
        self.answer_text.pack(padx=10, pady=10, side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Load Button Frame
        self.load_button_frame = tk.CTkFrame(master, corner_radius=10)
        self.load_button_frame.pack(padx=10, pady=10)

        self.load_button = tk.CTkButton(self.load_button_frame, text="Загрузить PDF", command=self.load_pdf)
        self.load_button.pack(side=tk.LEFT, padx=10, pady=10)

        self.load_all_button = tk.CTkButton(self.load_button_frame, text="Все PDF", command=self.all_pdf)
        self.load_all_button.pack(side=tk.LEFT, padx=10, pady=10)

        self.load_chroma_button = tk.CTkButton(self.load_button_frame, text="Загрузить БД", command=self.load_bd)
        self.load_chroma_button.pack(side=tk.LEFT, padx=10, pady=10)

        # Filename Label Frame
        self.filename_frame = tk.CTkFrame(master, corner_radius=10)
        self.filename_frame.pack(padx=10, pady=10)

        self.filename_label = tk.CTkLabel(self.filename_frame, text="Выбранный файл: ")
        self.filename_label.pack(fill=tk.X, padx=10, pady=10, expand=True)

        self.progressbar = tk.CTkProgressBar(master=self.filename_frame)
        self.progressbar.pack(padx=10, pady=10)
        self.progressbar.set(0)

        # load from disk Chroma
        self.gigachat_model = Model()


    def load_bd(self):
        self.gigachat_model.load_chroma()

    def load_pdf(self):
        # Открытие диалогового окна для выбора файла
        selected_file = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])

        # Проверка, выбран ли файл
        if selected_file:
            # Обновление метки с именем файла
            self.filename_label.configure(text=f"Выбранный файл: {os.path.basename(selected_file)}")
            self.result = pdf.start(os.path.basename(selected_file))
            # Create Model
            self.gigachat_model.setReport(self.result)
            self.gigachat_model.transform()
            self.gigachat_model.create_embeddings()

    def select_folder(self):
        # Get the selected folder path using filedialog
        folder_path = filedialog.askdirectory(title="Выберите папку с PDF файлами")

        # Check if a folder was selected
        if folder_path:
            # Update the filename label
            self.filename_label.configure(text=f"Выбранная папка: {folder_path}")

            # Process all PDF files in the folder
            self.process_pdf_files(folder_path)

    def process_pdf_files(self, folder_path):
        # Get a list of all PDF file paths in the folder
        pdf_file_paths = [os.path.join(folder_path, filename) for filename in os.listdir(folder_path) if
                          filename.endswith(".pdf")]
        total = len(pdf_file_paths)
        counter = 1
        self.all_text = ''
        for file_path in pdf_file_paths:
            counter += 1
            percent = counter/total
            self.progressbar.set(percent)
            self.progressbar.update()
            print(f"Processing PDF: {file_path}")
            self.filename_label.configure(text=f"Выбранный файл: {os.path.basename(file_path)}")
            self.result = pdf.start(os.path.abspath(file_path))  # pdf as text
            self.all_text += self.result

        # Create Model
        #self.gigachat_model = Model()
        self.gigachat_model.setReport(self.all_text)
        self.gigachat_model.transform()
        self.gigachat_model.create_embeddings()



    def all_pdf(self):
        self.select_folder()

    def get_answer(self):
        # Getting the question
        s = self.question_entry.get()
        self.question_entry.delete(0, tk.END)
        ans = self.gigachat_model.getAnswer(s)
        # Insert the new text into answer_text, keeping the existing content
        self.answer_text.delete(1.0, tk.END)
        self.answer_text.insert(tk.END, ans['result'])

