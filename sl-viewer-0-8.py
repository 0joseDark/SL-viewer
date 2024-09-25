# -*- coding: utf-8 -*-
import clr  # Para integrar com bibliotecas .NET
import sys  # Para manipulação de caminhos e módulos do sistema
import os   # Para operações com o sistema de arquivos
import tkinter as tk  # Biblioteca para criação de interfaces gráficas
from tkinter import messagebox  # Caixa de mensagens para interações com o usuário
import time  # Para adicionar tempos de espera

# Adiciona o caminho onde as DLLs da libopenmetaverse estão localizadas
# Substitua 'C:\caminho\para\dlls' pelo caminho real onde você extraiu as DLLs
sys.path.append(r'C:\Users\jose\Documents\GitHub\0joseDark\SL-viewer\DLLs')

# Carrega as bibliotecas .NET da libopenmetaverse
clr.AddReference(r'C:\Users\jose\Documents\GitHub\0joseDark\SL-viewer\DLLs\OpenMetaverse')
clr.AddReference(r'C:\Users\jose\Documents\GitHub\0joseDark\SL-viewer\DLLs\OpenMetaverseTypes')

# Importa as classes necessárias da libopenmetaverse
from OpenMetaverse import GridClient, LoginParams, LoginStatus, Vector3, Quaternion

# Variável global do cliente, que será usada para interagir com o Second Life
client = None

# Função para realizar login no Second Life
def login_second_life(username, password, grid_uri, start_location="last"):
    global client  # Utiliza a variável global para armazenar o cliente
    client = GridClient()  # Cria uma nova instância do GridClient

    # Configura o canal do visualizador (Viewer Channel)
    client.Settings.LOGIN_CHANNEL = "SL-Viewer"  # Nome do visualizador personalizado
    client.Settings.LOGIN_VERSION = "0.1.0"  # Versão do visualizador (opcional)

    # Aumenta o timeout de login para evitar falhas por tempo limite
    client.Settings.LOGIN_TIMEOUT = 120  # 120 segundos de timeout para a conexão

    # Configura os parâmetros de login com nome de usuário, senha e local de início
    first_name, last_name = username.split(" ")

    login_params = LoginParams()
    login_params.FirstName = first_name  # Primeiro nome do avatar
    login_params.LastName = last_name  # Último nome do avatar
    login_params.Password = password  # Senha do usuário
    login_params.URI = grid_uri  # URI do grid para o login, incluindo a porta 13001
    login_params.Start = start_location  # Local inicial (home, last, etc.)

    # Tenta realizar o login
    try:
        login_result = client.Network.Login(login_params)
        if login_result == LoginStatus.Success:
            print("Login realizado com sucesso como {}".format(username))
            status_label.config(text="Login realizado com sucesso!")
            return True
        else:
            print("Falha ao logar: {}".format(client.Network.LoginMessage))
            status_label.config(text="Falha ao logar: {}".format(client.Network.LoginMessage))
            return False
    except Exception as e:
        print("Erro ao tentar logar: {}".format(e))
        status_label.config(text="Erro ao tentar logar: {}".format(e))
        return False

# Função para enviar mensagens de chat no Second Life
def enviar_mensagem_chat(mensagem, canal=0):
    if client and client.Network.Connected:
        client.Self.Chat(mensagem, canal)  # Envia a mensagem para o canal especificado
        status_label.config(text="Mensagem enviada: {}".format(mensagem))
    else:
        status_label.config(text="Não conectado ao Second Life")

# Função para mover o avatar para uma direção específica
def mover_avatar_para_direcao(dx, dy, dz=0):
    if client and client.Network.Connected:
        # Obter a posição atual do avatar
        posicao_atual = client.Self.SimPosition
        # Nova posição baseada no deslocamento
        nova_posicao = Vector3(posicao_atual.X + dx, posicao_atual.Y + dy, posicao_atual.Z + dz)
        client.Self.AutoPilot(nova_posicao)  # Move o avatar automaticamente para a nova posição
        status_label.config(text="Movendo avatar para {}".format(nova_posicao))
    else:
        status_label.config(text="Não conectado ao Second Life")

# Função para teletransportar o avatar para coordenadas específicas
def mover_avatar(x, y, z):
    if client and client.Network.Connected:
        destino = Vector3(x, y, z)
        client.Self.Teleport(destino)  # Teleporta o avatar para a posição especificada
        status_label.config(text="Movendo avatar para {}".format(destino))
    else:
        status_label.config(text="Não conectado ao Second Life")

# Função para deslogar do Second Life
def logout():
    if client and client.Network.Connected:
        client.Network.Logout()  # Realiza o logout
        status_label.config(text="Deslogado com sucesso.")
    else:
        status_label.config(text="Não conectado ao Second Life")

# Função para associar teclas do teclado ao movimento do avatar
def tecla_pressionada(event):
    """Movimenta o avatar com base nas teclas pressionadas."""
    if event.keysym == "Up":
        mover_avatar_para_direcao(0, 1)  # Move para frente
    elif event.keysym == "Down":
        mover_avatar_para_direcao(0, -1)  # Move para trás
    elif event.keysym == "Left":
        mover_avatar_para_direcao(-1, 0)  # Move para a esquerda
    elif event.keysym == "Right":
        mover_avatar_para_direcao(1, 0)  # Move para a direita

# Função para rotacionar o avatar com o movimento do mouse
def rotacionar_avatar_com_rato(event):
    """Roda o avatar com o movimento do mouse."""
    if client and client.Network.Connected:
        # Calcular o ângulo de rotação baseado no movimento do mouse
        delta_x = event.x - root.winfo_width() / 2
        angulo = delta_x / 100.0  # Ajustar a sensibilidade conforme necessário
        rotacao = Quaternion(0, 0, 0, angulo)
        client.Self.Movement.BodyRotation = rotacao
        client.Self.Movement.SendUpdate()
        status_label.config(text="Rotacionando avatar.")
    else:
        status_label.config(text="Não conectado ao Second Life")

# Função para aplicar dano ao avatar com um tempo de espera
def aplicar_dano(dano, tempo_espera):
    if client and client.Network.Connected:
        time.sleep(tempo_espera)  # Espera pelo tempo especificado antes de aplicar o dano
        client.Self.Health -= dano  # Aplica o dano ao avatar
        status_label.config(text="Dano de {} aplicado ao avatar.".format(dano))
    else:
        status_label.config(text="Não conectado ao Second Life")

# Cria a janela principal usando o tkinter
root = tk.Tk()
root.title("Second Life Client")  # Define o título da janela

# Configura o menu principal
menu_bar = tk.Menu(root)
root.config(menu=menu_bar)

# Adiciona um menu de opções para escolher o grid (opções não alteradas)
grid_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Grid", menu=grid_menu)
grid_menu.add_command(label="Second Life", command=lambda: grid_var.set("https://login.agni.lindenlab.com/cgi-bin/login.cgi"))
grid_menu.add_command(label="Localhost", command=lambda: grid_var.set("http://localhost:9000"))
grid_menu.add_command(label="OSgrid", command=lambda: grid_var.set("http://osgrid.org"))

# Variável para armazenar o grid selecionado
grid_var = tk.StringVar(value="https://login.agni.lindenlab.com/cgi-bin/login.cgi")

# Campo de entrada para nome de usuário
tk.Label(root, text="Username:").grid(row=0, column=0, padx=10, pady=5)
username_entry = tk.Entry(root)
username_entry.grid(row=0, column=1, padx=10, pady=5)

# Campo de entrada para senha
tk.Label(root, text="Password:").grid(row=1, column=0, padx=10, pady=5)
password_entry = tk.Entry(root, show='*')
password_entry.grid(row=1, column=1, padx=10, pady=5)

# Campo de entrada para grid (adicionado um entry para permitir customização)
tk.Label(root, text="Grid:").grid(row=2, column=0, padx=10, pady=5)
grid_entry = tk.Entry(root, textvariable=grid_var)
grid_entry.grid(row=2, column=1, padx=10, pady=5)

# Botão de login
login_button = tk.Button(root, text="Login", command=lambda: login_second_life(username_entry.get(), password_entry.get(), grid_entry.get()))
login_button.grid(row=3, column=0, columnspan=2, pady=10)

# Campo de entrada e botão para enviar mensagem de chat
tk.Label(root, text="Mensagem de Chat:").grid(row=4, column=0, padx=10, pady=5)
chat_entry = tk.Entry(root)
chat_entry.grid(row=4, column=1, padx=10, pady=5)

send_chat_button = tk.Button(root, text="Enviar Mensagem", command=lambda: enviar_mensagem_chat(chat_entry.get()))
send_chat_button.grid(row=5, column=0, columnspan=2, pady=10)

# Campos de entrada para mover o avatar para coordenadas específicas (x, y, z)
tk.Label(root, text="Mover Avatar (x, y, z):").grid(row=6, column=0, padx=10, pady=5)
move_entry_x = tk.Entry(root)
move_entry_x.grid(row=6, column=1, padx=10, pady=5)
move_entry_y = tk.Entry(root)
move_entry_y.grid(row=7, column=1, padx=10, pady=5)
move_entry_z = tk.Entry(root)
move_entry_z.grid(row=8, column=1, padx=10, pady=5)

# Botão para mover o avatar
move_button = tk.Button(root, text="Mover Avatar", command=lambda: mover_avatar(float(move_entry_x.get()), float(move_entry_y.get()), float(move_entry_z.get())))
move_button.grid(row=9, column=0, columnspan=2, pady=10)

# Campo para tempo de espera antes de aplicar ações
tk.Label(root, text="Tempo de Espera (s):").grid(row=10, column=0, padx=10, pady=5)
tempo_espera_entry = tk.Entry(root)
tempo_espera_entry.grid(row=10, column=1, padx=10, pady=5)

# Campo para dano
tk.Label(root, text="Dano:").grid(row=11, column=0, padx=10, pady=5)
dano_entry = tk.Entry(root)
dano_entry.grid(row=11, column=1, padx=10, pady=5)

# Botão para aplicar dano
dano_button = tk.Button(root, text="Aplicar Dano", command=lambda: aplicar_dano(float(dano_entry.get()), float(tempo_espera_entry.get())))
dano_button.grid(row=12, column=0, columnspan=2, pady=10)

# Botão de logout
logout_button = tk.Button(root, text="Logout", command=logout)
logout_button.grid(row=13, column=0, columnspan=2, pady=10)

# Rótulo para exibir mensagens de status
status_label = tk.Label(root, text="")
status_label.grid(row=14, column=0, columnspan=2, pady=10)

# Associa teclas ao evento de movimento
root.bind("<KeyPress>", tecla_pressionada)

# Associa o movimento do mouse ao evento de rotação do avatar
root.bind("<Motion>", rotacionar_avatar_com_rato)

# Inicia a interface gráfica
root.mainloop()
