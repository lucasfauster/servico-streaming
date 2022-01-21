from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk

def login():
    name = name_input.get()
    password = password_input.get()
    if not name:
        output_label.config(text='Nome não pode ficar em branco!', foreground='red')
    elif not password:
        output_label.config(text='Senha não pode ficar em branco!', foreground='red')
    else:
        check_login()


# #  Janela
janela = Tk()
janela.title('Biting Wire - Login')
janela.configure(background='white')
width, height = 400, 500
janela.geometry(str(width) + "x" + str(height))

# Logo
logo = Frame(janela)
logo.pack(ipadx=200, pady=(50, 0))
logo.configure(background='white')
img = ImageTk.PhotoImage(Image.open("logo.png").resize((214, 120)))
logo_panel = Label(logo, image=img)
logo_panel.pack()
logo_panel.configure(background='white')

input_frame = Frame(janela)
input_frame.pack(pady=40)
input_frame.configure(background='white')

name_label = Label(input_frame, text="Nome")
name_label.pack(padx=(0, 160), pady=(10, 0))
name_label.configure(background='white')
name_input = Entry(input_frame, width=25, font="Helvetica 12 bold")
name_input.pack(ipady=7)
name_input.configure(background='grey')

password_label = Label(input_frame, text="Senha")
password_label.pack(padx=(0, 140), pady=(10, 0))
password_label.configure(background='white')
password_input = Entry(input_frame,  show="*", width=25, font="Helvetica 12 bold")
password_input.pack(ipady=7)
password_input.configure(background='grey')

menu_frame = Frame(janela)
menu_frame.pack()
menu_frame.configure(background='white')
output_label = Label(menu_frame, text="")
output_label.pack(pady=(0, 10))
output_label.configure(background='white')
login_button = Button(menu_frame, text="Entrar", width=12, height=2, bg="orange", command=login)
login_button.pack(side=LEFT, padx=10)
signin_video_button = Button(menu_frame, text="Cadastrar-se", width=12, height=2, bg="orange")
signin_video_button.pack(side=LEFT, padx=10)

janela.mainloop()
