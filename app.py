import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Cargar datos
df = pd.read_csv("employee_data.csv")

# Limpiar datos (espacios en columnas clave)
df["gender"] = df["gender"].str.strip()
df["marital_status"] = df["marital_status"].str.strip()

# --- TÍTULO Y DESCRIPCIÓN ---
st.title("Análisis de Desempeño de Empleados")
st.markdown("Esta aplicación muestra un resumen del desempeño de los colaboradores de Socialize your knowledge, con base en distintos filtros y visualizaciones interactivas.")

# --- LOGO (si tienes logo.png) ---
# st.image("logo.png", width=150)

# --- CONTROLES ---
genero = st.selectbox("Selecciona el género", options=df["gender"].unique())
rango_desempeno = st.slider("Selecciona el rango de puntaje de desempeño", 1, 5, (1, 5))
estado_civil = st.selectbox("Selecciona el estado civil", options=df["marital_status"].unique())

# --- FILTRADO ---
df_filtrado = df[
    (df["gender"] == genero) &
    (df["performance_score"].between(rango_desempeno[0], rango_desempeno[1])) &
    (df["marital_status"] == estado_civil)
]

st.markdown(f"Se encontraron **{len(df_filtrado)} empleados** con los criterios seleccionados.")

# --- GRAFICOS ---
st.subheader("Distribución del puntaje de desempeño")
fig1, ax1 = plt.subplots()
df["performance_score"].hist(bins=5, ax=ax1, color="skyblue", edgecolor="black")
ax1.set_xlabel("Puntaje de desempeño")
ax1.set_ylabel("Frecuencia")
st.pyplot(fig1)

st.subheader("Promedio de horas trabajadas por género")
fig2, ax2 = plt.subplots()
df.groupby("gender")["average_work_hours"].mean().plot(kind="bar", ax=ax2, color="salmon")
ax2.set_ylabel("Promedio de horas")
st.pyplot(fig2)

st.subheader("Relación entre edad y salario")
fig3, ax3 = plt.subplots()
ax3.scatter(df["age"], df["salary"], alpha=0.6)
ax3.set_xlabel("Edad")
ax3.set_ylabel("Salario")
st.pyplot(fig3)

st.subheader("Horas trabajadas vs. Puntaje de desempeño")
fig4, ax4 = plt.subplots()
ax4.scatter(df["average_work_hours"], df["performance_score"], alpha=0.5)
ax4.set_xlabel("Horas trabajadas promedio")
ax4.set_ylabel("Puntaje de desempeño")
st.pyplot(fig4)

# --- CONCLUSIÓN ---
st.subheader("Conclusiones")
st.markdown("""
Con base en el análisis, se observa una distribución equilibrada en los puntajes de desempeño. 
El promedio de horas varía ligeramente entre géneros. También se visualiza que no existe una relación estrictamente lineal entre edad y salario, ni entre horas trabajadas y desempeño, lo que puede indicar que hay otros factores influyentes en la productividad.
""")
