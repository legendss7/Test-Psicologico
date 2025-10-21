import streamlit as st
import numpy as np
from collections import defaultdict
import time # Para simular una pequeña espera de carga de resultados

# --- 1. CONFIGURACIÓN DEL TEST (BIG FIVE - OCEAN) ---

# Hemos expandido el test a 60 preguntas (12 por rasgo)
QUESTIONS = [
    # O - Apertura a la Experiencia (Openness)
    {"id": "O1", "text": "Tengo una imaginación muy activa y disfruto soñando despierto.", "trait": "O", "reverse": False},
    {"id": "O2", "text": "Disfruto con las ideas complejas y abstractas.", "trait": "O", "reverse": False},
    {"id": "O3", "text": "Suelo probar comidas nuevas y viajar a lugares desconocidos.", "trait": "O", "reverse": False},
    {"id": "O4", "text": "Prefiero la rutina a los cambios o las novedades.", "trait": "O", "reverse": True},
    {"id": "O5", "text": "No me interesa mucho el arte ni la poesía.", "trait": "O", "reverse": True},
    {"id": "O6", "text": "Soy una persona curiosa intelectualmente.", "trait": "O", "reverse": False},
    {"id": "O7", "text": "Me encanta explorar teorías filosóficas y debatir conceptos.", "trait": "O", "reverse": False},
    {"id": "O8", "text": "Soy capaz de ignorar el ruido o las distracciones fácilmente.", "trait": "O", "reverse": True},
    {"id": "O9", "text": "A menudo me pierdo en mis pensamientos o ideas.", "trait": "O", "reverse": False},
    {"id": "O10", "text": "Raramente busco aprender habilidades que no sean directamente útiles.", "trait": "O", "reverse": True},
    {"id": "O11", "text": "Disfruto de exposiciones de arte y música poco convencional.", "trait": "O", "reverse": False},
    {"id": "O12", "text": "Para mí, 'lo nuevo' a menudo significa 'peligroso'.", "trait": "O", "reverse": True},
    
    # C - Responsabilidad (Conscientiousness)
    {"id": "C1", "text": "Siempre me preparo con antelación para mis tareas y compromisos.", "trait": "C", "reverse": False},
    {"id": "C2", "text": "Soy muy metódico y ordenado en mi trabajo y mi casa.", "trait": "C", "reverse": False},
    {"id": "C3", "text": "A menudo me olvido de mis deberes y responsabilidades.", "trait": "C", "reverse": True},
    {"id": "C4", "text": "Trabajo con diligencia hasta completar cualquier tarea que comience.", "trait": "C", "reverse": False},
    {"id": "C5", "text": "No me importa dejar las cosas sin terminar si pierdo el interés.", "trait": "C", "reverse": True},
    {"id": "C6", "text": "Siempre procuro mantener mis promesas y compromisos.", "trait": "C", "reverse": False},
    {"id": "C7", "text": "Soy visto por otros como una persona muy fiable y puntual.", "trait": "C", "reverse": False},
    {"id": "C8", "text": "Tengo dificultades para concentrarme en una sola cosa por mucho tiempo.", "trait": "C", "reverse": True},
    {"id": "C9", "text": "Establezco objetivos claros y trabajo sistemáticamente para alcanzarlos.", "trait": "C", "reverse": False},
    {"id": "C10", "text": "Mi espacio de trabajo o estudio es a menudo un desorden.", "trait": "C", "reverse": True},
    {"id": "C11", "text": "Soy perfeccionista y reviso mi trabajo varias veces.", "trait": "C", "reverse": False},
    {"id": "C12", "text": "Tienden a describirme como impulsivo e irreflexivo.", "trait": "C", "reverse": True},

    # E - Extraversión (Extraversion)
    {"id": "E1", "text": "Soy el alma de la fiesta; disfruto siendo el centro de atención.", "trait": "E", "reverse": False},
    {"id": "E2", "text": "Me gusta tener mucha gente a mi alrededor.", "trait": "E", "reverse": False},
    {"id": "E3", "text": "Soy bastante reservado y tiendo a quedarme en un segundo plano.", "trait": "E", "reverse": True},
    {"id": "E4", "text": "Cuando hablo en un grupo, tiendo a dominar la conversación.", "trait": "E", "reverse": False},
    {"id": "E5", "text": "Prefiero las actividades que puedo realizar solo.", "trait": "E", "reverse": True},
    {"id": "E6", "text": "Expreso mis opiniones y sentimientos con facilidad y confianza.", "trait": "E", "reverse": False},
    {"id": "E7", "text": "Soy muy entusiasta y enérgico en casi todo lo que hago.", "trait": "E", "reverse": False},
    {"id": "E8", "text": "Me aburro fácilmente si no hay mucha actividad o estimulación.", "trait": "E", "reverse": False},
    {"id": "E9", "text": "Me resulta agotador pasar demasiado tiempo con otras personas.", "trait": "E", "reverse": True},
    {"id": "E10", "text": "Normalmente me siento incómodo al hablar con extraños.", "trait": "E", "reverse": True},
    {"id": "E11", "text": "Busco activamente nuevas amistades y contactos sociales.", "trait": "E", "reverse": False},
    {"id": "E12", "text": "Mi voz es baja y tiendo a hablar con cautela.", "trait": "E", "reverse": True},

    # A - Amabilidad (Agreeableness)
    {"id": "A1", "text": "Siento mucha empatía y compasión por los demás.", "trait": "A", "reverse": False},
    {"id": "A2", "text": "Generalmente confío en las intenciones de otras personas.", "trait": "A", "reverse": False},
    {"id": "A3", "text": "Pienso que la mayoría de la gente intenta aprovecharse de mí.", "trait": "A", "reverse": True},
    {"id": "A4", "text": "Evito las discusiones y prefiero el consenso.", "trait": "A", "reverse": False},
    {"id": "A5", "text": "No me molesta insultar a las personas si es necesario para ganar.", "trait": "A", "reverse": True},
    {"id": "A6", "text": "Tienden a describirme como una persona amable y considerada.", "trait": "A", "reverse": False},
    {"id": "A7", "text": "Me resulta fácil perdonar a quienes me han ofendido.", "trait": "A", "reverse": False},
    {"id": "A8", "text": "A veces manipulo a los demás para conseguir lo que quiero.", "trait": "A", "reverse": True},
    {"id": "A9", "text": "Me gusta ayudar a quienes lo necesitan, incluso a expensas de mi tiempo.", "trait": "A", "reverse": False},
    {"id": "A10", "text": "Soy muy directo y no me importa criticar a los demás.", "trait": "A", "reverse": True},
    {"id": "A11", "text": "Considero importante la armonía en mis relaciones.", "trait": "A", "reverse": False},
    {"id": "A12", "text": "Me resulta difícil simpatizar con la gente que se queja mucho.", "trait": "A", "reverse": True},
    
    # N - Neuroticismo (Neuroticism)
    {"id": "N1", "text": "Me preocupo a menudo por cosas pequeñas o insignificantes.", "trait": "N", "reverse": False},
    {"id": "N2", "text": "A veces me siento deprimido o melancólico sin razón aparente.", "trait": "N", "reverse": False},
    {"id": "N3", "text": "Tienden a estresarme las situaciones inesperadas o difíciles.", "trait": "N", "reverse": False},
    {"id": "N4", "text": "Soy una persona muy relajada y rara vez me siento ansioso.", "trait": "N", "reverse": True},
    {"id": "N5", "text": "Puedo mantener la calma en situaciones de alta presión.", "trait": "N", "reverse": True},
    {"id": "N6", "text": "Mi estado de ánimo es generalmente estable y tranquilo.", "trait": "N", "reverse": True},
    {"id": "N7", "text": "Me ofendo o me irrito con mucha facilidad.", "trait": "N", "reverse": False},
    {"id": "N8", "text": "Me cuesta volver a la normalidad después de un disgusto.", "trait": "N", "reverse": False},
    {"id": "N9", "text": "Soy propenso a sentirme celoso o envidioso.", "trait": "N", "reverse": False},
    {"id": "N10", "text": "Raramente me siento tenso o nervioso.", "trait": "N", "reverse": True},
    {"id": "N11", "text": "Siempre me siento seguro y optimista sobre el futuro.", "trait": "N", "reverse": True},
    {"id": "N12", "text": "Mis emociones son a menudo volátiles e inestables.", "trait": "N", "reverse": False},
]

# Parámetros de la Paginación
QUESTIONS_PER_PAGE = 10
TOTAL_QUESTIONS = len(QUESTIONS)
TOTAL_PAGES = (TOTAL_QUESTIONS + QUESTIONS_PER_PAGE - 1) // QUESTIONS_PER_PAGE # 60/10 = 6 páginas

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

# Colores para la visualización de resultados (Profesional)
LEVEL_COLORS = {
    "Alto_Positivo": "#004AAD",  # Azul Corporativo
    "Bajo_Negativo": "#C0392B",  # Rojo (para Baja Positiva o Alta Negativa)
    "Medio": "#F39C12",         # Amarillo/Naranja
    "Estable": "#16A085"        # Verde (para Baja en Neuroticismo)
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
                # El score de un item invertido (1-5) es (6 - score)
                score = 6 - score 
            
            scores[trait] += score
            
    return dict(scores)

def interpret_score(score, trait):
    """
    Interpreta la puntuación (Bajo, Medio, Alto) y devuelve el texto del perfil y el color.
    Nuevo rango de score: 12 (min) a 60 (max).
    """
    # Umbrales (Aproximadamente tercios del rango 12-60. Ancho de rango: 48)
    # Bajo: 12-28 | Medio: 29-43 | Alto: 44-60
    LOW_THRESHOLD = 28
    HIGH_THRESHOLD = 44
    
    if score <= LOW_THRESHOLD:
        level = "Bajo"
    elif score >= HIGH_THRESHOLD:
        level = "Alto"
    else:
        level = "Medio"
        
    # --- Descripciones de Perfil ---
    profiles = {
        "O": {
            "Alto": "**Alto en Apertura (Explorador):** Eres sumamente curioso, creativo y prefieres la variedad. Te sientes atraído por el arte, las ideas abstractas y la exploración de nuevas culturas o filosofías. Muestras una gran flexibilidad mental.",
            "Medio": "**Moderado en Apertura (Equilibrado):** Eres práctico pero estás abierto al cambio cuando se justifica. Tienes intereses variados y disfrutas de la cultura, pero valoras la estabilidad y la tradición en igual medida.",
            "Bajo": "**Bajo en Apertura (Pragmático):** Eres más tradicional, pragmático y prefieres lo conocido y familiar. Te enfocas en hechos concretos, eres reservado con las ideas abstractas y valoras la rutina y la seguridad."
        },
        "C": {
            "Alto": "**Alto en Responsabilidad (Organizado):** Eres extremadamente organizado, disciplinado, orientado a metas y muy confiable. Planificas con antelación, persistes en la dificultad y demuestras un alto nivel de autodisciplina.",
            "Medio": "**Moderado en Responsabilidad (Eficaz):** Eres capaz de ser organizado y cumplir tus metas, pero no te estresas excesivamente por la perfección. Eres confiable, pero te permites ser espontáneo cuando es necesario.",
            "Bajo": "**Bajo en Responsabilidad (Espontáneo):** Eres más flexible, espontáneo y, a veces, informal. Tiendes a posponer tareas, prefieres la improvisación y puedes carecer de un enfoque riguroso en los detalles."
        },
        "E": {
            "Alto": "**Alto en Extraversión (Sociable):** Eres exuberante, sociable, enérgico y asertivo. Buscas activamente la interacción social, disfrutas de los grandes grupos y te sientes energizado al estar rodeado de gente.",
            "Medio": "**Moderado en Extraversión (Ambivertido):** Tienes un equilibrio entre la vida social y la soledad. Disfrutas de la compañía, pero también necesitas tiempo a solas para recargar energías. Eres un buen comunicador, pero sabes escuchar.",
            "Bajo": "**Bajo en Extraversión (Reservado):** Eres más reservado, pensativo y tranquilo. Prefieres las interacciones profundas uno a uno a las grandes multitudes y te sientes más cómodo trabajando solo o en entornos de baja estimulación."
        },
        "A": {
            "Alto": "**Alto en Amabilidad (Cooperativo):** Eres compasivo, de buen corazón, cooperativo y empático. Tienes una fuerte motivación para ayudar a los demás, evitas el conflicto y tiendes a confiar fácilmente en la gente.",
            "Medio": "**Moderado en Amabilidad (Justo):** Eres una persona generalmente agradable que valora la cooperación, pero que también puede ser escéptica o crítica cuando la situación lo requiere. Sabes defender tus propios intereses.",
            "Bajo": "**Bajo en Amabilidad (Desafiante):** Eres competitivo, escéptico y directo, a veces hasta el punto de ser confrontacional. Tu franqueza es alta y priorizas la verdad o tus intereses por encima de la sensibilidad de los demás."
        },
        "N": {
            "Alto": "**Alto en Neuroticismo (Baja Estabilidad Emocional):** Eres propenso a experimentar ansiedad, tristeza, preocupación e inestabilidad emocional. Reaccionas intensamente al estrés y te cuesta recuperar la calma tras un evento negativo.",
            "Medio": "**Moderado en Neuroticismo (Sensible):** Eres capaz de gestionar el estrés en la mayoría de las situaciones, aunque puedes experimentar cierta ansiedad o preocupación en momentos de gran presión o incertidumbre.",
            "Bajo": "**Bajo en Neuroticismo (Alta Estabilidad Emocional):** Eres tranquilo, estable, resiliente y rara vez te sientes ansioso o perturbado. Muestras una gran capacidad para manejar el estrés y mantener un estado de ánimo positivo y uniforme."
        }
    }
    
    # Determinar Color y Código de Color
    if trait == 'N':
        # Neuroticism: Bajo (Low N) es deseable/estable.
        if level == "Bajo":
            color_hex = LEVEL_COLORS["Estable"] 
            color_label = "Muy Estable"
        elif level == "Alto":
            color_hex = LEVEL_COLORS["Bajo_Negativo"] 
            color_label = "Inestable"
        else:
            color_hex = LEVEL_COLORS["Medio"]
            color_label = "Moderado"
    else:
        # Otros rasgos: Alto es más pronunciado.
        if level == "Alto":
            color_hex = LEVEL_COLORS["Alto_Positivo"] 
            color_label = "Muy Pronunciado"
        elif level == "Bajo":
            color_hex = LEVEL_COLORS["Bajo_Negativo"] 
            color_label = "Bajo"
        else:
            color_hex = LEVEL_COLORS["Medio"]
            color_label = "Moderado"

    return profiles[trait][level], level, color_hex, color_label

# --- 3. FUNCIONES DE NAVEGACIÓN Y REINICIO ---

def next_page():
    """Avanza a la siguiente página del test."""
    if st.session_state.current_page < TOTAL_PAGES - 1:
        st.session_state.current_page += 1
        st.session_state.error_message = "" # Limpia el mensaje de error al avanzar

def prev_page():
    """Retrocede a la página anterior del test."""
    if st.session_state.current_page > 0:
        st.session_state.current_page -= 1
        st.session_state.error_message = ""

def check_page_completion(action):
    """Verifica que todas las preguntas de la página actual estén respondidas."""
    current_page = st.session_state.current_page
    start_index = current_page * QUESTIONS_PER_PAGE
    end_index = min(start_index + QUESTIONS_PER_PAGE, TOTAL_QUESTIONS)
    
    questions_on_page = [q['id'] for q in QUESTIONS[start_index:end_index]]
    
    # Comprobar cuántas preguntas han sido respondidas en esta página
    answered_count = sum(1 for q_id in questions_on_page if q_id in st.session_state.answers)
    
    if answered_count == len(questions_on_page):
        # Si están todas respondidas
        if action == "next":
            next_page()
        elif action == "finish":
            # Si es la última página, procede a finalizar el test
            st.session_state.test_completed = True
            st.session_state.error_message = ""
    else:
        # Si faltan preguntas
        st.session_state.error_message = "⚠️ Por favor, responde las " + str(len(questions_on_page) - answered_count) + " preguntas restantes de esta página antes de continuar."


def restart_test():
    """
    Resets the session state to restart the test.
    (Fix: Avoids st.rerun() in callback to prevent the 'no-op' warning)
    """
    st.session_state.answers = {}
    st.session_state.test_completed = False
    st.session_state.current_page = 0
    st.session_state.error_message = ""
    # st.rerun() ya no es necesario aquí, la modificación del estado provoca la reejecución.

# --- 4. CONFIGURACIÓN VISUAL Y DE INTERFAZ (CSS Profesional + Print Media) ---

def set_professional_style():
    """Aplica estilos CSS profesionales y de impresión."""
    st.markdown(f"""
    <style>
        /* Fuente y Estilo General */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
        html, body, [class*="st-"] {{
            font-family: 'Inter', sans-serif;
        }}
        
        /* Contenedor Principal */
        .main {{
            background-color: #F8F9FA; 
            border-radius: 12px;
            padding: 20px;
        }}
        
        /* Títulos y Encabezados */
        h1 {{
            color: #004AAD; 
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

        /* Estilo de las Preguntas (Controles) */
        .stRadio > label {{
            font-size: 1.05rem;
            font-weight: 500;
            color: #1f2937;
            margin-bottom: 15px;
            padding: 10px 0;
            display: block;
            border-left: 4px solid #D1D5DB; 
            padding-left: 15px;
            background-color: #FFFFFF;
            border-radius: 4px;
        }}
        .stRadio div[role="radiogroup"] {{
            display: flex;
            flex-direction: row; 
            gap: 15px;
            padding-bottom: 20px;
            border-bottom: 1px solid #E5E7EB;
            margin-bottom: 25px;
            flex-wrap: wrap; 
        }}
        /* Estilo para los labels del radio button para que sean claros */
        .stRadio div[role="radiogroup"] > label {{
            font-size: 0.9rem !important;
            border: 1px solid #CCC !important;
            padding: 8px 12px !important;
            border-radius: 6px !important;
            cursor: pointer;
            transition: all 0.2s;
            background-color: #F9F9F9;
        }}
        /* Estilo cuando el radio button está seleccionado */
        .stRadio div[role="radiogroup"] input:checked + div + div > label {{
            background-color: #004AAD !important;
            color: white !important;
            border-color: #004AAD !important;
            font-weight: 600;
        }}

        /* Contenedor de Resultados (para el PDF) */
        .profile-container {{
            background-color: #ffffff;
            border: 1px solid #E5E7EB;
            border-radius: 10px;
            padding: 25px;
            margin-top: 30px;
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.08);
        }}
        
        /* Botones de Navegación */
        .stButton>button:not(.restart-btn) {{
            background-color: #004AAD; 
            color: white;
            font-weight: 600;
            padding: 10px 20px;
            border-radius: 8px;
            border: none;
            transition: background-color 0.3s;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        }}
        .stButton>button:hover:not(.restart-btn) {{
            background-color: #003A8D; 
        }}
        /* Botón de Reinicio */
        .restart-btn button {{
            background-color: #6C757D !important;
            color: white !important;
        }}
        .restart-btn button:hover {{
            background-color: #5A6268 !important;
        }}

        /* Estilo para el botón de Imprimir/PDF (Green) */
        .print-button-container button {{
            background-color: #16A085 !important; /* Success Green */
            color: white !important;
            font-weight: 600;
            padding: 10px 20px;
            border-radius: 8px;
            border: none;
            transition: background-color 0.3s;
            box-shadow: 0 0 10px rgba(22, 160, 133, 0.4);
            cursor: pointer;
            width: 100%;
        }}
        .print-button-container button:hover {{
            background-color: #138D73 !important;
        }}
        
        /* === Media Query para Impresión (Limpieza profesional del PDF) === */
        @media print {{
            /* Ocultar todos los controles de la encuesta y la navegación */
            .stRadio, .stButton, .css-18z244q, .css-1d2a4o5, .stProgress:not(.results-progress), 
            .stAlert, .stSelectbox, .stTextInput, .print-button-container, 
            .stButton, .stProgress, 
            .stMarkdown:first-of-type, /* Esconde la descripción inicial */
            .css-fg4pbf, /* Esconde la navegación con columnas */
            .stMetric [data-testid="stMetricDelta"] /* Oculta el delta para limpiar */
            {{
                display: none !important;
            }}
            /* Forzar visualización de Títulos y Resultados */
            .profile-container, .trait-header, .stAlert, .stMetric, .stMarkdown, .stMarkdown > div > hr {{
                display: block !important;
                visibility: visible !important;
            }}
            /* Forzar color de fondo blanco para el PDF */
            .main {{
                background-color: white !important;
                padding: 10px !important;
                border: none !important;
                box-shadow: none !important;
            }}
            /* Asegurar visibilidad de texto */
            .profile-container h2, .trait-header, .stAlert p {{
                color: #000000 !important;
            }}
        }}

    </style>
    """, unsafe_allow_html=True)

# --- 5. FLUJO DE LA APLICACIÓN STREAMLIT ---

def run_test():
    """Función principal para correr la aplicación."""
    
    set_professional_style()

    # Inicializar el estado de la sesión
    if 'answers' not in st.session_state:
        st.session_state.answers = {}
    if 'test_completed' not in st.session_state:
        st.session_state.test_completed = False
    if 'current_page' not in st.session_state:
        st.session_state.current_page = 0
    if 'error_message' not in st.session_state:
        st.session_state.error_message = ""
        
    # Título y Encabezado
    st.markdown(f"""
    <div style="display: flex; align-items: center; margin-bottom: 20px;">
        <svg width="40" height="40" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M12 2C6.48 2 2 6.48 2 12C2 17.52 6.48 22 12 22C17.52 22 22 17.52 22 12C22 6.48 17.52 2 12 2ZM15 16H9V14H15V16ZM15 12H9V10H15V12ZM15 8H9V6H15V8Z" fill="#004AAD"/>
        </svg>
        <span style="font-size: 2rem; font-weight: 700; color: #004AAD; margin-left: 10px;">Perfil | OCEAN</span>
    </div>
    """, unsafe_allow_html=True)
    st.title("Test de Personalidad - Modelo de los Cinco Grandes (60 Ítems)")
    
    
    # --- A. Mostrar Resultados (Si el test está completado) ---
    if st.session_state.test_completed:
        
        # Simular una carga para mayor profesionalismo
        with st.spinner('Analizando y generando perfil de personalidad...'):
            time.sleep(1.5)

        # 1. Calcular la puntuación
        scores = calculate_score(st.session_state.answers)
        
        # 2. Mostrar el Perfil Container
        st.markdown(
            f"""
            <div class="profile-container">
                <h2>✅ Perfil de Personalidad Completado: Análisis Detallado</h2>
                <p>Tu análisis está basado en el **Modelo OCEAN**. La puntuación total por rasgo es de 60 puntos, donde 
                una puntuación alta indica una mayor intensidad de esa característica. El siguiente reporte es apto para impresión PDF.</p>
            </div>
            """, 
            unsafe_allow_html=True
        )
        
        # 3. Iterar y Mostrar Resultados
        for trait_code, score in scores.items():
            profile_text, level, color_hex, color_label = interpret_score(score, trait_code)
            trait_label = TRAIT_LABELS[trait_code]
            
            # Normalizar score para la barra de progreso (0 a 1.0). Rango 12-60 (48 puntos)
            normalized_score = (score - 12) / 48
            
            # Encabezado del Trait y Score
            st.markdown(f"""
            <div class="trait-header">
                {trait_label}
            </div>
            """, unsafe_allow_html=True)
            
            # Usar columnas para la visualización del resultado
            col_bar, col_score = st.columns([0.7, 0.3])

            with col_bar:
                # Se utiliza el HTML para inyectar el color dinámico y asegurar que el CSS de impresión lo mantenga
                st.markdown(f"""
                <div style="font-size: 0.9rem; color: #555;">Nivel Detectado: <b>{level}</b></div>
                <div style="height: 20px; border-radius: 4px; background-color: #E0E0E0; margin-top: 5px;">
                    <div style="width: {normalized_score*100}%; height: 100%; background-color: {color_hex}; border-radius: 4px;"></div>
                </div>
                """, unsafe_allow_html=True)

            with col_score:
                st.metric(label="Puntuación", value=f"{score}/60")
            
            # Mostrar la descripción
            st.info(profile_text, icon="💡")
            st.markdown("---")
        
        st.success("El análisis de tu perfil de personalidad ha concluido con éxito.")

        # 4. Botones de acción final (Imprimir y Reiniciar)
        col_print, col_restart = st.columns([0.6, 0.4])
        
        # Botón para Imprimir/Guardar como PDF (usa JavaScript nativo)
        with col_print:
            st.markdown("""
            <div class="print-button-container">
                <button onclick="window.print()">
                    🖨️ Imprimir/Guardar como PDF Profesional
                </button>
            </div>
            """, unsafe_allow_html=True)


        # Botón para reiniciar
        with col_restart:
            st.markdown('<div class="restart-btn">', unsafe_allow_html=True)
            st.button("🔄 Volver a Realizar el Test", on_click=restart_test, type="secondary", use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
            
            
    # --- B. Mostrar Cuestionario Paginado ---
    else:
        
        current_page = st.session_state.current_page
        start_index = current_page * QUESTIONS_PER_PAGE
        end_index = min(start_index + QUESTIONS_PER_PAGE, TOTAL_QUESTIONS)
        
        current_questions = QUESTIONS[start_index:end_index]
        
        # Visualización del Progreso y Página Actual
        answered_total = len(st.session_state.answers)
        progress_text = f"Progreso General: {answered_total}/{TOTAL_QUESTIONS} Preguntas"
        st.progress(answered_total / TOTAL_QUESTIONS, text=progress_text)
        
        st.subheader(f"Página {current_page + 1} de {TOTAL_PAGES}")
        st.markdown("---")

        # Mensaje de error (si existe)
        if st.session_state.error_message:
            st.error(st.session_state.error_message)

        
        # Controles de la Página Actual
        with st.form(key=f'page_form_{current_page}'):
            
            # Lista de opciones con el formato (Etiqueta, Valor)
            likert_options_tuple = [(v, k) for k, v in LIKERT_OPTIONS.items()]

            for q in current_questions:
                try:
                    # Recupera el valor de la respuesta si existe para mantener la selección
                    current_value = st.session_state.answers.get(q['id'])
                    # La tupla de opciones está en formato (String, Int). Buscamos por el valor.
                    current_index = [t[1] for t in likert_options_tuple].index(current_value) if current_value else -1
                    # Nota: Streamlit usa index para el valor inicial de radio, -1 si no hay valor
                except (ValueError, KeyError):
                    current_index = -1

                # El índice inicial en st.radio debe ser None o el índice (0-base) de la opción.
                # Si current_value es 1 (Totalmente en desacuerdo), su índice en likert_options_tuple es 4
                selected_index = current_index if current_index != -1 else None
                
                response_tuple = st.radio(
                    label=f"**{q['id']}.** {q['text']}",
                    options=likert_options_tuple,
                    key=f"question_{q['id']}",
                    index=selected_index,
                    format_func=lambda x: x[0]
                )
                
                # Almacenar el valor (el entero, que está en response_tuple[1])
                if response_tuple is not None:
                    st.session_state.answers[q['id']] = response_tuple[1]

            # --- Botones de Navegación ---
            st.markdown("---")
            col_prev, col_next_finish = st.columns([1, 1])

            with col_prev:
                if current_page > 0:
                    st.form_submit_button("← Anterior", on_click=prev_page)

            with col_next_finish:
                is_last_page = current_page == TOTAL_PAGES - 1
                
                if is_last_page:
                    st.form_submit_button("Finalizar Test y Ver Mi Perfil", on_click=check_page_completion, args=("finish",), type="primary")
                else:
                    st.form_submit_button(f"Siguiente → (Pág. {current_page + 2})", on_click=check_page_completion, args=("next",), type="secondary")
                    
# Ejecutar la aplicación
if __name__ == '__main__':
    run_test()
