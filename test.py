import streamlit as st
from collections import defaultdict
import time 

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
    {"id: "O9", "text": "A menudo me pierdo en mis pensamientos o ideas.", "trait": "O", "reverse": False},
    {"id": "O10", "text": "Raramente busco aprender habilidades que no sean directamente útiles.", "trait": "O", "reverse": True},
    {"id": "O11", "text": "Disfruto de exposiciones de arte y música poco convencional.", "trait": "O", "reverse": False},
    {"id": "O12", "text": "Para mí, 'lo nuevo' a menudo significa 'peligroso'.", "trait": "O", "reverse": True},
    
    # C - Responsabilidad (Conscientiousness)
    {"id": "C1", "text": "Siempre me preparo con antelación para mis tareas y compromisos.", "trait": "C", "reverse": False},
    {"id": "C2", "text": "Soy muy metódico y ordenado en mi trabajo y mi casa.", "trait": "C", "reverse": False},
    {"id": "C3", "text": "A menudo me olvido de mis deberes y responsabilidades.", "trait": "C", "reverse": True},
    {"id": "C4", "text": "Trabajo con diligencia hasta completar cualquier tarea que comience.", "trait": "C", "reverse": False},
    {"id": "C5", "text": "No me importa dejar las cosas sin terminar si pierdo el interés.", "trait": "C", "reverse": True},
    {"id: "C6", "text": "Siempre procuro mantener mis promesas y compromisos.", "trait": "C", "reverse": False},
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
    {"id: "A10", "text": "Soy muy directo y no me importa criticar a los demás.", "trait": "A", "reverse": True},
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
MAX_SCORE_PER_TRAIT = 12 * 5 # 12 preguntas * 5 puntos max = 60
MIN_SCORE_PER_TRAIT = 12 * 1 # 12 preguntas * 1 punto min = 12

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
    "Bajo_Negativo": "#C0392B",  # Rojo
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
                score = 6 - score 
            
            scores[trait] += score
            
    return dict(scores)

def interpret_score(score, trait):
    """
    Interpreta la puntuación (Bajo, Medio, Alto) y devuelve el texto del perfil y las áreas de mejora.
    Rango de score: 12 (min) a 60 (max).
    """
    # Umbrales (Aproximadamente tercios del rango 12-60. Ancho de rango: 48)
    LOW_THRESHOLD = 28
    HIGH_THRESHOLD = 44
    
    if score <= LOW_THRESHOLD:
        level = "Bajo"
    elif score >= HIGH_THRESHOLD:
        level = "Alto"
    else:
        level = "Medio"
        
    # --- Descripciones Detalladas y Áreas de Mejora ---
    profiles = {
        "O": {
            "Alto": {
                "desc": "Eres un **Explorador** innato, sumamente curioso, creativo y con una mente siempre abierta. Disfrutas de la complejidad, el arte y la diversidad. Esto te impulsa a la innovación y al crecimiento constante. Sin embargo, debes tener cuidado de no perder el foco en la practicidad.",
                "improvement": "A veces, la búsqueda constante de novedad puede llevarte a iniciar muchos proyectos sin finalizar ninguno. **Mejora:** Practica la disciplina de terminar lo que empiezas, enfocándote en implementar las ideas brillantes que ya tienes antes de pasar a la siguiente."
            },
            "Medio": {
                "desc": "Tienes un **perfil Equilibrado**, combinando la curiosidad y la apertura al cambio con un fuerte sentido de la estabilidad. Eres adaptable, pero no impulsivo, y puedes interactuar con éxito tanto en entornos creativos como tradicionales.",
                "improvement": "Tu equilibrio es tu fuerza, pero a veces puedes caer en una 'zona de confort'. **Mejora:** Desafíate a salir de la rutina de forma intencional y a profundizar en un área de conocimiento completamente nueva, superando la tendencia a ser demasiado pragmático."
            },
            "Bajo": {
                "desc": "Eres **Pragmático y Convencional**. Prefieres la familiaridad, la tradición y los métodos probados. Tu enfoque está en los hechos concretos y la utilidad práctica, lo que te hace muy eficiente en tareas bien definidas. Tiendes a resistirte a ideas demasiado abstractas.",
                "improvement": "Tu aversión al riesgo y a lo desconocido puede limitar tu potencial de crecimiento. **Mejora:** Busca activamente perspectivas diferentes a las tuyas, lee sobre temas que te incomoden intelectualmente y practica la empatía cognitiva para entender cómo otros abordan el mundo."
            }
        },
        "C": {
            "Alto": {
                "desc": "Eres un **Estratega y Organizado**. Muestras un alto nivel de autodisciplina, eres confiable, orientado a metas y meticuloso en los detalles. Tu ética de trabajo es ejemplar y siempre planeas con mucha antelación.",
                "improvement": "Tu perfeccionismo y rigor pueden llevar al agotamiento o a la inflexibilidad. **Mejora:** Aprende a delegar y a aceptar que 'suficientemente bueno' es a veces mejor que perfecto. Permítete períodos de espontaneidad para recargar tu energía y reducir el estrés."
            },
            "Medio": {
                "desc": "Eres una persona **Eficaz y Flexible**. Tienes la capacidad de organizarte y cumplir con los plazos, pero valoras la flexibilidad. Eres confiable, pero no te agobia la rigidez, permitiendo ajustes cuando la situación lo requiere.",
                "improvement": "Asegúrate de que tu flexibilidad no se convierta en inconsistencia. **Mejora:** Define objetivos intermedios más claros para evitar la procrastinación en tareas de baja prioridad y utiliza herramientas de gestión de tiempo para monitorear tu progreso de manera más sistemática."
            },
            "Bajo": {
                "desc": "Eres **Espontáneo y Despreocupado**. Priorizas la flexibilidad y la improvisación sobre el orden riguroso. Te sientes cómodo con el caos y puedes adaptarte rápidamente a los cambios, pero tiendes a la procrastinación y a un enfoque desorganizado.",
                "improvement": "Tu falta de estructura puede sabotear el logro de objetivos a largo plazo. **Mejora:** Implementa pequeñas rutinas diarias (ej. 15 minutos de planificación) y divide las tareas grandes en pasos minúsculos. Concéntrate en cumplir los compromisos, pues tu reputación depende de ello."
            }
        },
        "E": {
            "Alto": {
                "desc": "Eres un **Líder Sociable**, enérgico, asertivo y te revitalizas con la interacción. Disfrutas siendo el centro de atención, eres entusiasta y buscas activamente el contacto social. Tienes una gran influencia en grupos.",
                "improvement": "Tu necesidad de estimulación puede hacer que hables antes de escuchar o que evites la introspección. **Mejora:** Cultiva la escucha activa y programa tiempo de reflexión a solas. Desarrolla la empatía y asegúrate de que tu entusiasmo no abrume a las personas más reservadas."
            },
            "Medio": {
                "desc": "Tienes un **perfil Ambivertido**. Disfrutas de la compañía, pero también valoras profundamente el tiempo a solas. Eres un buen comunicador y puedes adaptarte a roles tanto sociales como independientes, gestionando bien tus niveles de energía.",
                "improvement": "Tu versatilidad puede llevar a la confusión sobre lo que realmente te energiza. **Mejora:** Sé más consciente de tus límites sociales; cuando te sientas agotado, no temas rechazar planes para dedicarte al tiempo de inactividad necesario para recargarte."
            },
            "Bajo": {
                "desc": "Eres **Reservado e Introvertido**. Prefieres la soledad, las interacciones profundas y te sientes agotado por las grandes multitudes. Eres reflexivo, observador y sueles ser muy cauteloso al hablar.",
                "improvement": "Tu reserva puede hacer que pierdas oportunidades de *networking* o que tus ideas no sean escuchadas. **Mejora:** Practica la asertividad controlada: prepárate para compartir tus ideas en reuniones con antelación y establece un mínimo de interacciones sociales estratégicas a la semana."
            }
        },
        "A": {
            "Alto": {
                "desc": "Eres **Cooperativo y Compasivo**. Eres empático, de buen corazón y buscas activamente la armonía en todas tus relaciones. Eres el mediador natural, impulsado por el deseo de ayudar y evitar el conflicto.",
                "improvement": "Tu deseo de agradar puede llevarte a descuidar tus propias necesidades o a ser explotado. **Mejora:** Aprende a establecer límites firmes y a decir 'no' sin sentir culpa. Practica la asertividad cuando sea necesario defender tus derechos o los de tu equipo, sin buscar siempre el consenso absoluto."
            },
            "Medio": {
                "desc": "Eres **Amable y Justo**. Eres generalmente agradable y cooperativo, pero mantienes un saludable escepticismo y puedes defender tus propios intereses. Eres un buen jugador de equipo que exige reciprocidad y justicia.",
                "improvement": "En situaciones de conflicto, puedes volverte excesivamente cauteloso para no ofender. **Mejora:** Aumenta tu confianza para expresar críticas constructivas directamente. Trabaja en distinguir entre amabilidad genuina y la necesidad de aprobación."
            },
            "Bajo": {
                "desc": "Eres **Desafiante y Escéptico**. Tiendes a ser competitivo, directo, y priorizas la verdad y tus intereses sobre la sensibilidad ajena. Tu escepticismo te hace resistente a la manipulación y excelente para negociar.",
                "improvement": "Tu franqueza puede ser percibida como frialdad o hostilidad, dificultando las alianzas. **Mejora:** Esfuérzate por 'suavizar el mensaje'. Antes de criticar, valida el esfuerzo del otro. Desarrolla activamente la empatía para entender por qué otros reaccionan emocionalmente."
            }
        },
        "N": {
            "Alto": {
                "desc": "Tu **Estabilidad Emocional es Baja (Reactiva)**. Eres muy sensible al estrés y experimentas ansiedad, preocupación e ira con facilidad. Tu estado de ánimo es a menudo volátil y te cuesta recuperar la calma tras un evento negativo.",
                "improvement": "La alta reactividad emocional consume energía y dificulta la toma de decisiones. **Mejora:** Implementa técnicas de manejo del estrés (meditación, respiración). Cuestiona tus pensamientos negativos (¿es esto un hecho o una emoción?). Busca la estabilidad en rutinas diarias predecibles."
            },
            "Medio": {
                "desc": "Tienes una **Estabilidad Emocional Moderada (Sensible)**. Eres capaz de gestionar el estrés diario, pero puedes volverte ansioso o preocupado bajo presión intensa. Eres empático con las emociones, pero mantienes un buen control la mayoría del tiempo.",
                "improvement": "Asegúrate de que no estás suprimiendo la ansiedad en lugar de gestionarla. **Mejora:** Identifica los detonantes de tu estrés y trabaja en estrategias preventivas. Evita la sobrecarga de trabajo y asegúrate de tener válvulas de escape saludables."
            },
            "Bajo": {
                "desc": "Tu **Estabilidad Emocional es Alta (Resiliente)**. Eres tranquilo, estable, resiliente y rara vez te sientes perturbado. Muestras una gran capacidad para manejar el estrés y recuperarte rápidamente de los contratiempos.",
                "improvement": "Tu calma puede ser malinterpretada como indiferencia o falta de compromiso. **Mejora:** Sé consciente de las emociones de quienes te rodean y valida sus sentimientos (aunque no los compartas). Esto mejorará tu conexión interpersonal sin sacrificar tu estabilidad."
            }
        }
    }
    
    # Determinar Color y Código de Color (sin cambios)
    if trait == 'N':
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
        if level == "Alto":
            color_hex = LEVEL_COLORS["Alto_Positivo"] 
            color_label = "Muy Pronunciado"
        elif level == "Bajo":
            color_hex = LEVEL_COLORS["Bajo_Negativo"] 
            color_label = "Bajo"
        else:
            color_hex = LEVEL_COLORS["Medio"]
            color_label = "Moderado"
            
    # Retorna un diccionario más estructurado
    return {
        "level": level, 
        "color_hex": color_hex, 
        "color_label": color_label,
        "description": profiles[trait][level]["desc"],
        "improvement": profiles[trait][level]["improvement"]
    }

# --- 3. FUNCIONES DE NAVEGACIÓN Y REINICIO ---

def next_page():
    """Avanza a la siguiente página del test."""
    if st.session_state.current_page < TOTAL_PAGES - 1:
        st.session_state.current_page += 1
        st.session_state.error_message = "" 

def prev_page():
    """Retrocede a la página anterior del test."""
    if st.session_state.current_page > 0:
        st.session_state.current_page -= 1
        st.session_state.error_message = ""

def restart_test():
    """Resets the session state to restart the test."""
    st.session_state.answers = {}
    st.session_state.test_completed = False
    st.session_state.current_page = 0
    st.session_state.error_message = ""
    # No se usa st.rerun() en el callback, lo que soluciona la advertencia "no-op".

# --- 4. CONFIGURACIÓN VISUAL Y DE INTERFAZ (CSS Profesional + Print Media) ---

def set_professional_style():
    """Aplica estilos CSS profesionales, de impresión y el script para scroll."""
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
            .stAlert:not(.result-alert), .stSelectbox, .stTextInput, .print-button-container, 
            .stButton, 
            .stMarkdown:first-of-type, /* Esconde la descripción inicial */
            .css-fg4pbf, .stMetric [data-testid="stMetricDelta"] /* Oculta el delta */
            {{
                display: none !important;
            }}
            /* Forzar visualización de Títulos y Resultados */
            .profile-container, .trait-header, .stAlert.result-alert, .stMetric, .stMarkdown, .stMarkdown > div > hr {{
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
            .stAlert {{
                border-left: 5px solid #004AAD !important;
            }}
            /* Asegurar visibilidad de texto */
            .profile-container h2, .trait-header, .stAlert.result-alert p {{
                color: #000000 !important;
            }}
        }}

    </style>
    """, unsafe_allow_html=True)
    
    # Script para forzar el scroll al inicio de la página en cada navegación
    st.markdown(
        """
        <script>
            function scrollToTop() {
                const main = document.querySelector('.main');
                if (main) {
                    main.scrollTo(0, 0);
                } else {
                    window.scrollTo(0, 0);
                }
            }
            scrollToTop();
        </script>
        """,
        unsafe_allow_html=True
    )

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
        with st.spinner('Analizando y generando perfil de personalidad detallado...'):
            time.sleep(1.5)

        # 1. Calcular la puntuación
        scores = calculate_score(st.session_state.answers)
        
        # 2. Mostrar el Perfil Container
        st.markdown(
            f"""
            <div class="profile-container">
                <h2>✅ Informe de Perfil Detallado</h2>
                <p>Este análisis se basa en el **Modelo OCEAN**. La puntuación máxima por rasgo es 60. Utiliza la opción de "Imprimir" en tu navegador para guardar este informe como PDF.</p>
            </div>
            """, 
            unsafe_allow_html=True
        )
        
        # 3. Iterar y Mostrar Resultados
        for trait_code, score in scores.items():
            results = interpret_score(score, trait_code)
            trait_label = TRAIT_LABELS[trait_code]
            
            # Normalizar score para la barra de progreso (0 a 1.0). Rango 12-60 (48 puntos)
            normalized_score = (score - MIN_SCORE_PER_TRAIT) / (MAX_SCORE_PER_TRAIT - MIN_SCORE_PER_TRAIT)
            
            # Encabezado del Trait y Score
            st.markdown(f"""
            <div class="trait-header">
                <h3>{trait_label}</h3>
            </div>
            """, unsafe_allow_html=True)
            
            # Usar columnas para la visualización del resultado
            col_bar, col_score = st.columns([0.7, 0.3])

            with col_bar:
                # Visualización de la barra de progreso con color dinámico
                st.markdown(f"""
                <div style="font-size: 0.9rem; color: #555;">Nivel Detectado: <b>{results['level']} ({results['color_label']})</b></div>
                <div style="height: 20px; border-radius: 4px; background-color: #E0E0E0; margin-top: 5px;">
                    <div style="width: {normalized_score*100}%; height: 100%; background-color: {results['color_hex']}; border-radius: 4px;"></div>
                </div>
                """, unsafe_allow_html=True)

            with col_score:
                st.metric(label="Puntuación", value=f"{score}/{MAX_SCORE_PER_TRAIT}")
            
            # Mostrar la descripción detallada
            st.markdown(f"**Análisis:** {results['description']}")
            
            # Mostrar las áreas de mejora en un bloque distintivo
            st.markdown(
                f'<div class="result-alert">', unsafe_allow_html=True
            )
            st.info(f"**💡 Consejos y Áreas de Crecimiento:** {results['improvement']}", icon="⭐")
            st.markdown('</div>', unsafe_allow_html=True)
            
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

        # Mensaje de error (si existe)
        if st.session_state.error_message:
            st.error(st.session_state.error_message)

        
        # Controles de la Página Actual (DENTRO DEL FORMULARIO)
        # Esto soluciona el problema del doble click al asegurar que los valores se actualicen al someter el form.
        with st.form(key=f'page_form_{current_page}'):
            
            # Lista de opciones con el formato (Etiqueta, Valor)
            likert_options_tuple = [(v, k) for k, v in LIKERT_OPTIONS.items()]
            
            # Diccionario para almacenar las respuestas de la página antes de la validación
            form_answers_current_page = {}

            for q in current_questions:
                q_id = q['id']
                
                # Recuperar valor actual de la sesión (para que persista)
                current_value = st.session_state.answers.get(q_id)
                selected_index = [t[1] for t in likert_options_tuple].index(current_value) if current_value else -1
                
                response_tuple = st.radio(
                    label=f"**{q_id}.** {q['text']}",
                    options=likert_options_tuple,
                    key=f"radio_{q_id}", # La clave debe ser única
                    index=selected_index if selected_index != -1 else None,
                    format_func=lambda x: x[0]
                )
                
                # Almacenar el valor seleccionado dentro del contexto del formulario
                if response_tuple is not None:
                    form_answers_current_page[q_id] = response_tuple[1]

            # --- Botones de Navegación ---
            st.markdown("---")
            col_prev, col_next_finish = st.columns([1, 1])

            with col_prev:
                if current_page > 0:
                    prev_button = st.form_submit_button("← Anterior")

            with col_next_finish:
                is_last_page = current_page == TOTAL_PAGES - 1
                
                if is_last_page:
                    submit_button = st.form_submit_button("Finalizar Test y Ver Mi Perfil", type="primary")
                else:
                    submit_button = st.form_submit_button(f"Siguiente → (Pág. {current_page + 2})", type="secondary")
        
        # --- Lógica de Manejo de Formulario (Fuera del bloque `with st.form`) ---
        
        if 'prev_button' in locals() and prev_button:
            # Si se presiona Anterior, simplemente se navega (no necesita validación)
            prev_page()
            st.rerun()

        if 'submit_button' in locals() and submit_button:
            # Primero, actualizamos el estado de la sesión con las respuestas del formulario
            st.session_state.answers.update(form_answers_current_page)
            
            # 1. Validar si todas las preguntas de esta página fueron respondidas
            answered_count_on_page = len(form_answers_current_page)
            questions_on_page_count = len(current_questions)

            if answered_count_on_page < questions_on_page_count:
                # Falla la validación
                st.session_state.error_message = f"⚠️ Por favor, responde las {questions_on_page_count - answered_count_on_page} preguntas restantes antes de continuar."
                st.rerun()
            else:
                # Pasa la validación
                st.session_state.error_message = "" # Limpiar error
                
                if is_last_page:
                    st.session_state.test_completed = True
                    st.rerun()
                else:
                    # Avanzar a la siguiente página
                    next_page()
                    st.rerun() # Forzar la reejecución para mostrar la nueva página

# Ejecutar la aplicación
if __name__ == '__main__':
    run_test()
