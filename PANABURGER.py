import streamlit as st
import pandas as pd
from datetime import datetime
import os

# Configuración de la página
st.set_page_config(page_title="Punto de Venta - Hamburguesería", page_icon="🍔", layout="centered")

# Precios de las 5 hamburguesas (Modifica los nombres y precios a tu gusto)
MENU = {
    "Hamburguesa Clásica": 5.00,
    "Hamburguesa con Queso": 6.00,
    "Hamburguesa Bacon/Tocino": 7.50,
    "Hamburguesa Doble Carne": 9.00,
    "Hamburguesa Veggie": 6.50
}

# Nombre del archivo donde se guardarán los datos
ARCHIVO_DATOS = "ventas_hamburguesas.csv"

# Función para cargar los datos existentes
def cargar_datos():
    if os.path.exists(ARCHIVO_DATOS):
        return pd.read_csv(ARCHIVO_DATOS)
    else:
        return pd.DataFrame(columns=["Fecha/Hora", "Hamburguesa", "Cantidad", "Precio Unitario", "Total", "Metodo Pago"])

# Inicializar los datos en la sesión
if "df_ventas" not in st.session_state:
    st.session_state.df_ventas = cargar_datos()

st.title("🍔 Sistema de Ventas Súper Fácil")
st.write("Registra las ventas de tu amigo en segundos para empezar a generar datos.")

# --- FORMULARIO DE VENTA ---
st.subheader("📝 Registrar Nueva Venta")

col1, col2 = st.columns(2)

with col1:
    hamburguesa_sel = st.selectbox("Selecciona la hamburguesa:", list(MENU.keys()))
    cantidad = st.number_input("Cantidad:", min_value=1, max_value=20, value=1, step=1)

with col2:
    precio_unitario = MENU[hamburguesa_sel]
    st.metric(label="Precio Unitario", value=f"${precio_unitario:.2f}")
    metodo_pago = st.selectbox("Método de Pago:", ["Efectivo", "Tarjeta", "Transferencia"])

# Calcular total de la venta actual
total_venta = precio_unitario * cantidad
st.subheader(f"Total a Cobrar: :green[${total_venta:.2f}]")

# Botón para registrar
if st.button("💾 Registrar Venta", use_container_width=True):
    nueva_fila = {
        "Fecha/Hora": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "Hamburguesa": hamburguesa_sel,
        "Cantidad": cantidad,
        "Precio Unitario": precio_unitario,
        "Total": total_venta,
        "Metodo Pago": metodo_pago
    }
    
    # Agregar a la sesión y guardar en el archivo CSV
    st.session_state.df_ventas = pd.concat([st.session_state.df_ventas, pd.DataFrame([nueva_fila])], ignore_index=True)
    st.session_state.df_ventas.to_csv(ARCHIVO_DATOS, index=False)
    st.success("¡Venta registrada con éxito!")



# --- VISUALIZADOR DE DATOS ---
st.subheader("📊 Historial de Ventas y Datos Generados")

if not st.session_state.df_ventas.empty:
    # Mostrar tabla con los datos
    st.dataframe(st.session_state.df_ventas, use_container_width=True)
    
    # Pequeño resumen de métricas
    total_recaudado = st.session_state.df_ventas["Total"].sum()
    total_hamburguesas = st.session_state.df_ventas["Cantidad"].sum()
    
    m_col1, m_col2 = st.columns(2)
    m_col1.metric("Ingresos Totales", f"${total_recaudado:.2f}")
    m_col2.metric("Hamburguesas Vendidas", int(total_hamburguesas))
    
    # Gráfico simple de las hamburguesas más vendidas
    st.write("### ¿Cuál es la que más se vende?")
    ventas_por_producto = st.session_state.df_ventas.groupby("Hamburguesa")["Cantidad"].sum()
    st.bar_chart(ventas_por_producto)
    
    # Botón para descargar el Excel directamente si quiere
    csv_data = st.session_state.df_ventas.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Descargar datos para Excel (CSV)",
        data=csv_data,
        file_name="ventas_restaurante.csv",
        mime="text/csv",
    )
else:
    st.info("Aún no hay ventas registradas hoy. ¡Registra la primera arriba!")