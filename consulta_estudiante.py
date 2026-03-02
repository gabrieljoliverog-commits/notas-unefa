import streamlit as st
from supabase import create_client, Client

# --- CONEXIÓN ---
URL = "https://ecqjfkbo fhkjpbfnvecd.supabase.co".replace(" ", "")
KEY = "sb_publishable_cUHEtiaPg4y5MHsB8EXnAQ_LBEY99Ex"
sb = create_client(URL, KEY)

# Configuración con Estilo Profesional y Personal
st.set_page_config(page_title="Control de Notas - Prof. Gabriel Olivero", page_icon="👨‍🏫")

# Estilo visual mejorado
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stButton>button { width: 100%; border-radius: 10px; background-color: #004085; color: white; height: 3em; font-weight: bold; }
    .card { background-color: white; padding: 25px; border-radius: 15px; border-top: 5px solid #004085; box-shadow: 0 4px 6px rgba(0,0,0,0.1); margin-bottom: 20px; }
    </style>
    """, unsafe_allow_html=True)

st.title("👨‍🏫 Control de Notas Académicas")
st.markdown("### **Prof. Gabriel Olivero**")

# Mensaje de aclaratoria sobre el sistema
st.info("Este portal es una herramienta de transparencia para el seguimiento de sus evaluaciones. Las notas definitivas serán cargadas en el sistema institucional SICEAU.")

with st.container():
    cedula_input = st.text_input("🆔 Ingrese su Cédula para consultar:", placeholder="Ej: 12345678").strip()
    if st.button("Consultar Mi Progreso"):
        if cedula_input:
            try:
                res = sb.table("unefa_nube").select("*").eq("cedula", cedula_input).execute()
                if res.data:
                    alumno = res.data[0]
                    
                    # Tarjeta de Identificación
                    st.markdown(f"""
                    <div class="card">
                        <h2 style='color: #004085; margin-top: 0;'>{alumno['nombre']}</h2>
                        <p style='font-size: 1.1em;'><b>Sección:</b> {alumno['seccion']} | <b>Cédula:</b> {alumno['cedula']}</p>
                        <h3 style='text-align: right; color: #28a745;'>Promedio Actual: {alumno['nota_final']} / 20</h3>
                    </div>
                    """, unsafe_allow_html=True)

                    st.write("### 📋 Detalle de Evaluaciones")
                    
                    # Mostrar las evaluaciones con sus nombres reales
                    col1, col2 = st.columns(2)
                    evals = [alumno.get('e1','Nota 1'), alumno.get('e2','Nota 2'), alumno.get('e3','Nota 3'), alumno.get('e4','Nota 4'), alumno.get('e5','Nota 5')]
                    notas = [alumno['n1'], alumno['n2'], alumno['n3'], alumno['n4'], alumno['n5']]

                    for i in range(5):
                        with col1 if i % 2 == 0 else col2:
                            st.metric(label=evals[i], value=f"{notas[i]} / 20")
                    
                else:
                    st.error("Cédula no encontrada. Verifique el número e intente de nuevo.")
            except Exception as e:
                st.error(f"Error al conectar con la base de datos: {e}")

st.divider()
st.caption("Sistema de gestión docente independiente.")
