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

def create_users_tab(notebook):
    users_tab = ttk.Frame(notebook)
    notebook.add(users_tab, text='Usuários')

def create_vehicle_management_tab(notebook):
    vehicle_tab = ttk.Frame(notebook)
    notebook.add(vehicle_tab, text='Gerenciamento de Veículos')
    
def create_rental_tab(notebook):
    rental_tab = ttk.Frame(notebook)
    notebook.add(rental_tab, text='Retirada')

def create_dev_tab(notebook):
    dev_tab = ttk.Frame(notebook)
    notebook.add(dev_tab, text='Devolução')
    
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
    create_dev_tab(notebook)

    app.mainloop()

if __name__ == "__main__":
    create_app()