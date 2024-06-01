import customtkinter as tk
from frame import QuestionAnswerApp

if __name__ == '__main__':
    root = tk.CTk()
    app = QuestionAnswerApp(root)
    root.geometry("640x480")
    root.mainloop()