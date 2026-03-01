import streamlit as st
from supabase import create_client, Client
import unicodedata

# --- EL ESCUDO DE LIMPIEZA (Para que la web ignore espacios y acentos) ---
def limpiar(t):
    if not t: return ""
    # Borra espacios dobles y finales, y pone todo en MAYÚSCULAS
    t = " ".join(t.split()).upper()
    # Elimina tildes y acentos
    return ''.join(c for c in unicodedata.normalize('NFD', t) if unicodedata.category(c) != 'Mn')

# --- CONFIGURACIÓN (Tus llaves de Supabase) ---
URL_NUBE = "https://ecqjfkbo fhkjpbfnvecd.supabase.co".replace(" ", "")
KEY_NUBE = "sb_publishable_cUHEtiaPg4y5MHsB8EXnAQ_LBEY99Ex"
supabase: Client = create_client(URL_NUBE, KEY_NUBE)

st.set_page_config(page_title="Consulta UNEFA", page_icon="🎓")

st.title("🎓 Sistema de Consulta de Notas")
st.write("Escribe tu nombre completo para ver tus resultados actuales.")

# Buscador con LIMPIEZA AUTOMÁTICA
nombre_sucio = st.text_input("Nombre del Estudiante:")
nombre_buscado = limpiar(nombre_sucio)

if st.button("Buscar Notas"):
    if nombre_buscado:
        # Consultamos a la nube usando el nombre ya limpio
        try:
            res = supabase.table("unefa_nube").select("*").eq("nombre", nombre_buscado).execute()
            
            if res.data:
                alumno = res.data[0]
                st.success(f"### Estudiante: {alumno['nombre']}")
                
                # Resumen en tarjetas
                c1, c2, c3 = st.columns(3)
                c1.metric("Sección", alumno['seccion'])
                c2.metric("Promedio", f"{alumno['nota_final']} / 20")
                estado = "APROBADO ✅" if alumno['nota_final'] >= 10 else "REPROBADO ❌"
                c3.write(f"**Estado:** \n### {estado}")

                # Tabla de detalles
                st.write("---")
                st.write("**Desglose de notas por corte:**")
                detalles = {
                    "Evaluación": ["Nota 1", "Nota 2", "Nota 3", "Nota 4", "Nota 5"],
                    "Puntaje": [alumno['n1'], alumno['n2'], alumno['n3'], alumno['n4'], alumno['n5']]
                }
                st.table(detalles)
            else:
                st.error("No se encontró ningún registro. Intenta sin acentos o revisa los espacios.")
        except Exception as e:
            st.error(f"Error de conexión: {e}")
    else:
        st.warning("Escribe un nombre antes de buscar.")
