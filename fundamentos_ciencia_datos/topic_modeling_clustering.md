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

El objetivo de esta parte del Curso es introducir Topic Models para encontrar grupos de palabras que permitan caracterizar a un conjunto de documentos.

Referencias: [Blei et al. 2003](http://www.jmlr.org/papers/volume3/blei03a/blei03a.pdf)

## Idea fundamental

* Documentos son mezclas de tópicos

## Que es un tópico?

* Distribución de probabilidad sobre la ocurrencia de palabras

## Topic Models

* Modelo *generativo* para documentos
* Documento en blanco con una cierta distribución de tópicos.
* Se escoge un tópico al azar a partir de la distribución.
* Se escoge al azar una palabra a partir de este tópico (recordemos la definición anterior de *tópico*)

\begin{tikzpicture}[remember picture, overlay]
\node[yshift=2.0cm, xshift=0cm] at (current page.south)
{
    \includegraphics[width=0.5\textwidth]{tm_model.png}
};
\end{tikzpicture}

---

\begin{tikzpicture}[remember picture, overlay]
\node[yshift=2.0cm, xshift=0cm] at (current page.south)
{
    \includegraphics[width=0.5\textwidth]{tm_equation_annotated_figures.png}
};
\end{tikzpicture}

## ¿De qué sirve esta perspectiva generadora de documentos?

* Existen técnicas estadísticas y computacionales para invertir este procedimiento a partir de documentos existentes (...nuestros documentos), pudiendo así inferir la composición *más probable* de los tópicos que permitieron generar esta colección de documentos.

En esta sección del curso revisaremos `Latent-Dirichlet Allocation`.

## Dirichlet distribution for documents in topics
