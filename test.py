import streamlit as st
from collections import defaultdict
import time 

# --- CONFIGURACIÓN DE PÁGINA PARA RESPONSIVIDAD ---
# Usamos el layout "wide" para aprovechar el espacio en escritorio.
st.set_page_config(layout="wide", page_title="Test Big Five Detallado", initial_sidebar_state="expanded")

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
    {"id": "A19", "text": "Siempre asumo lo mejor de las personas hasta que se demuestre lo contrario.", "trait": "A", "reverse": False},
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
    5: "Totalmente de acuerdo",
    4: "De acuerdo",
    3: "Neutral",
    2: "En desacuerdo",
    1: "Totalmente en desacuerdo"
}

# Etiquetas y Colores
TRAIT_LABELS = {
    "O": "Apertura a la Experiencia (Openness)",
    "C": "Responsabilidad (Conscientiousness)",
    "E": "Extraversión (Extraversion)",
    "A": "Amabilidad (Agreeableness)",
    "N": "Neuroticismo (Neuroticism)"
}

COLOR_VIBRANT_BLUE = "#4A90E2"
COLOR_MINT_GREEN = "#50E3C2"
COLOR_WARNING_ORANGE = "#F5A623"
COLOR_DANGER_RED = "#D0021B"

LEVEL_COLORS = {
    "Alto_Positivo": COLOR_VIBRANT_BLUE,
    "Bajo_Negativo": COLOR_DANGER_RED,
    "Medio": COLOR_WARNING_ORANGE,
    "Estable": COLOR_MINT_GREEN
}

# --- 2. LÓGICA DE PUNTUACIÓN Y PERFIL ---

def calculate_score(answers):
    """Calcula la puntuación para cada rasgo de personalidad."""
    scores = defaultdict(int)
    
    for q in QUESTIONS:
        q_id = q["id"]
        trait = q["trait"]
        is_reverse = q["reverse"]
        
        # Obtenemos la respuesta directamente del estado de sesión
        response = answers.get(q_id)
        
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
    incluyendo la Fortaleza y el Desafío Clave.
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
        
    # --- Descripciones Detalladas, Fortalezas y Desafíos Clave ---
    profiles = {
        "O": {
            "Alto": {
                "desc": "¡Eres un **Explorador Ilimitado**! Mente creativa y abierta, curiosidad insaciable por las ideas abstractas y la estética. Eres el motor de la innovación.",
                "strength": "Tu capacidad para conectar ideas dispares y tu visión no convencional te hacen un pensador excepcionalmente original y adaptable.",
                "challenge": "⚠️ **Desafío Clave (Riesgo de Falla):** Tendencia al escapismo y a la desconexión con la realidad práctica. Puedes ser visto como poco realista o inestable, iniciando proyectos sin la disciplina de finalizarlos."
            },
            "Medio": {
                "desc": "Tienes un **perfil Balanceado**. Combina la apertura al cambio con un sentido de la estabilidad. Eres adaptable y puedes interactuar con éxito en entornos creativos y pragmáticos.",
                "strength": "Posees la versatilidad para apreciar la novedad sin caer en la impulsividad, lo que te permite aprender sin rechazar lo ya conocido.",
                "challenge": "⚠️ **Desafío Clave (Riesgo de Falla):** Puedes caer en una 'zona de confort' intelectual, mostrando resistencia a invertir tiempo en ideas que percibas como innecesariamente complejas o demasiado disruptivas."
            },
            "Bajo": {
                "desc": "Eres **Pragmático y Convencional**. Prefieres la familiaridad, la tradición y los métodos probados. Tu enfoque está en los hechos concretos y la utilidad práctica, lo que te hace eficiente en tareas definidas.",
                "strength": "Tu estabilidad, tu enfoque en la realidad y tu resistencia a las modas pasajeras te hacen un pilar de fiabilidad en entornos que requieren estructura y lógica.",
                "challenge": "⚠️ **Desafío Clave (Riesgo de Falla):** Excesiva rigidez mental y aversión al cambio. Puedes ser percibido como dogmático o resistente a nuevas perspectivas, limitando tu potencial de crecimiento personal y profesional."
            }
        },
        "C": {
            "Alto": {
                "desc": "¡Eres un **Súper Organizador Meticuloso**! Muestras un alto nivel de autodisciplina, eres confiable, orientado a metas y obsesivo con los detalles. Tu ética de trabajo es ejemplar.",
                "strength": "Tu rigor, planificación y perseverancia garantizan la alta calidad de tu trabajo y te permiten alcanzar objetivos ambiciosos a largo plazo.",
                "challenge": "⚠️ **Desafío Clave (Riesgo de Falla):** Propensión al perfeccionismo paralizante y al agotamiento ('burnout'). Puedes experimentar altos niveles de estrés por el miedo a cometer errores y dificultad para delegar o improvisar."
            },
            "Medio": {
                "desc": "Eres una persona **Eficaz y Flexible**. Tienes la capacidad de organizarte y cumplir con los plazos, pero valoras la flexibilidad. Eres confiable, pero no te agobia la rigidez.",
                "strength": "Tienes un equilibrio práctico: eres lo suficientemente responsable para ser productivo, pero flexible para ajustarte a circunstancias cambiantes sin estresarte en exceso.",
                "challenge": "⚠️ **Desafío Clave (Riesgo de Falla):** Riesgo de inconsistencia. Puedes procrastinar en tareas de baja prioridad o fallar en el último detalle si no mantienes un sistema de seguimiento constante."
            },
            "Bajo": {
                "desc": "¡Eres **Espontáneo y Vives el Momento**! Priorizas la flexibilidad y la improvisación sobre el orden riguroso. Te sientes cómodo con el caos y puedes adaptarte rápidamente a los cambios.",
                "strength": "Tu adaptabilidad, creatividad bajo presión y capacidad de improvisación te permiten responder rápidamente a las crisis y aprovechar oportunidades inesperadas.",
                "challenge": "⚠️ **Desafío Clave (Riesgo de Falla):** Alta tendencia a la procrastinación crónica y a la desorganización. Tu falta de estructura puede afectar tu reputación y sabotear el logro de objetivos a largo plazo, resultando en fracasos por falta de seguimiento."
            }
        },
        "E": {
            "Alto": {
                "desc": "¡Eres la **Estrella del Escenario y Fuente de Energía**! Eres enérgico, asertivo y te revitalizas con la interacción social. Buscas activamente el contacto social y tienes una gran influencia en grupos.",
                "strength": "Tu entusiasmo es contagioso. Tu asertividad te convierte en un líder natural y tu amplia red social te abre constantemente nuevas oportunidades.",
                "challenge": "⚠️ **Desafío Clave (Riesgo de Falla):** Necesidad constante de atención, interrupción y tendencia a la **superficialidad** en las relaciones. Puedes ser percibido como dominante, ruidoso o incapaz de escuchar profundamente a los demás."
            },
            "Medio": {
                "desc": "Tienes un **perfil Ambivertido**. Disfrutas de la compañía, pero también valoras el tiempo a solas. Puedes adaptarte a roles tanto sociales como independientes, gestionando bien tus niveles de energía.",
                "strength": "Tu versatilidad te permite ser un puente entre diferentes tipos de personas y entornos, lo que te convierte en un comunicador y colaborador eficaz.",
                "challenge": "⚠️ **Desafío Clave (Riesgo de Falla):** A veces puedes confundir tus propias necesidades de energía, lo que puede llevar al agotamiento social por exceso o al arrepentimiento por haber rechazado oportunidades por introversión temporal."
            },
            "Bajo": {
                "desc": "Eres **Reservado e Introvertido**. Prefieres la soledad, las interacciones profundas y te sientes agotado por las grandes multitudes. Eres reflexivo, observador y sueles ser muy cauteloso al hablar.",
                "strength": "Tu capacidad de reflexión profunda, tu independencia y tu enfoque en la calidad de las relaciones te hacen un pensador estratégico y un amigo leal y profundo.",
                "challenge": "⚠️ **Desafío Clave (Riesgo de Falla):** Riesgo de aislamiento social excesivo o de ser invisible. Te resulta difícil defender tus ideas o ser escuchado en grupos, lo que puede estancar tu carrera o vida social."
            }
        },
        "A": {
            "Alto": {
                "desc": "¡Eres el **Agente de la Armonía**! Eres empático, de buen corazón y buscas activamente la cooperación. Eres el mediador natural, impulsado por el deseo de ayudar y evitar el conflicto a toda costa.",
                "strength": "Tu empatía, generosidad y capacidad de colaboración construyen relaciones sólidas y de confianza, creando un entorno pacífico y de apoyo mutuo.",
                "challenge": "⚠️ **Desafío Clave (Riesgo de Falla):** Evitar conflictos a toda costa, lo que lleva a la **sumisión**, a ser manipulado o a la dificultad para decir 'no'. Corres el riesgo de descuidar tus propias necesidades y sentirte resentido."
            },
            "Medio": {
                "desc": "Eres **Amable, Justo y Pragmático**. Eres generalmente agradable y cooperativo, pero mantienes un saludable escepticismo y puedes defender tus propios intereses cuando es necesario.",
                "strength": "Eres un colaborador valioso que equilibra la justicia con la calidez, ofreciendo ayuda, pero esperando reciprocidad y manteniendo la dignidad personal.",
                "challenge": "⚠️ **Desafío Clave (Riesgo de Falla):** Puedes dudar al tomar una postura moral o crítica para no ofender a nadie. Esto te hace parecer inconsistente en situaciones que exigen un liderazgo firme y polarizado."
            },
            "Bajo": {
                "desc": "Eres **Desafiante y Escepticismo**. Tiendes a ser competitivo, directo, y priorizas la verdad y tus intereses sobre la sensibilidad ajena. Eres excelente para negociar.",
                "strength": "Tu capacidad para la franqueza brutal, tu resistencia a la manipulación y tu enfoque en la competencia te hacen altamente efectivo en entornos de negociación y alta presión.",
                "challenge": "⚠️ **Desafío Clave (Riesgo de Falla):** Frecuente **hostilidad** y dificultad para confiar. Los demás te ven como insensible, frío o conflictivo, dificultando la construcción de alianzas a largo plazo y la lealtad de equipo."
            }
        },
        "N": {
            "Alto": {
                "desc": "Tu **Estabilidad Emocional es Baja (Reactiva)**. Eres muy sensible al estrés y experimentas ansiedad, preocupación e ira con facilidad. Tu estado de ánimo es a menudo volátil.",
                "strength": "Tu alta sensibilidad te permite experimentar las emociones y el arte profundamente. Tu capacidad de sentir la alarma rápidamente puede protegerte de riesgos inminentes.",
                "challenge": "⚠️ **Desafío Clave (Riesgo de Falla):** **Ansiedad crónica** y altos niveles de estrés que paralizan la acción. Tu inestabilidad dificulta la toma de decisiones objetivas y puede dañar tu salud y relaciones interpersonales."
            },
            "Medio": {
                "desc": "Tienes una **Estabilidad Emocional Moderada (Sensible)**. Eres capaz de gestionar el estrés diario, pero puedes volverte ansioso o preocupado bajo presión intensa. Eres empático, pero mantienes el control la mayoría del tiempo.",
                "strength": "Tu sensibilidad moderada te permite ser consciente de los riesgos sin ser abrumado por ellos, manteniendo la prudencia sin caer en el pánico.",
                "challenge": "⚠️ **Desafío Clave (Riesgo de Falla):** Tiendes a la rumiación mental y a la preocupación excesiva por el futuro. Puedes caer en la sobrecarga de trabajo al intentar controlar todas las variables externas."
            },
            "Bajo": {
                "desc": "¡Eres **Zen y Súper Resiliente**! Eres tranquilo, estable y rara vez te sientes perturbado. Muestras una gran capacidad para manejar el estrés y recuperarte rápidamente de los contratiempos.",
                "strength": "Tu calma, tu resiliencia y tu optimismo natural te permiten afrontar crisis y contratiempos con una cabeza fría, siendo un faro de estabilidad para los demás.",
                "challenge": "⚠️ **Desafío Clave (Riesgo de Falla):** Puedes parecer **indiferente o desinteresado** en los problemas emocionales ajenos. Corres el riesgo de subestimar peligros o de no prepararte adecuadamente para desastres por exceso de confianza."
            }
        }
    }
    
    # Determinación de color y nivel de estabilidad
    if trait_code == 'N':
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
        "description": profiles[trait_code][level]["desc"],
        "strength": profiles[trait_code][level]["strength"],
        "challenge": profiles[trait_code][level]["challenge"]
    }

# --- 3. FUNCIONES DE NAVEGACIÓN Y REINICIO ---

def scroll_to_top():
    """
    [SOLUCIÓN DE SCROLL FORZADO]
    Fuerza el scroll a la parte superior (0, 0) utilizando un 'instant' behavior 
    dentro de un setTimeout(0) para garantizar que se ejecute después del re-render.
    """
    st.markdown(
        """
        <script>
        setTimeout(function() {
            // 1. Scroll forzado INSTANTÁNEO en la ventana
            window.scrollTo({ top: 0, behavior: 'instant' }); 
            
            // 2. Fallbacks de compatibilidad en elementos root del documento
            document.body.scrollTop = 0; 
            document.documentElement.scrollTop = 0;
            
            // 3. Selector Streamlit-específico (el contenedor principal de la aplicación)
            const mainContent = document.querySelector('[data-testid="stAppViewBlock"]');
            if (mainContent) {
                mainContent.scrollTop = 0;
            }
            
        }, 0); 
        </script>
        """,
        unsafe_allow_html=True
    )

def restart_test():
    """Resets the session state to restart the test."""
    st.session_state.answers = {}
    st.session_state.test_completed = False
    st.session_state.current_page = 0
    st.session_state.error_message = ""
    # El scroll se forzará al final de run_test
    st.rerun()

def handle_navigation(action):
    """Maneja la validación de página y la navegación (Siguiente/Anterior/Finalizar)."""
    current_page = st.session_state.current_page
    start_index = current_page * QUESTIONS_PER_PAGE
    end_index = min(start_index + QUESTIONS_PER_PAGE, TOTAL_QUESTIONS)
    current_questions = QUESTIONS[start_index:end_index]
    
    # 1. Validar respuestas para avanzar o finalizar
    if action == "next" or action == "finish":
        # Contamos cuántas preguntas de la página actual tienen una respuesta válida
        answered_on_current_page = 0
        for q in current_questions:
            if q["id"] in st.session_state.answers and st.session_state.answers[q["id"]] is not None:
                answered_on_current_page += 1
        
        questions_on_page_count = len(current_questions)
        
        if answered_on_current_page < questions_on_page_count:
            # Falla la validación
            st.session_state.error_message = f"⚠️ ¡Alto! Responde las {questions_on_page_count - answered_on_current_page} preguntas de la página actual antes de continuar."
            # NO se llama a rerun(), para que se muestre el error y se quede en la misma página.
            return 
        else:
            # Pasa la validación
            st.session_state.error_message = ""
            
    # 2. Lógica de Navegación
    if action == "prev" and current_page > 0:
        st.session_state.current_page -= 1
        st.rerun()
        
    elif action == "next" and current_page < TOTAL_PAGES - 1:
        st.session_state.current_page += 1
        st.rerun()
        
    elif action == "finish":
        # Finalizar el test
        if len(st.session_state.answers) == TOTAL_QUESTIONS:
            st.session_state.test_completed = True
            st.rerun()
        else:
            # Error de conteo total
            st.session_state.error_message = "Error: Aún faltan respuestas totales para completar el test. Por favor, revisa."
            return

# --- 4. CONFIGURACIÓN VISUAL Y DE INTERFAZ (CSS) ---

def set_playful_style():
    """Aplica estilos CSS divertidos, dinámicos y de impresión."""
    
    V_BLUE = "#4A90E2"
    M_GREEN = "#50E3C2"
    D_RED = "#D0021B"
    
    # --- CSS Styles ---
    st.markdown(f"""
    <style>
        /* Deshabilita la animación de rebote en los encabezados si no se usa */
        @keyframes bounce {{ 0% {{transform: none;}} }} 
        .bouncing-header {{ display: inline-block; }}

        /* Fuente y Estilo General */
        @import url('https://fonts.googleapis.com/css2?family=Varela+Round&display=swap');
        html, body, [class*="st-"] {{
            font-family: 'Varela Round', sans-serif;
        }}
        
        /* Contenedor Principal y Fondo */
        .main {{
            background: linear-gradient(135deg, #F9F9FB 0%, #E0F7FA 100%); 
            border-radius: 18px;
            padding: 25px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
        }}
        
        /* Títulos y Encabezados */
        h1 {{
            color: {V_BLUE}; 
            border-bottom: 3px solid {M_GREEN};
            padding-bottom: 0.5rem;
            margin-bottom: 1.5rem;
            font-weight: 700;
        }}
        h2 {{
            color: {V_BLUE};
            font-weight: 600;
            margin-top: 2rem;
            text-shadow: 1px 1px 2px rgba(0,0,0,0.1);
        }}

        /* Preguntas (Cambiado: Sin Card Box alrededor del texto, solo en radio) */
        .stRadio label {{
            font-size: 1.05rem;
            font-weight: 500;
            color: #1f2937;
            padding: 15px 0 15px 0;
            display: block;
        }}
        
        /* Opciones de Radio Button - Flexbox y Responsive */
        .stRadio div[role="radiogroup"] {{
            display: flex;
            flex-direction: row; 
            gap: 8px;
            padding-bottom: 20px;
            border-bottom: 1px solid #E5E7EB;
            margin-bottom: 25px;
            flex-wrap: wrap; /* Asegura que las opciones se envuelvan en móvil */
        }}
        .stRadio div[role="radiogroup"] > label {{
            font-size: 0.85rem !important;
            border: 1px solid #CCC !important;
            padding: 8px 10px !important;
            border-radius: 20px !important;
            cursor: pointer;
            transition: all 0.3s ease;
            background-color: #F9F9F9;
            flex-grow: 1;
            text-align: center;
            border-left: none !important; 
            box-shadow: none !important;
            min-width: 120px; /* Asegura un buen tamaño para el dedo en móvil */
        }}
        /* Destacar la opción seleccionada */
        .stRadio div[role="radiogroup"] input:checked + div + div > label {{
            background-color: {V_BLUE} !important;
            color: white !important;
            border-color: {V_BLUE} !important;
            font-weight: 600;
            transform: scale(1.05);
        }}

        /* Contenedor de Resultados */
        .profile-container {{
            background-color: #ffffff;
            border: 1px solid #E5E7EB;
            border-radius: 15px;
            padding: 30px;
            margin-top: 30px;
            box-shadow: 0 10px 20px rgba(0, 0, 0, 0.08);
            border-top: 5px solid {M_GREEN};
        }}
        .trait-header h3 {{
            color: {V_BLUE};
            border-bottom: 2px dashed #EEE;
            padding-bottom: 10px;
        }}
        
        /* Estilo para Desafío Clave (Lo "malo") */
        .challenge-box {{
            background-color: #FFEFEF; /* Fondo rojo suave */
            border-left: 5px solid {D_RED};
            padding: 15px;
            border-radius: 8px;
            margin-top: 15px;
            font-size: 0.95rem;
        }}
        .challenge-box b {{
            color: {D_RED};
        }}
        
        /* Botones y Sidebar */
        .stButton>button {{
            font-weight: 600;
            padding: 10px 10px;
            border-radius: 12px;
            border: none;
            transition: all 0.3s;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.15);
            width: 100%; /* Ocupa todo el ancho en el sidebar */
            margin-bottom: 10px;
        }}
        
        /* Botones Primarios (Finalizar / Siguiente) */
        .stButton>button[kind="primary"] {{
            background-color: {M_GREEN} !important; 
            color: #1F2937 !important;
        }}
        /* Botón de Anterior */
        .stButton>button[kind="secondary"] {{
            background-color: #EFEFEF !important;
            color: #4A90E2 !important;
            border: 1px solid #4A90E2;
        }}
        
        /* Sidebar Navigation Grouping */
        .sidebar .stButton {{
            margin-bottom: 10px; 
        }}
        
        /* Estilo del Header del Sidebar */
        .sidebar h2 {{
            color: {V_BLUE};
            font-size: 1.5rem;
            margin-bottom: 10px;
            border-bottom: 2px solid {M_GREEN};
            padding-bottom: 5px;
        }}

        /* Botón de Imprimir/PDF (Acción Final) */
        .print-button-container button {{
            background-color: {V_BLUE} !important; 
            color: white !important;
            font-weight: 600;
            padding: 12px 20px;
            border-radius: 12px;
            border: none;
            transition: background-color 0.3s;
            box-shadow: 0 4px 6px rgba(74, 144, 226, 0.5);
            cursor: pointer;
            width: 100%;
        }}
        
        /* === Media Query para Impresión (Limpieza profesional del PDF) === */
        @media print {{
            /* Ocultar UI de Streamlit */
            .stSidebar, .stButton, .stProgress:not(.results-progress), 
            .stAlert:not(.result-alert), .css-fg4pbf, .stMetric [data-testid="stMetricDelta"],
            .st-emotion-cache-1cypcdb
            {{
                display: none !important;
            }}
            /* Forzar visualización de Títulos y Resultados */
            .main {{
                background: white !important;
                padding: 10px !important;
                border: none !important;
                box-shadow: none !important;
            }}
        }}

    </style>
    """, unsafe_allow_html=True)
    
# --- 5. FLUJO DE LA APLICACIÓN STREAMLIT ---

def run_test():
    """Función principal para correr la aplicación."""
    
    set_playful_style() # Aplica estilos
    
    # Inicializar el estado de la sesión
    if 'answers' not in st.session_state: st.session_state.answers = {}
    if 'test_completed' not in st.session_state: st.session_state.test_completed = False
    if 'current_page' not in st.session_state: st.session_state.current_page = 0
    if 'error_message' not in st.session_state: st.session_state.error_message = ""
        
    # Título y Encabezado
    st.markdown(f"""
    <div style="display: flex; align-items: center; margin-bottom: 20px;">
        <span style="font-size: 2rem; font-weight: 700; color: {COLOR_MINT_GREEN}; margin-right: 10px;">🧠</span>
        <h1 style="display: inline-block; margin: 0; border: none; padding: 0; color: {COLOR_VIBRANT_BLUE};">
            Test de Personalidad: ¡Descubre tu Perfil!
        </h1>
        <span style="font-size: 2rem; font-weight: 700; color: {COLOR_MINT_GREEN}; margin-left: 10px;">🌟</span>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"**Modelo OCEAN (Cinco Grandes)** | **{TOTAL_QUESTIONS} Ítems** (26 por rasgo)")
    st.markdown("---")
    
    # --- A. Mostrar Resultados (Si el test está completado) ---
    if st.session_state.test_completed:
        
        with st.spinner('✨ Analizando tu magia interior y generando tu perfil único...'):
            time.sleep(1.5)

        scores = calculate_score(st.session_state.answers)
        
        st.markdown(
            f"""
            <div class="profile-container">
                <h2>🎉 ¡Tu Perfil de Personalidad ha sido Desbloqueado!</h2>
                <p>Este análisis de 130 ítems te da una perspectiva detallada sobre tus rasgos dominantes del Modelo OCEAN. **Puntuación máxima por rasgo: {MAX_SCORE_PER_TRAIT}**.</p>
                
                <div class="print-button-container">
                    <button onclick="window.print()">
                        🖨️ ¡Guardar como PDF / Imprimir Informe Detallado!
                    </button>
                </div>
            </div>
            """, 
            unsafe_allow_html=True
        )
        
        for trait_code, score in scores.items():
            results = interpret_score(score, trait_code)
            trait_label = TRAIT_LABELS[trait_code]
            
            normalized_score = (score - MIN_SCORE_PER_TRAIT) / (MAX_SCORE_PER_TRAIT - MIN_SCORE_PER_TRAIT)
            
            st.markdown(f"""
            <div class="trait-header">
                <h3>{trait_label}</h3>
            </div>
            """, unsafe_allow_html=True)
            
            col_bar, col_score = st.columns([0.7, 0.3])

            with col_bar:
                st.markdown(f"""
                <div style="font-size: 0.9rem; color: #555;">Nivel Detectado: <b>{results['level']} ({results['color_label']})</b></div>
                <div style="height: 20px; border-radius: 10px; background-color: #E0E0E0; margin-top: 5px; overflow: hidden;">
                    <div style="width: {normalized_score*100}%; height: 100%; background-color: {results['color_hex']}; border-radius: 10px; transition: width 1s;"></div>
                </div>
                """, unsafe_allow_html=True)

            with col_score:
                st.metric(label="Puntuación", value=f"{score}/{MAX_SCORE_PER_TRAIT}", delta=f"Rango: {results['level']}")
            
            st.markdown(f"**Fortaleza Central:** {results['strength']}")
            
            st.markdown(
                f'<div class="challenge-box">', unsafe_allow_html=True
            )
            st.markdown(f"**{results['challenge']}**", unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
            
            st.markdown("<br>---<br>", unsafe_allow_html=True)
        
        st.markdown('<div class="restart-btn" style="text-align: center; margin-top: 30px;">', unsafe_allow_html=True)
        st.button("🔄 Quiero Explorar de Nuevo", on_click=restart_test, type="secondary", use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
            
    # --- B. Mostrar Cuestionario Paginado y Sidebar ---
    else:
        
        current_page = st.session_state.current_page
        start_index = current_page * QUESTIONS_PER_PAGE
        end_index = min(start_index + QUESTIONS_PER_PAGE, TOTAL_QUESTIONS)
        
        current_questions = QUESTIONS[start_index:end_index]
        
        # 1. Visualización del Progreso y Página Actual
        answered_total = len([ans for ans in st.session_state.answers.values() if ans is not None])
        progress_text = f"Progreso General: {answered_total}/{TOTAL_QUESTIONS} Preguntas"
        st.progress(answered_total / TOTAL_QUESTIONS, text=progress_text)
        
        st.subheader(f"Sección {current_page + 1} de {TOTAL_PAGES}")
        st.markdown("Marca tu nivel de acuerdo con cada afirmación:")
        st.markdown("---")


        # Mensaje de error (si existe)
        if st.session_state.error_message:
            st.error(st.session_state.error_message)
        
        # 2. Mostrar Preguntas (sin usar st.form)
        likert_options_tuple = [(v, k) for k, v in LIKERT_OPTIONS.items()]

        for q in current_questions:
            q_id = q['id']
            
            # Recuperar el valor actual del estado de sesión
            current_value = st.session_state.answers.get(q_id)
            
            selected_index = -1
            for i, (_, val) in enumerate(likert_options_tuple):
                if val == current_value:
                    selected_index = i
                    break
            
            # Usar st.radio para actualizar el estado de sesión directamente
            # Usamos un callback para guardar la respuesta en st.session_state.answers
            def update_answer(q_id, response_tuple):
                if response_tuple is not None:
                    st.session_state.answers[q_id] = response_tuple[1]
                else:
                    st.session_state.answers[q_id] = None
                # Limpiamos el mensaje de error al responder (feedback inmediato)
                st.session_state.error_message = "" 
                
            response_tuple = st.radio(
                label=f"**{q_id}.** {q['text']}",
                options=likert_options_tuple,
                key=f"radio_{q_id}", 
                index=selected_index if selected_index != -1 else None,
                format_func=lambda x: x[0],
                on_change=update_answer,
                args=(q_id, st.session_state[f"radio_{q_id}"]) # Pasa el nuevo valor seleccionado
            )
        
        st.markdown("---")
        
        # 3. Controles de Navegación en el Sidebar
        with st.sidebar:
            st.header("Navegación del Test")
            
            # Botón Anterior
            if current_page > 0:
                st.button("← Página Anterior", on_click=handle_navigation, args=("prev",), use_container_width=True, type="secondary")
            else:
                st.button("Inicio (Página 1)", disabled=True, use_container_width=True, type="secondary")
            
            st.markdown("<hr style='border: 1px dashed #DDD;'>", unsafe_allow_html=True)
            
            # Botón Siguiente / Finalizar
            is_last_page = current_page == TOTAL_PAGES - 1
            
            if is_last_page:
                st.button("🚀 Finalizar Test y Ver Mi Perfil", on_click=handle_navigation, args=("finish",), use_container_width=True, type="primary")
            else:
                st.button(f"Siguiente → (Pág. {current_page + 2} de {TOTAL_PAGES})", on_click=handle_navigation, args=("next",), use_container_width=True, type="primary")
                
            # Contador de Respuestas Pendientes en el Sidebar
            answered_current_page = 0
            for q in current_questions:
                if q["id"] in st.session_state.answers and st.session_state.answers[q["id"]] is not None:
                    answered_current_page += 1
            
            pending_count = len(current_questions) - answered_current_page

            st.markdown(f"""
                <div style="text-align: center; margin-top: 20px; padding: 10px; border: 1px solid #EEE; border-radius: 8px;">
                    <p style="font-size: 0.9rem; margin: 0; color: {COLOR_VIBRANT_BLUE};">Preguntas Pendientes:</p>
                    <p style="font-size: 1.5rem; font-weight: bold; color: {COLOR_DANGER_RED}; margin: 5px 0 0 0;">{pending_count}</p>
                </div>
            """, unsafe_allow_html=True)

        
        # --- APLICACIÓN DEL SCROLL FORZADO ---
        scroll_to_top()

# Ejecutar la aplicación
if __name__ == '__main__':
    run_test()
