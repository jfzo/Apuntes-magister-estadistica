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
- Métodos de Kernel y SVM
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

# Clasificación y Similaridad

<!--
  pandoc -t beamer ./clase04.md -o clase04.pdf --katex --slide-level=2
 -->

Se tienen dos clases de objetos. 
$$
(x_1,y_1),\ldots , (x_m,y_m) \in \mathcal{X}\times \{\pm 1\} 
$$ 

El aprendizaje consiste en poder generalizar sobre objetos no vistos anteriormente. Para un nuevo objeto $x\in \mathcal{X}$, predecir su correspondiente $y\in \{\pm 1\}$.

---

En esta sesión, nos concentraremos en métodos que escogen $y$ tal que $(x,y)$ es *similar* a los ejemplos de entrenamiento.

- Necesitamos contar con una noción de similitud en $\mathcal{X}$.$.
- Denominemos a esta medida de similitud como $\mathbf{k}$,

$$
\begin{array}{cc}
  k:&\mathcal{X}\times \mathcal{X} \rightarrow \mathbb{R}\\
  & (x,x')\rightarrow \mathbf{k}(x,x')
\end{array}
$$

- No cualquier medida sirve. Debe cumplir ciertas propiedades.
  - Ej. Producto interno $<\mathbf{x},\mathbf{x'}>=\sum_{i=1}^N x_i\cdot x_i$

---

Este tipo de productos para medir similitud presentan algunos inconvenientes:

- Los patrones no necesariamente provienen de una espacio con producto interno
  - Entonces, necesitamos representar los patrones originales en algun espacio con producto interno $\mathcal{H}$.
  - Usamos entonces el mapeo

$$
\begin{array}{cc}
\Phi :& \mathcal{X}\rightarrow \mathcal{X}\\
 & x\rightarrow \mathbf{x}:=\Phi (x) 
\end{array}
$$

---

*Incrustar* los datos en $\mathcal{H}$ vía $\Phi$ tiene 3 beneficios:

1. Asegura la utilidad de la medición de similitud mediante el producto interno $k(x,x'):=\langle\mathbf{x},\mathbf{x'}\rangle=\langle \Phi(x),\Phi(x')\rangle$
2. Permite abordar el problema de clasificación de manera geométrica
3. Un eventual mapeo $\Phi$ no lineal permite cambiar la representación vectorial en una más adecuada para el problema
   
\begin{tikzpicture}[remember picture, overlay]
    
    \node[above=1.0cm] at (current page.south) 
    {
        \includegraphics[width=0.5\textwidth]{nonlinear5.png}
    };
    \node[below=-0.9cm,font=\fontsize{5pt}{5pt}\selectfont] at (current page.south)  
    {
      Fuente fuente XXX
    };
\end{tikzpicture}

---

**Ejemplos**


$$
\begin{array}{cc}
  \Phi:&\mathbb{R}^2\rightarrow \mathbb{R}^3\\
  & (x_1,x_2) \rightarrow (z_1,z_2,z_3) := (x_1^2,\sqrt{2}x_1x_2,x_2^2)
\end{array}
$$

Suponemos que la frontera de clasificación es una elipse en el espacio de entrada. La tarea del proceso de aprendizaje es estimar esta frontera basandose en los datos observados de ambas clases.

La elipse (2D) es transformada en un hiperplano (3D), reduciendo el problema a estimar el hiperplano separador usando los objetos/puntos mapeados.

\begin{tikzpicture}[remember picture, overlay]
  \node[above=1.5cm, left=2.0cm] at (current page.south) 
  {
      \includegraphics[width=0.2\textwidth]{ringnorm.png}
  };
  \node[above=0.5cm] at (current page.south) 
  {
      \includegraphics[width=0.2\textwidth]{ringnorm-F2.png}
  };
  \node[below=-0.5cm, left=-3.0cm,font=\fontsize{5pt}{5pt}\selectfont] at (current page.south)  {Fuente fuente \textit{Hastie et al., 2017}};
\end{tikzpicture}

---

### Un algoritmo simple de clasificación


Suponga que $\mathcal{X}\subset \mathbb{R}^n$ y las dos clases son separables linealmente.

$$
\begin{array}{ccc}
  \mathbf{c}_+=\frac{1}{m_+}\sum_{\{i|y_i=+1\}}\mathbf{x_i}& & \mathbf{c}_-=\frac{1}{m_-}\sum_{\{i|y_i=-1\}}\mathbf{x_i}\\
  \mathbf{c}=\frac{1}{2}(\mathbf{c}_+ + \mathbf{c}_-)&&
\end{array}
$$

- Suponemos además que ambas clases tienen observaciones ($\mathbf{c}_+,\mathbf{c}_->0$)


\begin{tikzpicture}[remember picture, overlay]
    
  \node[above=0.8cm] at (current page.south) 
  {
      \includegraphics[width=0.4\textwidth]{parzen_algo.png}
  };
  \node[below=-1cm,font=\fontsize{5pt}{5pt}\selectfont] at (current page.south)  {Fuente fuente XXX};
\end{tikzpicture}

---

Asignaremos el nuevo punto $\mathbf{x}$ a la clase cuya media esté  más cerca.

Formularemos esta tarea en términos del producto interno $\langle .,.\rangle$

Para obtener la clase, revisaremos si el **ángulo** entre el vector que conecta punto central $\mathbf{c}$ con $\mathbf{x}$ y aquel que conecta los centros de ambas clases es menor que $\pi/2$.

\begin{tikzpicture}[remember picture, overlay]
    
  \node[above=0.9cm] at (current page.south) 
  {
      \includegraphics[width=0.22\textwidth]{ampliacion_angulo.png}
  };
  \node[below=-1cm,font=\fontsize{5pt}{5pt}\selectfont] at (current page.south)  {Fuente fuente XXX};
\end{tikzpicture}

---

En terminos formales, lo anterior equivale a 

$$
\begin{array}{cc}
  y=&sgn(\langle (\mathbf{x}-\mathbf{c}), (\mathbf{c}_+-\mathbf{c}_-)\rangle) \\
  =& sgn(\langle (\mathbf{x}-\frac{1}{2}(\mathbf{c}_+ + \mathbf{c}_-)), (\mathbf{c}_+-\mathbf{c}_-)\rangle) \\
  =& sgn(\langle\mathbf{x}, \mathbf{c}_+\rangle-\langle\mathbf{x}, \mathbf{c}_-\rangle- \frac{1}{2}\left (\Vert\mathbf{c}_+\Vert^2- \Vert\mathbf{c}_-\Vert^2 \right )) \\
=& sgn(\langle\mathbf{x}, \mathbf{c}_+\rangle-\langle\mathbf{x}, \mathbf{c}_-\rangle + b)  
\end{array}
$$

Podemos reescribir la función de decisión anterior, sustituyendo $\mathbf{c}_+$ y $\mathbf{c}_-$

$$
\begin{array}{cc}
  y=&sgn\left ( \frac{1}{m_+}\sum_{\{i|y_i=+1\}}\langle \mathbf{x},\mathbf{x_i}\rangle - 
  \frac{1}{m_-}\sum_{\{i|y_i=-1\}}\langle \mathbf{x}, \mathbf{x_i} \rangle + b
  \right ) \\
  =&sgn\left ( \frac{1}{m_+}\sum_{\{i|y_i=+1\}} k(x,x_i) - 
  \frac{1}{m_-}\sum_{\{i|y_i=-1\}} k(x, x_i) + b
  \right )
\end{array}
$$

---

$$y = sgn\left ( \frac{1}{m_+}\sum_{\{i|y_i=+1\}} k(x,x_i) - 
  \frac{1}{m_-}\sum_{\{i|y_i=-1\}} k(x,x_i) + b
  \right )$$

Podemos también hacer lo mismo con el término $b$, es decir

$$
b=\frac{1}{2}\left (
  \frac{1}{m_-^2}\sum_{\{(i,j)|y_i=y_j=-1\}} k(x_i,x_j)  - 
  \frac{1}{m_+^2}\sum_{\{(i,j)|y_i=y_j=+1\}} k(x_i,x_i)
  \right )
$$

## Mapeando al espacio de características


- No todos los problemas son linealmente separables
- No siempre $\mathcal{X}$ es un espacio con producto interno

**Enfoque basado en funciones de Kernel**

- Escoger un mapeo a algún espacio de características que sí tenga estas propiedades

\begin{tikzpicture}[remember picture, overlay]
    
  \node[above=1.0cm] at (current page.south) 
  {
      \includegraphics[width=0.5\textwidth]{nonlinear5.png}
  };
  \node[below=-1cm,font=\fontsize{5pt}{5pt}\selectfont] at (current page.south)  {Fuente fuente XXX};
\end{tikzpicture}

---

### Condición de Mercer

Si una función $k(x,x')$ es simétrica, 

$$\forall (\mathbf{x},\mathbf{x'})\in \mathcal{X}^2, k(\mathbf{x},\mathbf{x'})=k(\mathbf{x'},\mathbf{x})$$

y positiva definida, es decir, para cualquier $n \in \mathbb{R},\ (\mathbf{x}_1,\mathbf{x}_2,\ldots , \mathbf{x}_n)\in \mathcal{X}^n$ y $(a_1,a_2,\ldots , a_n)\in \mathbb{R}^n$:

$$\sum^{n}_{i=1}\sum^{n}_{j=1}a_ia_j k(\mathbf{x}_i,\mathbf{x}_j)\geq 0$$


Existe entonces un mapeo $\Phi$ que satsiface 
$$k(x,x')=\Phi(\mathbf{x})^{\mathsf{T}}\Phi(\mathbf{x'})$$

---

Algunas funciones que satisfacen estas condiciones son:

- $k(x,x')=(\mathbf{x}^{\mathsf{T}}\mathbf{x'}+ 1)^d$ (kernel polinomial)
- $k(x,x')=\mbox{exp}\left (-\frac{(\mathbf{x}-\mathbf{x'})^2}{\sigma} \right )$ (kernel gaussiano o radio basal)

- Otros kernels operan sobre objetos como grafos, cadenas de caracteres etc. 
- Permiten entonces medir similitud mediante productos internos en un espacio de caracterísitcas mejor dotado que el espacio original de atributos

# Maquinas de Vectores Soporte

**Hiperplano separador**

- Función de clasificación de la forma $y(\mathbf{x})=sgn(\langle \mathbf{w},\mathbf{x}\rangle + b)$
- Cada hiperplano tiene ecuación $D(\mathbf{x})=\langle \mathbf{w},\mathbf{x}\rangle +b =c\ , \ -1<c<1$
- El hiperplano óptimo es aquel que tiene el mayor margen

\begin{tikzpicture}[remember picture, overlay]    
  \node[above=1.0cm] at (current page.south) 
  {
      \includegraphics[width=0.5\textwidth]{hyp-book.png}
  };
  \node[below=-1cm,font=\fontsize{5pt}{5pt}\selectfont] at (current page.south)  {Fuente fuente Schölkopf et al., 2002};
\end{tikzpicture}

## Clasificador con margen máximo

Aquel con solución 
$$\underset{\mathbf{w}, b}{\operatorname{min}}\frac{1}{2}\Vert\mathbf{w}\Vert^2=\underset{\mathbf{w}, b}{\operatorname{max}}\frac{2}{\Vert\mathbf{w}\Vert}$$
sujeta las restricciones

$$y_i (\langle \mathbf{w},\mathbf{x}_i\rangle + b)\geq 1,\ \mbox{para }i=1,\ldots , n$$

* Problema de programación cuadrática
* Si hay separabilidad lineal, entonces existe solución

---


El problema anterior es un problema clásico de optimización con restricciones y puede ser resuelto mediante Multiplicadores de Lagrange.

$$L(\mathbf{w},b,\alpha)=\frac{1}{2}\Vert\mathbf{w} \Vert^2 -\sum_{i=1}^n \alpha_i(y_i (\langle \mathbf{w},\mathbf{x}_i\rangle + b)-1) $$

Minimizar la expresión de la lámina anterior equivale a maximizar esta última con respecto a los $\alpha_i$

Aquellos puntos $x_i$ cuyo $\alpha_i\neq 0$ serán usados como soporte

---

### SVM de margen suave

- El hiperplano separador puede no existir (existencia de ruido, clases traslapadas, etc.)
- A la formulación anterior se le introducen unas variables de holgura $\epsilon_i$

  $$y_i (\langle \mathbf{w},\Phi(\mathbf{x}_i)\rangle + b)\geq 1-\epsilon_i$$
- Se minimiza
  $$\underset{\mathbf{w}, b,\epsilon_i}{\operatorname{min}}\frac{1}{2}\Vert\mathbf{w}\Vert^2+\mathsf{C}\sum_{i=1}^{n}\epsilon_i$$

- $\mathsf{C}>0$ permite controlar el balance entre la max del margen y la min del error de entrenamiento. Es *seteado* por el usuario.

## Resumen

- Representaciones de objetos son mapeadas a un nuevo espacio denominado espacio de características
- El producto interno es calculado en **ese** espacio a través de la función de Kernel
- La clasificación se realiza usando el hiperplano con margen máximo
- Ese hiperplano es determinado por los vectores soporte
- La formulación de margen suave permite relajar el error para encontrar una solución
- El parámetro $\mathsf{C}$ permite al usuario controlar e balance entre margen máximo y error de entrenamiento mínimo