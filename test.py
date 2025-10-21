import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from collections import defaultdict
import time
import random

# --- 0. CONFIGURACIÓN INICIAL Y ESTÉTICA (¡AQUÍ ESTÁ EL CAMBIO PARA EL TEMA CLARO Y EL BOTÓN!) ---

st.set_page_config(
    layout="wide", 
    page_title="Test Big Five Detallado", 
    initial_sidebar_state="collapsed"
)

# CSS Personalizado para tema CLARO y amigable
st.markdown("""
<style>
    /* Forzar fondo blanco y texto oscuro */
    .stApp {
        background-color: #f0f2f6; /* Un color muy claro, casi blanco */
        color: #1c1e21; /* Texto oscuro */
    }
    /* Estilo para las tarjetas/contenedores */
    .st-emotion-cache-1r6r82b, .st-emotion-cache-139xi5s { /* Selector de contenedores y bloques de código */
        background-color: white !important;
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
        padding: 20px;
    }
    h1, h2, h3, .stMarkdown {
        color: #1c1e21;
    }
    /* Mejora del slider para que se vea más moderno */
    .stSlider > label {
        font-size: 1.1em;
        font-weight: 600;
        color: #2a688b;
    }
    
    /* ESTILO DE BOTONES: Aquí se corrige el problema del color del texto */
    .stButton>button {
        border-radius: 8px;
        padding: 10px 20px;
        font-weight: bold;
    }
    /* Botones primarios (azules): Forzar texto negro o muy oscuro para legibilidad */
    .stButton button[data-testid*="stButton-primary"] {
        color: #000000 !important; /* Texto negro */
        background-color: #81c784; /* Verde suave, como ejemplo amigable */
        border: 1px solid #66bb6a;
    }
    .stButton button[data-testid*="stButton-primary"]:hover {
        background-color: #66bb6a; /* Un tono más oscuro al pasar el mouse */
    }
</style>
""", unsafe_allow_html=True)

# --- 1. CONSTANTES Y DATOS DEL TEST ---

# Opciones de respuesta para el Likert Scale
LIKERT_OPTIONS = {
    5: "Totalmente de acuerdo",
    4: "De acuerdo",
    3: "Neutral",
    2: "En desacuerdo",
    1: "Totalmente en desacuerdo"
}
LIKERT_SCORES = list(LIKERT_OPTIONS.keys()) # [5, 4, 3, 2, 1]

# Etiquetas de los 5 grandes rasgos (OCEAN)
TRAIT_LABELS = {
    "O": "Apertura a la Experiencia",
    "C": "Concienzudo",
    "E": "Extraversión",
    "A": "Amabilidad",
    "N": "Neuroticismo"
}

# Definición de las 130 preguntas (26 por rasgo)
# Estructura: (ID, Texto, Rasgo (O, C, E, A, N), Inversa (True/False))
QUESTION_DATA = [
    # Extraversion (E) - 1 a 26
    (1, "Soy el alma de la fiesta.", "E", False),
    (2, "Me siento cómodo alrededor de otras personas.", "E", False),
    (3, "Empiezo las conversaciones.", "E", False),
    (4, "Hablo mucho con muchas personas diferentes en las fiestas.", "E", False),
    (5, "No me importa ser el centro de atención.", "E", False),
    (6, "No hablo mucho.", "E", True),
    (7, "Me mantengo en segundo plano.", "E", True),
    (8, "Tengo poco que decir.", "E", True),
    (9, "Soy reservado.", "E", True),
    (10, "Paso tiempo solo.", "E", True),
    (11, "Busco emoción y aventura.", "E", False),
    (12, "Disfruto con la compañía de la gente.", "E", False),
    (13, "Me expreso con facilidad.", "E", False),
    (14, "Soy una persona activa.", "E", False),
    (15, "Soy muy enérgico.", "E", False),
    (16, "A menudo me siento melancólico.", "E", True),
    (17, "Me deprimo fácilmente.", "E", True),
    (18, "Soy sociable.", "E", False),
    (19, "Soy una persona alegre.", "E", False),
    (20, "Hago amigos con facilidad.", "E", False),
    (21, "Me tomo las cosas con calma.", "E", True),
    (22, "Tiendo a ser callado.", "E", True),
    (23, "Disfruto de grandes multitudes.", "E", False),
    (24, "Soy tímido.", "E", True),
    (25, "Hago que otros se sientan incómodos.", "E", True),
    (26, "Me gusta el ruido y el alboroto.", "E", False),

    # Amabilidad (A) - 27 a 52
    (27, "Me intereso por los demás.", "A", False),
    (28, "Siento simpatía por los sentimientos de los demás.", "A", False),
    (29, "Tengo un corazón blando.", "A", False),
    (30, "Me tomo el tiempo para los demás.", "A", False),
    (31, "Hago que la gente se sienta a gusto.", "A", False),
    (32, "No me intereso por los problemas de los demás.", "A", True),
    (33, "Insulto a la gente.", "A", True),
    (34, "No me gusta la gente.", "A", True),
    (35, "Ignoro a la gente.", "A", True),
    (36, "Soy grosero con los demás.", "A", True),
    (37, "Sigo las reglas.", "A", False),
    (38, "Soy cooperativo.", "A", False),
    (39, "Soy amable con la gente.", "A", False),
    (40, "Soy cariñoso.", "A", False),
    (41, "Me llevo bien con la gente.", "A", False),
    (42, "No tengo tiempo para los demás.", "A", True),
    (43, "Soy frío con la gente.", "A", True),
    (44, "Confío en los demás.", "A", False),
    (45, "No tengo paciencia.", "A", True),
    (46, "Soy de mente abierta.", "A", False),
    (47, "Me gusta hacer daño a los demás.", "A", True),
    (48, "Me molesta la gente fácilmente.", "A", True),
    (49, "Soy una persona de buen humor.", "A", False),
    (50, "Muestro respeto.", "A", False),
    (51, "Juzgo a los demás.", "A", True),
    (52, "Soy considerado con los demás.", "A", False),

    # Concienzudo (C) - 53 a 78
    (53, "Estoy siempre preparado.", "C", False),
    (54, "Presto atención a los detalles.", "C", False),
    (55, "Hago mis tareas de inmediato.", "C", False),
    (56, "Me gusta el orden.", "C", False),
    (57, "Sigo un horario.", "C", False),
    (58, "Dejo mis pertenencias por ahí.", "C", True),
    (59, "Soy descuidado con mis cosas.", "C", True),
    (60, "Falto a mi deber.", "C", True),
    (61, "Soy desorganizado.", "C", True),
    (62, "Dejo las cosas sin terminar.", "C", True),
    (63, "Soy meticuloso.", "C", False),
    (64, "Soy eficiente.", "C", False),
    (65, "Planifico con anticipación.", "C", False),
    (66, "Soy fiable.", "C", False),
    (67, "Me distraigo fácilmente.", "C", True),
    (68, "Soy perezoso.", "C", True),
    (69, "Me concentro en la tarea.", "C", False),
    (70, "Soy persistente.", "C", False),
    (71, "Me esfuerzo por la excelencia.", "C", False),
    (72, "Me cuido.", "C", False),
    (73, "No soy sistemático.", "C", True),
    (74, "Trabajo duro.", "C", False),
    (75, "Soy irresponsable.", "C", True),
    (76, "Tengo buenas habilidades de gestión del tiempo.", "C", False),
    (77, "Soy impulsivo.", "C", True),
    (78, "Me gusta que todo esté limpio.", "C", False),

    # Neuroticismo (N) - 79 a 104
    (79, "Me altero fácilmente.", "N", False),
    (80, "Cambio de humor a menudo.", "N", False),
    (81, "Me preocupo por las cosas.", "N", False),
    (82, "Me irrito fácilmente.", "N", False),
    (83, "Tengo emociones inestables.", "N", False),
    (84, "Estoy relajado la mayor parte del tiempo.", "N", True),
    (85, "Raramente me siento azul.", "N", True),
    (86, "No me molesto fácilmente.", "N", True),
    (87, "Soy estable emocionalmente.", "N", True),
    (88, "Raramente me quejo.", "N", True),
    (89, "Me asusto fácilmente.", "N", False),
    (90, "Soy una persona tensa.", "N", False),
    (91, "Sufro de ansiedad.", "N", False),
    (92, "Me siento incómodo.", "N", False),
    (93, "Me siento triste.", "N", False),
    (94, "Puedo manejarme a mí mismo.", "N", True),
    (95, "Me siento seguro.", "N", True),
    (96, "Estoy tranquilo.", "N", True),
    (97, "Pienso en el suicidio.", "N", False),
    (98, "Estoy de mal humor.", "N", False),
    (99, "Soy autocrítico.", "N", False),
    (100, "Soy inseguro.", "N", False),
    (101, "Soy tranquilo bajo presión.", "N", True),
    (102, "Me siento inadecuado.", "N", False),
    (103, "Me abrumo fácilmente.", "N", False),
    (104, "Me enojo fácilmente.", "N", False),

    # Apertura a la Experiencia (O) - 105 a 130
    (105, "Tengo un vocabulario rico.", "O", False),
    (106, "Tengo una imaginación vívida.", "O", False),
    (107, "Tengo excelentes ideas.", "O", False),
    (108, "Soy rápido para entender las cosas.", "O", False),
    (109, "Uso palabras difíciles.", "O", False),
    (110, "No tengo buena imaginación.", "O", True),
    (111, "No me interesan las ideas abstractas.", "O", True),
    (112, "Tengo dificultades para entender las ideas.", "O", True),
    (113, "No soy artístico.", "O", True),
    (114, "Evito discusiones intelectuales.", "O", True),
    (115, "Me gusta la poesía.", "O", False),
    (116, "Disfruto de la belleza.", "O", False),
    (117, "Me gusta visitar museos de arte.", "O", False),
    (118, "Me interesan los problemas filosóficos.", "O", False),
    (119, "Me gusta el arte.", "O", False),
    (120, "Me intereso por el simbolismo.", "O", False),
    (121, "Disfruto con la variedad.", "O", False),
    (122, "No me gusta el cambio.", "O", True),
    (123, "No me gusta la rutina.", "O", False),
    (124, "Disfruto con actividades nuevas.", "O", False),
    (125, "Soy tradicionalista.", "O", True),
    (126, "Me gusta la rutina.", "O", True),
    (127, "Prefiero lo familiar.", "O", True),
    (128, "Soy curioso.", "O", False),
    (129, "Soy inteligente.", "O", False),
    (130, "Me gusta resolver problemas complejos.", "O", False),
]

# Ajuste de las variables de paginación
QUESTIONS_PER_PAGE = 10 
TOTAL_QUESTIONS = len(QUESTION_DATA) 
TOTAL_PAGES = (TOTAL_QUESTIONS + QUESTIONS_PER_PAGE - 1) // QUESTIONS_PER_PAGE # 130/10 = 13

# --- 2. FUNCIONES DE LÓGICA DEL TEST ---

def restart_test():
    """Reinicia el estado de la sesión para volver a empezar."""
    st.session_state['page'] = 0
    st.session_state['answers'] = {}
    st.session_state['name'] = ""
    st.session_state['email'] = ""
    # Uso de st.rerun() en lugar de la función obsoleta
    st.rerun() 

def next_page():
    """Avanza a la siguiente página."""
    st.session_state['page'] += 1
    # Asegurar que la vista suba al principio de la nueva página
    scroll_to_top()
    # Uso de st.rerun() en lugar de la función obsoleta
    st.rerun() 

def prev_page():
    """Retrocede a la página anterior."""
    if st.session_state['page'] > 1:
        st.session_state['page'] -= 1
        scroll_to_top()
        # Uso de st.rerun() en lugar de la función obsoleta
        st.rerun() 

def scroll_to_top():
    """Fuerza que la vista de la página suba al inicio."""
    st.markdown("""
        <script>
            window.scrollTo(0, 0);
        </script>
        """, unsafe_allow_html=True)

def calculate_results():
    """Calcula las puntuaciones finales de los 5 rasgos (escaladas de 0 a 100)."""
    results = defaultdict(lambda: {"score": 0, "count": 0})
    
    # Crear un mapeo rápido de Q_ID a datos para eficiencia
    q_map = {q[0]: (q[2], q[3]) for q in QUESTION_DATA}

    for q_id, answer in st.session_state['answers'].items():
        q_data = q_map.get(q_id)
        
        if q_data:
            trait, reverse = q_data
            
            # Aplicar la inversión de puntaje (escala 1-5)
            score = answer
            if reverse:
                score = 6 - answer 
            
            results[trait]["score"] += score
            results[trait]["count"] += 1

    # Calcular el puntaje promedio (escala 1-5)
    raw_scores = {
        trait: (data["score"] / data["count"]) if data["count"] > 0 else 0
        for trait, data in results.items()
    }
    
    # Escalar la puntuación promedio (1.0 a 5.0) a un porcentaje (0 a 100)
    # Fórmula: ((Puntuación_Obtenida - Min_Escala) / (Max_Escala - Min_Escala)) * 100
    final_scores = {
        trait: ((raw_score - 1) / 4) * 100 if raw_score > 0 else 0
        for trait, raw_score in raw_scores.items()
    }
    
    return {k: min(round(v), 100) for k, v in final_scores.items()}

# --- 3. PÁGINAS DE LA APLICACIÓN ---

def display_start_page():
    """Página de bienvenida y recolección de datos."""
    st.title("🌟 Test Detallado de los 5 Grandes Rasgos (Big Five)")
    st.subheader("¡Descubre tu Perfil de Personalidad!")
    
    st.markdown("""
    Este es un test psicológico basado en el modelo de los **Cinco Grandes Factores** (OCEAN). 
    Responde honestamente a cada afirmación usando la escala deslizante de **Totalmente en desacuerdo (1)** a **Totalmente de acuerdo (5)**. 
    Tu participación es anónima (a menos que proporciones tu email) y te ayudará a obtener un perfil de personalidad detallado y amigable.
    """)

    # Campos de entrada
    st.markdown("---")
    
    with st.container():
        st.subheader("Antes de empezar...")
        
        name = st.text_input("Tu Nombre (Opcional)", value=st.session_state['name'], max_chars=50)
        email = st.text_input("Tu Email (Opcional, para recibir resultados)", value=st.session_state['email'], max_chars=100)

        # Actualizar el estado de la sesión
        st.session_state['name'] = name
        st.session_state['email'] = email
    
    st.markdown("---")
    if st.button("Comenzar Test", type="primary", use_container_width=True):
        # Permite empezar sin datos
        next_page()


def display_test_page(page_index):
    """Muestra las preguntas para una página específica."""
    
    start_q_index = page_index * QUESTIONS_PER_PAGE
    end_q_index = min(start_q_index + QUESTIONS_PER_PAGE, TOTAL_QUESTIONS)
    questions_for_page = QUESTION_DATA[start_q_index:end_q_index]

    current_page = page_index + 1
    
    st.header(f"Página {current_page} de {TOTAL_PAGES} | Big Five Test")
    
    # Progreso de la prueba
    answered_count = len(st.session_state['answers'])
    st.markdown(f"**Progreso:** **{answered_count}** de **{TOTAL_QUESTIONS}** preguntas completadas")
    st.markdown("---")

    for i, q_data in enumerate(questions_for_page):
        q_id, q_text, q_trait, q_reverse = q_data

        # Determinar el valor actual o el valor por defecto (3 = Neutral)
        current_value = st.session_state['answers'].get(q_id, 3) 

        # Asegurar que st.slider reciba min_value y max_value explícitos.
        response = st.slider(
            label=f"**{q_id}.** {q_text}", # Usar q_id como número de pregunta
            min_value=1,       
            max_value=5,       
            value=current_value, 
            step=1,
            format="%d - %s",
            key=f"q_{q_id}",
            help=f"Rasgo: {TRAIT_LABELS[q_trait]} ({'Inversa' if q_reverse else 'Directa'})"
        )
        
        # Guardar la respuesta
        st.session_state['answers'][q_id] = response
        
        # Mostrar el significado de la respuesta seleccionada
        selected_description = LIKERT_OPTIONS.get(response, "Selecciona una opción")
        st.markdown(f"> **Tu respuesta:** *{selected_description}*")
        
        if i < len(questions_for_page) - 1:
            st.markdown("---")

    st.markdown("---")
    
    # Controles de navegación
    col_prev, col_next = st.columns([1, 1])

    with col_prev:
        if page_index > 0:
            st.button("↩️ Anterior", on_click=prev_page, type="secondary", use_container_width=True)

    with col_next:
        if current_page < TOTAL_PAGES:
            st.button("Siguiente ➡️", on_click=next_page, type="primary", use_container_width=True)
        else:
            # Solo muestra el botón de resultados si todas las preguntas han sido respondidas
            is_complete = len(st.session_state['answers']) == TOTAL_QUESTIONS
            
            if is_complete:
                if st.button("Ver Resultados ✨", on_click=next_page, type="primary", use_container_width=True):
                    pass # La navegación se maneja en next_page()

            elif st.button("Ver Resultados (Incompleto) ⚠️", on_click=next_page, type="secondary", use_container_width=True):
                # Permite al usuario ver resultados incompletos si lo desea
                pass


def display_results_page(scores):
    """Muestra la página de resultados con el gráfico de radar y la interpretación."""
    st.title(f"🎉 ¡{st.session_state['name'] if st.session_state['name'] else 'Tu'} Perfil de Personalidad está Listo!")
    st.subheader("Tu Patrón Único de los 5 Grandes Rasgos")

    # Muestra globos de confeti (detalles amigables)
    st.balloons()

    st.markdown("---")

    # 1. Gráfico de Radar
    traits = list(TRAIT_LABELS.values())
    scores_list = list(scores.values())

    fig = go.Figure(data=[
        go.Scatterpolar(
            r=scores_list + scores_list[:1], # Cierra el ciclo
            theta=traits + traits[:1],
            fill='toself',
            name='Tu Perfil',
            marker=dict(color='#2a688b'),
            line_color='#2a688b',
            opacity=0.8
        )
    ])

    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100],
                tickvals=[20, 40, 60, 80, 100],
                ticktext=['Bajo', 'Medio-Bajo', 'Medio', 'Medio-Alto', 'Alto'],
            ),
            bgcolor="#f8f9fa" # Fondo más claro para el gráfico
        ),
        showlegend=False,
        height=500,
        title='Gráfico de Patrón de Personalidad (Puntuación sobre 100)',
    )

    st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")
    
    # 2. Resumen por Rasgo (Interpretación)
    st.header("Análisis Detallado de tus Rasgos")
    
    # Interpretaciones detalladas basadas en el nivel (Baja, Media, Alta)
    INTERPRETATION_DATA = {
        "O": {
            "name": "Apertura a la Experiencia (O)",
            "Alta": "Eres extremadamente creativo, tienes una curiosidad intelectual insaciable y disfrutas de la variedad, el arte y las ideas abstractas. Tiendes a ser poco convencional.",
            "Media": "Eres flexible y abierto a nuevas ideas, pero valoras también la experiencia y la practicidad. Disfrutas de un equilibrio entre lo familiar y lo novedoso.",
            "Baja": "Prefieres la rutina, la estabilidad y lo conocido. Tiendes a ser más pragmático, evitas las ideas abstractas o el arte complejo y te sientes cómodo con las tradiciones."
        },
        "C": {
            "name": "Concienzudo (C)",
            "Alta": "Eres altamente organizado, responsable, autodisciplinado y orientado a objetivos. Tiendes a planificar con anticipación, eres confiable y perfeccionista.",
            "Media": "Muestras disciplina en áreas importantes, pero puedes ser flexible en otras. Eres generalmente responsable, pero permites cierta espontaneidad o desorden controlado.",
            "Baja": "Eres más espontáneo, menos estructurado y tiendes a ser más flexible o desorganizado. Puedes tener dificultades con la gestión del tiempo y la persistencia en tareas aburridas."
        },
        "E": {
            "name": "Extraversión (E)",
            "Alta": "Eres sociable, asertivo, hablas mucho y te energizas con la interacción social. Eres el alma de la fiesta y tiendes a ser optimista y activo.",
            "Media": "Disfrutas de las interacciones sociales, pero también valoras tu tiempo a solas. Puedes ser sociable en grupos pequeños y reservado en grandes multitudes.",
            "Baja": "Eres reservado, reflexivo y prefieres la soledad o el trato con un círculo íntimo. Las grandes multitudes y la estimulación excesiva te agotan."
        },
        "A": {
            "name": "Amabilidad (A)",
            "Alta": "Eres muy compasivo, cooperativo, confiado, bondadoso y siempre dispuesto a ayudar. Valoras la armonía y evitas la confrontación.",
            "Media": "Eres generalmente amable y considerado, pero puedes defender tus intereses si es necesario. Eres selectivo en tu confianza y cooperación.",
            "Baja": "Tiendes a ser más escéptico, competitivo o crítico. Te centras en tus propios intereses y no dudas en expresar tu opinión, incluso si es dura."
        },
        "N": {
            "name": "Neuroticismo (N)",
            "Alta": "Tiendes a experimentar emociones negativas (ansiedad, preocupación, ira) con frecuencia e intensidad. Eres vulnerable al estrés y a los cambios de humor.",
            "Media": "Experimentas altibajos emocionales típicos, manejas el estrés razonablemente, pero puedes reaccionar con preocupación en situaciones desafiantes.",
            "Baja": "Eres emocionalmente estable, tranquilo, resiliente y capaz de manejar el estrés sin alterarte. Raramente te sientes ansioso o deprimido."
        }
    }

    for trait_key, score in scores.items():
        data = INTERPRETATION_DATA.get(trait_key, {"name": "Rasgo Desconocido", "Alta": "No hay datos."})
        
        # Determinar el nivel para la interpretación y el color
        level_key = "Baja" if score < 40 else ("Media" if score < 60 else "Alta")
        color = "#e57373" if level_key == "Baja" else ("#ffb74d" if level_key == "Media" else "#81c784")
        interpretation = data[level_key]
        trait_name = data["name"]

        st.markdown(f"""
        <div style="background-color: {color}; padding: 10px 15px; border-radius: 8px; color: white; margin-bottom: 5px;">
            <h3 style="color: white; margin: 0; padding: 0;">{trait_name}: Nivel {level_key} ({score}%)</h3>
        </div>
        <p style="margin-top: 5px; margin-bottom: 20px;">{interpretation}</p>
        """, unsafe_allow_html=True)


    # Botón de reinicio
    st.markdown("---")
    st.button("Volver a Empezar Test", on_click=restart_test, type="secondary", use_container_width=True)


# --- 4. LÓGICA PRINCIPAL DE LA APLICACIÓN ---

def main_app():
    """Maneja el flujo de navegación de la aplicación."""
    
    # Inicialización del estado de la sesión
    if 'page' not in st.session_state:
        st.session_state['page'] = 0
    if 'answers' not in st.session_state:
        st.session_state['answers'] = {}
    if 'name' not in st.session_state:
        st.session_state['name'] = ""
    if 'email' not in st.session_state:
        st.session_state['email'] = ""

    current_page = st.session_state['page']
    
    if current_page == 0:
        display_start_page()
    elif 1 <= current_page <= TOTAL_PAGES:
        # Se muestra la página actual del test (current_page es el índice + 1)
        display_test_page(current_page - 1)
    elif current_page == TOTAL_PAGES + 1:
        # Página de resultados
        scores = calculate_results()
        display_results_page(scores)
    else:
        # En caso de un estado de página inválido, volvemos a la pantalla de inicio
        restart_test()

if __name__ == '__main__':
    # Streamlit por defecto busca una función llamada 'main' o ejecuta el código a nivel superior
    # Aquí nos aseguramos de llamar a nuestra función principal
    main_app()

