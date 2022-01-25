from client.clientUDP import ClientUDP
from client.clientTCP import ClientTCP


class Client:

    def __init__(self):
        self.user_name = ''
        self.user_type = ''
        self.client_udp = ClientUDP()

        self.client_tcp = ClientTCP()

        self.client_tcp.address_UDP = self.client_udp.address

    def login(self, user_name, user_type):
        self.user_name = user_name
        self.user_type = user_type
        self.client_tcp.log_in(user_name, user_type)

    def list_videos(self):
        return self.client_udp.list_videos()

    def play_video(self, video_name, resolution):
        self.client_udp.play_video(user_name=self.user_name, video_name=video_name, resolution=resolution)

    def create_group(self):
        self.client_tcp.create_group()

    def add_to_group(self, name):
        return self.client_tcp.add_to_group(name)

    def get_group(self):
        return self.client_tcp.get_group()

    def remove_from_group(self, name):
        return self.client_tcp.remove_from_group(name)

    def play_video_to_group(self, video_name, resolution):
        self.client_udp.play_video(user_name=self.user_name, video_name=video_name, resolution=resolution, option="GROUP")

    def get_in_group_room(self):
        return self.client_udp.get_in_group_room()

    def has_group(self):
        group = self.client_tcp.get_group()
        return len(group) > 1

    def log_out(self):
        self.client_tcp.log_out()

