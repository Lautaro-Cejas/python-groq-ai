import os
import sys
import sqlite3
from dotenv import load_dotenv
from groq import Groq

# 1. Cargar variables de entorno
load_dotenv()

# 2. Configuración de Groq
client = Groq(
    api_key=os.getenv("GROQ_API_KEY"),
)

# 3. Configuración de la base de datos SQLite en memoria
# Usamos check_same_thread=False para evitar problemas en scripts simples, 
# aunque no es estrictamente necesario aquí.
conn = sqlite3.connect(':memory:', check_same_thread=False)

# Configurar para que los resultados parezcan JSON (diccionarios) en lugar de tuplas
def dict_factory(cursor, row):
    fields = [column[0] for column in cursor.description]
    return {key: value for key, value in zip(fields, row)}

conn.row_factory = dict_factory
cursor = conn.cursor()

# 4. Crear tabla y poblar datos
# En Python ejecutamos el SQL directamente
cursor.execute("CREATE TABLE productos (id INTEGER, nombre TEXT, precio REAL, stock INTEGER)")

# Insertar datos de ejemplo
datos_iniciales = [
    (1, "Laptop Gamer", 1500.00, 5),
    (2, "Mouse Inalámbrico", 25.50, 100),
    (3, "Teclado Mecánico", 85.00, 30),
    (4, "Monitor 4K", 450.00, 12)
]
cursor.executemany("INSERT INTO productos VALUES (?, ?, ?, ?)", datos_iniciales)
conn.commit() # ¡Importante guardar cambios en Python!

def preguntar_a_data(pregunta_usuario):
    print(f"\n🤖 Usuario pregunta: \"{pregunta_usuario}\"")

    prompt_sistema = """
    Eres un experto en SQL. Tienes una tabla llamada 'productos' con las columnas: id, nombre, precio, stock.
    Tu trabajo es convertir la pregunta del usuario en una consulta SQL QUERY válida (Usa SIEMPRE 'LIKE' con % para búsquedas de texto) para SQLite.
    IMPORTANTE: Devuelve SOLO el código SQL puro. No uses bloques de código markdown (```). No des explicaciones.
    """

    try:
        # Generar la consulta SQL usando Groq
        chat_completion = client.chat.completions.create(
            messages=[
                { "role": "system", "content": prompt_sistema },
                { "role": "user", "content": pregunta_usuario }
            ],
            model="llama-3.1-8b-instant",
            temperature=0,
        )

        sql_query = chat_completion.choices[0].message.content or ""
        
        # Limpieza de markdown (igual que tu regex en JS)
        sql_query = sql_query.replace("```sql", "").replace("```", "").strip()
        
        print(f"⚡ IA generó SQL: {sql_query}")

        # Ejecutar la consulta SQL en la base de datos
        try:
            cursor.execute(sql_query)
            
            # Verificar si la query devuelve datos (es un SELECT)
            if cursor.description:
                resultados = cursor.fetchall()
                print("📊 Resultado de la DB:", resultados)
            else:
                # Es un INSERT/UPDATE/DELETE
                conn.commit()
                print("📊 Acción ejecutada correctamente (sin retorno de datos).")
                
        except sqlite3.Error as db_error:
            print(f"❌ Error en la query SQL: {db_error}")

    except Exception as e:
        print(f"Error conectando con la IA: {e}")

# Bloque principal de ejecución (equivalente a tu IIFE async)
if __name__ == "__main__":
    # Tomar argumentos de la línea de comandos
    # sys.argv[0] es el nombre del script, así que tomamos desde el 1
    args = sys.argv[1:]
    pregunta_usuario = " ".join(args)

    if not pregunta_usuario:
        print("Por favor, proporciona una pregunta como argumento.")
        print('Ejemplo: python main.py "cuantos teclados quedan?"')
        sys.exit(1)

    preguntar_a_data(pregunta_usuario)