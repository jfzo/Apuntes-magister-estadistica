---
title: Introducción
topic: EST852 -- Machine Learning
author: Juan Zamora O.
date: Octubre, 2024.
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
toc: true
toc-title: Estructura de la Presentación
section-titles: false
---


# Introducción

<!--
 pandoc -t beamer ./clase01.md -o clase01.pdf --katex --slide-level=2
 -->

- Subconjunto de la IA que incluye técnicas estadísticas que permiten que los algoritmos computacionales (máquinas) mejoren en su desempeño deuna tarea a medida que ganan experiencia ejecutandola.
- Algoritmos usados para segmentar los datos y predecir la verosimilitud de eventos futuros basandose en eventos pasados
- Programas pueden realizar tareas sin un conjunto de instrucciones programadas explicitamente para hacerlo


## Statistical Learning vs Machine Learning

- No hay una definición clara
- Diferencia puede venir 
  - del origen de los métodos
  - del volúmen y dimensionalidad de los datos usados
- Durante el desarrollo de este curso **no** haremos distinción alguna entre ellas

---

\begin{tikzpicture}[remember picture, overlay]
    \node[above=1.5cm] at (current page.south) 
    {
        \includegraphics[width=0.9\textwidth]{data-mining-Venn-diagram.png}
    };
    \node[below=-1cm,font=\fontsize{5pt}{5pt}\selectfont] at (current page.south)  {Fuente \url{wikipedia.org}};
\end{tikzpicture}


<!-- Todos los modelos están errados, la pregunta práctica es que tan errados tienen que estar para dejar de ser útiles. G.Box.
-->

## Tipos de Aprendizaje

En general se divide en tres grandes categorias:

1. Predictivo o **Supervisado**
2. No Supervisado
3. Reforzado
  
---

1. Predictivo o **Supervisado**
  - Observaciones (datos) representados por vectores $\mathbf{x}$ junto a las respuestas/salidas $\mathbf{y}$  generadas por el Sistema.
  - Cada $x_i$ es un vector $M$ dimensional y representa la colección de $M$ atributos medidos o covariables.
  - Las respuestas $y_i$ pueden ser nominal/categórica o real
  - El objetivo es aprender la asociación entre las covariables y la salida usando los datos ${(x_i,y_i)}_{i=1}^N$


---

2. Descriptivo o **No-Supervisado**
  - Observaciones (datos) representados por vectores $\mathbf{x}$ 
  - Cada $x_i$ es un vector $M$ dimensional y representa la colección de $M$ atributos medidos o covariables.
  - El objetivo es encontrar patrones que puedan ser útiles o interesantes

---

3. Reforzado
   - Consiste en aprender a actuar o comportarse usando mecanismos de recompensa y castigo

  \begin{tikzpicture}[remember picture, overlay]
    \node[above=1.0cm] at (current page.south) 
    {
        \includegraphics[width=0.4\textwidth]{agent_diagram.png}
    };
    \node[below=-1cm,font=\fontsize{5pt}{5pt}\selectfont] at (current page.south)  {Fuente \url{mathworks.com}};
  \end{tikzpicture}


## Videos de ejemplo
  \begin{tikzpicture}[remember picture, overlay]
    \node[above=2.0cm, left=3.0cm] at (current page.north) 
    {
        \includegraphics[width=0.4\textwidth]{pole_capture.png}
    };
    \node[below=-1cm,font=\fontsize{5pt}{5pt}\selectfont] at (current page.north)  {\url{https://youtu.be/5Q14EjnOJZc?t=9}};
  \end{tikzpicture}

  \begin{tikzpicture}[remember picture, overlay]
    \node[above=0.0cm] at (current page.center) 
    {
        \includegraphics[width=0.4\textwidth]{obj_detection.png}
    };
    \node[below=2cm,font=\fontsize{5pt}{5pt}\selectfont] at (current page.center)  {\url{https://youtu.be/O3b8lVF93jU?t=427}};
  \end{tikzpicture}

  \begin{tikzpicture}[remember picture, overlay]
    \node[above=1.0cm] at (current page.south) 
    {
        \includegraphics[width=0.4\textwidth]{image_segmentation.png}
    };
    \node[below=-1cm,font=\fontsize{5pt}{5pt}\selectfont] at (current page.south)  {\url{https://youtu.be/W-oVad7x-HQ?t=1078}};
  \end{tikzpicture}




## Contexto del Curso

Dentro del curso nos enfocaremos en el primero de los aprendizajes, es decir el aprendizaje supervisado.

# El problema del Aprendizaje Supervisado 

- Dada una serie de observaciones $X$ e $y$, se desea encontrar la función $f$ que relacione a $X$ con la respuesta $y$ 
- Esta función $f$ es desconocida e imposible de encontrar ... no tenemos *todos* los datos
- **Enfoque práctico**: Aproximarla mediante otra función $g$
- Este proceso de intentar alcanzar la mejor aproximación de $f$ se denomina **aprendizaje** 


## Proceso de aprendizaje

- El aprendizaje opera mediante ejemplos a través de un profesor
- El Sistema bajo estudio es observado en término de *entradas* y *salidas* $(\mathbf{x}_i,y_i)$
- Los valores de entrada al sistema $x_i$ son ingresadas a una versión artificial del Sistema que produce salidas $\hat{f}(\mathbf{x}_i)$ en respuesta

---

- Este sistema artificial puede modificar la asociación $\hat{f}$ entre la **entrada** y la **salida** en respuesta a las diferencias $y_i-\hat{f}(\mathbf{x}_i)$
- Este proceso de aprendizaje converge hacia una salida del sistema artificial *suficientemente cercana* (útil) para todas las posibles entradas que probablemente se encontraran en la practica  

---
### Ejemplos de aproximaciones

- Modelo lineal: $\hat{f}(\mathbf{x})=g_{\beta}(\mathbf{x})=\mathbf{x}^T\beta$
- Modelo con expansión de bases lineales: 
  $\hat{f}(\mathbf{x})=g_{\theta}(\mathbf{x})=\sum_{k=1}^Kh_k(\mathbf{x})\theta_k$
  - donde $h_k(\mathbf{x})$ puede ser expansiones polinomiales como $\{x_{1}^2, x_{1}x_{2}^2\}$ o trigonométricas $\{cos(x_1), x2\}$ si consideramos solo dos atributos por observación

Para el primer caso, es posible usar mínimos cuadrados para estimar los parámetros $\beta$ minimizando la suma residual de cuadrados: 
$$RSS(\beta)=\sum_{i=1}^N(y_i-f_{\beta}(\mathbf{x}_i))^2$$

## Medición de la calidad del Modelo

- El desempeño de un modelo ya entrenado se mide sobre un conjunto de datos no visto en la etapa de ajuste
- Este conjunto tiene observaciones representadas con los mismos atributos usados en la etapa de construcción del Modelo
- Se cuantifica mediante la calidad de la aproximación de las predicciones
  - E.g. Accuracy para clasificación
  - E.g. MSE para la tarea de regresión


## Algunos ejemplos

- Predecir si un paciente hospitalizado por un accidente cardiaco, tendrá otra ataque. 
- Identificar el borde de una imagen
- Identificar si un mensaje de correo es SPAM o no
- Identificar si un relato fue generado por una persona con ún trastorno mental

## El subproblema de Clasificación

- Si todos los $y_i\in \{1,...,C\}$ donde $C$ es el número de categorías de objetos
- Cuando $C=2$ el problema se denomina de clasificación binaria
- Valores $C>2$ determinan el problema como de clasificación multiclase
- Independiente de qué caso tratemos, el **objetivo** es realizar predicciones sobre **nuevas** observaciones de las cuales no tenemos la respuesta del Sistema
