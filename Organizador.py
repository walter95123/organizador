import streamlit as st

st.title("✅ Organizador de Tareas")
st.write("Pegá acá tus pasos técnicos, guías o procedimientos.")

# Variable de estado para guardar tareas
if "tareas" not in st.session_state:
    st.session_state.tareas = []

# Entrada de nueva tarea
nueva_tarea = st.text_input("📌 Escribí una nueva tarea:")

# Botón para agregarla
if st.button("Agregar tarea"):
    if nueva_tarea:
        st.session_state.tareas.append(nueva_tarea)
        st.success("Tarea agregada.")
    else:
        st.warning("Escribí algo antes de agregar.")

# Mostrar tareas actuales
st.subheader("📋 Lista de tareas:")
for i, tarea in enumerate(st.session_state.tareas, 1):
    st.write(f"{i}. {tarea}")