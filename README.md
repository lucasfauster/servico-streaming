### Aplicação de serviço de streaming em python para o trabalho de redes 2

- Bibliotecas Necessárias:
    - opencv-contrib-python v.4.5.4.60
    - imutils 0.5.4
    - pickle 
    - numpy 1.19.5
    - tkinter 8.6 (sudo apt-get install python3.6-tk)
    - pillow 8.4.0
 - Bibliotecas Nativas do Python:
    - Socket
    - Threading
    - Base64
    - sqlite3

Para executar a aplicação (usuário):
1. Inicie o servidor gerenciado de serviço através do seguinte comando:
> python3 service_manager_server/main.py 

2. Inicie o servidor de streaming através do seguinte comando:
> python3 streaming_server/serverUDP.py 

3. Inicie a GUI do cliente através do seguinte comando: 
> python3 janelas/GUI_login.py 


Para executar a aplicação (administrador):
1. Inicie a GUI do servidor através do seguinte comando: 
> python3 janelas/GUI_server.py 
