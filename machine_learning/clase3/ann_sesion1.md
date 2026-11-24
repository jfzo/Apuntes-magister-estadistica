---
title: EST-852
subtitle: Redes Neuronales Feedforward I
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

# Introducción a Redes Neuronales

**Organización**

- Dos visiones de las redes neuronales artificiales (RNA)
- Origen histórico y el límite del modelo lineal (XOR)
- Neurona, arquitectura y propagación hacia adelante en notación matricial
- Funciones de activación y capa de salida
- Función de costo: entropía cruzada
- Comparación con la SVM

## Red de Neuronas Artificiales (RNA)

- Explosión en popularidad en la última década
- Resultados destacados en competencias como ImageNet
- Dos factores habilitantes: hardware especializado y volumen de datos disponible
- *Shallow* vs *Deep*: número de capas de transformaciones apiladas

## Dos visiones de las RNA

- Medio de simulación del aprendizaje biológico
- Una manera de aumentar el poder de un modelo conocido, apilándolo en forma de grafo o red de cómputo
  - La cantidad de nodos controla la capacidad de aprendizaje
  - La arquitectura se adapta a un dominio particular (imágenes, audio, texto...)
  - Redes con muchas capas apiladas dieron origen al término "aprendizaje profundo"

**En este curso**: segunda visión. Una RNA es un modelo de regresión o clasificación con parámetros estimados por optimización.

# Origen y límite del modelo lineal

## El perceptrón (Rosenblatt, 1958)

:::::: {.columns}
::: {.column width="46%"}
- Primer modelo de neurona artificial **entrenable**
- Propuesto por Frank Rosenblatt en *Psychological Review* 65(6), pp. 386--408
- Inspirado en el modelo biológico de una neurona
- Implementado en una máquina de gran tamaño (*Mark I Perceptron*)
:::
::: {.column width="54%"}
\mbox{}
:::
::::::

\begin{tikzpicture}[remember picture, overlay]
    \node[xshift=4.4cm, yshift=-0.3cm] at (current page.center)
    {
        \includegraphics[width=0.40\textwidth]{retina-perceptron.png}
    };
\end{tikzpicture}


## El perceptrón: la máquina

:::::: {.columns}
::: {.column width="50%"}
\mbox{}
:::
::: {.column width="50%"}
- Regla de decisión:
$$\hat y = \mathbf{1}\{\wv^T\xv + b > 0\}$$
- Es un **clasificador lineal**: la frontera es el hiperplano $\wv^T\xv+b=0$
- Misma forma funcional que la SVM lineal, $f(\xv)=\wv^T\xv+b$
:::
::::::

\begin{tikzpicture}[remember picture, overlay]
    \node[xshift=-4.4cm, yshift=-0.3cm] at (current page.center)
    {
        \includegraphics[width=0.40\textwidth]{machine_perceptron.png}
    };
\end{tikzpicture}


## Límite: separabilidad lineal

- Minsky y Papert (1969, *Perceptrons*) analizaron la capacidad expresiva del perceptrón de una sola capa
- Un modelo lineal solo separa clases con un hiperplano
- Contra ejemplo, la función XOR: $y=1$ si sólo una de las entradas es 1

| $x_1$ | $x_2$ | $y$ |
|:-:|:-:|:-:|
| 0 | 0 | 0 |
| 1 | 0 | 1 |
| 0 | 1 | 1 |
| 1 | 1 | 0 |

- Ninguna recta clasifica correctamente los 4 puntos
- Regresión logística sobre estos 4 puntos: accuracy $=0{,}5$


## Del perceptrón a la neurona
 
:::::: {.columns}
::: {.column width="40%"}
\mbox{}
:::
::: {.column width="60%"}
- Recibe todas sus entradas, representadas por flechas
- Las combina linealmente, con un sesgo $b$:
$$z=\sum_{j=1}^{n} w_j x_j + b=\wv^T\xv+b$$
- Aplica una función de activación $g$:
$$a=g(z)$$
- Ej. Perceptrón: $g(z)=\mathbf{1}\{z>0\}$ 
- Ej. ReLU: $g(z)=\max(z,0)$
:::
::::::
\begin{tikzpicture}[remember picture, overlay]
    \node[xshift=-4.4cm, yshift=-0.3cm] at (current page.center)
    {
        \includegraphics[width=0.30\textwidth]{neurona.png}
    };
\end{tikzpicture}



## Solución: una capa oculta (XOR con 2 neuronas ReLU)

\begin{tikzpicture}[remember picture, overlay]
    \node[anchor=north, yshift=-3.55cm, xshift=-5.8cm] at (current page.center)
    {
        \includegraphics[scale=0.65]{fig_arch221.png}
    };
\end{tikzpicture}

\vspace*{5.7cm}

Red $2\to 2\to 1$ con pesos fijados a mano y ReLU en la capa oculta y salida lineal.

## Solución del XOR paso a paso

**General:** $a^{[1]}_k=\max\!\left(w^{[1]}_{1k}x_1+w^{[1]}_{2k}x_2+b^{[1]}_k,\,0\right)$, \ $\hat y=w^{[2]}_1a^{[1]}_1+w^{[2]}_2a^{[1]}_2+b^{[2]}$

**Con los valores de la red** ($w^{[1]}_{jk}=1$, $b^{[1]}=(0,-1)^T$, $W^{[2]}=(1,-2)^T$, $b^{[2]}=0$):
\small
$$\begin{aligned}a^{[1]}_1&=\max(1\cdot x_1+1\cdot x_2+0,\,0)=\max(x_1+x_2,\,0)\\[1pt]
a^{[1]}_2&=\max(1\cdot x_1+1\cdot x_2-1,\,0)=\max(x_1+x_2-1,\,0)\\[1pt]
\hat y&=1\cdot a^{[1]}_1+(-2)\cdot a^{[1]}_2+0=a^{[1]}_1-2\,a^{[1]}_2\end{aligned}$$
\normalsize

| $(x_1,x_2)$ | $\left(a^{[1]}_1,a^{[1]}_2\right)$ | $\hat y$ |
|:-:|:-:|:-:|
| (0,0) | (0,0) | 0 |
| (1,0) | (1,0) | 1 |
| (0,1) | (1,0) | 1 |
| (1,1) | (2,1) | 0 |

---

\begin{tikzpicture}[remember picture, overlay]
    \node[anchor=north, yshift=-1.55cm] at (current page.north)
    {
        \includegraphics[width=0.78\textwidth]{fig_xor.png}
    };
\end{tikzpicture}

\vspace*{5.6cm}

- En el espacio $\left(a^{[1]}_1,a^{[1]}_2\right)$ las clases **sí** son separables por una recta
- La capa oculta aprende una **nueva representación** de los datos

## Idea central y relación con SVM 

- Perceptrón / modelo lineal: $f(\xv)=\wv^T\xv+b$ sobre las variables originales
- Red con capa oculta: $f(\xv)=\wv^T\,\phi(\xv)+b$ con $\phi$ **estimada a partir de los datos**
- SVM con kernel: $f(\xv)=\wv^T\,\phi(\xv)+b$ con $\phi$ **fijada** por la elección del kernel y sus hiperparámetros
\vspace*{2.0cm}

- Referencia: Hastie, Tibshirani y Friedman (2009), *The Elements of Statistical Learning*, cap. 11 (redes neuronales) y cap. 12 (SVM)

# Arquitectura y propagación hacia adelante


## Arquitectura de ejemplo: red $2\to 3\to 1$

Para fijar la notación, extendamos el ejemplo XOR:
\begin{tikzpicture}[remember picture, overlay]
    \node[anchor=north, yshift=-1.75cm] at (current page.north)
    {
        \includegraphics[width=0.80\textwidth]{fig_arch231.png}
    };
\end{tikzpicture}

\vspace*{4.3cm}

- 2 variables de entrada, 1 capa oculta con 3 neuronas, 1 neurona de salida
- Total de parámetros: $2\cdot 3 + 3 + 3\cdot 1 + 1 = 13$

## ¿Qué representa cada arco?

- Cada variable independiente tiene un nodo en la capa de entrada
- Los valores se propagan a todos los nodos de la capa siguiente
- Cada arco entre dos capas es un **peso** que pondera el valor recibido
- Cada neurona (excepto las de entrada) tiene además un **sesgo**
- Con la salida de la red se calcula un **costo** que mide la distancia a la salida esperada

**Aprendizaje**: encontrar los pesos y sesgos que minimizan el costo.

## Notación para los datos

- Entrada: $\xv\in\R^{n}$ ($n$ características)
- $\xv^{(i)}$: $i$-ésima observación, $i=1,\ldots,m$
- $x_j^{(i)}$: $j$-ésima característica de la $i$-ésima observación
- $z^{[l]}$: entrada ponderada (combinación **afín**) de la capa $l$
- $a^{[l]}=g^{[l]}(z^{[l]})$: salida (activación) de la capa $l$
- $n_l$: número de neuronas de la capa $l$, con $n_0=n$

## La matriz de datos

Convención: **características $\times$ observaciones**

$$
X=[\xv^{(1)},\ldots,\xv^{(m)}]\in\R^{n\times m}
$$

Para $n=2$ características y $m=3$ observaciones:

$$
X=\left[\begin{array}{ccc}
x_1^{(1)} & x_1^{(2)} & x_1^{(3)}\\
x_2^{(1)} & x_2^{(2)} & x_2^{(3)}
\end{array}\right]
$$

**Nota**: `scikit-learn` usa la convención contraria, $m\times n$. 
<!--Por eso el código usa `X.T`.-->

## Pesos y sesgos

- Matriz de pesos entre las capas $(l-1)$ y $l$:
$$W^{[l]}\in\R^{n_{l-1}\times n_l},\qquad b^{[l]}\in\R^{n_l\times 1}$$
- $w^{[l]}_{jk}$: peso de la conexión entre la neurona $j$ de la capa $l-1$ y la neurona $k$ de la capa $l$
- La dimensión de $W^{[l]}$ depende solo del número de neuronas de las dos capas conectadas, **no** del número de observaciones

---

Red $2\to3\to1$:

| Parámetro | Dimensión |
|:--|:-:|
| $W^{[1]}$ | $2\times 3$ |
| $b^{[1]}$ | $3\times 1$ |
| $W^{[2]}$ | $3\times 1$ |
| $b^{[2]}$ | $1\times 1$ |

## Una neurona de la capa oculta

Neurona $k$ de la capa 1, para la observación $\xv=(x_1,x_2)^T$:

$$z^{[1]}_k=\sum_{j=1}^{2} w^{[1]}_{jk}\,x_j+b^{[1]}_k,\qquad a^{[1]}_k=g\!\left(z^{[1]}_k\right)$$

Las tres neuronas a la vez:

$$
z^{[1]}=W^{[1]T}\xv+b^{[1]}=
\left[\begin{array}{cc}
w_{11} & w_{21}\\
w_{12} & w_{22}\\
w_{13} & w_{23}
\end{array}\right]
\left[\begin{array}{c}x_1\\x_2\end{array}\right]+
\left[\begin{array}{c}b_1\\b_2\\b_3\end{array}\right]
$$

## Todas las observaciones a la vez

$$Z^{[1]}=W^{[1]T}X+b^{[1]}\in\R^{3\times m}$$

- $b^{[1]}$ ($3\times1$) se suma a cada columna (*broadcasting*)
- Función de activación aplicada elemento a elemento:

$$
A^{[1]}=g(Z^{[1]})=\left[\begin{array}{ccc}
g(z^{[1](1)}_{1}) & \cdots & g(z^{[1](m)}_{1})\\
g(z^{[1](1)}_{2}) & \cdots & g(z^{[1](m)}_{2})\\
g(z^{[1](1)}_{3}) & \cdots & g(z^{[1](m)}_{3})
\end{array}\right]
$$

- $g(z_k^{[1](i)})$: salida de la neurona $k$ ante la observación $i$

## Generalización a $L$ capas

Con $A^{[0]}=X$, para $l=1,\ldots,L$:

$$Z^{[l]}=W^{[l]T}A^{[l-1]}+b^{[l]},\qquad A^{[l]}=g^{[l]}\!\left(Z^{[l]}\right)$$

La predicción de la red es $\hat Y=A^{[L]}$.

Para la red $2\to3\to1$:

| Paso | Operación | Dimensión |
|:--|:--|:-:|
| 1 | $Z^{[1]}=W^{[1]T}X+b^{[1]}$ | $3\times m$ |
| 2 | $A^{[1]}=g(Z^{[1]})$ | $3\times m$ |
| 3 | $Z^{[2]}=W^{[2]T}A^{[1]}+b^{[2]}$ | $1\times m$ |
| 4 | $A^{[2]}=g(Z^{[2]})=\hat Y$ | $1\times m$ |

## ¿Por qué se necesita una activación no lineal?

Si $g$ fuera la identidad en ambas capas:

$$
\begin{aligned}
A^{[2]}&=W^{[2]T}\left(W^{[1]T}\xv+b^{[1]}\right)+b^{[2]}\\
&=\left(W^{[1]}W^{[2]}\right)^T\xv+\left(W^{[2]T}b^{[1]}+b^{[2]}\right)
\end{aligned}
$$

- La composición de funciones lineales resulta siempre en otra función lineal, sin importar cuántas capas se apilen
- La no linealidad de $g$ es lo que permite representar fronteras no lineales (como en el XOR)


## Teorema de aproximación universal
 
Sea $f$ continua en un conjunto compacto $K\subset\R^n$ y $\varepsilon>0$. Existen $N$, $c_k$, $\wv_k$, $b_k$ tales que
 
$$\sup_{\xv\in K}\Bigl|f(\xv)-\sum_{k=1}^{N}c_k\,g\!\left(\wv_k^T\xv+b_k\right)\Bigr|<\varepsilon$$
 
- Una **sola** capa oculta basta, con $N$ suficientemente grande
- Cybenko (1989): $g$ sigmoide; Hornik (1991) lo extiende a otras activaciones
- Leshno et al. (1993): vale si y solo si $g$ **no es un polinomio** (ReLU incluida)
- **No garantiza** cuántas neuronas hacen falta, que el entrenamiento encuentre sus pesos, ni que la red generalice



# Funciones de activación y capa de salida

## Funciones de activación

- Se aplican elemento a elemento sobre $Z^{[l]}$
- Cada capa puede usar una distinta
- Las más usadas:
  - sigmoide
  - tangente hiperbólica ($\tanh$)
  - ReLU
  - softmax (capa de salida multiclase)

## La función sigmoide

:::::: {.columns}
::: {.column width="46%"}
$$\sigma(z)=\frac{1}{1+e^{-z}}$$

- Salida en $(0,1)$
- Usada en regresión logística y en la capa de salida de clasificación binaria
- Si una capa tiene varias neuronas sigmoides, sus salidas **no** suman 1
:::
::: {.column width="54%"}
\mbox{}
:::
::::::

\begin{tikzpicture}[remember picture, overlay]
    \node[xshift=4.4cm, yshift=-0.3cm] at (current page.center)
    {
        \includegraphics[width=0.38\textwidth]{sigmoid_activation.png}
    };
\end{tikzpicture}


## La función tangente hiperbólica

:::::: {.columns}
::: {.column width="46%"}
$$\tanh(z)=\frac{e^{z}-e^{-z}}{e^{z}+e^{-z}}$$

- Forma de "S", salida en $(-1,1)$
- Centrada en 0
- Pendiente en el origen igual a 1 (la de la sigmoide es $1/4$)
- Relación: $\tanh(z)=2\sigma(2z)-1$
:::
::: {.column width="54%"}
\mbox{}
:::
::::::

\begin{tikzpicture}[remember picture, overlay]
    \node[xshift=4.4cm, yshift=-0.3cm] at (current page.center)
    {
        \includegraphics[width=0.38\textwidth]{tanh_activation.png}
    };
\end{tikzpicture}


## La función ReLU

:::::: {.columns}
::: {.column width="46%"}
$$g(z)=\max(z,0)$$

- *Rectified Linear Unit*
- Entrega 0 si $z<0$ y la misma entrada si $z\geq0$
- Cálculo muy barato
- Su efecto sobre el entrenamiento se revisa más adelante
:::
::: {.column width="54%"}
\mbox{}
:::
::::::

\begin{tikzpicture}[remember picture, overlay]
    \node[xshift=4.4cm, yshift=-0.3cm] at (current page.center)
    {
        \includegraphics[width=0.26\textwidth]{relu_activation.png}
    };
\end{tikzpicture}


## La función softmax

Para un vector $z\in\R^{K}$ ($K$ clases):

$$p_k=\frac{e^{z_k}}{\sum_{j=1}^{K}e^{z_j}},\qquad k=1,\ldots,K$$

- $p_k\in(0,1)$ y $\sum_k p_k=1$: es una distribución de probabilidad sobre las clases
- Preferida para problemas multiclase
- Con $K=2$ equivale a una sigmoide
- Estabilidad numérica: se calcula con $z_k-\max_j z_j$, lo que no altera $p_k$


## Entrenando con descenso por gradiente
 
- Parámetros: $\theta=\left(W^{[1]},b^{[1]},\ldots,W^{[L]},b^{[L]}\right)$; costo $J(\theta)$
- Entrenar es resolver $\min_\theta J(\theta)$
- Descenso por gradiente, con tasa de aprendizaje $\eta>0$:
$$\theta\leftarrow\theta-\eta\,\nabla_\theta J(\theta)$$
- $\nabla_\theta J$ reúne las derivadas parciales de $J$ respecto de cada peso y cada sesgo
- $J$ depende de $\theta$ a través de una composición: $z^{[1]}\to a^{[1]}\to\cdots\to z^{[L]}\to a^{[L]}\to J$
- Por la regla de la cadena, el gradiente incluye $g'(z)$ de cada capa y la derivada de la pérdida respecto de la salida

## Descenso por gradiente: elementos

- $-\nabla_\theta J(\theta)$ es la dirección de mayor descenso local de $J$
- Tasa de aprendizaje $\eta$: si es muy pequeña el avance es lento; si es muy grande, $J$ puede oscilar o aumentar
- **Iteración**: una actualización de $\theta$
- **Época**: una pasada completa por el conjunto de entrenamiento
- **Minibatch** de tamaño $b$: cada actualización usa $b$ observaciones; hay $\lceil m/b\rceil$ iteraciones por época
- $J(\theta)$ no es convexa: el punto al que se llega depende de la inicialización
- Experimentos y detalles más adelante.


## Descenso por gradiente: ejemplo con un solo peso

Minimizar $L(w)=(w-3)^2$, con $L'(w)=2(w-3)$; actualización $w\leftarrow w-\alpha L'(w)$, con $w=0$ y $\alpha=0{,}2$.

| Iteración | $w$ | $L(w)$ | $L'(w)$ | Paso $-\alpha L'(w)$ | Nuevo $w$ |
|:-:|:-:|:-:|:-:|:-:|:-:|
| 0 | 0,00 | 9,00 | $-6{,}00$ | $+1{,}20$ | 1,20 |
| 1 | 1,20 | 3,24 | $-3{,}60$ | $+0{,}72$ | 1,92 |
| 2 | 1,92 | 1,17 | $-2{,}16$ | $+0{,}43$ | 2,35 |
| 3 | 2,35 | 0,42 | $-1{,}30$ | $+0{,}26$ | 2,61 |

- El error baja de 9,00 a 0,42 en tres pasos; los pasos se achican porque la pendiente disminuye al acercarse al mínimo ($w=3$)


## Descenso por gradiente: ejemplo con un solo peso
 
\begin{tikzpicture}[remember picture, overlay]
    \node[anchor=north, yshift=-1.55cm] at (current page.north)
    {
        \includegraphics[width=0.62\textwidth]{fig_gd_parabola.png}
    };
\end{tikzpicture}



## El papel de la tasa de aprendizaje $\alpha$

Para este ejemplo, $w_{t+1}-3=(1-2\alpha)(w_t-3)$: el error al cuadrado se multiplica por $(1-2\alpha)^2$ en cada paso.

- $\alpha=0{,}2$: factor $0{,}6$ en la distancia a $w=3$; converge sin oscilar
- $\alpha$ muy pequeño: factor cercano a 1; avance lento
- $\alpha=0{,}8$: factor $-0{,}6$; salta de un lado a otro del mínimo, pero converge
- $\alpha>1$: factor de módulo mayor que 1; el error crece y el método diverge
- En una red, $\alpha$ es $\eta$ 
- $\nabla J$ se calcula con la regla de la cadena 


(Revisar código con múltiples tasas de aprendizaje)

## El papel de la tasa de aprendizaje $\alpha$
 
\begin{tikzpicture}[remember picture, overlay]
    \node[anchor=north, yshift=-1.55cm] at (current page.north)
    {
        \includegraphics[width=0.66\textwidth]{fig_gd_alpha.png}
    };
\end{tikzpicture}



## Derivadas de las funciones de activación
 

- Para calcular $\nabla_\theta J$ se necesita derivar cada función de activación
- La salida de una neurona es $a=g(z)$, con $z=\mathbf{w}^\top\mathbf{x}+b$ su entrada a la activación; se deriva **con respecto a $z$**:
$$g'(z)=\frac{da}{dz}$$
- Como $a$ depende de $w_j$ y $b$ solo a través de $z$: $\ \dfrac{\partial a}{\partial w_j}=g'(z)\,x_j$, $\ \dfrac{\partial a}{\partial b}=g'(z)$
- Se reutilizan los valores $a=g(z)$ ya calculados en la propagación hacia adelante

| $g(z)$ | $g'(z)$ |
|:--|:--|
| sigmoide $\sigma(z)$ | $\sigma(z)\,(1-\sigma(z))$ |
| $\tanh(z)$ | $1-\tanh^2(z)$ |
| ReLU $\max(z,0)$ | $1$ si $z>0$; $0$ si $z<0$ |
 
En $z=0$ la derivada de ReLU no está definida; en la práctica se asigna 0 o 1.
 

<!--

## Derivada de la sigmoide

$$
\begin{aligned}
\sigma(z)&=\left(1+e^{-z}\right)^{-1}\\
\sigma'(z)&=-\left(1+e^{-z}\right)^{-2}\left(-e^{-z}\right)=\frac{e^{-z}}{\left(1+e^{-z}\right)^{2}}\\
&=\frac{1}{1+e^{-z}}\cdot\frac{e^{-z}}{1+e^{-z}}\\
&=\sigma(z)\,\bigl(1-\sigma(z)\bigr)
\end{aligned}
$$


 TODO: revisar, no está muy clara !!!

## Ejemplo numérico: un paso de descenso por gradiente

Una neurona sigmoide y una observación: $x=2$, $y=1$; $w=0{,}5$, $b=0$, $\eta=0{,}5$. Pérdida $\ell=-\ln a$ (entropía cruzada con $y=1$).

\small
$$\begin{aligned}
z&=wx+b=1, & a&=\sigma(1)=0{,}7311, & \ell&=0{,}3133\\[2pt]
\frac{\partial\ell}{\partial a}&=-\frac1a=-1{,}3679, & \sigma'(z)&=a(1-a)=0{,}1966, & \frac{\partial\ell}{\partial z}&=-1{,}3679\cdot0{,}1966=-0{,}2689\\[2pt]
\frac{\partial\ell}{\partial w}&=\frac{\partial\ell}{\partial z}\,x=-0{,}5379, & \frac{\partial\ell}{\partial b}&=\frac{\partial\ell}{\partial z}=-0{,}2689
\end{aligned}$$
\normalsize

- $w\leftarrow0{,}5-0{,}5\,(-0{,}5379)=0{,}7689$, \quad $b\leftarrow0-0{,}5\,(-0{,}2689)=0{,}1345$
- Con los nuevos valores: $z=1{,}6724$, $a=0{,}8419$, $\ell=0{,}1721<0{,}3133$


 TODO: revisar, no está muy clara !!!

## Gradiente de $J$ en la red $2\to3\to1$

Una observación $(x,y)$, salida sigmoide y entropía cruzada binaria; $\delta^{[l]}_k=\partial\ell/\partial z^{[l]}_k$.

:::::: {.columns align=top}
::: {.column width=52%}
**Capa oculta** (6 + 3 derivadas)
$$\delta^{[1]}_k=\delta^{[2]}\,w^{[2]}_{k}\,g'\!\left(z^{[1]}_k\right)$$
$$\frac{\partial \ell}{\partial w^{[1]}_{jk}}=\delta^{[1]}_k\,x_j\quad(j=1,2;\ k=1,2,3)$$
$$\frac{\partial \ell}{\partial b^{[1]}_k}=\delta^{[1]}_k$$
:::
::: {.column width=48%}
**Capa de salida** (3 + 1 derivadas)
$$\delta^{[2]}=a^{[2]}-y$$
$$\frac{\partial \ell}{\partial w^{[2]}_{k}}=\delta^{[2]}\,a^{[1]}_k\quad(k=1,2,3)$$
$$\frac{\partial \ell}{\partial b^{[2]}}=\delta^{[2]}$$
:::
::::::

- En total, $3+1+6+3=13$ derivadas, una por parámetro
- Para el costo: $\dfrac{\partial J}{\partial\theta}=\dfrac1m\displaystyle\sum_{i=1}^{m}\dfrac{\partial \ell^{(i)}}{\partial\theta}$



## Derivada de softmax

Con $p_k=e^{z_k}/\sum_j e^{z_j}$, la derivada es una matriz (jacobiana):

$$
\frac{\partial p_i}{\partial z_j}=p_i\left(\delta_{ij}-p_j\right)
=\begin{cases}
p_i(1-p_i) & i=j\\
-p_i\,p_j & i\neq j
\end{cases}
$$

donde $\delta_{ij}=1$ si $i=j$ y $0$ en otro caso.

-->

## La capa de salida según la tarea

| Tarea | Neuronas de salida | Activación | Pérdida |
|:--|:-:|:--|:--|
| Regresión | 1 | identidad | error cuadrático |
| Clasificación binaria | 1 | sigmoide | entropía cruzada binaria |
| Clasificación de $K$ clases | $K$ | softmax | entropía cruzada multiclase |

- Binaria: $\hat y=a^{[L]}$ estima $P(Y=1\mid\xv)$
- Multiclase: la clase predicha es la de mayor probabilidad

# Función de costo

## Pérdida y costo

- **Pérdida** $\ell(\hat y^{(i)},y^{(i)})$: error de una observación
- **Costo** $J$: promedio de las pérdidas sobre el conjunto de entrenamiento
$$J=\frac{1}{m}\sum_{i=1}^{m}\ell\left(\hat y^{(i)},y^{(i)}\right)$$
- Regresión (error cuadrático): $\ell=\tfrac12\left(\hat y-y\right)^2$
- En la literatura ambos términos se usan a veces de manera indistinta

## Entropía cruzada (clasificación binaria)

Pérdida para una observación con $y\in\{0,1\}$ y $a=\hat y$:

$$\ell(a,y)=-\bigl[\,y\log a+(1-y)\log(1-a)\,\bigr]$$

Costo para $m$ observaciones:

$$J=-\frac{1}{m}\sum_{i=1}^{m}\left[y^{(i)}\log a^{(i)}+\left(1-y^{(i)}\right)\log\left(1-a^{(i)}\right)\right]$$

- Es la **log-verosimilitud negativa** de un modelo Bernoulli con $P(Y=1\mid\xv)=a$
- Una red sin capa oculta y con una neurona sigmoide **es** la regresión logística

## Entropía cruzada (multiclase)

Con $y$ codificada *one-hot* y $\hat y_k$ salida de softmax:

$$J=-\frac{1}{m}\sum_{i=1}^{m}\sum_{k=1}^{K}y_k^{(i)}\log\hat y_k^{(i)}$$

- Es la log-verosimilitud negativa de un modelo categórico
- La entropía cruzada **no** es una distancia: no es simétrica
- Con $y$ *one-hot* coincide con la divergencia de Kullback--Leibler entre $y$ y $\hat y$

## Derivadas de la pérdida respecto de la salida

Para una observación:

- Sigmoide + entropía cruzada binaria:
$$\frac{\partial \ell}{\partial a}=-\frac{y}{a}+\frac{1-y}{1-a}=\frac{a-y}{a(1-a)}$$
- Softmax + entropía cruzada, respecto de la entrada $z_k$ de la capa de salida:
$$\frac{\partial \ell}{\partial z_k}=\hat y_k-y_k$$

Más adelante se ve que el caso binario también conduce a $\partial\ell/\partial z=a-y$.

# Comparación y ejemplo

## RNA frente a SVM

| | SVM con kernel | RNA (MLP) |
|:--|:--|:--|
| Función de decisión | $\wv^T\phi(\xv)+b$, $\phi$ **fija** | $\wv^T\phi(\xv)+b$, $\phi$ **aprendida** |
| Pérdida | bisagra (*hinge*) | entropía cruzada o cuadrática |
| Problema de optimización | convexo | **no** convexo |
| Hiperparámetros principales | $C$, kernel y sus parámetros | capas, neuronas, activación, tasa de aprendizaje, regularización |
| Salida probabilística | no directa | sí (sigmoide / softmax) |

## Ejemplo: frontera de decisión en el conjunto *moons*

\begin{tikzpicture}[remember picture, overlay]
    \node[anchor=north, yshift=-1.55cm] at (current page.north)
    {
        \includegraphics[width=0.95\textwidth]{fig_moons.png}
    };
\end{tikzpicture}

\vspace*{3.5cm}

- 300 puntos, ruido 0,25; 210 de entrenamiento y 90 de prueba
- Accuracy en prueba: regresión logística 0,778; MLP con 1 neurona 0,778; con 3 neuronas 0,922; con 20 neuronas 0,933
- Con 90 observaciones de prueba, diferencias pequeñas no son concluyentes

## Resumen

- El perceptrón es un clasificador lineal; no resuelve el XOR
- Una capa oculta con activación no lineal aprende una representación en la que las clases son separables
- Propagación hacia adelante: $Z^{[l]}=W^{[l]T}A^{[l-1]}+b^{[l]}$, $A^{[l]}=g(Z^{[l]})$
- Capa de salida y costo dependen de la tarea; la entropía cruzada es la log-verosimilitud negativa
- Activación no-lineal permite construir una aproximación no-lineal

**Temas pendientes**: backpropagation, regularización y validación$^*$.

## Referencias

- Rosenblatt, F. (1958). The perceptron: a probabilistic model for information storage and organization in the brain. *Psychological Review*, 65(6), 386--408. doi:10.1037/h0042519
- Minsky, M. y Papert, S. (1969). *Perceptrons: An Introduction to Computational Geometry*. MIT Press.
- Hastie, T., Tibshirani, R. y Friedman, J. (2009). *The Elements of Statistical Learning* (2.ª ed.). Springer. Cap. 11 (redes neuronales).
- Goodfellow, I., Bengio, Y. y Courville, A. (2016). *Deep Learning*. MIT Press.
