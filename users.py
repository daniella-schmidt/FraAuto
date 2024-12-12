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

def validate_data(Codigo, idSecretaria, idSetor):
    try:
        connection = mysql.connector.connect(
            host='localhost',
            database='FraAuto',
            user='root',
            password='root'
        )
        cursor = connection.cursor() 

        cursor.execute("SELECT COUNT(*) FROM Codigo WHERE Codigo = %s", (Codigo,))
        if cursor.fetchone()[0] == 0:
            return "Código não existe."

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

def salvar_veiculo(Nome_entry, Matricula_entry, Codigo_entry, IdSecretaria_entry, IdSetor_entry):
    Nome = Nome_entry.get()
    Matricula = Matricula_entry.get()
    Codigo = Codigo_entry.get()
    IdSecretaria = IdSecretaria_entry.get()
    IdSetor = IdSetor_entry.get()

    if not (Nome and Matricula):
        messagebox.showerror("Erro", "Preencha todos os campos obrigatórios!")
        return

    error_message = validate_data(Codigo, IdSecretaria, IdSetor)
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

        if connection.is_connected():
            cursor = connection.cursor()
            insert_query = """
                INSERT INTO veiculos (Nome, Matricula, Codigo, IdSecretaria, IdSetor)
                VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(insert_query, (Nome, Matricula, Codigo, IdSecretaria, IdSetor))
            connection.commit()
            messagebox.showinfo("Sucesso", "Veículo cadastrado com sucesso!")

    except Error as e:
        print(f"Erro ao inserir dados no MySQL: {e}")
        messagebox.showerror("Erro", "Erro ao cadastrar o veículo.")
    finally:
        if 'cursor' in locals() and cursor:
            cursor.close()
        if 'connection' in locals() and connection.is_connected():
            connection.close()

def carregar_users(users_list):
    try:
        connection = mysql.connector.connect(
            host='localhost',
            database='FraAuto',
            user='root',
            password='root'
        )
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM `FraAuto`.`Usuario`")
        users = cursor.fetchall()

        users_list.delete(*users_list.get_children())

        for user in users:
            users_list.insert("", "end", values=user)

    except Error as e:
        print(f"Erro ao carregar usuários: {e}")
    finally:
        if 'cursor' in locals() and cursor:
            cursor.close()
        if 'connection' in locals() and connection.is_connected():
            connection.close()

def create_users_tab(notebook):
    users_tab = ttk.Frame(notebook)
    notebook.add(users_tab, text='Veículos')

    entry_frame = ttk.Frame(users_tab)
    entry_frame.pack(fill='x', padx=10, pady=10)

    ttk.Label(entry_frame, text="Nome:").grid(column=0, row=0, padx=5, pady=5)
    Nome_entry = ttk.Entry(entry_frame, width=20)
    Nome_entry.grid(column=1, row=0, padx=5, pady=5)

    ttk.Label(entry_frame, text="Matricula:").grid(column=0, row=2, padx=5, pady=5)
    Matricula_entry = ttk.Entry(entry_frame, width=20)
    Matricula_entry.grid(column=1, row=2, padx=5, pady=5)    
    
    ttk.Label(entry_frame, text="Codigo:").grid(column=0, row=3, padx=5, pady=5)
    Codigo_entry = ttk.Entry(entry_frame, width=20)
    Codigo_entry.grid(column=1, row=3, padx=5, pady=5)

    ttk.Label(entry_frame, text="IdSecretaria:").grid(column=0, row=4, padx=5, pady=5)
    IdSecretaria_entry = ttk.Entry(entry_frame, width=20)
    IdSecretaria_entry.grid(column=1, row=4, padx=5, pady=5)

    ttk.Label(entry_frame, text="IdSetor:").grid(column=0, row=5, padx=5, pady=5)
    IdSetor_entry = ttk.Entry(entry_frame, width=20)
    IdSetor_entry.grid(column=1, row=5, padx=5, pady=5)   
    
    save_button = ttk.Button(users_tab, text="Salvar", command=lambda: salvar_veiculo(Nome_entry, Matricula_entry, Codigo_entry, IdSecretaria_entry, IdSetor_entry))
    save_button.pack(pady=10)

    list_frame = ttk.Frame(users_tab)
    list_frame.pack(fill='both', expand=True, padx=10, pady=10)

    users_list = ttk.Treeview(list_frame)
    users_list['columns'] = ('Nome', 'Matricula', 'Codigo', 'IdSecretaria', 'IdSetor')

    users_list.column("#0", width=0, stretch=tk.NO)
    users_list.column("Nome", anchor=tk.W, width=100)
    users_list.column("Matricula", anchor=tk.W, width=50)
    users_list.column("Codigo", anchor=tk.W, width=50)
    users_list.column("IdSecretaria", anchor=tk.W, width=100)
    users_list.column("IdSetor", anchor=tk.W, width=100)

    users_list.heading("Nome", text="Nome", anchor=tk.W)
    users_list.heading("Matricula", text="Matricula", anchor=tk.W)
    users_list.heading("Codigo", text="Codigo", anchor=tk.W)
    users_list.heading("IdSecretaria", text="IdSecretaria", anchor=tk.W)
    users_list.heading("IdSetor", text="IdSetor", anchor=tk.W)

    users_list.pack(fill='both', expand=True)

    carregar_users(users_list)

def create_app():
    app = tk.Tk()
    app.title("FraAuto")
    app.geometry("800x600")

    notebook = ttk.Notebook(app)
    notebook.pack(fill='both', expand=True)

    create_users_tab(notebook)

    app.mainloop()

if __name__ == "__main__":
    create_app()
