import streamlit as st
import os
import re
import urllib.parse

st.set_page_config(page_title="Ammi - Accesorios y Joyas", layout="wide")

# Inicializar carrito en la sesión
if "carrito" not in st.session_state:
    st.session_state.carrito = {}

# Encabezado con logo y título
col1, col2 = st.columns([1, 5])
with col1:
    st.image("logo.png", width=150)
with col2:
    st.title("Nuestro Catálogo")

# Dirección
st.markdown("<p style='font-size:16px; color: gray;'>Bucaramanga</p>", unsafe_allow_html=True)
# Cargar catálogo
carpeta = "catalogo"
extensiones_validas = (".png", ".jpg", ".jpeg", ".webp", ".jfif")
imagenes = [f for f in os.listdir(carpeta) if f.lower().endswith(extensiones_validas)]
imagenes.sort()

catalogo = {}
tipos_disponibles = set()

for i, archivo in enumerate(imagenes):
    nombre_archivo = os.path.splitext(archivo)[0]
    partes = re.split(r"\s*-\s*", nombre_archivo)
    if len(partes) != 3:
        continue  # Ignorar si no cumple con el formato

    tipo = partes[0].strip()
    nombre = partes[1].strip()
    try:
        precio = int(partes[2].strip())
    except ValueError:
        continue  # Ignorar si el precio no es un número

    producto_id = f"item_{i}"
    catalogo[producto_id] = {
        "producto_id": producto_id,
        "archivo": archivo,
        "tipo": tipo,
        "nombre": nombre,
        "precio": precio
    }

    tipos_disponibles.add(tipo)

# Filtro por tipo
tipos_ordenados = sorted(tipos_disponibles)
tipo_seleccionado_filtro = st.selectbox("Filtrar por tipo", ["Todos"] + tipos_ordenados)

# Mostrar catálogo
for producto_id, item in catalogo.items():
    tipo = item["tipo"]
    nombre = item["nombre"]
    precio = item["precio"]
    archivo = item["archivo"]

    if tipo_seleccionado_filtro != "Todos" and tipo != tipo_seleccionado_filtro:
        continue

    col_img, col_info = st.columns([2, 3])
    with col_img:
        st.image(os.path.join(carpeta, archivo), width=350)
    with col_info:
        precio_formateado = "{:,.0f}".format(precio).replace(",", ".")
        st.markdown(f"### {nombre}")
        st.markdown(f"<h4 style='color: green;'>${precio_formateado}</h4>", unsafe_allow_html=True)

    st.markdown("---")