---
title: EST-852
subtitle: Redes Neuronales Feedforward II
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


# Entrenamiento de una red

**Organización**

- Planteamiento: parámetros, costo y gradiente
- Backpropagation paso a paso en la red $2\to3\to1$ (derivadas parciales)
- Forma matricial y verificación del gradiente
- Descenso por gradiente, minibatch, época e iteración
- Inicialización y gradiente que se desvanece
- Regularización y detención temprana
- Validación y selección de modelo; comparación con la SVM; Keras

## Recordatorio: la red $2\to3\to1$

\begin{tikzpicture}[remember picture, overlay]
    \node[anchor=north, yshift=-1.55cm] at (current page.north)
    {
        \includegraphics[width=0.55\textwidth]{fig_arch231.png}
    };
\end{tikzpicture}

\vspace*{3.9cm}

$$Z^{[1]}=W^{[1]T}X+b^{[1]},\ \ A^{[1]}=\sigma(Z^{[1]}),\ \ Z^{[2]}=W^{[2]T}A^{[1]}+b^{[2]},\ \ A^{[2]}=\sigma(Z^{[2]})$$

## Planteamiento del problema

- Parámetros: $\theta=\{W^{[1]},b^{[1]},W^{[2]},b^{[2]}\}$, en total $6+3+3+1=13$
- Costo (entropía cruzada binaria):
$$J(\theta)=\frac{1}{m}\sum_{i=1}^{m}\ell^{(i)},\qquad \ell=-\bigl[y\log a^{[2]}+(1-y)\log(1-a^{[2]})\bigr]$$
- Objetivo: $\min_\theta J(\theta)$ por **descenso por gradiente**
- Se necesitan las 13 derivadas parciales $\partial J/\partial\theta_k$
- **Backpropagation** es el cálculo ordenado de estas derivadas mediante la regla de la cadena, reutilizando resultados intermedios

# Backpropagation paso a paso

## Cadena de dependencias (una observación)

$$
\xv\ \xrightarrow{\ W^{[1]},\,b^{[1]}\ }\ z^{[1]}\ \xrightarrow{\ \sigma\ }\ a^{[1]}\ \xrightarrow{\ W^{[2]},\,b^{[2]}\ }\ z^{[2]}\ \xrightarrow{\ \sigma\ }\ a^{[2]}\ \xrightarrow{\ \ell\ }\ \ell(a^{[2]},y)
$$

- Cada flecha es una función simple con derivada conocida
- Los parámetros de la capa 1 afectan a $\ell$ **a través de** $z^{[1]}\to a^{[1]}\to z^{[2]}\to a^{[2]}$
- Regla de la cadena: la derivada de $\ell$ respecto de un parámetro es el producto de las derivadas a lo largo de la cadena
- Se recorre la cadena **hacia atrás**, desde $\ell$ hasta los parámetros

## Paso 1: derivada respecto de $z^{[2]}$

$$\ell=-\bigl[y\log a+(1-y)\log(1-a)\bigr],\qquad a=a^{[2]}=\sigma(z^{[2]})$$

$$\frac{\partial\ell}{\partial a}=-\frac{y}{a}+\frac{1-y}{1-a}=\frac{a-y}{a(1-a)},\qquad \frac{\partial a}{\partial z^{[2]}}=a(1-a)$$

$$\boxed{\ \frac{\partial\ell}{\partial z^{[2]}}=\frac{a-y}{a(1-a)}\cdot a(1-a)=a^{[2]}-y\ }$$

- La derivada de la sigmoide cancela el denominador
- Es el mismo resultado de la regresión logística

## Paso 2: parámetros de la capa de salida

$$z^{[2]}=\sum_{k=1}^{3}w^{[2]}_{k}\,a^{[1]}_{k}+b^{[2]}\quad\Rightarrow\quad \frac{\partial z^{[2]}}{\partial w^{[2]}_k}=a^{[1]}_k,\qquad \frac{\partial z^{[2]}}{\partial b^{[2]}}=1$$

Por la regla de la cadena:

$$\boxed{\ \frac{\partial\ell}{\partial w^{[2]}_k}=\left(a^{[2]}-y\right)a^{[1]}_k\ },\qquad \boxed{\ \frac{\partial\ell}{\partial b^{[2]}}=a^{[2]}-y\ }$$

para $k=1,2,3$.

## Paso 3: propagar el error a la capa oculta

$$\frac{\partial z^{[2]}}{\partial a^{[1]}_k}=w^{[2]}_k\quad\Rightarrow\quad\frac{\partial\ell}{\partial a^{[1]}_k}=\left(a^{[2]}-y\right)w^{[2]}_k$$

$$\frac{\partial a^{[1]}_k}{\partial z^{[1]}_k}=a^{[1]}_k\left(1-a^{[1]}_k\right)$$

Se define el **error de la neurona $k$ de la capa oculta**:

$$\boxed{\ \delta^{[1]}_k:=\frac{\partial\ell}{\partial z^{[1]}_k}=\left(a^{[2]}-y\right)w^{[2]}_k\,a^{[1]}_k\left(1-a^{[1]}_k\right)\ }$$

## Paso 4: parámetros de la capa oculta

$$z^{[1]}_k=\sum_{j=1}^{2}w^{[1]}_{jk}\,x_j+b^{[1]}_k\quad\Rightarrow\quad\frac{\partial z^{[1]}_k}{\partial w^{[1]}_{jk}}=x_j,\qquad\frac{\partial z^{[1]}_k}{\partial b^{[1]}_k}=1$$

$$\boxed{\ \frac{\partial\ell}{\partial w^{[1]}_{jk}}=\delta^{[1]}_k\,x_j\ },\qquad\boxed{\ \frac{\partial\ell}{\partial b^{[1]}_k}=\delta^{[1]}_k\ }$$

para $j=1,2$ y $k=1,2,3$.

## Resumen: las 13 derivadas (una observación)

Con $\delta^{[2]}=a^{[2]}-y$:

| Parámetro | Derivada parcial | Número |
|:--|:--|:-:|
| $w^{[2]}_k$ | $\delta^{[2]}\,a^{[1]}_k$ | 3 |
| $b^{[2]}$ | $\delta^{[2]}$ | 1 |
| $w^{[1]}_{jk}$ | $\delta^{[1]}_k\,x_j$, con $\delta^{[1]}_k=\delta^{[2]}w^{[2]}_k\,a^{[1]}_k(1-a^{[1]}_k)$ | 6 |
| $b^{[1]}_k$ | $\delta^{[1]}_k$ | 3 |

- El error $\delta^{[2]}$ se calcula una vez y se **reutiliza** para todos los parámetros anteriores
- La derivada de un peso es (error de la neurona destino) $\times$ (valor que entra por ese arco)

## Ejemplo numérico: propagación hacia adelante

Una observación $\xv=(0{,}5;\,-1)^T$, $y=1$.

$W^{[1]}=\left[\begin{smallmatrix}0{,}1&0{,}2&-0{,}3\\0{,}4&-0{,}5&0{,}6\end{smallmatrix}\right]$, $b^{[1]}=(0{,}1;\,0;\,-0{,}1)^T$, $W^{[2]}=(0{,}3;\,-0{,}2;\,0{,}5)^T$, $b^{[2]}=0{,}05$

| Cantidad | Valor |
|:--|:--|
| $z^{[1]}=W^{[1]T}\xv+b^{[1]}$ | $(-0{,}25;\ 0{,}60;\ -0{,}85)$ |
| $a^{[1]}=\sigma(z^{[1]})$ | $(0{,}4378;\ 0{,}6457;\ 0{,}2994)$ |
| $z^{[2]}=W^{[2]T}a^{[1]}+b^{[2]}$ | $0{,}2019$ |
| $a^{[2]}=\sigma(z^{[2]})$ | $0{,}5503$ |
| $\ell$ | $0{,}5973$ |

## Ejemplo numérico: propagación hacia atrás

| Cantidad | Valor |
|:--|:--|
| $\delta^{[2]}=a^{[2]}-y$ | $-0{,}4497$ |
| $\partial\ell/\partial w^{[2]}=\delta^{[2]}a^{[1]}$ | $(-0{,}1969;\ -0{,}2903;\ -0{,}1347)$ |
| $\delta^{[1]}_k=\delta^{[2]}w^{[2]}_k a^{[1]}_k(1-a^{[1]}_k)$ | $(-0{,}0332;\ 0{,}0206;\ -0{,}0472)$ |
| $\partial\ell/\partial w^{[1]}_{1k}=\delta^{[1]}_k\,x_1$ | $(-0{,}0166;\ 0{,}0103;\ -0{,}0236)$ |
| $\partial\ell/\partial w^{[1]}_{2k}=\delta^{[1]}_k\,x_2$ | $(0{,}0332;\ -0{,}0206;\ 0{,}0472)$ |

- Comparado con diferencias finitas ($\varepsilon=10^{-6}$), la diferencia máxima en $\partial\ell/\partial W^{[1]}$ es $7{,}4\times10^{-11}$

# Forma matricial y verificación

## De una observación a $m$ observaciones

Con $J=\frac1m\sum_i\ell^{(i)}$, para $A^{[2]},Y\in\R^{1\times m}$:

$$
\begin{aligned}
dZ^{[2]}&=\tfrac{1}{m}\left(A^{[2]}-Y\right) & (1\times m)\\
dW^{[2]}&=A^{[1]}\,dZ^{[2]T} & (3\times 1)\\
db^{[2]}&=\textstyle\sum_{i}dZ^{[2]}_{\cdot i} & (1\times1)\\
dA^{[1]}&=W^{[2]}\,dZ^{[2]} & (3\times m)\\
dZ^{[1]}&=dA^{[1]}\odot A^{[1]}\odot\left(1-A^{[1]}\right) & (3\times m)\\
dW^{[1]}&=X\,dZ^{[1]T} & (2\times 3)\\
db^{[1]}&=\textstyle\sum_{i}dZ^{[1]}_{\cdot i} & (3\times1)
\end{aligned}
$$

donde $dV:=\partial J/\partial V$ y $\odot$ es el producto elemento a elemento.

## Verificación de dimensiones

- Cada gradiente tiene **la misma forma** que el parámetro correspondiente

| Gradiente | Cálculo | Forma | Parámetro |
|:--|:--|:-:|:-:|
| $dW^{[2]}$ | $A^{[1]}\,dZ^{[2]T}$ : $(3\times m)(m\times1)$ | $3\times1$ | $W^{[2]}$: $3\times1$ |
| $dW^{[1]}$ | $X\,dZ^{[1]T}$ : $(2\times m)(m\times3)$ | $2\times3$ | $W^{[1]}$: $2\times3$ |
| $dA^{[1]}$ | $W^{[2]}dZ^{[2]}$ : $(3\times1)(1\times m)$ | $3\times m$ | $A^{[1]}$: $3\times m$ |

- Los sesgos se obtienen sumando las columnas de $dZ^{[l]}$

## Algoritmo de backpropagation

1. **Inicializar** $\theta$ (valores aleatorios pequeños)
2. **Propagación hacia adelante**: calcular y **guardar** $Z^{[l]}$ y $A^{[l]}$
3. **Costo** $J$
4. **Propagación hacia atrás**: calcular $dZ^{[2]},dW^{[2]},db^{[2]},dA^{[1]},dZ^{[1]},dW^{[1]},db^{[1]}$
5. **Actualizar**: $\theta\leftarrow\theta-\eta\,\nabla_\theta J$
6. Repetir 2--5 hasta un criterio de parada

- Los valores guardados en el paso 2 se usan en el paso 4
- Referencia: Rumelhart, Hinton y Williams (1986), *Nature* 323, 533--536

## Verificación numérica del gradiente

Diferencias centrales para cada parámetro $\theta_k$:

$$\frac{\partial J}{\partial\theta_k}\approx\frac{J(\theta_k+\varepsilon)-J(\theta_k-\varepsilon)}{2\varepsilon},\qquad\varepsilon=10^{-6}$$

Error relativo entre el gradiente analítico $g$ y el numérico $\hat g$:

$$\frac{\lVert g-\hat g\rVert}{\lVert g\rVert+\lVert\hat g\rVert}$$

- Red $2\to3\to1$ con $m=8$ observaciones aleatorias: error relativo máximo sobre los cuatro bloques de parámetros $=7\times10^{-9}$
- Es la forma de comprobar una implementación de backpropagation

## Equivalencia con scikit-learn

Un paso de `MLPClassifier` coincide con el cálculo manual si:

- `activation='logistic'`, `solver='sgd'`, `alpha=0`, `momentum=0`, `nesterovs_momentum=False`
- `batch_size` igual al número de observaciones (gradiente completo)

```python
m.coefs_ = [W1.copy(), W2.copy()]       # mismas matrices W
m.intercepts_ = [b1.copy(), b2.copy()]
m.partial_fit(X, y)                     # un paso de gradiente
```

- En scikit-learn `coefs_[l]` tiene forma $n_{l-1}\times n_l$, igual que $W^{[l]}$; `X` es $m\times n$
- Resultado verificado ($m=40$ observaciones): la diferencia máxima con el paso manual en los cuatro bloques de parámetros es $0{,}0$

# Optimización

## Descenso por gradiente

$$\theta\leftarrow\theta-\eta\,\nabla_\theta J(\theta)$$

- $\eta>0$: **tasa de aprendizaje**
- $\eta$ muy pequeña: avance lento; $\eta$ muy grande: el costo puede oscilar o aumentar
- La dirección $-\nabla J$ es la de mayor descenso local de $J$

---

\begin{tikzpicture}[remember picture, overlay]
    \node[anchor=north, yshift=-1.55cm] at (current page.north)
    {
        \includegraphics[width=0.72\textwidth]{fig_lr_batch.png}
    };
\end{tikzpicture}

\vspace*{3.8cm}

Izquierda: red $2\to4\to1$ en *moons* (210 obs.), 300 iteraciones de gradiente completo.

| $\eta$ | 0,01 | 0,1 | 1 | 5 |
|:--|:-:|:-:|:-:|:-:|
| $J$ final | 0,683 | 0,494 | 0,303 | 0,261 |
| accuracy prueba (90 obs.) | 0,50 | 0,76 | 0,78 | 0,82 |

## Época, iteración y minibatch

- **Iteración**: una actualización de $\theta$
- **Época**: una pasada completa por el conjunto de entrenamiento
- **Minibatch** de tamaño $b$: cada actualización usa $b$ observaciones; hay $\lceil m/b\rceil$ iteraciones por época

| $b$ | iteraciones por época | iteraciones en 100 épocas | $J$ final | accuracy prueba |
|:--|:-:|:-:|:-:|:-:|
| 210 (completo) | 1 | 100 | 0,381 | 0,77 |
| 32 | 7 | 700 | 0,303 | 0,77 |
| 1 | 210 | 21000 | 0,113 | 0,94 |

- Tasa 0,5; $m=210$. Con 90 observaciones de prueba, cada observación vale 1,1 puntos porcentuales

## No convexidad e inicialización

- $J(\theta)$ **no es convexa** en $\theta$: el descenso por gradiente converge a un punto estacionario que depende de la inicialización
- (En la SVM, el problema de optimización es convexo)
- Si todos los pesos parten en 0, las neuronas de una capa reciben gradientes idénticos y permanecen idénticas (**simetría**)

| Inicialización | columnas de $W^{[1]}$ | $J$ final | accuracy prueba |
|:--|:-:|:-:|:-:|
| ceros | idénticas | 0,693 | 0,50 |
| normal$(0;\,0{,}5^2)$ | distintas | 0,303 | 0,78 |

- $0{,}693=\ln 2$: la red predice $P(Y=1)=0{,}5$ para todos los puntos
- Red $2\to4\to1$, $\eta=1$, 300 iteraciones

## Gradiente que se desvanece

:::::: {.columns}
::: {.column width="50%"}
\mbox{}
:::
::: {.column width="50%"}
- $\sigma'(z)=\sigma(z)(1-\sigma(z))\leq\tfrac14$
- En $\delta^{[l]}$ aparece un factor $g'(z^{[l]})$ por cada capa que se atraviesa hacia atrás
- Con $L$ capas sigmoides la señal de error se multiplica por factores $\leq\tfrac14$ (además de los pesos)
- ReLU: $g'(z)=1$ si $z>0$; evita esta reducción en la región activa
- Si $z<0$ para toda observación, $g'=0$ y la neurona deja de actualizarse
:::
::::::

\begin{tikzpicture}[remember picture, overlay]
    \node[xshift=-4.4cm, yshift=-0.3cm] at (current page.center)
    {
        \includegraphics[width=0.36\textwidth]{fig_dsigmoid.png}
    };
\end{tikzpicture}


# Regularización y validación

## Regularización L2

- Se agrega una penalización a los pesos al costo:
$$J_\lambda(\theta)=J(\theta)+\frac{\lambda}{2m}\sum_{l}\left\lVert W^{[l]}\right\rVert_F^2$$
- Los sesgos no se penalizan
- En `MLPClassifier`, el parámetro `alpha` controla esta penalización
- Analogía formal con la SVM: allí la penalización entra como $\tfrac12\lVert\wv\rVert^2$ con coeficiente $1/C$ (ESL, cap. 12); un $C$ grande equivale a poca regularización, un `alpha` grande a mucha

## Detención temprana (*early stopping*)

\begin{tikzpicture}[remember picture, overlay]
    \node[anchor=north, yshift=-1.55cm] at (current page.north)
    {
        \includegraphics[width=0.62\textwidth]{fig_early.png}
    };
\end{tikzpicture}

\vspace*{3.3cm}

- `MLPClassifier(64,)` con `early_stopping=True`: 15 % del entrenamiento como validación, `n_iter_no_change=10`
- Se detuvo en la época 42; mejor accuracy de validación 0,963; accuracy en prueba 0,957
- La pérdida de entrenamiento sigue bajando; el criterio es el desempeño en validación

## Validación y selección de modelo

- Se reutiliza el protocolo visto en SVM: partición entrenamiento/prueba, validación cruzada, búsqueda en grilla
- Hiperparámetros de una RNA:
  - número de capas y de neuronas
  - función de activación
  - tasa de aprendizaje, tamaño de minibatch, número de épocas
  - penalización `alpha`
- Escalar las variables **dentro** del `Pipeline`, igual que en SVM
- `MLPClassifier` **no** tiene parámetro `class_weight` (verificado en scikit-learn 1.9.1). Con clases desbalanceadas se puede ajustar el umbral sobre `predict_proba` según los costos de error, como en la sesión de SVM

## Comparación: MLP frente a SVM en `load_digits`

- 1797 imágenes $8\times8$, 10 clases; 70 % entrenamiento (1257), 30 % prueba (540)
- Validación cruzada 5 pliegues estratificada, `random_state=0`

| Modelo | CV (5 pliegues) | Accuracy en prueba | Errores / 540 |
|:--|:-:|:-:|:-:|
| SVM RBF | 0,9865 | 0,9926 | 4 |
| MLP (mejor de 9 configuraciones) | 0,9753 | 0,9778 | 12 |

- SVM: $C=1$, $\gamma=0{,}001$. MLP: `StandardScaler` + grilla de `hidden_layer_sizes` y `alpha`; mejor $(128,)$ con `alpha`$=0{,}01$
- Diferencia de 8 observaciones en una única partición de prueba: no es concluyente sobre cuál método es mejor en general
- La SVM del cuaderno usa los píxeles sin escalar; el MLP, escalados

## Keras: la misma red con diferenciación automática

```python
model = keras.Sequential([keras.Input((64,)),
    keras.layers.Dense(64, activation='relu'),
    keras.layers.Dense(10, activation='softmax')])
model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])
h = model.fit(Xtr, ytr, epochs=100, batch_size=32, validation_split=0.15,
              callbacks=[keras.callbacks.EarlyStopping(patience=5)])
```

- No se escribe backpropagation: el framework calcula los gradientes
- 4810 parámetros ($64\cdot64+64+64\cdot10+10$); píxeles divididos por 16
- Corrida con TensorFlow 2.21.0 / Keras 3.15.1: accuracy en prueba 0,970 (llegó al máximo de 100 épocas sin activar la detención)

---

\begin{tikzpicture}[remember picture, overlay]
    \node[anchor=north, yshift=-1.55cm] at (current page.north)
    {
        \includegraphics[width=0.62\textwidth]{fig_keras.png}
    };
\end{tikzpicture}

\vspace*{3.3cm}

- Con softmax y entropía cruzada, el error de la capa de salida es $\hat y_k-y_k$, como en el caso binario

## Otras arquitecturas

:::::: {.columns}
::: {.column width="46%"}
- Redes **recurrentes**: el estado oculto en el instante $t$ depende de la entrada en $t$ y del estado en $t-1$
- Redes **convolucionales**: capas con pesos compartidos para datos con estructura espacial
- Mismo principio de entrenamiento: grafo de cómputo y backpropagation
:::
::: {.column width="54%"}
\mbox{}
:::
::::::

\begin{tikzpicture}[remember picture, overlay]
    \node[xshift=4.4cm, yshift=-0.3cm] at (current page.center)
    {
        \includegraphics[width=0.40\textwidth]{simple_rnn.png}
    };
\end{tikzpicture}


## Resumen

- Backpropagation = regla de la cadena aplicada de la salida hacia la entrada; $\delta^{[2]}=a^{[2]}-y$ se reutiliza en todas las derivadas
- Cada gradiente tiene la forma de su parámetro; la verificación numérica comprueba la implementación
- Descenso por gradiente: tasa de aprendizaje, minibatch, época e iteración
- $J$ no es convexa: importan la inicialización y el criterio de parada
- Regularización (`alpha`) y detención temprana controlan el sobreajuste
- Selección de hiperparámetros con validación cruzada, como en SVM

## Referencias

- Rumelhart, D. E., Hinton, G. E. y Williams, R. J. (1986). Learning representations by back-propagating errors. *Nature*, 323, 533--536.
- Hastie, T., Tibshirani, R. y Friedman, J. (2009). *The Elements of Statistical Learning* (2.ª ed.). Springer. Cap. 11 (redes neuronales) y cap. 12 (SVM).
- Goodfellow, I., Bengio, Y. y Courville, A. (2016). *Deep Learning*. MIT Press.
- Rosenblatt, F. (1958). The perceptron: a probabilistic model for information storage and organization in the brain. *Psychological Review*, 65(6), 386--408.
