---
title: EST-852
subtitle: Métodos de Kernel y SVM
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

# Motivación y clasificación por similitud

## Objetivos de la clase

Al finalizar la sesión, el estudiante podrá:

1. Formular la clasificación binaria como un problema de separación geométrica con margen.
2. Plantear los problemas primal y dual de la SVM de margen máximo e identificar los vectores soporte.
3. Extender la formulación a margen suave e interpretarla como *hinge loss* más regularización.
4. Construir fronteras no lineales mediante funciones de kernel (truco del kernel, condición de semidefinición positiva).
5. Seleccionar $C$ y $\gamma$ mediante validación cruzada y reconocer las limitaciones prácticas del método.

## Planteamiento del problema

Se dispone de $m$ observaciones etiquetadas

$$(\xv_1,y_1),\ldots,(\xv_m,y_m)\in\Xs\times\{\pm1\}.$$

El aprendizaje consiste en **generalizar** a objetos no vistos: dado un nuevo $\xv\in\Xs$, predecir su etiqueta $y\in\{\pm1\}$.

- En esta sesión se escoge $y$ de modo que el par $(\xv,y)$ sea *similar* a los ejemplos de entrenamiento.
- Por lo tanto, se necesita una **medida de similitud** en $\Xs$. No cualquier función sirve: debe cumplir ciertas propiedades (sección de kernels).

Notación: $m$ = número de observaciones; $d$ = dimensión, con $\Xs\subset\R^d$.

## Muchos hiperplanos separan los datos

\begin{center}
\includegraphics[height=0.42\textheight]{fig_hiperplanos.png}
\end{center}

- Si las clases son linealmente separables, existen infinitos hiperplanos con error de entrenamiento nulo.
- ¿Cuál elegir? El que maximiza el **margen**: la distancia mínima a los puntos de entrenamiento.
- Justificación: robustez ante pequeñas perturbaciones de los datos y una cota de generalización basada en los vectores soporte (se verá más adelante).

## Clasificador de centroides

Sea $\Xs\subset\R^d$ y supongamos que ambas clases tienen observaciones ($m_+,m_->0$).

$$\cv_+=\frac{1}{m_+}\sum_{i:\,y_i=+1}\xv_i,\qquad
  \cv_-=\frac{1}{m_-}\sum_{i:\,y_i=-1}\xv_i,\qquad
  \cv=\tfrac12(\cv_++\cv_-)$$

:::::: columns
::: {.column width="46%"}
- Regla: asignar el nuevo punto $\xv$ a la clase cuyo centroide esté más cerca.
- No se requiere separabilidad lineal. Tampoco se garantiza error de entrenamiento nulo cuando las clases son separables.
:::
::: {.column width="54%"}
\includegraphics[width=\linewidth,height=0.60\textheight,keepaspectratio]{fig_centroides.png}
:::
::::::

## Regla de decisión geométrica

Asignar $\xv$ al centroide más cercano equivale a evaluar el signo de una proyección:

$$\norm{\xv-\cv_-}^2-\norm{\xv-\cv_+}^2 \;=\; 2\,\ip{\xv-\cv}{\cv_+-\cv_-}$$

- El ángulo entre el vector $\xv-\cv$ (de $\cv$ a $\xv$) y $\cv_+-\cv_-$ (que conecta los centros de ambas clases) es menor que $\pi/2$ si y solo si $\xv$ está más cerca de $\cv_+$.
- La regla se formula solo con el producto interno $\ip{\cdot}{\cdot}$:

$$y=\sgn\,\ip{\xv-\cv}{\cv_+-\cv_-}$$

## Desarrollo de la regla

$$\begin{aligned}
y &= \sgn\,\ip{\xv-\cv}{\cv_+-\cv_-}\\[2pt]
  &= \sgn\Big(\ip{\xv}{\cv_+}-\ip{\xv}{\cv_-}-\tfrac12\big(\norm{\cv_+}^2-\norm{\cv_-}^2\big)\Big)\\[2pt]
  &= \sgn\Big(\ip{\xv}{\cv_+}-\ip{\xv}{\cv_-}+b\Big),
  \qquad b=\tfrac12\big(\norm{\cv_-}^2-\norm{\cv_+}^2\big)
\end{aligned}$$

Se usó que $\ip{\cv}{\cv_+-\cv_-}=\tfrac12\big(\norm{\cv_+}^2-\norm{\cv_-}^2\big)$.

## Forma en productos internos

Sustituyendo los centroides:

$$y=\sgn\Big(\frac{1}{m_+}\sum_{i:\,y_i=+1}\ip{\xv}{\xv_i}-\frac{1}{m_-}\sum_{i:\,y_i=-1}\ip{\xv}{\xv_i}+b\Big)$$

y el término $b$ también se expresa con productos internos:

$$b=\frac12\Big(\frac{1}{m_-^2}\sum_{\substack{(i,j):\\ y_i=y_j=-1}}\ip{\xv_i}{\xv_j}
 -\frac{1}{m_+^2}\sum_{\substack{(i,j):\\ y_i=y_j=+1}}\ip{\xv_i}{\xv_j}\Big)$$

## De $\ip{\xv}{\xv_i}$ a $k(\xv,\xv_i)$

**Observación clave:** los datos intervienen solo a través de productos internos. Si se reemplazan por una función de similitud $k$:

$$y=\sgn\Big(\frac{1}{m_+}\sum_{i:\,y_i=+1}k(\xv,\xv_i)-\frac{1}{m_-}\sum_{i:\,y_i=-1}k(\xv,\xv_i)+b\Big)$$

- El mismo algoritmo opera ahora con la noción de similitud $k$.
- Con un kernel gaussiano, las sumas son (salvo una constante) estimadores de densidad de ventana de Parzen de cada clase.
- Pregunta: ¿qué funciones $k$ son admisibles y qué espacio inducen? (siguiente sección)

# Kernels y espacio de características

## Limitaciones del producto interno en el espacio de entrada

- Las clases pueden no ser linealmente separables.
- $\Xs$ no siempre es un espacio con producto interno (grafos, cadenas de caracteres, etc.).

**Solución:** representar los objetos en un espacio $\Hs$ con producto interno (*espacio de características*) mediante el mapeo

$$\Phi:\Xs\to\Hs,\qquad x\mapsto\xv:=\Phi(x)$$

y medir la similitud con

$$k(x,x'):=\ip{\Phi(x)}{\Phi(x')}$$

## Beneficios de incrustar los datos en $\Hs$

1. Asegura que la medida de similitud proviene de un producto interno: $k(x,x')=\ip{\Phi(x)}{\Phi(x')}$.
2. Permite abordar la clasificación de manera geométrica (hiperplanos, ángulos, distancias).
3. Un mapeo $\Phi$ no lineal cambia la representación vectorial hacia una más adecuada para el problema.

## Ejemplo: mapeo cuadrático

$$\Phi:\R^2\to\R^3,\qquad (x_1,x_2)\mapsto(z_1,z_2,z_3)=(x_1^2,\sqrt2\,x_1x_2,x_2^2)$$

\begin{center}
\includegraphics[height=0.44\textheight]{fig_mapeo.png}
\end{center}

Una frontera elíptica $a x_1^2+b x_2^2=c$ en el espacio de entrada se transforma en el hiperplano $a z_1+b z_3=c$ en $\R^3$. Aprender la frontera se reduce a estimar un hiperplano con los puntos mapeados.

## El truco del kernel

$$\ip{\Phi(x)}{\Phi(x')}=x_1^2x_1'^2+2x_1x_2x_1'x_2'+x_2^2x_2'^2=(x_1x_1'+x_2x_2')^2=\ip{x}{x'}^2$$

- Se puede evaluar $k$ sin calcular $\Phi$ explícitamente.
- Kernel polinomial homogéneo de grado $p$ en $\R^d$: $\Phi$ tiene $\binom{d+p-1}{p}$ coordenadas. Con $d=100$ y $p=3$ son $171.700$, mientras que evaluar $k$ cuesta $O(d)$ operaciones.
- El kernel gaussiano corresponde a un espacio $\Hs$ de dimensión infinita.

## Condición de semidefinición positiva (Mercer)

\small

Una función $k:\Xs\times\Xs\to\R$ es un kernel válido si es

- **simétrica:** $k(x,x')=k(x',x)$, y
- **semidefinida positiva:** para todo $n\in\mathbb{N}$, $x_1,\ldots,x_n\in\Xs$ y $a\in\R^n$,
$$\sum_{i=1}^{n}\sum_{j=1}^{n}a_ia_j\,k(x_i,x_j)\ge0$$
(equivalentemente, la matriz de Gram $K_{ij}=k(x_i,x_j)$ es semidefinida positiva).

Entonces existe $\Phi:\Xs\to\Hs$ tal que $k(x,x')=\ip{\Phi(x)}{\Phi(x')}$.

<!--
- Esta condición caracteriza los núcleos semidefinidos positivos (teorema de Moore–Aronszajn). El teorema de Mercer añade una expansión en autofunciones para kernels continuos en dominios compactos.
- Verificación práctica: los autovalores de la matriz de Gram deben ser $\ge0$. El kernel sigmoide $\tanh(\kappa\ip{x}{x'}+\theta)$ no es semidefinido positivo para todos los parámetros.
-->

## Kernels usuales

| Kernel | $k(x,x')$ | Parámetros |
|:-------|:----------|:-----------|
| Lineal | $\ip{x}{x'}$ | --- |
| Polinomial | $(\ip{x}{x'}+1)^p$ | grado $p$ |
| Gaussiano (RBF) | $\exp\!\big(-\norm{x-x'}^2/2\sigma^2\big)=\exp\!\big(-\gamma\norm{x-x'}^2\big)$ | $\gamma=1/2\sigma^2$ |

- Con $\gamma$ grande ($\sigma$ pequeño) la similitud es muy local.
- Sumas y productos de kernels (con coeficientes positivos) son kernels.
- Existen kernels para objetos estructurados (cadenas de caracteres, grafos, etc.): miden similitud mediante productos internos en un espacio de características mejor dotado que el espacio original de atributos.

# SVM de margen máximo

## Hiperplano separador y margen

:::::: columns
::: {.column width="55%"}
- Función de decisión: $f(\xv)=\ip{\wv}{\xv}+b$, con clasificador $y(\xv)=\sgn f(\xv)$.
- La distancia de $\xv$ al hiperplano $f=0$ es $|f(\xv)|/\norm{\wv}$.
- $(\wv,b)$ está definido solo salvo escala positiva. **Forma canónica:** se escala de modo que $\min_i y_if(\xv_i)=1$.
- Los hiperplanos $f=\pm1$ pasan por los puntos más cercanos y distan entre sí $2/\norm{\wv}$ (el **margen**).
:::
::: {.column width="45%"}
\includegraphics[width=\linewidth,height=0.74\textheight,keepaspectratio]{fig_margen.png}
:::
::::::

## Problema primal

$$\min_{\wv,b}\ \tfrac12\norm{\wv}^2\qquad\text{sujeto a}\qquad y_i\big(\ip{\wv}{\xv_i}+b\big)\ge1,\quad i=1,\ldots,m$$

- Maximizar el margen $2/\norm{\wv}$ es equivalente a minimizar $\tfrac12\norm{\wv}^2$ (mismo minimizador; los valores óptimos no coinciden).
- Es un programa cuadrático convexo con restricciones lineales: no hay mínimos locales.
- Si las clases son linealmente separables, existe solución global y es única.

## Lagrangiano y condiciones KKT

$$L(\wv,b,\alpha)=\tfrac12\norm{\wv}^2-\sum_{i=1}^m\alpha_i\Big(y_i\big(\ip{\wv}{\xv_i}+b\big)-1\Big),\qquad\alpha_i\ge0$$

- Se **minimiza** respecto a $(\wv,b)$ y se **maximiza** respecto a $\alpha\ge0$ (punto silla).
- Derivando: $\ \wv=\sum_i\alpha_iy_i\xv_i\ $ y $\ \sum_i\alpha_iy_i=0$.
- Holgura complementaria: $\alpha_i\big[y_i(\ip{\wv}{\xv_i}+b)-1\big]=0$.
- Luego $\alpha_i>0$ solo si $y_if(\xv_i)=1$: el punto está sobre el margen. Esos puntos son los **vectores soporte**.

## Problema dual

Sustituyendo $\wv=\sum_i\alpha_iy_i\xv_i$ y $\sum_i\alpha_iy_i=0$ en $L$:

$$\max_{\alpha}\ \sum_{i=1}^m\alpha_i-\tfrac12\sum_{i,j=1}^m\alpha_i\alpha_jy_iy_j\ip{\xv_i}{\xv_j}
\quad\text{s.a.}\quad\alpha_i\ge0,\ \ \sum_{i}\alpha_iy_i=0$$

Función de decisión:

$$f(\xv)=\sum_{i=1}^m\alpha_iy_i\ip{\xv_i}{\xv}+b,\qquad b=y_s-\sum_i\alpha_iy_i\ip{\xv_i}{\xv_s}$$

donde $\xv_s$ es cualquier vector soporte ($\alpha_s>0$). Solo los vectores soporte contribuyen a la suma.

## Del dual al truco del kernel

Los datos aparecen únicamente a través de $\ip{\xv_i}{\xv_j}$. Reemplazándolos por $k(\xv_i,\xv_j)$:

$$\max_{\alpha}\ \sum_{i}\alpha_i-\tfrac12\sum_{i,j}\alpha_i\alpha_jy_iy_j\,k(\xv_i,\xv_j),\qquad
f(\xv)=\sum_{i\in SV}\alpha_iy_i\,k(\xv_i,\xv)+b$$

- Así se combinan el clasificador de margen máximo y el cálculo implícito de $\Phi$ (Boser, Guyon y Vapnik, 1992).
- Nunca se calculan $\Phi(\xv)$ ni $\wv$ en $\Hs$.
- Si $k$ es semidefinido positivo, el problema sigue siendo un programa cuadrático convexo.

## Vectores soporte y generalización

- Solo los vectores soporte determinan el hiperplano: eliminar un punto con $\alpha_i=0$ no modifica la solución.
- Cota de generalización (Cortes y Vapnik, 1995):

$$\mathbb{E}\big[P(\text{error})\big]\;\le\;\frac{\mathbb{E}\big[\text{n.º de vectores soporte}\big]}{m}$$

(las esperanzas se toman sobre muestras de entrenamiento).

- La cota no contiene explícitamente la dimensión del espacio de características.
- Por lo tanto, pocos vectores soporte sugieren buena generalización, incluso si $\Hs$ tiene dimensión muy alta.

# SVM de margen suave

## Formulación primal con holguras

- Con ruido o clases traslapadas, el hiperplano separador puede no existir.
- Se introducen **variables de holgura** $\xi_i\ge0$ (con $\Phi(\xv)=\xv$ se recupera el caso lineal):
$$y_i\big(\ip{\wv}{\Phi(\xv_i)}+b\big)\ge1-\xi_i,\qquad\xi_i\ge0$$

$$\min_{\wv,b,\xi}\ \tfrac12\norm{\wv}^2+C\sum_{i=1}^m\xi_i$$

- $\xi_i=0$: bien clasificado y fuera del margen; $0<\xi_i\le1$: dentro del margen pero bien clasificado; $\xi_i>1$: mal clasificado.
- $C>0$ balancea margen ancho y error de entrenamiento. Es un hiperparámetro: se elige por validación cruzada.

## Problema dual con restricción de caja

$$\max_{\alpha}\ \sum_{i}\alpha_i-\tfrac12\sum_{i,j}\alpha_i\alpha_jy_iy_j\,k(\xv_i,\xv_j)
\quad\text{s.a.}\quad0\le\alpha_i\le C,\ \ \sum_i\alpha_iy_i=0$$

- Única diferencia con el margen duro: la cota superior $\alpha_i\le C$ (aparece al derivar respecto a $\xi_i$).
- $\wv=\sum_i\alpha_iy_i\Phi(\xv_i)$ y $f(\xv)=\sum_i\alpha_iy_i\,k(\xv_i,\xv)+b$.

## Tres tipos de puntos

:::::: columns
::: {.column width="50%"}
- $\alpha_i=0$: $\ y_if(\xv_i)\ge1$. Sin influencia en la solución.
- $0<\alpha_i<C$: $\ y_if(\xv_i)=1$. Sobre el margen ($\xi_i=0$).
- $\alpha_i=C$: $\ y_if(\xv_i)\le1$. Dentro del margen o mal clasificado ($\xi_i\ge0$).

Los **vectores soporte** son los puntos con $\alpha_i>0$.
:::
::: {.column width="50%"}
\includegraphics[width=\linewidth,height=0.78\textheight,keepaspectratio]{fig_tipos_puntos.png}
:::
::::::

## Hinge loss y regularización

Eliminando las holguras, $\xi_i=\max\big(0,1-y_if(\xv_i)\big)$, y el problema es equivalente a
$$\min_{\wv,b}\ \sum_{i=1}^m\max\big(0,\,1-y_if(\xv_i)\big)+\lambda\norm{\wv}^2,\qquad\lambda=\frac{1}{2C}$$

:::::: columns
::: {.column width="54%"}
- Pérdida *hinge* más penalización $\ell_2$: misma estructura que ridge (ESL, §12.3.2).
- El hinge es una cota superior convexa de la pérdida 0-1.
- Es exactamente cero cuando $y_if(\xv_i)\ge1$: los puntos fuera del margen no influyen (esparsidad). La pérdida logística nunca es cero.
- $C$ grande $\Leftrightarrow$ $\lambda$ pequeño $\Leftrightarrow$ poca regularización.
:::
::: {.column width="46%"}
\includegraphics[width=\linewidth,height=0.46\textheight,keepaspectratio]{fig_hinge.png}
:::
::::::

## Efecto del hiperparámetro $C$

\begin{center}
\includegraphics[width=0.97\textwidth,height=0.38\textheight,keepaspectratio]{fig_C.png}
\end{center}

- $C$ pequeño: margen ancho, se toleran muchas violaciones, más vectores soporte; mayor sesgo y menor varianza (riesgo de subajuste).
- $C$ grande: margen estrecho, se penalizan las violaciones; menor sesgo y mayor varianza (riesgo de sobreajuste).
- Algunos textos parametrizan con un *presupuesto* de violaciones, lo que invierte el rol de $C$: verifique la convención de cada texto o software.

# SVM no lineal en la práctica

## Kernel gaussiano: efecto de $\gamma$ junto con $C$

:::::: columns
::: {.column width="42%"}
$$f(\xv)=\sum_{i\in SV}\alpha_iy_i\,e^{-\gamma\norm{\xv_i-\xv}^2}+b$$

- $\gamma$ pequeño: influencia amplia de cada punto, frontera suave (casi lineal).
- $\gamma$ grande: influencia local, frontera muy flexible (sobreajuste). Con $C$ pequeño casi todos los puntos terminan como vectores soporte.
- $C$ y $\gamma$ interactúan: se ajustan **conjuntamente**.
:::
::: {.column width="58%"}
\includegraphics[width=\linewidth,height=0.8\textheight,keepaspectratio]{fig_grid_C_gamma.png}
:::
::::::

## Preprocesamiento y selección de hiperparámetros

\small

- **Estandarizar** las variables antes de usar kernels basados en distancias o productos internos: sin esto, las variables de mayor escala dominan.
- Buscar $(C,\gamma)$ en una **grilla logarítmica** (p. ej. de $10^{-3}$ a $10^{3}$) con validación cruzada $k$-fold; reservar un conjunto de prueba independiente para la evaluación final.
- **Desbalance de clases:** ponderar $C$ por clase (`class_weight`) y evaluar con métricas adecuadas (F1, AUC-PR), no solo exactitud.
- **Probabilidades:** $f(\xv)$ no es una probabilidad; si se necesitan, se calibra la salida (escalamiento de Platt).
- **Costo computacional:** la matriz de Gram es $m\times m$ (memoria $O(m^2)$) y el tiempo de entrenamiento crece típicamente entre cuadrático y cúbico en $m$. Para $m$ grande, preferir SVM lineal o aproximaciones de kernel.

## Demostración en Python {.fragile}

\footnotesize

```python
from sklearn.datasets import make_moons
from sklearn.svm import SVC
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import GridSearchCV

X, y = make_moons(300, noise=0.3, random_state=0)
pipe = make_pipeline(StandardScaler(), SVC(kernel="rbf"))
grid = GridSearchCV(pipe, {"svc__C": [0.01, 0.1, 1, 10, 100],
                           "svc__gamma": [0.01, 0.1, 1, 10]}, cv=5)
grid.fit(X, y)
print(grid.best_params_, grid.best_score_)
print(grid.best_estimator_["svc"].n_support_)  # vectores soporte por clase
```

En `scikit-learn`, `gamma` es el $\gamma$ de $\exp(-\gamma\norm{x-x'}^2)$.

## Extensiones

- **Multiclase:** se combinan SVM binarias (uno-contra-uno o uno-contra-resto).
- **Regresión (SVR):** pérdida $\varepsilon$-insensible (ESL, §12.3.6 y §12.3.7).
- **Kernels para datos estructurados:** cadenas de caracteres, grafos.
- **Probabilidades calibradas:** si son el objetivo principal, considerar regresión logística.

## Comparación con otros clasificadores lineales

| Propiedad | Perceptrón | Regresión logística | SVM |
|:--------------|:--------------------------|:----------------------|:--------------------------|
| Pérdida | $\max(0,-yf)$ | $\log(1+e^{-yf})$ | $\max(0,1-yf)$ |
| Solución | cualquier hiperplano separador (no única) | única (con regularización) | hiperplano de margen máximo |
| Depende de | puntos mal clasificados durante el entrenamiento | todos los puntos | solo vectores soporte |
| Probabilidades | no | sí | no (requiere calibración) |

# Cierre

## Resumen

- Los objetos se mapean a un espacio de características $\Hs$; el producto interno se calcula **en ese espacio** a través de la función kernel.
- La clasificación se realiza con el hiperplano de margen máximo en $\Hs$.
- Ese hiperplano queda determinado por los vectores soporte ($\alpha_i>0$); el problema dual depende de los datos solo mediante $k(\xv_i,\xv_j)$.
- El margen suave relaja las restricciones con variables de holgura y equivale a minimizar *hinge loss* más una penalización $\ell_2$.
- $C$ controla el balance entre margen máximo y error de entrenamiento; con kernel gaussiano, $\gamma$ controla la flexibilidad de la frontera. Ambos se eligen por validación cruzada, con variables previamente estandarizadas.

## Preguntas para discusión

1. Si se elimina del conjunto de entrenamiento un punto con $\alpha_i=0$, ¿cambia la solución? ¿Y si se elimina un vector soporte?
2. ¿Cómo varía el número de vectores soporte cuando $C\to0$ y cuando $C\to\infty$?
3. ¿Por qué conviene estandarizar las variables antes de usar el kernel gaussiano?
4. Muestre que $k(x,x')=(\ip{x}{x'}+1)^2$ en $\R^2$ corresponde a un mapeo explícito $\Phi:\R^2\to\R^6$.

## Referencias

\footnotesize

- Boser, B. E., Guyon, I. M. y Vapnik, V. N. (1992). A training algorithm for optimal margin classifiers. *Proceedings of COLT '92*, 144--152. <https://doi.org/10.1145/130385.130401>
- Cortes, C. y Vapnik, V. (1995). Support-vector networks. *Machine Learning*, 20, 273--297. <https://doi.org/10.1007/BF00994018>
- Schölkopf, B. y Smola, A. J. (2002). *Learning with Kernels*. MIT Press.
- Hastie, T., Tibshirani, R. y Friedman, J. (2009). *The Elements of Statistical Learning* (2.ª ed.), cap. 12. Springer.
- James, G., Witten, D., Hastie, T. y Tibshirani, R. (2013). *An Introduction to Statistical Learning*, cap. 9. Springer.

<!-- Figuras: generadas con `figuras.py` (scikit-learn y matplotlib).-->
