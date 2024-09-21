# -*- coding: utf-8 -*-
import clr
import sys
import os
import tkinter as tk
from tkinter import messagebox

# Adicionar o caminho das DLLs da libopenmetaverse
sys.path.append(r'C:\Users\jose\Documents\GitHub\0joseDark\SL-viewer\DLLs')

# Carregar as bibliotecas
clr.AddReference('OpenMetaverse')
clr.AddReference('OpenMetaverseTypes')

# Importar classes da libopenmetaverse
from OpenMetaverse import GridClient, LoginParams, LoginStatus, Vector3, Quaternion

# Variável global do cliente
client = None

# Funções de interação com o Second Life
def login_second_life(username, password, grid_uri, start_location="last"):
    global client
    client = GridClient()

    # Configurar parâmetros de login
    login_params = client.Network.DefaultLoginParams(username, password, start_location)
    login_params.URI = grid_uri

    # Login no Second Life
    login_result = client.Network.Login(login_params)
    
    if login_result == LoginStatus.Success:
        messagebox.showinfo("Login", f"Login realizado com sucesso como {username}")
    else:
        messagebox.showerror("Login", f"Falha ao logar: {client.Network.LoginMessage}")

def enviar_mensagem_chat(mensagem, canal=0):
    if client and client.Network.Connected:
        client.Self.Chat(mensagem, canal)
        messagebox.showinfo("Chat", f"Mensagem enviada: {mensagem}")
    else:
        messagebox.showerror("Chat", "Não conectado ao Second Life")

def mover_avatar_para_direcao(dx, dy, dz=0):
    if client and client.Network.Connected:
        # Obter a posição atual do avatar
        posicao_atual = client.Self.SimPosition
        # Nova posição baseada no deslocamento
        nova_posicao = Vector3(posicao_atual.X + dx, posicao_atual.Y + dy, posicao_atual.Z + dz)
        client.Self.AutoPilot(nova_posicao)
        messagebox.showinfo("Movimento", f"Movendo avatar para {nova_posicao}")
    else:
        messagebox.showerror("Movimento", "Não conectado ao Second Life")

def mover_avatar(x, y, z):
    if client and client.Network.Connected:
        destino = Vector3(x, y, z)
        client.Self.Teleport(destino)
        messagebox.showinfo("Movimento", f"Movendo avatar para {destino}")
    else:
        messagebox.showerror("Movimento", "Não conectado ao Second Life")

def logout():
    if client and client.Network.Connected:
        client.Network.Logout()
        messagebox.showinfo("Logout", "Deslogado com sucesso.")
    else:
        messagebox.showerror("Logout", "Não conectado ao Second Life")

# Função para o botão de login na GUI
def realizar_login():
    username = username_entry.get()
    password = password_entry.get()
    grid = grid_var.get()
    
    grid_uri = {
        "Second Life": "https://login.agni.lindenlab.com/cgi-bin/login.cgi",
        "Localhost": "http://localhost:9000",
        "OSgrid": "https://login.osgrid.org/"
    }.get(grid, "https://login.agni.lindenlab.com/cgi-bin/login.cgi")
    
    login_second_life(username, password, grid_uri)

# Funções de controle do avatar com o teclado
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

# Criar janela principal
root = tk.Tk()
root.title("Second Life Client")

# Configurar o menu
menu_bar = tk.Menu(root)
root.config(menu=menu_bar)

# Menu de opções de grid
grid_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Grid", menu=grid_menu)
grid_menu.add_command(label="Second Life", command=lambda: grid_var.set("Second Life"))
grid_menu.add_command(label="Localhost", command=lambda: grid_var.set("Localhost"))
grid_menu.add_command(label="OSgrid", command=lambda: grid_var.set("OSgrid"))

# Variável para o grid selecionado
grid_var = tk.StringVar(value="Second Life")

# Campos de login
tk.Label(root, text="Nome de Usuário:").grid(row=0, column=0, padx=10, pady=5)
username_entry = tk.Entry(root)
username_entry.grid(row=0, column=1, padx=10, pady=5)

tk.Label(root, text="Senha:").grid(row=1, column=0, padx=10, pady=5)
password_entry = tk.Entry(root, show="*")
password_entry.grid(row=1, column=1, padx=10, pady=5)

tk.Label(root, text="Grid:").grid(row=2, column=0, padx=10, pady=5)
grid_label = tk.Label(root, textvariable=grid_var)
grid_label.grid(row=2, column=1, padx=10, pady=5)

# Botão de login
login_button = tk.Button(root, text="Login", command=realizar_login)
login_button.grid(row=3, column=0, columnspan=2, pady=10)

# Funções para enviar mensagem e mover avatar (exemplo simples)
tk.Label(root, text="Mensagem de Chat:").grid(row=4, column=0, padx=10, pady=5)
chat_entry = tk.Entry(root)
chat_entry.grid(row=4, column=1, padx=10, pady=5)

send_chat_button = tk.Button(root, text="Enviar Mensagem", command=lambda: enviar_mensagem_chat(chat_entry.get()))
send_chat_button.grid(row=5, column=0, columnspan=2, pady=10)

tk.Label(root, text="Mover Avatar (x, y, z):").grid(row=6, column=0, padx=10, pady=5)
move_entry_x = tk.Entry(root)
move_entry_x.grid(row=6, column=1, padx=10, pady=5)
move_entry_y = tk.Entry(root)
move_entry_y.grid(row=7, column=1, padx=10, pady=5)
move_entry_z = tk.Entry(root)
move_entry_z.grid(row=8, column=1, padx=10, pady=5)

move_button = tk.Button(root, text="Mover Avatar", command=lambda: mover_avatar(float(move_entry_x.get()), float(move_entry_y.get()), float(move_entry_z.get())))
move_button.grid(row=9, column=0, columnspan=2, pady=10)

# Botão de logout
logout_button = tk.Button(root, text="Logout", command=logout)
logout_button.grid(row=10, column=0, columnspan=2, pady=10)

# Vincular as teclas de setas para o movimento do avatar
root.bind("<Up>", tecla_pressionada)
root.bind("<Down>", tecla_pressionada)
root.bind("<Left>", tecla_pressionada)
root.bind("<Right>", tecla_pressionada)

# Vincular o movimento do mouse para rotacionar o avatar
root.bind("<Motion>", rotacionar_avatar_com_rato)

# Iniciar a interface gráfica
root.mainloop()
