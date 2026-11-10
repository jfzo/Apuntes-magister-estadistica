---
title: EST-852
subtitle: Métodos de Kernel y SVM en la Práctica
author: Juan Zamora O.
date: Machine Learning
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
graphics: true
linespread: 1.2
---

# Preguntas iniciales

## Respondamos antes de comenzar

1. ¿Qué es un **vector soporte**?
2. ¿Qué controlan los parámetros **$C$** y **$\gamma$**?
3. ¿Para qué sirve el **truco del kernel**?


## Pregunta guía de la sesión

Un modelo muestra 95 % de exactitud.

**¿Cómo podemos confiar en que este comportamiento se repetirá sobre datos nuevos?**


## Pregunta guía de la sesión

Un modelo muestra 95 % de exactitud.

> **¿Cómo podemos confiar en que este comportamiento se repetirá sobre datos nuevos?**

En esta sesión :

- ¿Qué parámetros se eligieron y cómo?
- ¿Qué se mide además de la exactitud?
- ¿Qué pasa si los errores no tienen el mismo costo?
- ¿Con qué datos se midió y con cuáles se eligió el modelo?


# Respuestas a las preguntas iniciales

## 1. Vector soporte

Un **vector soporte** es un punto de entrenamiento con multiplicador $\alpha_i>0$ en el problema dual. Solo estos puntos determinan la frontera:

$$f(\xv)=\sum_{i\in SV}\alpha_i y_i\,k(\xv_i,\xv)+b$$

| Tipo de punto | Condición | Posición |
|:--|:--|:--|
| $\alpha_i=0$ | $y_if(\xv_i)\ge1$ | Fuera del margen, bien clasificado. No influye |
| $0<\alpha_i<C$ | $y_if(\xv_i)=1$ | Exactamente sobre el margen |
| $\alpha_i=C$ | $y_if(\xv_i)\le1$ | Dentro del margen o mal clasificado |

Los puntos mal clasificados siempre son vectores soporte (ESL, §12.2, p. 421).

## 2. Qué controlan $C$ y $\gamma$

- **$C$** pondera las violaciones del margen frente al ancho del margen. $C$ pequeño produce un margen más ancho y $C$ grande penaliza más las violaciones (ESL, §12.2).
- **$\gamma$** es el parámetro del kernel gaussiano $k(x,x')=\exp(-\gamma\norm{x-x'}^2)$ y fija el alcance de la influencia de cada punto. 
    - $\gamma$ grande es una influencia local, $\gamma$ pequeño influencia amplia.
- Ambos son **hiperparámetros**: no los estima el algoritmo, se eligen con datos en la etapa de validación.

## 3. Truco del kernel

- El dual depende de los datos solo mediante productos internos $\ip{\xv_i}{\xv_j}$.
- Una función $k$ semidefinida positiva equivale a un producto interno en un espacio de características: $k(x,x')=\ip{\Phi(x)}{\Phi(x')}$.
- Al reemplazar $\ip{\xv_i}{\xv_j}$ por $k(\xv_i,\xv_j)$ se obtiene una frontera no lineal **sin calcular $\Phi$**.
- Kernels usuales: lineal, polinomial de grado $p$ y radial (gaussiano)
- En ESL (§12.3.1) también menciona el kernel de red neuronal, que no siempre es semidefinido positivo.

## Respuesta a la pregunta guía

Para confiar en el desempeño alcanzado por un modelo se necesita:

1. **Datos de evaluación independientes:** la cifra proviene de datos que no se usaron para entrenar ni para elegir parámetros.
2. **Parámetros elegidos sin mirar esos datos:** mediante validación cruzada sobre el entrenamiento.
3. **Una referencia:** comparación con la línea base y con un modelo simple.
4. **Errores desglosados por clase:** no solo la exactitud, porque los errores pueden tener costos distintos.
5. **Una medida de incertidumbre:** el tamaño del conjunto de evaluación limita la precisión de la cifra.

# Parámetros de la SVM y su efecto

## Parámetros involucrados

| Parámetro | Qué controla | Al aumentarlo |
|:--|:--|:--|
| Kernel | Forma posible de la frontera | Lineal: recta. Polinomial y radial: frontera curva |
| $C$ | Penalización de las violaciones del margen | Margen más estrecho, menos violaciones, menos vectores soporte |
| $\gamma$ (radial) | Alcance de cada punto | Frontera más local y flexible; riesgo de sobreajuste |
| Grado $p$ (polinomial) | Complejidad del polinomio | Frontera más flexible (ESL, §7.2)|



## $C$: formulación y convención

Margen suave con variables de holgura $\xi_i\ge0$:

$$\min_{\wv,b,\xi}\ \tfrac12\norm{\wv}^2+C\sum_{i=1}^m\xi_i\quad\text{s.a.}\quad y_i\big(\ip{\wv}{\xv_i}+b\big)\ge1-\xi_i$$

Forma equivalente de pérdida más penalización, con la pérdida *hinge*:

$$\min_{\wv,b}\ \sum_{i=1}^m\big[1-y_if(\xv_i)\big]_+ +\frac{\lambda}{2}\norm{\wv}^2,\qquad \lambda=\frac1C$$

(ESL, §12.3.2, p. 426). Por tanto, $C$ grande equivale a poca regularización.


## Efecto de $C$: ejemplo con dos lunas

Kernel radial con $\gamma=1$; 210 puntos de entrenamiento y 90 de prueba.

| $C$ | Vectores soporte | Exactitud entrenamiento | Exactitud prueba |
|:--|--:|--:|--:|
| 0,01 | 210 | 0,857 | 0,767 |
| 1 | 67 | 0,933 | 0,922 |
| 100 | 41 | 0,938 | 0,944 |

- $C$ pequeño: todos los puntos son vectores soporte y la frontera es casi lineal.
- $C$ grande: menos vectores soporte y frontera más ajustada a los datos.
- La diferencia entre $C=1$ y $C=100$ en prueba no es concluyente.

## Kernel y forma de la frontera

Dos lunas, $C=1$ y parámetros por defecto de cada kernel:

| Kernel | Vectores soporte | Exactitud entrenamiento | Exactitud prueba |
|:--|--:|--:|--:|
| Lineal | 76 | 0,857 | 0,767 |
| Polinomial (grado 3) | 95 | 0,886 | 0,822 |
| Radial | 66 | 0,933 | 0,900 |

- El kernel lineal solo traza una recta, polinomial y radial curvan la frontera.
- Un kernel más flexible no siempre es mejor, depende de la estructura de los datos y se decide con la validación (más adelante).


## Efecto de $\gamma$ en el kernel radial

Dos lunas, $C=1$:

| $\gamma$ | Vectores soporte | Exactitud entrenamiento | Exactitud prueba |
|:--|--:|--:|--:|
| 0,1 | 93 | 0,848 | 0,744 |
| 1 | 67 | 0,933 | 0,922 |
| 50 | 177 | 0,976 | 0,944 |

---

*Breast cancer* (30 variables, estandarizadas, $C=1$): con $\gamma=1$ hay 397 vectores soporte de 398 puntos, exactitud de entrenamiento 1,000 y de prueba 0,632, igual a la línea base. El modelo memoriza el entrenamiento.

- Señales de sobreajuste: brecha entre entrenamiento y prueba y aumento del número de vectores soporte.
- En el ejemplo de dos lunas, $\gamma=50$ no empeora en prueba (90 casos): una sola partición pequeña no basta para decidir.

## $C$ y $\gamma$ interactúan

Exactitud en validación cruzada (5 folds), *breast cancer* estandarizado:

| $C\backslash\gamma$ | 0,001 | 0,01 | 0,1 | 1 |
|:--|--:|--:|--:|--:|
| 0,1 | 0,696 | 0,942 | 0,942 | 0,628 |
| 1 | 0,950 | 0,972 | 0,970 | 0,628 |
| 10 | 0,975 | 0,982 | 0,967 | 0,633 |
| 100 | 0,990 | 0,987 | 0,967 | 0,633 |

- Con $\gamma=1$ ningún valor de $C$ compensa: el rendimiento queda en la línea base. Con $\gamma$ pequeño, $C$ pequeño produce un modelo demasiado rígido (0,696).
- Se eligen **conjuntamente**, en una grilla logarítmica.

## Escala de las variables

El kernel radial depende de $\norm{x-x'}^2$: una variable de escala grande domina la distancia.

*Breast cancer*: las variables van de $\approx0{,}03$ (`smoothness error`) a $\approx4000$ (`worst area`).

| Kernel | Exactitud en prueba sin estandarizar | Estandarizando |
|:--|--:|--:|
| Lineal | 0,942 | 0,953 |
| Radial | 0,906 | 0,953 |

- La estandarización debe ajustarse **solo con el entrenamiento**: dentro de un `Pipeline` (más adelante en validación).
- Cuando las variables ya comparten escala estandarizar no es necesariamente mejor.

# Métricas de evaluación

## Error de entrenamiento y error de prueba

- El **error de prueba** (de generalización) es el error esperado sobre datos nuevos, cuando el modelo ya se ajustó con un conjunto de entrenamiento dado.
- Disminuye al aumentar la complejidad. Un modelo con error de entrenamiento nulo suele estar sobreajustado y generaliza mal (ESL, §7.2).
- Por eso el desempeño se mide con datos que no participaron en el ajuste.
- La exactitud es una sola cifra y oculta qué tipo de error se comete.

## Matriz de confusión

Se define una clase **positiva** (aquí: tumor maligno, la clase de interés).

| | Predicho positivo | Predicho negativo |
|:--|:--:|:--:|
| **Real positivo** | Verdaderos positivos (VP) | Falsos negativos (FN) |
| **Real negativo** | Falsos positivos (FP) | Verdaderos negativos (VN) |

- **FN:** un caso positivo clasificado como negativo (aquí, un tumor maligno clasificado como benigno).
- **FP:** un caso negativo clasificado como positivo (una falsa alarma).
- Todas las métricas siguientes salen de estos cuatro conteos.

## Métricas derivadas

$$\begin{aligned}
\text{exactitud}&=\frac{VP+VN}{VP+FN+FP+VN} &
\text{precisión}&=\frac{VP}{VP+FP}\\[4pt]
\text{recall (sensibilidad)}&=\frac{VP}{VP+FN} &
\text{especificidad}&=\frac{VN}{VN+FP}
\end{aligned}$$

$$F_1=\frac{2\cdot\text{precisión}\cdot\text{recall}}{\text{precisión}+\text{recall}}$$

- **Sensibilidad:** probabilidad de predecir positivo dado que el caso es positivo. **Especificidad:** probabilidad de predecir negativo dado que el caso es negativo (ESL, §9.2.5, p. 316).
- **Precisión:** de los casos que se declaran positivos, qué fracción lo es.
- **$F_1$:** media armónica de precisión y recall.

## Ejemplo numérico: *breast cancer*

SVM radial con $C=1$ y $\gamma$ por defecto, variables estandarizadas; 171 casos de prueba, 64 malignos.

| | Predicho maligno | Predicho benigno |
|:--|:--:|:--:|
| **Real maligno (64)** | 60 | 4 |
| **Real benigno (107)** | 4 | 103 |

| Métrica | Cálculo | Valor |
|:--|:--|--:|
| Exactitud | $163/171$ | 0,953 |
| Precisión (maligno) | $60/64$ | 0,938 |
| Recall (maligno) | $60/64$ | 0,938 |
| Especificidad | $103/107$ | 0,963 |
| $F_1$ (maligno) | | 0,938 |

## Exactitud y línea base

- La **línea base** es la exactitud de un modelo que siempre responde la clase más frecuente. En la partición de ejemplo: $107/171=0{,}626$.
- Un modelo con exactitud cercana a la línea base no aprendió nada útil (como $\gamma=1$ en *breast cancer*: 0,632).
- Con clases desbalanceadas o con costos distintos por error, la exactitud puede ser alta y aun así dejar sin detectar la clase de interés.
- Se reporta la exactitud **junto con** la línea base y con las métricas por clase.

## Umbral de decisión

La SVM clasifica como positivo si $f(\xv)>t$; el valor por defecto es $t=0$. Cambiar $t$ desplaza la frontera sin reentrenar.

| Umbral $t$ | FN | FP | Recall | Precisión | Exactitud |
|--:|--:|--:|--:|--:|--:|
| 0,5 | 10 | 0 | 0,844 | 1,000 | 0,942 |
| 0 | 4 | 4 | 0,938 | 0,938 | 0,953 |
| $-0{,}25$ | 3 | 8 | 0,953 | 0,884 | 0,936 |
| $-0{,}5$ | 2 | 11 | 0,969 | 0,849 | 0,924 |
| $-1$ | 0 | 22 | 1,000 | 0,744 | 0,871 |

Bajar el umbral reduce los FN y aumenta los FP: **no existe un umbral sin costo**.

## Curva ROC

- La curva ROC grafica la sensibilidad frente a la especificidad al variar los parámetros de una regla de clasificación (ESL, §9.2.5, p. 317).
- Cada punto corresponde a un umbral distinto sobre $f(\xv)$.
- Variar el umbral recorre la curva: aumenta la sensibilidad y disminuye la especificidad, o al revés (ESL, §9.2.5, p. 316).
- La curva resume el desempeño **para todos los umbrales**; la elección del umbral depende del costo de cada error.

# Ponderación del error por clase

## Errores con costos distintos

- En diagnóstico, clasificar un tumor maligno como benigno (FN) suele costar más que una falsa alarma (FP).
- Se formaliza con una **matriz de pérdida** $L$ de $K\times K$, donde $L_{kk'}$ es la pérdida de clasificar como $k'$ una observación de la clase $k$ (ESL, §9.2.4, p. 310).
- Dos clases con costos $c_{FN}$ y $c_{FP}$: el costo total esperado es

$$c_{FN}\cdot FN + c_{FP}\cdot FP$$

- Minimizar el número de errores equivale a $c_{FN}=c_{FP}$. Si los costos difieren, el modelo con menor exactitud puede ser el de menor costo.

## Regla de decisión con costos

Si un modelo estima $p(\xv)=P(Y=+1\mid\xv)$, el costo esperado mínimo se obtiene clasificando como positivo cuando

$$p(\xv)\ \ge\ \frac{c_{FP}}{c_{FP}+c_{FN}}$$

- Con costos iguales el umbral es $1/2$. Con $c_{FN}=5\,c_{FP}$ es $1/6$: se acepta más falsas alarmas para perder menos casos positivos.
- ESL (§9.2.5, p. 316) muestra el mismo efecto con una regla análoga: variar las pérdidas relativas aumenta la sensibilidad y disminuye la especificidad.
- La SVM no estima $p(\xv)$ directamente: la función $f(\xv)$ no es una probabilidad. Por eso el umbral sobre $f$ se calibra empíricamente.

## Ponderar las clases en el entrenamiento

Para dos clases, ESL (§9.2.4, p. 310) propone ponderar las observaciones de cada clase por su pérdida. En la SVM se pondera la penalización de las holguras:

$$\min_{\wv,b,\xi}\ \tfrac12\norm{\wv}^2+C\sum_{i=1}^m w_{y_i}\,\xi_i\qquad\Longleftrightarrow\qquad0\le\alpha_i\le C\,w_{y_i}$$

- El peso $w_k$ multiplica $C$ para la clase $k$: equivocarse en una clase con peso alto cuesta más durante el entrenamiento, y los multiplicadores de esa clase pueden crecer más.
- `class_weight='balanced'` usa $w_k=\dfrac{n}{K\,n_k}$ ($n_k$: tamaño de la clase $k$). En el entrenamiento de ejemplo: 0,796 para benigno y 1,345 para maligno.
- Ponderar observaciones **altera la probabilidad a priori de las clases** (ESL, §9.2.4, p. 311).

## Efecto de la ponderación en las métricas

*Breast cancer*, mismo modelo, 171 casos de prueba:

| Ponderación | FN | FP | Recall | Precisión | $F_1$ | Exactitud |
|:--|--:|--:|--:|--:|--:|--:|
| Sin ponderar | 4 | 4 | 0,938 | 0,938 | 0,938 | 0,953 |
| `balanced` | 4 | 5 | 0,938 | 0,923 | 0,930 | 0,947 |
| Maligno con peso 5 | 2 | 6 | 0,969 | 0,912 | 0,939 | 0,953 |

- En general, aumentar el peso de la clase positiva **sube el recall y baja la precisión**: se detectan más positivos a cambio de más falsas alarmas.
- Aquí `balanced` no mejora (las clases no están muy desbalanceadas: 37 % de malignos). El peso 5 cambia dos casos.
- Con una sola partición de 171 casos, estas diferencias no permiten declarar un ganador.

## Umbral frente a ponderación

| | Umbral sobre $f(\xv)$ | `class_weight` |
|:--|:--|:--|
| Cuándo actúa | Después de entrenar | Durante el entrenamiento |
| Reentrena | No | Sí |
| Qué cambia | Solo la regla de decisión | La frontera misma y los vectores soporte |
| Reversible | Sí, sin costo | Requiere reajustar |
| Efecto típico | Recorre el compromiso FN/FP | Desplaza la frontera hacia la clase de menor peso |

- Ambos desplazan el compromiso entre FN y FP, ninguno agrega información nueva.
- Se elige según el costo de cada error, y el efecto se **evalúa con validación cruzada**.

# Validación y selección de modelo

## Para qué se valida

Dos objetivos distintos, con datos distintos:

1. **Selección:** comparar modelos o hiperparámetros ($C$, $\gamma$, kernel) para elegir uno.
2. **Evaluación:** estimar el error del modelo final sobre datos nuevos.

- El error de entrenamiento no sirve para ninguna de las dos: es optimista y decrece con la complejidad (ESL, §7.2).
- Si el mismo dato se usa para seleccionar y para evaluar, la cifra final queda sesgada a favor del modelo elegido.

## Partición entrenamiento, validación y prueba

Con datos abundantes, ESL (§7.2, p. 222) sugiere dividir al azar en tres conjuntos; un ejemplo típico es 50 % para entrenamiento y 25 % para validación y para prueba.

| Conjunto | Uso |
|:--|:--|
| Entrenamiento | Ajustar los parámetros del modelo ($\alpha_i$, $b$) |
| Validación | Elegir hiperparámetros y comparar modelos |
| Prueba | Estimar el error final, **una sola vez** |

- El conjunto de prueba debe guardarse y usarse solo al final (ESL, §7.2, p. 222).
- Con pocos datos, el conjunto de validación se reemplaza por **validación cruzada**.

## Validación cruzada de $K$ pliegues

1. Dividir el entrenamiento en $K$ partes de tamaño similar.
2. Para cada parte $k$: ajustar el modelo con las otras $K-1$ y medir el error en la parte $k$.
3. Promediar los $K$ errores.

$$\text{CV}=\frac1K\sum_{k=1}^K \text{error}_k\qquad\text{(se reporta también la dispersión entre pliegues)}$$

- Valores típicos: $K=5$ o $10$. Con $K=N$ (dejar uno fuera) el sesgo es bajo pero la varianza puede ser alta; ESL recomienda 5 o 10 pliegues como un buen compromiso (§7.10.1).
- En clasificación se estratifica por clase para mantener sus proporciones en cada pliegue.

## Selección de hiperparámetros: procedimiento

1. Fijar una **grilla logarítmica** de valores (por ejemplo, $C\in\{0{,}1,1,10,100\}$ y $\gamma\in\{10^{-3},\dots,1\}$).
2. Evaluar **cada combinación** con validación cruzada sobre el entrenamiento.
3. Elegir la combinación con mayor exactitud promedio (o menor costo).
4. Reajustar el modelo con todo el entrenamiento y esos parámetros.
5. Evaluar en el conjunto de prueba **una sola vez**.

- Si el mejor valor cae en el **borde** de la grilla, se amplía en esa dirección.
- Combinaciones cuyas medias difieren menos que la dispersión entre pliegues no se distinguen: se prefiere el modelo más simple.
- Esta elección se aplica a $C$, $\gamma$ y al kernel. En la simulación de ESL (§12.3.4) $C$ se eligió minimizando el error de prueba, lo que favorece a la SVM: no debe hacerse en una evaluación real.

## La forma correcta e incorrecta de validar

Cualquier paso que use las etiquetas debe ejecutarse **dentro** de cada pliegue (ESL, §7.10.2).

- **Incorrecto:** filtrar variables según su relación con la clase usando todos los datos, y luego validar solo el clasificador. La estimación sale artificialmente buena: en el ejemplo de ESL, el error de validación cruzada fue cercano a 3 % frente a un error real de 50 %.
- **Correcto:** separar los pliegues primero y repetir el filtrado, el ajuste y la predicción en cada pliegue, usando solo las demás observaciones.
- **Regla:** las muestras se dejan fuera antes de cualquier selección o filtrado (ESL, p. 246). El filtrado que no usa las etiquetas puede hacerse antes.

En la práctica: estandarización, selección de variables y SVM van dentro de un `Pipeline` que se valida completo.

## Incertidumbre de la estimación

Con $n$ casos de evaluación, la exactitud observada $\hat p$ tiene un error estándar binomial aproximado

$$\text{EE}\approx\sqrt{\frac{\hat p\,(1-\hat p)}{n}}$$

| Exactitud | Casos de prueba | EE aproximado |
|--:|--:|--:|
| 0,953 | 171 | 0,016 |
| 0,953 | 1000 | 0,007 |

- Con 171 casos, una diferencia de 0,01 entre dos modelos (menos de dos pacientes) es menor que el error estándar: no es evidencia de que uno sea mejor.
- Para comparar modelos con más rigor se repite la partición varias veces o se usa validación cruzada.

## Ejemplo: *breast cancer*, comparación con validación cruzada

Validación cruzada de 5 pliegues estratificados sobre el entrenamiento (398 casos):

| Modelo | Media | Desv. est. entre pliegues |
|:--|--:|--:|
| Lineal | 0,990 | 0,009 |
| Radial por defecto | 0,982 | 0,010 |

- La diferencia (0,008) es menor que la dispersión entre pliegues: no hay un ganador claro.
- Mejor combinación en la grilla de la sección anterior: $C=100$, $\gamma=0{,}001$, con CV 0,990. Cae en el **borde** de la grilla (mayor $C$ y menor $\gamma$), por lo que convendría ampliarla.
- La combinación vecina ($C=100$, $\gamma=0{,}01$) obtiene 0,987: dentro de la dispersión.

## Ejemplo: *breast cancer*, evaluación final

Con el modelo elegido, el conjunto de prueba se abre **una sola vez**:

| Cantidad | Valor |
|:--|--:|
| Exactitud CV del mejor modelo | 0,990 |
| Exactitud en prueba (171 casos) | 0,953 |
| Línea base | 0,626 |
| Modelo lineal simple en prueba | 0,953 |
| Recall y precisión de la clase maligna en prueba | 0,922 y 0,952 |

- La prueba queda bajo la CV: la CV se usó para elegir (es algo optimista) y 171 casos dejan una incertidumbre de $\pm0{,}016$.
- El modelo lineal simple empata en prueba: sin evidencia para preferir el kernel radial.

## Flujo recomendado

1. **Particionar** (estratificado) y fijar una **línea base**.
2. Construir un `Pipeline` con el preprocesamiento y la SVM.
3. **Comparar** kernels y un modelo simple con validación cruzada.
4. **Sintonizar** $C$ y $\gamma$ en una grilla logarítmica (ampliarla si el óptimo cae en el borde).
5. Decidir la **regla de decisión** según el costo de cada error: umbral o `class_weight`, evaluado con validación cruzada.
6. **Evaluar una sola vez** en el conjunto de prueba; reportar la exactitud, las métricas por clase y su incertidumbre.

# Cierre

## Resumen

- **Parámetros:** el kernel define la forma de la frontera; $C$ pondera las violaciones del margen; $\gamma$ fija el alcance de cada punto. Se ven en la frontera, el margen y los vectores soporte, y se eligen conjuntamente.
- **Métricas:** la exactitud no basta; la matriz de confusión entrega precisión, recall y especificidad, y el umbral recorre el compromiso entre FN y FP.
- **Ponderación:** con costos distintos por error se usa una matriz de pérdida; en la SVM, `class_weight` multiplica $C$ por clase y, en general, sube el recall y baja la precisión de la clase ponderada.
- **Validación:** los hiperparámetros se eligen con validación cruzada dentro de un `Pipeline`; el conjunto de prueba se usa una sola vez y la cifra se reporta con su incertidumbre.

## Preguntas para discusión

1. Si se elimina un punto con $\alpha_i=0$, ¿cambia la solución? ¿Y si se elimina un vector soporte?
2. Con $\gamma$ grande, ¿puede $C$ compensar el sobreajuste? ¿Qué evidencia de la tabla de la grilla lo respalda?
3. ¿Por qué un recall de 1,000 no es necesariamente un buen resultado? ¿Qué métrica lo acompaña?
4. En un problema donde un FN cuesta cinco veces un FP, ¿qué umbral de probabilidad corresponde y cómo se aproxima con una SVM?
5. ¿Qué error se comete al estandarizar con todos los datos antes de validar? ¿Por qué ESL lo considera una forma incorrecta?
6. Con 171 casos de prueba, ¿qué diferencia entre dos modelos consideraría relevante y por qué?

## Referencias

\footnotesize

- Hastie, T., Tibshirani, R. y Friedman, J. (2009). *The Elements of Statistical Learning: Data Mining, Inference, and Prediction* (2.ª ed.). Springer. Secciones citadas: §7.1–7.2 (evaluación y complejidad), §7.10 (validación cruzada), §9.2.4–9.2.5 (matriz de pérdida, sensibilidad, especificidad y curva ROC), §12.2 (clasificador de vectores soporte), §12.3 (SVM y kernels, SVM como método de penalización).
- Las cifras de los ejemplos provienen del cuaderno `cuaderno_sesion_svm_practica.ipynb` (scikit-learn 1.9.1, semilla 0).

<!-- Nota: los números de página de ESL corresponden a la 2.ª edición impresa; el 7.º tiraje (2013) trae correcciones. -->