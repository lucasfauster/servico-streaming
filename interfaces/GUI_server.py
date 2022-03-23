from tkinter import *
from tkinter import ttk
from db.video_transactions import *
from tkinter.filedialog import askopenfile
from shutil import copyfile
from tkinter.ttk import Progressbar
from PIL import Image, ImageTk
import cv2
import imutils
import os
import time


class ServerGUI:
    WIDTH = 700
    HEIGHT = 500
    LOGO = "logo.png"

    def __init__(self):
        self.window = Tk()
        self.videos = None

        self.logo = Frame(self.window)
        self.img = ImageTk.PhotoImage(Image.open(self.LOGO).resize((214, 120)))
        self.logo_panel = Label(self.logo, image=self.img)
        self.output_label = Label(self.window, text="")

        self.style = ttk.Style()
        self.table_frame = Frame(self.window)
        self.table_scroll = Scrollbar(self.table_frame)
        self.table_view = ttk.Treeview(self.table_frame, yscrollcommand=self.table_scroll.set, selectmode="browse")

        self.menu_frame = Frame(self.window)

        self.play_button = Button(self.menu_frame, text="Reproduzir Vídeo", width=12, height=2,
                                  command=self.play_video, bg="orange")
        self.add_video_button = Button(self.menu_frame, text="Adicionar Vídeo", width=12, height=2,
                                       command=self.add_video, bg="orange")
        self.edit_video_button = Button(self.menu_frame, text="Editar Vídeo", width=12, height=2,
                                        command=self.update_video, bg="orange")
        self.remove_video_button = Button(self.menu_frame, text="Remover Vídeo", width=12, height=2,
                                          command=self.delete_video, bg="orange")

        # ------------------
        self.transaction = self.add_video_window = None
        self.id_video = self.name = self.resolution = self.path = None
        self.name_label = self.name_input = None
        self.resolution_label = self.option = self.resolution_input = None
        self.file_label = self.path_input = None
        self.choose_file_button = self.add_video_output_label = None
        self.add_or_edit_video_button = None
        self.progress_bar = self.bar_style = None

    def configure(self):
        self.window.title('Biting Wire - Seu Programa de Streaming Favorito')
        self.window.configure(background='white')
        self.window.geometry(str(self.WIDTH) + "x" + str(self.HEIGHT))

        self.logo.pack(padx=(0, 40), pady=(0, 10))
        self.logo_panel.pack()
        self.logo_panel.configure(background='white')

        self.output_label.pack(padx=(0, 40))
        self.output_label.configure(background='white')

        self.style.theme_use("default")
        self.style.configure("Treeview", background="#D3D3D3", foreground="black",
                             rowheight=25, fieldbackground="#D3D3D3")
        self.style.map('Treeview', background=[('selected', '#785923')])

        self.table_frame.pack(side="top", padx=50, pady=10)
        self.table_frame.configure(background='white')
        self.table_scroll.pack(side=RIGHT, fill=Y)
        self.table_view.pack()
        self.table_scroll.config(command=self.table_view.yview)
        self.table_view['columns'] = ("ID", "Vídeo", "Qualidade", "Caminho")
        self.table_view.column("#0", width=0, stretch=NO)
        self.table_view.column("ID", anchor=CENTER, width=50)
        self.table_view.column("Vídeo", anchor=W, width=140)
        self.table_view.column("Qualidade", anchor=CENTER, width=100)
        self.table_view.column("Caminho", anchor=CENTER, width=250)
        self.table_view.heading("#0", text="", anchor=CENTER)
        self.table_view.heading("ID", text="ID", anchor=CENTER)
        self.table_view.heading("Vídeo", text="Vídeo", anchor=CENTER)
        self.table_view.heading("Qualidade", text="Qualidade", anchor=CENTER)
        self.table_view.heading("Caminho", text="Caminho", anchor=CENTER)
        self.table_view.tag_configure('oddrow', background="white")
        self.table_view.tag_configure('evenrow', background="orange")

        self.menu_frame.pack()
        self.menu_frame.configure(background='white')

        self.play_button.pack(side=LEFT, padx=10)
        self.add_video_button.pack(side=LEFT, padx=10)
        self.edit_video_button.pack(side=LEFT, padx=10)
        self.remove_video_button.pack(side=LEFT, padx=10)

    def render(self):
        self.configure()
        self.list_videos()
        self.window.mainloop()

    def list_videos(self):
        count = 0
        self.videos = read_videos_transaction_to_server()
        for video in self.videos:
            if count % 2 == 0:
                self.table_view.insert(parent='', index='end', iid=str(count), text="",
                                       values=(video[0], video[1], video[2], video[3]), tags=('evenrow',))
            else:
                self.table_view.insert(parent='', index='end', iid=str(count), text="",
                                       values=(video[0], video[1], video[2], video[3]), tags=('oddrow',))
            count += 1

    def refresh_list_videos(self):
        for video in self.table_view.get_children():
            self.table_view.delete(video)
        self.list_videos()

    def play_video(self):
        self.output_label.config(text='')
        selected = self.table_view.focus()
        if selected:
            id_video, name, resolution, path = self.table_view.item(selected, 'value')
            self.video_stream(name, resolution, path)
        else:
            self.output_label.config(text='Nenhum vídeo selecionado!', foreground='red')

    @staticmethod
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
                    video_cap.release()
                    cv2.destroyWindow('Frame')
                    break
            else:
                video_cap.release()
                cv2.destroyWindow('Frame')
                break

    def delete_video(self):
        self.output_label.config(text='')
        selected = self.table_view.focus()
        if selected:
            id_video, name, resolution, path = self.table_view.item(selected, 'value')
            os.remove(f'../videos/{resolution}/{name}')
            delete_video_transaction(id_video)
            self.refresh_list_videos()
        else:
            self.output_label.config(text='Nenhum vídeo selecionado!', foreground='red')

    def add_video(self):
        self.output_label.config(text='')
        self.initialize_add_video_window("CREATE")

    def update_video(self):
        self.output_label.config(text='')
        selected = self.table_view.focus()
        if selected:
            id_video, name, resolution, path = self.table_view.item(selected, 'value')
            self.initialize_add_video_window("UPDATE", id_video, name, resolution, path)
        else:
            self.output_label.config(text='Nenhum vídeo selecionado!', foreground='red')

    def initialize_add_video_window(self, transaction, id_video="", name="", resolution="", path=""):
        self.transaction = transaction
        self.add_video_window = Toplevel(self.window)

        self.id_video = id_video
        self.name = name
        self.resolution = resolution
        self.path = path

        self.name_label = Label(self.add_video_window, text="Nome do Vídeo: ")
        self.name_input = Entry(self.add_video_window, width=30)

        self.resolution_label = Label(self.add_video_window, text="Resolução: ")
        self.option = StringVar(self.add_video_window)
        self.resolution_input = OptionMenu(self.add_video_window, self.option, "240p", "480p", "720p")
        self.resolution_input.grid(sticky="W", row=1, column=1, pady=10, padx=10)

        self.file_label = Label(self.add_video_window, text="Arquivo: ")
        self.path_input = Entry(self.add_video_window, width=30)

        self.choose_file_button = Button(self.add_video_window, text='Escolher Arquivo',
                                         command=lambda: self.choose_file())
        self.add_video_output_label = Label(self.add_video_window, text="")

        self.add_or_edit_video_button = None

        self.progress_bar = Progressbar(self.add_video_window, orient=HORIZONTAL, length=300, mode='determinate',
                                        style='TProgressbar')
        self.bar_style = ttk.Style()
        self.configure_add_video_window()

    def configure_add_video_window(self):
        self.add_video_window.title('Adicionar Vídeo')
        self.add_video_window.geometry('400x220')
        self.add_video_window.configure(background='#b3b3b3')

        self.name_label.grid(row=0, column=0, pady=10, padx=10)
        self.name_label.configure(background='#b3b3b3')
        self.name_input.grid(row=0, column=1, columnspan=2, pady=10, padx=10)
        if self.transaction == "UPDATE":
            self.name_input.insert(0, self.name)

        self.resolution_label.grid(sticky="E", row=1, column=0, pady=10, padx=10)
        self.resolution_label.configure(background='#b3b3b3')
        self.resolution_input.grid(sticky="W", row=1, column=1, pady=10, padx=10)
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
        self.add_video_output_label.grid(row=4, columnspan=3, pady=10)
        self.add_video_output_label.configure(background='#b3b3b3')

        if self.transaction == "CREATE":
            button_text = 'Adicionar Vídeo'
            self.add_or_edit_video_button = Button(self.add_video_window, text=button_text,
                                                   command=lambda: self.save_video())
        elif self.transaction == "UPDATE":
            button_text = 'Atualizar Vídeo'
            self.add_or_edit_video_button = Button(self.add_video_window, text=button_text,
                                                   command=lambda: self.save_video())
        self.add_or_edit_video_button.grid(row=3, column=1, pady=5)
        self.bar_style.configure("TProgressbar", troughcolor='gray', background='green')

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
            self.add_video_output_label.config(text='Nome não pode ficar em branco!', foreground='red')
        elif self.path == ' Nenhum arquivo selecionado' or not self.path:
            self.add_video_output_label.config(text='Arquivo não pode ficar em branco!', foreground='red')
        elif not self.resolution:
            self.add_video_output_label.config(text='Resolução não pode ficar em branco!', foreground='red')
        else:
            self.add_video_output_label.config(text='Erro ao adicionar vídeo!', foreground='red')
        return False

    def save_video(self):
        old_name = self.name
        self.name = self.name_input.get()
        old_resolution = self.resolution
        self.resolution = self.option.get()
        old_path = self.path
        self.path = self.path_input.get()
        final_path = f'../videos/{self.resolution}/{self.name}'
        copyfile(self.path, final_path)

        if self.validates():
            self.progress_bar.grid(row=4, columnspan=3, pady=20)
            for i in range(5):
                self.add_video_window.update_idletasks()
                self.progress_bar['value'] += 20
                time.sleep(0.2)
            self.progress_bar.destroy()
            if self.transaction == "CREATE":
                create_video_transaction(self.name, self.resolution, final_path)
                self.add_video_output_label.config(text='Vídeo adicionado com sucesso!', foreground='green')
            elif self.transaction == "UPDATE" and self.id_video:
                if (self.name != old_name) or (self.resolution != old_resolution):
                    os.remove(old_path)
                update_videos_transaction(self.id_video, self.name, self.resolution, final_path)
                self.add_video_output_label.config(text='Vídeo atualizado com sucesso!', foreground='green')
            self.add_or_edit_video_button.destroy()
            quit_button = Button(self.add_video_window, text='Fechar', command=lambda: self.add_video_window.destroy())
            quit_button.grid(row=3, column=1, pady=5)
            self.refresh_list_videos()


def main():
    server_gui = ServerGUI()
    server_gui.render()


if __name__ == "__main__":
    main()
