import streamlit as st

# Título de la aplicación
st.title("Hello, World!")

# Texto de bienvenida
st.write("¡Bienvenido a tu primera app con Streamlit!")

# Botón de interacción
if st.button("Haz clic aquí"):
    st.write("¡Hola, Streamlit!")

# Entrada de texto
nombre = st.text_input("¿Cuál es tu nombre?")
if nombre:
    st.write(f"¡Hola, {nombre}! Bienvenido a Streamlit.")
