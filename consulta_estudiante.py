import streamlit as st
from supabase import create_client, Client

# --- CONEXIÓN ---
URL = "https://ecqjfkbo fhkjpbfnvecd.supabase.co".replace(" ", "")
KEY = "sb_publishable_cUHEtiaPg4y5MHsB8EXnAQ_LBEY99Ex"
sb = create_client(URL, KEY)

st.set_page_config(page_title="Consulta UNEFA", page_icon="🎓")
st.title("🎓 Sistema de Consulta de Notas")

# --- BUSCADOR POR CÉDULA ---
st.write("Introduce tu número de cédula para ver tus resultados.")
cedula_input = st.text_input("Número de Cédula:").strip()

if st.button("Buscar Notas"):
    if cedula_input:
        try:
            # Buscamos por cédula para que aparezcan los datos correctos
            res = sb.table("unefa_nube").select("*").eq("cedula", cedula_input).execute()
            
            if res.data:
                alumno = res.data[0]
                # Aquí es donde el sistema "te reconoce" por tu nombre
                st.success(f"✅ BIENVENIDO: {alumno['nombre']}")
                
                # Resumen de datos
                col1, col2 = st.columns(2)
                col1.metric("Sección", alumno['seccion'])
                col2.metric("Promedio Final", f"{alumno['nota_final']} / 20")
                
                # Tabla de notas
                st.subheader("📋 Calificaciones Detalladas")
                notas = {
                    "Evaluación": ["Nota 1", "Nota 2", "Nota 3", "Nota 4", "Nota 5"],
                    "Puntaje": [alumno['n1'], alumno['n2'], alumno['n3'], alumno['n4'], alumno['n5']]
                }
                st.table(notas)
            else:
                st.error("❌ Cédula no encontrada. Verifica los números e intenta de nuevo.")
        except Exception as e:
            st.error(f"Error de conexión: {e}")
    else:
        st.warning("Por favor, ingresa tu cédula primero.")
