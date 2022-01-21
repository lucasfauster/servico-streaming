from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
from db.video_transactions import *

group = 1
owner =True

def clicker(e):
    table_view.focus()

def list_group():
    count = 0
    videos = read_videos_transaction()
    for video in videos:
        if count % 2 == 0:
            group_table_view.insert(parent='', index='end', iid=count, text="",
                              values=(video[1], video[2]), tags=('evenrow',))
        else:
            group_table_view.insert(parent='', index='end', iid=count, text="",
                              values=(video[1], video[2]), tags=('oddrow',))
        count += 1

def list_videos():
    count = 0
    videos = read_videos_transaction()
    for video in videos:
        if count % 2 == 0:
            table_view.insert(parent='', index='end', iid=count, text="",
                               values=(video[1], video[2]), tags=('evenrow',))
        else:
            table_view.insert(parent='', index='end', iid=count, text="",
                               values=(video[1], video[2]), tags=('oddrow',))
        count += 1

# #  Janela
janela = Tk()
janela.title('Biting Wire - Seu Programa de Streaming Favorito')
janela.configure(background='white')
width, height = 800, 500
janela.geometry(str(width) + "x" + str(height))

# Logo
logo = Frame(janela)
logo.pack( pady=5)
img = ImageTk.PhotoImage(Image.open("logo.png").resize((214, 120)))
logo_panel = Label(logo, image=img)
logo_panel.pack()
logo_panel.configure(background='white')

main_frame = Frame(janela)
main_frame.pack()
main_frame.configure(background='white')

style = ttk.Style()
style.theme_use("default")
style.configure("Treeview", background="#D3D3D3", foreground="black", rowheight=25, fieldbackground="#D3D3D3")
style.map('Treeview', background=[('selected', '#785923')])

# Tabela
style = ttk.Style()
tabela_frame = Frame(main_frame)
tabela_frame.pack(side=LEFT, padx=50, pady=20)
tabela_frame.configure(background='white')
tabela_scroll = Scrollbar(tabela_frame)
tabela_scroll.pack(side=RIGHT, fill=Y)
table_view = ttk.Treeview(tabela_frame, yscrollcommand=tabela_scroll.set, selectmode="browse")
table_view.pack()
tabela_scroll.config(command=table_view.yview)
table_view['columns'] = ("Vídeo", "Qualidade")
table_view.column("#0", width=0, stretch=NO)
table_view.column("Vídeo", anchor=W, width=140)
table_view.column("Qualidade", anchor=CENTER, width=100)
table_view.heading("#0", text="", anchor=CENTER)
table_view.heading("Vídeo", text="Vídeo", anchor=CENTER)
table_view.heading("Qualidade", text="Qualidade", anchor=CENTER)
table_view.tag_configure('oddrow', background="white")
table_view.tag_configure('evenrow', background="orange")


group_table_frame = Frame(main_frame)
group_table_frame.pack(side=LEFT, padx=50, pady=20)
group_table_frame.configure(background='white')
group_table_scroll = Scrollbar(group_table_frame)
group_table_scroll.pack(side=RIGHT, fill=Y)
group_table_view = ttk.Treeview(group_table_frame, yscrollcommand=group_table_scroll.set, selectmode="browse")
group_table_view.pack()
group_table_scroll.config(command=group_table_view.yview)
group_table_view['columns'] = ("Grupo", "Tipo")
group_table_view.column("#0", width=0, stretch=NO)
group_table_view.column("Grupo", anchor=W, width=140)
group_table_view.column("Tipo", anchor=CENTER, width=100)
group_table_view.heading("#0", text="", anchor=CENTER)
group_table_view.heading("Grupo", text="Grupo", anchor=CENTER)
group_table_view.tag_configure('oddrow', background="white")
group_table_view.tag_configure('evenrow', background="orange")


# Botões
menu_frame = Frame(janela)
menu_frame.pack()
menu_frame.configure(background='white')
play_button = Button(menu_frame, text="Reproduzir Vídeo", width=12, height=2, bg="orange")
play_button.pack(side=LEFT, padx=10)
if not group:
    create_group_button = Button(menu_frame, text="Criar grupo", width=12, height=2, bg="orange")
    create_group_button.pack(side=LEFT, padx=10)
elif group and not owner:
    leave_group_button = Button(menu_frame, text="Sair do grupo", width=12, height=2,bg="orange")
    leave_group_button.pack(side=LEFT, padx=10)
elif group and owner:
    play_group_button = Button(menu_frame, text="Reproduzir para o grupo", width=20, height=2, bg="orange")
    play_group_button.pack(side=LEFT, padx=5)
    add_user_button = Button(menu_frame, text="Adicionar usuário ao grupo", width=20, height=2, bg="orange")
    add_user_button.pack(side=LEFT, padx=5)
    remove_user_button = Button(menu_frame, text="Remover usuário do grupo", width=20, height=2,bg="orange")
    remove_user_button.pack(side=LEFT, padx=5)

table_view.bind("<ButtonRelease-1>", clicker)

list_videos()
list_group()
janela.mainloop()
