from tkinter import *
from tkinter import ttk
from db.video_transactions import *
from tkinter.filedialog import askopenfile
from shutil import copyfile
from tkinter.ttk import Progressbar
import time


class AddVideoGUI:
    def __init__(self, main, transaction, id_video="", name="", resolution="", path=""):
        self.main = main
        self.transaction = transaction
        self.window = Toplevel(main)
        
        self.id_video = id_video
        self.name = name
        self.resolution = resolution
        self.path = path

        self.name_label = Label(self.window, text="Nome do Vídeo: ")
        self.name_input = Entry(self.window, width=30)

        self.resolution_label = Label(self.window, text="Resolução: ")
        self.option = StringVar(self.window)
        self.resolution_input = OptionMenu(self.window, self.option, "240p", "480p", "720p")
        self.resolution_input.grid(sticky="W", row=1, column=1, pady=10, padx=10)

        self.file_label = Label(self.window, text="Arquivo: ")
        self.path_input = Entry(self.window, width=30)

        self.choose_file_button = Button(self.window, text='Escolher Arquivo', command=lambda: self.choose_file())
        self.output_label = Label(self.window, text="")

        self.add_video_button = None

        self.progress_bar = Progressbar(self.window, orient=HORIZONTAL, length=300, mode='determinate', style='TProgressbar')
        self.bar_style = ttk.Style()

    def configure(self):
        self.window.title('Adicionar Vídeo')
        self.window.geometry('400x220')
        self.window.configure(background='#b3b3b3')

        self.name_label.grid(row=0, column=0, pady=10, padx=10)
        self.name_label.configure(background='#b3b3b3')
        self.name_input.grid(row=0, column=1, columnspan=2, pady=10, padx=10)
        if self.transaction == "UPDATE":
            self.name_input.insert(0, self.name)

        self.resolution_label.grid(sticky="E", row=1, column=0, pady=10, padx=10)
        self.resolution_label.configure(background='#b3b3b3')
        if self.transaction == "CREATE":
            self.option.set("240p")
        elif self.transaction == "UPDATE":
            self.option.set(self.resolution)

        self.file_label.grid(sticky="E", row=2, column=0, pady=10, padx=10)
        self.file_label.configure(background='#b3b3b3')
        self.path_input.grid(row=2, column=1, columnspan=2, pady=10, padx=10)
        if self.transaction == "CREATE":
            self.path_input.insert(0, ' Nenhum arquivo selecionado')
        elif self.transaction == "UPDATE":
            self.path_input.insert(0, self.path)
        self.path_input.configure(state=DISABLED)

        self.choose_file_button.grid(row=1, column=2)
        self.output_label.grid(row=4, columnspan=3, pady=10)
        self.output_label.configure(background='#b3b3b3')

        if self.transaction == "CREATE":
            button_text = 'Adicionar Vídeo'
            self.add_video_button = Button(self.window, text=button_text, command=lambda: self.save_video())
        elif self.transaction == "UPDATE":
            button_text = 'Atualizar Vídeo'
            self.add_video_button = Button(self.window, text=button_text,  command=lambda: self.save_video())
        self.add_video_button.grid(row=3, column=1, pady=5)
        self.bar_style.configure("TProgressbar", troughcolor='gray', background='green')
 
    def render(self):
        self.configure()
        self.window.mainloop()

    def choose_file(self):
        path_file = askopenfile(mode='r', filetypes=[('Vídeos', '*mp4')])
        path_file = path_file.name
        if path_file:
            self.path_input.configure(state=NORMAL)
            self.path_input.delete(0, END)
            self.path_input.insert(0, path_file)
            self.path_input.configure(state=DISABLED)

    def validates(self):
        if self.name and self.resolution and self.path and self.path != ' Nenhum arquivo selecionado':
            return True
        elif not self.name:
            self.output_label.config(text='Nome não pode ficar em branco!', foreground='red')
        elif self.path == ' Nenhum arquivo selecionado' or not self.path:
            self.output_label.config(text='Arquivo não pode ficar em branco!', foreground='red')
        elif not self.resolution:
            self.output_label.config(text='Resolução não pode ficar em branco!', foreground='red')
        else:
            self.output_label.config(text='Erro ao adicionar vídeo!', foreground='red')
        return False

    def save_video(self):
        self.name = self.name_input.get()
        self.resolution = self.option.get()
        self.path = self.path_input.get()
        final_path = f'../videos/{self.resolution}/{self.name}'
        copyfile(self.path, final_path)
    
        if self.validates():
            self.progress_bar.grid(row=4, columnspan=3, pady=20)
            for i in range(5):
                self.window.update_idletasks()
                self.progress_bar['value'] += 20
                time.sleep(0.2)
            self.progress_bar.destroy()
            if self.transaction == "CREATE":
                create_video_transaction(self.name, self.resolution, final_path)  # Chamada SQL
                self.output_label.config(text='Vídeo adicionado com sucesso!', foreground='green')
            elif self.transaction == "UPDATE" and self.id_video:
                update_videos_transaction(self.id_video, self.name, self.resolution, final_path)  # Chamada SQL
                self.output_label.config(text='Vídeo atualizado com sucesso!', foreground='green')
            self.add_video_button.destroy()
            quit_button = Button(self.window, text='Fechar', command=lambda: self.window.destroy())
            quit_button.grid(row=3, column=1, pady=5)
