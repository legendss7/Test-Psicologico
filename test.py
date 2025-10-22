import streamlit as st
import pandas as pd
import time
from io import BytesIO
import random # Necesario para la función de completar al azar

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(
    page_title="Test Psicológico de Personalidad",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- DATOS DEL TEST ---
# Se incluyen las 132 preguntas divididas en 5 categorías para un perfil más completo.
# Cada pregunta tiene un puntaje directo (1-4).
preguntas_test = {
    "Estabilidad Emocional": [
        "Me mantengo tranquilo/a en situaciones de alta presión.",
        "Raramente me siento ansioso/a o preocupado/a sin motivo.",
        "Manejo bien el estrés y no me abrumo fácilmente.",
        "Mis emociones son generalmente estables y predecibles.",
        "Puedo recuperarme rápidamente de contratiempos o decepciones.",
        "No me irrito con facilidad por pequeñas molestias.",
        "Siento confianza en mis habilidades para manejar problemas inesperados.",
        "Raramente experimento cambios de humor drásticos.",
        "Soy una persona optimista la mayor parte del tiempo.",
        "Acepto las críticas constructivas sin ponerme a la defensiva.",
        "No suelo darle vueltas a mis errores del pasado.",
        "Duermo bien por la noche, sin que las preocupaciones me mantengan despierto/a.",
        "Me siento seguro/a y en control de mi vida.",
        "Puedo pensar con claridad y tomar decisiones bajo presión.",
        "No me ofendo fácilmente por los comentarios de los demás.",
        "Tengo una visión positiva del futuro.",
        "Me adapto bien a los cambios inesperados en mis planes.",
        "Disfruto de la vida y encuentro alegría en las cosas cotidianas.",
        "No necesito la validación constante de los demás para sentirme bien.",
        "Puedo perdonar a los demás y no guardo rencor.",
        "Siento que mis niveles de energía son constantes a lo largo del día.",
        "Puedo expresar mis sentimientos de manera calmada y racional.",
        "No me dejo llevar por el pánico en situaciones de emergencia.",
        "Me siento satisfecho/a con quién soy.",
        "Confío en que las cosas saldrán bien al final.",
        "No soy propenso/a a sentir celos o envidia."
    ],
    "Extroversión": [
        "Disfruto siendo el centro de atención en reuniones sociales.",
        "Me siento con energía después de pasar tiempo con mucha gente.",
        "Soy una persona habladora y sociable.",
        "Me es fácil iniciar conversaciones con desconocidos.",
        "Prefiero las actividades en grupo que las solitarias.",
        "Me consideran una persona extrovertida y sociable.",
        "Busco activamente nuevas interacciones sociales.",
        "Me siento cómodo/a en ambientes concurridos y ruidosos.",
        "Tengo un amplio círculo de amigos y conocidos.",
        "Me gusta organizar eventos y fiestas.",
        "Expreso mis opiniones abiertamente en discusiones de grupo.",
        "Me siento aburrido/a cuando paso mucho tiempo solo/a.",
        "Me gusta conocer gente nueva en fiestas o eventos.",
        "Soy una persona entusiasta y llena de energía.",
        "No tengo miedo de hablar en público.",
        "Prefiero un trabajo que implique mucha interacción con otras personas.",
        "Me describo como una persona alegre y animada.",
        "Suelo ser el/la primero/a en romper el hielo en una conversación.",
        "Me siento a gusto liderando un grupo.",
        "Disfruto de las actividades que implican acción y aventura.",
        "Me resulta fácil hacer amigos.",
        "Me gusta estar ocupado/a con muchas actividades.",
        "No dudo en tomar la iniciativa en situaciones sociales.",
        "La gente diría que soy una persona divertida y entretenida.",
        "Me siento más productivo/a cuando trabajo en equipo.",
        "Me encanta compartir mis experiencias con los demás.",
        "Busco oportunidades para socializar siempre que puedo."
    ],
    "Amabilidad": [
        "Siento empatía por los sentimientos de los demás.",
        "Disfruto ayudando a otras personas.",
        "Confío en la bondad de la gente.",
        "Soy una persona cooperativa y me gusta trabajar en equipo.",
        "Me preocupo por el bienestar de los demás.",
        "Soy paciente con las personas, incluso cuando cometen errores.",
        "Me resulta fácil perdonar a quienes me han ofendido.",
        "Soy una persona cortés y respetuosa con todos.",
        "Evito los conflictos y busco soluciones pacíficas.",
        "Me considero una persona cálida y compasiva.",
        "Estoy dispuesto/a a comprometerse para satisfacer las necesidades de otros.",
        "Creo que la mayoría de la gente tiene buenas intenciones.",
        "Me siento bien cuando hago algo bueno por alguien sin esperar nada a cambio.",
        "Escucho atentamente los problemas de los demás.",
        "No soy una persona cínica o desconfiada.",
        "Me gusta hacer que los demás se sientan cómodos y bienvenidos.",
        "Valoro la armonía en mis relaciones personales.",
        "No me gusta criticar o juzgar a los demás.",
        "Soy generoso/a con mi tiempo y recursos.",
        "Me intereso sinceramente por la vida de otras personas.",
        "Soy sensible a las necesidades emocionales de los que me rodean.",
        "La gente me describe como alguien amable y de buen corazón.",
        "Prefiero colaborar antes que competir.",
        "Me esfuerzo por ver lo mejor en cada persona.",
        "Trato a los demás como me gustaría que me trataran a mí.",
        "Ofrezco mi ayuda sin que me la pidan."
    ],
    "Responsabilidad": [
        "Soy una persona muy organizada y metódica.",
        "Presto atención a los detalles y me aseguro de que el trabajo esté bien hecho.",
        "Siempre cumplo con mis plazos y compromisos.",
        "Me gusta planificar mis actividades con antelación.",
        "Soy disciplinado/a y perseverante en mis tareas.",
        "Mantengo mi espacio de trabajo y mi hogar ordenados.",
        "No dejo las cosas para después (no procastino).",
        "La gente me considera una persona fiable y de confianza.",
        "Me fijo metas claras y trabajo de manera constante para alcanzarlas.",
        "Prefiero seguir una rutina establecida.",
        "Soy una persona puntual.",
        "Pienso antes de actuar y considero las consecuencias.",
        "Me tomo mis obligaciones muy en serio.",
        "Me gusta tener todo bajo control.",
        "Termino lo que empiezo.",
        "Soy trabajador/a y me esfuerzo por dar lo mejor de mí.",
        "Preparo listas de tareas para mantenerme organizado/a.",
        "No me distraigo fácilmente de mis objetivos.",
        "Prefiero la seguridad y la estabilidad a la espontaneidad.",
        "Soy una persona diligente y eficiente.",
        "Reviso mi trabajo varias veces para evitar errores.",
        "Me siento culpable si no cumplo con mis responsabilidades.",
        "La gente puede contar conmigo para hacer lo correcto.",
        "Actúo de acuerdo con mis principios y valores.",
        "Me enorgullezco de mi ética de trabajo.",
        "Sigo las reglas y los procedimientos establecidos.",
        "Prefiero un plan bien pensado a una improvisación."
    ],
    "Apertura a la Experiencia": [
        "Disfruto de las experiencias nuevas y desconocidas.",
        "Tengo una gran imaginación y me gusta soñar despierto/a.",
        "Me siento fascinado/a por el arte, la música y la naturaleza.",
        "Soy una persona curiosa y me gusta aprender cosas nuevas.",
        "Estoy abierto/a a probar comidas exóticas y diferentes.",
        "Me gusta viajar a lugares que no conozco.",
        "Disfruto de los debates intelectuales y las ideas abstractas.",
        "No me asustan los cambios; los veo como oportunidades.",
        "Tengo una amplia gama de intereses y pasatiempos.",
        "Me gusta resolver problemas complejos y rompecabezas.",
        "Prefiero la variedad a la rutina.",
        "Me considero una persona creativa.",
        "Estoy dispuesto/a a cuestionar mis propias creencias y valores.",
        "Me gusta leer sobre temas diversas y explorar nuevas ideas.",
        "Siento una profunda conexión con mis emociones.",
        "Disfruto de la belleza en sus diferentes formas.",
        "No me gusta que mi vida sea predecible.",
        "Tengo ideas originales y poco convencionales.",
        "Me gusta rodearme de personas con puntos de vista diferentes a los míos.",
        "Las metáforas y los símbolos me resultan interesantes.",
        "Me adapto con facilidad a nuevas culturas y entornos.",
        "Me gusta experimentar en lugar de seguir caminos ya probados.",
        "Tengo una mente abierta a las ideas no tradicionales.",
        "La rutina me aburre rápidamente.",
        "Busco la inspiración en fuentes diversas.",
        "Me gusta pensar en conceptos teóricos y filosóficos."
    ]
}

# Aplanar la lista de preguntas para el test
todas_las_preguntas = []
for categoria, lista_preguntas in preguntas_test.items():
    for pregunta in lista_preguntas:
        todas_las_preguntas.append({
            "pregunta": pregunta,
            "categoria": categoria,
            "opciones": ["Totalmente en desacuerdo", "En desacuerdo", "De acuerdo", "Totalmente de acuerdo"],
            "puntajes": [1, 2, 3, 4]
        })
TOTAL_PREGUNTAS = len(todas_las_preguntas)

# --- ESTILOS CSS ---
def cargar_css():
    st.markdown("""
    <style>
        /* Estilo general */
        body {
            font-family: 'Inter', sans-serif;
        }

        /* Contenedor principal del test */
        .stApp {
            background-color: #f0f2f6;
        }
        
        /* Títulos y textos */
        h1, h2, h3 {
            font-weight: 700;
            color: #1E3A8A; /* Azul oscuro */
        }
        
        /* Botones */
        .stButton>button {
            border-radius: 20px;
            border: 2px solid #1E3A8A;
            background-color: white;
            color: #1E3A8A;
            padding: 10px 24px;
            font-weight: bold;
            transition: all 0.3s ease;
        }
        .stButton>button:hover {
            background-color: #1E3A8A;
            color: white;
            border-color: #1E3A8A;
        }
        .stButton>button:focus {
            box-shadow: 0 0 0 3px #93C5FD;
            outline: none;
        }
        /* Estilo para el botón de completar al azar (destacado) */
        .stButton.random-complete>button {
            background-color: #FBBF24; /* Amarillo */
            color: #1E3A8A;
            border-color: #D97706;
        }
        .stButton.random-complete>button:hover {
            background-color: #F59E0B;
            color: white;
        }

        /* Botones de opción seleccionados */
        div[data-testid="stRadio"] label {
            display: block;
            margin-bottom: 10px;
            padding: 12px;
            background-color: #FFFFFF;
            border-radius: 12px;
            border: 1px solid #D1D5DB;
            cursor: pointer;
            transition: all 0.2s ease-in-out;
        }
        div[data-testid="stRadio"] label:hover {
            background-color: #EFF6FF;
            border-color: #3B82F6;
        }
        /* Ocultar el radio button nativo */
        div[data-testid="stRadio"] input {
            display: none;
        }
        
        /* Barra de progreso */
        .stProgress > div > div > div > div {
            background-color: #3B82F6; /* Azul brillante */
        }

        /* Estilo para las tarjetas de puntaje */
        .score-card {
            background-color: white;
            border-radius: 10px;
            padding: 20px;
            text-align: center;
            box-shadow: 0 4px 10px rgba(0,0,0,0.1);
            min-height: 150px;
        }
        .score-card h3 {
            margin-bottom: 5px;
            color: #3B82F6;
            font-size: 1.1em;
        }
        .score-card p {
            font-size: 2.5em;
            font-weight: bold;
            color: #1E3A8A;
            margin: 0;
        }

        /* Estilo para tarjetas de resultados detallados */
        .result-detail-card {
            background-color: white;
            border-radius: 15px;
            padding: 20px;
            margin-bottom: 20px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }
        
        /* Color para Fortalezas */
        .fortalezas { border-left: 5px solid #10B981; }
        /* Color para Debilidades */
        .debilidades { border-left: 5px solid #EF4444; }
        /* Color para Oportunidades */
        .oportunidades { border-left: 5px solid #3B82F6; }

        .result-detail-card h3 {
            margin-top: 0;
            font-size: 1.5em;
        }
        .result-detail-card h4 {
            margin-top: 10px;
            margin-bottom: 5px;
            font-size: 1.1em;
            color: #1E3A8A;
        }

    </style>
    """, unsafe_allow_html=True)

# --- FUNCIONES AUXILIARES ---

# Función MAXIMAMENTE FORZADA para el scroll al top
def forzar_scroll_al_top(idx):
    # Código JavaScript para forzar el scroll al inicio de la página
    js_code = f"""
        <script>
            // Forzar el scroll tras un retardo largo (250ms) para que el contenido se renderice
            setTimeout(function() {{
                var topAnchor = window.parent.document.getElementById('top-anchor');
                
                if (topAnchor) {{
                    // Usar scrollIntoView en el ancla oculta (la más fiable)
                    topAnchor.scrollIntoView({{ behavior: 'auto', block: 'start' }});
                }} else {{
                    // Opciones de fallback 
                    window.parent.scrollTo({{ top: 0, behavior: 'auto' }});
                    
                    var mainContent = window.parent.document.querySelector('[data-testid="stAppViewContainer"]');
                    if (mainContent) {{
                        mainContent.scrollTo({{ top: 0, behavior: 'auto' }});
                    }}
                }}
            }}, 250); 
        </script>
        """
    st.components.v1.html(js_code, height=0, scrolling=False)


# Función para inicializar el estado de la sesión
def inicializar_estado():
    if 'current_question' not in st.session_state:
        st.session_state.current_question = 0
    if 'answers' not in st.session_state:
        st.session_state.answers = {}
    if 'test_started' not in st.session_state:
        st.session_state.test_started = False
    if 'test_completed' not in st.session_state:
        st.session_state.test_completed = False
    if 'start_time' not in st.session_state:
        st.session_state.start_time = 0
    # Bandera para controlar el desplazamiento
    if 'should_scroll' not in st.session_state:
        st.session_state.should_scroll = False

# Función para reiniciar el test y volver a la pantalla de inicio
def volver_a_inicio():
    st.session_state.current_question = 0
    st.session_state.answers = {}
    st.session_state.test_started = False
    st.session_state.test_completed = False
    st.session_state.start_time = 0
    st.session_state.should_scroll = False
    st.rerun()

# Función para completar el test al azar (NUEVA FUNCIÓN)
def completar_al_azar():
    # Reiniciar el estado por si acaso ya había respuestas a medias
    st.session_state.answers = {} 
    st.session_state.start_time = time.time() # Usar el tiempo actual

    for idx, pregunta_data in enumerate(todas_las_preguntas):
        # Seleccionar una opción al azar
        opciones = pregunta_data['opciones']
        puntajes = pregunta_data['puntajes']
        
        # Elegir un índice aleatorio (0, 1, 2, o 3)
        random_index = random.randint(0, len(opciones) - 1)
        
        respuesta_elegida = opciones[random_index]
        puntaje_elegido = puntajes[random_index]

        # Almacenar la respuesta
        st.session_state.answers[idx] = {
            "pregunta": pregunta_data['pregunta'],
            "categoria": pregunta_data['categoria'],
            "respuesta": respuesta_elegida,
            "puntaje": puntaje_elegido
        }
        
    # Cambiar al estado de completado
    st.session_state.test_started = True
    st.session_state.test_completed = True
    st.rerun()

# Función para convertir DataFrame a Excel con resumen (ACTUALIZADA)
@st.cache_data
def to_excel_with_summary(df_raw, df_summary):
    output = BytesIO()
    # Usamos el motor xlsxwriter para crear múltiples hojas ordenadas
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        # Hoja 1: Respuestas Detalladas
        df_raw.to_excel(writer, sheet_name='Respuestas_Detalladas', index=False)
        
        # Hoja 2: Resumen de Puntajes
        df_summary.to_excel(writer, sheet_name='Resumen_Puntajes', index=False)

    processed_data = output.getvalue()
    return processed_data

# --- INTERPRETACIÓN DE RESULTADOS DETALLADA (MODIFICADA) ---
def interpretar_puntaje(categoria, puntaje):
    # Interpretación basada en el puntaje porcentual (Normalizado 0-100)
    
    # 1. Títulos de nivel de puntaje
    nivel = ""
    if puntaje >= 75:
        nivel = "Puntaje **Alto**"
    elif puntaje <= 40:
        nivel = "Puntaje **Bajo**"
    else:
        nivel = "Puntaje **Moderado**"

    # 2. Generación de textos detallados
    fortalezas_text = ""
    debilidades_text = ""
    oportunidades_text = ""
    
    # ESTABILIDAD EMOCIONAL (NEUROTICISMO INVERSO)
    if categoria == "Estabilidad Emocional":
        if puntaje >= 75: 
            fortalezas_text = "Muestras una notable calma y resiliencia. Eres capaz de manejar el estrés sin que te abrume, mantienes un estado de ánimo equilibrado y te recuperas rápidamente de los contratiempos. Tu serenidad es una fuente de fortaleza en entornos volátiles."
            debilidades_text = "En ocasiones, tu alta estabilidad puede llevarte a subestimar la seriedad de algunas situaciones estresantes o a parecer menos empático/a con la preocupación ajena."
            oportunidades_text = "Continúa practicando técnicas de manejo del estrés preventivo, como la atención plena, y asegúrate de que tu confianza no te haga descuidar la planificación de riesgos emocionales."
        elif puntaje <= 40:
            fortalezas_text = "Tienes una gran capacidad para sentir y procesar emociones profundas, lo que te hace sensible y perceptivo/a a las sutilezas de tu entorno."
            debilidades_text = "Tiendes a experimentar altos niveles de ansiedad, preocupación o inestabilidad emocional. El estrés te afecta profundamente, dificultando la toma de decisiones clara bajo presión. Eres propenso/a a cambios de humor y te cuesta recuperarte de las decepciones."
            oportunidades_text = "El foco principal es desarrollar estrategias de regulación emocional, como la meditación o la reestructuración cognitiva. Busca apoyo en momentos de alta tensión para evitar el agotamiento."
        else: 
            fortalezas_text = "Generalmente mantienes la compostura, pero eres consciente de tus límites emocionales. Tienes momentos de calma y momentos de sensibilidad, lo que te permite ser flexible."
            debilidades_text = "Puedes ser susceptible al estrés en momentos clave. La presión prolongada puede erosionar tu equilibrio, y a veces tardas en 'volver a la normalidad' después de un evento negativo."
            oportunidades_text = "Identifica las fuentes específicas de tu estrés y trabaja en límites personales más firmes. Busca un equilibrio entre el control emocional y la expresión sana de tus sentimientos."
    
    # EXTROVERSIÓN
    elif categoria == "Extroversión":
        if puntaje >= 75: 
            fortalezas_text = "Eres el alma de la fiesta; enérgico/a, sociable y entusiasta. Disfrutas de la interacción, te expresas abiertamente y buscas activamente la compañía. Esto te hace un líder nato y un excelente networker."
            debilidades_text = "El exceso de tiempo a solas te drena. Puedes parecer dominante en conversaciones o tomar decisiones impulsivas en busca de estimulación social constante."
            oportunidades_text = "Practica la escucha activa y dedica tiempo a la reflexión personal o a actividades solitarias para recargar tu energía interna y no depender solo del estímulo externo."
        elif puntaje <= 40:
            fortalezas_text = "Prefieres la tranquilidad, la concentración y la reflexión profunda. Trabajas mejor solo/a o en pequeños grupos. Tu capacidad de observación es alta y eres excelente en tareas que requieren autonomía."
            debilidades_text = "Puedes ser percibido/a como reservado/a o distante. Las situaciones sociales grandes te agotan rápidamente, y te cuesta iniciar conversaciones o expresarte abiertamente en público."
            oportunidades_text = "Busca activamente el contacto social cuando sea necesario, especialmente para el desarrollo profesional. No temas compartir tus ideas; tu profundidad de pensamiento es valiosa."
        else: 
            fortalezas_text = "Disfrutas de un equilibrio sano. Puedes ser sociable cuando es necesario y también valoras tu tiempo a solas. Eres flexible en diferentes entornos."
            debilidades_text = "A veces, la necesidad de equilibrio puede hacer que dudes entre la acción y la reflexión, o que te sientas indeciso/a sobre aceptar invitaciones sociales."
            oportunidades_text = "Sé consciente de tus niveles de energía en cada momento y aprende a comunicar tus necesidades de socialización o de aislamiento sin sentir culpa."

    # AMABILIDAD
    elif categoria == "Amabilidad":
        if puntaje >= 75: 
            fortalezas_text = "Eres una persona empática, bondadosa, cooperativa y de buen corazón. Tu deseo de ayudar y mantener la armonía es muy alto, y eres muy valorado/a por tu paciencia y compasión."
            debilidades_text = "Tu deseo de evitar conflictos puede llevarte a ser demasiado complaciente o a descuidar tus propias necesidades por las de los demás. Eres susceptible de que se aprovechen de tu generosidad."
            oportunidades_text = "Aprende a establecer límites firmes y a decir 'no' de manera asertiva. Recuerda que cuidar de ti mismo/a es esencial para poder seguir ayudando a los demás."
        elif puntaje <= 40:
            fortalezas_text = "Tienes un alto sentido de la justicia y no temes defender tus intereses. Eres directo/a y escéptico/a, lo que te protege de la manipulación."
            debilidades_text = "Puedes ser visto/a como crítico/a, cínico/a o combativo/a. Tiendes a priorizar tus objetivos sobre la cooperación y te cuesta empatizar con aquellos cuyas opiniones difieren."
            oportunidades_text = "Practica la escucha activa antes de reaccionar. Intenta buscar el beneficio mutuo en lugar de la victoria personal en las interacciones y trabaja en la expresión de la paciencia."
        else: 
            fortalezas_text = "Eres capaz de ser cooperativo/a y cortés, pero sabes cuándo es necesario defender tus derechos. Tienes un equilibrio entre la empatía y la asertividad."
            debilidades_text = "Puedes fluctuar entre ser demasiado complaciente en algunas situaciones y demasiado crítico/a en otras. Tu nivel de amabilidad depende mucho de la persona y el contexto."
            oportunidades_text = "Busca la coherencia en tus relaciones. Esfuérzate por mantener un nivel constante de respeto y cooperación, independientemente de tu opinión sobre la otra persona."

    # RESPONSABILIDAD
    elif categoria == "Responsabilidad":
        if puntaje >= 75: 
            fortalezas_text = "Eres altamente organizado/a, fiable y orientado/a a objetivos. Tu diligencia, disciplina y ética de trabajo te convierten en una persona de total confianza y en un motor de productividad."
            debilidades_text = "Tu rigor puede llevarte al perfeccionismo excesivo, lo que genera estrés innecesario y dificultad para delegar. Puedes ser percibido/a como rígido/a o inflexible ante cambios de última hora."
            oportunidades_text = "Aprende a aceptar la 'suficiencia' en lugar de la 'perfección'. Practica la delegación, confía en la capacidad de otros y desarrolla flexibilidad para manejar la incertidumbre sin ansiedad."
        elif puntaje <= 40:
            fortalezas_text = "Eres espontáneo/a, flexible y te adaptas rápidamente a los cambios. No te estresas por los detalles y disfrutas de la libertad de la improvisación."
            debilidades_text = "La organización, la puntualidad y el seguimiento de tareas son un desafío. Eres propenso/a a la procrastinación, lo que puede afectar tu fiabilidad y la consecución de metas a largo plazo."
            oportunidades_text = "Crea sistemas de recordatorio y estructuras mínimas (listas de tareas, planificación diaria simple) que te ayuden a cumplir compromisos sin sacrificar tu espontaneidad. Enfócate en la finalización de proyectos."
        else: 
            fortalezas_text = "Tienes un buen equilibrio entre planificación y flexibilidad. Eres capaz de ser responsable en áreas importantes mientras te permites cierta espontaneidad."
            debilidades_text = "Tu nivel de organización puede variar significativamente, siendo muy riguroso/a en unas áreas y despreocupado/a en otras. Esto puede generar inconsistencia."
            oportunidades_text = "Identifica las áreas de tu vida donde la responsabilidad tiene mayor impacto (trabajo, finanzas) y aplica conscientemente tus habilidades organizativas a ellas, manteniendo la flexibilidad en áreas de ocio."

    # APERTURA A LA EXPERIENCIA
    elif categoria == "Apertura a la Experiencia":
        if puntaje >= 75: 
            fortalezas_text = "Eres altamente creativo/a, intelectualmente curioso/a y posees una imaginación vívida. Disfrutas explorando nuevas ideas, artes y culturas, y te adaptas con facilidad a los cambios."
            debilidades_text = "Tu constante búsqueda de novedad puede llevar a la inconstancia en tus proyectos. Puedes aburrirte fácilmente con la rutina y la gente práctica puede encontrarte soñador/a o poco realista."
            oportunidades_text = "Aprende a canalizar tu curiosidad en proyectos a largo plazo que te permitan la profundidad sin caer en la rutina. Combina tus ideas abstractas con pasos prácticos y concretos."
        elif puntaje <= 40:
            fortalezas_text = "Eres práctico/a, realista y tienes los pies bien puestos en la tierra. Prefieres lo conocido y probado, lo que te brinda estabilidad y predictibilidad en tu vida."
            debilidades_text = "Tiendes a ser resistente al cambio y puedes tener dificultades para adaptarte a ideas muy abstractas o poco convencionales. Tu creatividad puede estar limitada por el deseo de mantener la rutina."
            oportunidades_text = "Busca pequeñas y seguras oportunidades para salir de tu zona de confort, como probar un nuevo hobby o leer sobre un tema totalmente ajeno a tus intereses habituales. La variedad puede enriquecer tu vida sin desestabilizarla."
        else: 
            fortalezas_text = "Aceptas la novedad cuando es necesario, pero también valoras la tradición y la estabilidad. Eres selectivo/a en las experiencias que eliges explorar."
            debilidades_text = "Tu apertura se limita a áreas específicas. Puedes ser reacio/a a probar cosas fuera de tu esfera de confort intelectual o práctico."
            oportunidades_text = "Evalúa dónde te estás limitando innecesariamente. Usa tu curiosidad moderada para explorar áreas de cambio que te brinden un claro beneficio o crecimiento personal."
            
    # 3. Formatear la salida
    
    # Unir el nivel de puntaje con los textos
    fortaleza = f"**{categoria} ({nivel}):** {fortalezas_text}"
    debilidad = f"**{categoria} ({nivel}):** {debilidades_text}"
    oportunidad = f"**{categoria} ({nivel}):** {oportunidades_text}"

    return fortaleza, debilidad, oportunidad


# --- LÓGICA DE LA APLICACIÓN ---

# 1. Cargar estilos y estado
cargar_css()
inicializar_estado()

# 2. ANCLA OCULTA (Para que el scrollIntoView() funcione de forma fiable)
st.markdown('<div id="top-anchor" style="position: absolute; top: 0px; height: 1px; width: 1px;"></div>', unsafe_allow_html=True)

idx = st.session_state.current_question

# 3. EJECUCIÓN CONDICIONAL DEL SCROLL
if st.session_state.should_scroll:
    forzar_scroll_al_top(idx)
    st.session_state.should_scroll = False


# --- PANTALLA DE INICIO ---
if not st.session_state.test_started:
    st.title("🧠 Test Psicológico de Personalidad")
    st.markdown("""
    Bienvenido/a a este test de personalidad. A través de **132 preguntas**, exploraremos cinco grandes dimensiones de tu carácter.
    
    - **No hay respuestas correctas o incorrectas.**
    - **Responde con sinceridad** para obtener el perfil más preciso.
    - El test tomará aproximadamente **15-20 minutos**.
    
    Al finalizar, recibirás un resumen detallado de tu perfil, incluyendo fortalezas, áreas a mejorar y oportunidades de crecimiento.
    """)
    
    st.markdown("---")
    
    col_start1, col_start2 = st.columns([1, 1])
    
    with col_start1:
        if st.button("🚀 Comenzar el Test", key="start_button"):
            st.session_state.test_started = True
            st.session_state.start_time = time.time()
            st.rerun()

    # NUEVO BOTÓN: COMPLETAR AL AZAR
    with col_start2:
        st.markdown('<div class="random-complete">', unsafe_allow_html=True) # Usar la clase CSS para el estilo
        if st.button("🎲 Completar al Azar (Demo)", key="random_button"):
            completar_al_azar()
        st.markdown('</div>', unsafe_allow_html=True) # Cerrar el div

# --- PANTALLA DEL TEST ---
elif not st.session_state.test_completed:
    
    pregunta_actual = todas_las_preguntas[idx]
    
    # Barra de progreso
    st.progress((idx + 1) / TOTAL_PREGUNTAS)
    st.markdown(f"#### Pregunta {idx + 1} de {TOTAL_PREGUNTAS}")

    st.markdown(f"### {pregunta_actual['pregunta']}")

    # Opciones de respuesta
    # Intentar cargar la respuesta previamente guardada
    current_answer_index = None
    if idx in st.session_state.answers:
        try:
            current_answer_text = st.session_state.answers[idx]['respuesta']
            # Obtener el índice de la opción guardada
            current_answer_index = pregunta_actual['opciones'].index(current_answer_text)
        except ValueError:
            current_answer_index = None # Si la respuesta guardada no está en opciones, no seleccionar nada

    respuesta = st.radio(
        "Selecciona tu respuesta:",
        options=pregunta_actual['opciones'],
        index=current_answer_index, # Usar la respuesta guardada
        key=f"q_{idx}"
    )

    # Almacenar la respuesta
    if respuesta:
        st.session_state.answers[idx] = {
            "pregunta": pregunta_actual['pregunta'],
            "categoria": pregunta_actual['categoria'],
            "respuesta": respuesta,
            "puntaje": pregunta_actual['puntajes'][pregunta_actual['opciones'].index(respuesta)]
        }
    
    st.markdown("<br>", unsafe_allow_html=True)

    # Navegación
    col1, col2, col3, col4 = st.columns([1, 1, 1, 1])

    with col1:
        # BOTÓN: VOLVER A INICIO (con advertencia si hay respuestas)
        if st.button("🏠 Inicio"):
            # Usamos un truco con un botón extra para la confirmación
            if len(st.session_state.answers) > 0 and not st.session_state.get('confirm_restart', False):
                 # Mensaje de advertencia
                st.warning("⚠️ Perderás tu progreso. Confirma si deseas volver a la pantalla de inicio.")
                if st.button("Sí, Volver a Inicio", key="confirm_home_action"):
                    volver_a_inicio()
            else:
                 volver_a_inicio() # Si no hay respuestas o ya confirmó, va directo

    with col2:
        if idx > 0:
            if st.button("⬅️ Anterior"):
                st.session_state.current_question -= 1
                st.session_state.should_scroll = True # Establece la bandera de scroll
                st.rerun()

    with col4:
        # Validar que se haya respondido
        if idx in st.session_state.answers:
            if idx < TOTAL_PREGUNTAS - 1:
                if st.button("Siguiente ➡️"):
                    st.session_state.current_question += 1
                    st.session_state.should_scroll = True # Establece la bandera de scroll
                    st.rerun()
            else:
                if st.button("🎉 Finalizar Test"):
                    st.session_state.test_completed = True
                    st.rerun()
        else:
            st.warning("Por favor, selecciona una respuesta para continuar.")


# --- PANTALLA DE RESULTADOS ---
else:
    st.balloons()
    st.title("✅ ¡Test Completado! Aquí está tu Perfil de Personalidad")
    
    end_time = time.time()
    # Calcular tiempo
    if abs(end_time - st.session_state.start_time) < 1:
        st.info("Resultado generado por la opción **Completar al Azar (Demo)**.")
    else:
        total_time = round((end_time - st.session_state.start_time) / 60, 2)
        st.info(f"Tiempo total para completar el test: **{total_time} minutos**.")

    # --- CÁLCULO DE RESULTADOS ---
    puntajes_por_categoria = {cat: [] for cat in preguntas_test.keys()}
    for idx_res, data in st.session_state.answers.items():
        puntajes_por_categoria[data['categoria']].append(data['puntaje'])

    resultados_finales = {}
    for categoria, puntajes in puntajes_por_categoria.items():
        total_preguntas_cat = len(preguntas_test[categoria])
        puntaje_max_cat = total_preguntas_cat * 4
        puntaje_obtenido = sum(puntajes)
        # Normalizar el puntaje a una escala de 100 para facilitar la interpretación
        porcentaje = round((puntaje_obtenido / puntaje_max_cat) * 100)
        resultados_finales[categoria] = porcentaje

    # --- PUNTUACIONES FINALES (REEMPLAZANDO EL GRÁFICO) ---
    st.markdown("---")
    st.header("🎯 Tus Puntajes Finales por Dimensión")
    st.markdown("""
    Tu perfil se basa en el modelo de los **Cinco Grandes Factores (Big Five)**, donde cada dimensión se puntúa de 0% (muy bajo) a 100% (muy alto).
    """)

    # Display scores using columns/metrics
    col_scores = st.columns(5)
    
    # Mapping para íconos
    icon_map = {
        "Estabilidad Emocional": "🧘",
        "Extroversión": "🗣️",
        "Amabilidad": "🤝",
        "Responsabilidad": "✅",
        "Apertura a la Experiencia": "✨"
    }

    for i, (cat, score) in enumerate(resultados_finales.items()):
        # Usar HTML con la clase score-card para un mejor estilo
        with col_scores[i]:
            st.markdown(f"""
            <div class="score-card">
                <h3>{icon_map.get(cat, '❓')} {cat}</h3>
                <p>{score}%</p>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("---")
    st.header("💡 Análisis Detallado de tu Perfil")

    fortalezas_list = []
    debilidades_list = []
    oportunidades_list = []
    
    # Generar todas las interpretaciones
    for cat, score in resultados_finales.items():
        f, d, o = interpretar_puntaje(cat, score)
        if f: fortalezas_list.append(f)
        if d: debilidades_list.append(d)
        if o: oportunidades_list.append(o)
        
    # Mostrar la interpretación en 3 columnas
    col_int1, col_int2, col_int3 = st.columns(3)

    with col_int1:
        st.markdown('<div class="result-detail-card fortalezas"><h3>🌟 Fortalezas Clave</h3></div>', unsafe_allow_html=True)
        if fortalezas_list:
            for item in fortalezas_list:
                # Separar el título del texto
                titulo, texto = item.split(':', 1)
                st.markdown(f"**{titulo.strip()}**")
                st.markdown(f"<p style='margin-left: 10px; border-left: 2px solid #D1D5DB; padding-left: 8px;'>{texto.strip()}</p>", unsafe_allow_html=True)
        else:
            st.info("No se identificaron fortalezas claras en este perfil.")

    with col_int2:
        st.markdown('<div class="result-detail-card debilidades"><h3>⚠️ Puntos de Mejora (Debilidades)</h3></div>', unsafe_allow_html=True)
        if debilidades_list:
            for item in debilidades_list:
                titulo, texto = item.split(':', 1)
                st.markdown(f"**{titulo.strip()}**")
                st.markdown(f"<p style='margin-left: 10px; border-left: 2px solid #D1D5DB; padding-left: 8px;'>{texto.strip()}</p>", unsafe_allow_html=True)
        else:
            st.info("¡Excelente! No hay áreas de debilidad significativas identificadas.")

    with col_int3:
        st.markdown('<div class="result-detail-card oportunidades"><h3>🌱 Estrategias de Crecimiento</h3></div>', unsafe_allow_html=True)
        if oportunidades_list:
            for item in oportunidades_list:
                titulo, texto = item.split(':', 1)
                st.markdown(f"**{titulo.strip()}**")
                st.markdown(f"<p style='margin-left: 10px; border-left: 2px solid #D1D5DB; padding-left: 8px;'>{texto.strip()}</p>", unsafe_allow_html=True)
        else:
            st.info("Tu perfil está bien definido; el crecimiento se centra en profundizar tus fortalezas principales.")
            
    st.markdown("---")
    
    # --- DESCARGA DE RESULTADOS (MEJORADA) ---
    with st.expander("📥 Descargar tus respuestas y resultados detallados"):
        # Preparar DataFrame de respuestas
        df_export = pd.DataFrame(list(st.session_state.answers.values()))
        st.dataframe(df_export.head()) # Mostrar solo una vista previa
        
        # Preparar DataFrame de Resumen (para el Excel)
        df_resumen_final = pd.DataFrame(list(resultados_finales.items()), columns=['Dimensión', 'Puntaje_Porcentaje'])
        
        col_dl1, col_dl2 = st.columns(2)
        with col_dl1:
            csv = df_export.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="Descargar Respuestas (CSV)",
                data=csv,
                file_name='mis_respuestas_detalladas.csv',
                mime='text/csv',
            )
        with col_dl2:
            # Llamar a la función actualizada con ambas tablas
            excel_data = to_excel_with_summary(df_export, df_resumen_final)
            st.download_button(
                label="Descargar Resultados Completos (Excel)",
                data=excel_data,
                file_name='mis_resultados_test_detallado.xlsx',
                mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            )

    # --- REINICIAR TEST Y VOLVER A INICIO ---
    st.markdown("---")
    if st.button("🔄 Volver a la pantalla de bienvenida"):
        volver_a_inicio()
