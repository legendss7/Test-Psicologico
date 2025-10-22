import streamlit as st
import pandas as pd
import time
import random 
from io import BytesIO

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(
    page_title="Test Psicológico de Personalidad",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- DATOS DEL TEST ---
# Se incluyen las 132 preguntas divididas en 5 categorías.
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
TOTAL_PREGUNTAS = sum(len(v) for v in preguntas_test.values())
# FIX NameError: Se define total_puntaje_maximo aquí para que esté disponible en el footer
total_puntaje_maximo = TOTAL_PREGUNTAS * 4

# --- ESTILOS CSS ---
def cargar_css():
    st.markdown("""
    <style>
        /* Estilo general de Streamlit */
        .stApp { background-color: #f0f2f6; }
        h1, h2, h3 { font-weight: 700; color: #1E3A8A; } /* Azul oscuro */
        
        /* Botones generales */
        .stButton>button {
            border-radius: 20px;
            border: 2px solid #1E3A8A;
            background-color: white;
            color: #1E3A8A;
            padding: 10px 24px;
            font-weight: bold;
            transition: all 0.3s ease;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }
        .stButton>button:hover { background-color: #1E3A8A; color: white; border-color: #1E3A8A; box-shadow: 0 6px 10px rgba(0,0,0,0.2); }

        /* Estilo para el botón de completar al azar (destacado) */
        .stButton.random-complete>button {
            background-color: #FBBF24; /* Amarillo */
            color: #1E3A8A;
            border-color: #D97706;
            box-shadow: 0 4px 6px rgba(245, 158, 11, 0.4);
        }
        .stButton.random-complete>button:hover { background-color: #F59E0B; color: white; border-color: #F59E0B; }

        /* Estilo para las tarjetas de puntaje (Puntuación general) */
        .score-card-native {
            background-color: white;
            border-radius: 10px;
            padding: 20px;
            text-align: center;
            box-shadow: 0 4px 10px rgba(0,0,0,0.1);
            min-height: 150px;
        }

        /* --- ESTILO DEL FOOTER FIJO --- */
        .app-footer {
            position: fixed;
            bottom: 0;
            left: 0;
            width: 100%;
            background-color: #f0f2f6; /* Coincide con el fondo de la app */
            padding: 10px 0;
            text-align: center;
            font-size: 0.85em;
            color: #6B7280;
            border-top: 1px solid #E5E7EB;
            z-index: 100;
        }
        
        /* --- ESTILO PARA LA PANTALLA DE INICIO (ACCESIBILIDAD) --- */
        
        /* Título Principal Animado */
        .animated-title {
            font-size: 3.5em; /* Aumentado */
            font-weight: 900;
            color: #4C1D95; /* Morado Oscuro */
            text-align: center;
            margin-bottom: 20px;
            animation: pulseShadow 2s infinite alternate ease-in-out;
        }

        @keyframes pulseShadow {
            from {
                text-shadow: 0 0 10px rgba(76, 29, 149, 0.5), 0 0 20px rgba(76, 29, 149, 0.1);
            }
            to {
                text-shadow: 0 0 20px rgba(76, 29, 149, 0.8), 0 0 30px rgba(76, 29, 149, 0.4);
            }
        }

        /* Estilo para el contenedor de la introducción */
        .welcome-card {
            background-color: white;
            border-radius: 12px;
            padding: 30px;
            box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1);
        }
        
        /* Texto de introducción AUMENTADO para accesibilidad */
        .welcome-intro {
            font-size: 1.5em; 
            line-height: 1.8;
            color: #1F2937; /* Color oscuro para alto contraste */
        }
        
        /* Estilo para la lista de factores AUMENTADO para accesibilidad */
        .factor-list li {
            margin-bottom: 15px;
            font-size: 1.3em;
            font-weight: 600;
        }
        
        .stSubheader {
            font-size: 1.8em; /* Aumentado */
            font-weight: 700;
            color: #1E3A8A;
        }
    </style>
    """, unsafe_allow_html=True)

# --- FUNCIONES AUXILIARES (Sin cambios) ---

# Función para añadir el footer al final de la página (Usa HTML, ya que Streamlit no tiene componente fijo)
def display_footer(nombre, puntaje_bruto, puntaje_maximo, nivel_general):
    st.markdown(f"""
    <div class="app-footer">
        Test creado por **{nombre}**: Puntaje Bruto: **{puntaje_bruto}** de **{puntaje_maximo}** posibles. | Nivel General: Puntaje **{nivel_general}**
    </div>
    """, unsafe_allow_html=True)


# Función MAXIMAMENTE FORZADA para el scroll al top
def forzar_scroll_al_top(idx):
    js_code = f"""
        <script>
            setTimeout(function() {{
                var topAnchor = window.parent.document.getElementById('top-anchor');
                if (topAnchor) {{
                    topAnchor.scrollIntoView({{ behavior: 'auto', block: 'start' }});
                }} else {{
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
    if 'current_question' not in st.session_state: st.session_state.current_question = 0
    if 'answers' not in st.session_state: st.session_state.answers = {}
    if 'test_started' not in st.session_state: st.session_state.test_started = False
    if 'test_completed' not in st.session_state: st.session_state.test_completed = False
    if 'start_time' not in st.session_state: st.session_state.start_time = 0
    if 'should_scroll' not in st.session_state: st.session_state.should_scroll = False
    if 'show_restart_warning' not in st.session_state: st.session_state.show_restart_warning = False

# Función para reiniciar el test y volver a la pantalla de inicio
def volver_a_inicio():
    st.session_state.current_question = 0
    st.session_state.answers = {}
    st.session_state.test_started = False
    st.session_state.test_completed = False
    st.session_state.start_time = 0
    st.session_state.should_scroll = False
    st.session_state.show_restart_warning = False
    st.rerun()

# Función para completar el test al azar (Simulación)
def completar_al_azar():
    st.session_state.answers = {} 
    st.session_state.start_time = time.time()
    
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

    for idx, pregunta_data in enumerate(todas_las_preguntas):
        opciones = pregunta_data['opciones']
        puntajes = pregunta_data['puntajes']
        random_index = random.randint(0, len(opciones) - 1)
        
        st.session_state.answers[idx] = {
            "pregunta": pregunta_data['pregunta'],
            "categoria": pregunta_data['categoria'],
            "respuesta": opciones[random_index],
            "puntaje": puntajes[random_index]
        }
        
    st.session_state.test_started = True
    st.session_state.test_completed = True
    st.rerun()

# Función para convertir DataFrame a Excel con resumen
@st.cache_data
def to_excel_with_summary(df_raw, df_summary):
    output = BytesIO()
    with pd.ExcelWriter(output) as writer:
        df_raw.to_excel(writer, sheet_name='Respuestas_Detalladas', index=False)
        df_summary.to_excel(writer, sheet_name='Resumen_Puntajes', index=False)
    processed_data = output.getvalue()
    return processed_data

# Función para generar el análisis (SÓLO Streamlit)
def generar_analisis_componente(categoria, porcentaje, puntaje_obtenido, puntaje_maximo, nivel_descriptor, fortalezas_text, debilidades_text, oportunidades_text):
    
    # Contenedor principal de la tarjeta (Streamlit Nativo)
    with st.container(border=True): 
        st.markdown(f"### {icon_map.get(categoria, '❓')} {categoria}")
        
        # Puntaje Porcentual
        st.markdown(f"""
        <p style="font-size: 3em; font-weight: 800; color: #4C1D95; margin: 0;">{porcentaje}%</p>
        """, unsafe_allow_html=True) # Pequeña excepción para estilo grande

        # Datos Brutos y Nivel General (Usando Markdown y Columns para evitar la falla)
        col_pb, col_ng = st.columns([1, 1])
        with col_pb:
            st.markdown(f"**Puntaje Bruto:** {puntaje_obtenido} de {puntaje_maximo} posibles.")
        with col_ng:
            # FIX CRÍTICO: Usamos 'nivel_descriptor' directamente (ej: **Alto**)
            st.markdown(f"**Nivel General:** Puntaje {nivel_descriptor}")
        
        st.divider()

        # Fortaleza (Usando st.success para un buen estilo)
        st.success(f"""
        **💪 Fortaleza:** {fortalezas_text}
        """)

        # Punto de Mejora (Usando st.warning para un buen estilo)
        st.warning(f"""
        **🚩 Punto de Mejora:** {debilidades_text}
        """)
        
        # Oportunidad (Usando st.info para un buen estilo)
        st.info(f"""
        **🌱 Oportunidad:** {oportunidades_text}
        """)

# --- INTERPRETACIÓN DE RESULTADOS DETALLADA (Sin cambios) ---
def interpretar_puntaje(categoria, puntaje):
    
    nivel = ""
    if puntaje >= 75: nivel = "**Alto**"
    elif puntaje <= 40: nivel = "**Bajo**"
    else: nivel = "**Moderado**"

    fortalezas_text, debilidades_text, oportunidades_text = "", "", ""
    
    # Textos detallados por categoría
    if categoria == "Estabilidad Emocional":
        if nivel == "**Alto**": 
            fortalezas_text = "Muestras una notable calma y resiliencia. Eres capaz de manejar el estrés sin que te abrume, mantienes un estado de ánimo equilibrado y te recuperas rápidamente de los contratiempos. Tu serenidad es una fuente de fortaleza en entornos volátiles. **Tu alta puntuación refleja una baja reactividad emocional**."
            debilidades_text = "En ocasiones, tu alta estabilidad puede llevarte a subestimar la seriedad de algunas situaciones estresantes o a parecer menos empático/a con la preocupación ajena. Procura no reprimir emociones importantes."
            oportunidades_text = "Continúa practicando técnicas de manejo del estrés preventivo y asegúrate de que tu confianza no te haga descuidar la planificación de riesgos emocionales. Trabaja en la validación emocional de los demás."
        elif nivel == "**Bajo**":
            fortalezas_text = "Tienes una gran capacidad para sentir y procesar emociones profundas, lo que te hace sensible y perceptivo/a a las sutilezas de tu entorno. **Tu profundidad emocional puede ser una ventaja para la creatividad y la empatía**."
            debilidades_text = "Tiendes a experimentar altos niveles de ansiedad, preocupación o inestabilidad emocional. El estrés te afecta profundamente, dificultando la toma de decisiones clara bajo presión. La preocupación es una respuesta frecuente."
            oportunidades_text = "El foco principal es desarrollar estrategias de regulación emocional, como la meditación o la reestructuración cognitiva. Busca apoyo en momentos de alta tensión para evitar el agotamiento y establece rutinas para la calma."
        else: 
            fortalezas_text = "Generalmente mantienes la compostura, pero eres consciente de tus límites emocionales. Tienes momentos de calma y momentos de sensibilidad, lo que te permite ser flexible. **Tu respuesta emocional es adecuada a la mayoría de las situaciones**."
            debilidades_text = "Puedes ser susceptible al estrés en momentos clave. La presión prolongada puede erosionar tu equilibrio, y a veces tardas en 'volver a la normalidad' después de un evento negativo. Tiendes a internalizar las tensiones."
            oportunidades_text = "Identifica las fuentes específicas de tu estrés y trabaja en límites personales más firmes. Busca un equilibrio entre el control emocional y la expresión sana de tus sentimientos, mejorando la gestión de la recuperación post-estrés."
    
    elif categoria == "Extroversión":
        if nivel == "**Alto**": 
            fortalezas_text = "Eres el alma de la fiesta; enérgico/a, sociable y entusiasta. Disfrutas de la interacción, te expresas abiertamente y buscas activamente la compañía. **Esto te hace un líder nato, un excelente networker y promotor de actividades grupales**."
            debilidades_text = "El exceso de tiempo a solas te drena. Puedes parecer dominante en conversaciones o tomar decisiones impulsivas en busca de estimulación social constante. Podrías sobrecargar tu agenda social."
            oportunidades_text = "Practica la escucha activa y dedica tiempo a la reflexión personal o a actividades solitarias para recargar tu energía interna y no depender solo del estímulo externo. Fomenta la profundidad en tus interacciones."
        elif nivel == "**Bajo**":
            fortalezas_text = "Prefieres la tranquilidad, la concentración y la reflexión profunda. Trabajas mejor solo/a o en pequeños grupos. **Tu capacidad de observación es alta y eres excelente en tareas que requieren autonomía y pensamiento concentrado**."
            debilidades_text = "Puedes ser percibido/a como reservado/a o distante. Las situaciones sociales grandes te agotan rápidamente, y te cuesta iniciar conversaciones o expresarte abiertamente en público, limitando tu visibilidad."
            oportunidades_text = "Busca activamente el contacto social cuando sea necesario, especialmente para el desarrollo profesional. No temas compartir tus ideas; tu profundidad de pensamiento es valiosa. Practica la comunicación asertiva en entornos pequeños."
        else: 
            fortalezas_text = "Disfrutas de un equilibrio sano. Puedes ser sociable cuando es necesario y también valoras tu tiempo a solas. **Eres flexible en diferentes entornos y puedes adaptarte a la demanda social sin agotarte totalmente**."
            debilidades_text = "A veces, la necesidad de equilibrio puede hacer que dudes entre la acción y la reflexión, o que te sientas indeciso/a sobre aceptar invitaciones sociales. Tu nivel de energía social es variable."
            oportunidades_text = "Sé consciente de tus niveles de energía en cada momento y aprende a comunicar tus necesidades de socialización o de aislamiento sin sentir culpa. Planifica estratégicamente tus interacciones más importantes."

    elif categoria == "Amabilidad":
        if nivel == "**Alto**": 
            fortalezas_text = "Eres una persona empática, bondadosa, cooperativa y de buen corazón. Tu deseo de ayudar y mantener la armonía es muy alto, y eres muy valorado/a por tu paciencia y compasión. **Actúas como mediador natural y fomentas la cohesión social**."
            debilidades_text = "Tu deseo de evitar conflictos puede llevarte a ser demasiado complaciente o a descuidar tus propias necesidades por las de los demás. Eres susceptible de que se aprovechen de tu generosidad y te cuesta establecer límites."
            oportunidades_text = "Aprende a establecer límites firmes y a decir 'no' de manera asertiva. Recuerda que cuidar de ti mismo/a es esencial para poder seguir ayudando a los demás. El desarrollo de la asertividad es clave."
        elif nivel == "**Bajo**":
            fortalezas_text = "Tienes un alto sentido de la justicia y no temes defender tus intereses. Eres directo/a y escéptico/a, lo que te protege de la manipulación. **Eres firme en tus convicciones y ofreces opiniones honestas y críticas**."
            debilidades_text = "Puedes ser visto/a como crítico/a, cínico/a o combativo/a. Tiendes a priorizar tus objetivos sobre la cooperación y te cuesta empatizar con aquellos cuyas opiniones difieren, lo que puede generar fricción."
            oportunidades_text = "Practica la escucha activa antes de reaccionar. Intenta buscar el beneficio mutuo en lugar de la victoria personal en las interacciones y trabaja en la expresión de la paciencia y la diplomacia."
        else: 
            fortalezas_text = "Eres capaz de ser cooperativo/a y cortés, pero sabes cuándo es necesario defender tus derechos. **Tienes un equilibrio entre la empatía y la asertividad que te permite negociar eficazmente**."
            debilidades_text = "Puedes fluctuar entre ser demasiado complaciente en algunas situaciones y demasiado crítico/a en otras. Tu nivel de amabilidad depende mucho de la persona y el contexto, resultando en inconsistencia."
            oportunidades_text = "Busca la coherencia en tus relaciones. Esfuérzate por mantener un nivel constante de respeto y cooperación, independientemente de tu opinión sobre la otra persona, aplicando la asertividad de forma equilibrada."

    elif categoria == "Responsabilidad":
        if nivel == "**Alto**": 
            fortalezas_text = "Eres altamente organizado/a, fiable y orientado/a a objetivos. Tu diligencia, disciplina y ética de trabajo te convierten en una persona de total confianza y en un motor de productividad. **Tu planificación a largo plazo es excelente**."
            debilidades_text = "Tu rigor puede llevarte al perfeccionismo excesivo, lo que genera estrés innecesario y dificultad para delegar. Puedes ser percibido/a como rígido/a o inflexible ante cambios de última hora, luchando contra la entropía."
            oportunidades_text = "Aprende a aceptar la 'suficiencia' en lugar de la 'perfección'. Practica la delegación, confía en la capacidad de otros y desarrolla flexibilidad para manejar la incertidumbre sin ansiedad. Integra el descanso planificado."
        elif nivel == "**Bajo**":
            fortalezas_text = "Eres espontáneo/a, flexible y te adaptas rápidamente a los cambios. No te estresas por los detalles y disfrutas de la libertad de la improvisación. **Tu adaptabilidad te hace resiliente ante los imprevistos**."
            debilidades_text = "La organización, la puntualidad y el seguimiento de tareas son un desafío. Eres propenso/a a la procrastinación, lo que puede afectar tu fiabilidad y la consecución de metas a largo plazo. Tiendes a enfocarte en el presente inmediato."
            oportunidades_text = "Crea sistemas de recordatorio y estructuras mínimas (listas de tareas, planificación diaria simple) que te ayuden a cumplir compromisos sin sacrificar tu espontaneidad. Enfócate en la finalización de proyectos antes de empezar nuevos."
        else: 
            fortalezas_text = "Tienes un buen equilibrio entre planificación y flexibilidad. Eres capaz de ser responsable en áreas importantes mientras te permites cierta espontaneidad. **Puedes ser un planificador eficiente sin ser esclavo de la rutina**."
            debilidades_text = "Tu nivel de organización puede variar significativamente, siendo muy riguroso/a en unas áreas y despreocupado/a en otras. Esto puede generar inconsistencia y que se te escapen detalles importantes."
            oportunidades_text = "Identifica las áreas de tu vida donde la responsabilidad tiene mayor impacto (trabajo, finanzas) y aplica conscientemente tus habilidades organizativas a ellas, manteniendo la flexibilidad en áreas de ocio. Busca un nivel de rigor constante."

    elif categoria == "Apertura a la Experiencia":
        if nivel == "**Alto**": 
            fortalezas_text = "Eres altamente creativo/a, intelectualmente curioso/a y posees una imaginación vívida. Disfrutas explorando nuevas ideas, artes y culturas, y te adaptas con facilidad a los cambios. **Tu mente es un motor constante de innovación**."
            debilidades_text = "Tu constante búsqueda de novedad puede llevar a la inconstancia en tus proyectos. Puedes aburrirte fácilmente con la rutina y la gente práctica puede encontrarte soñador/a o poco realista, perdiendo el foco."
            oportunidades_text = "Aprende a canalizar tu curiosidad en proyectos a largo plazo que te permitan la profundidad sin caer en la rutina. Combina tus ideas abstractas con pasos prácticos y concretos. Define objetivos a medio plazo."
        elif nivel == "**Bajo**":
            fortalezas_text = "Eres práctico/a, realista y tienes los pies bien puestos en la tierra. Prefieres lo conocido y probado, lo que te brinda estabilidad y predictibilidad en tu vida. **Eres fiable en tu juicio y valoras la experiencia demostrada**."
            debilidades_text = "Tiendes a ser resistente al cambio y puedes tener dificultades para adaptarte a ideas muy abstractas o poco convencionales. Tu creatividad puede estar limitada por el deseo de mantener la rutina y la tradición."
            oportunidades_text = "Busca pequeñas y seguras oportunidades para salir de tu zona de confort, como probar un nuevo hobby o leer sobre un tema totalmente ajeno a tus intereses habituales. La variedad puede enriquecer tu vida sin desestabilizarla. Expande tus horizontes intelectuales de forma gradual."
        else: 
            fortalezas_text = "Aceptas la novedad cuando es necesario, pero también valoras la tradición y la estabilidad. **Eres selectivo/a en las experiencias que eliges explorar y tienes un enfoque pragmático de la creatividad**."
            debilidades_text = "Tu apertura se limita a áreas específicas. Puedes ser reacio/a a probar cosas fuera de tu esfera de confort intelectual o práctico, lo que limita el crecimiento en áreas no familiares."
            oportunidades_text = "Evalúa dónde te estás limitando innecesariamente. Usa tu curiosidad moderada para explorar áreas de cambio que te brinden un claro beneficio o crecimiento personal. Busca activamente la perspectiva de otros."
            
    # Devolvemos solo el descriptor del nivel (ej: "**Alto**") y los textos de análisis
    return nivel, fortalezas_text, debilidades_text, oportunidades_text


# --- LÓGICA PRINCIPAL ---

# 1. Cargar estilos y estado
cargar_css()
inicializar_estado()

# 2. ANCLA OCULTA
st.markdown('<div id="top-anchor" style="position: absolute; top: 0px; height: 1px; width: 1px;"></div>', unsafe_allow_html=True)

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

idx = st.session_state.current_question

# 3. EJECUCIÓN CONDICIONAL DEL SCROLL
if st.session_state.should_scroll:
    forzar_scroll_al_top(idx)
    st.session_state.should_scroll = False

# --- PANTALLA DE INICIO (ACCESIBLE Y CON TÍTULO ANIMADO) ---
if not st.session_state.test_started:
    
    # Título Animado y Llamativo
    st.markdown('<p class="animated-title">🧠 Tu Perfil Personalizado: El Modelo Big Five</p>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Usamos un solo contenedor ya que la imagen fue eliminada
    st.container()
    
    # Contenedor de Bienvenida con estilos de accesibilidad (clases CSS aumentadas)
    st.markdown('<div class="welcome-card">', unsafe_allow_html=True)
    st.markdown('<h2 class="stSubheader">¡Bienvenido/a al Viaje del Auto-Descubrimiento!</h2>', unsafe_allow_html=True)
    
    st.markdown("""
    <p class="welcome-intro">
    Este cuestionario es tu herramienta para explorar tu personalidad según el **Modelo de los Cinco Grandes Factores (Big Five)**, la referencia más sólida y aceptada en la psicología moderna. Conocer estos factores te ofrece una base científica para entender tu comportamiento, tus motivaciones y tu interacción con el mundo.
    </p>
    
    <p class="welcome-intro" style="font-weight: bold;">
    Dedica unos 10-15 minutos a responder **132 preguntas** con total honestidad.
    </p>
    
    <h4 style="color: #1E3A8A; margin-top: 25px; font-size: 1.5em; font-weight: 700;">Las 5 Dimensiones que Explorarás:</h4>
    <ul class="factor-list">
        <li><span style="font-weight: bold; color: #3B82F6;">🧘 Estabilidad Emocional (Neuroticismo):</span> ¿Manejas bien el estrés o eres propenso/a a la ansiedad?</li>
        <li><span style="font-weight: bold; color: #3B82F6;">🗣️ Extroversión:</span> ¿Buscas la compañía social o prefieres la tranquilidad a solas?</li>
        <li><span style="font-weight: bold; color: #3B82F6;">🤝 Amabilidad:</span> ¿Eres cooperativo, empático y buscas la armonía?</li>
        <li><span style="font-weight: bold; color: #3B82F6;">✅ Responsabilidad:</span> ¿Eres organizado, metódico y orientado a cumplir metas?</li>
        <li><span style="font-weight: bold; color: #3B82F6;">✨ Apertura a la Experiencia:</span> ¿Eres creativo, curioso y abierto a nuevas ideas y culturas?</li>
    </ul>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Botones centrados con mejor distribución
    col_start1, col_start2, col_start3 = st.columns([1.5, 0.5, 1.5])
    
    with col_start1:
        # Botón principal, grande y visible
        if st.button("🚀 Comenzar el Test Ahora", key="start_button", use_container_width=True):
            st.session_state.test_started = True
            st.session_state.start_time = time.time()
            st.rerun()

    with col_start3:
        st.markdown('<div class="random-complete">', unsafe_allow_html=True) 
        # Botón demo
        if st.button("🎲 Completar al Azar (Ver Demo Rápida)", key="random_button", use_container_width=True):
            completar_al_azar()
        st.markdown('</div>', unsafe_allow_html=True) 

# --- PANTALLA DEL TEST (Sin cambios) ---
elif not st.session_state.test_completed:
    
    pregunta_actual = todas_las_preguntas[idx]
    
    # Barra de progreso
    st.progress((idx + 1) / TOTAL_PREGUNTAS)
    st.markdown(f"#### Pregunta {idx + 1} de {TOTAL_PREGUNTAS}")

    st.markdown(f"### {pregunta_actual['pregunta']}")

    current_answer_index = None
    if idx in st.session_state.answers:
        try:
            current_answer_text = st.session_state.answers[idx]['respuesta']
            current_answer_index = pregunta_actual['opciones'].index(current_answer_text)
        except ValueError:
            current_answer_index = None

    respuesta = st.radio(
        "Selecciona tu respuesta:",
        options=pregunta_actual['opciones'],
        index=current_answer_index,
        key=f"q_{idx}"
    )

    if respuesta:
        st.session_state.answers[idx] = {
            "pregunta": pregunta_actual['pregunta'],
            "categoria": pregunta_actual['categoria'],
            "respuesta": respuesta,
            "puntaje": pregunta_actual['puntajes'][pregunta_actual['opciones'].index(respuesta)]
        }
    
    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns([1, 1, 1, 1])

    with col1:
        if st.button("🏠 Inicio", key="home_button_test"):
            if len(st.session_state.answers) > 0:
                st.session_state.show_restart_warning = True
            else:
                volver_a_inicio()

    with col2:
        if idx > 0:
            if st.button("⬅️ Anterior"):
                st.session_state.current_question -= 1
                st.session_state.should_scroll = True
                st.rerun()

    with col4:
        if idx in st.session_state.answers:
            if idx < TOTAL_PREGUNTAS - 1:
                if st.button("Siguiente ➡️"):
                    st.session_state.current_question += 1
                    st.session_state.should_scroll = True
                    st.rerun()
            else:
                if st.button("🎉 Finalizar Test"):
                    st.session_state.test_completed = True
                    st.rerun()
        else:
            st.warning("Por favor, selecciona una respuesta para continuar.")
            
    if st.session_state.get('show_restart_warning', False):
        st.error("⚠️ Advertencia: Perderás **TODO** tu progreso actual. ¿Estás seguro/a que deseas volver al inicio?")
        
        col_conf1, col_conf2, _ = st.columns([1, 1, 2])
        with col_conf1:
            if st.button("Sí, volver", key="confirm_restart_yes"):
                volver_a_inicio()
        with col_conf2:
            if st.button("No, seguir en el test", key="confirm_restart_no"):
                st.session_state.show_restart_warning = False
                st.rerun() 

# --- PANTALLA DE RESULTADOS (Sin cambios) ---
else:
    st.balloons()
    st.title("✅ ¡Test Completado! Aquí está tu Perfil de Personalidad")
    
    end_time = time.time()
    total_time = 0
    if abs(end_time - st.session_state.start_time) < 1:
        st.info("Resultado generado por la opción **Completar al Azar (Demo)**.")
    else:
        total_time = round((end_time - st.session_state.start_time) / 60, 2)
        st.info(f"Tiempo total para completar el test: **{total_time} minutos**.")

    # --- CÁLCULO DE RESULTADOS AMPLIADO ---
    puntajes_por_categoria = {cat: [] for cat in preguntas_test.keys()}
    for data in st.session_state.answers.values():
        puntajes_por_categoria[data['categoria']].append(data['puntaje'])

    total_puntaje_bruto = sum(item['puntaje'] for item in st.session_state.answers.values())
    
    # Calcular el Nivel General (a modo de ejemplo, basado en el promedio)
    porcentaje_global = round((total_puntaje_bruto / total_puntaje_maximo) * 100)
    if porcentaje_global >= 75: nivel_general = "**Alto**"
    elif porcentaje_global <= 40: nivel_general = "**Bajo**"
    else: nivel_general = "**Moderado**"


    resultados_finales = {}
    for categoria, puntajes in puntajes_por_categoria.items():
        total_preguntas_cat = len(preguntas_test[categoria])
        puntaje_max_cat = total_preguntas_cat * 4
        puntaje_obtenido = sum(puntajes)
        porcentaje = round((puntaje_obtenido / puntaje_max_cat) * 100)
        
        resultados_finales[categoria] = {
            'porcentaje': porcentaje,
            'obtenido': puntaje_obtenido,
            'maximo': puntaje_max_cat,
            'preguntas': total_preguntas_cat
        }

    # --- PUNTUACIONES FINALES ---
    st.markdown("---")
    st.header("🎯 Tus Puntajes Finales por Dimensión")
    st.markdown("""
    Tu perfil se basa en el modelo de los **Cinco Grandes Factores (Big Five)**, donde cada dimensión se puntúa de 0% (muy bajo) a 100% (muy alto).
    """)

    col_scores = st.columns(5)
    icon_map = {
        "Estabilidad Emocional": "🧘",
        "Extroversión": "🗣️",
        "Amabilidad": "🤝",
        "Responsabilidad": "✅",
        "Apertura a la Experiencia": "✨"
    }

    for i, (cat, data) in enumerate(resultados_finales.items()):
        with col_scores[i]:
            # Usamos una estructura HTML simple para la tarjeta del puntaje principal
            st.markdown(f"""
            <div class="score-card-native">
                <h3 style="margin-bottom: 5px; color: #3B82F6; font-size: 1.1em;">{icon_map.get(cat, '❓')} {cat}</h3>
                <p style="font-size: 2.5em; font-weight: bold; color: #1E3A8A; margin: 0;">{data['porcentaje']}%</p>
                <p style="font-size: 0.8em; color: #6B7280; font-weight: normal; margin-top: 10px;">
                    ({data['obtenido']} de {data['maximo']} puntos)
                </p>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("---")
    st.header("💡 Análisis Detallado de tu Perfil por Factor (Grilla)")
    st.markdown("Aquí se desglosa tu perfil, utilizando componentes nativos de Streamlit para una presentación estable y organizada.")

    # --- LÓGICA DE ANÁLISIS DETALLADO EN GRILLA ---
    
    # Creamos dos columnas persistentes para la grilla
    cols_analysis = st.columns(2)
    col_idx = 0
    
    for categoria, data in resultados_finales.items():
        porcentaje = data['porcentaje']
        puntaje_obtenido = data['obtenido']
        puntaje_maximo = data['maximo']
        
        nivel_descriptor, fortalezas_text, debilidades_text, oportunidades_text = interpretar_puntaje(categoria, porcentaje)
        
        # Rotamos entre las dos columnas
        with cols_analysis[col_idx % 2]:
            # Llamamos a la función con el descriptor corregido
            generar_analisis_componente(
                categoria, 
                porcentaje, 
                puntaje_obtenido, 
                puntaje_maximo, 
                nivel_descriptor, 
                fortalezas_text, 
                debilidades_text, 
                oportunidades_text
            )
            
        col_idx += 1
        
    # --- DESCARGA DE RESULTADOS ---
    st.markdown("---")
    with st.expander("📥 Descargar tus resultados detallados (Excel)"):
        # Preparar DataFrame de respuestas
        df_export = pd.DataFrame(list(st.session_state.answers.values()))
        
        # Preparar DataFrame de Resumen
        orden_categorias = list(preguntas_test.keys())
        resumen_data = {
            'Dimensión': orden_categorias,
            'Puntaje_Porcentaje': [resultados_finales[cat]['porcentaje'] for cat in orden_categorias],
            'Puntaje_Obtenido': [resultados_finales[cat]['obtenido'] for cat in orden_categorias],
            'Puntaje_Maximo': [resultados_finales[cat]['maximo'] for cat in orden_categorias]
        }
        df_resumen_final = pd.DataFrame(resumen_data)
        
        col_dl1, _ = st.columns([1, 2])
        with col_dl1:
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


# 4. FOOTER (Se muestra en todas las páginas)
if st.session_state.test_completed:
    display_footer("José Ignacio Taj-Taj", total_puntaje_bruto, total_puntaje_maximo, nivel_general)
else:
    display_footer("José Ignacio Taj-Taj", 0, total_puntaje_maximo, "No disponible")

