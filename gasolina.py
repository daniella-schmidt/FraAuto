import tkinter as tk
from tkinter import ttk
import mysql.connector
from mysql.connector import Error
from tkinter import messagebox
from datetime import datetime

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
            print(f"Conectado ao banco de dados: {record[0]}")

    except Error as e:
        print(f"Erro ao conectar ao MySQL: {e}")
    finally:
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()

def gasolina_tab(notebook):
    tab_control = ttk.Notebook(notebook)
    tab_control.pack(fill="both", expand=1)
    tab1 = ttk.Frame(tab_control)
    tab_control.add(tab1, text='Gasolina')
    
    entry_frame = ttk.Frame(tab1)  # Corrigido para usar 'tab1' em vez de 'gasolina_tab'
    entry_frame.pack(fill='x', padx=10, pady=10)

    ttk.Label(entry_frame, text="Placa:").grid(column=0, row=0, padx=5, pady=5)
    Placa_entry = ttk.Entry(entry_frame, width=20)
    Placa_entry.grid(column=1, row=0, padx=5, pady=5)

    ttk.Label(entry_frame, text="Status:").grid(column=0, row=1, padx=5, pady=5)
    Status_entry = ttk.Entry(entry_frame, width=20)
    Status_entry.grid(column=1, row=1, padx=5, pady=5)

    ttk.Label(entry_frame, text="DH_abastecimento:").grid(column=0, row=2, padx=5, pady=5)
    DataHoraAbastecimento_entry = ttk.Entry(entry_frame, width=20)
    DataHoraAbastecimento_entry.grid(column=1, row=2, padx=5, pady=5)
    
    def salvar_gaso():
        Placa = Placa_entry.get()
        Status = Status_entry.get()
        DH_abastecimento = DataHoraAbastecimento_entry.get()

        if not (Placa and Status and DH_abastecimento and Status):
            messagebox.showerror("Erro", "Preencha todos os campos obrigatórios!")
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
                    INSERT INTO Gasolina (Placa, Status, DH_abastecimento)
                    VALUES (%s, %s, %s, %s)
                """
                cursor.execute(insert_query, (Placa, Matricula, Dh_inicial, Onom_inicial))
                connection.commit()

                messagebox.showinfo("Sucesso", "Registro cadastrado com sucesso!")

        except Error as e:
            print(f"Erro ao salvar registro no MySQL: {e}")
            messagebox.showerror("Erro", f"Erro ao salvar registro: {e}")
        finally:
            if 'cursor' in locals() and cursor:
                cursor.close()
            if 'connection' in locals() and connection.is_connected():
                connection.close()
                
    salvar_button = ttk.Button(entry_frame, text="Salvar", command=salvar_gaso)
    salvar_button.grid(column=0, row=5, columnspan=2, pady=10)

root = tk.Tk()
root.title("FraAuto")
root.geometry("700x700")
notebook = ttk.Notebook(root)
notebook.pack(fill='both', expand=True)

gasolina_tab(notebook)

root.mainloop()