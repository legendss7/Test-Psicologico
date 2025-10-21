import streamlit as st
import pandas as pd
import time
from io import BytesIO

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(
    page_title="Test Psicológico Avanzado",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- ESTILOS CSS PERSONALIZADOS ---
def load_css():
    """Carga estilos CSS para mejorar la apariencia de la aplicación."""
    st.markdown("""
        <style>
            /* --- Estilos Generales --- */
            .stApp {
                background-color: #f0f2f6;
            }
            
            /* --- Contenedor Principal --- */
            .main .block-container {
                padding-top: 2rem;
                padding-bottom: 2rem;
                padding-left: 3rem;
                padding-right: 3rem;
                border-radius: 20px;
            }
            
            /* --- Títulos y Texto --- */
            h1, h2 {
                color: #1E3A8A; /* Azul oscuro */
                font-weight: bold;
                text-align: center;
            }
            
            .question-text {
                font-size: 1.5rem;
                font-weight: 600;
                color: #334155; /* Gris oscuro */
                text-align: center;
                padding: 1.5rem;
                background-color: #FFFFFF;
                border-radius: 15px;
                border: 1px solid #e2e8f0;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
                margin-bottom: 2rem;
            }

            /* --- Botones --- */
            .stButton>button {
                width: 100%;
                border-radius: 12px;
                padding: 1rem;
                font-weight: bold;
                font-size: 1.1rem;
                color: #FFFFFF;
                border: none;
                transition: all 0.3s ease;
                box-shadow: 0 4px 14px rgba(0, 0, 0, 0.1);
            }
            
            /* Botón Principal (Comenzar, Siguiente) */
            div[data-testid="stHorizontalBlock"]>div:last-child .stButton>button {
                background-color: #2563EB; /* Azul primario */
            }
            div[data-testid="stHorizontalBlock"]>div:last-child .stButton>button:hover {
                background-color: #1D4ED8;
                transform: translateY(-2px);
            }
            
            /* Botón Secundario (Anterior, Reiniciar) */
            div[data-testid="stHorizontalBlock"]>div:first-child .stButton>button, .stDownloadButton>button {
                background-color: #64748B; /* Gris */
            }
             div[data-testid="stHorizontalBlock"]>div:first-child .stButton>button:hover, .stDownloadButton>button:hover {
                background-color: #475569;
                transform: translateY(-2px);
            }
            
            /* --- Opciones de Respuesta (Radio Buttons) --- */
            .stRadio > div {
                display: flex;
                flex-wrap: wrap;
                justify-content: center;
                gap: 1rem;
            }
            .stRadio > div > label {
                background-color: #FFFFFF;
                padding: 1.2rem 1.5rem;
                border-radius: 12px;
                border: 2px solid #d1d5db;
                color: #4b5563;
                font-weight: 500;
                transition: all 0.2s ease-in-out;
                cursor: pointer;
                box-shadow: 0 2px 4px rgba(0,0,0,0.05);
            }
            .stRadio > div > label:hover {
                border-color: #2563EB;
                color: #2563EB;
            }
            /* Ocultar el punto del radio button original */
            .stRadio > div > label > div:first-child {
                display: none;
            }
            
            /* --- Barra de Progreso --- */
            .stProgress > div > div > div > div {
                background-color: #2563EB;
            }
            
            /* --- Tarjetas de Resultados --- */
            .result-card {
                background-color: #FFFFFF;
                padding: 2rem;
                border-radius: 15px;
                box-shadow: 0 10px 20px rgba(0, 0, 0, 0.07);
                margin-bottom: 1.5rem;
                border-left: 8px solid #1E3A8A;
            }
            .result-card h3 {
                color: #1E3A8A;
                margin-top: 0;
            }
        </style>
    """, unsafe_allow_html=True)

# --- DATOS DEL TEST: 132 PREGUNTAS ---
# Se agrupan conceptualmente para facilitar la interpretación, aunque el test se presenta secuencialmente.
# Opciones y puntajes estandarizados:
# "Totalmente en desacuerdo": 1, "En desacuerdo": 2, "De acuerdo": 3, "Totalmente de acuerdo": 4
OPTIONS = ["Totalmente en desacuerdo", "En desacuerdo", "De acuerdo", "Totalmente de acuerdo"]
SCORES = [1, 2, 3, 4]

# Función para crear una pregunta estandarizada
def create_question(text):
    return {"pregunta": text, "opciones": OPTIONS, "puntajes": SCORES}

QUESTIONS = [
    # Dimensión: Autoconciencia Emocional
    create_question("Reconozco mis emociones cuando las siento."),
    create_question("Entiendo las causas de mis sentimientos."),
    create_question("Soy consciente de cómo mis emociones afectan mi comportamiento."),
    create_question("Me doy cuenta de mis puntos fuertes y debilidades."),
    create_question("Reflexiono sobre mis experiencias para aprender de ellas."),
    create_question("Sé qué situaciones me generan estrés o ansiedad."),
    create_question("Puedo nombrar la emoción que estoy sintiendo en un momento dado."),
    create_question("Noto cómo cambia mi estado de ánimo a lo largo del día."),
    create_question("Comprendo la conexión entre mi cuerpo y mis emociones (ej. nudo en el estómago por nervios)."),
    create_question("Tengo confianza en mis capacidades."),
    create_question("Pido feedback para entender mejor cómo me ven los demás."),
    create_question("Reconozco cuando necesito un descanso o un tiempo para mí."),
    
    # Dimensión: Autorregulación
    create_question("Mantengo la calma en situaciones de presión."),
    create_question("Pienso antes de actuar cuando estoy molesto/a."),
    create_question("Puedo manejar mis impulsos de manera efectiva."),
    create_question("Me adapto fácilmente a los cambios inesperados."),
    create_question("Soy capaz de decir 'no' cuando es necesario."),
    create_question("Cumplo con mis compromisos y promesas."),
    create_question("Manejo bien el estrés sin recurrir a hábitos poco saludables."),
    create_question("Puedo recuperarme rápidamente de las decepciones."),
    create_question("Mantengo una actitud positiva incluso cuando las cosas van mal."),
    create_question("Acepto la responsabilidad por mis errores."),
    create_question("Puedo concentrarme en una tarea a pesar de las distracciones."),
    create_question("Gestiono mi tiempo de forma eficaz."),

    # Dimensión: Motivación
    create_question("Me siento motivado/a para alcanzar mis metas."),
    create_question("Busco constantemente formas de mejorar."),
    create_question("Soy optimista sobre el futuro."),
    create_question("Tengo iniciativa y no espero a que me digan lo que tengo que hacer."),
    create_question("Persisto en mis esfuerzos a pesar de los obstáculos."),
    create_question("Encuentro satisfacción en el trabajo bien hecho."),
    create_question("Estoy dispuesto/a a salir de mi zona de confort para crecer."),
    create_question("Celebro mis logros, tanto grandes como pequeños."),
    create_question("Veo los fracasos como oportunidades de aprendizaje."),
    create_question("Me fijo metas desafiantes pero realistas."),
    create_question("Me inspira el éxito de los demás."),
    create_question("Tengo una visión clara de lo que quiero lograr en la vida."),

    # Dimensión: Empatía
    create_question("Me doy cuenta de las emociones de las personas que me rodean."),
    create_question("Escucho activamente cuando los demás hablan."),
    create_question("Puedo ponerme en el lugar de otra persona."),
    create_question("Ofrezco ayuda cuando veo que alguien la necesita."),
    create_question("Soy sensible a las necesidades y preocupaciones de los demás."),
    create_question("Entiendo las señales no verbales (lenguaje corporal, tono de voz)."),
    create_question("Respeto las opiniones de los demás, aunque no las comparta."),
    create_question("Me intereso genuinamente por las historias y experiencias de otras personas."),
    create_question("Evito juzgar a las personas sin conocer su situación."),
    create_question("Puedo dar feedback constructivo de manera respetuosa."),
    create_question("Fomento un ambiente de inclusión y respeto."),
    create_question("Me doy cuenta de las dinámicas de poder en un grupo."),

    # Dimensión: Habilidades Sociales
    create_question("Me resulta fácil iniciar conversaciones."),
    create_question("Soy bueno/a construyendo y manteniendo relaciones."),
    create_question("Puedo persuadir a otros de mi punto de vista de forma efectiva."),
    create_question("Manejo bien los conflictos y desacuerdos."),
    create_question("Trabajo bien en equipo y colaboro con los demás."),
    create_question("Me comunico de forma clara y concisa."),
    create_question("Soy capaz de inspirar y guiar a otros."),
    create_question("Disfruto conociendo gente nueva."),
    create_question("Sé cómo establecer límites saludables en mis relaciones."),
    create_question("Me siento cómodo/a hablando en público."),
    create_question("Soy un/a buen/a negociador/a."),
    create_question("Organizo y lidero actividades sociales o de grupo con facilidad."),

    # Dimensión: Resiliencia y Adaptabilidad
    create_question("Me adapto bien a nuevas culturas o entornos."),
    create_question("Cuando enfrento una crisis, busco soluciones activamente."),
    create_question("Mantengo la perspectiva a largo plazo durante momentos difíciles."),
    create_question("Aprendo de las críticas y las uso para mejorar."),
    create_question("Soy flexible en mi forma de pensar."),
    create_question("Puedo manejar múltiples tareas a la vez sin sentirme abrumado/a."),
    create_question("Acepto que el cambio es una parte natural de la vida."),
    create_question("Confío en mi capacidad para superar los desafíos."),
    create_question("Busco apoyo en amigos, familiares o colegas cuando lo necesito."),
    create_question("Mantengo mis rutinas de autocuidado (sueño, alimentación, ejercicio) en tiempos de estrés."),
    create_question("Soy capaz de encontrar el lado positivo en situaciones negativas."),
    create_question("Después de un revés, vuelvo a intentarlo con la misma o más energía."),
    
    # Dimensión: Organización y Planificación
    create_question("Planifico mis tareas diarias y semanales."),
    create_question("Priorizo mis responsabilidades de manera efectiva."),
    create_question("Mi espacio de trabajo (físico o digital) está ordenado."),
    create_question("Cumplo con los plazos de entrega."),
    create_question("Divido los proyectos grandes en tareas más pequeñas y manejables."),
    create_question("Uso herramientas como agendas o calendarios para organizarme."),
    create_question("Preparo con antelación lo que necesito para el día siguiente."),
    create_question("Evito la procrastinación."),
    create_question("Termino lo que empiezo."),
    create_question("Tomo notas en reuniones o clases para no olvidar detalles importantes."),
    create_question("Reviso mi progreso hacia mis metas regularmente."),
    create_question("Anticipo posibles problemas y planifico cómo abordarlos."),

    # Dimensión: Mentalidad de Crecimiento
    create_question("Creo que puedo desarrollar mis talentos y habilidades con esfuerzo."),
    create_question("Disfruto de los desafíos y los veo como oportunidades."),
    create_question("Me inspira el esfuerzo y la dedicación, no solo el talento innato."),
    create_question("Busco activamente aprender cosas nuevas."),
    create_question("No me desanimo si algo no me sale bien a la primera."),
    create_question("Estoy abierto/a a nuevas ideas y perspectivas."),
    create_question("Prefiero tareas que me exigen y me hacen crecer."),
    create_question("El esfuerzo es parte fundamental del camino al éxito."),
    create_question("Cuando alguien tiene éxito, me siento inspirado/a, no amenazado/a."),
    create_question("Invierto tiempo en mi desarrollo personal y profesional."),
    create_question("La palabra 'todavía' es importante para mí (ej. 'no sé hacerlo todavía')."),
    create_question("Valoro más el proceso de aprendizaje que el resultado final."),

    # Dimensión: Bienestar y Manejo del Estrés
    create_question("Dedico tiempo a hobbies y actividades que disfruto."),
    create_question("Duermo las horas suficientes para sentirme descansado/a."),
    create_question("Mi alimentación es generalmente equilibrada y saludable."),
    create_question("Realizo actividad física de forma regular."),
    create_question("Practico técnicas de relajación como la meditación o la respiración profunda."),
    create_question("Siento que tengo un buen equilibrio entre mi vida personal y laboral/académica."),
    create_question("Tengo relaciones sociales que me aportan y me hacen sentir bien."),
    create_question("Sé desconectar del trabajo o los estudios al final del día."),
    create_question("Limito mi exposición a noticias o redes sociales si me generan ansiedad."),
    create_question("Paso tiempo en la naturaleza."),
    create_question("Río con frecuencia."),
    create_question("Siento gratitud por las cosas buenas de mi vida."),
    
    # Dimensión: Creatividad y Curiosidad
    create_question("Me gusta explorar ideas fuera de lo común."),
    create_question("Hago preguntas para entender cómo funcionan las cosas."),
    create_question("Disfruto resolviendo problemas complejos."),
    create_question("Busco diferentes enfoques para una misma tarea."),
    create_question("Me siento cómodo/a con la ambigüedad y la incertidumbre."),
    create_question("Consumo contenidos variados (libros, documentales, podcasts) para ampliar mis horizontes."),
    create_question("Tengo facilidad para encontrar conexiones entre ideas aparentemente no relacionadas."),
    create_question("Experimento con nuevas formas de hacer las cosas."),
    create_question("No tengo miedo a cometer errores en el proceso creativo."),
    create_question("Tomo nota de ideas que se me ocurren de repente."),
    create_question("Dedico tiempo a actividades artísticas o de expresión personal."),
    create_question("Me considero una persona curiosa."),

    # Dimensión: Integridad y Ética
    create_question("Actúo de acuerdo con mis valores, incluso si es difícil."),
    create_question("Soy honesto/a y transparente en mis interacciones."),
    create_question("Mantengo la confidencialidad de la información que se me confía."),
    create_question("Trato a todas las personas con justicia y equidad."),
    create_question("Admito mis equivocaciones sin culpar a otros."),
    create_question("Defiendo lo que creo que es correcto."),
    create_question("Mis acciones son consistentes con mis palabras."),
    create_question("Se puede confiar en mí."),
    create_question("Considero el impacto de mis decisiones en los demás."),
    create_question("Me esfuerzo por hacer lo correcto, no solo lo más fácil."),
    create_question("Respeto las reglas y normativas establecidas."),
    create_question("Soy leal a las personas y causas que me importan.")
]

TOTAL_QUESTIONS = len(QUESTIONS)

# --- INICIALIZACIÓN DEL ESTADO DE LA SESIÓN ---
def initialize_session_state():
    """Inicializa las variables necesarias en el estado de la sesión."""
    if 'page' not in st.session_state:
        st.session_state.page = 'home'
    if 'current_question' not in st.session_state:
        st.session_state.current_question = 0
    if 'answers' not in st.session_state:
        st.session_state.answers = {}
    if 'start_time' not in st.session_state:
        st.session_state.start_time = 0

# --- LÓGICA DE INTERPRETACIÓN DE RESULTADOS ---
def get_profile_analysis(total_score):
    """Genera un análisis del perfil basado en el puntaje total."""
    strengths = []
    weaknesses = []
    opportunities = []

    # Se definen rangos de puntaje para cada dimensión (12 preguntas por dimensión, 11 dimensiones)
    # Puntaje min: 132 * 1 = 132
    # Puntaje máx: 132 * 4 = 528
    
    if total_score >= 450:
        strengths.append("Inteligencia Emocional Excepcional: Posees un profundo conocimiento de ti mismo y de los demás. Tu capacidad para gestionar emociones, motivarte y construir relaciones es un activo invaluable.")
        opportunities.append("Liderazgo Inspirador: Considera roles de mentoría o liderazgo donde puedas guiar a otros a desarrollar su propia inteligencia emocional.")
    elif 400 <= total_score < 450:
        strengths.append("Alta Inteligencia Emocional: Demuestras una sólida capacidad para manejar tus emociones y entender las de los demás. Eres empático/a, motivado/a y socialmente hábil.")
        opportunities.append("Consolidación de Habilidades: Identifica un área específica (ej. negociación, hablar en público) y busca perfeccionarla aún más.")
    elif 320 <= total_score < 400:
        strengths.append("Buena Inteligencia Emocional: Tienes una base funcional de habilidades emocionales. Generalmente manejas bien las situaciones, aunque hay áreas con claro potencial de mejora.")
        weaknesses.append("Inconsistencias en la Autorregulación: En momentos de alto estrés, podrías reaccionar de forma impulsiva. La práctica de la pausa consciente antes de actuar puede ser muy beneficiosa.")
        opportunities.append("Desarrollo de la Empatía Activa: Intenta practicar la escucha activa con más frecuencia, enfocándote en entender la perspectiva del otro sin interrumpir.")
    elif 250 <= total_score < 320:
        strengths.append("Potencial en Desarrollo: Reconoces la importancia de las emociones, pero a menudo luchas por gestionarlas de manera efectiva. Este es un punto de partida excelente para un crecimiento significativo.")
        weaknesses.append("Baja Autoconciencia: Puede que te cueste identificar y nombrar tus emociones, lo que dificulta su manejo. Un diario emocional puede ser una herramienta poderosa.")
        weaknesses.append("Dificultades en las Relaciones Interpersonales: Los malentendidos pueden ser frecuentes si te cuesta leer las señales emocionales de los demás.")
        opportunities.append("Fundamentos de la Inteligencia Emocional: Comienza con lo básico. Cursos o libros sobre autoconciencia y autorregulación pueden proporcionarte herramientas prácticas y efectivas.")
    else: # Menor a 250
        strengths.append("Disposición al Autoconocimiento: El hecho de haber completado este test demuestra una valiosa voluntad de conocerte y mejorar.")
        weaknesses.append("Áreas Críticas para el Desarrollo: Las habilidades de inteligencia emocional parecen ser un desafío importante en este momento, afectando probablemente varias áreas de tu vida (trabajo, relaciones, bienestar).")
        opportunities.append("Apoyo Profesional: Considera buscar la ayuda de un coach o terapeuta. Un profesional puede ofrecerte una guía estructurada y personalizada para un desarrollo emocional profundo y duradero.")

    recommendations = [
        "**Mindfulness y Meditación:** Dedica 5-10 minutos al día a prácticas de atención plena para mejorar la autoconciencia y reducir el estrés.",
        "**Diario de Emociones:** Anota diariamente cómo te sientes y qué causó esas emociones. Esto aumenta el reconocimiento emocional.",
        "**Busca Feedback:** Pide a personas de confianza comentarios sobre cómo manejas las situaciones sociales y emocionales.",
        "**Lectura Focalizada:** Lee libros sobre comunicación asertiva, manejo de conflictos o el área que consideres más débil.",
        "**Establece Metas Pequeñas:** En lugar de 'ser más empático', proponte 'preguntar a un colega cómo está y escuchar su respuesta sin interrumpir' una vez al día."
    ]

    return strengths, weaknesses, opportunities, recommendations

# --- FUNCIONES DE RENDERIZADO DE PÁGINAS ---

def show_home_page():
    """Muestra la página de inicio del test."""
    st.title("🧠 Test Psicológico de Perfil Integral")
    st.markdown("---")
    
    st.markdown("""
    <div style="text-align: center; background-color: #ffffff; padding: 2rem; border-radius: 15px; box-shadow: 0 8px 16px rgba(0,0,0,0.1);">
        <h2>Bienvenido/a</h2>
        <p style="font-size: 1.1rem; color: #4B5569;">
            Este test está diseñado para ayudarte a explorar diversas facetas de tu personalidad y tus habilidades socioemocionales. A través de <strong>132 preguntas</strong>, obtendrás una visión más clara de tus fortalezas, áreas de oportunidad y posibles caminos para tu desarrollo personal.
        </p>
        <p style="font-size: 1.1rem; color: #4B5569;">
            No hay respuestas correctas o incorrectas. Responde con la mayor honestidad posible para que los resultados sean un reflejo fiel de quién eres. El test tomará aproximadamente <strong>15-20 minutos</strong> en completarse.
        </p>
        <p style="font-weight: bold; font-size: 1.1rem;">¿Estás listo/a para comenzar este viaje de autodescubrimiento?</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Botón centrado
    col1, col2, col3 = st.columns([2, 1, 2])
    with col2:
        if st.button("🚀 Comenzar el Test", use_container_width=True):
            st.session_state.page = 'test'
            st.session_state.start_time = time.time()
            st.experimental_rerun()

def show_test_page():
    """Muestra la página del test con las preguntas."""
    st.markdown(f'<p style="text-align:center; font-size: 1.2rem; color: #1E3A8A; font-weight: bold;">Pregunta {st.session_state.current_question + 1} de {TOTAL_QUESTIONS}</p>', unsafe_allow_html=True)

    # Barra de progreso
    progress_value = (st.session_state.current_question + 1) / TOTAL_QUESTIONS
    st.progress(progress_value)

    st.markdown("<br>", unsafe_allow_html=True)

    q_index = st.session_state.current_question
    question = QUESTIONS[q_index]

    # Mostrar pregunta
    st.markdown(f'<p class="question-text">{question["pregunta"]}</p>', unsafe_allow_html=True)
    
    # Scroll al principio de la página
    st.components.v1.html("<script>window.parent.document.body.scrollTop = 0;</script>", height=0)

    # Opciones de respuesta
    # Usamos el texto de la pregunta como clave única para el radio button
    answer_key = f"q_{q_index}"
    current_answer_index = st.session_state.answers.get(q_index, None)
    
    # Convertir el puntaje guardado de nuevo a su índice en la lista de opciones
    if current_answer_index is not None:
        try:
            current_answer_index = question["puntajes"].index(current_answer_index)
        except ValueError:
            current_answer_index = None # Si el puntaje no está en la lista

    answer = st.radio(
        label="Selecciona una opción:",
        options=question["opciones"],
        index=current_answer_index if current_answer_index is not None else None,
        key=answer_key,
        label_visibility="collapsed"
    )

    # Guardar respuesta en session_state
    if answer:
        score_index = question["opciones"].index(answer)
        st.session_state.answers[q_index] = question["puntajes"][score_index]

    st.markdown("<br><br>", unsafe_allow_html=True)

    # --- Botones de Navegación ---
    col1, col2, col3, col4, col5 = st.columns([2, 2, 2, 2, 2])

    with col1:
        if st.button("⬅️ Anterior", use_container_width=True, disabled=(q_index == 0)):
            st.session_state.current_question -= 1
            st.experimental_rerun()

    with col5:
        # Lógica para el botón "Siguiente" o "Finalizar"
        is_last_question = (q_index == TOTAL_QUESTIONS - 1)
        button_text = "🎉 Finalizar Test" if is_last_question else "Siguiente ➡️"
        
        # Validar que se haya respondido antes de avanzar
        if st.button(button_text, use_container_width=True, disabled=(q_index not in st.session_state.answers)):
            if is_last_question:
                st.session_state.page = 'results'
            else:
                st.session_state.current_question += 1
            st.experimental_rerun()

def show_results_page():
    """Muestra la página de resultados y análisis del perfil."""
    st.title("✅ Resultados de tu Perfil Integral")
    st.markdown("---")

    # --- Cálculo de tiempo y puntaje ---
    total_time = time.time() - st.session_state.start_time
    minutes, seconds = divmod(total_time, 60)
    
    total_score = sum(st.session_state.answers.values())
    max_score = TOTAL_QUESTIONS * max(SCORES)
    score_percentage = (total_score / max_score) * 100

    st.info(f"Test completado en **{int(minutes)} minutos y {int(seconds)} segundos**.")
    
    st.markdown("### Puntuación General")
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric(label="Tu Puntuación Total", value=f"{total_score} / {max_score}")
    with col2:
        st.metric(label="Equivalente Porcentual", value=f"{score_percentage:.2f}%")
        
    st.markdown("<hr>", unsafe_allow_html=True)
    
    # --- Análisis del Perfil ---
    st.header("🔍 Análisis Detallado de tu Perfil")
    
    strengths, weaknesses, opportunities, recommendations = get_profile_analysis(total_score)
    
    # Fortalezas
    st.markdown("""
    <div class="result-card" style="border-left-color: #10B981;">
        <h3>💪 Fortalezas / Puntos Destacados</h3>
    </div>
    """, unsafe_allow_html=True)
    for item in strengths:
        st.markdown(f"- **{item}**")

    # Debilidades
    if weaknesses:
        st.markdown("""
        <div class="result-card" style="border-left-color: #F59E0B;">
            <h3>🌱 Aspectos a Mejorar</h3>
        </div>
        """, unsafe_allow_html=True)
        for item in weaknesses:
            st.markdown(f"- {item}")
    
    # Áreas de Oportunidad
    st.markdown("""
    <div class="result-card" style="border-left-color: #3B82F6;">
        <h3>🚀 Áreas de Oportunidad</h3>
    </div>
    """, unsafe_allow_html=True)
    for item in opportunities:
        st.markdown(f"- {item}")
        
    # Recomendaciones
    with st.expander("Ver Recomendaciones Generales", expanded=True):
        st.markdown("Aquí tienes algunas acciones prácticas que puedes empezar a implementar para tu desarrollo:")
        for rec in recommendations:
            st.markdown(f"- {rec}")
            
    st.markdown("<hr>", unsafe_allow_html=True)
    
    # --- Opciones de Descarga y Reinicio ---
    st.header("📥 Acciones Adicionales")
    
    # Preparar datos para descarga
    results_data = []
    for i, q in enumerate(QUESTIONS):
        score = st.session_state.answers.get(i, 'N/A')
        answer_text = ""
        if score != 'N/A':
            try:
                answer_index = q['puntajes'].index(score)
                answer_text = q['opciones'][answer_index]
            except ValueError:
                answer_text = "Respuesta inválida"
        
        results_data.append({
            "Nº Pregunta": i + 1,
            "Pregunta": q['pregunta'],
            "Respuesta Seleccionada": answer_text,
            "Puntaje": score
        })

    df = pd.DataFrame(results_data)
    
    # Convertir a Excel para descarga
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Resultados')
        # Auto-ajustar ancho de columnas
        worksheet = writer.sheets['Resultados']
        for idx, col in enumerate(df):
            series = df[col]
            max_len = max((
                series.astype(str).map(len).max(),
                len(str(series.name))
            )) + 2
            worksheet.set_column(idx, idx, max_len)
    excel_data = output.getvalue()

    col1, col2 = st.columns(2)
    with col1:
        st.download_button(
            label="📄 Descargar Resultados (Excel)",
            data=excel_data,
            file_name="resultados_test_psicologico.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True
        )

    with col2:
        if st.button("🔄 Reiniciar Test", use_container_width=True):
            # Limpiar todo el session state
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.experimental_rerun()

# --- CONTROLADOR PRINCIPAL DE LA APLICACIÓN ---
def main():
    """Función principal que controla el flujo de la aplicación."""
    load_css()
    initialize_session_state()

    if st.session_state.page == 'home':
        show_home_page()
    elif st.session_state.page == 'test':
        show_test_page()
    elif st.session_state.page == 'results':
        show_results_page()

if __name__ == "__main__":
    main()

