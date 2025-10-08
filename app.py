import scipy.stats
import streamlit as st
import time
import pandas as pd

st.header('Lanzar una moneda 🪙')

# Slider y botón
number_of_trials = st.slider('¿Número de intentos?', 1, 1000, 10)
start_button = st.button('Ejecutar experimento')

if start_button:
    st.write(f'🎯 Realizando {number_of_trials} lanzamientos...')

    # Crear contenedor para la gráfica
    placeholder = st.empty()

    # Datos iniciales
    means = []
    outcome_1_count = 0

    # Generar resultados
    trial_outcomes = scipy.stats.bernoulli.rvs(p=0.5, size=number_of_trials)

    for i, outcome in enumerate(trial_outcomes, start=1):
        if outcome == 1:
            outcome_1_count += 1

        mean = outcome_1_count / i
        means.append(mean)

        # Actualizar gráfico dinámico
        df = pd.DataFrame(means, columns=["Media acumulada"])
        placeholder.line_chart(df)

        # Pequeña pausa para animación
        time.sleep(0.05)

    st.success(f'✅ Media final: {mean:.3f}')
