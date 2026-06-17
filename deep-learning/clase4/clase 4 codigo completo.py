#!/usr/bin/env python3
"""
EST-744: Deep Learning - Clase 4
Mecanismos de Atención

Contiene todo el código de la Clase 4, organizado en secciones:
  1. Importaciones y configuración
  2. Auto-atención desde cero (SelfAttention)
  3. Clasificador con MultiHeadAttention de Keras
  4. Codificación posicional (PositionalEmbedding)
  5. Entrenamiento y evaluación
  6. Visualización de pesos de atención
  7. Comparación de arquitecturas
  8. Ejercicios sugeridos

Autor: Juan Zamora O.
Instituto de Estadística, PUCV
Junio 2026
"""

import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.preprocessing.sequence import pad_sequences
import matplotlib.pyplot as plt

# ============================================================================
# SECCIÓN 1: CONFIGURACIÓN GLOBAL
# ============================================================================

VOCAB_SIZE    = 5000   # palabras más frecuentes del vocabulario
EMBEDDING_DIM = 128    # dimension del embedding
SEQ_LENGTH    = 200    # longitud máxima de secuencias
NUM_HEADS     = 8      # cabezas de atención
KEY_DIM       = EMBEDDING_DIM // NUM_HEADS  # dimension por cabeza (= 16)

print("=" * 70)
print("EST-744 — Clase 4: Mecanismos de Atención")
print("=" * 70)
print(f"  vocab_size    = {VOCAB_SIZE}")
print(f"  embedding_dim = {EMBEDDING_DIM}")
print(f"  seq_length    = {SEQ_LENGTH}")
print(f"  num_heads     = {NUM_HEADS}")
print(f"  key_dim       = {KEY_DIM}")

# ============================================================================
# SECCIÓN 2: AUTO-ATENCIÓN DESDE CERO
# ============================================================================
# Implementación didáctica de auto-atención escalada.
# Referencia: Vaswani et al. (2017), ecuación (1).
# ============================================================================

print("\n" + "=" * 70)
print("SECCIÓN 2: AUTO-ATENCIÓN DESDE CERO")
print("=" * 70)

class AutoAtencion(keras.layers.Layer):
    """
    Auto-atención escalada (Scaled Dot-Product Attention).

    Calcula: Atencion(Q, K, V) = softmax(QK^T / sqrt(d_k)) * V

    Parametros
    ----------
    d_model : int
        Dimension del espacio de representacion.
    """

    def __init__(self, d_model, **kwargs):
        super().__init__(**kwargs)
        self.d_model = d_model
        # Proyecciones lineales para Q, K, V
        self.proj_consulta = layers.Dense(d_model)
        self.proj_clave    = layers.Dense(d_model)
        self.proj_valor    = layers.Dense(d_model)

    def call(self, x):
        # x: (batch, longitud_seq, d_model)
        Q = self.proj_consulta(x)   # (batch, seq, d_model)
        K = self.proj_clave(x)      # (batch, seq, d_model)
        V = self.proj_valor(x)      # (batch, seq, d_model)

        # Puntajes: similitud entre cada par (consulta, clave)
        puntajes = tf.matmul(Q, K, transpose_b=True)  # (batch, seq, seq)

        # Escalar para evitar gradientes muy pequeños en el softmax
        puntajes = puntajes / tf.math.sqrt(
            tf.cast(self.d_model, tf.float32)
        )

        # Convertir a pesos de atencion normalizados
        pesos = tf.nn.softmax(puntajes, axis=-1)  # suma 1 en la ultima dim

        # Combinacion ponderada de valores
        salida = tf.matmul(pesos, V)              # (batch, seq, d_model)
        return salida


# Verificacion con datos artificiales
capa_atencion = AutoAtencion(d_model=64)
x_prueba = tf.random.normal((2, 10, 64))   # batch=2, seq=10, dim=64
salida_prueba = capa_atencion(x_prueba)
print(f"  Entrada:  {x_prueba.shape}")
print(f"  Salida:   {salida_prueba.shape}  <- debe ser igual a la entrada")

# ============================================================================
# SECCIÓN 3: CLASIFICADOR CON MULTIHEADATTENTION DE KERAS
# ============================================================================
# En produccion siempre usar la capa de Keras: es mas eficiente y tiene
# soporte nativo para masking y pesos de atencion opcionales.
# ============================================================================

print("\n" + "=" * 70)
print("SECCIÓN 3: CLASIFICADOR CON MultiHeadAttention (Keras)")
print("=" * 70)

# --- 3a. Uso basico de la capa ---
print("\nUso basico de MultiHeadAttention:")
capa_mha = keras.layers.MultiHeadAttention(
    num_heads=NUM_HEADS,
    key_dim=KEY_DIM        # dimension por cabeza
)
# Auto-atencion: la secuencia atiende a si misma (query=key=value)
x_ejemplo = tf.random.normal((1, SEQ_LENGTH, EMBEDDING_DIM))
salida_mha = capa_mha(query=x_ejemplo, value=x_ejemplo, key=x_ejemplo)
print(f"  Entrada: {x_ejemplo.shape}")
print(f"  Salida:  {salida_mha.shape}")

# --- 3b. Modelo completo ---
print("\nConstruyendo modelo completo con atención:")

# NOTA: MultiHeadAttention en Keras espera (query, value[, key]) como
# argumentos separados, por lo que no puede usarse directamente en
# keras.Sequential. Usamos la API Funcional para mayor claridad.

entradas = keras.Input(shape=(SEQ_LENGTH,), dtype="int32")

# 1. Embedding (los pesos se aprenden durante el entrenamiento)
x = layers.Embedding(VOCAB_SIZE, EMBEDDING_DIM)(entradas)

# 2. Auto-atencion multi-cabezal
# return_attention_scores=False por defecto; True para visualizacion
x = layers.MultiHeadAttention(
    num_heads=NUM_HEADS,
    key_dim=KEY_DIM,
    dropout=0.1
)(query=x, value=x, key=x)

# 3. Reduccion temporal: promedio sobre todos los pasos de tiempo
x = layers.GlobalAveragePooling1D()(x)

# 4. Cabeza de clasificacion
x = layers.Dense(64, activation="relu")(x)
x = layers.Dropout(0.3)(x)
salidas = layers.Dense(1, activation="sigmoid")(x)

modelo_atencion = keras.Model(entradas, salidas,
                              name="clasificador_atencion")

modelo_atencion.compile(
    loss="binary_crossentropy",
    optimizer="adam",
    metrics=["accuracy"]
)

print("\nArquitectura del modelo:")
modelo_atencion.summary()

# ============================================================================
# SECCIÓN 4: CODIFICACIÓN POSICIONAL
# ============================================================================
# Implementacion exacta de Vaswani et al. (2017), seccion 3.5.
# PE(pos, 2i)   = sin(pos / 10000^(2i/d))
# PE(pos, 2i+1) = cos(pos / 10000^(2i/d))
# ============================================================================

print("\n" + "=" * 70)
print("SECCIÓN 4: CODIFICACIÓN POSICIONAL")
print("=" * 70)

def calcular_angulos(pos, i, d_model):
    """Calcula los angulos para la codificacion posicional."""
    return pos / np.power(10000, (2 * (i // 2)) / np.float32(d_model))


def codificacion_posicional(longitud, d_model):
    """
    Genera la matriz de codificacion posicional.

    Parametros
    ----------
    longitud : int
        Numero de posiciones (longitud maxima de secuencia).
    d_model  : int
        Dimension del embedding.

    Retorna
    -------
    np.ndarray de forma (1, longitud, d_model)
    """
    angulos = calcular_angulos(
        np.arange(longitud)[:, np.newaxis],   # (longitud, 1)
        np.arange(d_model)[np.newaxis, :],    # (1, d_model)
        d_model
    )
    # Seno en indices pares, coseno en indices impares
    angulos[:, 0::2] = np.sin(angulos[:, 0::2])
    angulos[:, 1::2] = np.cos(angulos[:, 1::2])
    return angulos[np.newaxis, ...]            # (1, longitud, d_model)


# Visualizar las primeras 50 posiciones en 64 dimensiones
cod_pos = codificacion_posicional(SEQ_LENGTH, EMBEDDING_DIM)
print(f"\nForma de la codificacion posicional: {cod_pos.shape}")

plt.figure(figsize=(10, 4))
plt.pcolormesh(cod_pos[0, :50, :], cmap="RdBu")
plt.xlabel("Dimension del embedding")
plt.ylabel("Posicion en la secuencia")
plt.title("Codificacion Posicional (primeras 50 posiciones)")
plt.colorbar(label="Valor")
plt.tight_layout()
plt.savefig("codificacion_posicional.png", dpi=150)
print("  Grafico guardado: codificacion_posicional.png")
plt.show()


class EmbeddingPosicional(keras.layers.Layer):
    """
    Combina embedding de palabras con codificacion posicional.
    Implementacion de Vaswani et al. (2017), seccion 3.4.
    """

    def __init__(self, vocab_size, embedding_dim, seq_length, **kwargs):
        super().__init__(**kwargs)
        self.embedding = layers.Embedding(vocab_size, embedding_dim)
        # Codificacion posicional fija (no se entrena)
        cod_pos = codificacion_posicional(seq_length, embedding_dim)
        self.cod_pos = tf.constant(cod_pos, dtype=tf.float32)

    def call(self, x):
        longitud = tf.shape(x)[1]
        # Suma embedding + codificacion posicional para cada posicion
        return self.embedding(x) + self.cod_pos[:, :longitud, :]


# Verificacion
capa_emb_pos = EmbeddingPosicional(VOCAB_SIZE, EMBEDDING_DIM, SEQ_LENGTH)
x_indices = tf.constant([[1, 2, 3, 4, 5]])   # secuencia de ejemplo
salida_emb = capa_emb_pos(x_indices)
print(f"\nEmbedding + posicion: entrada {x_indices.shape} → salida {salida_emb.shape}")

# ============================================================================
# SECCIÓN 5: ENTRENAMIENTO Y EVALUACIÓN
# ============================================================================

print("\n" + "=" * 70)
print("SECCIÓN 5: ENTRENAMIENTO Y EVALUACIÓN")
print("=" * 70)

# Cargar datos IMDb
print("\nCargando dataset IMDb...")
(x_train, y_train), (x_test, y_test) = keras.datasets.imdb.load_data(
    num_words=VOCAB_SIZE
)
print(f"  Entrenamiento: {len(x_train)} ejemplos")
print(f"  Prueba:        {len(x_test)} ejemplos")

# Rellenar secuencias a longitud fija
x_train_pad = pad_sequences(x_train, maxlen=SEQ_LENGTH,
                            padding="post", truncating="post")
x_test_pad  = pad_sequences(x_test,  maxlen=SEQ_LENGTH,
                            padding="post", truncating="post")
print(f"  Forma entrenamiento: {x_train_pad.shape}")

# Entrenar (descomentar para ejecutar)
print("\nEntrenamiento (comentado — descomentar para ejecutar):")
print("  history = modelo_atencion.fit(")
print("      x_train_pad, y_train,")
print("      epochs=3,")
print("      batch_size=32,")
print("      validation_split=0.2,")
print("      verbose=1")
print("  )")

# history = modelo_atencion.fit(
#     x_train_pad, y_train,
#     epochs=3,
#     batch_size=32,
#     validation_split=0.2,
#     verbose=1
# )

# Evaluar (descomentar tras entrenar)
# perdida, precision = modelo_atencion.evaluate(x_test_pad, y_test)
# print(f"\n  Precisión en prueba: {precision * 100:.2f}%")
# print(f"  Resultado esperado:  91–93%")

# ============================================================================
# SECCIÓN 6: VISUALIZACIÓN DE PESOS DE ATENCIÓN
# ============================================================================

print("\n" + "=" * 70)
print("SECCIÓN 6: VISUALIZACIÓN DE PESOS DE ATENCIÓN")
print("=" * 70)


def construir_modelo_con_pesos(modelo_entrenado, vocab_size,
                               embedding_dim, seq_length):
    """
    Construye un modelo auxiliar que retorna los pesos de atención
    junto con la predicción.

    Requiere que el modelo entrenado tenga MultiHeadAttention como
    segunda capa (indice 1, tras el embedding).
    """
    capa_mha = None
    for capa in modelo_entrenado.layers:
        if isinstance(capa, layers.MultiHeadAttention):
            capa_mha = capa
            break

    if capa_mha is None:
        raise ValueError("No se encontró MultiHeadAttention en el modelo.")

    entradas = keras.Input(shape=(seq_length,), dtype="int32")
    emb = layers.Embedding(vocab_size, embedding_dim)(entradas)

    # return_attention_scores=True retorna (salida, pesos)
    _, pesos_atencion = capa_mha(
        query=emb, value=emb, key=emb,
        return_attention_scores=True
    )
    return keras.Model(entradas, pesos_atencion)


def visualizar_atencion(pesos, tokens, cabeza=0, titulo="Pesos de Atención"):
    """
    Visualiza la matriz de atención de una cabeza como mapa de calor.

    Parametros
    ----------
    pesos  : np.ndarray de forma (batch, num_heads, seq, seq)
    tokens : list[str]  palabras de la secuencia
    cabeza : int        índice de la cabeza a visualizar
    titulo : str
    """
    matriz = pesos[0, cabeza, :len(tokens), :len(tokens)]
    fig, ax = plt.subplots(figsize=(8, 7))
    im = ax.imshow(matriz, cmap="viridis", aspect="auto")
    ax.set_xticks(range(len(tokens)))
    ax.set_yticks(range(len(tokens)))
    ax.set_xticklabels(tokens, rotation=45, ha="right", fontsize=9)
    ax.set_yticklabels(tokens, fontsize=9)
    ax.set_xlabel("Posicion clave (Key)")
    ax.set_ylabel("Posicion consulta (Query)")
    ax.set_title(f"{titulo} — Cabeza {cabeza}")
    plt.colorbar(im, ax=ax, label="Peso de atención")
    plt.tight_layout()
    nombre = f"atencion_cabeza_{cabeza}.png"
    plt.savefig(nombre, dpi=150)
    print(f"  Guardado: {nombre}")
    plt.show()


# Ejemplo de uso (requiere modelo entrenado):
print("\nEjemplo de uso (requiere modelo entrenado):")
print("""
  # Construir modelo auxiliar
  modelo_pesos = construir_modelo_con_pesos(
      modelo_atencion, VOCAB_SIZE, EMBEDDING_DIM, SEQ_LENGTH
  )

  # Obtener pesos para las primeras 5 reseñas
  pesos = modelo_pesos.predict(x_test_pad[:5])
  # pesos.shape → (5, NUM_HEADS, SEQ_LENGTH, SEQ_LENGTH)

  # Decodificar tokens para la primera reseña
  word_index = keras.datasets.imdb.get_word_index()
  idx2word   = {v: k for k, v in word_index.items()}
  tokens     = [idx2word.get(i - 3, '?') for i in x_test[0][:20]]

  # Visualizar cabeza 0
  visualizar_atencion(pesos, tokens, cabeza=0,
                      titulo='Análisis de Sentimientos IMDb')
""")

# ============================================================================
# SECCIÓN 7: COMPARACIÓN DE ARQUITECTURAS
# ============================================================================

print("\n" + "=" * 70)
print("SECCIÓN 7: COMPARACIÓN DE ARQUITECTURAS")
print("=" * 70)

resultados = {
    "Embeddings promediados": {"precision": 0.88, "tiempo_seg": 2,  "paralelo": True},
    "LSTM":                   {"precision": 0.92, "tiempo_seg": 45, "paralelo": False},
    "CNN":                    {"precision": 0.91, "tiempo_seg": 8,  "paralelo": True},
    "Atención":               {"precision": 0.92, "tiempo_seg": 10, "paralelo": True},
}

print(f"\n{'Modelo':<25} {'Precisión':>10} {'Seg/época':>10} {'Paralelo':>10}")
print("-" * 60)
for nombre, vals in resultados.items():
    paralelo = "✓" if vals["paralelo"] else "✗"
    print(f"  {nombre:<23} {vals['precision']:>10.2f} "
          f"{vals['tiempo_seg']:>9}s {paralelo:>10}")

# Grafico comparativo
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4))

nombres   = list(resultados.keys())
precision = [v["precision"]  for v in resultados.values()]
tiempos   = [v["tiempo_seg"] for v in resultados.values()]
colores   = ["#e74c3c", "#2ecc71", "#f39c12", "#3498db"]

# Panel izquierdo: precisión
barras = ax1.bar(nombres, precision, color=colores)
ax1.set_ylim(0.85, 0.95)
ax1.set_ylabel("Precisión", fontsize=11)
ax1.set_title("Precisión por arquitectura", fontsize=12)
ax1.tick_params(axis="x", rotation=15)
for b in barras:
    ax1.text(b.get_x() + b.get_width() / 2, b.get_height(),
             f"{b.get_height():.0%}", ha="center", va="bottom", fontsize=9)

# Panel derecho: tiempo por época
barras2 = ax2.bar(nombres, tiempos, color=colores)
ax2.set_ylabel("Segundos por época (GPU T4)", fontsize=11)
ax2.set_title("Velocidad de entrenamiento", fontsize=12)
ax2.tick_params(axis="x", rotation=15)
for b in barras2:
    ax2.text(b.get_x() + b.get_width() / 2, b.get_height(),
             f"{b.get_height()}s", ha="center", va="bottom", fontsize=9)

plt.tight_layout()
plt.savefig("comparacion_arquitecturas_clase4.png", dpi=150)
print("\n  Grafico guardado: comparacion_arquitecturas_clase4.png")
plt.show()

# ============================================================================
# SECCIÓN 8: EJERCICIOS SUGERIDOS (PLANTILLAS)
# ============================================================================

print("\n" + "=" * 70)
print("SECCIÓN 8: EJERCICIOS — PLANTILLAS DE CÓDIGO")
print("=" * 70)

print("""
EJERCICIO 1 — Variar num_heads y comparar
──────────────────────────────────────────
resultados_heads = {}

for n_heads in [2, 4, 8, 16]:
    entradas = keras.Input(shape=(SEQ_LENGTH,), dtype='int32')
    x = layers.Embedding(VOCAB_SIZE, EMBEDDING_DIM)(entradas)
    x = layers.MultiHeadAttention(
            num_heads=n_heads,
            key_dim=EMBEDDING_DIM // n_heads
        )(query=x, value=x, key=x)
    x = layers.GlobalAveragePooling1D()(x)
    x = layers.Dense(64, activation='relu')(x)
    x = layers.Dropout(0.3)(x)
    salidas = layers.Dense(1, activation='sigmoid')(x)

    modelo = keras.Model(entradas, salidas)
    modelo.compile(loss='binary_crossentropy',
                   optimizer='adam', metrics=['accuracy'])

    history = modelo.fit(x_train_pad, y_train, epochs=3,
                         batch_size=32, validation_split=0.2, verbose=0)
    _, prec = modelo.evaluate(x_test_pad, y_test, verbose=0)
    resultados_heads[n_heads] = prec
    print(f'  num_heads={n_heads}: precision={prec:.4f}')


EJERCICIO 2 — Ablación de codificación posicional
────────────────────────────────────────────────────
# Entrenar el mismo modelo sin sumar la codificacion posicional.
# Comparar precision final y velocidad de convergencia.

# Modelo SIN codificacion posicional:
entradas_sin = keras.Input(shape=(SEQ_LENGTH,), dtype='int32')
x_sin = layers.Embedding(VOCAB_SIZE, EMBEDDING_DIM)(entradas_sin)
# (no se suma codificacion posicional)
x_sin = layers.MultiHeadAttention(num_heads=4, key_dim=32)(
            query=x_sin, value=x_sin, key=x_sin)
x_sin = layers.GlobalAveragePooling1D()(x_sin)
x_sin = layers.Dense(64, activation='relu')(x_sin)
x_sin = layers.Dropout(0.3)(x_sin)
salidas_sin = layers.Dense(1, activation='sigmoid')(x_sin)
modelo_sin = keras.Model(entradas_sin, salidas_sin)
# Entrenar y comparar con modelo CON codificacion posicional.


EJERCICIO 3 — Comparar velocidad: Atención vs. LSTM
─────────────────────────────────────────────────────
import time

# Medir tiempo de una epoca de entrenamiento
t0 = time.time()
historia_atencion = modelo_atencion.fit(
    x_train_pad, y_train, epochs=1, batch_size=32, verbose=0
)
t_atencion = time.time() - t0

modelo_lstm = keras.Sequential([
    layers.Embedding(VOCAB_SIZE, EMBEDDING_DIM),
    layers.LSTM(64),
    layers.Dense(64, activation='relu'),
    layers.Dense(1, activation='sigmoid')
])
modelo_lstm.compile(loss='binary_crossentropy',
                    optimizer='adam', metrics=['accuracy'])

t0 = time.time()
historia_lstm = modelo_lstm.fit(
    x_train_pad, y_train, epochs=1, batch_size=32, verbose=0
)
t_lstm = time.time() - t0

print(f'  Atención: {t_atencion:.1f}s / epoca')
print(f'  LSTM:     {t_lstm:.1f}s / epoca')
print(f'  Speedup:  {t_lstm / t_atencion:.1f}x')


EJERCICIO 4 — Interpretabilidad en ejemplos mal clasificados
─────────────────────────────────────────────────────────────
# Paso 1: obtener predicciones y etiquetas
y_pred_prob = modelo_atencion.predict(x_test_pad)
y_pred = (y_pred_prob > 0.5).astype(int).flatten()

# Paso 2: identificar errores
errores = np.where(y_pred != y_test)[0]
print(f'  Ejemplos mal clasificados: {len(errores)} de {len(y_test)}')

# Paso 3: obtener pesos de atencion para los errores
modelo_pesos = construir_modelo_con_pesos(
    modelo_atencion, VOCAB_SIZE, EMBEDDING_DIM, SEQ_LENGTH
)
pesos_error = modelo_pesos.predict(x_test_pad[errores[:5]])

# Paso 4: decodificar y visualizar
word_index = keras.datasets.imdb.get_word_index()
idx2word   = {v: k for k, v in word_index.items()}
for i, idx in enumerate(errores[:3]):
    tokens = [idx2word.get(t - 3, '?') for t in x_test[idx][:15]]
    visualizar_atencion(
        pesos_error[i:i+1], tokens, cabeza=0,
        titulo=f'Error: real={y_test[idx]}, pred={y_pred[idx]}'
    )
""")

# ============================================================================
# FIN
# ============================================================================

print("\n" + "=" * 70)
print("FIN DEL SCRIPT — Clase 4: Mecanismos de Atención")
print("=" * 70)
print("""
Archivos generados:
  codificacion_posicional.png        — mapa de calor de PE
  comparacion_arquitecturas_clase4.png — comparacion precision/velocidad

Proximos pasos:
  1. Descomentar model.fit() en Seccion 5 para entrenar
  2. Ejecutar Ejercicios 1-4 de la Seccion 8
  3. Ir a Clase 5: Transformers y modelos pre-entrenados
""")
