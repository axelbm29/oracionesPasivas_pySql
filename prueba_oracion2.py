import streamlit as st
import pandas as pd
import re
import sqlite3

# Conexión a la base de datos SQLite
conn = sqlite3.connect('datos_oraciones.db')
cursor = conn.cursor()

# Crear la tabla si no existe
cursor.execute('''
    CREATE TABLE IF NOT EXISTS oraciones (
        id INTEGER PRIMARY KEY,
        oracion TEXT
    )
''')
conn.commit()

def es_oracion_pasiva(oracion):
    if re.search(r'\b(?:será|serán|fue|fueron|está|están|ha|es|ser|estar)\b', oracion) and re.search(r'\b\w+(?:ado|ada|idos|idas|ido|ada|tos|tas|so|sa|sos|sas|cho|cha|chos|chas)\b', oracion):
        return True
    else:
        return False

def almacenar_en_bd(oracion):
    cursor.execute("INSERT INTO oraciones (oracion) VALUES (?)", (oracion,))
    conn.commit()

def eliminar_oracion(id_oracion):
    cursor.execute("DELETE FROM oraciones WHERE id=?", (id_oracion,))
    conn.commit()

def mostrar_oraciones():
    cursor.execute("SELECT * FROM oraciones")
    rows = cursor.fetchall()
    df = pd.DataFrame(rows, columns=['ID', 'Oracion'])
    st.write("\nContenido de la Base de Datos:")
    st.write(df)

def main():
    st.title('Análisis de Oraciones Pasivas')
    oracion_ingresada = st.text_input("Ingrese una oración:")

    if st.button("Agregar"):
        if es_oracion_pasiva(oracion_ingresada):
            almacenar_en_bd(oracion_ingresada)
            st.success("La oración es pasiva y ha sido almacenada en la Base de Datos.")
        else:
            st.warning("La oración no es pasiva.")

    # Sección para eliminar oraciones
    if st.button("Eliminar última oración"):
        cursor.execute("SELECT MAX(id) FROM oraciones")
        max_id = cursor.fetchone()[0]
        if max_id:
            eliminar_oracion(max_id)
            st.success("La última oración ha sido eliminada.")
        else:
            st.warning("No hay oraciones para eliminar.")

    mostrar_oraciones()

if __name__ == "__main__":
    main()
