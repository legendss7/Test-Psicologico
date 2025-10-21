import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np 

# --- CONFIGURACIÓN DE LA PÁGINA Y ESTILO (Mejoras de Última Tecnología) ---

# 1. Configuración general (modo ancho, título, ícono)
st.set_page_config(
    page_title="Test Psicológico Dinámico | 132 Preguntas",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Inyección de CSS moderno (Dark Mode & Tarjetas con Sombra)
st.markdown("""
    <style>
        /* Fuente y Color Principal */
        @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;700&display=swap');
        html, body, [class*="st-"] {
            font-family: 'Space Grotesk', sans-serif;
        }
        
        /* Tema Oscuro y Cabecera Destacada */
        h1 {
            color: #4B0082; /* Índigo vibrante */
            text-align: center;
            font-size: 2.5em;
            padding: 10px 0;
            border-bottom: 3px solid #FFD700; /* Oro para destacar */
        }
        
        /* Estilo para los botones (Efecto Hover y Sombra) */
        .stButton>button {
            background-color: #00BFFF; /* Azul vibrante (Deep Sky Blue) */
            color: white;
            font-weight: bold;
            border: none;
            border-radius: 10px;
            padding: 10px 20px;
            transition: all 0.3s ease;
            box-shadow: 0 4px 15px rgba(0, 191, 255, 0.5);
        }
        .stButton>button:hover {
            background-color: #4B0082; /* Cambio a Índigo en hover */
            box-shadow: 0 6px 20px rgba(75, 0, 130, 0.7);
            transform: translateY(-2px);
        }

        /* Contenedores tipo tarjeta con sombra animada */
        .stContainer {
            background-color: #1e1e1e; /* Fondo oscuro sutil */
            padding: 20px;
            border-radius: 15px;
            box-shadow: 0 8px 30px rgba(0, 0, 0, 0.5);
            margin-bottom: 20px;
            border: 1px solid #333;
        }

        /* Texto de ayuda y etiquetas en color claro */
        .stSlider label, .stSelectbox label {
            font-weight: 500;
            color: #A9A9A9;
        }
    </style>
""", unsafe_allow_html=True)

# --- CONFIGURACIÓN Y GENERACIÓN DE LAS 132 PREGUNTAS ---

# Definición de las 5 Categorías de Liderazgo
categories = ["Estrategia", "Análisis", "Confrontación", "Decisión", "Resiliencia"]

# Distribución de 132 preguntas
q_per_category = {
    "Estrategia": 26, 
    "Análisis": 26, 
    "Confrontación": 26, 
    "Decisión": 26, 
    "Resiliencia": 28 
}

MAX_SCORE_PER_ITEM = 5
# Score máximo teórico para el gráfico de radar (28 * 5 = 140)
MAX_SCORE_RADAR = q_per_category["Resiliencia"] * MAX_SCORE_PER_ITEM 

# Generación de la lista de 132 preguntas con IDs únicos
questions_data = []
q_counter = 1
for cat in categories:
    num_q = q_per_category[cat]
    for j in range(num_q):
        questions_data.append({
            "q": f"Declaración {q_counter}: En situaciones de '{cat}', me siento cómodo tomando la delantera y asumiendo riesgos.",
            "category": cat,
            "id": f"q_{q_counter}"
        })
        q_counter += 1


# --- INICIO DE LA APLICACIÓN ---

st.title("🧠 Test Psicológico de Liderazgo | 132 Declaraciones")
st.markdown("### Desarrolla tu Potencial con Tecnología de Última Generación")

# Inicializar o reiniciar el estado de la aplicación
if 'test_started' not in st.session_state:
    st.session_state.test_started = False
if 'results' not in st.session_state:
    st.session_state.results = None

# --- PANTALLA DE INICIO ---
if not st.session_state.test_started and not st.session_state.results:
    with st.container(border=True):
        st.header("🚀 ¡Comienza la Evaluación!")
        st.markdown(f"""
            Esta es una prueba exhaustiva con **{len(questions_data)} declaraciones** diseñada para mapear tus fortalezas en 5 áreas clave del liderazgo moderno.
            
            **Instrucciones:** Utiliza la escala deslizante (Slider) de 1 a 5 para cada declaración:
            * **1:** Totalmente en Desacuerdo
            * **5:** Totalmente de Acuerdo
            
            Haz clic en "Iniciar Test" para empezar la secuencia de preguntas.
        """)
        
        # Botón de inicio con animación
        if st.button("🌟 INICIAR TEST", key="start_button"):
            st.session_state.test_started = True
            # Inicializar los valores del slider en el estado de sesión (valor por defecto 3)
            for item in questions_data:
                 if item['id'] not in st.session_state:
                     st.session_state[item['id']] = 3 
            st.rerun()

# --- PANTALLA DEL TEST ---
elif st.session_state.test_started:
    # Contenedor principal para las preguntas
    with st.form(key='psych_test_form'):
        st.header("Cuestionario de Liderazgo (132 Declaraciones)")
        
        st.markdown("""
        <p style='color: #FFD700; font-weight: bold;'>
            Desliza el marcador: 1 (Desacuerdo) a 5 (Acuerdo)
        </p>
        """, unsafe_allow_html=True)

        # Generar las 132 preguntas
        for i, item in enumerate(questions_data):
            # Pregunta en un contenedor tipo tarjeta
            with st.container(border=True):
                st.subheader(f"Declaración {i+1} | Área: {item['category']}")
                
                # Slider (Escala Likert)
                st.slider(
                    label=item['q'],
                    min_value=1,
                    max_value=MAX_SCORE_PER_ITEM,
                    value=st.session_state[item['id']], 
                    step=1,
                    key=item['id'],
                    help="1: Totalmente en Desacuerdo | 5: Totalmente de Acuerdo"
                )
        
        st.markdown("---")
        
        # Botón de envío del formulario
        submit_button = st.form_submit_button(label="CALCULAR RESULTADOS ⚡")

        # Lógica al enviar el formulario
        if submit_button:
            
            # Cálculo de Puntuaciones sumando los valores del slider
            final_scores = {cat: 0 for cat in categories}
            
            for item in questions_data:
                score = st.session_state[item['id']]
                final_scores[item['category']] += score

            st.session_state.results = final_scores
            st.session_state.test_started = False
            
            # 🎉 Animación de éxito y notificación
            st.balloons()
            st.toast('¡Resultados calculados con éxito!', icon='✅')
            st.rerun()

# --- PANTALLA DE RESULTADOS ---
elif st.session_state.results:
    st.header("🏆 Resultados del Test: Tu Perfil de Liderazgo")
    
    results = st.session_state.results
    categories_list = list(results.keys())
    scores = list(results.values())
    
    # Calcular el máximo score teórico para CADA categoría (para las métricas)
    max_scores_by_category = {cat: q_per_category[cat] * MAX_SCORE_PER_ITEM for cat in categories}
    
    # 1. GENERACIÓN DEL GRÁFICO DE RADAR (PLOTLY)
    fig = go.Figure(
        data=[
            go.Scatterpolar(
                r=scores + [scores[0]], # Cierra el polígono en el gráfico
                theta=categories_list + [categories_list[0]], # Cierra el polígono en el gráfico
                fill='toself',
                name='Puntuación',
                # Colores y estilo moderno
                fillcolor='rgba(0, 191, 255, 0.4)',  
                line_color='#00BFFF'
            )
        ],
        layout=go.Layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, MAX_SCORE_RADAR], 
                    tickvals=np.arange(0, MAX_SCORE_RADAR + 1, 20), # Marcas de 0 a 140
                    gridcolor='rgba(255, 255, 255, 0.2)'
                ),
                angularaxis=dict(
                    linecolor='rgba(255, 255, 255, 0.5)'
                )
            ),
            # Diseño oscuro y minimalista
            template='plotly_dark',
            title=dict(text='Distribución de Habilidades', font=dict(size=24, color='#FFD700')),
            showlegend=False,
            height=600,
            paper_bgcolor='rgba(30, 30, 30, 1)', 
            plot_bgcolor='rgba(30, 30, 30, 1)' 
        )
    )

    # 2. LAYOUT DE RESULTADOS (Gráfico y Análisis)
    col1, col2 = st.columns([2, 1])

    with col1:
        st.subheader("Gráfico de Habilidades (Radar Dinámico)")
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("Análisis Detallado")
        max_category = max(results, key=results.get)
        
        st.markdown(f"""
            <div class='stContainer' style='border: 2px solid #4B0082;'>
                <p style='color:#FFD700; font-size:1.2em; font-weight:bold;'>Tu Perfil Dominante:</p>
                <p>Tu puntuación más alta se encuentra en **{max_category}**.</p>
                <p>Puntaje: {results[max_category]}/{max_scores_by_category[max_category]}</p>
                <p>¡Esta es tu mayor fortaleza para el liderazgo moderno!</p>
                
                <hr style='border-top: 1px dashed #555;'>
                
                <p style='color:#A9A9A9;'>Resumen de Puntuaciones (Progreso):</p>
                
                """, unsafe_allow_html=True)
                
        # Mostrar las puntuaciones usando "progress" y st.metric para un aspecto dinámico
        for category, score in results.items():
            max_cat_score = max_scores_by_category[category]
            progress_value = score / max_cat_score
            st.metric(label=f"🟢 {category}", value=f"{score}/{max_cat_score}")
            st.progress(progress_value)

    st.markdown("---")
    
    # 3. BOTÓN DE REINICIO
    if st.button("🔄 REINICIAR TEST", key="reset_button", use_container_width=True):
        # Limpiar el estado para volver a la pantalla de inicio
        st.session_state.test_started = False
        st.session_state.results = None
        st.toast('Test reiniciado', icon='♻️')
        st.rerun()

    # 4. Footer estilizado
    st.markdown("---")
    st.markdown("<p style='text-align: center; color: #555;'>Powered by Streamlit & Plotly: Visualización de Datos Avanzada.</p>", unsafe_allow_html=True)
