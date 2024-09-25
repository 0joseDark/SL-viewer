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

# Valores padrão para login
USERNAME = "avatar name"
PASSWORD = "1234"
GRID_URI = "https://login.agni.lindenlab.com/cgi-bin/login.cgi"  # URI correspondente ao grid Second Life

# Função para realizar login no Second Life
def login_second_life(username, password, grid_uri, start_location="last"):
    global client  # Utiliza a variável global para armazenar o cliente
    client = GridClient()  # Cria uma nova instância do GridClient

    # Configura os parâmetros de login com nome de usuário, senha e local de início
    login_params = client.Network.DefaultLoginParams(username, password, start_location)
    login_params.URI = grid_uri  # Define o URI do grid (Second Life, localhost, etc.)

    # Tenta realizar o login
    login_result = client.Network.Login(login_params)
    
    # Verifica o status do login
    if login_result == LoginStatus.Success:
        print("Login realizado com sucesso como {}".format(username))
    else:
        print("Falha ao logar: {}".format(client.Network.LoginMessage))
        return False

    return True

# Função para enviar mensagens de chat no Second Life
def enviar_mensagem_chat(mensagem, canal=0):
    if client and client.Network.Connected:
        client.Self.Chat(mensagem, canal)  # Envia a mensagem para o canal especificado
        messagebox.showinfo("Chat", "Mensagem enviada: {}".format(mensagem))
    else:
        messagebox.showerror("Chat", "Não conectado ao Second Life")

# Função para mover o avatar para uma direção específica
def mover_avatar_para_direcao(dx, dy, dz=0):
    if client and client.Network.Connected:
        # Obter a posição atual do avatar
        posicao_atual = client.Self.SimPosition
        # Nova posição baseada no deslocamento
        nova_posicao = Vector3(posicao_atual.X + dx, posicao_atual.Y + dy, posicao_atual.Z + dz)
        client.Self.AutoPilot(nova_posicao)  # Move o avatar automaticamente para a nova posição
        messagebox.showinfo("Movimento", "Movendo avatar para {}".format(nova_posicao))
    else:
        messagebox.showerror("Movimento", "Não conectado ao Second Life")

# Função para teletransportar o avatar para coordenadas específicas
def mover_avatar(x, y, z):
    if client and client.Network.Connected:
        destino = Vector3(x, y, z)
        client.Self.Teleport(destino)  # Teleporta o avatar para a posição especificada
        messagebox.showinfo("Movimento", "Movendo avatar para {}".format(destino))
    else:
        messagebox.showerror("Movimento", "Não conectado ao Second Life")

# Função para deslogar do Second Life
def logout():
    if client and client.Network.Connected:
        client.Network.Logout()  # Realiza o logout
        messagebox.showinfo("Logout", "Deslogado com sucesso.")
    else:
        messagebox.showerror("Logout", "Não conectado ao Second Life")

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
    else:
        messagebox.showerror("Movimento", "Não conectado ao Second Life")

# Função para aplicar dano ao avatar com um tempo de espera
def aplicar_dano(dano, tempo_espera):
    if client and client.Network.Connected:
        time.sleep(tempo_espera)  # Espera pelo tempo especificado antes de aplicar o dano
        client.Self.Health -= dano  # Aplica o dano ao avatar
        messagebox.showinfo("Dano", "Dano de {} aplicado ao avatar.".format(dano))
    else:
        messagebox.showerror("Dano", "Não conectado ao Second Life")

# Cria a janela principal usando o tkinter
root = tk.Tk()
root.title("Second Life Client")  # Define o título da janela

# Configura o menu principal
menu_bar = tk.Menu(root)
root.config(menu=menu_bar)

# Adiciona um menu de opções para escolher o grid (opções não alteradas)
grid_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Grid", menu=grid_menu)
grid_menu.add_command(label="Second Life", command=lambda: grid_var.set("Second Life"))
grid_menu.add_command(label="Localhost", command=lambda: grid_var.set("Localhost"))
grid_menu.add_command(label="OSgrid", command=lambda: grid_var.set("OSgrid"))

# Variável para armazenar o grid selecionado (não utilizada após a modificação)
grid_var = tk.StringVar(value="Second Life")

# Botão de login (agora redundante, mas mantido para referência)
login_button = tk.Button(root, text="Login", command=lambda: login_second_life(USERNAME, PASSWORD, GRID_URI))
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

# Associa teclas ao evento de movimento
root.bind("<KeyPress>", tecla_pressionada)

# Associa o movimento do mouse ao evento de rotação do avatar
root.bind("<Motion>", rotacionar_avatar_com_rato)

# Inicia a interface gráfica

# Tenta realizar login automaticamente ao iniciar o script
if login_second_life(USERNAME, PASSWORD, GRID_URI):
    messagebox.showinfo("Conexão", "Login automático realizado com sucesso.")
else:
    messagebox.showerror("Conexão", "Falha ao realizar login automático. Verifique as credenciais e a conexão com o servidor.")

root.mainloop()
