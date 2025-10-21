import streamlit as st
from collections import defaultdict
import pandas as pd
import math

def scroll_to_top():
    """
    Fuerza el scroll a la parte superior usando múltiples métodos.
    """
    st.markdown(
        """
        <script>
        setTimeout(function() {
            // Método 1: Contenedor principal de Streamlit
            const mainContent = document.querySelector('[data-testid="stAppViewBlock"]');
            if (mainContent) {
                mainContent.scrollTop = 0;
            }
            
            // Método 2: Elemento main
            const main = document.querySelector('.main');
            if (main) {
                main.scrollTop = 0;
            }

            // Método 3: Ventana y documento
            window.scrollTo(0, 0);
            document.documentElement.scrollTop = 0;
            document.body.scrollTop = 0;

            // Método 4: Forzar scroll incluso si hay iframes
            const scrollToTop = function() {
                window.scrollTo(0, 0);
                document.documentElement.scrollTo(0, 0);
                document.body.scrollTo(0, 0);
            };
            scrollToTop();
            
        }, 100);
        </script>
        """,
        unsafe_allow_html=True
    )

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(
    layout="wide", 
    page_title="Test Big Five Detallado", 
    initial_sidebar_state="expanded"
)

# --- 1. CONFIGURACIÓN DEL TEST (BIG FIVE - OCEAN) ---

# Opciones de respuesta para el Likert Scale
LIKERT_OPTIONS = {
    5: "Totalmente de acuerdo",
    4: "De acuerdo", 
    3: "Neutral",
    2: "En desacuerdo",
    1: "Totalmente en desacuerdo"
}

LIKERT_SCORES = list(LIKERT_OPTIONS.keys())

# Preguntas del test (reducidas para el ejemplo)
QUESTIONS = [
    # O - Apertura a la Experiencia (Openness)
    {"id": "O1", "text": "Disfruto profundamente con la exploración de ideas abstractas.", "trait": "O", "reverse": False},
    {"id": "O2", "text": "Tengo una imaginación muy vívida y disfruto soñando despierto.", "trait": "O", "reverse": False},
    {"id": "O3", "text": "Suelo probar comidas nuevas y explorar culturas diferentes.", "trait": "O", "reverse": False},
    {"id": "O4", "text": "Prefiero seguir métodos tradicionales y probados.", "trait": "O", "reverse": True},
    
    # C - Responsabilidad (Conscientiousness)
    {"id": "C1", "text": "Siempre me preparo meticulosamente con antelación.", "trait": "C", "reverse": False},
    {"id": "C2", "text": "Soy muy metódico, organizado y ordenado.", "trait": "C", "reverse": False},
    {"id": "C3", "text": "A menudo me olvido de mis deberes y responsabilidades importantes.", "trait": "C", "reverse": True},
    {"id": "C4", "text": "Trabajo con diligencia hasta completar cualquier tarea que comience.", "trait": "C", "reverse": False},
    
    # E - Extraversión (Extraversion)
    {"id": "E1", "text": "Soy el alma de la fiesta y busco el centro de atención.", "trait": "E", "reverse": False},
    {"id": "E2", "text": "Me gusta tener mucha gente a mi alrededor la mayor parte del tiempo.", "trait": "E", "reverse": False},
    {"id": "E3", "text": "Soy bastante reservado y tiendo a quedarme en un segundo plano.", "trait": "E", "reverse": True},
    {"id": "E4", "text": "Cuando estoy en un grupo, tiendo a ser el que más habla.", "trait": "E", "reverse": False},
    
    # A - Amabilidad (Agreeableness)
    {"id": "A1", "text": "Siento una profunda empatía y compasión por los demás.", "trait": "A", "reverse": False},
    {"id": "A2", "text": "Generalmente confío en las buenas intenciones de la gente.", "trait": "A", "reverse": False},
    {"id": "A3", "text": "Pienso que la mayoría de la gente intenta aprovecharse de los demás.", "trait": "A", "reverse": True},
    {"id": "A4", "text": "Evito las discusiones y prefiero buscar el consenso rápidamente.", "trait": "A", "reverse": False},
    
    # N - Neuroticismo (Neuroticism)
    {"id": "N1", "text": "Me preocupo a menudo por cosas pequeñas o insignificantes.", "trait": "N", "reverse": False},
    {"id": "N2", "text": "A veces me siento deprimido, melancólico o infeliz.", "trait": "N", "reverse": False},
    {"id": "N3", "text": "Tienden a estresarme las situaciones inesperadas o difíciles.", "trait": "N", "reverse": False},
    {"id": "N4", "text": "Soy una persona muy relajada y rara vez me siento ansioso.", "trait": "N", "reverse": True},
]

# Parámetros del Test
TOTAL_QUESTIONS = len(QUESTIONS)
QUESTIONS_PER_PAGE = 5
TOTAL_PAGES = math.ceil(TOTAL_QUESTIONS / QUESTIONS_PER_PAGE)
ITEMS_PER_TRAIT = 4
MAX_SCORE_PER_TRAIT = ITEMS_PER_TRAIT * 5
MIN_SCORE_PER_TRAIT = ITEMS_PER_TRAIT * 1

# Etiquetas y Colores
TRAIT_LABELS = {
    "O": "Apertura a la Experiencia",
    "C": "Responsabilidad", 
    "E": "Extraversión",
    "A": "Amabilidad",
    "N": "Neuroticismo"
}

TRAIT_DESCRIPTIONS = {
    "O": "Creatividad, curiosidad y apertura a nuevas experiencias",
    "C": "Organización, responsabilidad y confiabilidad",
    "E": "Sociabilidad, energía y búsqueda de estimulación",
    "A": "Cooperación, empatía y amabilidad hacia los demás", 
    "N": "Estabilidad emocional vs. tendencia a emociones negativas"
}

COLORS = {
    "O": "#FF6B6B",
    "C": "#4ECDC4", 
    "E": "#45B7D1",
    "A": "#96CEB4",
    "N": "#FFEAA7"
}

# --- 2. LÓGICA DE PUNTUACIÓN ---

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
                score = 6 - score  # Invertir puntuación
            scores[trait] += score
            
    return dict(scores)

def interpret_score(score, trait_code):
    """Interpreta la puntuación y devuelve el perfil."""
    # Umbrales ajustados para el rango actual
    max_possible = ITEMS_PER_TRAIT * 5
    low_threshold = max_possible * 0.4
    high_threshold = max_possible * 0.7
    
    if score <= low_threshold:
        level = "Bajo"
        color = "#FF6B6B"  # Rojo
    elif score >= high_threshold:
        level = "Alto" 
        color = "#4ECDC4"  # Verde
    else:
        level = "Medio"
        color = "#FFE66D"  # Amarillo
        
    # Descripciones según el nivel
    descriptions = {
        "O": {
            "Bajo": "Prefieres lo familiar y tradicional",
            "Medio": "Equilibrado entre tradición y novedad", 
            "Alto": "Muy creativo y abierto a nuevas experiencias"
        },
        "C": {
            "Bajo": "Flexible y espontáneo",
            "Medio": "Organizado pero adaptable",
            "Alto": "Muy organizado y responsable"
        },
        "E": {
            "Bajo": "Reservado e introspectivo",
            "Medio": "Sociable pero valora la soledad",
            "Alto": "Muy sociable y enérgico"
        },
        "A": {
            "Bajo": "Directo y assertivo",
            "Medio": "Cooperativo pero con límites",
            "Alto": "Muy cooperativo y empático"
        },
        "N": {
            "Bajo": "Emocionalmente estable",
            "Medio": "Algo sensible al estrés",
            "Alto": "Emocionalmente reactivo"
        }
    }
    
    return level, color, descriptions[trait_code][level]

def create_bar_chart(scores):
    """Crea un gráfico de barras simple usando HTML/CSS."""
    
    max_score = MAX_SCORE_PER_TRAIT
    bars_html = ""
    
    for trait, score in scores.items():
        percentage = (score / max_score) * 100
        color = COLORS[trait]
        
        bars_html += f"""
        <div style="margin: 15px 0;">
            <div style="display: flex; justify-content: space-between; margin-bottom: 5px;">
                <span><strong>{TRAIT_LABELS[trait]}</strong></span>
                <span>{score}/{max_score}</span>
            </div>
            <div style="background: #f0f0f0; border-radius: 10px; height: 20px;">
                <div style="background: {color}; width: {percentage}%; height: 100%; border-radius: 10px; 
                          transition: width 0.5s ease;"></div>
            </div>
            <div style="font-size: 0.8em; color: #666; margin-top: 2px;">
                {TRAIT_DESCRIPTIONS[trait]}
            </div>
        </div>
        """
    
    return f"""
    <div style="background: white; padding: 20px; border-radius: 10px; border: 1px solid #e0e0e0;">
        <h3 style="text-align: center; margin-bottom: 20px;">Perfil de Personalidad</h3>
        {bars_html}
    </div>
    """

# --- 3. INTERFAZ DE USUARIO ---

# Inicialización del estado
if 'current_page' not in st.session_state:
    st.session_state.current_page = 0
    st.session_state.answers = {}
    st.session_state.test_completed = False
    st.session_state.scroll_trigger = False

# Funciones de navegación
def next_page():
    if st.session_state.current_page < TOTAL_PAGES - 1:
        st.session_state.current_page += 1
        st.session_state.scroll_trigger = True

def prev_page():
    if st.session_state.current_page > 0:
        st.session_state.current_page -= 1
        st.session_state.scroll_trigger = True

def reset_test():
    st.session_state.current_page = 0
    st.session_state.answers = {}
    st.session_state.test_completed = False
    st.session_state.scroll_trigger = True

# --- HEADER ---
st.markdown(
    """
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                padding: 25px; border-radius: 10px; margin-bottom: 20px;">
        <h1 style="color: white; text-align: center; margin: 0;">🧠 Test de Personalidad Big Five</h1>
        <p style="color: white; text-align: center; margin: 10px 0 0 0;">
            Descubre tu perfil psicológico completo
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

# Mostrar contenido según el estado
if not st.session_state.test_completed:
    # --- PÁGINAS DE PREGUNTAS ---
    
    # Barra de progreso
    progress = (st.session_state.current_page + 1) / TOTAL_PAGES
    st.progress(progress)
    
    col_left, col_center, col_right = st.columns([1, 2, 1])
    with col_center:
        st.markdown(f"**Página {st.session_state.current_page + 1} de {TOTAL_PAGES}**")
    
    # Botones de navegación superiores
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col1:
        if st.session_state.current_page > 0:
            if st.button("⬅️ Anterior", use_container_width=True, key="prev_top"):
                prev_page()
                st.rerun()
    
    with col3:
        if st.session_state.current_page < TOTAL_PAGES - 1:
            if st.button("Siguiente ➡️", use_container_width=True, key="next_top"):
                next_page()
                st.rerun()
        else:
            if st.button("📊 Ver Resultados", use_container_width=True, type="primary", key="results_top"):
                st.session_state.test_completed = True
                st.session_state.scroll_trigger = True
                st.rerun()
    
    # Preguntas de la página actual
    start_idx = st.session_state.current_page * QUESTIONS_PER_PAGE
    end_idx = min(start_idx + QUESTIONS_PER_PAGE, TOTAL_QUESTIONS)
    
    st.markdown("---")
    st.markdown("### Por favor, responde con sinceridad:")
    
    for i in range(start_idx, end_idx):
        question = QUESTIONS[i]
        q_id = question["id"]
        
        with st.container():
            st.markdown(f"**{i + 1}. {question['text']}**")
            
            # Mostrar opciones de respuesta en columnas
            cols = st.columns(5)
            current_answer = st.session_state.answers.get(q_id)
            
            for idx, (score, label) in enumerate(LIKERT_OPTIONS.items()):
                with cols[idx]:
                    is_selected = current_answer == score
                    button_type = "primary" if is_selected else "secondary"
                    
                    if st.button(
                        label,
                        key=f"{q_id}_{score}",
                        use_container_width=True,
                        type=button_type
                    ):
                        st.session_state.answers[q_id] = score
                        st.rerun()
            
            # Mostrar respuesta actual
            if current_answer:
                st.info(f"Respuesta actual: **{LIKERT_OPTIONS[current_answer]}**")
            else:
                st.warning("Por favor selecciona una respuesta")
            
            st.markdown("---")
    
    # Botones de navegación inferiores
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col1:
        if st.session_state.current_page > 0:
            if st.button("⬅️ Anterior", use_container_width=True, key="prev_bottom"):
                prev_page()
                st.rerun()
    
    with col3:
        if st.session_state.current_page < TOTAL_PAGES - 1:
            if st.button("Siguiente ➡️", use_container_width=True, key="next_bottom"):
                next_page()
                st.rerun()
        else:
            if st.button("📊 Ver Resultados", use_container_width=True, type="primary", key="results_bottom"):
                st.session_state.test_completed = True
                st.session_state.scroll_trigger = True
                st.rerun()

else:
    # --- PÁGINA DE RESULTADOS ---
    st.markdown("## 📊 Tus Resultados del Test Big Five")
    
    # Calcular puntuaciones
    scores = calculate_score(st.session_state.answers)
    
    # Mostrar gráfico de barras
    st.markdown("### Tu Perfil de Personalidad")
    chart_html = create_bar_chart(scores)
    st.markdown(chart_html, unsafe_allow_html=True)
    
    # Análisis detallado por rasgo
    st.markdown("### Análisis Detallado por Rasgo")
    
    for trait_code, trait_name in TRAIT_LABELS.items():
        score = scores.get(trait_code, 0)
        level, color, description = interpret_score(score, trait_code)
        
        with st.expander(f"{trait_name} - {level} ({score}/{MAX_SCORE_PER_TRAIT})", expanded=True):
            st.markdown(f"**Descripción:** {description}")
            
            # Barras de progreso para cada rasgo
            progress = score / MAX_SCORE_PER_TRAIT
            st.progress(progress)
            
            # Recomendaciones según el nivel
            if level == "Alto":
                st.success("**Fortaleza:** Este rasgo está bien desarrollado en tu personalidad.")
            elif level == "Bajo":
                st.info("**Oportunidad:** Hay espacio para desarrollar este aspecto.")
            else:
                st.warning("**Equilibrio:** Este rasgo está en un nivel balanceado.")

    # Estadísticas generales
    st.markdown("### 📈 Estadísticas del Test")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        answered = len(st.session_state.answers)
        st.metric("Preguntas respondidas", f"{answered}/{TOTAL_QUESTIONS}")
    
    with col2:
        completion_rate = (answered / TOTAL_QUESTIONS) * 100
        st.metric("Tasa de completitud", f"{completion_rate:.1f}%")
    
    with col3:
        avg_score = sum(scores.values()) / len(scores) if scores else 0
        st.metric("Puntuación promedio", f"{avg_score:.1f}")

    # Botón para reiniciar
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🔄 Realizar el Test Nuevamente", use_container_width=True, type="primary"):
            reset_test()
            st.rerun()

# --- SCROLL AUTOMÁTICO ---
if st.session_state.scroll_trigger:
    scroll_to_top()
    st.session_state.scroll_trigger = False

# --- FOOTER ---
st.markdown("---")
st.markdown(
    """
    <div style="text-align: center; color: #666; font-size: 0.9em;">
        <p>Test Big Five basado en el modelo OCEAN de personalidad. 
        Para fines educativos y de autoconocimiento.</p>
    </div>
    """,
    unsafe_allow_html=True
)
