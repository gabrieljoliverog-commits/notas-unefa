           import streamlit as st
from supabase import create_client, Client

# --- CONEXIÓN A TU NUBE ---
URL = "https://ecqjfkbo fhkjpbfnvecd.supabase.co".replace(" ", "")
KEY = "sb_publishable_cUHEtiaPg4y5MHsB8EXnAQ_LBEY99Ex"
sb = create_client(URL, KEY)

# Configuración de página
st.set_page_config(page_title="Consulta UNEFA", page_icon="🎓")
st.title("🎓 Sistema de Consulta de Notas")

# --- BUSCADOR POR CÉDULA ---
st.write("Escribe tu número de cédula para consultar tus resultados.")
cedula_input = st.text_input("Número de Cédula (V-XXXXXXXX):").strip()

if st.button("Buscar Notas"):
    if cedula_input:
        try:
            # Buscamos en la columna 'cedula' que acabas de crear en Supabase
            res = sb.table("unefa_nube").select("*").eq("cedula", cedula_input).execute()
            
            if res.data:
                alumno = res.data[0]
                # AQUÍ APARECE EL NOMBRE AUTOMÁTICAMENTE
                st.success(f"✅ REGISTRO ENCONTRADO: {alumno['nombre']}")
                
                # Cuadro de información principal
                st.info(f"📍 Sección: {alumno['seccion']} | 📊 Promedio Final: {alumno['nota_final']}")
                
                # Tabla detallada de sus notas
                st.subheader("📋 Detalle de Calificaciones")
                notas_detalladas = {
                    "Evaluación": ["Nota 1", "Nota 2", "Nota 3", "Nota 4", "Nota 5"],
                    "Puntaje": [alumno['n1'], alumno['n2'], alumno['n3'], alumno['n4'], alumno['n5']]
                }
                st.table(notas_detalladas)
                
            else:
                st.error("❌ No encontramos ninguna cédula que coincida. Verifica los números.")
        except Exception as e:
            st.error(f"Hubo un problema de conexión: {e}")
    else:
        st.warning("Debes ingresar un número de cédula para buscar.")  
