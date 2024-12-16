import tkinter as tk
from tkinter import ttk
import mysql.connector
from mysql.connector import Error
from tkinter import messagebox
from datetime import datetime

def registro_tab(notebook):
    registro_tab = ttk.Frame(notebook)
    notebook.add(registro_tab, text='Registro')

    entry_frame = ttk.Frame(registro_tab)
    entry_frame.pack(fill='x', padx=10, pady=10)

    ttk.Label(entry_frame, text="Matrícula:").grid(column=0, row=0, padx=5, pady=5)
    Matricula_entry = ttk.Entry(entry_frame, width=20)
    Matricula_entry.grid(column=1, row=0, padx=5, pady=5)

    ttk.Label(entry_frame, text="Placa:").grid(column=0, row=1, padx=5, pady=5)
    Placa_entry = ttk.Entry(entry_frame, width=20)
    Placa_entry.grid(column=1, row=1, padx=5, pady=5)

    ttk.Label(entry_frame, text="Onom. inicial:").grid(column=0, row=2, padx=5, pady=5)
    Onom_inicial_entry = ttk.Entry(entry_frame, width=20)
    Onom_inicial_entry.grid(column=1, row=2, padx=5, pady=5)

    ttk.Label(entry_frame, text="D/H inicial:").grid(column=0, row=3, padx=5, pady=5)
    Dh_inicial_entry = ttk.Entry(entry_frame, width=20)
    Dh_inicial_entry.grid(column=1, row=3, padx=5, pady=5)
    Dh_inicial_entry.insert(0, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    def buscar_matricula_onometro(event):
        placa = Placa_entry.get()
        if placa:
            try:
                connection = mysql.connector.connect(
                    host='localhost',
                    database='FraAuto',
                    user='root',
                    password='root'
                )

                if connection.is_connected():
                    cursor = connection.cursor()
                    select_query = "SELECT Odometro FROM Veiculo WHERE Placa = %s"
                    cursor.execute(select_query, (placa,))
                    result = cursor.fetchone()

                    if result:
                        Onom_inicial_entry.delete(0, tk.END)
                        Onom_inicial_entry.insert(0, result[0])
                    else:
                        messagebox.showwarning("Aviso", "Placa não encontrada.")

            except Error as e:
                print(f"Erro ao buscar dados no MySQL: {e}")
                messagebox.showerror("Erro", "Erro ao buscar odômetro.")
            finally:
                if 'cursor' in locals() and cursor:
                    cursor.close()
                if 'connection' in locals() and connection.is_connected():
                    connection.close()

    Placa_entry.bind("<FocusOut>", buscar_matricula_onometro)

    def salvar_registro():
        Placa = Placa_entry.get()
        Matricula = Matricula_entry.get()
        Dh_inicial = Dh_inicial_entry.get()
        Onom_inicial = Onom_inicial_entry.get()

        if not (Placa and Matricula and Dh_inicial and Onom_inicial):
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
                    INSERT INTO Registro (Placa, Matricula, DH_inicial, Odom_inicial)
                    VALUES (%s, %s, %s, %s)
                """
                cursor.execute(insert_query, (Placa, Matricula, Dh_inicial, Onom_inicial))
                connection.commit()

                messagebox.showinfo("Sucesso", "Registrada com sucesso!")

        except Error as e:
            print(f"Erro ao salvar registro no MySQL: {e}")
            messagebox.showerror("Erro", f"Erro ao salvar registro: {e}")
        finally:
            if 'cursor' in locals() and cursor:
                cursor.close()
            if 'connection' in locals() and connection.is_connected():
                connection.close()

    salvar_button = ttk.Button(entry_frame, text="Salvar", command=salvar_registro)
    salvar_button.grid(column=0, row=5, columnspan=2, pady=10)

root = tk.Tk()
root.title("FraAuto")
root.geometry("700x700")
notebook = ttk.Notebook(root)
notebook.pack(fill='both', expand=True)

registro_tab(notebook)

root.mainloop()
