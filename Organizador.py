import streamlit as st
import re
import io

st.title("📘 Organizador de Guías Técnicas")
st.subheader("📥 Pegá tu lista de pasos (uno por línea):")
texto = st.text_area("")

# Función que calcula la indentación según ID
def calcular_indentacion(id_paso):
    id_limpio = re.sub(r'[^\d\.]', '', id_paso)
    nivel = id_limpio.count('.')
    if re.search(r'[a-zA-Z]$', id_paso):
        nivel += 1
    return nivel

# Función que organiza los pasos
def organizar_pasos(texto):
    lineas = texto.strip().split('\n')
    pasos = []
    for linea in lineas:
        match = re.match(r'^([0-9]+(?:\.[0-9]+)*[a-z]?)\s+(.*)', linea.strip())
        if match:
            pasos.append((match.group(1), match.group(2)))
        elif linea.strip() != "":
            pasos.append(("⚠️", f"Línea sin ID reconocida: {linea.strip()}"))
    return pasos

# Función que los muestra con markdown
def generar_markdown(pasos):
    salida = ""
    for id_paso, contenido in pasos:
        if id_paso == "⚠️":
            salida += f"\n⚠️ `{contenido}`\n"
        else:
            indentacion = "   " * calcular_indentacion(id_paso)
            salida += f"{indentacion}- **{id_paso}** {contenido}\n"
    return salida

# Procesar y mostrar
if st.button("📄 Organizar y mostrar pasos"):
    if texto:
        pasos_organizados = organizar_pasos(texto)
        markdown_resultado = generar_markdown(pasos_organizados)
        st.markdown("---")
        st.markdown(markdown_resultado)

        # Botón para guardar .txt
        contenido = "\n".join(f"{id_paso} {linea}" for id_paso, linea in pasos_organizados)

        st.download_button("💾 Guardar como TXT", contenido, file_name="guia_tecnica.txt")
    else:
        st.warning("Pegá una lista primero.")

# --- Cargar archivo desde el dispositivo ---
st.markdown("---")
st.subheader("📂 O cargar un archivo .txt con pasos:")

archivo_subido = st.file_uploader("Elegí un archivo .txt", type=["txt"])

if archivo_subido:
    contenido_archivo = archivo_subido.read().decode("utf-8")
    pasos_archivo = organizar_pasos(contenido_archivo)
    markdown_archivo = generar_markdown(pasos_archivo)
    st.markdown("### ✅ Pasos desde el archivo:")
    st.markdown(markdown_archivo)
