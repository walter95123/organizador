import streamlit as st
import re


st.title("📘 Organizador de Guías Técnicas")

st.subheader("📥 Pegá tu lista de pasos (uno por línea):")
texto = st.text_area("")

def calcular_indentacion(id_paso):
    # Detecta niveles según formato: 1, 1.1, 1.1a, etc.
    id_limpio = re.sub(r'[^\d\.]', '', id_paso)  # elimina letras (como la "a")
    nivel = id_limpio.count('.')
    if re.search(r'[a-zA-Z]$', id_paso):
        nivel += 1  # si termina en letra, subnivel más
    return nivel

def formatear_pasos(texto):
    lineas = texto.strip().split('\n')
    salida = ""
    for linea in lineas:
        match = re.match(r'^([0-9]+(?:\.[0-9]+)*[a-z]?)\s+(.*)', linea.strip())
        if match:
            id_paso = match.group(1)
            contenido = match.group(2)
            indentacion = "   " * calcular_indentacion(id_paso)
            salida += f"{indentacion}- **{id_paso}** {contenido}\n"
        elif linea.strip() != "":
            salida += f"\n⚠️ Línea sin ID reconocida: `{linea.strip()}`\n"
    return salida

if st.button("📄 Organizar y mostrar pasos"):
    if texto:
        st.markdown("---")
        st.markdown(formatear_pasos(texto))
    else:
        st.warning("Pegá una lista primero.")

import io

pasos_organizados = []

if st.button("📄 Organizar y mostrar pasos"):
    if texto:
        pasos_organizados = organizar_pasos(texto)
        markdown_resultado = generar_markdown(pasos_organizados)
        st.markdown("---")
        st.markdown(markdown_resultado)

        # Mostrar botón para guardar como TXT
        contenido = "\n".join(linea for _, linea in pasos_organizados)
        st.download_button("💾 Guardar como TXT", contenido, file_name="guia_tecnica.txt")
    else:
        st.warning("Pegá una lista primero.")