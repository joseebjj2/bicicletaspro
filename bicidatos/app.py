import streamlit as st

st.set_page_config(
    page_title="VELO // Analytics",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilos CSS minimalistas 2026 (tarjetas glass/dark y tipografía limpia)
st.markdown("""
<style>
    /* Reducir espacio superior innecesario */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    /* Estilo aesthetic para tarjetas de métricas (KPIs) */
    div[data-testid="stMetric"] {
        background-color: #131A26;
        border: 1px solid #1E293B;
        padding: 18px 22px;
        border-radius: 14px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.25);
    }
    div[data-testid="stMetric"] label {
        color: #94A3B8 !important;
        font-size: 0.85rem !important;
        letter-spacing: 0.04em;
        text-transform: uppercase;
    }
    div[data-testid="stMetricValue"] {
        color: #F8FAFC !important;
        font-weight: 700 !important;
    }
    /* Suavizar bordes de botones */
    .stButton > button, .stDownloadButton > button, .stLinkButton > a {
        border-radius: 10px !important;
        font-weight: 500 !important;
        transition: all 0.2s ease;
    }
    /* Línea divisoria sutil */
    hr {
        border-color: #1E293B;
    }
</style>
""", unsafe_allow_html=True)

# Inicializar variables de estado (R1 y R3)
if "df" not in st.session_state:
    st.session_state.df = None
if "tipo_usuario" not in st.session_state:
    st.session_state.tipo_usuario = "Todos"
if "tipo_dia" not in st.session_state:
    st.session_state.tipo_dia = "Todos"
if "rango_horas" not in st.session_state:
    st.session_state.rango_horas = (0, 23)

# Definir las dos páginas (R2)
pagina_explorar = st.Page(
    "paginas/explorar.py",
    title="Explorar los datos",
    icon=":material/analytics:",
    default=True
)
pagina_comparar = st.Page(
    "paginas/comparar.py",
    title="Comparar horarios",
    icon=":material/bar_chart:"
)

pg = st.navigation([pagina_explorar, pagina_comparar])

# Barra lateral minimalista (R3)
with st.sidebar:
    st.markdown("## ⚡ VELO `2026`")
    st.caption("URBAN MOBILITY INTELLIGENCE")
    st.divider()
    
    st.markdown("##### PARÁMETROS DE FILTRO")
    
    # Control 3: st.selectbox
    st.session_state.tipo_usuario = st.selectbox(
        "Tipo de usuario",
        options=["Todos", "Ocasionales", "Registrados"],
        index=["Todos", "Ocasionales", "Registrados"].index(st.session_state.tipo_usuario)
    )
    
    # Control 4: st.radio
    st.session_state.tipo_dia = st.radio(
        "Tipo de día",
        options=["Todos", "Laborable", "No laborable"],
        index=["Todos", "Laborable", "No laborable"].index(st.session_state.tipo_dia)
    )
    
    # Control 5: st.slider
    st.session_state.rango_horas = st.slider(
        "Horas del día",
        min_value=0,
        max_value=23,
        value=st.session_state.rango_horas
    )

pg.run()