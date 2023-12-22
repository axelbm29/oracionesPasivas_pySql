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

def eliminar_oracion_por_id(id):
    cursor.execute("DELETE FROM oraciones WHERE id=?", (id,))
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

    mostrar_oraciones()

    # Eliminar oraciones por ID en la barra lateral
    with st.sidebar:
        st.header("Eliminar Oración por ID")
        id_a_eliminar = st.number_input("Ingrese el ID de la oración a eliminar:", step=1)
        id_a_eliminar = int(id_a_eliminar)  # Convertir a entero explícitamente
        confirmado = st.checkbox("Confirmar eliminación")
        if st.button("Eliminar"):
            if confirmado:
                eliminar_oracion_por_id(id_a_eliminar)
                st.success(f"Oración con ID {id_a_eliminar} eliminada correctamente.")
            else:
                st.warning("Por favor, confirme la eliminación.")

if __name__ == "__main__":
    main()