import streamlit as st
# import urllib.parse  # Eliminado, ya no es necesario para mailto
from collections import defaultdict

# --- 1. CONFIGURACIÓN DEL TEST (BIG FIVE - OCEAN) ---

QUESTIONS = [
    # O - Openness
    {"id": "O1", "text": "Tengo una imaginación muy activa y disfruto soñando despierto.", "trait": "O", "reverse": False},
    {"id": "O2", "text": "Disfruto con las ideas complejas y abstractas.", "trait": "O", "reverse": False},
    {"id": "O3", "text": "Suelo probar comidas nuevas y viajar a lugares desconocidos.", "trait": "O", "reverse": False},
    {"id": "O4", "text": "Prefiero la rutina a los cambios o las novedades.", "trait": "O", "reverse": True},
    {"id": "O5", "text": "No me interesa mucho el arte ni la poesía.", "trait": "O", "reverse": True},
    {"id": "O6", "text": "Soy una persona curiosa intelectualmente.", "trait": "O", "reverse": False},
    
    # C - Conscientiousness
    {"id": "C1", "text": "Siempre me preparo con antelación para mis tareas y compromisos.", "trait": "C", "reverse": False},
    {"id": "C2", "text": "Soy muy metódico y ordenado en mi trabajo y mi casa.", "trait": "C", "reverse": False},
    {"id": "C3", "text": "A menudo me olvido de mis deberes y responsabilidades.", "trait": "C", "reverse": True},
    {"id": "C4", "text": "Trabajo con diligencia hasta completar cualquier tarea que comience.", "trait": "C", "reverse": False},
    {"id": "C5", "text": "No me importa dejar las cosas sin terminar si pierdo el interés.", "trait": "C", "reverse": True},
    {"id": "C6", "text": "Siempre procuro mantener mis promesas y compromisos.", "trait": "C", "reverse": False},

    # E - Extraversion
    {"id": "E1", "text": "Soy el alma de la fiesta; disfruto siendo el centro de atención.", "trait": "E", "reverse": False},
    {"id": "E2", "text": "Me gusta tener mucha gente a mi alrededor.", "trait": "E", "reverse": False},
    {"id": "E3", "text": "Soy bastante reservado y tiendo a quedarme en un segundo plano.", "trait": "E", "reverse": True},
    {"id": "E4", "text": "Cuando hablo en un grupo, tiendo a dominar la conversación.", "trait": "E", "reverse": False},
    {"id": "E5", "text": "Prefiero las actividades que puedo realizar solo.", "trait": "E", "reverse": True},
    {"id": "E6", "text": "Expreso mis opiniones y sentimientos con facilidad y confianza.", "trait": "E", "reverse": False},

    # A - Agreeableness
    {"id": "A1", "text": "Siento mucha empatía y compasión por los demás.", "trait": "A", "reverse": False},
    {"id": "A2", "text": "Generalmente confío en las intenciones de otras personas.", "trait": "A", "reverse": False},
    {"id": "A3", "text": "Pienso que la mayoría de la gente intenta aprovecharse de mí.", "trait": "A", "reverse": True},
    {"id": "A4", "text": "Evito las discusiones y prefiero el consenso.", "trait": "A", "reverse": False},
    {"id": "A5", "text": "No me molesta insultar a las personas si es necesario para ganar.", "trait": "A", "reverse": True},
    {"id": "A6", "text": "Tienden a describirme como una persona amable y considerada.", "trait": "A", "reverse": False},
    
    # N - Neuroticism
    {"id": "N1", "text": "Me preocupo a menudo por cosas pequeñas o insignificantes.", "trait": "N", "reverse": False},
    {"id": "N2", "text": "A veces me siento deprimido o melancólico sin razón aparente.", "trait": "N", "reverse": False},
    {"id": "N3", "text": "Tienden a estresarme las situaciones inesperadas o difíciles.", "trait": "N", "reverse": False},
    {"id": "N4", "text": "Soy una persona muy relajada y rara vez me siento ansioso.", "trait": "N", "reverse": True},
    {"id": "N5", "text": "Puedo mantener la calma en situaciones de alta presión.", "trait": "N", "reverse": True},
    {"id": "N6", "text": "Mi estado de ánimo es generalmente estable y tranquilo.", "trait": "N", "reverse": True},
]

# Opciones de respuesta para el Likert Scale
LIKERT_OPTIONS = {
    5: "Totalmente de acuerdo",
    4: "De acuerdo",
    3: "Neutral",
    2: "En desacuerdo",
    1: "Totalmente en desacuerdo"
}

# Etiquetas para la barra de progreso
TRAIT_LABELS = {
    "O": "Apertura a la Experiencia (Openness)",
    "C": "Responsabilidad (Conscientiousness)",
    "E": "Extraversión (Extraversion)",
    "A": "Amabilidad (Agreeableness)",
    "N": "Neuroticismo (Neuroticism)"
}

# Colores para la visualización de resultados
LEVEL_COLORS = {
    # Estos colores se invertirán para Neuroticism
    "Alto_Positivo": "#004AAD",  # Azul Corporativo (para Alto en O, C, E, A)
    "Bajo_Negativo": "#C0392B",  # Rojo (para Bajo en O, C, E, A, y Alto en N)
    "Medio": "#F39C12",         # Amarillo
    "Estable": "#16A085"        # Verde (para Bajo en N)
}

# --- 2. LÓGICA DE PUNTUACIÓN Y PERFIL ---

def calculate_score(answers):
    """Calcula la puntuación para cada rasgo de personalidad."""
    scores = defaultdict(int)
    
    for q in QUESTIONS:
        q_id = q["id"]
        trait = q["trait"]
        is_reverse = q["reverse"]
        
        response = answers.get(q_id)
        
        if response is not None:
            score = response
            
            if is_reverse:
                score = 6 - score
            
            scores[trait] += score
            
    return dict(scores)

def interpret_score(score, trait):
    """Interpreta la puntuación (Bajo, Medio, Alto) y devuelve el texto del perfil y el color."""
    
    # Umbrales (Aproximadamente tercios del rango 6-30)
    LOW_THRESHOLD = 14
    HIGH_THRESHOLD = 23
    
    if score <= LOW_THRESHOLD:
        level = "Bajo"
    elif score >= HIGH_THRESHOLD:
        level = "Alto"
    else:
        level = "Medio"
        
    # --- Descripciones de Perfil ---
    profiles = {
        "O": {
            "Alto": "**Alto en Apertura:** Eres imaginativo, curioso, original y con una amplia gama de intereses. Disfrutas explorando nuevas ideas y experiencias, y te sientes cómodo con lo poco convencional.",
            "Medio": "**Moderado en Apertura:** Eres práctico y estás dispuesto a considerar nuevas ideas, pero mantienes un equilibrio saludable con la tradición y la familiaridad. Valoras tanto la novedad como la estabilidad.",
            "Bajo": "**Bajo en Apertura:** Eres más tradicional, pragmático y prefieres la familiaridad. Tiendes a ser resistente al cambio y prefieres enfocarte en hechos concretos en lugar de en ideas abstractas o el arte."
        },
        "C": {
            "Alto": "**Alto en Responsabilidad:** Eres organizado, disciplinado, orientado a metas y altamente confiable. Planificas meticulosamente y te esfuerzas por completar las tareas a tiempo y con excelencia.",
            "Medio": "**Moderado en Responsabilidad:** Eres una persona capaz de organizarse y cumplir con los plazos, pero también te permites ser espontáneo o flexible cuando la situación lo requiere. Eres confiable en general.",
            "Bajo": "**Bajo en Responsabilidad:** Eres más espontáneo y flexible, pero a veces careces de disciplina y organización. Tiendes a posponer tareas, prefieres la improvisación y puedes parecer despreocupado."
        },
        "E": {
            "Alto": "**Alto en Extraversión:** Eres sociable, enérgico, asertivo y te revitalizas al interactuar con otros. Disfrutas de la emoción, eres entusiasta y tiendes a ser el centro de atención en grupos.",
            "Medio": "**Moderado en Extraversión:** Eres una persona equilibrada que disfruta tanto del tiempo social como de la soledad. Puedes ser conversador, pero también valoras la introspección y las interacciones uno a uno.",
            "Bajo": "**Bajo en Extraversión (Introvertido):** Eres reservado, callado y prefieres las interacciones profundas con pocas personas. Te sientes agotado por las multitudes y te recargas estando solo."
        },
        "A": {
            "Alto": "**Alto en Amabilidad:** Eres cooperativo, compasivo, empático y tiendes a ser cortés y amable. Estás motivado por el bienestar de los demás y evitas el conflicto directo.",
            "Medio": "**Moderado en Amabilidad:** Eres una persona generalmente agradable, pero que también puede ser crítica o escéptica cuando es necesario. Cooperas, pero te aseguras de defender tus propios intereses.",
            "Bajo": "**Bajo en Amabilidad:** Tiendes a ser competitivo, escéptico y a veces confrontativo. Eres directo y honesto, incluso si eso significa incomodar a otros. Tus intereses personales suelen tener prioridad."
        },
        "N": {
            "Alto": "**Alto en Neuroticismo (Baja Estabilidad Emocional):** Tiendes a experimentar emociones negativas (ansiedad, preocupación, ira) con facilidad. Eres sensible al estrés y puedes reaccionar intensamente ante los desafíos.",
            "Medio": "**Moderado en Neuroticismo:** Eres capaz de gestionar el estrés en la mayoría de las situaciones, aunque puedes experimentar ansiedad o preocupación en momentos de gran presión o incertidumbre.",
            "Bajo": "**Bajo en Neuroticismo (Alta Estabilidad Emocional):** Eres calmado, estable, resiliente y rara vez te sientes perturbado. Eres eficaz para manejar el estrés y recuperarte rápidamente de los contratiempos."
        }
    }
    
    # Determinar Color y Código de Color
    if trait == 'N':
        # Neuroticism: Bajo (Low N) es deseable/estable.
        if level == "Bajo":
            color_hex = LEVEL_COLORS["Estable"] # Verde
            color_label = "Estable"
        elif level == "Alto":
            color_hex = LEVEL_COLORS["Bajo_Negativo"] # Rojo
            color_label = "Inestable"
        else:
            color_hex = LEVEL_COLORS["Medio"]
            color_label = "Moderado"
    else:
        # Otros rasgos: Alto es más pronunciado.
        if level == "Alto":
            color_hex = LEVEL_COLORS["Alto_Positivo"] # Azul Corporativo
            color_label = "Pronunciado"
        elif level == "Bajo":
            color_hex = LEVEL_COLORS["Bajo_Negativo"] # Rojo
            color_label = "Bajo"
        else:
            color_hex = LEVEL_COLORS["Medio"]
            color_label = "Moderado"

    return profiles[trait][level], level, color_hex, color_label

# --- 3. FUNCIÓN PARA COMPARTIR POR EMAIL (ELIMINADA) ---

# --- Función para reiniciar el test ---
def restart_test():
    """
    Resets the session state to restart the test.
    (Removimos st.rerun() para evitar advertencias en callbacks).
    """
    st.session_state.answers = {}
    st.session_state.test_completed = False
    # st.rerun() ya no es necesario aquí y previene la advertencia. 

# --- 4. CONFIGURACIÓN VISUAL Y DE INTERFAZ ---

def set_professional_style():
    """Aplica estilos CSS para una apariencia corporativa y profesional, e incluye estilos de impresión."""
    st.markdown(f"""
    <style>
        /* Fuente y Estilo General */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
        html, body, [class*="st-"] {{
            font-family: 'Inter', sans-serif;
        }}
        
        /* Contenedor Principal y Header */
        .main {{
            background-color: #F8F9FA; /* Light Gray Background */
            border-radius: 12px;
        }}
        
        /* Títulos y Encabezados */
        h1 {{
            color: #004AAD; /* Corporate Blue */
            border-bottom: 3px solid #004AAD;
            padding-bottom: 0.5rem;
            margin-bottom: 1.5rem;
            font-weight: 700;
        }}
        h2 {{
            color: #004AAD;
            font-weight: 600;
            margin-top: 2rem;
        }}

        /* Encabezado del Trait */
        .trait-header {{
            font-size: 1.3rem;
            font-weight: 600;
            margin-bottom: 5px;
            padding: 8px 0;
            color: #1F2937;
        }}
        
        /* Estilo de las Preguntas (Controles) */
        .stRadio > label {{
            font-size: 1.05rem;
            font-weight: 500;
            color: #1f2937;
            margin-bottom: 10px;
            padding: 8px 0;
            display: block;
            border-left: 4px solid #D1D5DB; /* Light gray border */
            padding-left: 15px;
        }}
        .stRadio div[role="radiogroup"] {{
            display: flex;
            flex-direction: row; 
            gap: 10px;
            padding-bottom: 15px;
            border-bottom: 1px solid #E5E7EB;
            margin-bottom: 20px;
            flex-wrap: wrap; /* Asegura el responsive */
        }}
        
        /* Botones de Acción (Reiniciar y Enviar) */
        .stButton>button {{
            background-color: #004AAD; /* Corporate Blue */
            color: white;
            font-weight: 600;
            padding: 10px 20px;
            border-radius: 8px;
            border: none;
            transition: background-color 0.3s;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }}
        .stButton>button:hover {{
            background-color: #003A8D; /* Darker Blue on Hover */
        }}

        /* Estilo del Perfil Final Container */
        .profile-container {{
            background-color: #ffffff;
            border: 1px solid #004AAD;
            border-radius: 10px;
            padding: 25px;
            margin-top: 30px;
            box-shadow: 0 10px 20px rgba(0, 74, 173, 0.1);
        }}
        
        /* Estilos para el Progress Bar dinámico */
        .stProgress > div > div > div > div {{
            background-color: {LEVEL_COLORS["Alto_Positivo"]};
            transition: background-color 0.5s ease;
        }}

        /* Estilo para el botón de Imprimir (reemplaza al de Email) */
        .print-button-container button {{
            background-color: #16A085 !important; /* Success Green */
            color: white !important;
            font-weight: 600;
            padding: 10px 20px;
            border-radius: 8px;
            border: none;
            transition: background-color 0.3s;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            cursor: pointer;
            width: 100%;
        }}
        .print-button-container button:hover {{
            background-color: #138D73 !important;
        }}
        
        /* Media Query para Impresión (Limpieza profesional del PDF) */
        @media print {{
            /* Ocultar elementos de UI que no son resultados */
            .stRadio, .stButton, .stTabs, h1, .stMarkdown:nth-child(2), .css-18z244q, .css-1d2a4o5 {{
                display: none !important;
            }}
            /* Mostrar solo el contenido de resultados (h2 y st.info) */
            .profile-container, .trait-header, .stAlert, .stProgress, .stMetric, .stMarkdown > div > hr, .stMetric > div > label > div > div > span {{
                display: block !important;
            }}
            /* Forzar el color de fondo blanco para el PDF */
            .main {{
                background-color: white !important;
                padding: 0;
            }}
            /* Asegurar que el logo y título de resultados se vean */
            .profile-container h2, .trait-header {{
                color: #000000 !important;
            }}
            /* Ocultar el botón de reinicio y el de impresión */
            .print-button-container, .stButton:nth-child(2) {{ 
                display: none !important; 
            }}
        }}

    </style>
    """, unsafe_allow_html=True)

# --- 5. FLUJO DE LA APLICACIÓN STREAMLIT ---

def run_test():
    """Función principal para correr la aplicación."""
    
    set_professional_style()

    # Añadir un logo simple (SVG) para un toque corporativo
    st.markdown(f"""
    <div style="display: flex; align-items: center; margin-bottom: 20px;">
        <svg width="40" height="40" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M12 2C6.48 2 2 6.48 2 12C2 17.52 6.48 22 12 22C17.52 22 22 17.52 22 12C22 6.48 17.52 2 12 2ZM15 16H9V14H15V16ZM15 12H9V10H15V12ZM15 8H9V6H15V8Z" fill="#004AAD"/>
        </svg>
        <span style="font-size: 2rem; font-weight: 700; color: #004AAD; margin-left: 10px;">Perfil | OCEAN</span>
    </div>
    """, unsafe_allow_html=True)

    st.title("Test de Personalidad - El Modelo de los Cinco Grandes")
    st.markdown("""
        Este cuestionario de 30 preguntas está diseñado para evaluar tu perfil en las cinco dimensiones clave de la personalidad (Apertura, Responsabilidad, Extraversión, Amabilidad y Neuroticismo). 
        Selecciona la opción que mejor describa tu acuerdo o desacuerdo con cada afirmación.
        **Tu honestidad garantiza un perfil más preciso.**
    """)
    
    # Inicializar el estado de la sesión
    if 'answers' not in st.session_state:
        st.session_state.answers = {}
    if 'test_completed' not in st.session_state:
        st.session_state.test_completed = False
        
    # Lista de opciones con el formato (Etiqueta, Valor)
    likert_options_tuple = [(v, k) for k, v in LIKERT_OPTIONS.items()]

    tabs = st.tabs([f"Bloque {i+1} ({i*6 + 1}-{i*6 + 6})" for i in range(5)])
    
    with st.form(key='personality_test_form'):
        
        for i, tab in enumerate(tabs):
            with tab:
                st.markdown(f"## Bloque {i+1}: Evaluación")
                
                start_index = i * 6
                end_index = start_index + 6
                current_questions = QUESTIONS[start_index:end_index]

                for q in current_questions:
                    try:
                        # Recupera el valor de la respuesta si existe para mantener la selección
                        current_value = st.session_state.answers.get(q['id'])
                        current_index = likert_options_tuple.index((LIKERT_OPTIONS[current_value], current_value)) if current_value else None
                    except (ValueError, KeyError):
                        current_index = None

                    response = st.radio(
                        label=f"**{q['id']}.** {q['text']}",
                        options=likert_options_tuple,
                        key=q['id'],
                        index=current_index,
                        format_func=lambda x: x[0]
                    )
                    
                    if response is not None:
                        st.session_state.answers[q['id']] = response[1]

        st.markdown("---")
        submit_button = st.form_submit_button(label='Finalizar Test y Ver Mi Perfil')

    # --- Lógica de procesamiento de resultados ---
    if submit_button or st.session_state.test_completed:
        if len(st.session_state.answers) < len(QUESTIONS):
            st.warning("¡Alto ahí! Por favor, responde las 30 preguntas antes de finalizar el test.")
            st.session_state.test_completed = False
            return
        
        st.session_state.test_completed = True
        
        # 5. Calcular la puntuación
        scores = calculate_score(st.session_state.answers)
        all_results_data = {} # Almacenar todos los datos para el email (aunque ya no se use, se mantiene la estructura)

        # 6. Mostrar el Perfil
        st.markdown(
            f"""
            <div class="profile-container">
                <h2>✅ Perfil de Personalidad Completado: Análisis Detallado</h2>
                <p>Tu análisis está basado en el **Modelo OCEAN**. La puntuación alta
                en un rasgo indica una mayor intensidad de esa característica.</p>
            </div>
            """, 
            unsafe_allow_html=True
        )
        
        # 7. Iterar y Mostrar Resultados
        for trait_code, score in scores.items():
            profile_text, level, color_hex, color_label = interpret_score(score, trait_code)
            trait_label = TRAIT_LABELS[trait_code]
            
            # Almacenar datos (mantenido por si se necesita exportación futura)
            all_results_data[trait_code] = {
                "label": trait_label,
                "score": score,
                "level": level,
                "profile": profile_text
            }
            
            # Normalizar score para la barra de progreso (0 a 1.0)
            normalized_score = (score - 6) / 24
            
            # Encabezado del Trait y Score
            st.markdown(f"""
            <div class="trait-header">
                {trait_label} &mdash; Nivel {level}
            </div>
            """, unsafe_allow_html=True)
            
            # Usar columnas para la visualización del resultado
            col_bar, col_score = st.columns([0.7, 0.3])

            with col_bar:
                # Inyectar el color dinámico en el CSS del progress bar
                st.markdown(f"""
                <style>
                    /* Target the specific progress bar */
                    .stProgress[data-testid="stProgress"] > div > div > div > div {{
                        background-color: {color_hex} !important;
                    }}
                </style>
                """, unsafe_allow_html=True)
                st.progress(normalized_score)

            with col_score:
                st.metric(label="Puntuación", value=f"{score}/30", delta=color_label, delta_color="off")
            
            # Mostrar la descripción
            st.info(profile_text, icon="💡")
            st.markdown("---")
        
        st.success("El análisis de tu perfil de personalidad ha concluido con éxito.")

        # 8. Botones de acción final (Imprimir y Reiniciar)
        # Se usan dos columnas de igual tamaño para los botones principales
        col_print, col_restart = st.columns([0.5, 0.5])
        
        # Botón para Imprimir (usando JS para el diálogo de impresión del navegador)
        with col_print:
            st.markdown("""
            <div class="print-button-container">
                <button onclick="window.print()">
                    🖨️ Imprimir/Guardar como PDF
                </button>
            </div>
            """, unsafe_allow_html=True)


        # Botón para reiniciar (llama a la función sin st.rerun())
        with col_restart:
            st.button("🔄 Volver a Realizar el Test", on_click=restart_test, type="secondary", use_container_width=True)

# Ejecutar la aplicación
if __name__ == '__main__':
    run_test()
