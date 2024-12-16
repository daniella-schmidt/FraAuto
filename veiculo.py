import tkinter as tk
from tkinter import ttk
import mysql.connector
from mysql.connector import Error
from tkinter import messagebox

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

def validate_data(ano, idFabricante, idModelo, idSecretaria, idSetor):
    if not ano.isdigit() or not (1900 <= int(ano) <= 2024):
        return "Ano inválido. O ano deve estar entre 1900  e 2024."
    
    try:
        connection = mysql.connector.connect(
            host='localhost',
            database='FraAuto',
            user='root',
            password='root'
        )
        cursor = connection.cursor()

        cursor.execute("SELECT COUNT(*) FROM Fabricante WHERE IdFabricante = %s", (idFabricante,))
        if cursor.fetchone()[0] == 0:
            return "IdFabricante não existe."

        cursor.execute("SELECT COUNT(*) FROM Modelo WHERE IdModelo = %s", (idModelo,))
        if cursor.fetchone()[0] == 0:
            return "IdModelo não existe."

        cursor.execute("SELECT COUNT(*) FROM Secretaria WHERE IdSecretaria = %s", (idSecretaria,))
        if cursor.fetchone()[0] == 0:
            return "IdSecretaria não existe."

        cursor.execute("SELECT COUNT(*) FROM Setor WHERE IdSetor = %s", (idSetor,))
        if cursor.fetchone()[0] == 0:
            return "IdSetor não existe."

    except Error as e:
        return f"Erro ao validar dados: {e}"
    finally:
        if 'cursor' in locals() and cursor:
            cursor.close()
        if 'connection' in locals() and connection.is_connected():
            connection.close()
    
    return None

def create_vehicle_management_tab(notebook):
    vehicle_tab = ttk.Frame(notebook)
    notebook.add(vehicle_tab, text='Veículos')

    entry_frame = ttk.Frame(vehicle_tab)
    entry_frame.pack(fill='x', padx=10, pady=10)

    ttk.Label(entry_frame, text="Placa:").grid(column=0, row=0, padx=5, pady=5)
    Placa_entry = ttk.Entry(entry_frame, width=20)
    Placa_entry.grid(column=1, row=0, padx=5, pady=5)

    ttk.Label(entry_frame, text="Ano:").grid(column=0, row=2, padx=5, pady=5)
    Ano_entry = ttk.Entry(entry_frame, width=20)
    Ano_entry.grid(column=1, row=2, padx=5, pady=5)

    ttk.Label(entry_frame, text="Cor:").grid(column=0, row=3, padx=5, pady=5)
    Cor_entry = ttk.Entry(entry_frame, width=20)
    Cor_entry.grid(column=1, row=3, padx=5, pady=5)

    ttk.Label(entry_frame, text="Odômetro:").grid(column=0, row=4, padx=5, pady=5)
    Odometro_entry = ttk.Entry(entry_frame, width=20)
    Odometro_entry.grid(column=1, row=4, padx=5, pady=5)

    ttk.Label(entry_frame, text="IdFabricante:").grid(column=0, row=5, padx=5, pady=5)
    IdFabricante_entry = ttk.Entry(entry_frame, width=20)
    IdFabricante_entry.grid(column=1, row=5, padx=5, pady=5)

    ttk.Label(entry_frame, text="IdModelo:").grid(column=0, row=6, padx=5, pady=5)
    IdModelo_entry = ttk.Entry(entry_frame, width=20)
    IdModelo_entry.grid(column=1, row=6, padx=5, pady=5)

    ttk.Label(entry_frame, text="IdSecretaria:").grid(column=0, row=7, padx=5, pady=5)
    IdSecretaria_entry = ttk.Entry(entry_frame, width=20)
    IdSecretaria_entry.grid(column=1, row=7, padx=5, pady=5)

    ttk.Label(entry_frame, text="IdSetor:").grid(column=0, row=8, padx=5, pady=5)
    IdSetor_entry = ttk.Entry(entry_frame, width=20)
    IdSetor_entry.grid(column=1, row=8, padx=5, pady=5)

    ttk.Label(entry_frame, text="Frotas:").grid(column=0, row=9, padx=5, pady=5)
    Frotas_entry = ttk.Entry(entry_frame, width=20)
    Frotas_entry.grid(column=1, row=9, padx=5, pady=5)
    
    ttk.Label(entry_frame, text="Garantia:").grid(column=0, row=10, padx=5, pady=5)
    Garantia_entry = ttk.Entry(entry_frame, width=20)
    Garantia_entry.grid(column=1, row=10, padx=5, pady=5)

    def salvar_veiculo():
        Placa = Placa_entry.get()
        Ano = Ano_entry.get()
        Cor = Cor_entry.get()
        Odometro = Odometro_entry.get()
        IdFabricante = IdFabricante_entry.get()
        IdModelo = IdModelo_entry.get()
        IdSecretaria = IdSecretaria_entry.get()
        IdSetor = IdSetor_entry.get()
        Frotas = Frotas_entry.get()
        Garantia = Garantia_entry.get()

        if not (Placa and Ano and Cor):
            messagebox.showerror("Erro", "Preencha todos os campos obrigatórios!")
            return

        error_message = validate_data(Ano, IdFabricante, IdModelo, IdSecretaria, IdSetor)
        if error_message:
            messagebox.showerror("Erro", error_message)
            return

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
                INSERT INTO Veiculo (Placa, Ano, Cor, Odometro, IdFabricante, IdModelo, IdSecretaria, IdSetor, Frotas, Garantia) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, 
                (Placa, Ano, Cor, Odometro, IdFabricante, IdModelo, IdSecretaria, IdSetor, Frotas, Garantia)
            )
            connection.commit()
            messagebox.showinfo("Sucesso", "Veículo cadastrado com sucesso!")
        except Error as e:
            messagebox.showerror("Erro", f"Erro ao cadastrar veículo: {e}")
        finally:
            if 'cursor' in locals() and cursor:
                cursor.close()
            if 'connection' in locals() and connection.is_connected():
                connection.close()

    salvar_button = ttk.Button(entry_frame, text="Salvar", command=salvar_veiculo)
    salvar_button.grid(column=0, row=11, columnspan=2, padx=5, pady=10)

    list_frame = ttk.Frame(vehicle_tab)
    list_frame.pack(fill='both', expand=True, padx=10, pady=10)

    veiculos_list = ttk.Treeview(list_frame)
    veiculos_list['columns'] = ('Placa', 'Ano', 'Cor', 'Odometro', 'IdFabricante', 'IdModelo', 'IdSecretaria', 'IdSetor', 'Frotas', 'Garantia') 

    veiculos_list.column("#0", width=0, stretch=tk.NO)
    veiculos_list.column("Placa", anchor=tk.W, width=100)
    veiculos_list.column("Ano", anchor=tk.W, width=50)
    veiculos_list.column("Cor", anchor=tk.W, width=50)
    veiculos_list.column("Odometro", anchor=tk.W, width=50)
    veiculos_list.column("IdFabricante", anchor=tk.W, width=100)
    veiculos_list.column("IdModelo", anchor=tk.W, width=100)
    veiculos_list.column("IdSecretaria", anchor=tk.W, width=100)
    veiculos_list.column("IdSetor", anchor=tk.W, width=100)
    veiculos_list.column("Frotas", anchor=tk.W, width=50)
    veiculos_list.column("Garantia", anchor=tk.W, width=50)

    veiculos_list.heading("Placa", text="Placa", anchor=tk.W)
    veiculos_list.heading("Ano", text="Ano", anchor=tk.W)
    veiculos_list.heading("Cor", text="Cor", anchor=tk.W)
    veiculos_list.heading("Odometro", text="Odômetro", anchor=tk.W)
    veiculos_list.heading("IdFabricante", text="IdFabricante", anchor=tk.W)
    veiculos_list.heading("IdModelo", text="IdModelo", anchor=tk.W)
    veiculos_list.heading("IdSecretaria", text="IdSecretaria", anchor=tk.W)
    veiculos_list.heading("IdSetor", text="IdSetor", anchor=tk.W)
    veiculos_list.heading("Frotas", text="Frotas", anchor=tk.W)
    veiculos_list.heading("Garantia", text="Garantia", anchor=tk.W)

    veiculos_list.pack(fill='both', expand=True)

    def carregar_veiculos():
        try:
            connection = mysql.connector.connect(
                host='localhost',
                database='FraAuto',
                user='root',
                password='root'
            )
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM `FraAuto`.`Veiculo`")
            veiculos = cursor.fetchall()

            veiculos_list.delete(*veiculos_list.get_children())

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

def create_app():
    app = tk.Tk()
    app.title("FraAuto")
    app.geometry("800x600")

    notebook = ttk.Notebook(app)
    notebook.pack(fill='both', expand=True)
    
    create_vehicle_management_tab(notebook)

    app.mainloop()

if __name__ == "__main__":
    create_app()