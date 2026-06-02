---
title: EST-744
subtitle: Embeddings y Aprendizaje de Representaciones
author: Juan Zamora O.
date: Deep Learning para Estadísticos
fonttheme: "professionalfonts"
fontsize: 11pt
theme: default
innertheme: circles
urlcolor: blue
linkstyle: bold
aspectratio: 169
titlegraphic: logosAzul.png
logo: logoAzul.png
section-titles: false
toc: false
toc-depth: 1
toc-title: Estructura de la Presentación
---


# Introducción

## El Problema: El Texto es Simbólico

¿Cómo alimentamos palabras a redes neuronales?

\vspace{0.3cm}

El desafío fundamental es que las palabras son símbolos discretos sin estructura numérica inherente. Las redes neuronales operan sobre números y geometrías continuas. Necesitamos construir un puente.

---

**Enfoques tradicionales** (insuficientes):

- **Codificación one-hot**: "gato" → [0, 0, ..., 1, 0, ..., 0] 
  - Vocabulario de 10,000 palabras = 10,000 dimensiones
  - No captura relaciones semánticas (todas las palabras equidistantes)
  - Vectores enormes y dispersos (99.99% ceros)
  - Desperdicia la estructura subyacente del lenguaje

\vspace{0.3cm}

**Insight fundamental**: Aprender representaciones densas donde el significado se codifica en la **geometría** del espacio de vectores, no en la presencia/ausencia de dimensiones




# Embeddings: De Símbolos a Números

## La Idea Central

Un **embedding** es un mapeo aprendido que transforma cada palabra en un vector denso de dimensionalidad mucho menor (típicamente 50-300).

\vspace{0.3cm}

```
"gato"   → [0.23, -0.15, 0.08, ..., 0.42]    (300 dimensiones)
"perro"  → [0.25, -0.13, 0.07, ..., 0.41]
"rey"    → [0.12,  0.45, -0.22, ..., 0.61]
"reina"  → [0.10,  0.50, -0.20, ..., 0.58]
```

\vspace{0.3cm}

**Propiedad emergente**: Palabras similares tienen vectores cercanos en el espacio

**¿Por qué funciona?** La distancia euclidiana entre vectores codifica similitud semántica: 
$$\text{similaridad} \propto \frac{1}{1 + \text{distancia}}$$

## La Hipótesis Distribucional

**"Conocerás una palabra por la compañía que frecuenta"** (Firth, 1957)

\vspace{0.3cm}

**Principio linguístico**: Palabras que aparecen en contextos similares tienen significados similares

\vspace{0.2cm}

**Ejemplo práctico**:
- "gato" aparece con: "mascota", "ronroneo", "felino", "suave"
- "perro" aparece con: "mascota", "ladrido", "canino", "leal"
- **Contexto compartido** → los vectores deberían ser cercanos

\vspace{0.2cm}

Este principio es el fundamento teórico de todos los métodos modernos de embeddings.


# Word2Vec: Aprendiendo Embeddings

## Idea Central del Modelo Skip-Gram

En lugar de tratar de predecir la siguiente palabra (como en un modelo de lenguaje), **predecimos las palabras contextuales a partir de la palabra objetivo**.

\vspace{0.3cm}

```
Oración: "Adoro mi [gato] muy tierno"
         Contexto: "Adoro", "mi", "muy", "tierno"
         Objetivo: "gato"
         
Tarea: Dado "gato" → predecir palabras contextuales
```

\vspace{0.3cm}

**Arquitectura de la red**:
1. Entrada: palabra objetivo codificada one-hot
2. Capa oculta: matriz de embeddings $W \in \mathbb{R}^{|V| \times d}$ (|V| = vocab, d = dim embedding)
3. Salida: distribución de probabilidad sobre palabras contextuales

\vspace{0.2cm}

**Truco elegante**: Después del entrenamiento, descartamos la capa de salida y usamos los **pesos de la capa oculta como embeddings**.



## Proceso de Entrenamiento

1. **Extracción de pares**: Recorrer el corpus con ventana de contexto (ej: 5 palabras a cada lado)

2. **Construcción de ejemplos**: Para cada palabra objetivo, generar pares (objetivo, contexto)

3. **Optimización**: Maximizar probabilidad de palabras contextuales dada la palabra objetivo
   $$\mathcal{L} = -\sum_{t=1}^{T} \sum_{-m \leq j \leq m, j \neq 0} \log P(w_{t+j} | w_t)$$
   
4. **Emergencia de estructura**: La red aprende automáticamente que palabras similares tienen vectores similares

5. **Resultado**: Vectores que capturan relaciones semánticas y sintácticas



# Relaciones Semánticas en Embeddings

## Operaciones Vectoriales Significativas

Los embeddings capturan no solo similitud, sino **relaciones funcionales**:

$$\text{rey} - \text{hombre} + \text{mujer} \approx \text{reina}$$

---

**¿Por qué funciona?**

Piensa en cada dimensión del embedding como codificar un atributo semántico (no interpretable directamente, pero existe):

- "rey" tiene componentes de "autoridad" + "masculinidad"
- "hombre" codifica principalmente "masculinidad"  
- Restar "hombre" elimina el componente de masculinidad
- Sumar "mujer" añade "feminidad"
- Resultado: "autoridad" + "feminidad" ≈ "reina"

---

**Otras relaciones capturadas**:
- París - Francia + Londres ≈ Inglaterra (relaciones geográficas)
- malo - bueno ≈ triste - feliz (analogías de sentimiento)
- programador - programación + música ≈ músico (roles vs. dominios)

\vspace{0.2cm}

**Advertencia importante**: No todas las relaciones se preservan perfectamente. Las operaciones vectoriales son aproximadas, especialmente para conceptos abstractos.



# Métodos Pre-entrenados: Word2Vec, GloVe, FastText

## Comparación de Alternativas

No se entrena embeddings desde cero; se usan modelos pre-entrenados en corpus masivos:

| Método | Dimensiones | Corpus | Ventajas | Limitaciones |
|--------|------------|--------|----------|--------------|
| **Word2Vec** | 300 | Google News (3B palabras) | Rápido, intuitivo, eficiente | Palabras OOV desconocidas |
| **GloVe** | 300 | Wikipedia + Gigaword (6B) | Equilibra contexto local y global | Más lento en entrenamiento |
| **FastText** | 300 | Common Crawl (840B) | Maneja OOV via subpalabras | Archivos grandes (~7 GB) |

---

**¿Cuál elegir?**

- **Word2Vec**: Baseline rápida, buena para tareas generales
- **GloVe**: Si importa equilibrio entre contexto inmediato y correlaciones globales
- **FastText**: Cuando hay palabras raras, idiomas morfológicamente ricos, o necesitas robusted

\vspace{0.2cm}

**Para este curso**: Usaremos `gensim` (Word2Vec) por simplicidad e interpretabilidad


# Capas de Embeddings en Redes Neuronales

## Integrando Embeddings en Modelos Deep Learning

En lugar de mandar one-hot encoding a la red, usamos una **capa de embeddings** que actúa como tabla de búsqueda:

```python
keras.layers.Embedding(
    input_dim=vocab_size,      # ¿Cuántas palabras en vocabulario?
    output_dim=embedding_dim,   # Dimensionalidad del embedding (ej: 128)
    input_length=max_length     # Largo máximo de secuencia
)
```

---

**Flujo de datos**:

1. **Tokenización**: "el gato duerme" → [3, 42, 157]
2. **Embedding layer**: [3, 42, 157] → matriz de shape (3, embedding_dim)
   - Fila 0: embedding de palabra con índice 3
   - Fila 1: embedding de palabra con índice 42
   - Fila 2: embedding de palabra con índice 157
3. **Propagación**: Esta matriz se pasa a capas posteriores (LSTM, CNN, etc.)

---

**Dos estrategias**:

1. **Aprender from scratch**: Si tienes mucho datos etiquetados
   - La capa de embeddings se optimiza junto con toda la red
   - `trainable=True`

2. **Transfer learning** (recomendado): Cargar pre-entrenados y fine-tunear
   - Inicializar con Word2Vec/GloVe
   - `trainable=True` solo si dataset es suficientemente grande
   - Típicamente: `trainable=False` para datasets pequeños

---

# Agregación a Nivel de Documento

## Del Nivel de Palabra al Documento

Los embeddings word-level son poderosos, pero ¿cómo representamos documentos completos?

\vspace{0.3cm}

### Opción 1: Promediado Simple

```
oración = "el gato es muy feliz"
embedding_documento = mean([emb(el), emb(gato), emb(es), emb(muy), emb(feliz)])
```

**Pros**: Simple, rápido, funciona sorprendentemente bien
**Contras**: Pierde orden de palabras ("no bueno" = "bueno no")

---

### Opción 2: Promediado Ponderado (TF-IDF)

$$\text{emb}_{\text{doc}} = \frac{\sum_i \text{tfidf}_i \cdot \text{emb}_i}{\sum_i \text{tfidf}_i}$$

Palabras comunes (artículos) contribuyen menos; palabras discriminativas contribuyen más.

**Pros**: Mitiga el impacto del ruido
**Contras**: Aún pierde información de orden

---

### Opción 3: Pooling Aprendido

Permitir que la red aprenda cómo combinar embeddings de palabra:
- **Max pooling**: Tomar el máximo por dimensión
- **Attention pooling**: Aprender pesos de importancia (veremos en clases posteriores)

**Pros**: Más flexible y adaptativo
**Contras**: Requiere más datos de entrenamiento




# Ejemplo Práctico: Clasificación de Sentimientos

## Descripción de la Tarea

**Objetivo**: Predecir si una reseña de película es positiva o negativa

**Dataset**: IMDb (25,000 reseñas para entrenamiento, 25,000 para prueba)

**Pipeline propuesto**:
1. Cargar embeddings pre-entrenados (Word2Vec)
2. Tokenizar y convertir reseñas a secuencias de índices
3. Agregar embeddings (promedio simple)
4. Alimentar a clasificador simple (capas Dense)

\vspace{0.3cm}

**Expectativa**: ~85-90% de exactitud (limitado por promediado)

---

# Código: Preparación de Embeddings

## Cargando Embeddings Pre-entrenados

```python
from gensim.models import KeyedVectors
import numpy as np

# Cargar Word2Vec pre-entrenado (Google News)
# Nota: Descarga requiere ~1.5 GB
w2v = KeyedVectors.load_word2vec_format(
    'GoogleNews-vectors-negative300.bin', binary=True
)

# Verificar que funcionó
print(f"Vocabulario: {len(w2v)}")  # ~3 millones palabras
print(f"Dimensionalidad: {w2v.vector_size}")  # 300

# Probar similitud
print(w2v.similarity('gato', 'perro'))  # ~0.8 (muy similar)
print(w2v.similarity('gato', 'coche'))  # ~0.1 (poco similar)
```


## Construyendo Matriz de Embeddings para Nuestro Vocabulario

```python
# Crear matriz de embeddings para nuestro vocabulario específico
vocab_size = 10000
embedding_dim = 300
word_index = {}  # palabra -> índice
embedding_matrix = np.zeros((vocab_size, embedding_dim))

# Poblar matriz: palabras conocidas usan pre-entrenados,
# palabras desconocidas inicializan aleatoriamente
for idx, word in enumerate(word_list[:vocab_size]):
    word_index[word] = idx
    if word in w2v:
        # Palabra conocida: copiar embedding pre-entrenado
        embedding_matrix[idx] = w2v[word]
    else:
        # Palabra desconocida: inicializar de N(0, 1)
        embedding_matrix[idx] = np.random.normal(
            loc=0, scale=0.5, size=embedding_dim
        )

print(f"Matriz de embeddings: {embedding_matrix.shape}")
# (10000, 300)
```



# Código: Modelo de Clasificación

## Pipeline Completo con Embeddings Promediados

```python
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import numpy as np

# ============================================
# 1. CARGA DE DATOS
# ============================================
(x_train, y_train), (x_test, y_test) = \
    keras.datasets.imdb.load_data(num_words=10000)

# IMDb devuelve secuencias de índices de palabras
# x_train[0] es una lista de enteros: [1, 14, 22, 16, ...]
print(f"Shape de entrada: {x_train[0].shape}")  # (variable)

# ============================================
# 2. CONVERSIÓN A EMBEDDINGS PROMEDIADOS
# ============================================
def sequences_to_embeddings(sequences, embedding_matrix, max_length=None):
    """Convierte secuencias de índices a vectores promediados"""
    embeddings = []
    for seq in sequences:
        # Obtener embeddings de cada palabra en la secuencia
        seq_emb = embedding_matrix[seq]
        # Promediar sobre todas las palabras
        doc_emb = seq_emb.mean(axis=0)
        embeddings.append(doc_emb)
    return np.array(embeddings)

x_train_emb = sequences_to_embeddings(x_train, embedding_matrix)
x_test_emb = sequences_to_embeddings(x_test, embedding_matrix)

print(f"Embeddings train: {x_train_emb.shape}")  # (25000, 300)
print(f"Embeddings test: {x_test_emb.shape}")    # (25000, 300)

# ============================================
# 3. DEFINICIÓN DEL MODELO
# ============================================
model = keras.Sequential([
    # Capa oculta con regularización
    layers.Dense(128, activation='relu', input_shape=(embedding_dim,)),
    layers.Dropout(0.3),
    
    # Segunda capa
    layers.Dense(64, activation='relu'),
    layers.Dropout(0.2),
    
    # Salida binaria (positivo/negativo)
    layers.Dense(1, activation='sigmoid')
])

# ============================================
# 4. COMPILACIÓN Y ENTRENAMIENTO
# ============================================
model.compile(
    loss='binary_crossentropy',
    optimizer='adam',
    metrics=['accuracy']
)

history = model.fit(
    x_train_emb, y_train,
    epochs=15,
    batch_size=32,
    validation_split=0.2,
    verbose=1
)

# ============================================
# 5. EVALUACIÓN
# ============================================
test_loss, test_accuracy = model.evaluate(x_test_emb, y_test)
print(f"\nTest Loss: {test_loss:.4f}")
print(f"Test Accuracy: {test_accuracy:.4f}")

# Ver predicciones en muestra pequeña
predictions = model.predict(x_test_emb[:5])
for i in range(5):
    pred_label = "Positiva" if predictions[i][0] > 0.5 else "Negativa"
    true_label = "Positiva" if y_test[i] == 1 else "Negativa"
    print(f"Predicción: {pred_label}, Real: {true_label}")
```

**Resultado esperado**: ~86-89% de exactitud




# Visualización: Inspeccionando Embeddings

## Visualización con t-SNE

Los embeddings viven en espacios de 300 dimensiones. Para visualizar, usamos **t-SNE** (t-Distributed Stochastic Neighbor Embedding), que preserva distancias locales.

\vspace{0.2cm}

```python
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt

# Reducir a 2D (puede tomar minutos)
tsne = TSNE(n_components=2, random_state=42, 
            perplexity=30, n_iter=1000)
embeddings_2d = tsne.fit_transform(embedding_matrix[:2000])

# Graficar
fig, ax = plt.subplots(figsize=(14, 10))
ax.scatter(embeddings_2d[:, 0], embeddings_2d[:, 1], 
           alpha=0.4, s=20, color='steelblue')

# Anotaciones para palabras seleccionadas
interesting_words = ['gato', 'perro', 'rey', 'reina', 'Francia', 
                     'París', 'bueno', 'malo', 'película', 'actor']
for word in interesting_words:
    if word in word_index and word_index[word] < 2000:
        idx = word_index[word]
        ax.annotate(word, 
                   (embeddings_2d[idx, 0], embeddings_2d[idx, 1]),
                   fontsize=9, fontweight='bold',
                   bbox=dict(boxstyle='round,pad=0.3', 
                            facecolor='yellow', alpha=0.5))

ax.set_title('Visualización de Embeddings (t-SNE)', fontsize=14)
ax.set_xlabel('Dimensión 1 (t-SNE)')
ax.set_ylabel('Dimensión 2 (t-SNE)')
plt.tight_layout()
plt.show()
```

\vspace{0.2cm}

**Qué observar**: Palabras relacionadas deberían formar clusters (animales, números, adjetivos, etc.)




# Pruebas de Analogías: Validación de Calidad

## Función para Resolver Analogías

```python
def resolver_analogia(w1, w2, w3, modelo, top_n=5):
    """
    Resuelve: w1 es a w2 como w3 es a ?
    
    Ejemplo: "rey" es a "hombre" como "reina" es a ?
    """
    try:
        resultados = modelo.most_similar(
            positive=[w2, w3],
            negative=[w1],
            topn=top_n
        )
        return resultados
    except KeyError as e:
        return f"Palabra desconocida: {e}"

# ============================================
# PRUEBAS DE RELACIONES SEMÁNTICAS
# ============================================

# Relaciones de género
print("=== Relaciones de Género ===")
print("rey - hombre + mujer ≈ ?")
print(resolver_analogia("rey", "hombre", "mujer", w2v))
# Esperado: [('reina', 0.75), ...]

# Relaciones geográficas
print("\n=== Relaciones Geográficas ===")
print("París - Francia + Londres ≈ ?")
print(resolver_analogia("París", "Francia", "Londres", w2v))
# Esperado: [('Inglaterra', 0.70), ('Gran Bretaña', 0.65), ...]

# Relaciones de familia
print("\n=== Relaciones de Familia ===")
print("padre - hombre + mujer ≈ ?")
print(resolver_analogia("padre", "hombre", "mujer", w2v))
# Esperado: [('madre', 0.80), ...]

# Relaciones de profesión
print("\n=== Relaciones de Profesión ===")
print("doctor - medicina + ley ≈ ?")
print(resolver_analogia("doctor", "medicina", "ley", w2v))
# Esperado: [('abogado', 0.65), ...]

# ============================================
# ANÁLISIS DE FALLOS
# ============================================

# No todas las analogías funcionan
print("\n=== Analogías que Típicamente Fallan ===")
print("grande - grande + pequeño ≈ ?")
print(resolver_analogia("grande", "grande", "pequeño", w2v))
# Problema: Conceptos abstractos comparativos son difíciles
```



# Conceptos Clave: Resumen

## Las Cuatro Ideas Centrales

1. **One-hot encoding es ineficiente**
   - Espacios enormes y dispersos
   - No captura similitud semántica
   
2. **Embeddings codifican significado en geometría**
   - Palabras similares → vectores cercanos
   - Relaciones semánticas → operaciones vectoriales
   - Compresión: 10k dims → 300 dims

3. **Distributional hypothesis como fundamento**
   - Contexto similar → palabras similares
   - Aprender de corpus no etiquetado (unsupervised)

4. **Transfer learning es estándar**
   - No entrenar embeddings desde cero
   - Usar pre-entrenados (Word2Vec, GloVe, FastText)
   - Fine-tune según necesidad



## Por Qué Importan los Embeddings

- **Compacidad**: 300 dimensiones vs. 10,000+ dimensiones one-hot
- **Significado**: Capturan relaciones semánticas reales
- **Transferibilidad**: Úsalos en múltiples tareas
- **Eficiencia**: Pre-entrenados, listos para usar



# Limitaciones y Problemas Comunes

## Tabla de Troubleshooting

| Problema | Causa Raíz | Solución |
|----------|-----------|----------|
| **Palabras OOV** | Vocabulario pre-entrenado no cubre palabra rara | Usar FastText (subpalabras) o reentrenar |
| **Baja exactitud** | Promediado pierde orden y contexto | Usar RNN/LSTM (próxima clase) |
| **Archivos grandes** | Embeddings completos pesan GB | Usar dimensiones menores (50-100) |
| **Overfitting** | Dataset pequeño + modelo complejo | Congelar embeddings (`trainable=False`) |
| **Sin diferenciación** | Todas las palabras se mapean igual | Revisar: ¿matriz inicializada correctamente? |
| **Analogías falsas** | Relaciones ruidosas en embeddings | Entrenados en corpus sesgado (revisar datos) |

\vspace{0.2cm}

**Lección**: Los embeddings pre-entrenados no son mágicos. Heredan sesgos y limitaciones del corpus de entrenamiento.



# Ejercicios Propuestos

## Actividades Hands-On

1. **Comparación de embeddings**
   - Carga Word2Vec y GloVe
   - Compara resultados en tareas de analogía
   - ¿Cuál es mejor para tu dominio?

2. **Estudio de dimensionalidad**
   - Entrena modelos con embeddings de 50, 100, 200, 300 dims
   - ¿Hay punto de saturación?
   - Trade-off: exactitud vs. velocidad

3. **Frozen vs. Trainable**
   - Modelo A: embeddings congelados (`trainable=False`)
   - Modelo B: embeddings ajustables (`trainable=True`)
   - ¿Cuál generaliza mejor en dataset pequeño?

---

4. **Caza de analogías**
   - Encuentra 10 analogías que funcionan bien
   - Encuentra 5 que fallan
   - Analiza por qué fallan

5. **Visualización t-SNE**
   - Visualiza 3000+ embeddings
   - Identifica clusters semanticos
   - Describe patrones observados

6. **Pooling alternativo**
   - Implementa max pooling: `seq_emb.max(axis=0)`
   - Implementa weighted pooling con TF-IDF
   - Compara exactitud vs. promediado simple




# Conexión con la Próxima Clase

## Limitaciones Actuales

El promediado de embeddings funciona, pero ignora:

- **Orden de palabras**: "no bueno" vs. "bueno no" → mismo embedding
- **Contexto variable**: Mismo verbo con significados diferentes según contexto
- **Dependencias a largo plazo**: Relaciones entre palabras lejanas

---

**Ejemplo de limitación**:

Oración 1: "Este película **no es** buena" → promedio ≈ "negativo"
Oración 2: "Esta película es **muy** buena" → promedio ≈ "positivo"

Cambio de una palabra invierte sentimiento, pero promediado es sensible.


## Solución: Modelos Secuenciales

**Clase 3: Clasificación de Texto con RNNs/LSTMs**

- Procesar palabras **en orden**
- Recordar contexto acumulativo a través de secuencias
- Capturar dependencias a largo plazo
- Mejora esperada: 89% → 95%+


# Referencias y Lecturas Recomendadas

## Papers Clásicos

- **Mikolov et al. (2013)**. "Efficient Estimation of Word Representations in Vector Space". ICLR. [Word2Vec original]

- **Pennington, Socher & Manning (2014)**. "GloVe: Global Vectors for Word Representation". EMNLP. [GloVe]

- **Firth, J. R. (1957)**. "A Synopsis of Linguistic Theory". Studies in Linguistic Analysis. [Hipótesis distribucional]



## Recursos Implementación

- **Gensim**: https://radimrehurek.com/gensim/
- **Spacy**: https://spacy.io/
- **TensorFlow Embedding Layer**: https://www.tensorflow.org/api_docs/python/tf/keras/layers/Embedding

\vspace{0.2cm}

## Visualización y Análisis

- **TensorBoard**: Visualización interactiva de embeddings (projector.tensorflow.org)
- **t-SNE**: van der Maaten & Hinton (2008), "Visualizing Data using t-SNE"



# Discusión Final

## Lecciones clave

**Los embeddings transforman lo simbólico en geométrico.**

\vspace{0.3cm}

Pasamos de:

- Palabras como etiquetas sin relación → **Palabras como puntos en un espacio semántico**
- Diccionarios discretos → **Espacios continuos con estructura**
- Vocabulario cerrado → **Capacidad de generalización a palabras nuevas** (especialmente FastText)


Este puente entre lenguaje y geometría es lo que permite a las redes neuronales razonar sobre significado.




## Próximas Preguntas

¿Cómo capturamos **orden y contexto** dinámico?

¿Cómo manejamos **ambigüedad** (misma palabra, múltiples significados)?

¿Cómo escalamos a **idiomas morfológicamente complejos**?

→ **Respuestas en clases futuras con RNNs, Transformers y embeddings contextuales (ELMo, BERT)**

---

# Preguntas y Discusión

Gracias por la atención.

**Preguntas frecuentes**:
- ¿Puedo combinar múltiples esquemas de embeddings?
- ¿Qué pasa si mi idioma no tiene embeddings pre-entrenados?
- ¿Cómo detecto y mitigo sesgos en embeddings?

**Siguiente**: Deep dive en RNNs para procesamiento secuencial.
