import mysql.connector
import mysql.connector
from mysql.connector import Error

def verificar_manutencao():
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
    # Consulta SQL
    
    query = """
    SELECT 
        v.id AS veiculo_id,
        v.modelo,
        v.ano,
        v.ultima_manutencao,
        v.km_atual,
        CASE 
            WHEN DATEDIFF(CURDATE(), v.ultima_manutencao) >= 365 THEN 'Necessário manutenção (1 ano passado)'
            WHEN (v.km_atual - IFNULL(h.km_manutencao, 0)) >= 10000 THEN 'Necessário troca de óleo (10.000 km rodados)'
            ELSE 'Sem necessidade de manutenção'
        END AS status_manutencao
    FROM 
        veiculos v
    LEFT JOIN 
        historico h ON v.id = h.veiculo_id
    ORDER BY 
        v.id;
    """
    cursor.execute(query)
    resultados = cursor.fetchall()

    # Exibir resultados no console ou no Dashboard
    for row in resultados:
        print(f"Veículo ID: {row[0]}, Modelo: {row[1]}, Ano: {row[2]}, Status: {row[5]}")

    cursor.close()

verificar_manutencao()
