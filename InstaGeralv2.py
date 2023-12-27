import instaloader
import tkinter as tk
from ttkbootstrap import Style
from tkinter import messagebox
import sys
import os
import threading

def apagar_arquivos(perfil_alvo):
    pasta_perfil = os.path.join(os.getcwd(), perfil_alvo)
    for file_name in os.listdir(pasta_perfil):
        if file_name.endswith('.xz') or file_name.endswith('.txt'):
            os.remove(os.path.join(pasta_perfil, file_name))

def baixar_perfil(perfil_alvo, text_box):
    L = instaloader.Instaloader()

    try:
        profile = instaloader.Profile.from_username(L.context, perfil_alvo)
        text_box.config(state=tk.NORMAL)
        text_box.delete(1.0, tk.END)  # Limpar o conteúdo anterior
        text_box.insert(tk.END, f'Download em andamento para {perfil_alvo}...\n\n')

        for post in profile.get_posts():
            text_box.insert(tk.END, f'Baixando: {post.url}\n')
            L.download_post(post, target=perfil_alvo)

        text_box.insert(tk.END, f'\nDownload concluído para {perfil_alvo}!')
        text_box.config(state=tk.DISABLED)
        messagebox.showinfo('Sucesso', f'Download concluído para {perfil_alvo}!')

        # Apagar arquivos .txt e .xz
        apagar_arquivos(perfil_alvo)

    except instaloader.exceptions.InstaloaderException as e:
        text_box.config(state=tk.NORMAL)
        text_box.delete(1.0, tk.END)  # Limpar o conteúdo anterior
        text_box.insert(tk.END, f'Erro ao baixar perfil: {str(e)}')
        text_box.config(state=tk.DISABLED)
        messagebox.showerror('Erro', f'Erro ao baixar perfil: {str(e)}')

    except instaloader.exceptions.ConnectionException as e:
        text_box.config(state=tk.NORMAL)
        text_box.delete(1.0, tk.END)  # Limpar o conteúdo anterior
        text_box.insert(tk.END, f'Erro de conexão: {str(e)}')
        text_box.config(state=tk.DISABLED)
        messagebox.showerror('Erro', f'Erro de conexão: {str(e)}')

def baixar_callback(perfil_alvo, text_box):
    threading.Thread(target=baixar_perfil, args=(perfil_alvo, text_box)).start()

def main(perfil_alvo):
    root = tk.Tk()
    root.title('InstaGeral')

    # Configurar o estilo para o tema "solar"
    style = Style(theme='solar')

    frame = tk.Frame(root, padx=10, pady=10)
    frame.pack()

    entry = tk.Entry(frame, width=20, justify=tk.CENTER)  # Centralizar o texto na entrada
    entry.grid(row=0, column=0, pady=10)
    entry.insert(0, perfil_alvo)
    entry.focus()  # Dar foco à entrada

    # Dica para os usuários
    dica = tk.Label(frame, text='Digite o nome de usuário do Instagram acima e clique em "Baixar".', font=('Arial', 8))
    dica.grid(row=1, column=0, pady=5)

    text_box = tk.Text(frame, height=10, width=40, state=tk.DISABLED)
    text_box.grid(row=2, column=0, pady=5)

    button_baixar = tk.Button(frame, text='Baixar', command=lambda: baixar_callback(entry.get(), text_box))
    button_baixar.grid(row=3, column=0, pady=5)

    button_sair = tk.Button(frame, text='Sair', command=root.destroy)
    button_sair.grid(row=4, column=0, pady=5)

    root.mainloop()

if __name__ == '__main__':
    if len(sys.argv) > 1:
        perfil_alvo = sys.argv[1]
    else:
        perfil_alvo = ''

    main(perfil_alvo)
