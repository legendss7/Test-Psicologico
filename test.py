import streamlit as st
import pandas as pd
import time
from io import BytesIO

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

        /* Tarjetas de resultados */
        .result-card {
            background-color: white;
            border-radius: 15px;
            padding: 25px;
            margin-bottom: 20px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            border-left: 5px solid #1E3A8A;
        }
        .result-card h3 {
            margin-top: 0;
            color: #1E3A8A;
        }

    </style>
    """, unsafe_allow_html=True)

# --- FUNCIONES AUXILIARES ---

# Función MAXIMAMENTE FORZADA para el scroll al top
def forzar_scroll_al_top(idx):
    # Se inyecta el índice (idx) en el script para forzar a Streamlit a considerarlo
    # un componente único y re-renderizarlo, ejecutando el JavaScript de nuevo.
    js_code = f"""
        <script>
            // Pregunta única para forzar render: {idx}
            setTimeout(function() {{
                // 1. Scroll en la ventana principal (más genérico)
                window.parent.scrollTo({{ top: 0, behavior: 'auto' }});
                
                // 2. Scroll en el body de la ventana principal
                window.parent.document.body.scrollTo({{ top: 0, behavior: 'auto' }});
                
                // 3. Intenta encontrar y scroll en el contenedor principal de Streamlit
                var mainContent = window.parent.document.querySelector('[data-testid="stAppViewContainer"]');
                if (mainContent) {{
                    mainContent.scrollTo({{ top: 0, behavior: 'auto' }});
                }}
            }}, 50); // Retardo de 50 milisegundos para asegurar el renderizado completo
        </script>
        """
    # El key es opcional aquí, pero el contenido único de js_code es lo que realmente lo fuerza
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

# Función para reiniciar el test
def reiniciar_test():
    st.session_state.current_question = 0
    st.session_state.answers = {}
    st.session_state.test_started = False
    st.session_state.test_completed = False
    st.session_state.start_time = 0
    # Restablecer la bandera de scroll
    st.session_state.should_scroll = False
    st.rerun()

# Función para convertir DataFrame a Excel
@st.cache_data
def to_excel(df):
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Resultados')
    processed_data = output.getvalue()
    return processed_data

# --- LÓGICA DE LA APLICACIÓN ---

# Cargar estilos y estado
cargar_css()
inicializar_estado()

idx = st.session_state.current_question

# EJECUCIÓN CONDICIONAL DEL SCROLL (AL INICIO DEL RENDERIZADO)
# Se pasa el índice para forzar el re-renderizado del script de scroll.
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
    
    if st.button("🚀 Comenzar el Test", key="start_button"):
        st.session_state.test_started = True
        st.session_state.start_time = time.time()
        st.rerun()

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
    col1, col2, col3 = st.columns([1, 2, 1])

    with col1:
        if idx > 0:
            if st.button("⬅️ Anterior"):
                st.session_state.current_question -= 1
                st.session_state.should_scroll = True # Establece la bandera de scroll
                st.rerun()

    with col3:
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

    # --- INTERPRETACIÓN DE RESULTADOS ---
    def interpretar_puntaje(categoria, puntaje):
        fortalezas, debilidades, oportunidades = "", "", ""

        # Lógica de interpretación simple (se puede expandir)
        if puntaje >= 75:
            fortalezas = f"**{categoria}:** Tu alto puntaje ({puntaje}%) sugiere que esta es una de tus grandes fortalezas. Eres una persona que..."
        elif puntaje <= 40:
            debilidades = f"**{categoria}:** Tu puntaje ({puntaje}%) indica que esta puede ser un área desafiante para ti. Podrías encontrar dificultades en..."
        else:
            oportunidades = f"**{categoria}:** Tu puntaje ({puntaje}%) se encuentra en un rango intermedio. Tienes una base sólida, pero hay espacio para crecer en..."

        # Textos específicos por categoría
        if categoria == "Estabilidad Emocional":
            if puntaje >= 75: fortalezas += " manejas el estrés con calma, eres resiliente y mantienes un equilibrio emocional admirable."
            elif puntaje <= 40: debilidades += " manejar la ansiedad, el estrés o mantener la calma bajo presión."
            else: oportunidades += " desarrollar aún más tu resiliencia y manejo del estrés para afrontar desafíos con mayor serenidad."
        
        elif categoria == "Extroversión":
            if puntaje >= 75: fortalezas += " disfrutas de la interacción social, te sientes energizado/a por la compañía de otros y eres comunicativo/a."
            elif puntaje <= 40: debilidades += " sentirte cómodo/a en grandes grupos sociales o al iniciar conversaciones."
            else: oportunidades += " explorar nuevas situaciones sociales para aumentar tu confianza y ampliar tu círculo de confort."

        elif categoria == "Amabilidad":
            if puntaje >= 75: fortalezas += " eres empático/a, cooperativo/a y te preocupas genuinamente por el bienestar de los demás."
            elif puntaje <= 40: debilidades += " priorizar las necesidades de los demás o confiar en las intenciones de la gente."
            else: oportunidades += " practicar la empatía y la escucha activa para fortalecer tus relaciones interpersonales."

        elif categoria == "Responsabilidad":
            if puntaje >= 75: fortalezas += " eres una persona organizada, disciplinada y fiable. Cumples tus compromisos con diligencia."
            elif puntaje <= 40: debilidades += " la organización, la planificación a largo plazo o la autodisciplina."
            else: oportunidades += " establecer metas más claras y sistemas de organización para mejorar tu eficacia y fiabilidad."

        elif categoria == "Apertura a la Experiencia":
            if puntaje >= 75: fortalezas += " eres curioso/a, creativo/a y estás abierto/a a nuevas ideas y experiencias. Disfrutas de la novedad."
            elif puntaje <= 40: debilidades += " salir de tu zona de confort, adaptarte a los cambios o disfrutar de lo abstracto."
            else: oportunidades += " exponerte a nuevas actividades, culturas o ideas para expandir tus horizontes y fomentar tu creatividad."

        return fortalezas, debilidades, oportunidades

    st.markdown("---")
    st.header("📊 Resumen Gráfico de tu Personalidad")
    
    # Crear un DataFrame para el gráfico
    df_resultados = pd.DataFrame(list(resultados_finales.items()), columns=['Dimensión', 'Puntaje (%)'])
    st.bar_chart(df_resultados.set_index('Dimensión'))

    st.markdown("---")
    st.header("💡 Análisis Detallado de tu Perfil")

    fortalezas_list, debilidades_list, oportunidades_list = [], [], []
    for cat, score in resultados_finales.items():
        f, d, o = interpretar_puntaje(cat, score)
        if f: fortalezas_list.append(f)
        if d: debilidades_list.append(d)
        if o: oportunidades_list.append(o)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown('<div class="result-card"><h3>🌟 Fortalezas</h3></div>', unsafe_allow_html=True)
        for item in fortalezas_list:
            st.markdown(f"- {item}")
    
    with col2:
        st.markdown('<div class="result-card"><h3>⚠️ Debilidades</h3></div>', unsafe_allow_html=True)
        for item in debilidades_list:
            st.markdown(f"- {item}")

    with col3:
        st.markdown('<div class="result-card"><h3>🌱 Áreas de Oportunidad</h3></div>', unsafe_allow_html=True)
        for item in oportunidades_list:
            st.markdown(f"- {item}")
            
    st.markdown("---")
    
    # --- DESCARGA DE RESULTADOS ---
    with st.expander("📥 Descargar tus respuestas y resultados"):
        # Preparar DataFrame para descarga
        df_export = pd.DataFrame(list(st.session_state.answers.values()))
        st.dataframe(df_export)
        
        col_dl1, col_dl2 = st.columns(2)
        with col_dl1:
            csv = df_export.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="Descargar como CSV",
                data=csv,
                file_name='mis_resultados_test.csv',
                mime='text/csv',
            )
        with col_dl2:
            excel_data = to_excel(df_export)
            st.download_button(
                label="Descargar como Excel",
                data=excel_data,
                file_name='mis_resultados_test.xlsx',
                mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            )

    # --- REINICIAR TEST ---
    st.markdown("---")
    if st.button("🔄 Realizar el test de nuevo"):
        reiniciar_test()
