from GUI_client import *
from client.client import Client


class LoginGUI:
    WIDTH = 350
    HEIGHT = 500
    LOGO = "logo.png"
    USER_TYPE = {1: "convidado", 2: "premium"}

    def __init__(self):
        self.client = Client()
        self.window = Tk()

        self.login_frame = Frame(self.window)
        self.logo = Frame(self.login_frame)
        self.img = ImageTk.PhotoImage(Image.open(self.LOGO).resize((214, 120)))
        self.logo_label = Label(self.logo, image=self.img)

        self.name_frame = Frame(self.login_frame)
        self.name_label = Label(self.name_frame, text="Nome")
        self.name_input = Entry(self.name_frame, width=25, font="Helvetica 12 bold")

        self.type_frame = Frame(self.login_frame)
        self.option_input = IntVar()
        self.radio_button1 = Radiobutton(self.type_frame, text="Convidado", variable=self.option_input,
                                         value=1, selectcolor='#dedede')
        self.radio_button2 = Radiobutton(self.type_frame, text="Premium", variable=self.option_input,
                                         value=2, selectcolor='#dedede')

        self.menu_frame = Frame(self.login_frame)
        self.output_label = Label(self.menu_frame, text="")
        self.login_button = Button(self.menu_frame, text="Entrar", width=12, height=2, bg="orange", command=self.login)

    def configure(self):
        self.window.title('Biting Wire - Login')
        self.window.configure(background='white')
        self.window.geometry(str(self.WIDTH) + "x" + str(self.HEIGHT))

        self.login_frame.pack()
        self.login_frame.configure(background='white')

        self.logo.pack(ipadx=200, pady=(50, 0))
        self.logo.configure(background='white')
        self.logo_label.pack()
        self.logo_label.configure(background='white')

        self.name_frame.pack(pady=30)
        self.name_frame.configure(background='white')
        self.name_label.pack(padx=(0, 160), pady=(10, 0))
        self.name_label.configure(background='white')
        self.name_input.pack(ipady=7)
        self.name_input.configure(background='grey')

        self.type_frame.pack(pady=10)
        self.type_frame.configure(background='white')
        self.option_input.set(1)
        self.radio_button1.configure(background='white', highlightthickness=0)
        self.radio_button2.configure(background='white', highlightthickness=0)
        self.radio_button1.pack(side=LEFT, padx=10)
        self.radio_button2.pack(padx=10)

        self.menu_frame.pack()
        self.menu_frame.configure(background='white')

        self.output_label.pack(pady=(0, 10))
        self.output_label.configure(background='white')

        self.login_button.pack()

    def login(self):
        name = self.name_input.get()
        option = self.option_input.get()

        if not name:
            self.output_label.config(text='Nome não pode ficar em branco!', foreground='red')
        else:
            self.client.login(name, self.USER_TYPE.get(option))
            self.window.title('Biting Wire - Seu Programa de Streaming Favorito')
            self.window.geometry("750x510")
            self.login_frame.destroy()
            render_client_gui(self.window, self.client, self.USER_TYPE.get(option))
            self.client.log_out()

    def render(self):
        self.configure()
        self.window.mainloop()


def main():
    login_gui = LoginGUI()
    login_gui.render()


if __name__ == "__main__":
    main()
