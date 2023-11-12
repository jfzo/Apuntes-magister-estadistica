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

# Aproximaciones Low-Rank para Clustering

Una matriz $X$ de rango $r$ admite una factorización de la forma $$X=BC^T, \ B\in\mathbf{R}^{m\times r}, \ C\in\mathbf{R}^{n\times r}$$


$X$ es aproximada con bajo rango (low-rank) cuando $rango(X) << \min(m,n)$

\begin{tikzpicture}[remember picture, overlay]
\node[yshift=1.5cm, xshift=0cm] at (current page.south) 
{
    \includegraphics[width=0.3\textwidth]{nmf_view.png}
};
\end{tikzpicture}    

# (NMF) Factorización de matrices no-negativas

- Grupo de algoritmos de de análisis multivariado y algebra lineal donde una matriz $X$ es factorizada en dos matrices $W$ y $H$
- Cada columna de $X$ es aproximada por una combinación lineal no-negativa de las columnas de $W$, donde los coeficientes de mezcla corresponden a las columnas de $H$ 
- Las tres matrices tienen elementos no-negativos
- Usado en sistemas recomendadores, procesamiento de audio, agrupamiento de texto.

# NMF

- Dada  una matriz no-negativa $X\in \mathbf{R}^{m\times n}$ y un $k\in\mathbf{Z}<< \min(m,n)$
- Encuentra matrices no-negativas $W\in \mathbf{R}^{m\times k}$ y $H\in \mathbf{R}^{k\times n}$ tales que minimizan $$\lVert X-WH \rVert^{2}_{F}=\sum_i\sum_j(X_{ij}-[WH]_{ij})^2$$

* $W$: base para un espacio $k$-dimensional, la $i$-ésima columna de H: corresponde a representación k-dim de $i$-ésima columna de $X$

# Aplicación de NMF para extracción de tópicos en texto

- Se construye matriz de terminos vs documentos
- Se aplica NMF para obtener $W$ y $H$


\begin{tikzpicture}[remember picture, overlay]
\node[yshift=2.0cm, xshift=0cm] at (current page.south) 
{
    \includegraphics[width=0.5\textwidth]{nmf_ex_topics.png}
};
\end{tikzpicture}    