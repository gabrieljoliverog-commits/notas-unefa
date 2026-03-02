import streamlit as st
from supabase import create_client, Client

# Conexión
URL = "https://ecqjfkbo fhkjpbfnvecd.supabase.co".replace(" ", "")
KEY = "sb_publishable_cUHEtiaPg4y5MHsB8EXnAQ_LBEY99Ex"
sb = create_client(URL, KEY)

# Configuración con Estilo Profesional
st.set_page_config(page_title="UNEFA - Consulta de Notas", page_icon="🎓", layout="centered")

# Estilo CSS personalizado para colores UNEFA (Azul y Dorado)
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stButton>button { width: 100%; border-radius: 20px; background-color: #003366; color: white; }
    .report-card { background-color: white; padding: 20px; border-radius: 15px; border-left: 8px solid #003366; box-shadow: 2px 2px 10px rgba(0,0,0,0.1); }
    </style>
    """, unsafe_allow_html=True)

st.title("🎓 Portal de Calificaciones UNEFA")
st.info("Bienvenido al sistema de consulta. Introduce tus datos para generar tu boleta digital.")

with st.container():
    cedula_input = st.text_input("🆔 Número de Cédula:", placeholder="Ej: 12345678").strip()
    boton = st.button("Consultar Expediente")

if boton:
    if cedula_input:
        res = sb.table("unefa_nube").select("*").eq("cedula", cedula_input).execute()
        if res.data:
            alumno = res.data[0]
            
            # --- DISEÑO DE TARJETA DE ESTUDIANTE ---
            st.markdown(f"""
            <div class="report-card">
                <h2 style='color: #003366; margin-bottom: 0;'>{alumno['nombre']}</h2>
                <p style='color: #666;'>Cédula: {alumno['cedula']} | Sección: {alumno['seccion']}</p>
                <hr>
                <h3 style='text-align: center; color: #1f77b4;'>Promedio: {alumno['nota_final']} / 20</h3>
            </div>
            """, unsafe_allow_html=True)

            st.write("### 📋 Desglose de Evaluaciones")
            
            # Columnas para las notas (más visual)
            col1, col2 = st.columns(2)
            evals = [alumno.get('e1','Ev 1'), alumno.get('e2','Ev 2'), alumno.get('e3','Ev 3'), alumno.get('e4','Ev 4'), alumno.get('e5','Ev 5')]
            notas = [alumno['n1'], alumno['n2'], alumno['n3'], alumno['n4'], alumno['n5']]

            for i in range(5):
                with col1 if i < 3 else col2:
                    st.metric(label=evals[i], value=f"{notas[i]} pts")
            
            st.caption("Nota: Estas calificaciones son de carácter informativo.")
        else:
            st.error("Cédula no registrada en el sistema.")
