import streamlit as st

st.set_page_config(page_title="Clasificador de Patrones 3x3", layout="wide")

st.title("Tarea 3 — Clasificando Patrones con una Máquina Simple")
st.markdown("""
Este sistema interactivo extiende la máquina de puntuación transformándola en un **clasificador automático** capaz de decidir si un patrón es una **T** o **No es una T** comparando el puntaje con un umbral (*threshold*).
""")

# 1. BASE DE DATOS DE IMÁGENES (3 Positivas y 3 Negativas)
imagenes = {
    "T Clásica (Positivo 1)": {"matriz": [[1, 1, 1], [0, 1, 0], [0, 1, 0]], "es_T": True},
    "T Gruesa (Positivo 2)": {"matriz": [[1, 1, 1], [1, 1, 1], [0, 1, 0]], "es_T": True},
    "T Alta (Positivo 3)": {"matriz": [[1, 1, 1], [0, 1, 0], [0, 1, 0]], "es_T": True},
    "Línea Horizontal (Negativo 1)": {"matriz": [[1, 1, 1], [0, 0, 0], [0, 0, 0]], "es_T": False},
    "Cruz / Invertida (Negativo 2)": {"matriz": [[0, 1, 0], [1, 1, 1], [0, 1, 0]], "es_T": False},
    "Cuadrado Hueco (Negativo 3)": {"matriz": [[1, 1, 1], [1, 0, 1], [1, 1, 1]], "es_T": False}
}

# 2. CONTROLES INTERACTIVOS (Sidebar)
st.sidebar.header("⚙️ Parámetros del Clasificador")

# Valores iniciales recomendados
valores_iniciales = [
    [2, 2, 2],
    [-1, 3, -1],
    [-1, 3, -1]
]

st.sidebar.subheader("Matriz de Pesos (w)")
pesos = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
for i in range(3):
    cols = st.sidebar.columns(3)
    for j in range(3):
        with cols[j]:
            pesos[i][j] = st.sidebar.slider(f"w_{i}{j}", min_value=-5, max_value=5, value=valores_iniciales[i][j], key=f"w_{i}_{j}")

threshold = st.sidebar.slider("Umbral de Decisión (Threshold)", min_value=-5, max_value=15, value=4)

# FUNCIÓN AUXILIAR DE CÁLCULO MANUAL (Sin librerías prohibidas)
def calcular_puntaje(matriz, pesos):
    puntaje = 0
    for i in range(3):
        for j in range(3):
            puntaje += matriz[i][j] * pesos[i][j]
    return puntaje

# 3. INTERFAZ PRINCIPAL - DOS PESTAÑAS
tab1, tab2 = st.tabs(["🔎 Evaluación Individual", "📊 Evaluación de Todos los Ejemplos"])

with tab1:
    col_izq, col_der = st.columns([1, 1])
    
    with col_izq:
        st.subheader("🖼️ Selección de Patrón")
        nombre_sel = st.selectbox("Elige un patrón para evaluar individualmente:", list(imagenes.keys()))
        info_img = imagenes[nombre_sel]
        matriz_img = info_img["matriz"]
        
        st.write("**Visualización de Píxeles:**")
        for fila in matriz_img:
            celdas = "".join([f"⬛" if pixel == 1 else f"⬜" for pixel in fila])
            st.markdown(f"### {celdas}")
            
    with col_der:
        st.subheader("🧮 Operación de la Máquina")
        puntaje_final = calcular_puntaje(matriz_img, pesos)
        
        st.metric(label="Puntaje Calculado (y)", value=puntaje_final)
        st.metric(label="Umbral (Threshold)", value=threshold)
        
        # Regla de clasificación automática exigida
        st.markdown("**Decisión Automática:**")
        if puntaje_final >= threshold:
            st.success("🤖 Clasificación: **Es una T**")
        else:
            st.error("🤖 Clasificación: **No es una T**")

with tab2:
    st.subheader("📈 Matriz de Rendimiento Global")
    st.write("Observa cómo afectan tus parámetros a todos los ejemplos en tiempo real para evitar errores de clasificación:")
    
    errores = 0
    columnas_ejemplos = st.columns(6)
    
    for idx, (nombre, info) in enumerate(imagenes.items()):
        with columnas_ejemplos[idx]:
            st.markdown(f"**{nombre.split(' ')[0]}**")
            score = calcular_puntaje(info["matriz"], pesos)
            prediccion_es_T = score >= threshold
            es_correcto = prediccion_es_T == info["es_T"]
            
            if not es_correcto:
                errores += 1
                st.error(f"Puntaje: {score}\n\n❌ Error")
            else:
                st.success(f"Puntaje: {score}\n\n✅ OK")
                
    st.markdown("---")
    if errores == 0:
        st.balloons()
        st.success("🎉 **¡Configuración Perfecta!** La máquina clasifica correctamente los 6 patrones sin cometer ningún error.")
    else:
        st.warning(f"⚠️ La máquina tiene actualmente **{errores} error(es)** de clasificación con estos parámetros. ¡Ajusta los pesos o el umbral!")
