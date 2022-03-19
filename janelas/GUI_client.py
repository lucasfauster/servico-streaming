from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk


class ClientGUI:

    def __init__(self, window, client):
        self.window = window
        self.client = client

        self.logo_frame = Frame(self.window)
        self.logo_frame.pack(pady=5)
        self.img = ImageTk.PhotoImage(Image.open("logo.png").resize((214, 120)))
        self.logo_panel = Label(self.logo_frame, image=self.img)
        self.logo_panel.pack()
        self.logo_panel.configure(background='white')

        self.output_label = Label(self.window, text="")
        self.output_label.pack(pady=(5, 0))
        self.output_label.configure(background='white')

        self.main_frame = Frame(self.window)
        self.main_frame.pack()
        self.main_frame.configure(background='white')

        self.style = ttk.Style()
        self.style.theme_use("default")
        self.style.configure("Treeview", background="#D3D3D3", foreground="black", rowheight=25, fieldbackground="#D3D3D3")
        self.style.map('Treeview', background=[('selected', '#785923')])

        # Tabela
        self.table_frame = Frame(self.main_frame)
        self.table_frame.pack(side=LEFT, padx=50, pady=10)
        self.table_frame.configure(background='white')
        self.table_scroll = Scrollbar(self.table_frame)
        self.table_scroll.pack(side=RIGHT, fill=Y)
        self.table_view = ttk.Treeview(self.table_frame, yscrollcommand=self.table_scroll.set, selectmode="browse")
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

        # Botões
        self.menu_frame = Frame(self.window)
        self.menu_frame.pack()
        self.menu_frame.configure(background='white')

        if self.client.is_premium():
            self.play_button = Button(self.menu_frame, text="Reproduzir Vídeo", width=12, height=2, bg="orange",
                                 command=lambda: self.play_video(self))
            self.play_button.pack(side=LEFT, padx=10)
            self.create_group_button = Button(self.menu_frame, text="Criar grupo", width=12, height=2, bg="orange",
                                         command=lambda: self.create_group(self))
            self.create_group_button.pack(side=LEFT, padx=10)

            self.check_group_button = Button(self.menu_frame, text="Checar grupos", width=12, height=2, bg="orange",
                                        command=lambda: self.check_group(self))
        else:
            self.check_group_button = Button(self.menu_frame, text="Checar grupos", width=12, height=2, bg="orange",
                                        command=lambda: self.check_group(self))
        self.check_group_button.pack(side=LEFT, padx=10)

        # videos = client.list_videos()
        # list_videos(videos, table_view)
        self.window.mainloop()



    def check_group(self):
        print('mon amour')

    def create_group(self):
        print('mon amour')

    def play_video(self):
        print('mon amour')

#
# def add_user_to_group(main, group_table_view, name_input, output_label, client):
#     name = name_input.get()
#     if name:
#         if client.add_to_group(name):
#             output_label.config(text=f'Usuário "{name}" adicionado ao grupo com sucesso!', foreground='green')
#         else:
#             output_label.config(text=f'Usuário "{name} não encontrado!', foreground='red')
#
#     else:
#         output_label.config(text='Nome não pode ficar em branco!', foreground='red')
#     group = client.get_group()
#     refresh_list_group(group, group_table_view)
#     main.destroy()
#
#
# def create_group(self.create_group_button, check_group_button, self.window, self.main_frame, self.menu_frame,
#                  table_view, output_label, client):
#     check_group_button.destroy()
#     output_label.config(text='')
#     self.create_group_button.destroy()
#     render_group_table(window, main_frame, menu_frame, table_view, output_label, client)
#     output_label.config(text='Grupo criado com sucesso!', foreground='green')
#
#
# def wait_for_video(output_label, client, invited_group_table_view):
#     output_label.config(text='')
#     client.get_in_group_room()
#     output_label.config(text='Vídeo terminado!', foreground='green')
#     if client.is_premium():
#         group = client.get_group()
#         refresh_list_group(group, invited_group_table_view)
#
#
# def check_group(check_group_button, output_label, client, main_frame, menu_frame, create_group_button=None,
#                 play_video_button=None):
#     output_label.config(text='')
#     invited_group_table_view = None
#     if client.has_group():
#         output_label.config(text='Você foi incluído(a) em um grupo!', foreground='green')
#         if play_video_button:
#             play_video_button.destroy()
#         if create_group_button:
#             create_group_button.destroy()
#         check_group_button.pack_forget()
#         if client.is_premium():
#             invited_group_table_frame = Frame(main_frame)
#             invited_group_table_frame.pack(side=LEFT, padx=50, pady=10)
#             invited_group_table_frame.configure(background='white')
#             invited_group_table_scroll = Scrollbar(invited_group_table_frame)
#             invited_group_table_scroll.pack(side=RIGHT, fill=Y)
#             invited_group_table_view = ttk.Treeview(invited_group_table_frame,
#                                                     yscrollcommand=invited_group_table_scroll.set, selectmode="browse")
#             invited_group_table_view.pack()
#             invited_group_table_scroll.config(command=invited_group_table_view.yview)
#             invited_group_table_view['columns'] = "Grupo"
#             invited_group_table_view.column("#0", width=0, stretch=NO)
#             invited_group_table_view.column("Grupo", anchor=W, width=140)
#             invited_group_table_view.heading("#0", text="", anchor=CENTER)
#             invited_group_table_view.heading("Grupo", text="Grupo", anchor=CENTER)
#             invited_group_table_view.tag_configure('oddrow', background="white")
#             invited_group_table_view.tag_configure('evenrow', background="orange")
#
#             group = client.get_group()
#             refresh_list_group(group, invited_group_table_view)
#
#         wait_for_video_button = Button(menu_frame, text="Aguardar video", width=12, height=2, bg="orange",
#                                        command=lambda: wait_for_video(output_label, client,
#                                                                                 invited_group_table_view))
#         wait_for_video_button.pack(side=LEFT, padx=10)
#     else:
#         output_label.config(text='Você ainda não foi incluído(a) em nenhum grupo', foreground='red')
#
#
# def add_user(window, group_table_view, output_label, client):
#     output_label.config(text='')
#     main = Toplevel(window)
#     main.title('Adicionar usuário ao grupo')
#     main.geometry('220x120')
#     main.configure(background='#b3b3b3')
#     name_label = Label(main, text="Nome do Usuário: ")
#     name_label.pack()
#     name_label.configure(background='#b3b3b3')
#     name_input = Entry(main, width=20)
#     name_input.pack()
#     add_user_button = Button(main, text="Adicionar", width=12, height=2,
#                              command=lambda: add_user_to_group(main, group_table_view, name_input, output_label,
#                                                                client), bg="orange")
#     add_user_button.pack(padx=10)
#
#
# def remove_user(group_table_view, output_label, client):
#     output_label.config(text='')
#     selected = group_table_view.focus()
#     group = client.get_group()
#     if selected:
#         user = group_table_view.item(selected, 'value')[0]
#         if user == group[-1]:
#             output_label.config(text=f'Você não pode remover a si mesmo(a)!', foreground='red')
#         else:
#             if client.remove_from_group(user):
#                 output_label.config(text=f'Usuário "{user}" foi removido(a) com sucesso!', foreground='green')
#             else:
#                 output_label.config(text=f'Usuário "{user}" não encontrado!', foreground='red')
#     else:
#         output_label.config(text='Nenhum usuário selecionado!', foreground='red')
#     group = client.get_group()
#     refresh_list_group(group, group_table_view)
#
#
# def play_video(table_view, output_label, client):
#     output_label.config(text='')
#     selected = table_view.focus()
#     if selected:
#         name, resolution = table_view.item(selected, 'value')
#         client.play_video(name, resolution)
#     else:
#         output_label.config(text='Nenhum vídeo selecionado!', foreground='red')
#
#
# def play_video_group(table_view, output_label, client):
#     output_label.config(text='')
#     selected = table_view.focus()
#     if selected:
#         name, resolution = table_view.item(selected, 'value')
#         client.play_video_to_group(name, resolution)
#     else:
#         output_label.config(text='Nenhum vídeo selecionado!', foreground='red')
#
#
# def render_group_table(window, main_frame, menu_frame, table_view, output_label, client):
#     group_table_frame = Frame(main_frame)
#     group_table_frame.pack(side=LEFT, padx=50, pady=10)
#     group_table_frame.configure(background='white')
#     group_table_scroll = Scrollbar(group_table_frame)
#     group_table_scroll.pack(side=RIGHT, fill=Y)
#     group_table_view = ttk.Treeview(group_table_frame, yscrollcommand=group_table_scroll.set, selectmode="browse")
#     group_table_view.pack()
#     group_table_scroll.config(command=group_table_view.yview)
#     group_table_view['columns'] = "Grupo"
#     group_table_view.column("#0", width=0, stretch=NO)
#     group_table_view.column("Grupo", anchor=W, width=140)
#     group_table_view.heading("#0", text="", anchor=CENTER)
#     group_table_view.heading("Grupo", text="Grupo", anchor=CENTER)
#     group_table_view.tag_configure('oddrow', background="white")
#     group_table_view.tag_configure('evenrow', background="orange")
#
#     client.create_group()
#
#     play_group_button = Button(menu_frame, text="Reproduzir para o grupo", width=20, height=2, bg="orange",
#                                command=lambda: play_video_group(table_view, output_label, client))
#     play_group_button.pack(side=LEFT, padx=5)
#
#     add_user_button = Button(menu_frame, text="Adicionar usuário ao grupo", width=20, height=2, bg="orange",
#                              command=lambda: add_user(window, group_table_view, output_label, client))
#     add_user_button.pack(side=LEFT, padx=5)
#
#     remove_user_button = Button(menu_frame, text="Remover usuário do grupo", width=20, height=2, bg="orange",
#                                 command=lambda: remove_user(group_table_view, output_label, client))
#     remove_user_button.pack()
#
#     group = client.get_group()
#     list_group(group, group_table_view)
#
#
# def list_group(group, group_table_view):
#     count = 0
#     for user in group:
#         if count % 2 == 0:
#             group_table_view.insert(parent='', index='end', iid=count, text="", values=user, tags=('evenrow',))
#         else:
#             group_table_view.insert(parent='', index='end', iid=count, text="", values=user, tags=('oddrow',))
#         count += 1
#
#
# def refresh_list_group(group, group_table_view):
#     for user in group_table_view.get_children():
#         group_table_view.delete(user)
#     list_group(group, group_table_view)
#
#
# def list_videos(videos, table_view):
#     count = 0
#     for video in videos:
#         if count % 2 == 0:
#             table_view.insert(parent='', index='end', iid=count, text="", values=(video[0], video[1]),
#                               tags=('evenrow',))
#         else:
#             table_view.insert(parent='', index='end', iid=count, text="", values=(video[0], video[1]), tags=('oddrow',))
#         count += 1
#
#


def render_client_gui(window, client, client_type):
    client_gui = ClientGUI(window, client)
    # Depois que a janela é fechada, volta para login para que ele efetue o log out
    return
