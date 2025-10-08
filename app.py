import pandas as pd
import scipy.stats
import streamlit as st
import time

# ===============================
# VARIABLES DE ESTADO (persisten entre ejecuciones)
# ===============================
if 'experiment_no' not in st.session_state:
    st.session_state['experiment_no'] = 0

if 'df_experiment_results' not in st.session_state:
    st.session_state['df_experiment_results'] = pd.DataFrame(columns=['# Experimento', 'Iteraciones', 'Media final'])

# ===============================
# INTERFAZ
# ===============================
st.header('🎲 Lanzar una moneda 🪙')

number_of_trials = st.slider('¿Número de intentos?', 1, 1000, 10)
start_button = st.button('Ejecutar experimento')

# ===============================
# FUNCIÓN PRINCIPAL
# ===============================
def toss_coin(n):
    """Lanza una moneda n veces y actualiza la gráfica dinámicamente."""
    trial_outcomes = scipy.stats.bernoulli.rvs(p=0.5, size=n)

    # Inicialización
    means = []
    outcome_1_count = 0

    # Crear contenedor de gráfico
    placeholder = st.empty()

    for i, outcome in enumerate(trial_outcomes, start=1):
        if outcome == 1:
            outcome_1_count += 1

        mean = outcome_1_count / i
        means.append(mean)

        # Actualizar gráfico dinámico
        df = pd.DataFrame(means, columns=["Media acumulada"])
        placeholder.line_chart(df)

        # Pequeña pausa visual
        time.sleep(0.03)

    return mean

# ===============================
# EJECUCIÓN DEL EXPERIMENTO
# ===============================
if start_button:
    st.session_state['experiment_no'] += 1
    st.write(f'🔄 Ejecutando experimento #{st.session_state["experiment_no"]} con {number_of_trials} intentos...')
    mean = toss_coin(number_of_trials)

    # Guardar resultado en el historial
    nuevo_resultado = pd.DataFrame({
        '# Experimento': [st.session_state['experiment_no']],
        'Iteraciones': [number_of_trials],
        'Media final': [round(mean, 3)]
    })

    st.session_state['df_experiment_results'] = pd.concat(
        [st.session_state['df_experiment_results'], nuevo_resultado],
        ignore_index=True
    )

    st.success(f'✅ Media final del experimento #{st.session_state["experiment_no"]}: {mean:.3f}')

# ===============================
# MOSTRAR RESULTADOS ACUMULADOS
# ===============================
st.subheader("📊 Historial de experimentos")
st.dataframe(st.session_state['df_experiment_results'], use_container_width=True)
