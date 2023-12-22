import pandas as pd
import re

def es_oracion_pasiva(oracion):
    if re.search(r'\b(?:será|serán|fue|fueron|está|están|ha|es|ser|estar)\b', oracion) and re.search(r'\b\w+(?:ado|ada|idos|idas|ido|ada|tos|tas|so|sa|sos|sas|cho|cha|chos|chas)\b', oracion):
        return True
    else:
        return False

def almacenar_en_dataframe(oracion, dataframe):
    dataframe = dataframe.append({'Oracion': oracion}, ignore_index=True)
    return dataframe

def mostrar_dataframe(dataframe):
    print("\nContenido del DataFrame:")
    print(dataframe)

def main():
    df_conocimiento = pd.DataFrame(columns=['Oracion'])

    while True:
        print("\n--- MENÚ ---")
        print("1. Agregar oración pasiva")
        print("2. Ver contenido del DataFrame")
        print("3. Salir")

        opcion = input("Ingrese el número de la opción que desea: ")

        if opcion == "1":
            oracion_ingresada = input("Ingrese una oración: ")
            if es_oracion_pasiva(oracion_ingresada):
                df_conocimiento = almacenar_en_dataframe(oracion_ingresada, df_conocimiento)
                print("La oración es pasiva y ha sido almacenada en el DataFrame.")
            else:
                print("La oración no es pasiva.")

        elif opcion == "2":
            mostrar_dataframe(df_conocimiento)

        elif opcion == "3":
            print("Saliendo...")
            break

        else:
            print("Opción no válida. Por favor, ingrese un número válido.")

if __name__ == "__main__":
    main()
