import streamlit as st
import pandas as pd
import plotly.express as px

# Cargar datos
df = pd.read_csv("employee_data.csv")

# Título y descripción
st.title("Análisis de Desempeño de Empleados - Socialize Your Knowledge")
st.markdown("""
Esta aplicación permite visualizar el rendimiento de los empleados usando distintos filtros.
""")

# Filtros
gender_filter = st.multiselect("Selecciona género(s):", df["gender"].unique(), default=df["gender"].unique())
performance_filter = st.slider("Puntaje de desempeño:", 1, 5, (1, 5))
marital_filter = st.multiselect("Estado civil:", df["marital_status"].unique(), default=df["marital_status"].unique())

# Aplicar filtros para gráficos generales
df_filtered = df[
    (df["gender"].isin(gender_filter)) &
    (df["performance_score"].between(*performance_filter)) &
    (df["marital_status"].isin(marital_filter))
]

st.markdown(f"**Total de registros que cumplen los filtros: {len(df_filtered)}**")

# Gráficos: 2 por fila
col1, col2 = st.columns(2)
with col1:
    st.subheader("Distribución del puntaje de desempeño")
    fig1 = px.histogram(df_filtered, x="performance_score", nbins=5, text_auto=True)
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    st.subheader("Promedio de horas trabajadas por género")
    df_horas = df[
        (df["performance_score"].between(*performance_filter)) &
        (df["marital_status"].isin(marital_filter))
    ]
    fig2 = px.bar(
        df_horas.groupby("gender")["average_work_hours"].mean().reset_index(),
        x="gender", y="average_work_hours", color="gender", text_auto=True,
        labels={"average_work_hours": "Horas promedio"},
        title="Horas trabajadas por género"
    )
    st.plotly_chart(fig2, use_container_width=True)

col3, col4 = st.columns(2)
with col3:
    st.subheader("Edad vs. Salario")
    fig3 = px.scatter(
        df_filtered, x="age", y="salary", color="position",
        hover_data=["name_employee", "gender"], title="Relación entre edad y salario"
    )
    st.plotly_chart(fig3, use_container_width=True)

with col4:
    st.subheader("Horas vs. Puntaje de desempeño")
    fig4 = px.box(
        df_filtered, x="performance_score", y="average_work_hours", points="all",
        labels={"average_work_hours": "Horas trabajadas"},
        title="Promedio de horas por desempeño"
    )
    st.plotly_chart(fig4, use_container_width=True)

# Conclusión
st.markdown("""
### Conclusión

Este dashboard permite una visión integral de cómo se relacionan los datos de desempeño con otras variables relevantes. 
Los filtros dinámicos ayudan a enfocar los análisis en diferentes perfiles.
""")