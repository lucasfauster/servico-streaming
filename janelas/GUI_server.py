from tkinter import *
from tkinter import ttk
from tkinter.ttk import Progressbar
from PIL import Image, ImageTk
from db.video_transactions import *
from tkinter.filedialog import askopenfile
import cv2
import time
import imutils
from shutil import copyfile


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
    final_path = f'../videos/{resolution}/{name}.mp4'
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


def list_videos():
    count = 0
    videos = read_videos_transaction()
    for video in videos:
        if count % 2 == 0:
            table_view.insert(parent='', index='end', iid=count, text="",
                               values=(video[0], video[1], video[2], video[3]), tags=('evenrow',))
        else:
            table_view.insert(parent='', index='end', iid=count, text="",
                               values=(video[0], video[1], video[2], video[3]), tags=('oddrow',))
        count += 1


def add_video():
    show_video_window(janela, "CREATE")


def update_video():
    selected = table_view.focus()
    if selected:
        id_video, name, resolution, path = table_view.item(selected, 'value')
        show_video_window(janela, "UPDATE", id_video, name, resolution, path)
    else:
        print("Nenhum vídeo selecionado")


def delete_video():
    selected = table_view.focus()
    if selected:
        id_video = table_view.item(selected, 'value')[0]
        delete_video_transaction(id_video)
        refresh_list_videos()
    else:
        print("Nenhum vídeo selecionado")


def refresh_list_videos():
    for video in table_view.get_children():
        table_view.delete(video)
    list_videos()


def video_stream(name, resolution, path):
    video_cap = cv2.VideoCapture(path)

    while video_cap.isOpened():
        ret, frame = video_cap.read()
        if ret:
            frame = imutils.resize(frame, width=600)
            cv2.imshow('Frame', frame)
            cv2.setWindowTitle('Frame', f'{name} ({resolution})')
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                print("VÍDEO FECHADO")
                video_cap.release()
                cv2.destroyWindow('Frame')
                break
        else:
            print("VIDEO TERMINOU!")
            video_cap.release()
            cv2.destroyWindow('Frame')
            break




def play_video():
    selected = table_view.focus()
    id_video, name, resolution, path = table_view.item(selected, 'value')
    video_stream(name, resolution, path)


def clicker(e):
    table_view.focus()


# #  Janela
janela = Tk()
janela.title('Biting Wire - Seu Programa de Streaming Favorito')
janela.configure(background='white')
width, height = 700, 500
janela.geometry(str(width) + "x" + str(height))

# Logo
logo = Frame(janela)
logo.pack(padx=(0, 70), pady=5)
img = ImageTk.PhotoImage(Image.open("logo.png").resize((214, 120)))
logo_panel = Label(logo, image=img)
logo_panel.pack()
logo_panel.configure(background='white')

# Tabela
style = ttk.Style()
style.theme_use("default")
style.configure("Treeview", background="#D3D3D3", foreground="black", rowheight=25, fieldbackground="#D3D3D3")
style.map('Treeview', background=[('selected', '#785923')])
tabela_frame = Frame(janela)
tabela_frame.pack(side="top", padx=50, pady=20)
tabela_frame.configure(background='white')
tabela_scroll = Scrollbar(tabela_frame)
tabela_scroll.pack(side=RIGHT, fill=Y)
table_view = ttk.Treeview(tabela_frame, yscrollcommand=tabela_scroll.set, selectmode="browse")
table_view.pack()
tabela_scroll.config(command=table_view.yview)
table_view['columns'] = ("ID", "Vídeo", "Qualidade", "Caminho")
table_view.column("#0", width=0, stretch=NO)
table_view.column("ID", anchor=CENTER, width=50)
table_view.column("Vídeo", anchor=W, width=140)
table_view.column("Qualidade", anchor=CENTER, width=100)
table_view.column("Caminho", anchor=CENTER, width=250)
table_view.heading("#0", text="", anchor=CENTER)
table_view.heading("ID", text="ID", anchor=CENTER)
table_view.heading("Vídeo", text="Vídeo", anchor=CENTER)
table_view.heading("Qualidade", text="Qualidade", anchor=CENTER)
table_view.heading("Caminho", text="Caminho", anchor=CENTER)
table_view.tag_configure('oddrow', background="white")
table_view.tag_configure('evenrow', background="orange")

# Botões
menu_frame = Frame(janela)
menu_frame.pack()
menu_frame.configure(background='white')
reproduzir_button = Button(menu_frame, text="Reproduzir Vídeo", width=12, height=2, command=play_video, bg="orange")
reproduzir_button.pack(side=LEFT, padx=10)
adicionar_video_button = Button(menu_frame, text="Adicionar Vídeo", width=12, height=2, command=add_video, bg="orange")
adicionar_video_button.pack(side=LEFT, padx=10)
editar_video_button = Button(menu_frame, text="Editar Vídeo", width=12, height=2, command=update_video, bg="orange")
editar_video_button.pack(side=LEFT, padx=10)
remover_video_button = Button(menu_frame, text="Remover Vídeo", width=12, height=2, command=delete_video, bg="orange")
remover_video_button.pack(side=LEFT, padx=10)


table_view.bind("<ButtonRelease-1>", clicker)

list_videos()
janela.mainloop()
