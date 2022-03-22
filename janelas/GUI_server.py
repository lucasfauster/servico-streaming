from GUI_video import *
from PIL import Image, ImageTk
import cv2
import imutils
import os


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

    def configure(self):
        self.window.title('Biting Wire - Seu Programa de Streaming Favorito')
        self.window.configure(background='white')
        self.window.geometry(str(self.WIDTH) + "x" + str(self.HEIGHT))
        
        self.logo.pack(padx=(0, 70), pady=5)
        self.logo_panel.pack()
        self.logo_panel.configure(background='white')

        self.style.theme_use("default")
        self.style.configure("Treeview", background="#D3D3D3", foreground="black", 
                             rowheight=25, fieldbackground="#D3D3D3")
        self.style.map('Treeview', background=[('selected', '#785923')])

        self.table_frame.pack(side="top", padx=50, pady=20)
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
        selected = self.table_view.focus()
        if selected:
            id_video, name, resolution, path = self.table_view.item(selected, 'value')
            self.video_stream(name, resolution, path)
        else:
            print("Nenhum vídeo selecionado")

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
                    print("VÍDEO FECHADO")
                    video_cap.release()
                    cv2.destroyWindow('Frame')
                    break
            else:
                print("VIDEO TERMINOU!")
                video_cap.release()
                cv2.destroyWindow('Frame')
                break

    def delete_video(self):
        selected = self.table_view.focus()
        if selected:
            id_video, name, resolution, path = self.table_view.item(selected, 'value')
            os.remove(f'../videos/{resolution}/{name}')
            delete_video_transaction(id_video)
            self.refresh_list_videos()
        else:
            print("Nenhum vídeo selecionado")

    def add_video(self):
        add_video_gui = AddVideoGUI(self.window, "CREATE")
        add_video_gui.render()
        self.refresh_list_videos()

    def update_video(self):
        selected = self.table_view.focus()
        if selected:
            id_video, name, resolution, path = self.table_view.item(selected, 'value')
            os.remove(f'../videos/{resolution}/{name}')
            add_video_gui = AddVideoGUI(self.window, "UPDATE", id_video, name, resolution, path)
            add_video_gui.render()
            self.refresh_list_videos()
        else:
            print("Nenhum vídeo selecionado")


def main():
    server_gui = ServerGUI()
    server_gui.render()


if __name__ == "__main__":
    main()


