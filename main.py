import customtkinter as сtk
import tkinter as tk

from frame import QuestionAnswerApp

if __name__ == '__main__':
    root = tk.Tk()
    app = QuestionAnswerApp(root)
    root.title('Анализ отчетов')
    root.geometry("640x480")
    root.update()
    root.mainloop()