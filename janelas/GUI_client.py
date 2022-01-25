from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk


def add_user_to_group(main, group_table_view, name_input, output_label, client):
    name = name_input.get()
    if name:
        if client.add_to_group(name):
            output_label.config(text=f'Usuário "{name}" adicionado ao grupo com sucesso!', foreground='green')
        else:
            output_label.config(text=f'Usuário "{name} não encontrado!', foreground='red')

    else:
        output_label.config(text='Nome não pode ficar em branco!', foreground='red')
    group = client.get_group()
    refresh_list_group(group, group_table_view)
    main.destroy()


def create_group(create_group_button, window, main_frame, menu_frame, table_view, output_label, client):
    output_label.config(text='')
    create_group_button.destroy()
    render_group_table(window, main_frame, menu_frame, table_view, output_label, client)
    output_label.config(text='Grupo criado com sucesso!', foreground='green')


# # Quando receber inclusão no grupo via socket chamar essa função
def was_added_group(create_group_button, output_label):
    create_group_button.destroy()
    output_label.config(text='Você foi incluído(a) em um grupo! Aguarde a reprodução do vídeo começar.', foreground='green')


def add_user(window, group_table_view, output_label, client):
    output_label.config(text='')
    main = Toplevel(window)
    main.title('Adicionar usuário ao grupo')
    main.geometry('220x120')
    main.configure(background='#b3b3b3')
    name_label = Label(main, text="Nome do Usuário: ")
    name_label.pack()
    name_label.configure(background='#b3b3b3')
    name_input = Entry(main, width=20)
    name_input.pack()
    add_user_button = Button(main, text="Adicionar", width=12, height=2,
                             command=lambda: add_user_to_group(main, group_table_view, name_input, output_label, client), bg="orange")
    add_user_button.pack(padx=10)


def remove_user(group_table_view, output_label, client):
    output_label.config(text='')
    selected = group_table_view.focus()
    if selected:
        user = group_table_view.item(selected, 'value')[0]
        if client.remove_from_group(user):
            output_label.config(text=f'Usuário "{user}" foi removido(a) com sucesso!', foreground='green')
        else:
            output_label.config(text=f'Usuário "{user}" não encontrado!', foreground='red')
    else:
        output_label.config(text='Nenhum usuário selecionado!', foreground='red')
    group = client.get_group()
    refresh_list_group(group, group_table_view)


def play_video(table_view, output_label, client):
    output_label.config(text='')
    selected = table_view.focus()
    if selected:
        name, resolution = table_view.item(selected, 'value')
        client.play_video(name, resolution)
    else:
        output_label.config(text='Nenhum vídeo selecionado!', foreground='red')


def play_video_group(table_view, output_label, client):
    output_label.config(text='')
    selected = table_view.focus()
    if selected:
        name, resolution = table_view.item(selected, 'value')
        client.play_video_to_group(name, resolution)
    else:
        output_label.config(text='Nenhum vídeo selecionado!', foreground='red')


def render_group_table(window, main_frame, menu_frame, table_view, output_label, client):
    group_table_frame = Frame(main_frame)
    group_table_frame.pack(side=LEFT, padx=50, pady=10)
    group_table_frame.configure(background='white')
    group_table_scroll = Scrollbar(group_table_frame)
    group_table_scroll.pack(side=RIGHT, fill=Y)
    group_table_view = ttk.Treeview(group_table_frame, yscrollcommand=group_table_scroll.set, selectmode="browse")
    group_table_view.pack()
    group_table_scroll.config(command=group_table_view.yview)
    group_table_view['columns'] = "Grupo"
    group_table_view.column("#0", width=0, stretch=NO)
    group_table_view.column("Grupo", anchor=W, width=140)
    group_table_view.heading("#0", text="", anchor=CENTER)
    group_table_view.heading("Grupo", text="Grupo", anchor=CENTER)
    group_table_view.tag_configure('oddrow', background="white")
    group_table_view.tag_configure('evenrow', background="orange")

    client.create_group()

    play_group_button = Button(menu_frame, text="Reproduzir para o grupo", width=20, height=2, bg="orange",
                               command=lambda: play_video_group(table_view, output_label, client))
    play_group_button.pack(side=LEFT, padx=5)

    add_user_button = Button(menu_frame, text="Adicionar usuário ao grupo", width=20, height=2, bg="orange",
                             command=lambda: add_user(window, group_table_view, output_label, client))
    add_user_button.pack(side=LEFT, padx=5)

    remove_user_button = Button(menu_frame, text="Remover usuário do grupo", width=20, height=2, bg="orange",
                                command=lambda: remove_user(group_table_view, output_label, client))
    remove_user_button.pack()

    group = client.get_group()
    list_group(group, group_table_view)


def list_group(group, group_table_view):
    count = 0
    for user in group:
        if count % 2 == 0:
            group_table_view.insert(parent='', index='end', iid=count, text="", values=user, tags=('evenrow',))
        else:
            group_table_view.insert(parent='', index='end', iid=count, text="", values=user, tags=('oddrow',))
        count += 1


def refresh_list_group(group, group_table_view):
    for user in group_table_view.get_children():
        group_table_view.delete(user)
    list_group(group, group_table_view)


def list_videos(videos, table_view):
    count = 0
    for video in videos:
        if count % 2 == 0:
            table_view.insert(parent='', index='end', iid=count, text="", values=(video[0], video[1]), tags=('evenrow',))
        else:
            table_view.insert(parent='', index='end', iid=count, text="", values=(video[0], video[1]), tags=('oddrow',))
        count += 1


def render_client_gui(window, client):
    # Logo
    logo_frame = Frame(window)
    logo_frame.pack(pady=5)
    img = ImageTk.PhotoImage(Image.open("logo.png").resize((214, 120)))
    logo_panel = Label(logo_frame, image=img)
    logo_panel.pack()
    logo_panel.configure(background='white')

    output_label = Label(window, text="")
    output_label.pack(pady=(5, 0))
    output_label.configure(background='white')

    main_frame = Frame(window)
    main_frame.pack()
    main_frame.configure(background='white')

    style = ttk.Style()
    style.theme_use("default")
    style.configure("Treeview", background="#D3D3D3", foreground="black", rowheight=25, fieldbackground="#D3D3D3")
    style.map('Treeview', background=[('selected', '#785923')])

    # Tabela
    style = ttk.Style()
    tabela_frame = Frame(main_frame)
    tabela_frame.pack(side=LEFT, padx=50, pady=10)
    tabela_frame.configure(background='white')
    tabela_scroll = Scrollbar(tabela_frame)
    tabela_scroll.pack(side=RIGHT, fill=Y)
    table_view = ttk.Treeview(tabela_frame, yscrollcommand=tabela_scroll.set, selectmode="browse")
    table_view.pack()
    tabela_scroll.config(command=table_view.yview)
    table_view['columns'] = ("Vídeo", "Qualidade")
    table_view.column("#0", width=0, stretch=NO)
    table_view.column("Vídeo", anchor=W, width=140)
    table_view.column("Qualidade", anchor=CENTER, width=150)
    table_view.heading("#0", text="", anchor=CENTER)
    table_view.heading("Vídeo", text="Vídeo", anchor=CENTER)
    table_view.heading("Qualidade", text="Qualidade", anchor=CENTER)
    table_view.tag_configure('oddrow', background="white")
    table_view.tag_configure('evenrow', background="orange")

    # Botões
    menu_frame = Frame(window)
    menu_frame.pack()
    menu_frame.configure(background='white')
    play_button = Button(menu_frame, text="Reproduzir Vídeo", width=12, height=2, bg="orange",
                         command=lambda: play_video(table_view, output_label, client))
    play_button.pack(side=LEFT, padx=10)
    create_group_button = Button(menu_frame, text="Criar grupo", width=12, height=2, bg="orange",
                                 command=lambda: create_group(create_group_button, window, main_frame, menu_frame,
                                                              table_view, output_label, client))
    create_group_button.pack(side=LEFT, padx=10)

    videos = client.list_videos()
    list_videos(videos, table_view)
    window.mainloop()
