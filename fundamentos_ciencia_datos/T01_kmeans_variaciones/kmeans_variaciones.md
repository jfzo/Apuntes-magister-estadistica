---
title: MSC-011
topic: Fundamentos de Ciencia de Datos
author: Juan Zamora O.
date: Octubre, 2023.
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



# Algoritmo Kernel K-Means

- K-means realiza una separación en el espacio original de características de los datos
- El uso del *Kernel Trick* puede ayudar a construir grupos usando transformaciones no-lineales de este espacio

---

- Se mapea cada $\mathbf{x_j}\in\mathcal{C}$ mediante $\phi(\mathbf{x_j})$
- Una función de kernel $\mathbf{K}$ es aplicada sobre cada par de puntos, $\mathbf{K}(\mathbf{x_i}, \mathbf{x_j})=\phi(\mathbf{x_i})^T\phi(\mathbf{x_j})$
- Se aplica K-Means en este nuevo espacio 
- La nueva función objetivo en el espacio de características es:
$$\mathop{\min}\limits_{\mathcal{C}}SSE(\mathcal{C})= \sum_{i=1}^k\sum_{\mathbf{x}_j\in C_i}\lVert \phi(\mathbf{x}_j) -\mu^{\phi}_i \rVert^2$$

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

# Clustering Spectral

## Vista general del método

1. Pre-procesamiento: Construir una representación de grafo (matriz)
2. Descomposición: 
    - Calcular los valores y vectores propios de la matriz
    - Mapear cada punto en $\mathcal{D}$ a una representación vectorial basado en uno o más vectores propios
3. Agrupar
    - Asignar todos los puntos a 2 o más grupos, usando la nueva representación vectorial
    
## Particionamiento espectral de un grafo

- Dado un grafo $G=(V,E)$, con $V=\{1,2,\ldots , n\}$ y $E:V\times V \rightarrow \{0,1\}$
- $A$: Matriz de adyacencia de un grafo no dirigido que codifica los vecindarios de cada nodo en $G$
    - $A_{ij}=1$ cuando existe conexión entre instancias $i$ y $j$. $0$ en otro caso.
    - Simétrica
    - Tiene $n$ valores propios
    - Vectores propios reales y ortogonales 
- $D$: Matriz de grados
    - $D=[d_{ii}]$, donde $d_{ii}$ es el grado del nodo $i$
    - Es diagonal
  
    

## Laplaciano

- $L = D-A$: Matriz Laplaciano
- Todos sus valores propios son $\geq 0$
- $xLx=\sum_{ij}L_{ij}x_ix_j \geq 0$ para todo $x$
- Multiplicidad del primer valor propio es igual al número de componentes conectados
- Si vértices $i$ y $j$ están conectados en el grafo, en algún vector propio asociado al primer valor propio las conmponentes $i$ y $j$ serán $1$

## Clustering

- El segundo valor propio es clave
- El vector propio de este segundo valor será usado para encontrar los grupos
- **Obj.** Minimizar la cantidad de arcos de una partición a otra.
- Este vector es real, no tiene etiquetas $\{-1,+1\}$
    - Puede usarse la función signo

\begin{tikzpicture}[remember picture, overlay]
    \node[above=0.1cm, xshift=3.7cm] at (current page.south) 
    {
        \includegraphics[width=0.45\textwidth]{spectral_example.png}
    };
    \end{tikzpicture}

---

**¿Cómo generar más de 2 clusters?**

- Tomar los $k$ vectores propios asociados a los valores propios más pequeños
- Esta matriz de $n\times k$ es entregada a otro  método (e.g. K-Means)


## Ejemplo

::: columns

:::: {.column width=60%}

\begin{tikzpicture}[remember picture, overlay]
    \node[above=-0.9cm, xshift=-4.7cm] at (current page.south) 
    {
        \includegraphics[width=2.1\textwidth]{toy_graph.png}
    };
\end{tikzpicture}

::::

:::: {.column width=40%}


- **Adyacencia**

$\begin{bmatrix} 0 & 1 & 1 & 1 & 0 & 0 \\ 1 & 0 & 1 & 0 & 0 & 0 \\ 1 & 1 & 0 & 0 & 1 & 0 \\ 1 & 0 & 0 & 0 & 1 & 1 \\ 0 & 0 & 1 & 1 & 0 & 1 \\ 0 & 0 & 0 & 1 & 1 & 0 \end{bmatrix}$

\vspace{10pt}

- **Grado**

$\begin{bmatrix} 3 & 0 & 0 & 0 & 0 & 0 \\ 0 & 2 & 0 & 0 & 0 & 0 \\ 0 & 0 & 3 & 0 & 0 & 0 \\ 0 & 0 & 0 & 3 & 0 & 0 \\ 0 & 0 & 0 & 0 & 3 & 0 \\ 0 & 0 & 0 & 0 & 0 & 2 \end{bmatrix}$


::::

:::

## Las otras matrices ...

::: columns

:::: {.column width=40%}

* $L = D - A$

\vspace{10pt}

- **Laplaciano**

$\begin{bmatrix} 3 & -1 & -1 & -1 & 0 & 0 \\ -1 & 2 & -1 & 0 & 0 & 0 \\ -1 & -1 & 3 & 0 & -1 & 0 \\ -1 & 0 & 0 & 3 & -1 & -1 \\ 0 & 0 & -1 & -1 & 3 & -1 \\ 0 & 0 & 0 & -1 & -1 & 2 \end{bmatrix}$

::::

:::: {.column width=60%}

- **Valores propios**

$\begin{bmatrix} 0 & 0 & 0 & 0 & 0 & 0 \\ 0 & 1 & 0 & 0 & 0 & 0 \\ 0 & 0 & 3 & 0 & 0 & 0 \\ 0 & 0 & 0 & 3 & 0 & 0 \\ 0 & 0 & 0 & 0 & 4 & 0 \\ 0 & 0 & 0 & 0 & 0 & 5 \end{bmatrix}$

\vspace{10pt}

- **Vectores propios**

$\begin{bmatrix} -0.408 & 0.289 & 0 & -0.577 & -0.408 & 0.5 \\ -0.408 & 0.577 & 0.5 & 0.289 & 0.408 & 0 \\ -0.408 & 0.289 & -0.5 & 0.289 & -0.408 & -0.5 \\ -0.408 & -0.289 & 0 & -0.577 & 0.408 & -0.5 \\ -0.408 & -0.289 & -0.5 & 0.289 & 0.408 & 0.5 \\ -0.408 & -0.577 & 0.5 & 0.289 & -0.408 & 0 \end{bmatrix}$


::::

:::

## Datos proyectados sobre los vectores propios

::: columns

:::: {.column width=40%}


\begin{equation*}
    \left(\begin{BMAT}{cccccc}{cccccc}
    -0.408 & 0.289 & 0 & -0.577 & -0.408 & 0.5 \\ 
    -0.408 & 0.577 & 0.5 & 0.289 & 0.408 & 0 \\ 
    -0.408 & 0.289 & -0.5 & 0.289 & -0.408 & -0.5 \\ 
    -0.408 & -0.289 & 0 & -0.577 & 0.408 & -0.5 \\ 
    -0.408 & -0.289 & -0.5 & 0.289 & 0.408 & 0.5 \\ 
    -0.408 & -0.577 & 0.5 & 0.289 & -0.408 & 0
    \addpath{(0,0,0)rrddddddlluuuuuurr}
    \end{BMAT}\right)
\end{equation*}


::::

:::: {.column width=60%}



\begin{tikzpicture}[remember picture, overlay]
\node[yshift=5cm, xshift=5cm] at (current page.south) 
{
    \includegraphics[width=0.7\textwidth]{data_projected.png}
};
\end{tikzpicture}
    
::::

:::


---

\begin{equation*}
    \left(\begin{BMAT}{cccccc}{cccccc}
    -0.408 & 0.289 & 0 & -0.577 & -0.408 & 0.5 \\ 
    -0.408 & 0.577 & 0.5 & 0.289 & 0.408 & 0 \\ 
    -0.408 & 0.289 & -0.5 & 0.289 & -0.408 & -0.5 \\ 
    -0.408 & -0.289 & 0 & -0.577 & 0.408 & -0.5 \\ 
    -0.408 & -0.289 & -0.5 & 0.289 & 0.408 & 0.5 \\ 
    -0.408 & -0.577 & 0.5 & 0.289 & -0.408 & 0
    \addpath{(0,0,0)rrrddddddllluuuuuurrr}
    \end{BMAT}\right)
\end{equation*}
