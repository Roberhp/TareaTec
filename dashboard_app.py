import pandas as pd
import plotly.express as px
import streamlit as st

# Cargar datos
df = pd.read_csv("employee_data.csv")

# Título y descripción
st.title("Análisis de Desempeño de los Colaboradores")
st.markdown("Este dashboard permite explorar datos clave del personal de Socialize your Knowledge, facilitando la toma de decisiones basadas en desempeño, género y otros atributos laborales.")

# Logo
st.image("https://cdn-icons-png.flaticon.com/512/1055/1055646.png", width=150)

# Filtros
st.sidebar.header("Filtros")
selected_genders = st.sidebar.multiselect("Selecciona género(s)", df['gender'].unique(), default=df['gender'].unique())
performance_range = st.sidebar.slider("Puntaje de desempeño", int(df['performance_score'].min()), int(df['performance_score'].max()), (1, 5))
selected_marital = st.sidebar.selectbox("Selecciona estado civil", ["Todos"] + list(df['marital_status'].unique()))

# Aplicar filtros
filtered_df = df[
    (df['gender'].isin(selected_genders)) &
    (df['performance_score'] >= performance_range[0]) &
    (df['performance_score'] <= performance_range[1])
]
if selected_marital != "Todos":
    filtered_df = filtered_df[filtered_df['marital_status'] == selected_marital]

# Gráficos lado a lado
col1, col2 = st.columns(2)

with col1:
    st.subheader("Distribución de Puntajes de Desempeño")
    fig1 = px.histogram(filtered_df, x='performance_score', nbins=5, 
                        title="Puntaje de desempeño", labels={'performance_score': 'Puntaje'},
                        text_auto=True)
    st.plotly_chart(fig1)

with col2:
    st.subheader("Promedio de Horas Trabajadas por Género")
    df_hrs = df[
        (df['performance_score'] >= performance_range[0]) &
        (df['performance_score'] <= performance_range[1])
    ]
    if selected_marital != "Todos":
        df_hrs = df_hrs[df_hrs['marital_status'] == selected_marital]
    fig2 = px.bar(df_hrs.groupby('gender')['average_work_hours'].mean().reset_index(), 
                  x='gender', y='average_work_hours',
                  title="Horas promedio por género", labels={'average_work_hours': 'Horas promedio'})
    st.plotly_chart(fig2)

# Gráficos completos
st.subheader("Relación entre Edad y Salario")
fig3 = px.scatter(filtered_df, x='age', y='salary', color='gender',
                  hover_data=['position'], title="Edad vs Salario", 
                  labels={'age': 'Edad', 'salary': 'Salario'})
st.plotly_chart(fig3)

st.subheader("Relación entre Horas Trabajadas y Desempeño")
fig4 = px.scatter(filtered_df, x='average_work_hours', y='performance_score', color='gender',
                  title="Horas Trabajadas vs Desempeño", 
                  labels={'average_work_hours': 'Horas promedio', 'performance_score': 'Desempeño'})
st.plotly_chart(fig4)

# Tabla resumen
st.subheader("Vista de Datos Filtrados")
cols = ['name_employee', 'position', 'hiring_date', 'last_performance_date', 'satisfaction_level', 'absences']
st.dataframe(filtered_df[cols])

# Conclusión
st.subheader("Conclusión del Análisis")
st.markdown("""
Este dashboard muestra cómo ciertos factores como el género, estado civil y desempeño están relacionados con el promedio de horas trabajadas, edad y salario. 
Estos datos pueden ayudar a identificar oportunidades de mejora en la gestión de personal.
""")