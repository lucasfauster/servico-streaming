from GUI_client import *
from client.client import Client


def login():
    name = name_input.get()
    option = option_input.get()
    print(option)
    user_type = {1: "convidado", 2: "premium"}
    if not name:
        output_label.config(text='Nome não pode ficar em branco!', foreground='red')
    else:
        client = Client()
        client.login(name, user_type.get(option))
        window.title('Biting Wire - Seu Programa de Streaming Favorito')
        window.geometry("750x510")
        login_frame.destroy()
        render_client_gui(window, client)


# #  Janela
window = Tk()
window.title('Biting Wire - Login')
window.configure(background='white')
width, height = 350, 500
window.geometry(str(width) + "x" + str(height))

login_frame = Frame(window)
login_frame.pack()
login_frame.configure(background='white')

# Logo
logo = Frame(login_frame)
logo.pack(ipadx=200, pady=(50, 0))
logo.configure(background='white')
img = ImageTk.PhotoImage(Image.open("logo.png").resize((214, 120)))
logo_panel = Label(logo, image=img)
logo_panel.pack()
logo_panel.configure(background='white')

name_frame = Frame(login_frame)
name_frame.pack(pady=30)
name_frame.configure(background='white')
name_label = Label(name_frame, text="Nome")
name_label.pack(padx=(0, 160), pady=(10, 0))
name_label.configure(background='white')
name_input = Entry(name_frame, width=25, font="Helvetica 12 bold")
name_input.pack(ipady=7)
name_input.configure(background='grey')

type_frame = Frame(login_frame)
type_frame.pack(pady=10)
type_frame.configure(background='white')
option_input = IntVar()
option_input.set(1)
radio_button1 = Radiobutton(type_frame, text="Convidado", variable=option_input, value=1, selectcolor='#dedede')
radio_button1.configure(background='white', highlightthickness=0)
radio_button2 = Radiobutton(type_frame, text="Premium", variable=option_input, value=2, selectcolor='#dedede')
radio_button2.configure(background='white', highlightthickness=0)
radio_button1.pack(side=LEFT, padx=10)
radio_button2.pack(padx=10)

menu_frame = Frame(login_frame)
menu_frame.pack()
menu_frame.configure(background='white')
output_label = Label(menu_frame, text="")
output_label.pack(pady=(0, 10))
output_label.configure(background='white')
login_button = Button(menu_frame, text="Entrar", width=12, height=2, bg="orange", command=login)
login_button.pack()

window.mainloop()
