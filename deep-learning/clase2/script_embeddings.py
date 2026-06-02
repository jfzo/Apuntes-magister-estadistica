"""
Script Completo: Embeddings y Clasificacion de Sentimientos
EST-744: Deep Learning para Estadisticos

Este script implementa el flujo completo de la clase:
1. Cargar embeddings pre-entrenados (Word2Vec)
2. Preparar datos (IMDb)
3. Crear representaciones de documentos
4. Entrenar clasificador simple
5. Visualizar resultados
"""

import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import matplotlib.pyplot as plt
from sklearn.manifold import TSNE
from gensim.models import KeyedVectors
import warnings
warnings.filterwarnings('ignore')

# ============================================================================
# CONFIGURACION
# ============================================================================

# Hiperparametros
VOCAB_SIZE = 10000
EMBEDDING_DIM = 300
MAX_LENGTH = 500
BATCH_SIZE = 32
EPOCHS = 15
VALIDATION_SPLIT = 0.2

print("=" * 70)
print("Embeddings y Clasificacion de Sentimientos")
print("EST-744: Deep Learning para Estadisticos")
print("=" * 70)

# ============================================================================
# PARTE 1: CARGA DE DATOS
# ============================================================================

print("\n[1/6] Cargando dataset IMDb...")

# Dataset IMDb: resenas de peliculas (positive/negative)
# La carga devuelve secuencias de indices, no texto directo
(x_train, y_train), (x_test, y_test) = keras.datasets.imdb.load_data(
    num_words=VOCAB_SIZE
)

print("  Train: {} resenas".format(len(x_train)))
print("  Test: {} resenas".format(len(x_test)))
print("  Ejemplo de secuencia: {}...".format(x_train[0][:20]))
print("  Label del ejemplo: {} (1=positivo, 0=negativo)".format(y_train[0]))

# Cargar word index (indice -> palabra)
word_index = keras.datasets.imdb.get_word_index()
reverse_word_index = {value: key for key, value in word_index.items()}

def decode_review(sequence):
    """Decodifica secuencia de indices a texto"""
    return ' '.join([reverse_word_index.get(i - 3, '?') for i in sequence])

print("\n  Resena decodificada: {}...".format(decode_review(x_train[0])[:200]))

# ============================================================================
# PARTE 2: CARGA DE EMBEDDINGS PRE-ENTRENADOS
# ============================================================================

print("\n[2/6] Cargando embeddings pre-entrenados...")
print("  (Este paso requiere descarga de ~1.5 GB)")
print("  (En produccion, descargaria antes una sola vez)")

# NOTA: En un entorno real, descargarias Word2Vec asi:
# from gensim.downloader import load
# w2v = load('word2vec-google-news-300')

# Para este ejemplo, simularemos embeddings aleatorios
# (En clase real, usarias Word2Vec genuino)

print("\n  SIMULACION: Usando embeddings aleatorios")
print("    (En clase real, cargarias Word2Vec genuino)")

# Simular embeddings pre-entrenados
np.random.seed(42)
embedding_matrix = np.random.normal(
    loc=0, 
    scale=0.5, 
    size=(VOCAB_SIZE, EMBEDDING_DIM)
)

# Palabras frecuentes tendrian embeddings mas estructurados
# Por simplicidad, todas son aleatorias en esta simulacion
print("  Matriz de embeddings: {}".format(embedding_matrix.shape))
print("  Embedding de palabra #1: {}...".format(embedding_matrix[1, :5]))

# ============================================================================
# PARTE 3: AGREGACION A NIVEL DE DOCUMENTO
# ============================================================================

print("\n[3/6] Agregando embeddings a nivel de documento...")

def sequences_to_embeddings(sequences, embedding_matrix, strategy='mean'):
    """
    Convierte secuencias de indices a vectores de documento.
    
    Args:
        sequences: Lista de listas de indices
        embedding_matrix: Matriz (vocab_size, embedding_dim)
        strategy: 'mean', 'max', o 'weighted'
    
    Returns:
        Array (n_samples, embedding_dim) de documentos agregados
    """
    embeddings = []
    
    for seq in sequences:
        if len(seq) == 0:  # Secuencia vacia
            embeddings.append(np.zeros(embedding_matrix.shape[1]))
            continue
        
        # Obtener embeddings de cada palabra
        seq_emb = embedding_matrix[seq]
        
        if strategy == 'mean':
            # Promedio simple
            doc_emb = seq_emb.mean(axis=0)
        elif strategy == 'max':
            # Max pooling
            doc_emb = seq_emb.max(axis=0)
        elif strategy == 'weighted':
            # Promedio ponderado
            weights = np.ones(len(seq)) / len(seq)
            doc_emb = (seq_emb * weights[:, np.newaxis]).sum(axis=0)
        
        embeddings.append(doc_emb)
    
    return np.array(embeddings)

# Convertir secuencias a embeddings
x_train_emb = sequences_to_embeddings(x_train, embedding_matrix, strategy='mean')
x_test_emb = sequences_to_embeddings(x_test, embedding_matrix, strategy='mean')

print("  Embeddings train: {}".format(x_train_emb.shape))
print("  Embeddings test: {}".format(x_test_emb.shape))
print("  Ejemplo: primer documento -> {}-D vector".format(EMBEDDING_DIM))
print("    Primeros 5 valores: {}".format(x_train_emb[0, :5]))

# ============================================================================
# PARTE 4: CONSTRUCCION Y ENTRENAMIENTO DEL MODELO
# ============================================================================

print("\n[4/6] Construyendo y entrenando modelo de clasificacion...")

# Arquitectura: capas densas sobre embeddings promediados
model = keras.Sequential([
    layers.Input(shape=(EMBEDDING_DIM,)),
    
    # Capa oculta 1
    layers.Dense(128, activation='relu'),
    layers.Dropout(0.3),  # Regularizacion
    
    # Capa oculta 2
    layers.Dense(64, activation='relu'),
    layers.Dropout(0.2),
    
    # Capa de salida: clasificacion binaria
    layers.Dense(1, activation='sigmoid')
])

# Ver arquitectura
print("\n  Arquitectura del modelo:")
model.summary()

# Compilacion
model.compile(
    loss='binary_crossentropy',
    optimizer='adam',
    metrics=['accuracy']
)

# Entrenamiento
print("\n  Entrenando...")
history = model.fit(
    x_train_emb, y_train,
    epochs=EPOCHS,
    batch_size=BATCH_SIZE,
    validation_split=VALIDATION_SPLIT,
    verbose=1
)

# ============================================================================
# PARTE 5: EVALUACION
# ============================================================================

print("\n[5/6] Evaluando en conjunto de prueba...")

test_loss, test_accuracy = model.evaluate(x_test_emb, y_test, verbose=0)
print("  Test Loss: {:.4f}".format(test_loss))
print("  Test Accuracy: {:.4f}".format(test_accuracy))

# Analisis de predicciones
predictions = model.predict(x_test_emb, verbose=0)

# Mostrar ejemplos
print("\n  Ejemplos de predicciones:")
for i in range(5):
    pred_prob = predictions[i][0]
    pred_label = "Positiva" if pred_prob > 0.5 else "Negativa"
    true_label = "Positiva" if y_test[i] == 1 else "Negativa"
    
    match = "OK" if (pred_prob > 0.5) == (y_test[i] == 1) else "NO"
    
    print("    {} Prediccion: {} (prob: {:.2f}), Real: {}".format(
        match, pred_label, pred_prob, true_label))

# Matriz de confusion
from sklearn.metrics import confusion_matrix, classification_report

y_pred_binary = (predictions > 0.5).astype(int).flatten()
cm = confusion_matrix(y_test, y_pred_binary)

print("\n  Matriz de confusion:")
print("    Verdaderos Negativos: {}".format(cm[0,0]))
print("    Falsos Positivos:     {}".format(cm[0,1]))
print("    Falsos Negativos:     {}".format(cm[1,0]))
print("    Verdaderos Positivos: {}".format(cm[1,1]))

# ============================================================================
# PARTE 6: VISUALIZACION
# ============================================================================

print("\n[6/6] Generando visualizaciones...")

fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# Grafico 1: Exactitud de entrenamiento
ax = axes[0, 0]
ax.plot(history.history['accuracy'], label='Entrenamiento', linewidth=2)
ax.plot(history.history['val_accuracy'], label='Validacion', linewidth=2)
ax.set_xlabel('Epoca')
ax.set_ylabel('Exactitud')
ax.set_title('Exactitud: Entrenamiento vs. Validacion')
ax.legend()
ax.grid(True, alpha=0.3)

# Grafico 2: Perdida de entrenamiento
ax = axes[0, 1]
ax.plot(history.history['loss'], label='Entrenamiento', linewidth=2)
ax.plot(history.history['val_loss'], label='Validacion', linewidth=2)
ax.set_xlabel('Epoca')
ax.set_ylabel('Perdida')
ax.set_title('Perdida: Entrenamiento vs. Validacion')
ax.legend()
ax.grid(True, alpha=0.3)

# Grafico 3: Distribucion de probabilidades predichas
ax = axes[1, 0]
ax.hist(predictions[y_test == 0], bins=30, alpha=0.6, label='Reales: Negativas')
ax.hist(predictions[y_test == 1], bins=30, alpha=0.6, label='Reales: Positivas')
ax.axvline(0.5, color='red', linestyle='--', linewidth=2, label='Umbral (0.5)')
ax.set_xlabel('Probabilidad Predicha')
ax.set_ylabel('Frecuencia')
ax.set_title('Distribucion de Predicciones')
ax.legend()

# Grafico 4: Matriz de confusion
ax = axes[1, 1]
im = ax.imshow(cm, cmap='Blues', aspect='auto')
ax.set_xticks([0, 1])
ax.set_yticks([0, 1])
ax.set_xticklabels(['Negativo', 'Positivo'])
ax.set_yticklabels(['Negativo', 'Positivo'])
ax.set_ylabel('Real')
ax.set_xlabel('Prediccion')
ax.set_title('Matriz de Confusion')

# Anotaciones en matriz
for i in range(2):
    for j in range(2):
        text = ax.text(j, i, cm[i, j], ha="center", va="center", 
                      color="white" if cm[i, j] > cm.max()/2 else "black",
                      fontsize=14)

plt.tight_layout()
plt.savefig('/mnt/user-data/outputs/embeddings_results.png', dpi=150, bbox_inches='tight')
print("  Graficos guardados en: embeddings_results.png")

# ============================================================================
# ANALISIS COMPLEMENTARIO: Visualizacion de Embeddings con t-SNE
# ============================================================================

print("\n" + "=" * 70)
print("ANALISIS ADICIONAL: Visualizacion de Embeddings")
print("=" * 70)

print("\nGenerando visualizacion t-SNE (puede tomar 1-2 minutos)...")

# Seleccionar subset de embeddings (t-SNE es costoso)
sample_size = 1000
sample_indices = np.random.choice(len(x_train_emb), sample_size, replace=False)
embeddings_sample = x_train_emb[sample_indices]
labels_sample = y_train[sample_indices]

# Aplicar t-SNE
tsne = TSNE(n_components=2, random_state=42, perplexity=30, n_iter=1000)
embeddings_2d = tsne.fit_transform(embeddings_sample)

# Visualizar
fig, ax = plt.subplots(figsize=(12, 8))

# Scatter plot coloreado por sentimiento
scatter = ax.scatter(
    embeddings_2d[labels_sample == 0, 0], 
    embeddings_2d[labels_sample == 0, 1],
    c='red', alpha=0.6, s=50, label='Negativas'
)
scatter = ax.scatter(
    embeddings_2d[labels_sample == 1, 0], 
    embeddings_2d[labels_sample == 1, 1],
    c='green', alpha=0.6, s=50, label='Positivas'
)

ax.set_title('Visualizacion t-SNE de Embeddings de Documentos\n(1000 resenas de IMDb)', 
            fontsize=14, fontweight='bold')
ax.set_xlabel('Dimension 1 (t-SNE)')
ax.set_ylabel('Dimension 2 (t-SNE)')
ax.legend(fontsize=12)
ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('/mnt/user-data/outputs/embeddings_tsne.png', dpi=150, bbox_inches='tight')
print("  Visualizacion t-SNE guardada en: embeddings_tsne.png")

# ============================================================================
# ANALISIS: Similitud Semantica (Simulado)
# ============================================================================

print("\n" + "=" * 70)
print("ANALISIS ADICIONAL: Analogias y Similitud (Simulado)")
print("=" * 70)

print("\nNota: En una aplicacion real con Word2Vec genuino, podrias hacer:")
print("  - w2v.similarity('gato', 'perro') -> similitud numerica")
print("  - w2v.most_similar('rey') -> palabras cercanas")
print("  - resolver_analogia('rey', 'hombre', 'mujer', w2v) -> 'reina'")

print("\nCon embeddings aleatorios (simulacion), esto no tiene sentido.")
print("Pero en clase, usarias Word2Vec pre-entrenado genuino.")

# ============================================================================
# RESUMEN Y LECCIONES
# ============================================================================

print("\n" + "=" * 70)
print("RESUMEN Y CONCLUSIONES")
print("=" * 70)

print("""
1. ARQUITECTURA EMBEDDINGS
   - Convierte one-hot (10,000 dims) -> densos (300 dims)
   - Relacion de compresion: 33x mas pequeno

2. RESULTADOS
   - Exactitud: {:.1%}
   - Metodo: Promediado simple de embeddings de palabra
   - Limitacion: Pierde orden de palabras

3. TRADE-OFFS
   - Promediado: Rapido pero informacion limitada
   - RNN/LSTM: Mas lento pero captura secuencias
   - Transformer: Mas costoso pero captura contexto bidireccional

4. PROXIMOS PASOS
   - Clase 3: RNN/LSTM para capturar orden
   - Clase 4: Attention mechanisms
   - Clase 5: Transformers (BERT, embeddings contextuales)

5. APLICACIONES REALES
   - Busqueda semantica (encontrar documentos similares)
   - Clasificacion de texto (sentimientos, spam, categorias)
   - Recomendaciones basadas en contenido
   - Deteccion de anomalias en texto
""".format(test_accuracy))

print("=" * 70)
print("Fin del script")
print("=" * 70)
