import streamlit as st
import pandas as pd
import altair as alt

st.markdown("# Comparar horarios")
st.caption("Distribución promedio por franja horaria y evaluación de umbrales de demanda.")

# Verificar si los datos están cargados (R1 / R2)
if st.session_state.df is None:
    st.info("Ve a la página **Explorar los datos**, sube el archivo CSV y pulsa **Cargar datos** para comenzar.")
    st.stop()

# --- Aplicar filtros compartidos (R3) ---
df_filtrado = st.session_state.df.copy()

if st.session_state.tipo_dia != "Todos":
    df_filtrado = df_filtrado[df_filtrado["tipo_dia"] == st.session_state.tipo_dia]

hora_min, hora_max = st.session_state.rango_horas
df_filtrado = df_filtrado[
    (df_filtrado["hora"] >= hora_min) & (df_filtrado["hora"] <= hora_max)
]

mapa_columnas = {
    "Todos": "alquileres_total",
    "Ocasionales": "alquileres_ocasionales",
    "Registrados": "alquileres_registrados"
}
col_alquileres = mapa_columnas[st.session_state.tipo_usuario]
df_filtrado["alquileres"] = df_filtrado[col_alquileres]

if len(df_filtrado) == 0:
    st.warning("No hay registros que coincidan con los filtros seleccionados.")
    st.stop()

# --- R6: Dibujar el promedio de alquileres de cada hora ---
col_color, col_chk = st.columns([1, 2], vertical_alignment="bottom")
with col_color:
    # Control 8: st.color_picker
    color_barras = st.color_picker("Color de las barras", value="#00E5A8")
with col_chk:
    # Control 9: st.checkbox
    mostrar_tabla = st.checkbox("Mostrar tabla de promedios")

df_horas = (
    df_filtrado.groupby("hora", as_index=False)["alquileres"]
    .mean()
    .rename(columns={"alquileres": "promedio"})
    .sort_values("hora")
)

grafico_barras = (
    alt.Chart(df_horas)
    .mark_bar(color=color_barras, cornerRadiusTopLeft=5, cornerRadiusTopRight=5)
    .encode(
        x=alt.X("hora:O", title="Hora del día", axis=alt.Axis(labelAngle=0, grid=False, labelColor="#94A3B8", titleColor="#CBD5E1")),
        y=alt.Y("promedio:Q", title="Alquileres por hora observada", axis=alt.Axis(gridColor="#1E293B", labelColor="#94A3B8", titleColor="#CBD5E1")),
        tooltip=[
            alt.Tooltip("hora:O", title="Hora"),
            alt.Tooltip("promedio:Q", title="Promedio", format=".1f")
        ]
    )
    .properties(height=360)
    .configure_view(strokeWidth=0)
)
st.altair_chart(grafico_barras, use_container_width=True)

if mostrar_tabla:
    df_tabla_promedios = df_horas.copy()
    df_tabla_promedios["Hora formateada"] = df_tabla_promedios["hora"].apply(lambda h: f"{int(h):02d}:00")
    df_tabla_promedios["Promedio"] = df_tabla_promedios["promedio"].round(2)
    st.dataframe(
        df_tabla_promedios[["Hora formateada", "Promedio"]],
        use_container_width=True,
        hide_index=True
    )

st.divider()

# --- R7: Identificar las horas cuyo promedio supera el límite ---
col_num, col_res = st.columns([1, 2], vertical_alignment="center")

with col_num:
    # Control 10: st.number_input
    limite = st.number_input(
        "Límite de alquileres por hora",
        min_value=0,
        value=250,
        step=10
    )

horas_superan = df_horas[df_horas["promedio"] > limite]["hora"].tolist()
total_horas_con_datos = len(df_horas)

with col_res:
    st.metric(
        label="Horarios con promedio mayor que el límite",
        value=f"{len(horas_superan)}/{total_horas_con_datos}"
    )

if len(horas_superan) > 0:
    lista_formateada = ", ".join([f"{int(h):02d}:00" for h in horas_superan])
    st.info(f"**Horarios:** {lista_formateada}.")
else:
    st.info("**Horarios:** Ninguno.")