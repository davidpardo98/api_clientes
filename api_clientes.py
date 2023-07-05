from flask import Flask, jsonify, request
import pyodbc

app = Flask(__name__)

# Establece la cadena de conexión a tu base de datos SQL Server
conn = pyodbc.connect('DRIVER={SQL Server};SERVER=GRAND;DATABASE=MNG_LOVECHI;UID=sa;PWD=masterkey')
cursor = conn.cursor()



# Ruta para obtener todos los clientes
@app.route('/api/clientes', methods=['GET'])
def get_clientes():
    cursor.execute('SELECT TOP (100) * FROM CLIENTES')
    rows = cursor.fetchall()

    clientes = []
    for row in rows:
        cliente = dict(zip([column[0] for column in cursor.description], row))
        for key, value in cliente.items():
            if isinstance(value, bytes):
                try:
                    cliente[key] = value.decode('utf-8')  # Intenta decodificar a UTF-8
                except UnicodeDecodeError:
                    cliente[key] = value.decode('latin-1')  # Si falla, decodifica a Latin-1 u otra codificación adecuada
        clientes.append(cliente)

    return jsonify(clientes)




if __name__ == '__main__':
    app.run()
