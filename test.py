import streamlit as st
from collections import defaultdict
import time
import pandas as pd
import plotly.graph_objects as go
import numpy as np

# --- CONFIGURACIÓN DE PÁGINA Y ESTILO INYECTADO (Ultra-Moderno) ---

# Usamos el layout "wide" para aprovechar el espacio en escritorio.
st.set_page_config(layout="wide", page_title="Test Big Five Detallado", initial_sidebar_state="collapsed")

# Definición de colores vibrantes
COLOR_VIBRANT_BLUE = "#4A90E2"  # Principal para Alto/Positivo
COLOR_MINT_GREEN = "#50E3C2"    # Para Neuroticismo Bajo (Estabilidad)
COLOR_WARNING_ORANGE = "#F5A623" # Para Nivel Medio
COLOR_DANGER_RED = "#D0021B"    # Para Nivel Bajo o Neuroticismo Alto

LEVEL_COLORS = {
    "Alto_Positivo": COLOR_VIBRANT_BLUE,
    "Bajo_Negativo": COLOR_DANGER_RED,
    "Medio": COLOR_WARNING_ORANGE,
    "Estable": COLOR_MINT_GREEN
}

st.markdown(f"""
    <style>
        /* 1. Fuente y Tema Oscuro Principal */
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;700&display=swap');
        html, body, [class*="st-"] {{
            font-family: 'Poppins', sans-serif;
        }}
        .main, .stApp {{
            background-color: #0d1117; /* GitHub Dark Theme Background */
            color: #c9d1d9;
        }}

        /* 2. Cabeceras y Título Principal */
        h1 {{
            color: {COLOR_VIBRANT_BLUE};
            text-align: center;
            font-size: 2.8em;
            padding-bottom: 10px;
            border-bottom: 4px solid {COLOR_MINT_GREEN}; /* Línea de Énfasis */
        }}
        h2, h3 {{
            color: #ffffff; /* Blanco Puro */
        }}

        /* 3. Estilo para las Tarjetas de Pregunta (Contenedores) */
        .stContainer, [data-testid="stVerticalBlock"] {{
            background-color: #161b22; /* Fondo de Tarjeta más oscuro */
            padding: 15px 25px;
            border-radius: 12px;
            margin-bottom: 15px;
            border-left: 5px solid {COLOR_VIBRANT_BLUE};
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.4); /* Sombra suave */
            transition: all 0.3s ease;
        }}
        .stContainer:hover {{
            border-left: 5px solid {COLOR_MINT_GREEN};
            box-shadow: 0 6px 20px rgba(74, 144, 226, 0.3);
        }}
        
        /* 4. Estilo para Sliders (Personalización de la escala Likert) */
        .stSlider label, .stMarkdown p {{
            font-weight: 500;
            color: #c9d1d9;
        }}
        
        /* 5. Botones de Navegación */
        .stButton>button {{
            background-color: {COLOR_VIBRANT_BLUE};
            color: white;
            font-weight: bold;
            border: none;
            border-radius: 8px;
            padding: 10px 20px;
            transition: all 0.3s ease;
            box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);
        }}
        .stButton>button:hover {{
            background-color: {COLOR_MINT_GREEN};
            color: #0d1117;
            transform: translateY(-1px);
        }}
        
        /* 6. Mensaje de Error (Destacado) */
        [data-testid="stNotification"] {{
            background-color: {COLOR_DANGER_RED} !important;
            color: white !important;
        }}
        
        /* 7. Estilo para la Interpretación de Resultados */
        .profile-card {{
            background-color: #161b22;
            padding: 20px;
            border-radius: 10px;
            margin-top: 15px;
            border: 1px solid #30363d;
        }}
        .profile-strength {{
            color: {COLOR_MINT_GREEN};
            font-weight: bold;
        }}
        .profile-challenge {{
            color: {COLOR_DANGER_RED};
            font-weight: bold;
        }}
    </style>
""", unsafe_allow_html=True)


# --- 1. CONFIGURACIÓN DEL TEST (BIG FIVE - OCEAN) ---

# Se ha escalado el test a 130 preguntas (26 por rasgo) para una medición más precisa.
# La estructura del test es (ID, Texto, Rasgo, Inversa)
QUESTIONS = [
    # O - Apertura a la Experiencia (Openness) - 26 items
    {"id": "O1", "text": "Disfruto profundamente con la exploración de ideas abstractas.", "trait": "O", "reverse": False},
    {"id": "O2", "text": "Tengo una imaginación muy vívida y disfruto soñando despierto.", "trait": "O", "reverse": False},
    {"id": "O3", "text": "Suelo probar comidas nuevas y explorar culturas diferentes.", "trait": "O", "reverse": False},
    {"id": "O4", "text": "Prefiero seguir métodos tradicionales y probados.", "trait": "O", "reverse": True},
    {"id": "O5", "text": "El arte y la poesía no me resultan particularmente interesantes.", "trait": "O", "reverse": True},
    {"id": "O6", "text": "Soy una persona muy curiosa intelectualmente y busco aprender.", "trait": "O", "reverse": False},
    {"id": "O7", "text": "Me encanta debatir conceptos filosóficos complejos.", "trait": "O", "reverse": False},
    {"id": "O8", "text": "Soy capaz de ignorar el ruido y las distracciones fácilmente.", "trait": "O", "reverse": True},
    {"id": "O9", "text": "A menudo me pierdo en mis pensamientos profundos.", "trait": "O", "reverse": False},
    {"id": "O10", "text": "No me molesta si mi entorno permanece igual durante mucho tiempo.", "trait": "O", "reverse": True},
    {"id": "O11", "text": "Valoro la belleza y la estética de las cosas que me rodean.", "trait": "O", "reverse": False},
    {"id": "O12", "text": "Me siento incómodo cuando las cosas cambian repentinamente.", "trait": "O", "reverse": True},
    {"id": "O13", "text": "Busco activamente experiencias que me hagan ver el mundo de otra manera.", "trait": "O", "reverse": False},
    {"id": "O14", "text": "Soy más un pensador práctico que teórico.", "trait": "O", "reverse": True},
    {"id": "O15", "text": "Disfruto de la música poco convencional o experimental.", "trait": "O", "reverse": False},
    {"id": "O16", "text": "Me resulta difícil entender las emociones ajenas a través del arte.", "trait": "O", "reverse": True},
    {"id": "O17", "text": "Siempre estoy abierto a reconsiderar mis puntos de vista sobre el universo.", "trait": "O", "reverse": False},
    {"id": "O18", "text": "El futuro me parece más seguro si es predecible.", "trait": "O", "reverse": True},
    {"id": "O19", "text": "Disfruto improvisando y creando cosas nuevas sin planificación.", "trait": "O", "reverse": False},
    {"id": "O20", "text": "No me gusta perder el tiempo en fantasías o especulaciones.", "trait": "O", "reverse": True},
    {"id": "O21", "text": "Me emociona aprender nuevos idiomas o habilidades complejas.", "trait": "O", "reverse": False},
    {"id": "O22", "text": "Prefiero las películas que son realistas a las de ciencia ficción.", "trait": "O", "reverse": True},
    {"id": "O23", "text": "Tengo la capacidad de relacionar ideas que parecen inconexas.", "trait": "O", "reverse": False},
    {"id": "O24", "text": "Sigo una línea estricta de pensamiento lógico y objetivo.", "trait": "O", "reverse": True},
    {"id": "O25", "text": "Me gusta experimentar con diferentes estilos de vida o roles.", "trait": "O", "reverse": False},
    {"id": "O26", "text": "Las teorías científicas complejas me aburren rápidamente.", "trait": "O", "reverse": True},

    # C - Responsabilidad (Conscientiousness) - 26 items
    {"id": "C1", "text": "Siempre me preparo meticulosamente con antelación.", "trait": "C", "reverse": False},
    {"id": "C2", "text": "Soy muy metódico, organizado y ordenado.", "trait": "C", "reverse": False},
    {"id": "C3", "text": "A menudo me olvido de mis deberes y responsabilidades importantes.", "trait": "C", "reverse": True},
    {"id": "C4", "text": "Trabajo con diligencia hasta completar cualquier tarea que comience.", "trait": "C", "reverse": False},
    {"id": "C5", "text": "Dejo cosas sin terminar si pierdo el interés inicial.", "trait": "C", "reverse": True},
    {"id": "C6", "text": "Siempre procuro mantener mis promesas, incluso las pequeñas.", "trait": "C", "reverse": False},
    {"id": "C7", "text": "Soy visto por otros como una persona extremadamente fiable y puntual.", "trait": "C", "reverse": False},
    {"id": "C8", "text": "Tengo dificultades para concentrarme en una sola cosa por mucho tiempo.", "trait": "C", "reverse": True},
    {"id": "C9", "text": "Establezco objetivos claros y trabajo sistemáticamente para alcanzarlos.", "trait": "C", "reverse": False},
    {"id": "C10", "text": "Mi espacio de trabajo o estudio es a menudo caótico.", "trait": "C", "reverse": True},
    {"id": "C11", "text": "Soy un perfeccionista que revisa cada detalle.", "trait": "C", "reverse": False},
    {"id": "C12", "text": "Tienden a describirme como impulsivo e irreflexivo en mis acciones.", "trait": "C", "reverse": True},
    {"id": "C13", "text": "Nunca llego tarde a una cita o compromiso.", "trait": "C", "reverse": False},
    {"id": "C14", "text": "Mis decisiones se basan a menudo en el impulso del momento.", "trait": "C", "reverse": True},
    {"id": "C15", "text": "Hago listas de tareas pendientes y las sigo rigurosamente.", "trait": "C", "reverse": False},
    {"id": "C16", "text": "No me importa si las cosas están ligeramente desordenadas.", "trait": "C", "reverse": True},
    {"id": "C17", "text": "Soy cauteloso y pienso en las consecuencias antes de actuar.", "trait": "C", "reverse": False},
    {"id": "C18", "text": "A veces pospongo mis tareas importantes hasta el último minuto.", "trait": "C", "reverse": True},
    {"id": "C19", "text": "Mantengo un horario estricto y lo sigo diariamente.", "trait": "C", "reverse": False},
    {"id": "C20", "text": "Soy perezoso y no me gusta hacer un esfuerzo extra.", "trait": "C", "reverse": True},
    {"id": "C21", "text": "Siempre busco la mejor manera y más eficiente de hacer una tarea.", "trait": "C", "reverse": False},
    {"id": "C22", "text": "Suelo perder o extraviar mis pertenencias personales.", "trait": "C", "reverse": True},
    {"id": "C23", "text": "Soy muy consciente de mis obligaciones financieras y las cumplo a tiempo.", "trait": "C", "reverse": False},
    {"id": "C24", "text": "No me gusta la planificación a largo plazo; prefiero la sorpresa.", "trait": "C", "reverse": True},
    {"id": "C25", "text": "La gente me pide ayuda para organizar eventos o proyectos.", "trait": "C", "reverse": False},
    {"id": "C26", "text": "Me rindo fácilmente cuando una tarea se vuelve demasiado difícil.", "trait": "C", "reverse": True},

    # E - Extraversión (Extraversion) - 26 items
    {"id": "E1", "text": "Soy el alma de la fiesta y busco el centro de atención.", "trait": "E", "reverse": False},
    {"id": "E2", "text": "Me gusta tener mucha gente a mi alrededor la mayor parte del tiempo.", "trait": "E", "reverse": False},
    {"id": "E3", "text": "Soy bastante reservado y tiendo a quedarme en un segundo plano.", "trait": "E", "reverse": True},
    {"id": "E4", "text": "Cuando estoy en un grupo, tiendo a ser el que más habla.", "trait": "E", "reverse": False},
    {"id": "E5", "text": "Prefiero las actividades que puedo realizar solo en casa.", "trait": "E", "reverse": True},
    {"id": "E6", "text": "Expreso mis opiniones y sentimientos con facilidad y confianza.", "trait": "E", "reverse": False},
    {"id": "E7", "text": "Soy muy entusiasta, ruidoso y enérgico.", "trait": "E", "reverse": False},
    {"id": "E8", "text": "Me aburro fácilmente si no hay mucha actividad o estimulación social.", "trait": "E", "reverse": False},
    {"id": "E9", "text": "Me resulta agotador pasar demasiado tiempo con otras personas.", "trait": "E", "reverse": True},
    {"id": "E10", "text": "Normalmente me siento incómodo al hablar con extraños.", "trait": "E", "reverse": True},
    {"id": "E11", "text": "Busco activamente nuevas amistades y contactos sociales.", "trait": "E", "reverse": False},
    {"id": "E12", "text": "Mi voz es baja y tiendo a hablar con mucha cautela.", "trait": "E", "reverse": True},
    {"id": "E13", "text": "Soy propenso a tomar riesgos y a buscar la aventura.", "trait": "E", "reverse": False},
    {"id": "E14", "text": "Disfruto en entornos silenciosos y de baja estimulación.", "trait": "E", "reverse": True},
    {"id": "E15", "text": "Me río mucho y mi risa es a menudo fuerte.", "trait": "E", "reverse": False},
    {"id": "E16", "text": "Soy lento para hacer nuevos amigos y conectar con la gente.", "trait": "E", "reverse": True},
    {"id": "E17", "text": "Me gusta organizar eventos sociales y reuniones.", "trait": "E", "reverse": False},
    {"id": "E18", "text": "Tiendo a ser un observador en lugar de un participante activo.", "trait": "E", "reverse": True},
    {"id": "E19", "text": "Cuando me siento feliz, lo muestro abiertamente.", "trait": "E", "reverse": False},
    {"id": "E20", "text": "No me gusta que me hagan preguntas personales.", "trait": "E", "reverse": True},
    {"id": "E21", "text": "En un equipo, prefiero tomar el papel de líder.", "trait": "E", "reverse": False},
    {"id": "E22", "text": "Me considero una persona sombría o seria.", "trait": "E", "reverse": True},
    {"id": "E23", "text": "Busco elogios y reconocimiento por mis logros.", "trait": "E", "reverse": False},
    {"id": "E24", "text": "Me siento más cómodo expresándome por escrito que hablando.", "trait": "E", "reverse": True},
    {"id": "E25", "text": "Soy rápido para responder y reaccionar en una conversación.", "trait": "E", "reverse": False},
    {"id": "E26", "text": "Necesito mucho tiempo a solas para pensar y recargar energía.", "trait": "E", "reverse": True},

    # A - Amabilidad (Agreeableness) - 26 items
    {"id": "A1", "text": "Siento una profunda empatía y compasión por los demás.", "trait": "A", "reverse": False},
    {"id": "A2", "text": "Generalmente confío en las buenas intenciones de la gente.", "trait": "A", "reverse": False},
    {"id": "A3", "text": "Pienso que la mayoría de la gente intenta aprovecharse de los demás.", "trait": "A", "reverse": True},
    {"id": "A4", "text": "Evito las discusiones y prefiero buscar el consenso rápidamente.", "trait": "A", "reverse": False},
    {"id": "A5", "text": "No dudo en insultar o manipular a las personas si es necesario para ganar.", "trait": "A", "reverse": True},
    {"id": "A6", "text": "Tienden a describirme como una persona amable, cálida y considerada.", "trait": "A", "reverse": False},
    {"id": "A7", "text": "Me resulta fácil perdonar a quienes me han ofendido o traicionado.", "trait": "A", "reverse": False},
    {"id": "A8", "text": "A veces manipulo a los demás para conseguir mis metas.", "trait": "A", "reverse": True},
    {"id": "A9", "text": "Me gusta ayudar activamente a quienes lo necesitan, sin esperar nada a cambio.", "trait": "A", "reverse": False},
    {"id": "A10", "text": "Soy muy directo y no me importa criticar a los demás abiertamente.", "trait": "A", "reverse": True},
    {"id": "A11", "text": "Considero esencial la armonía en mis relaciones personales.", "trait": "A", "reverse": False},
    {"id": "A12", "text": "Me resulta difícil simpatizar con la gente que se queja constantemente.", "trait": "A", "reverse": True},
    {"id": "A13", "text": "Siento un gran afecto por los animales y los niños.", "trait": "A", "reverse": False},
    {"id": "A14", "text": "No me importa hacer trampa si todos los demás lo están haciendo.", "trait": "A", "reverse": True},
    {"id": "A15", "text": "Soy conocido por ser indulgente y de mente abierta.", "trait": "A", "reverse": False},
    {"id": "A16", "text": "Creo que la ley del más fuerte es la que debe prevalecer.", "trait": "A", "reverse": True},
    {"id": "A17", "text": "Prefiero cooperar antes que competir en casi cualquier situación.", "trait": "A", "reverse": False},
    {"id": "A18", "text": "A menudo me burlo de los defectos de los demás.", "trait": "A", "reverse": True},
    {"id": "A19", "text": "Siempre asumo lo best of las personas hasta que se demuestre lo contrario.", "trait": "A", "reverse": False},
    {"id": "A20", "text": "Soy rencoroso y me cuesta olvidar cuando me han hecho daño.", "trait": "A", "reverse": True},
    {"id": "A21", "text": "Dedico tiempo a escuchar los problemas de mis amigos.", "trait": "A", "reverse": False},
    {"id": "A22", "text": "Tiendo a ser sarcástico o cínico en mis comentarios.", "trait": "A", "reverse": True},
    {"id": "A23", "text": "Me considero una persona humilde y modesta.", "trait": "A", "reverse": False},
    {"id": "A24", "text": "No siento remordimiento por mis errores pasados.", "trait": "A", "reverse": True},
    {"id": "A25", "text": "Soy muy paciente con la gente lenta o incompetente.", "trait": "A", "reverse": False},
    {"id": "A26", "text": "Me cuesta ponerme en el lugar de alguien que sufre mucho.", "trait": "A", "reverse": True},

    # N - Neuroticismo (Neuroticism) - 26 items
    {"id": "N1", "text": "Me preocupo a menudo por cosas pequeñas o insignificantes.", "trait": "N", "reverse": False},
    {"id": "N2", "text": "A veces me siento deprimido, melancólico o infeliz.", "trait": "N", "reverse": False},
    {"id": "N3", "text": "Tienden a estresarme las situaciones inesperadas o difíciles.", "trait": "N", "reverse": False},
    {"id": "N4", "text": "Soy una persona muy relajada y rara vez me siento ansioso.", "trait": "N", "reverse": True},
    {"id": "N5", "text": "Puedo mantener la calma bajo presión extrema.", "trait": "N", "reverse": True},
    {"id": "N6", "text": "Mi estado de ánimo es generalmente estable, tranquilo y predecible.", "trait": "N", "reverse": True},
    {"id": "N7", "text": "Me ofendo o me irrito con mucha facilidad por comentarios ajenos.", "trait": "N", "reverse": False},
    {"id": "N8", "text": "Me cuesta volver a la normalidad después de un disgusto o un enfado.", "trait": "N", "reverse": False},
    {"id": "N9", "text": "Soy propenso a sentir celos o envidia de los logros de otros.", "trait": "N", "reverse": False},
    {"id": "N10", "text": "Raramente me siento tenso, nervioso o asustado.", "trait": "N", "reverse": True},
    {"id": "N11", "text": "Siempre me siento seguro y optimista sobre mi futuro.", "trait": "N", "reverse": True},
    {"id": "N12", "text": "Mis emociones son a menudo volátiles e inestables.", "trait": "N", "reverse": False},
    {"id": "N13", "text": "Tengo un miedo persistente de que algo terrible va a suceder.", "trait": "N", "reverse": False},
    {"id": "N14", "text": "No me tomo las críticas personales, las veo como una oportunidad para mejorar.", "trait": "N", "reverse": True},
    {"id": "N15", "text": "Me preocupo mucho por lo que los demás piensan de mí.", "trait": "N", "reverse": False},
    {"id": "N16", "text": "Soy capaz de ignorar los pensamientos negativos y destructivos.", "trait": "N", "reverse": True},
    {"id": "N17", "text": "La presión me hace trabajar mejor y me enfoca.", "trait": "N", "reverse": True},
    {"id": "N18", "text": "A menudo me siento solo o abandonado.", "trait": "N", "reverse": False},
    {"id": "N19", "text": "Sufro de cambios de humor sin una causa obvia.", "trait": "N", "reverse": False},
    {"id": "N20", "text": "Raramente siento lástima por mí mismo.", "trait": "N", "reverse": True},
    {"id": "N21", "text": "Mi salud y estado de ánimo se ven afectados por el estrés.", "trait": "N", "reverse": False},
    {"id": "N22", "text": "Tengo una actitud de 'dejar que las cosas pasen' ante los problemas.", "trait": "N", "reverse": True},
    {"id": "N23", "text": "Soy hipersensible a los ruidos fuertes o a la luz intensa.", "trait": "N", "reverse": False},
    {"id": "N24", "text": "Me siento seguro de mi capacidad para resolver cualquier crisis.", "trait": "N", "reverse": True},
    {"id": "N25", "text": "Tiendo a ver la vida a través de un cristal de color gris.", "trait": "N", "reverse": False},
    {"id": "N26", "text": "Soy una persona que se rinde fácilmente ante la desesperación.", "trait": "N", "reverse": False},
]

# Parámetros del Test (Ajustados a 130 preguntas)
TOTAL_QUESTIONS = len(QUESTIONS) # 130 preguntas
QUESTIONS_PER_PAGE = 10
TOTAL_PAGES = (TOTAL_QUESTIONS + QUESTIONS_PER_PAGE - 1) // QUESTIONS_PER_PAGE # 13 páginas
ITEMS_PER_TRAIT = 26
MAX_SCORE_PER_TRAIT = ITEMS_PER_TRAIT * 5 # 26 * 5 = 130
MIN_SCORE_PER_TRAIT = ITEMS_PER_TRAIT * 1 # 26 * 1 = 26

# Opciones de respuesta para el Likert Scale
LIKERT_OPTIONS = {
    5: "5 - Totalmente de acuerdo",
    4: "4 - De acuerdo",
    3: "3 - Neutral",
    2: "2 - En desacuerdo",
    1: "1 - Totalmente en desacuerdo"
}
LIKERT_SCORES = list(LIKERT_OPTIONS.keys()) # [5, 4, 3, 2, 1]

# Etiquetas de los Rasgos
TRAIT_LABELS = {
    "O": "Apertura a la Experiencia (Openness)",
    "C": "Responsabilidad (Conscientiousness)",
    "E": "Extraversión (Extraversion)",
    "A": "Amabilidad (Agreeableness)",
    "N": "Neuroticismo (Neuroticism)"
}

# --- 2. LÓGICA DE PUNTUACIÓN Y PERFIL ---

def calculate_score(answers):
    """Calcula la puntuación para cada rasgo de personalidad (maneja la puntuación inversa)."""
    scores = defaultdict(int)
    
    # Crea un mapa rápido de preguntas por ID
    q_map = {q['id']: q for q in QUESTIONS}

    for q_id, response in answers.items():
        q = q_map.get(q_id)
        if not q:
            continue
            
        trait = q["trait"]
        is_reverse = q["reverse"]

        if response is not None:
            score = response

            if is_reverse:
                # La puntuación invertida es (Max Score + 1) - Score = 6 - Score
                score = 6 - score

            scores[trait] += score

    return dict(scores)

def interpret_score(score, trait):
    """
    Interpreta la puntuación (Bajo, Medio, Alto) y devuelve el texto del perfil,
    incluyendo la Fortaleza y el Desafío Clave (los aspectos "malos").
    Rango de score: 26 (min) a 130 (max).
    """
    # Umbrales ajustados para el rango 26-130
    LOW_THRESHOLD = 60
    HIGH_THRESHOLD = 96

    if score <= LOW_THRESHOLD:
        level = "Bajo"
    elif score >= HIGH_THRESHOLD:
        level = "Alto"
    else:
        level = "Medio"

    # --- Descripciones Detalladas, Fortalezas y Desafíos Clave (Cosas "malas") ---
    profiles = {
        "O": {
            "Alto": {
                "desc": "¡Eres un **Explorador Ilimitado**! Mente creativa y abierta, curiosidad insaciable por las ideas abstractas y la estética. Eres el motor de la innovación.",
                "strength": "Tu capacidad para conectar ideas dispares y tu visión no convencional te hacen un pensador excepcionalmente original y adaptable.",
                "challenge": "⚠️ **Riesgo de Falla:** Tendencia al escapismo y a la desconexión con la realidad práctica. Puedes ser visto como poco realista o inestable, iniciando proyectos sin la disciplina de finalizarlos."
            },
            "Medio": {
                "desc": "Tienes un **perfil Balanceado**. Combina la apertura al cambio con un sentido de la estabilidad. Eres adaptable y puedes interactuar con éxito en entornos creativos y pragmáticos.",
                "strength": "Posees la versatilidad para apreciar la novedad sin caer en la impulsividad, lo que te permite aprender sin rechazar lo ya conocido.",
                "challenge": "⚠️ **Riesgo de Falla:** Puedes caer en una 'zona de confort' intelectual, mostrando resistencia a invertir tiempo en ideas que percibas como innecesariamente complejas o demasiado disruptivas."
            },
            "Bajo": {
                "desc": "Eres **Pragmático y Convencional**. Prefieres la familiaridad, la tradición y los métodos probados. Tu enfoque está en los hechos concretos y la utilidad práctica, lo que te hace eficiente en tareas definidas.",
                "strength": "Tu estabilidad, tu enfoque en la realidad y tu resistencia a las modas pasajeras te hacen un pilar de fiabilidad en entornos que requieren estructura y lógica.",
                "challenge": "⚠️ **Riesgo de Falla:** Excesiva rigidez mental y aversión al cambio. Puedes ser percibido como dogmático o resistente a nuevas perspectivas, limitando tu potencial de crecimiento personal y profesional."
            }
        },
        "C": {
            "Alto": {
                "desc": "¡Eres un **Súper Organizador Meticuloso**! Muestras un alto nivel de autodisciplina, eres confiable, orientado a metas y obsesivo con los detalles. Tu ética de trabajo es ejemplar.",
                "strength": "Tu rigor, planificación y perseverancia garantizan la alta calidad de tu trabajo y te permiten alcanzar objetivos ambiciosos a largo plazo.",
                "challenge": "⚠️ **Riesgo de Falla:** Propensión al perfeccionismo paralizante y al agotamiento ('burnout'). Puedes experimentar altos niveles de estrés por el miedo a cometer errores y dificultad para delegar o improvisar."
            },
            "Medio": {
                "desc": "Eres una persona **Eficaz y Flexible**. Tienes la capacidad de organizarte y cumplir con los plazos, pero valoras la flexibilidad. Eres confiable, pero no te agobia la rigidez.",
                "strength": "Tienes un equilibrio práctico: eres lo suficientemente responsable para ser productivo, pero flexible para ajustarte a circunstancias cambiantes sin estresarte en exceso.",
                "challenge": "⚠️ **Riesgo de Falla:** Riesgo de inconsistencia. Puedes procrastinar en tareas de baja prioridad o fallar en el último detalle si no mantienes un sistema de seguimiento constante."
            },
            "Bajo": {
                "desc": "¡Eres **Espontáneo y Vives el Momento**! Priorizas la flexibilidad y la improvisación sobre el orden riguroso. Te sientes cómodo con el caos y puedes adaptarte rápidamente a los cambios.",
                "strength": "Tu adaptabilidad, creatividad bajo presión y capacidad de improvisación te permiten responder rápidamente a las crisis y aprovechar oportunidades inesperadas.",
                "challenge": "⚠️ **Riesgo de Falla:** Alta tendencia a la procrastinación crónica y a la desorganización. Tu falta de estructura puede afectar tu reputación y sabotear el logro de objetivos a largo plazo, resultando en fracasos por falta de seguimiento."
            }
        },
        "E": {
            "Alto": {
                "desc": "¡Eres la **Estrella del Escenario y Fuente de Energía**! Eres enérgico, asertivo y te revitalizas con la interacción social. Buscas activamente el contacto social y tienes una gran influencia en grupos.",
                "strength": "Tu entusiasmo es contagioso. Tu asertividad te convierte en un líder natural y tu amplia red social te abre constantemente nuevas oportunidades.",
                "challenge": "⚠️ **Riesgo de Falla:** Necesidad constante de atención, interrupción y tendencia a la **superficialidad** en las relaciones. Puedes ser percibido como dominante, ruidoso o incapaz de escuchar profundamente a los demás."
            },
            "Medio": {
                "desc": "Tienes un **perfil Ambivertido**. Disfrutas de la compañía, pero también valoras el tiempo a solas. Puedes adaptarte a roles tanto sociales como independientes, gestionando bien tus niveles de energía.",
                "strength": "Tu versatilidad te permite ser un puente entre diferentes tipos de personas y entornos, lo que te convierte en un comunicador y colaborador eficaz.",
                "challenge": "⚠️ **Riesgo de Falla:** A veces puedes confundir tus propias necesidades de energía, lo que puede llevar al agotamiento social por exceso o al arrepentimiento por haber rechazado oportunidades por introversión temporal."
            },
            "Bajo": {
                "desc": "Eres **Reservado e Introvertido**. Prefieres la soledad, las interacciones profundas y te sientes agotado por las grandes multitudes. Eres reflexivo, observador y sueles ser muy cauteloso al hablar.",
                "strength": "Tu capacidad de reflexión profunda, tu independencia y tu enfoque en la calidad de las relaciones te hacen un pensador estratégico y un amigo leal y profundo.",
                "challenge": "⚠️ **Riesgo de Falla:** Riesgo de aislamiento social excesivo o de ser invisible. Te resulta difícil defender tus ideas o ser escuchado en grupos, lo que puede estancar tu carrera o vida social."
            }
        },
        "A": {
            "Alto": {
                "desc": "¡Eres el **Agente de la Armonía**! Eres empático, de buen corazón y buscas activamente la cooperación. Eres el mediador natural, impulsado por el deseo de ayudar y evitar el conflicto a toda costa.",
                "strength": "Tu empatía, generosidad y capacidad de colaboración construyen relaciones sólidas y de confianza, creando un entorno pacífico y de apoyo mutuo.",
                "challenge": "⚠️ **Riesgo de Falla:** Evitar conflictos a toda costa, lo que lleva a la **sumisión**, a ser manipulado o a la dificultad para decir 'no'. Corres el riesgo de descuidar tus propias necesidades y sentirte resentido."
            },
            "Medio": {
                "desc": "Eres **Amable, Justo y Pragmático**. Eres generalmente agradable y cooperativo, but mantienes un saludable escepticismo y puedes defender tus propios intereses cuando es necesario.",
                "strength": "Eres un colaborador valioso que equilibra la justicia con la calidez, ofreciendo ayuda, pero esperando reciprocidad y manteniendo la dignidad personal.",
                "challenge": "⚠️ **Riesgo de Falla:** Puedes dudar al tomar una postura moral o crítica para no ofender a nadie. Esto te hace parecer inconsistente en situaciones que exigen un liderazgo firme y polarizado."
            },
            "Bajo": {
                "desc": "Eres **Desafiante y Escéptico**. Tiendes a ser competitivo, directo, y priorizas la verdad y tus intereses sobre la sensibilidad ajena. Eres excelente para negociar.",
                "strength": "Tu capacidad para la franqueza brutal, tu resistencia a la manipulación y tu enfoque en la competencia te hacen altamente efectivo en entornos de negociación y alta presión.",
                "challenge": "⚠️ **Riesgo de Falla:** Frecuente **hostilidad** y dificultad para confiar. Los demás te ven como insensible, frío o conflictivo, dificultando la construcción de alianzas a largo plazo y la lealtad de equipo."
            }
        },
        "N": {
            "Alto": {
                "desc": "Tu **Estabilidad Emocional es Baja (Reactiva)**. Eres muy sensible al estrés y experimentas ansiedad, preocupación e ira con facilidad. Tu estado de ánimo es a menudo volátil.",
                "strength": "Tu alta sensibilidad te permite experimentar las emociones y el arte profundamente. Tu capacidad de sentir la alarma rápidamente puede protegerte de riesgos inminentes.",
                "challenge": "⚠️ **Riesgo de Falla:** **Ansiedad crónica** y altos niveles de estrés que paralizan la acción. Tu inestabilidad dificulta la toma de decisiones objetivas y puede dañar tu salud y relaciones interpersonales."
            },
            "Medio": {
                "desc": "Tienes una **Estabilidad Emocional Moderada (Sensible)**. Eres capaz de gestionar el estrés diario, pero puedes volverte ansioso o preocupado bajo presión intensa. Eres empático, pero mantienes el control la mayoría del tiempo.",
                "strength": "Tu sensibilidad moderada te permite ser consciente de los riesgos sin ser abrumado por ellos, manteniendo la prudencia sin caer en el pánico.",
                "challenge": "⚠️ **Riesgo de Falla:** Tiendes a la rumiación mental y a la preocupación excesiva por el futuro. Puedes caer en la sobrecarga de trabajo al intentar controlar todas las variables externas."
            },
            "Bajo": {
                "desc": "¡Eres **Zen y Súper Resiliente**! Eres tranquilo, estable y rara vez te sientes perturbado. Muestras una gran capacidad para manejar el estrés y recuperarte rápidamente de los contratiempos.",
                "strength": "Tu calma, tu resiliencia y tu optimismo natural te permiten afrontar crisis y contratiempos con una cabeza fría, siendo un faro de estabilidad para los demás.",
                "challenge": "⚠️ **Riesgo de Falla:** Puedes parecer **indiferente o desinteresado** en los problemas emocionales ajenos. Corres el riesgo de subestimar peligros o de no prepararte adecuadamente para desastres por exceso de confianza."
            }
        }
    }

    # Determinación de color y nivel de estabilidad
    if trait == 'N':
        if level == "Bajo":
            color_hex = LEVEL_COLORS["Estable"]
            color_label = "Muy Estable (Bajo Neuroticismo)"
        elif level == "Alto":
            color_hex = LEVEL_COLORS["Bajo_Negativo"]
            color_label = "Inestable (Alto Neuroticismo)"
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

    # Retorna un diccionario estructurado
    return {
        "level": level,
        "color_hex": color_hex,
        "color_label": color_label,
        "Descripcion": profiles[trait][level]["desc"],
        "Fortaleza": profiles[trait][level]["strength"],
        "Desafio": profiles[trait][level]["challenge"]
    }

# --- 3. FUNCIONES DE NAVEGACIÓN Y REINICIO ---

def scroll_to_top():
    """
    Inyecta JavaScript con un retraso y múltiples métodos para forzar el scroll
    de la ventana al inicio (0, 0), contrarrestando la memoria de scroll.
    """
    st.markdown(
        """
        <script>
        setTimeout(() => {
            window.scrollTo(0, 0);
            document.body.scrollTop = 0;
            document.documentElement.scrollTop = 0;
        }, 200);
        </script>
        """,
        unsafe_allow_html=True
    )

def next_page():
    """Avanza a la siguiente página del test."""
    
    start_index = st.session_state.current_page * QUESTIONS_PER_PAGE
    end_index = min(start_index + QUESTIONS_PER_PAGE, TOTAL_QUESTIONS)
    
    # Validación: Asegurarse de que todas las preguntas en la página actual estén respondidas
    missing_answers = []
    for i in range(start_index, end_index):
        q_id = QUESTIONS[i]["id"]
        if st.session_state.answers.get(q_id) is None:
            missing_answers.append(q_id)

    if missing_answers:
        st.session_state.error_message = f"¡ERROR! Debes responder todas las {len(missing_answers)} preguntas restantes en esta página antes de continuar."
    else:
        if st.session_state.current_page < TOTAL_PAGES - 1:
            st.session_state.current_page += 1
            st.session_state.error_message = ""
            scroll_to_top()
        elif st.session_state.current_page == TOTAL_PAGES - 1:
            # Si es la última página, procede a la finalización
            st.session_state.test_completed = True
            st.session_state.error_message = ""
            scroll_to_top()

def prev_page():
    """Retrocede a la página anterior del test."""
    if st.session_state.current_page > 0:
        st.session_state.current_page -= 1
        st.session_state.error_message = ""
        scroll_to_top()

def restart_test():
    """Resets the session state to restart the test."""
    st.session_state.answers = {}
    st.session_state.test_completed = False
    st.session_state.current_page = 0
    st.session_state.error_message = ""
    st.session_state.name = ""
    st.session_state.email = ""
    scroll_to_top()

# --- 4. FUNCIONES DE DISPLAY UI ---

def display_start_page():
    """Muestra la página de inicio y las instrucciones."""
    st.title("Test Big Five (OCEAN) Detallado")
    st.markdown("## Mapeo de Personalidad de 130 Items")

    with st.container():
        st.markdown(
            f"""
            <div class='stContainer'>
                <h3 style='color: {COLOR_MINT_GREEN};'>🚀 Instrucciones de Evaluación</h3>
                <p>Este cuestionario se compone de **{TOTAL_QUESTIONS} declaraciones** (26 por rasgo) y está dividido en {TOTAL_PAGES} páginas para una experiencia fluida.</p>
                <p>Responde a cada afirmación seleccionando la opción que mejor describa cómo te percibes a ti mismo, utilizando la siguiente escala de 1 a 5:</p>
                <ul>
                    <li style='color: {COLOR_VIBRANT_BLUE};'>**5** - Totalmente de acuerdo</li>
                    <li style='color: #c9d1d9;'>**3** - Neutral</li>
                    <li style='color: {COLOR_DANGER_RED};'>**1** - Totalmente en desacuerdo</li>
                </ul>
                <p>El test está diseñado para revelar tus **Fortalezas Clave** y tus **Desafíos Críticos** (puntos de riesgo o fracaso potencial).</p>
            </div>
            """, unsafe_allow_html=True
        )

    st.markdown("### 📝 Datos de Participante (Opcional)")
    col_name, col_email = st.columns(2)
    with col_name:
        st.session_state.name = st.text_input("Tu Nombre", value=st.session_state.get('name', ''), key="input_name")
    with col_email:
        st.session_state.email = st.text_input("Tu Correo Electrónico (Para fines de guardado)", value=st.session_state.get('email', ''), key="input_email")

    st.markdown("---")
    col_start, col_placeholder = st.columns([1, 4])
    with col_start:
        if st.button("Comenzar Evaluación ⚡", key="start_test_btn", use_container_width=True):
            st.session_state.current_page = 1
            scroll_to_top()
            st.rerun()

def display_test_page(page_num):
    """Muestra una página específica del test."""
    st.title(f"Página {page_num + 1} de {TOTAL_PAGES} | Big Five Test")

    start_index = page_num * QUESTIONS_PER_PAGE
    end_index = min(start_index + QUESTIONS_PER_PAGE, TOTAL_QUESTIONS)
    
    progress_percent = (start_index / TOTAL_QUESTIONS)
    st.progress(progress_percent, text=f"Progreso: {start_index} de {TOTAL_QUESTIONS} preguntas completadas")

    # Muestra el mensaje de error si existe
    if st.session_state.error_message:
        st.error(st.session_state.error_message)

    with st.form(key=f'page_form_{page_num}'):
        for i in range(start_index, end_index):
            q_data = QUESTIONS[i]
            q_id = q_data["id"]
            
            # Obtener el valor actual de la respuesta, o 3 (Neutral) si es la primera vez
            default_value = st.session_state.answers.get(q_id, 3) 

            # Crear el slider
            # El format_func muestra la descripción del Likert en lugar del número
            response = st.slider(
                label=f"**{i+1}.** {q_data['text']}",
                min_value=1,
                max_value=5,
                value=default_value,
                step=1,
                key=f"slider_{q_id}",
                format_func=lambda x: LIKERT_OPTIONS[x],
                help=f"Rasgo: {TRAIT_LABELS[q_data['trait']]} ({'Inversa' if q_data['reverse'] else 'Directa'})"
            )
            # Guardar la respuesta en el estado de la sesión
            st.session_state.answers[q_id] = response
            
        st.markdown("---")
        
        # Botones de navegación
        col_prev, col_next, col_progress_placeholder = st.columns([1, 1, 3])
        
        with col_prev:
            if page_num > 0:
                st.form_submit_button("◀️ Atrás", on_click=prev_page, use_container_width=True)
            else:
                 st.form_submit_button("Inicio", on_click=restart_test, use_container_width=True)

        with col_next:
            if page_num < TOTAL_PAGES - 1:
                st.form_submit_button("Siguiente ▶️", on_click=next_page, use_container_width=True)
            else:
                if st.form_submit_button("FINALIZAR TEST ✅", on_click=next_page, type="primary", use_container_width=True):
                    # La función next_page manejará la validación y el cambio a la página de resultados
                    pass


def display_results_page(scores):
    """Muestra los resultados finales, el gráfico de radar y las interpretaciones detalladas."""
    st.balloons()
    st.title(f"🎉 Resultados del Perfil de Personalidad Big Five")
    if st.session_state.name:
        st.header(f"Perfil para: {st.session_state.name}")
        
    # Calcular interpretaciones para el Dataframe y Radar
    interpretations = {}
    trait_names = []
    trait_scores = []
    trait_levels = []
    
    for trait_code, score in scores.items():
        interpretation = interpret_score(score, trait_code)
        interpretations[trait_code] = interpretation
        
        # Data para el Radar Chart
        trait_names.append(TRAIT_LABELS[trait_code].split(' ')[0]) # Solo la palabra principal
        trait_scores.append(score)
        
        # Data para la tabla de resumen
        trait_levels.append({
            "Rasgo": TRAIT_LABELS[trait_code],
            "Puntuación": score,
            "Nivel": f"{interpretation['color_label']} ({interpretation['level']})",
            "Color": interpretation['color_hex'],
            "Descripcion": interpretation['Descripcion'],
            "Fortaleza": interpretation['Fortaleza'],
            "Desafio": interpretation['Desafio']
        })

    # Crear el DataFrame para visualización tabular
    df_results = pd.DataFrame(trait_levels)
    
    # --- GRÁFICO DE RADAR PLOTLY ---
    fig = go.Figure(
        data=[
            go.Scatterpolar(
                r=trait_scores + [trait_scores[0]], 
                theta=trait_names + [trait_names[0]], 
                fill='toself',
                name='Puntuación',
                fillcolor='rgba(74, 144, 226, 0.4)',  
                line_color=COLOR_VIBRANT_BLUE
            )
        ],
        layout=go.Layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[MIN_SCORE_PER_TRAIT, MAX_SCORE_PER_TRAIT], # Rango 26 a 130
                    tickvals=np.arange(MIN_SCORE_PER_TRAIT, MAX_SCORE_PER_TRAIT + 1, 25),
                    gridcolor='rgba(200, 200, 200, 0.2)'
                ),
                angularaxis=dict(
                    linecolor='rgba(255, 255, 255, 0.5)'
                )
            ),
            # Diseño oscuro y profesional
            template='plotly_dark',
            title=dict(text='Distribución de Rasgos Big Five', font=dict(size=24, color='#ffffff')),
            showlegend=False,
            height=600,
            paper_bgcolor='rgba(13, 17, 23, 1)', # Fondo de la app
            plot_bgcolor='rgba(22, 27, 34, 1)' # Fondo de la tarjeta
        )
    )

    col_graph, col_summary = st.columns([3, 2])

    with col_graph:
        st.subheader("Mapa Visual de tu Personalidad")
        st.plotly_chart(fig, use_container_width=True)

    with col_summary:
        st.subheader("Resumen General de Puntuaciones")
        # Mostrar las métricas principales
        for index, row in df_results.iterrows():
            st.markdown(
                f"""
                <div style='background-color: #1e242f; border-left: 5px solid {row['Color']}; padding: 10px; border-radius: 5px; margin-bottom: 8px;'>
                    <h4 style='color: {row['Color']}; margin: 0; font-size: 1.1em;'>{row['Rasgo']}</h4>
                    <p style='margin: 0;'>Puntuación: **{row['Puntuación']}** de 130 | Nivel: **{row['Nivel']}**</p>
                </div>
                """, unsafe_allow_html=True
            )

    st.markdown("---")
    st.subheader("Interpretación Detallada: Fortalezas y Desafíos")

    # Mostrar la interpretación detallada con fortalezas y desafíos
    for index, row in df_results.iterrows():
        st.markdown(f"### {row['Rasgo']} - Nivel: {row['Nivel']}")
        
        col_desc, col_res = st.columns([1, 1])
        
        with col_desc:
            st.markdown(
                f"""
                <div class='profile-card' style='border-left: 5px solid {row['Color']};'>
                    <p style='color: {row['Color']}; font-weight: bold;'>{row['Descripcion']}</p>
                </div>
                """, unsafe_allow_html=True)
            
        with col_res:
            st.markdown(f"**💪 Fortaleza Clave:** <span class='profile-strength'>{row['Fortaleza']}</span>", unsafe_allow_html=True)
            st.markdown(f"**🚨 Desafío Crítico (Riesgo de Falla):** <span class='profile-challenge'>{row['Desafio']}</span>", unsafe_allow_html=True)
            st.markdown("---")

    # Botón de reinicio
    st.markdown("---")
    st.button("Volver a Empezar Test", on_click=restart_test, type="secondary", use_container_width=True)


# --- 5. LÓGICA PRINCIPAL DE LA APLICACIÓN ---

def main_app():
    """Maneja el flujo de navegación de la aplicación."""
    
    # Inicialización del estado de la sesión
    if 'current_page' not in st.session_state:
        st.session_state.current_page = 0
    if 'answers' not in st.session_state:
        st.session_state.answers = {}
    if 'test_completed' not in st.session_state:
        st.session_state.test_completed = False
    if 'error_message' not in st.session_state:
        st.session_state.error_message = ""
    if 'name' not in st.session_state:
        st.session_state.name = ""
    if 'email' not in st.session_state:
        st.session_state.email = ""

    current_page = st.session_state.current_page
    test_completed = st.session_state.test_completed
    
    if current_page == 0:
        # Página de inicio
        display_start_page()
    elif not test_completed and 1 <= current_page <= TOTAL_PAGES:
        # Páginas del test
        display_test_page(current_page - 1)
    elif test_completed:
        # Resultados
        scores = calculate_score(st.session_state.answers)
        display_results_page(scores)

# Ejecución de la aplicación
if __name__ == '__main__':
    main_app()
