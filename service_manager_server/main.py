from service_manager import ServiceManager


def main():
    service_manager = ServiceManager()
    service_manager.listen_to_streaming_server()
    while True:
        service_manager.listen_to_user()


if __name__ == "__main__":
    main()
