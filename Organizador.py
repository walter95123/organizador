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

# Organiza los pasos
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

# Muestra pasos con checkboxes en la misma fila
def mostrar_pasos_con_checks(pasos):
    for id_paso, contenido in pasos:
        cols = st.columns([0.9, 0.1])
        if id_paso == "⚠️":
            cols[0].markdown(f"⚠️ `{contenido}`")
        else:
            indent = "&nbsp;" * (calcular_indentacion(id_paso) * 4)
            cols[0].markdown(f"{indent}- **{id_paso}** {contenido}", unsafe_allow_html=True)
            cols[1].checkbox("", key=id_paso)



# Guardar texto en archivo
def exportar_txt(pasos):
    return "\n".join(f"{id_paso} {contenido}" for id_paso, contenido in pasos)

# Mostrar resultado
if st.button("📄 Organizar y mostrar pasos"):
    if texto:
        pasos_organizados = organizar_pasos(texto)
        st.markdown("---")
        mostrar_pasos_con_checks(pasos_organizados)
        contenido = exportar_txt(pasos_organizados)
        st.download_button("💾 Guardar como TXT", contenido, file_name="guia_tecnica.txt")
    else:
        st.warning("Pegá una lista primero.")

# Cargar archivo externo
st.markdown("---")
st.subheader("📂 O cargar un archivo .txt con pasos:")

archivo_subido = st.file_uploader("Elegí un archivo .txt", type=["txt"])

if archivo_subido:
    contenido_archivo = archivo_subido.read().decode("utf-8")
    pasos_archivo = organizar_pasos(contenido_archivo)
    st.markdown("### ✅ Pasos desde el archivo:")
    mostrar_pasos_con_checks(pasos_archivo)
