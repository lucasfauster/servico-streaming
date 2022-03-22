import os
from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
from db.video_transactions import *
import cv2
import imutils
from tkinter.filedialog import askopenfile
from shutil import copyfile
import time
from tkinter.ttk import Progressbar


def choose_file(path_input):
    path_file = askopenfile(mode='r', filetypes=[('Vídeos', '*mp4')])
    path_file = path_file.name
    if path_file:
        path_input.configure(state=NORMAL)
        path_input.delete(0, END)
        path_input.insert(0, path_file)
        path_input.configure(state=DISABLED)

def validates(name, resolution, path, output_label):
    if name and resolution and path and path != ' Nenhum arquivo selecionado':
        return True
    elif not name:
        output_label.config(text='Nome não pode ficar em branco!', foreground='red')
    elif path == ' Nenhum arquivo selecionado' or not path:
        output_label.config(text='Arquivo não pode ficar em branco!', foreground='red')
    elif not resolution:
        output_label.config(text='Resolução não pode ficar em branco!', foreground='red')
    else:
        output_label.config(text='Erro ao adicionar vídeo!', foreground='red')
    return False


def show_video_window(main, transaction, id_video="", name="", resolution="", path=""):
    window = Toplevel(main)
    window.title('Adicionar Vídeo')
    window.geometry('400x220')
    window.configure(background='#b3b3b3')
    style_barra = ttk.Style()
    style_barra.configure("TProgressbar", troughcolor='gray', background='green')

    # Name
    name_label = Label(window, text="Nome do Vídeo: ")
    name_label.grid(row=0, column=0, pady=10, padx=10)
    name_label.configure(background='#b3b3b3')
    name_input = Entry(window, width=30)
    name_input.grid(row=0, column=1, columnspan=2, pady=10, padx=10)
    if transaction == "UPDATE":
        name_input.insert(0, name)

    # Resolution
    resolution_label = Label(window, text="Resolução: ")
    resolution_label.grid(sticky="E", row=1, column=0, pady=10, padx=10)
    resolution_label.configure(background='#b3b3b3')
    option = StringVar(window)
    if transaction == "CREATE":
        option.set("240p")
    elif transaction == "UPDATE":
        option.set(resolution)
    resolution_input = OptionMenu(window, option, "240p", "480p", "720p")
    resolution_input.grid(sticky="W", row=1, column=1, pady=10, padx=10)

    # File Path
    file_label = Label(window, text="Arquivo: ")
    file_label.grid(sticky="E", row=2, column=0, pady=10, padx=10)
    file_label.configure(background='#b3b3b3')
    path_input = Entry(window, width=30)
    path_input.grid(row=2, column=1, columnspan=2, pady=10, padx=10)
    if transaction == "CREATE":
        path_input.insert(0, ' Nenhum arquivo selecionado')
    elif transaction == "UPDATE":
        path_input.insert(0, path)
    path_input.configure(state=DISABLED)
    choose_file_button = Button(window, text='Escolher Arquivo', command=lambda: choose_file(path_input))
    choose_file_button.grid(row=1, column=2)

    # Add video
    output_label = Label(window, text="")
    output_label.grid(row=4, columnspan=3, pady=10)
    output_label.configure(background='#b3b3b3')
    if transaction == "CREATE":
        button_text = 'Adicionar Vídeo'
        add_video_button = Button(window, text=button_text,
                                  command=lambda: save_video(name_input, option, path_input, output_label, window,
                                                             add_video_button, transaction))
    elif transaction == "UPDATE":
        button_text = 'Atualizar Vídeo'
        add_video_button = Button(window, text=button_text,
                                  command=lambda: save_video(name_input, option, path_input, output_label, window,
                                                             add_video_button, transaction, id_video))

    add_video_button.grid(row=3, column=1, pady=5)


def save_video(name_input, option, path_input, output_label, window, add_video_button, transaction, id_video=""):
    name = name_input.get()
    resolution = option.get()
    path = path_input.get()
    final_path = f'../videos/{resolution}/{name}'
    copyfile(path, final_path)

    if validates(name, resolution, path, output_label):
        barra_progresso = Progressbar(window, orient=HORIZONTAL, length=300, mode='determinate', style='TProgressbar')
        barra_progresso.grid(row=4, columnspan=3, pady=20)
        for i in range(5):
            window.update_idletasks()
            barra_progresso['value'] += 20
            time.sleep(0.2)
        barra_progresso.destroy()
        if transaction == "CREATE":
            create_video_transaction(name, resolution, final_path)  # Chamada SQL
            output_label.config(text='Vídeo adicionado com sucesso!', foreground='green')
        elif transaction == "UPDATE" and id_video:
            update_videos_transaction(id_video, name, resolution, final_path)  # Chamada SQL
            output_label.config(text='Vídeo atualizado com sucesso!', foreground='green')
        add_video_button.destroy()
        quit_button = Button(window, text='Fechar', command=lambda: window.destroy())
        quit_button.grid(row=3, column=1, pady=5)
        refresh_list_videos()