import streamlit as st
from supabase import create_client, Client

# Conexión
URL = "https://ecqjfkbo fhkjpbfnvecd.supabase.co".replace(" ", "")
KEY = "sb_publishable_cUHEtiaPg4y5MHsB8EXnAQ_LBEY99Ex"
sb = create_client(URL, KEY)

st.set_page_config(page_title="Consulta UNEFA", page_icon="🎓")
st.title("🎓 Sistema de Consulta de Notas")

cedula_input = st.text_input("Ingresa tu Cédula para consultar:").strip()

if st.button("Buscar Notas"):
    if cedula_input:
        try:
            res = sb.table("unefa_nube").select("*").eq("cedula", cedula_input).execute()
            if res.data:
                alumno = res.data[0]
                st.success(f"✅ ESTUDIANTE: {alumno['nombre']}")
                
                # Aquí está la magia: Usa los nombres guardados en e1, e2...
                # Si no hay nombre guardado, pondrá "Evaluación X" por defecto.
                tabla_notas = {
                    "Materia / Evaluación": [
                        alumno.get('e1', 'Evaluación 1'), 
                        alumno.get('e2', 'Evaluación 2'), 
                        alumno.get('e3', 'Evaluación 3'), 
                        alumno.get('e4', 'Evaluación 4'), 
                        alumno.get('e5', 'Evaluación 5')
                    ],
                    "Puntaje": [alumno['n1'], alumno['n2'], alumno['n3'], alumno['n4'], alumno['n5']]
                }
                st.table(tabla_notas)
                st.metric("Promedio Final", f"{alumno['nota_final']} / 20")
            else:
                st.error("❌ Cédula no encontrada.")
        except Exception as e:
            st.error(f"Error de conexión: {e}")
