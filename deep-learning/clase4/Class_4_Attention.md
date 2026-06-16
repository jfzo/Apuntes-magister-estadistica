---
title: EST-744
subtitle: Mecanismos de Atención
author: Juan Zamora O.
date: Deep Learning
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
graphics: true
---

# Introducción

## El Problema: Cuello de Botella Secuencial

Las RNN procesan una palabra a la vez, creando un cuello de botella:

\begin{center}
\includegraphics[width=1.05\textwidth]{d1_rnn_bottleneck-1.png}
\end{center}

---

**Problemas**:

- No se puede paralelizar (hay que procesar en secuencia)
- El contexto lejano se desvanece (gradientes desvanecientes)
- Entrenamiento lento en secuencias largas

\vspace{0.3cm}

**¿Qué pasaría si cada palabra pudiera "mirar" a todas las demás al mismo tiempo?**

\vspace{0.5cm}

\footnotesize Vaswani et al. (2017), "Attention Is All You Need", NeurIPS. El artículo que introdujo los Transformers — disponible en \texttt{arxiv.org/abs/1706.03762}

# La Idea de la Atención

## Selección Suave

En lugar de leer de izquierda a derecha, la **atención** permite enfocarse en las palabras relevantes:

\begin{center}
\includegraphics[width=0.72\textwidth]{d2_soft_selection-1.png}
\end{center}

---

**Enfoque selectivo del mecanismo de Atención**:

| Componente | Pregunta que responde |
|---|---|
| **Consulta** (*Query*) $Q$ | "¿Qué estoy tratando de entender?" |
| **Clave** (*Key*) $K$ | "¿Qué es cada palabra?" |
| **Valor** (*Value*) $V$ | "¿Qué información contiene cada palabra?" |
| **Salida** | Promedio ponderado de las palabras relevantes |

\vspace{0.2cm}
\footnotesize Bahdanau, Cho \& Bengio (2015), "Neural Machine Translation by Jointly Learning to Align and Translate", ICLR. El artículo original de atención — \texttt{arxiv.org/abs/1409.0473}

# *Self-Attention*: Consulta, Clave, Valor

## Notación y su significado

$$\text{Atención}(Q, K, V) = \text{softmax}\!\left(\frac{QK^T}{\sqrt{d_k}}\right)V$$

\vspace{0.3cm}

**Paso a paso**:

1. **Consulta** $Q$: proyección lineal de la posición actual — "¿qué busco?"
2. **Producto** $QK^T$: similitud entre la consulta y cada clave — "¿cuánto encaja cada palabra?"
3. **Escala** $/ \sqrt{d_k}$: evita que los productos internos crezcan demasiado y saturen el softmax
4. **Softmax**: convierte similitudes en pesos de atención (entre 0 y 1, suman 1)
5. **Valores** $V$: combinación ponderada de los vectores de palabras

\vspace{0.2cm}
\footnotesize Vaswani et al. (2017), sección 3.2. Para una derivación paso a paso: Alammar (2018), "The Illustrated Transformer" — \url{https://jalammar.github.io/illustrated-transformer/}

# Ejemplo Numérico de Atención

## Ejemplo de Atención sobre "fue"

\begin{center}
\includegraphics[width=0.58\textwidth]{d3_qkv_example-1.png}
\end{center}


La representación final de "fue" incorpora información de toda la oración, especialmente de "genial" — capturando la relación semántica entre verbo y adjetivo.

# Atención Multi-Cabezal

## Múltiples Perspectivas Simultáneas

Una sola cabeza de atención no captura todas las relaciones posibles.

**Solución**: usar varias cabezas (*heads*), cada una aprendiendo patrones distintos:

\begin{center}
\includegraphics[width=0.70\textwidth]{d4_multihead-1.png}
\end{center}

---

Las salidas de todas las cabezas se **concatenan** y se proyectan linealmente:

$$\text{MultiHead}(Q,K,V) = \text{Concat}(\text{cabeza}_1, \ldots, \text{cabeza}_h)\, W^O$$

\vspace{0.3cm}

**¿Por qué múltiples cabezas?**
- Captura distintas dimensiones del significado en paralelo
- Robustez: si una cabeza falla, las demás compensan

\vspace{0.2cm}
\footnotesize Vaswani et al. (2017), sección 3.3. En el paper original se usan $h=8$ cabezas con $d_k = d_v = 64$.

# Paralelización: La Ventaja Clave

## RNN vs. Atención

\begin{center}
\includegraphics[width=0.75\textwidth]{d5_parallel-1.png}
\end{center}

| Métrica | RNN/LSTM | Atención |
|---|---|---|
| Procesamiento | Secuencial | **Paralelo** |
| Ganancia en velocidad | 1× (base) | **10–50×** en secuencias largas |
| Uso de GPU | Bajo (un paso a la vez) | **Alto** (todos los pares) |

# Codificación Posicional

## ¿Cómo Sabe la Atención el Orden?

La atención trata todas las palabras por igual: no tiene noción de posición.

\vspace{0.3cm}

**Problema**: "El perro mordió al hombre" ≠ "El hombre mordió al perro" producirían la misma representación sin información posicional.

\vspace{0.3cm}

**Solución**: sumar una **codificación posicional** (Positional Encoding) al embedding de cada palabra:

$$PE(\text{pos},\, 2i)   = \sin\!\left(\frac{\text{pos}}{10000^{2i/d}}\right)$$
$$PE(\text{pos},\, 2i+1) = \cos\!\left(\frac{\text{pos}}{10000^{2i/d}}\right)$$

---

Cada posición recibe un patrón sinusoidal único que varía a distintas frecuencias:

\begin{center}
\includegraphics[width=0.82\textwidth]{d9_positional_table-1.png}
\end{center}

\footnotesize El uso de sinusoides permite al modelo generalizar a secuencias más largas que las vistas en entrenamiento. Ver Vaswani et al. (2017), sección 3.5.

# El Bloque Transformer

## Las Piezas Ensambladas

\begin{center}
\includegraphics[width=0.62\textwidth]{d6_transformer_block-1.png}
\end{center}

---

**Conexión residual y normalización** (*Add & Norm*):

$$\text{Salida} = \text{LayerNorm}\!\left(x + \text{Atención}(x)\right)$$


**¿Por qué residual?** *Add* toma la entrada original de una capa y la suma directamente a la salida procesada de esa misma capa. Ayuda a preservar la información original y evita que se pierda a medida que el modelo se vuelve más profundo.

Luego se aplica una técnica de normalización al resultado combinado. Esto estabiliza el flujo de gradientes, evitando que sean demasiado grandes o pequeños.


\vspace{0.2cm}
\footnotesize He et al. (2016), "Deep Residual Learning for Image Recognition" — origen de las conexiones residuales, aplicadas luego a transformers.

# API de Atención en Keras

## Usar la Capa Incorporada

TensorFlow 2.x incluye `MultiHeadAttention` lista para usar:

```python
capa_atencion = keras.layers.MultiHeadAttention(
    num_heads=8,       # numero de cabezas independientes
    key_dim=64         # dimension por cabeza (total = key_dim x num_heads)
)

# Auto-atencion sobre si misma
salida = capa_atencion(query=x, value=x, key=x)
```


**Parámetros clave**:

| Parámetro | Significado | Valor típico |
|---|---|---|
| `num_heads` | Cabezas independientes | 4–16 |
| `key_dim` | Dimensión por cabeza | 32–128 |
| `dropout` | Regularización en los pesos | 0.1–0.3 |

El código completo del modelo, codificación posicional, entrenamiento y visualización está en **`clase_4_codigo_completo.py`**.


# Ejemplo Práctico: Clasificación de Sentimientos

## Tarea y Arquitectura

**Actividad**: clasificar reseñas de IMDb como positivas/negativas usando atención con la siguiente arquitectura.

\begin{center}
\includegraphics[width=0.45\textwidth]{d7_classifier-1.png}
\end{center}


# Rendimiento y Velocidad

## Ventajas de la atención

- Precisión comparable a LSTM
- Mucho más rápido (paralelizable)
- Mejor escalabilidad a secuencias largas
- **Interpretable**: los pesos de atención muestran en qué se enfocó el modelo


# Visualización de los Pesos de Atención

## ¿Qué Está Mirando el Modelo?

Los pesos de atención permiten **interpretar** las decisiones del modelo:

\vspace{0.2cm}

\begin{center}
\includegraphics[width=0.55\textwidth]{d8_attention_heatmap-1.png}
\end{center}

## Relevancia de este mecanismo

Interpretabilidad es una ventaja concreta sobre LSTM, donde los estados ocultos son difíciles de leer directamente.

La atención es el **mecanismo central** de BERT, GPT y todos los modelos modernos de NLP. Comprender su funcionamiento es imprescindible para la Clase 5.


\vspace{0.2cm}
\footnotesize *Clark et al. (2019), "What Does BERT Look at?", ACL. Análisis detallado de qué aprenden las cabezas de atención en modelos pre-entrenados.*


# Problemas Comunes

## Diagnóstico

| Problema | Causa | Solución |
|---|---|---|
| Toda la atención a una sola palabra | Entrenamiento insuficiente | Entrenar más épocas; aumentar tasa de aprendizaje |
| Atención uniforme (sin foco) | Modelo muy simple | Agregar más cabezas o capas más profundas |
| Error de memoria | Muchas cabezas × dimensiones altas | Reducir `key_dim` o `num_heads` |
| Entrenamiento lento | Implementación ineficiente | Usar capas integradas de Keras, no implementación manual |
| Sobreajuste severo | Pocos datos o modelo muy grande | Agregar `dropout` en atención y capas densas |


# Cierre

Los mecanismos de atención permiten que cada palabra "vea" a todas las demás de forma instantánea y paralela

Esta combinación de expresividad y eficiencia computacional es la razón por la que los Transformers dominan las aplicaciones modernas de NLP



# Referencias

## Para Profundizar

- **Vaswani et al. (2017).** "Attention Is All You Need." *NeurIPS*. \texttt{arxiv.org/abs/1706.03762} — El artículo fundacional de los Transformers; lectura obligatoria.

- **Bahdanau, Cho \& Bengio (2015).** "Neural Machine Translation by Jointly Learning to Align and Translate." *ICLR*. \texttt{arxiv.org/abs/1409.0473} — Origen del mecanismo de atención para secuencias.

- **Alammar, J. (2018).** "The Illustrated Transformer." \texttt{jalammar.github.io/illustrated-transformer} — La explicación visual más recomendada; sin necesidad de código previo.

- **Goodfellow, Bengio \& Courville (2016).** *Deep Learning*, Cap. 12. MIT Press. \texttt{deeplearningbook.org} — Marco teórico de modelos de secuencias.

- **Clark et al. (2019).** "What Does BERT Look at?" *ACL Workshop*. \texttt{arxiv.org/abs/1906.04341} — Análisis empírico de qué aprenden las cabezas de atención.

- **He et al. (2016).** "Deep Residual Learning for Image Recognition." *CVPR*. \texttt{arxiv.org/abs/1512.03385} — Origen de las conexiones residuales usadas en el bloque Transformer.





# Ejercicios para la Clase 4

## Tareas Prácticas

1. **Visualizar atención**: obtener pesos de atención para 10 reseñas. ¿Los patrones tienen sentido lingüístico?

2. **Variar `num_heads`**: probar 2, 4, 8 y 16 cabezas. ¿Más siempre es mejor?

3. **Comparar con LSTM**: entrenar LSTM con los mismos hiperparámetros. ¿Cuánto gana la atención en velocidad?

4. **Ablación posicional**: entrenar sin codificación posicional. ¿Cuánto impacta en la precisión?

5. **Interpretabilidad**: para reseñas mal clasificadas, ¿qué atendió el modelo? ¿Explica el error?

6. **Escala**: entrenar con secuencias de largo 100, 500 y 1000. Comparar tiempo de época: Atención vs. LSTM.
