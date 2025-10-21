import streamlit as st

# --- 1. CONFIGURACIÓN DEL TEST (BIG FIVE - OCEAN) ---
# O: Openness (Apertura a la Experiencia)
# C: Conscientiousness (Responsabilidad)
# E: Extraversion (Extraversión)
# A: Agreeableness (Amabilidad)
# N: Neuroticism (Neuroticismo / Estabilidad Emocional - N-score alto = Inestable)

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
    "O": "Apertura a la Experiencia (O)",
    "C": "Responsabilidad (C)",
    "E": "Extraversión (E)",
    "A": "Amabilidad (A)",
    "N": "Neuroticismo (N)"
}

# --- 2. LÓGICA DE PUNTUACIÓN Y PERFIL ---

def calculate_score(answers):
    """Calcula la puntuación para cada rasgo de personalidad."""
    scores = {"O": 0, "C": 0, "E": 0, "A": 0, "N": 0}
    
    for q in QUESTIONS:
        q_id = q["id"]
        trait = q["trait"]
        is_reverse = q["reverse"]
        
        # Obtener la respuesta del estado de la sesión
        response = answers.get(q_id)
        
        if response is not None:
            score = response
            
            # Aplicar puntuación inversa si es necesario
            if is_reverse:
                # 1 -> 5, 2 -> 4, 3 -> 3, 4 -> 2, 5 -> 1
                score = 6 - score
            
            scores[trait] += score
            
    return scores

def interpret_score(score, trait):
    """Interpreta la puntuación (Bajo, Medio, Alto) y devuelve el texto del perfil."""
    # Min Score: 6 (6 preguntas * 1 punto)
    # Max Score: 30 (6 preguntas * 5 puntos)
    # Rango: 24
    
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
    
    return profiles[trait][level], level

# --- 3. CONFIGURACIÓN VISUAL Y DE INTERFAZ ---

def set_professional_style():
    """Aplica estilos CSS para una apariencia profesional."""
    st.markdown("""
    <style>
        /* Fuente y Estilo General */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
        html, body, [class*="st-"] {
            font-family: 'Inter', sans-serif;
        }
        
        /* Contenedor Principal */
        .main {
            background-color: #f7f9fc; /* Gris muy claro */
            padding: 2rem;
            border-radius: 12px;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
        }
        
        /* Títulos y Encabezados */
        h1 {
            color: #1e3a8a; /* Azul oscuro corporativo */
            border-bottom: 3px solid #3b82f6; /* Azul brillante */
            padding-bottom: 0.5rem;
            margin-bottom: 1.5rem;
            font-weight: 700;
        }
        h2 {
            color: #3b82f6;
            font-weight: 600;
            margin-top: 2rem;
        }
        
        /* Estilo de las Preguntas (Controles) */
        .stRadio > label {
            font-size: 1.05rem;
            font-weight: 500;
            color: #1f2937;
            margin-bottom: 10px;
            padding: 8px 0;
            display: block;
            border-left: 5px solid #e5e7eb;
            padding-left: 15px;
        }
        .stRadio div[role="radiogroup"] {
            display: flex;
            flex-direction: row; /* Poner opciones en fila */
            gap: 15px;
            padding-bottom: 15px;
            border-bottom: 1px dashed #e5e7eb;
            margin-bottom: 20px;
        }
        
        /* Botones */
        .stButton>button {
            background-color: #3b82f6;
            color: white;
            font-weight: 600;
            padding: 10px 20px;
            border-radius: 8px;
            border: none;
            transition: background-color 0.3s;
        }
        .stButton>button:hover {
            background-color: #1e3a8a;
        }

        /* Estilo del Perfil Final */
        .profile-container {
            background-color: #ffffff;
            border: 2px solid #3b82f6;
            border-radius: 10px;
            padding: 20px;
            margin-top: 30px;
            box-shadow: 0 8px 16px rgba(59, 130, 246, 0.15);
        }
        .trait-result {
            margin-bottom: 15px;
            padding: 10px;
            border-left: 5px solid #1e3a8a;
            background-color: #f0f7ff;
            border-radius: 4px;
        }
    </style>
    """, unsafe_allow_html=True)

# --- 4. FLUJO DE LA APLICACIÓN STREAMLIT ---

def run_test():
    """Función principal para correr la aplicación."""
    
    set_professional_style()
    st.title("Test de Personalidad - El Modelo de los Cinco Grandes (OCEAN)")
    st.markdown("""
        Este cuestionario consta de 30 preguntas diseñadas para evaluar tu perfil de personalidad
        en cinco dimensiones principales: Apertura, Responsabilidad, Extraversión, Amabilidad y Neuroticismo.
        Selecciona la opción que mejor describa tu acuerdo o desacuerdo con cada afirmación.
        **No hay respuestas correctas o incorrectas, solo tu perspectiva.**
    """)
    
    # Inicializar el estado de la sesión si es la primera vez
    if 'answers' not in st.session_state:
        st.session_state.answers = {}
    if 'test_completed' not in st.session_state:
        st.session_state.test_completed = False
        
    # Crear una lista de opciones con el formato (Etiqueta, Valor)
    # Streamlit usa el valor para el callback, lo que facilita el cálculo.
    likert_options_tuple = [(v, k) for k, v in LIKERT_OPTIONS.items()]

    # Dividir las 30 preguntas en 5 pestañas de 6 preguntas cada una
    tabs = st.tabs([f"Bloque {i+1} ({i*6 + 1}-{i*6 + 6})" for i in range(5)])
    
    # Usar un formulario para agrupar las preguntas y el botón de enviar
    with st.form(key='personality_test_form'):
        
        for i, tab in enumerate(tabs):
            with tab:
                st.markdown(f"## Bloque {i+1}: Sentimientos, Acciones y Pensamientos")
                
                # Cargar 6 preguntas por tab
                start_index = i * 6
                end_index = start_index + 6
                current_questions = QUESTIONS[start_index:end_index]

                for q in current_questions:
                    # El widget radio devuelve el 'value' (1 a 5)
                    response = st.radio(
                        label=f"{q['id']}. {q['text']}",
                        options=likert_options_tuple,
                        key=q['id'],
                        index=None if q['id'] not in st.session_state.answers else likert_options_tuple.index((LIKERT_OPTIONS[st.session_state.answers[q['id']]], st.session_state.answers[q['id']])),
                        format_func=lambda x: x[0] # Muestra solo la etiqueta (Totalmente de acuerdo)
                    )
                    
                    # Almacenar la respuesta (solo el valor numérico) en el estado de la sesión
                    if response is not None:
                        st.session_state.answers[q['id']] = response[1] # response[1] es el valor numérico (1-5)

        st.markdown("---")
        submit_button = st.form_submit_button(label='Finalizar Test y Ver Mi Perfil')

    # --- Lógica de procesamiento al presionar el botón ---
    if submit_button or st.session_state.test_completed:
        # Verificar que todas las preguntas estén respondidas
        if len(st.session_state.answers) < len(QUESTIONS):
            st.warning("¡Alto ahí! Por favor, responde las 30 preguntas antes de finalizar el test.")
            st.session_state.test_completed = False
            return # Detener la ejecución para forzar la respuesta
        
        st.session_state.test_completed = True
        
        # 5. Calcular la puntuación
        scores = calculate_score(st.session_state.answers)
        
        # 6. Mostrar el Perfil
        st.markdown(
            f"""
            <div class="profile-container">
                <h2>✅ Perfil de Personalidad Completado</h2>
                <p>Tu análisis está basado en el **Modelo de los Cinco Grandes (OCEAN)**.
                A continuación, se detalla tu puntuación en cada rasgo y su interpretación.</p>
            </div>
            """, 
            unsafe_allow_html=True
        )

        for trait_code, score in scores.items():
            profile_text, level = interpret_score(score, trait_code)
            trait_label = TRAIT_LABELS[trait_code]
            
            # Normalizar score para la barra de progreso (0 a 1.0)
            # Rango es de 6 a 30. Convertir a 0 a 100%.
            normalized_score = (score - 6) / 24
            
            # Usar HTML para mostrar la puntuación y la barra de forma elegante
            st.markdown(f"<h3>{trait_label} ({level})</h3>", unsafe_allow_html=True)
            
            col1, col2 = st.columns([0.2, 0.8])
            with col1:
                # Mostrar el score numérico
                st.metric(label="Puntuación", value=f"{score}/30", delta=level, delta_color="off")
            
            with col2:
                # Mostrar la barra de progreso
                st.progress(normalized_score)
                # Mostrar la descripción del perfil
                st.markdown(
                    f"""
                    <div class="trait-result">
                        {profile_text}
                    </div>
                    """, 
                    unsafe_allow_html=True
                )
        
        # 7. Conclusión y recomendación
        st.markdown("---")
        st.success("""
            **¡Felicidades!** Has completado tu Test de Perfil. 
            Esta información puede ser valiosa para el autoconocimiento y el desarrollo profesional. 
            Recuerda que la personalidad es dinámica y estos resultados son una fotografía de tu estado actual.
        """)
        
# Ejecutar la aplicación
if __name__ == '__main__':
    run_test()