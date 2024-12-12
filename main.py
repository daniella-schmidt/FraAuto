import tkinter as tk
from tkinter import ttk
import mysql.connector
from mysql.connector import Error

def connect_to_database():
    connection = None
    cursor = None
    try:
        connection = mysql.connector.connect(
            host='localhost',  
            database='FraAuto',  
            user='root',  
            password='root'  
        )

        if connection.is_connected():
            cursor = connection.cursor()
            cursor.execute("SELECT DATABASE();")
            record = cursor.fetchone()

    except Error as e:
        print(f"Erro ao conectar ao MySQL: {e}")
    finally:
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()

def create_dashboard_tab(notebook):
    dashboard_tab = ttk.Frame(notebook)
    notebook.add(dashboard_tab, text='Dashboard')
    # Adicione widgets para o dashboard aqui

def create_users_tab(notebook):
    users_tab = ttk.Frame(notebook)
    notebook.add(users_tab, text='Usuários')
    # Adicione widgets para gerenciar usuários aqui

def create_vehicle_management_tab(notebook):
    vehicle_tab = ttk.Frame(notebook)
    notebook.add(vehicle_tab, text='Veículos')

    # Crie um frame para os campos de entrada
    entry_frame = ttk.Frame(vehicle_tab)
    entry_frame.pack(fill='x', padx=10, pady=10)

    # Crie os campos de entrada
    ttk.Label(entry_frame, text="Placa:").grid(column=0, row=0, padx=5, pady=5)
    placa_entry = ttk.Entry(entry_frame, width=20)
    placa_entry.grid(column=1, row=0, padx=5, pady=5)

    ttk.Label(entry_frame, text="Modelo:").grid(column=0, row=1, padx=5, pady=5)
    modelo_entry = ttk.Entry(entry_frame, width=20)
    modelo_entry.grid(column=1, row=1, padx=5, pady=5)

    ttk.Label(entry_frame, text="Ano:").grid(column=0, row=2, padx=5, pady=5)
    ano_entry = ttk.Entry(entry_frame, width=20)
    ano_entry.grid(column=1, row=2, padx=5, pady=5)

    ttk.Label(entry_frame, text="Cor:").grid(column=0, row=3, padx=5, pady=5)
    cor_entry = ttk.Entry(entry_frame, width=20)
    cor_entry.grid(column=1, row=3, padx=5, pady=5)

    ttk.Label(entry_frame, text="Frotas:").grid(column=0, row=4, padx=5, pady=5)
    frotas_entry = ttk.Entry(entry_frame, width=20)
    frotas_entry.grid(column=1, row=4, padx=5, pady=5)

    ttk.Label(entry_frame, text="Odômetro:").grid(column=0, row=5, padx=5, pady=5)
    odometro_entry = ttk.Entry(entry_frame, width=20)
    odometro_entry.grid(column=1, row=5, padx=5, pady=5)

    ttk.Label(entry_frame, text="IdFabricante:").grid(column=0, row=6, padx=5, pady=5)
    idFabricante_entry = ttk.Entry(entry_frame, width=20)
    idFabricante_entry.grid(column=1, row=6, padx=5, pady=5)

    ttk.Label(entry_frame, text="IdModelo:").grid(column=0, row=7, padx=5, pady=5)
    idModelo_entry = ttk.Entry(entry_frame, width=20)
    idModelo_entry.grid(column=1, row=7, padx=5, pady=5)

    ttk.Label(entry_frame, text="IdSecretaria:").grid(column=0, row=8, padx=5, pady=5)
    idSecretaria_entry = ttk.Entry(entry_frame, width=20)
    idSecretaria_entry.grid(column=1, row=8, padx=5, pady=5)

    ttk.Label(entry_frame, text="IdSetor:").grid(column=0, row=9, padx=5, pady=5)
    idSetor_entry = ttk.Entry(entry_frame, width=20)
    idSetor_entry.grid(column=1, row=9, padx=5, pady=5)

    # Crie um botão para salvar o veículo
    def salvar_veiculo():
        placa = placa_entry.get()
        modelo = modelo_entry.get()
        ano = ano_entry.get()
        cor = cor_entry.get()
        frotas = frotas_entry.get()
        odometro = odometro_entry.get()
        idFabricante = idFabricante_entry.get()
        idModelo = idModelo_entry.get()
        idSecretaria = idSecretaria_entry.get()
        idSetor = idSetor_entry.get()

        if placa and modelo and ano and cor:
            try:
                connection = mysql.connector.connect(
                    host='localhost',
                    database='FraAuto',
                    user='root',
                    password='root'
                )

                cursor = connection.cursor()
                cursor.execute(
                    """
                    INSERT INTO veiculos (placa, modelo, ano, cor, frotas, odometro, idFabricante, idModelo, idSecretaria, idSetor) 
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """, 
                    (placa, modelo, ano, cor, frotas, odometro, idFabricante, idModelo, idSecretaria, idSetor)
                )
                connection.commit()
                print("Veículo cadastrado com sucesso!")
            except Error as e:
                print(f"Erro ao cadastrar veículo: {e}")
            finally:
                if 'cursor' in locals() and cursor:
                    cursor.close()
                if 'connection' in locals() and connection.is_connected():
                    connection.close()
        else:
            print("Preencha todos os campos obrigatórios!")

    salvar_button = ttk.Button(entry_frame, text="Salvar", command=salvar_veiculo)
    salvar_button.grid(column=0, row=10, columnspan=2, padx=5, pady=10)

    # Crie um frame para a lista de veículos
    list_frame = ttk.Frame(vehicle_tab)
    list_frame.pack(fill='both', expand=True, padx=10, pady=10)

    # Crie uma lista de veículos
    veiculos_list = ttk.Treeview(list_frame)
    veiculos_list['columns'] = ('placa', 'modelo', 'ano', 'cor', 'frotas', 'odometro', 'idFabricante', 'idModelo', 'idSecretaria', 'idSetor')

    veiculos_list.column("#0", width=0, stretch=tk.NO)
    veiculos_list.column("placa", anchor=tk.W, width=100)
    veiculos_list.column("modelo", anchor=tk.W, width=100)
    veiculos_list.column("ano", anchor=tk.W, width=50)
    veiculos_list.column("cor", anchor=tk.W, width=50)
    veiculos_list.column("frotas", anchor=tk.W, width=50)
    veiculos_list.column("odometro", anchor=tk.W, width=50)
    veiculos_list.column("idFabricante", anchor=tk.W, width=100)
    veiculos_list.column("idModelo", anchor=tk.W, width=100)
    veiculos_list.column("idSecretaria", anchor=tk.W, width=100)
    veiculos_list.column("idSetor", anchor=tk.W, width=100)

    veiculos_list.heading("placa", text="Placa", anchor=tk.W)
    veiculos_list.heading("modelo", text="Modelo", anchor=tk.W)
    veiculos_list.heading("ano", text="Ano", anchor=tk.W)
    veiculos_list.heading("cor", text="Cor", anchor=tk.W)
    veiculos_list.heading("frotas", text="Frotas", anchor=tk.W)
    veiculos_list.heading("odometro", text="Odômetro", anchor=tk.W)
    veiculos_list.heading("idFabricante", text="IdFabricante", anchor=tk.W)
    veiculos_list.heading("idModelo", text="IdModelo", anchor=tk.W)
    veiculos_list.heading("idSecretaria", text="IdSecretaria", anchor=tk.W)
    veiculos_list.heading("idSetor", text="IdSetor", anchor=tk.W)

    veiculos_list.pack(fill='both', expand=True)

    # Carregue a lista de veículos
    def carregar_veiculos():
        try:
            connection = mysql.connector.connect(
                host='localhost',
                database='FraAuto',
                user='root',
                password='root'
            )

            cursor = connection.cursor()
            cursor.execute("SELECT * FROM veiculos")
            veiculos = cursor.fetchall()

            veiculos_list.delete(*veiculos_list.get_children())  # Limpa a lista antes de carregar novos dados

            for veiculo in veiculos:
                veiculos_list.insert('', 'end', values=veiculo)
        except Error as e:
            print(f"Erro ao carregar veículos: {e}")
        finally:
            if 'cursor' in locals() and cursor:
                cursor.close()
            if 'connection' in locals() and connection.is_connected():
                connection.close()

    carregar_veiculos()

def create_rental_tab(notebook):
    rental_tab = ttk.Frame(notebook)
    notebook.add(rental_tab, text='Retirada/Entrega')
    # Adicione widgets para registrar retirada e entrega aqui

def create_app():
    app = tk.Tk()
    app.title("FraAuto")
    app.geometry("800x600")

    notebook = ttk.Notebook(app)
    notebook.pack(fill='both', expand=True)

    create_dashboard_tab(notebook)
    create_users_tab(notebook)
    create_vehicle_management_tab(notebook)
    create_rental_tab(notebook)

    app.mainloop()

if __name__ == "__main__":
    create_app()