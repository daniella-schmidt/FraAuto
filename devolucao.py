import tkinter as tk
from tkinter import ttk
import mysql.connector
from mysql.connector import Error
from tkinter import messagebox
from datetime import datetime

def devolucao_tab(notebook):
    devolucao_tab = ttk.Frame(notebook)
    notebook.add(devolucao_tab, text='Devolução')

    entry_frame = ttk.Frame(devolucao_tab)
    entry_frame.pack(fill='x', padx=10, pady=10)

    ttk.Label(entry_frame, text="Placa:").grid(column=0, row=0, padx=5, pady=5)
    Placa_devolucao_entry = ttk.Entry(entry_frame, width=20)
    Placa_devolucao_entry.grid(column=1, row=0, padx=5, pady=5)

    ttk.Label(entry_frame, text="D/H Devolução:").grid(column=0, row=1, padx=5, pady=5)
    Dh_devolucao_entry = ttk.Entry(entry_frame, width=20)
    Dh_devolucao_entry.grid(column=1, row=1, padx=5, pady=5)
    Dh_devolucao_entry.insert(0, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))  
    
    ttk.Label(entry_frame, text="Odom. final:").grid(column=0, row=2, padx=5, pady=5)
    Odom_final_entry = ttk.Entry(entry_frame, width=20)
    Odom_final_entry.grid(column=1, row=2, padx=5, pady=5)

    def salvar_devolucao():
        Placa = Placa_devolucao_entry.get().strip()
        Dh_devolucao = Dh_devolucao_entry.get().strip()
        Odom_final = Odom_final_entry.get().strip()

        if not (Placa and Dh_devolucao and Odom_final):
            messagebox.showerror("Erro", "Preencha todos os campos obrigatórios!")
            return

        try:
            datetime.strptime(Dh_devolucao, "%Y-%m-%d %H:%M:%S")
        except ValueError:
            messagebox.showerror("Erro", "Formato de data/hora inválido! Use: YYYY-MM-DD HH:MM:SS")
            return

        if not Odom_final.isdigit():
            messagebox.showerror("Erro", "O campo 'Odom. final' deve conter apenas números!")
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

                check_query = "SELECT COUNT(*) FROM Registro WHERE Placa = %s"
                cursor.execute(check_query, (Placa,))
                result = cursor.fetchone()
                if result[0] == 0:
                    messagebox.showwarning("Aviso", "Placa não encontrada no sistema.")
                    return

                update_query = """
                    UPDATE Registro
                    SET `D/H final` = %s, `Odom. final` = %s
                    WHERE Placa = %s
                """
                cursor.execute(update_query, (Dh_devolucao, Odom_final, Placa))
                connection.commit()

                if cursor.rowcount > 0:
                    messagebox.showinfo("Sucesso", "Devolução registrada com sucesso!")
                else:
                    messagebox.showwarning("Aviso", "Nenhuma alteração foi feita.")

        except Error as e:
            print(f"Erro ao acessar o MySQL: {e}")
            messagebox.showerror("Erro", f"Erro ao acessar o banco de dados: {e}")
        finally:
            if 'cursor' in locals() and cursor:
                cursor.close()
            if 'connection' in locals() and connection.is_connected():
                connection.close()

    save_devolucao_button = ttk.Button(devolucao_tab, text="Registrar Devolução", command=salvar_devolucao)
    save_devolucao_button.pack(pady=10)

def create_app():
    app = tk.Tk()
    app.title("FraAuto")
    app.geometry("700x700")

    notebook = ttk.Notebook(app)
    notebook.pack(fill='both', expand=True)

    devolucao_tab(notebook)

    app.mainloop()

if __name__ == "__main__":
    create_app()
