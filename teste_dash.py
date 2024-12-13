import dash
from dash import dcc, html
from dash.dash_table import DataTable
import pandas as pd
import mysql.connector
from mysql.connector import Error
import plotly.express as px

# Função para conectar ao banco de dados e obter dados
def fetch_data(table_name):
    connection = None
    cursor = None
    data = []
    try:
        connection = mysql.connector.connect(
            host='localhost',  
            database='FraAuto',  
            user='root',  
            password='root'  
        )

        if connection.is_connected():
            cursor = connection.cursor()
            cursor.execute(f"SELECT * FROM {table_name}")  # Consulta a tabela especificada
            data = cursor.fetchall()
            columns = [i[0] for i in cursor.description]  # Obtém os nomes das colunas

            return pd.DataFrame(data, columns=columns)

    except Error as e:
        print(f"Erro ao conectar ao MySQL: {e}")
    finally:
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()

app = dash.Dash(__name__)

# Obtém os dados do banco de dados
df_registros = fetch_data('Registro')  # Tabela de registros
df_usuarios = fetch_data('Usuario')     # Tabela de usuários

# Exemplo de gráfico (substitua com seus dados)
# Corrigido para usar 'Nome' em vez de 'nome'
fig = px.bar(df_usuarios, x='IdSetor', y='IdSecretaria', title='Locais')  # Exemplo de gráfico

# Layout da dashboard
app.layout = html.Div(style={'padding': '20px', 'fontFamily': 'Arial, sans-serif'}, children=[
    html.H1("Dashboard de Registros e Usuários", style={'textAlign': 'center', 'color': '#4A4A4A'}),
    
    html.Div(style={'display': 'flex', 'flexDirection': 'row', 'justifyContent': 'space-between'}, children=[
        html.Div(style={'flex': '1', 'marginRight': '10px'}, children=[
            html.H2("Tabela de Registros", style={'color': '#2E86C1'}),
            DataTable(
                id='tabela-registros',
                columns=[{"name": i, "id": i} for i in df_registros.columns],
                data=df_registros.to_dict('records'),
                page_size=10,  # Número de registros por página
                style_table={'overflowX': 'auto'},
                style_cell={
                    'textAlign': 'left',
                    'padding': '10px',
                    'border': '1px solid #ddd',
                    'backgroundColor': '#f9f9f9'
                },
                style_header={
                    'backgroundColor': '#2E86C1',
                    'color': 'white',
                    'fontWeight': 'bold'
                },
                style_data_conditional=[
                    {
                        'if': {'row_index': 'odd'},
                        'backgroundColor': '#f2f2f2'
                    }
                ]
            ),
        ]),
        
        html.Div(style={'flex': '1', 'marginLeft': '10px'}, children=[
            html.H2("Gráfico de Usuários", style={'color': '#2E86C1'}),
            dcc.Graph(
                id='grafico-usuarios',
                figure=fig
            )
        ]),
    ]),
    
    html.Div(style={'marginTop': '40px'}, children=[
        html.H2("Tabela de Usuários", style={'color': '#2E86C1'}),
        DataTable(
            id='tabela-usuarios',
            columns=[{"name": i, "id": i} for i in df_usuarios.columns],
            data=df_usuarios.to_dict('records'),
            page_size=10,  # Número de registros por página
            style_table={'overflowX': 'auto'},
            style_cell={
                'textAlign': 'left',
                'padding': '10px',
                'border': '1px solid #ddd',
                'backgroundColor': '#f9f9f9'
            },
            style_header={
                'backgroundColor': '#2E86C1',
                'color': 'white',
                'fontWeight': 'bold'
            },
            style_data_conditional=[
                {
                    'if': {'row_index': 'odd'},
                    'backgroundColor': '#f2f2f2'
                }
            ]
        ),
    ]),
])

if __name__ == '__main__':
    app.run_server(debug=True)