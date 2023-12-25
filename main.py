from flask import Flask, render_template, jsonify
from flask_cors import CORS  # Añadido para el soporte CORS
import pymysql

app = Flask(__name__)
CORS(app)  # Añadido para el soporte CORS

# ... (otras rutas)

@app.route('/', methods=['GET'])
def mostrar_numeros():
    cantidad_aleatorios = 2

    try:
        with pymysql.connect(host='bgumgxsdvc4biuaqa7lz-mysql.services.clever-cloud.com', user='un7kcgf6ih5t59l7', passwd='RaJQ617Jy7Nc9gcXvE90', db='bgumgxsdvc4biuaqa7lz') as miConexion:
            cur = miConexion.cursor()

            cur.execute("SELECT COUNT(*) FROM grupo WHERE estado=1")
            total_registros_estado = cur.fetchone()[0]

            if total_registros_estado < cantidad_aleatorios:
                return jsonify({"error": "No hay suficientes registros activos para obtener la cantidad deseada."})
            else:
                consulta_sql = f"SELECT code FROM grupo WHERE estado=1 ORDER BY RAND() LIMIT 2"
                cur.execute(consulta_sql)

                elegidos = [code[0] for code in cur.fetchall()]

                if len(elegidos) == cantidad_aleatorios:
                    for num_aleatorio in elegidos:
                        cur.execute("INSERT INTO compra_boletas (code) VALUES (%s)", (num_aleatorio,))
                        cur.execute("UPDATE grupo SET estado = 0 WHERE code = %s", (num_aleatorio,))

                    miConexion.commit()
 
                    # En lugar de renderizar la plantilla HTML, ahora devolvemos los números aleatorios como JSON
                    return jsonify({"numeros": elegidos})
    except pymysql.Error as e:
        return jsonify({"error": f"Error de base de datos: {e}"})

if __name__ == '__main__':
    app.run(debug=True)
