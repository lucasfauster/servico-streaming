from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk


class ClientGUI:
    def __init__(self, window, client):
        self.window = window
        self.client = client

        self.logo_frame = Frame(self.window)
        self.img = ImageTk.PhotoImage(Image.open("logo.png").resize((214, 120)))
        self.logo_panel = Label(self.logo_frame, image=self.img)

        self.output_label = Label(self.window, text="")
        self.main_frame = Frame(self.window)

        self.style = ttk.Style()
        self.table_frame = Frame(self.main_frame)
        self.table_scroll = Scrollbar(self.table_frame)

        self.table_view = ttk.Treeview(self.table_frame, yscrollcommand=self.table_scroll.set, selectmode="browse")

        self.menu_frame = Frame(self.window)
        self.play_button = Button(self.menu_frame, text="Reproduzir Vídeo", width=12, height=2, bg="orange",
                                  command=lambda: self.play_video())
        self.create_group_button = Button(self.menu_frame, text="Criar grupo", width=12, height=2, bg="orange",
                                          command=lambda: self.create_group())
        self.check_group_button = Button(self.menu_frame, text="Checar grupos", width=12, height=2, bg="orange",
                                         command=lambda: self.check_group())
        self.videos = self.client.list_videos()

        self.group = None
        self.group_table_frame = None
        self.group_table_scroll = None
        self.group_table_view = None
        self.play_group_button = None
        self.add_user_button = None
        self.remove_user_button = None
        self.invited_group_table_view = None
        self.invited_group_table_frame = None
        self.invited_group_table_scroll = None
        self.wait_for_video_button = None
        self.play_video_button = None
        self.main = None
        self.name_input = None

    def configure(self):
        self.logo_frame.pack(pady=5)

        self.logo_panel.pack()
        self.logo_panel.configure(background='white')

        self.output_label.pack(pady=(5, 0))
        self.output_label.configure(background='white')

        self.main_frame.pack()
        self.main_frame.configure(background='white')

        self.style.theme_use("default")
        self.style.configure("Treeview", background="#D3D3D3", foreground="black",
                             rowheight=25, fieldbackground="#D3D3D3")
        self.style.map('Treeview', background=[('selected', '#785923')])

        self.table_frame.pack(side=LEFT, padx=50, pady=10)
        self.table_frame.configure(background='white')

        self.table_scroll.pack(side=RIGHT, fill=Y)
        self.table_view.pack()
        self.table_scroll.config(command=self.table_view.yview)
        self.table_view['columns'] = ("Vídeo", "Qualidade")
        self.table_view.column("#0", width=0, stretch=NO)
        self.table_view.column("Vídeo", anchor=W, width=140)
        self.table_view.column("Qualidade", anchor=CENTER, width=150)
        self.table_view.heading("#0", text="", anchor=CENTER)
        self.table_view.heading("Vídeo", text="Vídeo", anchor=CENTER)
        self.table_view.heading("Qualidade", text="Qualidade", anchor=CENTER)
        self.table_view.tag_configure('oddrow', background="white")
        self.table_view.tag_configure('evenrow', background="orange")

        self.menu_frame.pack()
        self.menu_frame.configure(background='white')

        if self.client.is_premium():
            self.play_button.pack(side=LEFT, padx=10)
            self.create_group_button.pack(side=LEFT, padx=10)
        self.check_group_button.pack(side=LEFT, padx=10)

        self.list_videos()

    def list_videos(self):
        count = 0
        for video in self.videos:
            if count % 2 == 0:
                self.table_view.insert(parent='', index='end', iid=str(count), text="", values=(video[0], video[1]),
                                       tags=('evenrow',))
            else:
                self.table_view.insert(parent='', index='end', iid=str(count), text="", values=(video[0], video[1]),
                                       tags=('oddrow',))
            count += 1

    def play_video(self):
        self.output_label.config(text='')
        selected = self.table_view.focus()
        if selected:
            name, resolution = self.table_view.item(selected, 'value')
            self.client.play_video(name, resolution)
        else:
            self.output_label.config(text='Nenhum vídeo selecionado!', foreground='red')

    def play_video_group(self):
        self.output_label.config(text='')
        selected = self.table_view.focus()
        if selected:
            name, resolution = self.table_view.item(selected, 'value')
            self.client.play_video_to_group(name, resolution)
        else:
            self.output_label.config(text='Nenhum vídeo selecionado!', foreground='red')

    def list_group(self, table_view):
        count = 0
        for user in self.group:
            if count % 2 == 0:
                table_view.insert(parent='', index='end', iid=count, text="", values=user, tags=('evenrow',))
            else:
                table_view.insert(parent='', index='end', iid=count, text="", values=user, tags=('oddrow',))
            count += 1

    def refresh_list_group(self, table_view):
        for user in table_view.get_children():
            table_view.delete(user)
        self.list_group(table_view)

    def create_group(self):
        self.check_group_button.destroy()
        self.output_label.config(text='')
        self.create_group_button.destroy()
        self.render_group_table()
        self.output_label.config(text='Grupo criado com sucesso!', foreground='green')

    def check_group(self):
        self.output_label.config(text='')
        if self.client.has_group():
            self.output_label.config(text='Você foi incluído(a) em um grupo!', foreground='green')
            if self.play_video_button:
                self.play_video_button.destroy()
            if self.create_group_button:
                self.create_group_button.destroy()
            self.check_group_button.pack_forget()
            if self.client.is_premium():
                self.render_invited_group_table()
                self.group = self.client.get_group()
                self.refresh_list_group(self.invited_group_table_view)
            self.wait_for_video_button = Button(self.menu_frame, text="Aguardar video", width=12, height=2, bg="orange",
                                                command=lambda: self.wait_for_video())
            self.wait_for_video_button.pack(side=LEFT, padx=10)
        else:
            self.output_label.config(text='Você ainda não foi incluído(a) em nenhum grupo', foreground='red')

    def add_user(self):
        self.output_label.config(text='')
        self.main = Toplevel(self.window)
        self.main.title('Adicionar usuário ao grupo')
        self.main.geometry('220x120')
        self.main.configure(background='#b3b3b3')
        name_label = Label(self.main, text="Nome do Usuário: ")
        name_label.pack()
        name_label.configure(background='#b3b3b3')
        self.name_input = Entry(self.main, width=20)
        self.name_input.pack()
        add_user_button = Button(self.main, text="Adicionar", width=12, height=2, bg="orange",
                                 command=lambda: self.add_user_to_group())
        add_user_button.pack(padx=10)

    def add_user_to_group(self):
        name = self.name_input.get()
        if name:
            if self.client.add_to_group(name):
                self.output_label.config(text=f'Usuário "{name}" adicionado ao grupo com sucesso!', foreground='green')
            else:
                self.output_label.config(text=f'Usuário "{name} não encontrado!', foreground='red')

        else:
            self.output_label.config(text='Nome não pode ficar em branco!', foreground='red')
        self.group = self.client.get_group()
        self.refresh_list_group(self.group_table_view)
        self.main.destroy()

    def remove_user(self):
        self.output_label.config(text='')
        selected = self.group_table_view.focus()
        self.group = self.client.get_group()
        if selected:
            user = self.group_table_view.item(selected, 'value')[0]
            if user == self.group[-1]:
                self.output_label.config(text=f'Você não pode remover a si mesmo(a)!', foreground='red')
            else:
                if self.client.remove_from_group(user):
                    self.output_label.config(text=f'Usuário "{user}" foi removido(a) com sucesso!', foreground='green')
                else:
                    self.output_label.config(text=f'Usuário "{user}" não encontrado!', foreground='red')
        else:
            self.output_label.config(text='Nenhum usuário selecionado!', foreground='red')
        self.group = self.client.get_group()
        self.refresh_list_group(self.group_table_view)

    def wait_for_video(self):
        self.output_label.config(text='')
        self.client.get_in_group_room()
        self.output_label.config(text='Vídeo terminado!', foreground='green')
        if self.client.is_premium():
            self.group = self.client.get_group()
            self.refresh_list_group(self.invited_group_table_view)

    def initialize_group_table(self):
        self.group_table_frame = Frame(self.main_frame)
        self.group_table_scroll = Scrollbar(self.group_table_frame)
        self.group_table_view = ttk.Treeview(self.group_table_frame,
                                             yscrollcommand=self.group_table_scroll.set, selectmode="browse")
        self.play_group_button = Button(self.menu_frame, text="Reproduzir para o grupo", width=20, height=2,
                                        bg="orange", command=lambda: self.play_video_group())
        self.add_user_button = Button(self.menu_frame, text="Adicionar usuário ao grupo", width=20, height=2,
                                      bg="orange", command=lambda: self.add_user())
        self.remove_user_button = Button(self.menu_frame, text="Remover usuário do grupo", width=20, height=2,
                                         bg="orange", command=lambda: self.remove_user())

    def configure_group_table(self):
        self.group_table_frame.pack(side=LEFT, padx=50, pady=10)
        self.group_table_frame.configure(background='white')
        self.group_table_scroll.pack(side=RIGHT, fill=Y)

        self.group_table_view.pack()
        self.group_table_scroll.config(command=self.group_table_view.yview)
        self.group_table_view['columns'] = "Grupo"
        self.group_table_view.column("#0", width=0, stretch=NO)
        self.group_table_view.column("Grupo", anchor=W, width=140)
        self.group_table_view.heading("#0", text="", anchor=CENTER)
        self.group_table_view.heading("Grupo", text="Grupo", anchor=CENTER)
        self.group_table_view.tag_configure('oddrow', background="white")
        self.group_table_view.tag_configure('evenrow', background="orange")

        self.client.create_group()

        self.play_group_button.pack(side=LEFT, padx=5)
        self.add_user_button.pack(side=LEFT, padx=5)
        self.remove_user_button.pack()

        self.group = self.client.get_group()
        self.list_group(self.group_table_view)

    def render_group_table(self):
        self.initialize_group_table()
        self.configure_group_table()

    def render_invited_group_table(self):
        self.invited_group_table_frame = Frame(self.main_frame)
        self.invited_group_table_frame.pack(side=LEFT, padx=50, pady=10)
        self.invited_group_table_frame.configure(background='white')
        self.invited_group_table_scroll = Scrollbar(self.invited_group_table_frame)
        self.invited_group_table_scroll.pack(side=RIGHT, fill=Y)
        self.invited_group_table_view = ttk.Treeview(self.invited_group_table_frame, selectmode="browse",
                                                     yscrollcommand=self.invited_group_table_scroll.set)
        self.invited_group_table_view.pack()
        self.invited_group_table_scroll.config(command=self.invited_group_table_view.yview)
        self.invited_group_table_view['columns'] = "Grupo"
        self.invited_group_table_view.column("#0", width=0, stretch=NO)
        self.invited_group_table_view.column("Grupo", anchor=W, width=140)
        self.invited_group_table_view.heading("#0", text="", anchor=CENTER)
        self.invited_group_table_view.heading("Grupo", text="Grupo", anchor=CENTER)
        self.invited_group_table_view.tag_configure('oddrow', background="white")
        self.invited_group_table_view.tag_configure('evenrow', background="orange")

    def render(self):
        self.configure()
        self.window.mainloop()
