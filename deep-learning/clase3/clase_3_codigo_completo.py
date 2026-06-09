#!/usr/bin/env python3
"""
EST-744: Deep Learning - Clase 3
Clasificación de Texto con Redes Neuronales (RNN, LSTM, CNN)

Este archivo contiene todos los ejemplos de código de la Clase 3,
organizados por sección y arquitectura.

Autor: Juan Zamora O.
Instituto de Estadística, PUCV
Junio 2026
"""

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from sklearn.metrics import confusion_matrix, classification_report
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# ============================================================================
# SECCIÓN 1: PREPARACIÓN DE DATOS - Dataset IMDb
# ============================================================================

print("=" * 70)
print("SECCIÓN 1: CARGA Y EXPLORACIÓN DE DATOS")
print("=" * 70)

# Cargar dataset IMDb (25,000 entrenamiento, 25,000 prueba)
(x_train, y_train), (x_test, y_test) = keras.datasets.imdb.load_data(num_words=5000)

print(f"Número de ejemplos entrenamiento: {len(x_train)}")  # 25000
print(f"Número de ejemplos prueba: {len(x_test)}")          # 25000
print(f"Etiqueta primera reseña (1=positiva, 0=negativa): {y_train[0]}")
print(f"Largo de la reseña: {len(x_train[0])}")

# Recuperar palabras originales
word_index = keras.datasets.imdb.get_word_index()
reverse_word_index = dict([(value, key) for (key, value) in word_index.items()])

def decode_review(review_sequence, max_words=100):
    """Convierte secuencia de índices a palabras."""
    return ' '.join([reverse_word_index.get(i - 3, '?') 
                     for i in review_sequence[:max_words]])

print(f"\nPrimera reseña decodificada:")
print(f"{decode_review(x_train[0])}")

# ============================================================================
# SECCIÓN 2: PREPARACIÓN DE SECUENCIAS - Padding
# ============================================================================

print("\n" + "=" * 70)
print("SECCIÓN 2: PADDING Y PREPARACIÓN DE SECUENCIAS")
print("=" * 70)

# Problema: las secuencias tienen diferentes longitudes
# Solución: rellenar/truncar a longitud fija

max_length = 200

x_train_padded = pad_sequences(x_train, maxlen=max_length, 
                               padding='post', truncating='post')
x_test_padded = pad_sequences(x_test, maxlen=max_length,
                              padding='post', truncating='post')

print(f"Forma original: {x_train.shape}")          # (25000,) variable
print(f"Forma rellenada: {x_train_padded.shape}")  # (25000, 200)
print(f"Verificación: primera secuencia rellenada tiene {len(x_train_padded[0])} elementos")

# ============================================================================
# SECCIÓN 3: MODELO LSTM SIMPLE
# ============================================================================

print("\n" + "=" * 70)
print("SECCIÓN 3: MODELO LSTM - IMPLEMENTACIÓN")
print("=" * 70)

# Construir modelo LSTM
model_lstm = keras.Sequential([
    # Capa 1: Embedding - convierte índices a vectores densos
    layers.Embedding(input_dim=5000,      # tamaño del vocabulario
                    output_dim=128,       # dimensión del embedding
                    input_length=max_length),
    
    # Capa 2: LSTM - procesa la secuencia
    layers.LSTM(units=64,                 # células LSTM
               dropout=0.2,               # dropout durante entrenamiento
               recurrent_dropout=0.2),    # dropout en conexiones recurrentes
    
    # Capas 3-4: Clasificación final
    layers.Dense(32, activation='relu'),
    layers.Dropout(0.5),
    layers.Dense(1, activation='sigmoid')  # salida: probabilidad positiva
])

# Compilar
model_lstm.compile(
    loss='binary_crossentropy',      # para clasificación binaria
    optimizer='adam',                 # optimizer robusto
    metrics=['accuracy']              # seguir precisión
)

print("\nArquitectura LSTM:")
model_lstm.summary()

# Entrenar (comentado para no ejecutar automáticamente)
print("\nEntrenamiento LSTM (comentado):")
print("history = model_lstm.fit(")
print("    x_train_padded, y_train,")
print("    epochs=5,")
print("    batch_size=32,")
print("    validation_split=0.2,")
print("    verbose=1")
print(")")

# Descomentar y ejecutar si deseas entrenar:
# history = model_lstm.fit(
#     x_train_padded, y_train,
#     epochs=5,
#     batch_size=32,
#     validation_split=0.2,
#     verbose=1
# )

# Evaluar (comentado sin modelo entrenado)
# test_loss, test_acc = model_lstm.evaluate(x_test_padded, y_test)
# print(f"Precisión en prueba LSTM: {test_acc * 100:.2f}%")

# ============================================================================
# SECCIÓN 4: MODELO CNN
# ============================================================================

print("\n" + "=" * 70)
print("SECCIÓN 4: MODELO CNN - IMPLEMENTACIÓN")
print("=" * 70)

# CNN modelo con convolución 1D
model_cnn = keras.Sequential([
    # Embedding
    layers.Embedding(input_dim=5000,
                    output_dim=128,
                    input_length=max_length),
    
    # Convolución: detecta patrones de 3 palabras consecutivas
    layers.Conv1D(filters=128,          # número de filtros
                 kernel_size=3,         # n-gramas de tamaño 3
                 activation='relu'),
    
    # Pooling: selecciona la característica más importante
    layers.GlobalMaxPooling1D(),
    
    # Capas densas
    layers.Dense(64, activation='relu'),
    layers.Dropout(0.5),
    layers.Dense(1, activation='sigmoid')
])

model_cnn.compile(
    loss='binary_crossentropy',
    optimizer='adam',
    metrics=['accuracy']
)

print("\nArquitectura CNN:")
model_cnn.summary()

# Entrenar (comentado)
print("\nEntrenamiento CNN (comentado):")
# history = model_cnn.fit(
#     x_train_padded, y_train,
#     epochs=5,
#     batch_size=32,
#     validation_split=0.2
# )

# ============================================================================
# SECCIÓN 5: COMPARACIÓN DE RESULTADOS
# ============================================================================

print("\n" + "=" * 70)
print("SECCIÓN 5: COMPARACIÓN DE ARQUITECTURAS")
print("=" * 70)

# Resultados típicos (para visualización)
resultados_modelos = {
    'Embeddings Promediados': 0.88,
    'CNN': 0.91,
    'LSTM': 0.92
}

print("\nResultados típicos por arquitectura:")
for modelo, acc in resultados_modelos.items():
    print(f"  {modelo:.<30} {acc * 100:6.2f}%")

# Crear gráfico de comparación
fig, ax = plt.subplots(figsize=(8, 5))
bars = ax.bar(resultados_modelos.keys(), resultados_modelos.values())

# Colorear barras
colors = ['red', 'orange', 'green']
for bar, color in zip(bars, colors):
    bar.set_color(color)

ax.set_ylabel('Precisión', fontsize=12)
ax.set_title('Comparación de Arquitecturas para Análisis de Sentimientos', 
             fontsize=14)
ax.set_ylim([0.85, 0.95])

# Añadir valores en las barras
for bar in bars:
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2., height,
           f'{height:.2%}',
           ha='center', va='bottom', fontsize=11)

plt.tight_layout()
plt.savefig('comparacion_arquitecturas.png', dpi=150)
print("\nGráfico guardado como 'comparacion_arquitecturas.png'")
plt.show()

# ============================================================================
# SECCIÓN 6: EXTENSIONES - LSTM BIDIRECCIONAL
# ============================================================================

print("\n" + "=" * 70)
print("SECCIÓN 6: EXTENSIÓN - LSTM BIDIRECCIONAL")
print("=" * 70)

model_bilstm = keras.Sequential([
    layers.Embedding(5000, 128, input_length=200),
    
    # Procesa en ambas direcciones
    layers.Bidirectional(
        layers.LSTM(64, dropout=0.2, recurrent_dropout=0.2)
    ),
    
    layers.Dense(32, activation='relu'),
    layers.Dropout(0.5),
    layers.Dense(1, activation='sigmoid')
])

model_bilstm.compile(
    loss='binary_crossentropy',
    optimizer='adam',
    metrics=['accuracy']
)

print("\nArquitectura LSTM Bidireccional:")
model_bilstm.summary()

# Ventaja: típicamente 0.5-1% mejor que unidireccional

# ============================================================================
# SECCIÓN 7: EXTENSIÓN - CNN CON MÚLTIPLES TAMAÑOS DE FILTRO
# ============================================================================

print("\n" + "=" * 70)
print("SECCIÓN 7: EXTENSIÓN - CNN CON MÚLTIPLES FILTROS")
print("=" * 70)

from tensorflow.keras import Input, Model

# Input
inputs = Input(shape=(200,), dtype='int32')
x = layers.Embedding(5000, 128)(inputs)

# Tres tamaños de filtro en paralelo
conv3 = layers.Conv1D(64, kernel_size=3, activation='relu')(x)
pool3 = layers.GlobalMaxPooling1D()(conv3)

conv4 = layers.Conv1D(64, kernel_size=4, activation='relu')(x)
pool4 = layers.GlobalMaxPooling1D()(conv4)

conv5 = layers.Conv1D(64, kernel_size=5, activation='relu')(x)
pool5 = layers.GlobalMaxPooling1D()(conv5)

# Concatenar características
merged = layers.Concatenate()([pool3, pool4, pool5])

# Clasificación
output = layers.Dense(32, activation='relu')(merged)
output = layers.Dropout(0.5)(output)
output = layers.Dense(1, activation='sigmoid')(output)

model_multicnn = Model(inputs, output)
model_multicnn.compile(
    loss='binary_crossentropy',
    optimizer='adam',
    metrics=['accuracy']
)

print("\nArquitectura CNN Multi-Filtro:")
model_multicnn.summary()

# ============================================================================
# SECCIÓN 8: EXTENSIÓN - LSTM APILADA
# ============================================================================

print("\n" + "=" * 70)
print("SECCIÓN 8: EXTENSIÓN - LSTM APILADA (PROFUNDA)")
print("=" * 70)

model_deep_lstm = keras.Sequential([
    layers.Embedding(5000, 128, input_length=200),
    
    # Capa 1: pasar estados a siguiente capa (return_sequences=True)
    layers.LSTM(128, return_sequences=True, dropout=0.2),
    
    # Capa 2: procesar toda la secuencia de capa 1
    layers.LSTM(64, return_sequences=False, dropout=0.2),
    
    layers.Dense(32, activation='relu'),
    layers.Dropout(0.5),
    layers.Dense(1, activation='sigmoid')
])

model_deep_lstm.compile(
    loss='binary_crossentropy',
    optimizer='adam',
    metrics=['accuracy']
)

print("\nArquitectura LSTM Apilada:")
model_deep_lstm.summary()

# ============================================================================
# SECCIÓN 9: ANÁLISIS DE RESULTADOS (simulado)
# ============================================================================

print("\n" + "=" * 70)
print("SECCIÓN 9: ANÁLISIS DE RESULTADOS - MATRIZ DE CONFUSIÓN")
print("=" * 70)

# Simulación de predicciones para demostración
# (En práctica real, esto provendría del modelo entrenado)
np.random.seed(42)
y_test_sample = np.random.binomial(1, 0.5, 100)
y_pred_prob = np.random.uniform(0.3, 0.9, 100)
y_pred = (y_pred_prob > 0.5).astype(int)

# Matriz de confusión
cm = confusion_matrix(y_test_sample, y_pred)

print("\nMatriz de Confusión:")
print(cm)
print(f"\nVerdaderos Positivos (VP): {cm[1,1]}")
print(f"Falsos Positivos (FP): {cm[0,1]}")
print(f"Verdaderos Negativos (VN): {cm[0,0]}")
print(f"Falsos Negativos (FN): {cm[1,0]}")

# Reporte detallado
print("\nReporte de Clasificación:")
print(classification_report(y_test_sample, y_pred,
                          target_names=['Negativa', 'Positiva']))

# ============================================================================
# SECCIÓN 10: EJERCICIOS SUGERIDOS
# ============================================================================

print("\n" + "=" * 70)
print("SECCIÓN 10: EJERCICIOS SUGERIDOS (CÓDIGO PLANTILLA)")
print("=" * 70)

print("""
EJERCICIO 1: Cambiar max_length y medir impacto
──────────────────────────────────────────────
for max_len in [50, 100, 200, 500]:
    x_train_test = pad_sequences(x_train, maxlen=max_len, padding='post')
    x_test_test = pad_sequences(x_test, maxlen=max_len, padding='post')
    
    model = keras.Sequential([...])  # construir modelo
    history = model.fit(x_train_test, y_train, epochs=3, verbose=0)
    acc = model.evaluate(x_test_test, y_test)[1]
    
    print(f"max_length={max_len}: accuracy={acc:.4f}, tiempo_memoria=...")


EJERCICIO 2: Ajustar dropout y comparar
────────────────────────────────────────
dropout_rates = [0.0, 0.2, 0.5]
results = {}

for dropout_rate in dropout_rates:
    model = keras.Sequential([
        layers.Embedding(5000, 128, input_length=200),
        layers.LSTM(64, dropout=dropout_rate),
        layers.Dense(32, activation='relu'),
        layers.Dropout(dropout_rate),
        layers.Dense(1, activation='sigmoid')
    ])
    # entrenar y evaluar...
    results[dropout_rate] = accuracy


EJERCICIO 3: Extraer y visualizar estados ocultos
──────────────────────────────────────────────────
# Crear modelo que extrae estados ocultos de la capa LSTM
layer_output = model.layers[1].output
intermediate_model = keras.Model(inputs=model.input, outputs=layer_output)

# Obtener estados para algunas reseñas
hidden_states = intermediate_model.predict(x_test_padded[:5])

# Visualizar
import matplotlib.pyplot as plt
plt.figure(figsize=(12, 4))
plt.imshow(hidden_states[0])  # primera reseña
plt.colorbar()
plt.title('Estados Ocultos LSTM para Primera Reseña')
plt.xlabel('Dimensión del estado oculto')
plt.ylabel('Paso temporal')
plt.show()


EJERCICIO 4: Predecir una reseña inventada
────────────────────────────────────────────
# Crear una reseña personalizada
reseña_texto = "Esta película fue excelente, muy recomendada para todos"

# Tokenizar manualmente (simulado)
# En práctica, usar el mismo tokenizador usado en entrenamiento
seq = [10, 45, 100, 2, 30, 150]  # índices simulados

# Rellenar
seq_padded = pad_sequences([seq], maxlen=200)

# Predecir
predicción = model.predict(seq_padded)
sentimiento = 'POSITIVO' if predicción[0][0] > 0.5 else 'NEGATIVO'
confianza = max(predicción[0][0], 1 - predicción[0][0])

print(f"Reseña: {reseña_texto}")
print(f"Sentimiento: {sentimiento}")
print(f"Confianza: {confianza * 100:.2f}%")
""")

# ============================================================================
# SECCIÓN 11: PROBLEMAS COMUNES Y SOLUCIONES
# ============================================================================

print("\n" + "=" * 70)
print("SECCIÓN 11: PROBLEMAS COMUNES Y DIAGNÓSTICO")
print("=" * 70)

problemas = {
    "Precisión bajo (<85%)": [
        "Verificar que los datos estén normalizados correctamente",
        "Revisar que el relleno se haya aplicado correctamente",
        "Aumentar epochs de entrenamiento",
        "Incrementar unidades LSTM o capas densas"
    ],
    "Sobreajuste evidente": [
        "Aumentar dropout (0.2 → 0.3 o 0.5)",
        "Reducir unidades LSTM (64 → 32)",
        "Añadir regularización L1/L2",
        "Usar early stopping"
    ],
    "Entrenamiento lentísimo": [
        "Reducir max_length (200 → 100)",
        "Usar CNN en lugar de LSTM",
        "Reducir embedding_dim (128 → 64)",
        "Aumentar batch_size (32 → 64 o 128)"
    ],
    "LSTM sin mejora vs. baseline": [
        "Probar LSTM bidireccional",
        "Apilar dos capas LSTM",
        "Aumentar número de unidades",
        "Revisar tasa de aprendizaje"
    ]
}

for problema, soluciones in problemas.items():
    print(f"\n{problema}:")
    for i, sol in enumerate(soluciones, 1):
        print(f"  {i}. {sol}")

# ============================================================================
# SECCIÓN 12: RESUMEN Y CONCLUSIONES
# ============================================================================

print("\n" + "=" * 70)
print("RESUMEN: COMPARACIÓN DE ARQUITECTURAS")
print("=" * 70)

resumen = pd.DataFrame({
    'Arquitectura': ['Embeddings Promediados', 'CNN', 'LSTM'],
    'Precisión': ['88%', '91%', '92%'],
    'Velocidad': ['Muy rápida', 'Rápida', 'Lenta'],
    'Captura Orden': ['No', 'Parcial', 'Sí'],
    'Contexto Largo': ['No', 'Limitado', 'Sí'],
    'Mejor para': [
        'Baseline rápido',
        'Producción (velocidad)',
        'Máxima precisión'
    ]
})

print("\n")
print(resumen.to_string(index=False))

print("\n\nRecomendaciones:")
print("""
1. INICIAR CON: Embeddings promediados (baseline rápido)
2. MEJORAR CON: CNN si velocidad es crítica
3. OPTIMIZAR CON: LSTM si precisión es lo primero
4. PRODUCCIÓN: CNN bidireccional es buen equilibrio
5. INVESTIGACIÓN: LSTM apilada o transformers (Clase 4)
""")

print("=" * 70)
print("FIN DEL SCRIPT - Clase 3: Clasificación de Texto con RNN")
print("=" * 70)
