import streamlit as st
import pandas as pd
import re

# Variable global para almacenar el DataFrame
if 'df_conocimiento' not in st.session_state:
    st.session_state.df_conocimiento = pd.DataFrame(columns=['Oracion'])

def es_oracion_pasiva(oracion):
    if re.search(r'\b(?:será|serán|fue|fueron|está|están|ha|es|ser|estar)\b', oracion) and re.search(r'\b\w+(?:ado|ada|idos|idas|ido|ada|tos|tas|so|sa|sos|sas|cho|cha|chos|chas)\b', oracion):
        return True
    else:
        return False

def almacenar_en_dataframe(oracion, dataframe):
    dataframe = dataframe.append({'Oracion': oracion}, ignore_index=True)
    return dataframe

def mostrar_dataframe(dataframe):
    st.write("\nContenido del DataFrame:")
    st.write(dataframe)

def main():
    st.title('Análisis de Oraciones Pasivas')
    oracion_ingresada = st.text_input("Ingrese una oración:")

    if st.button("Agregar"):
        if es_oracion_pasiva(oracion_ingresada):
            st.session_state.df_conocimiento = almacenar_en_dataframe(oracion_ingresada, st.session_state.df_conocimiento)
            st.success("La oración es pasiva y ha sido almacenada en el DataFrame.")
        else:
            st.warning("La oración no es pasiva.")

    mostrar_dataframe(st.session_state.df_conocimiento)

if __name__ == "__main__":
    main()
