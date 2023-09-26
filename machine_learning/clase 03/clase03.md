docker run --rm -it -v ${PWD}:/workdir danteev/texlive pandoc
---
title: 
- EST-733 2022-II
subtitle:
- Machine Learning
author:
- Juan Zamora O.
#theme:
#- Copenhagen
date:
- Evaluación y Selección de modelos
header-includes: |
    \usepackage{breqn}
    \usepackage{tikz}
    \usetikzlibrary{calc,tikzmark,arrows,shapes,backgrounds}
    \usetikzlibrary{fit, arrows.meta, shapes}        
    \usepackage[T1]{fontenc}
    \usepackage[utf8]{inputenc}
    \usepackage{url}
    \usepackage{colortbl}

    \definecolor{LightRed}{RGB}{252,160,140}
    \definecolor{LightBlue}{RGB}{140,186,252}   
    \newcolumntype{a}{>{\columncolor{LightRed}}c}
    \newcolumntype{b}{>{\columncolor{LightBlue}}c}

    \newcommand{\empt}[2]{#1^{( #2 )}}
    \thispagestyle{empty}

    \titlegraphic { 
    \begin{tikzpicture}[overlay,remember picture]
    \node[below=-2.6cm] at (current page.south){
        \includegraphics[width=6cm]{logosAzul.png}
    };
    \end{tikzpicture}
    }
    \logo{
	\begin{tikzpicture}[overlay,remember picture]
		\node[opacity=0.4,right=-0.6cm, above=0.07cm] at (current page.south east){
    			\includegraphics[height=1cm]{logoAzul.png}
        };
	\end{tikzpicture}
    }
---
# Introducción

<!--
  pandoc -t beamer ./clase03.md -o clase03.pdf --katex --slide-level=2
 -->


- La calidad de un método se mide por su capacidad de generalización
- Esta capacidad se relaciona con su poder predictivo sobre datos de prueba independientes
- Es muy importante poder evaluar este desempeño 
  - Guía la elección del *método de aprendizaje*/modelo
  - Entrega medida de la calidad esperada del modelo escogido


<!-- metodos clave para la evlauación del desempeño y su uso para la selección de modelos-->

## Sesgo y Varianza

**Escenario general** 

Se tiene una variable objetivo $Y\in \mathbb{R}$, un vector de entradas $X$ y un modelo de predicción $\hat{f}(X)$ estimada a partir de un conjunto de entrenamiento $\mathcal{T}$.


La función que permite cuantificar el error en las predicciones se denomina **función de pérdida** y se denota mediante $L(Y, \hat{f}(X))$

---

* Algunas elecciones para esta función de pérdida son
$$
L(Y,\hat{f}(X))=
  \begin{cases}
  (Y-\hat{f}(X))^2 & \mbox{, error cuadr\'atico}\\
  |Y-\hat{f}(X)| & \mbox{, error absoluto}
  \end{cases}
$$

---

* Para respuestas categóricas $G$ con $K$ valores, generalmente se modelan las probabilidades $p_k(X)=Pr(G=k|X)$ y se escoge $\hat{G}(X)=\underset{k}{\operatorname{argmax}}\hat{p}_k$
$$
\begin{array}{ccc} 
L(G,\hat{G}(X))= & I(G\neq\hat{G}(X))^2 & \mbox{, p\'erdida 0-1}\\
L(G,\hat{p}(X))= & -2\sum_{k=1}^{K}log\ \hat{p}_k(X)& \mbox{, \textit{deviance}}\\
\end{array}
$$ 

## Error de predicción

* El error de generalización o **error de prueba** corresponde al error de predicción  sobre una muestra de prueba independiente específica $\mathcal{T}$
    $$Err_{\mathcal{T}}=E[L(Y,\hat{f}(X))|\mathcal{T}]$$
    * Cada par $(X,Y)$ es escogido al azar a partir de su distribución conjunta

---

* Otra cantidad relacionada es el error de predicción esperado
    $$Err = E[Err_{\mathcal{T}}] = E[L(Y,\hat{f}(X))]$$
  
    * En este caso la esperanza se calcula sobre todo lo aleatorio, incluyendo la aleatoriedad en el conjunto de entrenamiento $\mathcal{T}$ que produjo $\hat{f}$.

* A continuación, se muestra ejemplo de modelo ajustado sobre 100 conjuntos de entrenamiento distintos ($Err_{\mathcal{T}}$ en rojo claro)
  
---

\begin{tikzpicture}[remember picture, overlay]
    \node[below=1cm,font=\fontsize{11pt}{11pt}\selectfont,text width=10cm] at (current page.north)  {Modelo ajustado sobre 100 conjuntos simulados de entrenamiento distintos ($Err_{\mathcal{T}}$ en rojo claro). La estimación de $Err$ es el promedio y aparece en rojo oscuro.};

    \node[above=1.0cm] at (current page.south) 
    {
        \includegraphics[width=0.7\textwidth]{test_train_sample_errors.png}
    };
    \node[below=-1cm,font=\fontsize{5pt}{5pt}\selectfont] at (current page.south)  {Fuente fuente \textit{Hastie et al., 2017}};
\end{tikzpicture}

<!-- 
---

- La estimación de $Err$ tiene mayor sintonía con un análisis estadístico, no es posible estimar el error condicional, dada solamente la información de el mismo conjunto de entrenamiento
- Nuestro objetivo será realizar una estimación de $Err_{\mathcal{T}}$-->


## Error de entrenamiento

- Se define como la pérdida promedio sobre la muestra de entrenamiento
$$\overline{err}=\frac{1}{|\mathcal{T}|}\sum_{i=1}^{|\mathcal{T}|}L(y_i, \hat{f}(x_i))$$

o también

$$\overline{err}=-\frac{2}{|\mathcal{T}|}\sum_{i=1}^{|\mathcal{T}|}log\ \hat{p}_{g_i}(x_i)$$

---

- En la figura anterior, el error de entrenamiento aparece en azul.
- Este error es un **estimador optimista** del error de predicción

## Error vs complejidad del modelo

- A medida que el modelo aumenta su complejidad se adapta de manera más cercana a los datos de entrenamiento
- Es decir, se produce una disminución del error de entrenamiento
- La complejidad está asociada a algún parámetro del modelo
- Se produce una disminución en el sesgo y un aumento en la varianza del error de predicción

## ¿Para qué todo esto?

Perseguiremos dos tareas/objetivos 

- **Selección del modelo**
  - Estimar el desempeño de diferentes modelos para escoger el mejor
- **Evaluación del Modelo**
  - Luego de escoger el mejor modelo, estimar su error de predicción sobre nuevos datos

---

### Escenario con abundancia de datos

- Ambos problemas pueden ser abordados dividiendo los datos en 3 grupos

    |   |   |   |
    |---|---|---|
    | **Entrenamiento** | **Validación** | **Prueba** |
    |---|---|---|
    | Para ajustar los modelos | Estimar error de pred. en la selección de modelos | Evaluación del error de generalización para el modelo escogido

- Muchos/Pocos datos depende de la complejidad del modelo, razón señal a ruido de función generadora de los datos ...

---

### Escenario con insuficiencia de datos

- Métodos analíticos: AIC, BIC, MDL
  - Útiles para clases de estimadores lineales en sus parámetros
  - Usados para comparar entre modelos en lugar de estimar capacidad de generalización
- Remuestreo: CV o Bootstrap
  - Útilidad para cualquier estimador del error de predicción

<!-- Si alcanzo, completar con la descomposición sesgo varianza de la p.223-->

## Validación Cruzada

- Mecanismo más simple y usado para estimar el error de predicción
- Usaremos parte de los datos disponibles para ajustar el modelo y otra parte distinta para probarlo (varias veces)

---

### K-Fold cv

- Datos se dividen en $K$ grupos de igual tamaño
- E.g. $K=5$
\vspace{10pt}

\begin{table}[]
\begin{tabular}{baaaa}
\hline
  Valid & Train & Train & Train & Train  \\ 
\end{tabular}

\begin{tabular}{abaaa}
  Train & Valid & Train & Train & Train  \\ 
\end{tabular}

\begin{tabular}{aabaa}
  Train & Train & Valid & Train & Train \\ 
\end{tabular}

\begin{tabular}{aaaba}
  Train & Train & Train & Valid & Train \\ 
\end{tabular}

\begin{tabular}{aaaab}
  Train & Train & Train & Train & Valid  \\ \hline
\end{tabular}
\end{table}
\vspace{10pt}

- Se ajusta el modelo con $K-1$ partes y se calcula el error de predicción sobre la restante

---

- Se obtienen $K$ estimaciones del error de predicción
- Cada observación $i$ es mapeada a una partición mediante la función $\kappa : \{ 1\ldots N\}\longrightarrow\{1\ldots K\}$
- Además, anotemos como $\hat{f}^{-k}(x)$ a la función ajustada calculada sin la $k$-ésima parte del conjunto de datos 
- Luego, el estimador CV del error de predicción es 

$$CV(\hat{f})=\frac{1}{N}\sum_{i=1}^{N}L(y_i,\hat{f}^{-\kappa(i)}(x_i))$$

---

#### Selección de Modelo usando k-fold cv


Si consideramos un conjunto de modelos indexados sobre el parámetro $\alpha$, anotaremos $\hat{f}_{\alpha}^{-k}(x)$ al $\alpha$-ésimo modelo ajustado sin la $k$-ésima parte del conjunto de datos

La siguiente función entregará estimador de su error de predicción 

$$CV(\hat{f}_{\alpha})=\frac{1}{N}\sum_{i=1}^{N}L(y_i,\hat{f}_{\alpha}^{-\kappa(i)}(x_i))$$

Finalmente, el valor $\hat{\alpha}$ que la minimiza nos permitirá seleccionar nuestro modelo.

---

### Consideraciones generales

- Valor de $k$ generalmente está entre $5$ y $10$
- Algunos métodos pueden ser muy sensibles al tamaño del conjunto de entrenamiento, especialmente cuando hay pocos datos ($<100$)
- Usar información de la respuesta $Y$ antes de aplicar k-fold cv sobre los mismos datos es trampa
  - Se obtendrá una estimación optimista del error
  - Por ejemplo, seleccionar variables usando Información Mutua sobre todos los datos antes de aplicar CV.


## Actividad

1. Averigüe acerca del uso de la Información mutua para selección de variables
2. Busque en `Scikit-learn` cómo realizar este cálculo respecto de la variable objetivo (*target*)
3. Escoja un conjunto de datos para la tarea de clasificación
4. *Rankee* las co-variables según Información mutua
5. Escoja las top-$P$
6. Escoja un modelo de clasificación (e.g. Naive Bayes) y fije los valores de sus parámetros
7. Realice $k$-fold CV usando únicamente los predictores seleccionados
8. Reporte $CV(\hat{f}_{\alpha})$
9. Repita 5-8 para 3 valores distintos de $P$