---
title: 
- MSC-011
subtitle:
- Fundamentos de Ciencia de Datos
author:
- Juan Zamora O.
documentclass: beamer
date: Octubre 2023
fontsize: 11pt
innertheme: circles
urlcolor: blue
linkstyle: bold
aspectratio: 169
section-titles: false
toc: true
toc-title: Estructura de la Presentación
section-titles: false
header-includes: |  
    \usepackage{libertinus-otf}
	\usepackage{tikz}
    \usetikzlibrary{calc,tikzmark,arrows,shapes,backgrounds}
    \usetikzlibrary{fit, arrows.meta, shapes}        
    \usepackage[spanish]{babel} 
    \usepackage{url}
    \usefonttheme{professionalfonts}
    \usepackage{fontspec}
    \setmainfont[Path = ./Roboto/,BoldFont=Roboto-Bold.ttf,ItalicFont=Roboto-Italic.ttf]{Roboto-Regular.ttf}    
    \setsansfont[Path = ./Roboto/,BoldFont=Roboto-Bold.ttf,ItalicFont=Roboto-Italic.ttf]{Roboto-Regular.ttf}
    \usepackage{algorithm}
    \usepackage{algorithmicx}
    \useinnertheme{circles}
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

# Clustering basado en representantes

<!--
pandoc -t beamer clase01.md -o clase01.pdf --katex --slide-level=2 --dpi=300 --toc --citeproc  --listings --shift-heading-level=0 --pdf-engine=lualatex
 -->
 
- Dado un conjunto de datos con $n$ puntos en un espacio $d$-dimensional, $\mathcal{D}=\{\mathbf{x}_j\}_{j=1}^{n}$
- Dado también $k\in\mathbb{Z}$ , el número de grupos a encontrar en $\mathcal{D}$

- El **objetivo** de la tarea es particionar $\mathcal{D}$ en $k$ grupos o *clusters*, representados como $\mathcal{C}=\{C_1,C_2,\ldots , C_k\}$ 

- Luego, para cada cluster $C_i$ existe un punto representativo $\mu_i$ 
    - Comúnmente se le denomina centroide y corresponde a $$\mu_i=\frac{1}{|C_i|}\sum_{\mathbf{x}_j\in C_i}\mathbf{x}_j$$
    

## Método de Fuerza bruta 

Una posible solución a este problema consiste en 

1. Generar todos las posibles particiones de $n$ puntos en $k$ grupos, $\binom{n}{k}$
2. Para cada una, evaluar alguna puntuación que favorezca *ciertas propiedades*
    - Podría usarse $$SSE(\mathcal{C})=\sum_{i=1}^k\sum_{\mathbf{x}_j\in C_i} \lVert \mathbf{x}_j -\mu_i \rVert^2$$
3. Reportar aquella partición con la mejor puntuación, es decir 
$$\mathcal{C}^{*}=\mathop{\arg \min}\limits_{\mathcal{C}}SSE(\mathcal{C}) $$

**Problema** $\mathcal{O}(k^n/k!)$ posibles soluciones ... 

## Algoritmo K-Means

- K-Means utiliza una estrategia *Greedy* e iterativa para encontrar $\mathcal{C}^{*}$
    1. Inicializa los centroides al azar, generando $k$ puntos en $\mathbb{R}^d$
    2. Comienza a iterar y en cada iteración realiza dos pasos: Asignación a un grupo y actualización de centroides
    1. Cada punto es asignado al grupo asociado al centroide más cercano.
    2. Se actualizan los centroides, calculando nuevamente las medias sobre los puntos asignados en el paso anterior.
    3. Al alcanzarse una cierta cantidad de iteraciones, no haber cambios en las asignaciones o bien, no encontrarse cambios significativos, el método termina.


---


\begin{tikzpicture}[remember picture, overlay]
    \node[above=1.5cm] at (current page.south) 
    {
        \includegraphics[width=0.7\textwidth]{kmeans_alg.png}
    };
\end{tikzpicture}

# Kernel K-Means

## Funciones de Kernel

14.2

14.2.1

14.2.3

14.4

14.4.2


## Algoritmo Kernel K-Means

- K-means realiza una separación en el espacio original de características de los datos
- El uso del *Kernel Trick* puede ayudar a construir grupos usando transformaciones no-lineales de este espacio

---

- Se mapea cada $\mathbf{x_j}\in\mathcal{C}$ mediante $\phi(\mathbf{x_j})$
- Una función de kernel $\mathbf{K}$ es aplicada sobre cada par de puntos, $\mathbf{K}(\mathbf{x_i}, \mathbf{x_j})=\phi(\mathbf{x_i})^T\phi(\mathbf{x_j})$
- Se aplica K-Means en este nuevo espacio 
- La nueva función objetivo en el espacio de características es:
$$\mathop{\min}\limits_{\mathcal{C}}SSE(\mathcal{C})= \sum_{i=1}^k\sum_{\mathbf{x}_j\in C_i}\lVert \mathbf{x}_j -\mu^{\phi}_i \rVert^2$$

$$\mathop{\min}\limits_{\mathcal{C}}SSE(\mathcal{C})= \sum_{j=1}^{n}\mathbf{K}(\mathbf{x}_j,\mathbf{x}_j)-\sum_{i=1}^k\frac{1}{|C_i|}\sum_{\mathbf{x}_p\in C_i}\sum_{\mathbf{x}_q\in C_i}\mathbf{K}(\mathbf{x}_p,\mathbf{x}_q)$$


---


\begin{tikzpicture}[remember picture, overlay]
    \node[above=0.5cm] at (current page.south) 
    {
        \includegraphics[width=0.7\textwidth]{kernelkmeans_alg.png}
    };
\end{tikzpicture}
    
<!--  
- *Análisis de Sentimiento* busca determinar la polaridad de las opiniones de usuarios (pos,neg o neutra)  acerca de un determinado asunto.

- *Clasificación de sentimiento* se refiere al conjunto de métodos que permiten determinar si una oración o documento encierra una polaridad positiva, negativa o neutra.

\note{Aplicaciones reales en que la identificacion automatica de sentimiento sea de utilidad}
* Utilidad en diversos dominios masivos.
- Servicios [@salinca2015business], Turísmo [@grabner2012classification], Educación [@sangeetha2021sentiment] ...
- Tendencias en algunas acciones en mercados financieros [@li2014news]


\begin{tikzpicture}[remember picture, overlay]
    \node[above=1.5cm] at (current page.south) 
    {
        \includegraphics[width=0.9\textwidth]{data-mining-Venn-diagram.png}
    };
    \node[below=-1cm,font=\fontsize{5pt}{5pt}\selectfont] at (current page.south)  {Fuente \url{wikipedia.org}};
\end{tikzpicture}
-->

