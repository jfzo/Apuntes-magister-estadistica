---
title: MSC-011
topic: Fundamentos de Ciencia de Datos
author: Juan Zamora O.
date: Noviembre, 2023.
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
