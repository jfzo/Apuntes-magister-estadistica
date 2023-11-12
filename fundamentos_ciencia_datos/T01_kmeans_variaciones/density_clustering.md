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
    \usepackage{easybmat}
	\usepackage{tikz}
    \usetikzlibrary{matrix,calc,tikzmark,arrows,shapes,backgrounds}
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

# Revisitando técnicas basadas en representantes

**Supuesto** bastante usado

- Grupos/Clusters generados a partir de una distribución o mezcla de distribuciones simétricas (e.g. Normal)
- Expectation Maximization, K-Means y extensiones por mencionar algunos


Enfoque basado en densidad no supone forma específica.

- Útil por ejemplo en datos geo-espaciales.

---

\begin{tikzpicture}[remember picture, overlay]
\node[yshift=0cm, xshift=-4cm] at (current page.center) 
{
    \includegraphics[width=0.4\textwidth]{kmeans_fails_rolls.png}
};
\end{tikzpicture}


\begin{tikzpicture}[remember picture, overlay]
\node[yshift=0cm, xshift=4cm] at (current page.center) 
{
    \includegraphics[width=0.4\textwidth]{kmeans_voronoi.jpeg}
};
\end{tikzpicture}

--- 

- Minimización de la distancia al cuadrado entre los puntos y sus respectivos centroides produce a un particionamiento tipo polígono de Voronoi.
 Esto no solo ocurren en 2D
- **Urge** contar con mecanismos de descubrimiento de grupos 
    - con forma arbitraria.
    - identificando ruido
    - que no requieran de $k$
    
    
## Clustering basado en densidad    

- *Grupos basados en densidad* se definen como areas densas y conectadas, *separadas* entre sí por áreas de  menor densidad.
- El ruído se define como áreas con densidad menor que la de los clusters
- Noción de *Localidad* asociada a la definición de cluster
    - Posibilita encontrar regiones densas con forma arbitraria
    
\begin{tikzpicture}[remember picture, overlay]
\node[yshift=2.0cm, xshift=5cm] at (current page.south) 
{
    \includegraphics[width=0.25\textwidth]{density_clusters_example.png}
};
\end{tikzpicture}    


# DBSCAN Clustering

- Cuenta la cantidad de puntos en vecindarios de radio fijo ($\epsilon$) $$N_{\epsilon}(p)=\{q\in \mathbf{D} | dist(p,q)\leq \epsilon\}$$
- Considera dos puntos conectados cuando son vecinos recíprocos
- Un *core-point* es aquel cuyo vecindario contiene *al menos* *MinPts* puntos
    - Es decir, punto cuya densidad excede un determinado umbral.
- Un punto $q$ es alcanzable de manera directa (*directly-density-reachable*) por un *core-point* $p$ si se encuentra en su vecindario, $$|N_{\epsilon}(p)|\geq MinPts \ y \ q\in N_{\epsilon}(p)$$

---

- Alcance (*density-reachable*($\mathsf{R}$)) queda dado por la clausura transitiva de la relación *directly-density-reachable*($\mathsf{DR}$) $$q\mathsf{R}p\exists p_1,\ldots,p_m\ \mbox{con}\ p_1=p\ y \ p_m=q \ \ t.q.\ \  p_{i+1}\mathsf{DR}p_i$$
- Dos puntos $p$ y $q$ están conectados por densidad (*density-connected*) si existe otro $r$ a partir del cual ambos son *density-reachable*
- Un **cluster** es entonces un conjunto de puntos conectados por densidad (*density-connected*($\mathsf{C}$))
    - maximal respecto de *density-reachability* $$q\mathsf{C}p, \exists r\ \  t.q.\ \ r\mathsf{R}p\ \land r\mathsf{R}q$$
- Ruido se define como aquel conjunto de puntos que no pertenecen a ningún cluster 

\begin{tikzpicture}[remember picture, overlay]
\node[yshift=3.5cm, xshift=6cm] at (current page.south) 
{
    \includegraphics[width=0.3\textwidth]{transitive_closure_relation.png}
};
\end{tikzpicture}    

# OPTICS Clustering

- Dificil caracterizar estructura intrinseca de grupos mediante parámetros globales de densidad
- Pueden existir grupos de diversa densidad en distintas regiones del espacio
- *Idea base*: Grupos de mayor densidad están contenidos en grupos con menor densidad
- Se construyen *simultaneamente* grupos con diferentes densidades para un valor fijo de *MinPts*

## Conceptos relevantes

OPTICS introduce dos conceptos:

1. *Core-distance*: Valor $\epsilon$ más pequeño para un punto $p$ que lo convierte en *core-point*.
2. *reachability-distance*: Distancia más pequeña entre un par de puntos $p$ y $q$ que los hace directamente alcanzables

Además usa un gráfico (*reachability  plot*) que muestra la densidad y conectividad de los puntos. **Útil** para distinguir clusters

\begin{tikzpicture}[remember picture, overlay]
\node[yshift=1.5cm, xshift=4cm] at (current page.south) 
{
    \includegraphics[width=0.4\textwidth]{reachability_plot.jpeg}
};
\end{tikzpicture}   