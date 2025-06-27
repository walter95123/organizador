import streamlit as st
import re

st.title("📘 Organizador de Guías Técnicas")

st.subheader("📥 Pegá tu lista de pasos (uno por línea):")
texto = st.text_area("")

def calcular_indentacion(id_paso):
    # Cuenta cuántos niveles tiene el ID (1 → 0, 1.1 → 1, 1.1a → 2)
    if re.match(r'^\d+[a-z]$', id_paso): return 2
    return id_paso.count('.')

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