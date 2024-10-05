---
title: EST-850
subtitle: Modelación Estadística de Aplicaciones Multidisciplinarias
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
toc-title: Estructura
bibliography: referencias.bib
natbib: true
natbiboptions: square,numbers
section-titles: false
---

# Minería de Opiniones

- *Análisis de Sentimiento* busca determinar la polaridad de las opiniones de usuarios (pos,neg o neutra)  acerca de un determinado asunto.
- *Clasificación de sentimiento* se refiere al conjunto de métodos que permiten determinar si una oración o documento encierra una polaridad positiva, negativa o neutra.
\note{Aplicaciones reales en que la identificacion automatica de sentimiento sea de utilidad}
- Utilidad en diversos dominios masivos.
- Servicios [@salinca2015business], Turísmo [@grabner2012classification], Educación [@sangeetha2021sentiment] ...
- Tendencias en algunas acciones en mercados financieros [@li2014news]


## Carga emotiva en texto

\note{Ejemplos textuales que denotan este fenómeno}

```...awesome caramel sauce and sweet toasty almonds. I love this place! ```

```...awful pizza and ridiculously overpriced...```

¿Qué rasgos de estos textos permiten identificar su polaridad?



## Palabras positivas y negativas

- A menudo usamos palabras para describir como nos sentimos respecto de *algo* \itemsep=1em
- Las personas asocian determinadas connotaciones y significados a las palabras \itemsep=1em
- Algunas son evidentes
    - Amor, amistad, sí... transmiten sentimientos **positivos**.
    - Odio, malo, no ... transmiten sentimientos **negativos**.
- Otras no tanto
    - Quizás, indiferente ...
     
---

- SA basado en lexicons emplea palabras y frases recolectadas y graduadas según polaridad.
- La polaridad de las palabras en el texto es evaluada según el Lexicon para determinar la orientación del texto.


## Lexicons generados manualmente

- Existen vocabularios anotados (Lexicon) que permiten identificar la polaridad de cada palabra 

- Opinion Lexicon: [www.cs.uic.edu/~liub/FBS/sentiment-analysis.html](https://www.cs.uic.edu/~liub/FBS/sentiment-analysis.html)
- Opinion Finder: [mpqa.cs.pitt.edu/opinionfinder/](https://mpqa.cs.pitt.edu/opinionfinder/)
- Linguistic Inquiry and Word Count (LIWC) [liwc.wpengine.com/](http://liwc.wpengine.com/)
- Valence Aware Dictionary and sEntiment Reasoner (VADER) [github.com/cjhutto/vaderSentiment](https://github.com/cjhutto/vaderSentiment)
- Avanzado: Ver [@hutto2014vader]

---

- ... también librerías que permiten  componer las polaridades individuales para generar una general por texto
    - **Poco para el castellano**

```No volvería, aunque fuera gratis.```
```python
>>> [{'neg': 0.196, 'neu': 0.804, 'pos': 0.0, 'compound': -0.296}
```

---

### Algoritmo aditivo simple de identificación de polaridad

**Estrategia**

- Usando vocabulario con palabras positivas ($+1$) y negativas ($+1$)
- Dado un texto $t$, contabilizar palabras Positivas (**P**) y Negativas (**N**)
- Definir el sentimiento del texto como: $$sent(t)= \frac{P-N}{P+N}$$

Este método permite identificar la tendencia dominante entre Positiva y Negativa.

---

### Extensión multiplicativa con modificadores

Anteriormente...

- Palabras contribuyen aditivamente a la puntuación de sentimiento
- Ausencia de contexto ...
    - Ejemplo: "not pretty" es radicalmente distinto a "pretty"
- Luego, una idea es incorporar el cambio en polaridad multiplicando la valencia de cada palabra por la de su modificadora
- *n-gramas*

---

**Modificadores**

- Se define el peso de cada modificador, es decir:
    - *not* $\Rightarrow -1.0$
    - *much* $\Rightarrow +1.3$    
    - *very* $\Rightarrow +1.5$
    - *pretty* $\Rightarrow +1.5$
    - *somewhat* $\Rightarrow +1.2$
- Cada palabra encontrada es buscada primero en los modificadores.
- Si no está, se busca en las palabras con valencia (pos o neg).
- Si no es modificadora y tampoco tiene valencia, entonces es una señal de continuar con el sgte. n-grama.

## Lexicons generados automáticamente con Corpus

- Existen grandes volúmenes de textos con valoraciones generadas por miles de personas
    - Generalmente, estas valoraciones están en una escala (e.g. 1-5)

¿Es posible construir lexicons de manera automática?

- Sí, usando Machine Learning.
- Cada lexicon generado es aplicable al dominio de donde se generó
- ¡También tiene sesgos!


## Detección de emociones

- A menudo se asocia el análisis de sentimiento con el de emociones
- El reconocimiento de emociones a partir del texto consiste en identificar los sentimientos  (alegría, pena, rabia ...) plasmados en cada documento.
- Ver [@nandwani2021review] para más detalle.

# Procesamiento de texto para análisis de sentimiento

\note{Colocar ejemplo que vaya mostrando el resultado de cada etapa}

\begin{tikzpicture}[remember picture, overlay]
    \node[above=2.5cm] at (current page.south) 
    {
        \includegraphics[width=0.6\textwidth]{steps_sa.png}
    };
\end{tikzpicture}


\vspace{140pt}
Fuente [@nandwani2021review]



# Clasificación de sentimiento usando Machine Learning 

## Extracción de rasgos para la clasificación de sentimiento

- El enfoque más sencillo es *Bag of Words* (BoW)
    $$\vec{d}_{ij}=\mbox{freq}(d_i, j)$$
    
- Otra alternativa es *Tf-IDf*
    $$\vec{d}_{ij}=\frac{\mbox{freq}(d_i, j)}{\max\mbox{freq}(d_i, k)}\times \log \frac{N}{n_j}$$
    

## Selección características

- Es posible filtrar por frecuencia
- Criterios como $\chi^2$ o información mutua
    - Ver [@madasu2020efficient]

---

### Selección de términos usando $\chi^2$

- $\chi^2$ permite medir la relación entre variables
- Se usa para medir relación entre característica (palabra) y la etiqueta de clase (variable objetivo)
- Un valor igual a $0$  indica independencia, mientras que valores más altos representan mayor relación
- Se calcula para cada palabra, y contrasta la cantidad de ocurrencias en todos los documentos de cada clase **con** la proporción esperada de su ocurrencia en cada clase
$$\hat{\chi}^2(w_i)=\sum_{k=1}^C\frac{n_k}{N}\cdot \chi^2(w_i,c_k)$$


## Métodos usados

En general cualquier técnica vectorial:

- Naive Bayes (ejemplo)
- Support Vector Machines
- XGB

## Calidad de los resultados obtenidos

- Dado que la tarea es de clasificación, se usan las medidas tradicionales
    - Accuracy = $\frac{TP+TN}{TP+TN+FP+FN}$ \itemsep=1.2em
    - Precision = $\frac{TP}{TP+FP}$
    - Recall = $\frac{TP}{TP+FN}$
    - F1 = $\frac{2*\mbox{Precision}*\mbox{Recall}}{\mbox{Precision}+\mbox{Recall}} = \frac{2*TP}{2*TP+FP+FN}$

## Selección y Validación del Modelo

### Escenario con abundancia de datos

- División de los datos en 3 grupos

    |   |   |   |
    |---|---|---|
    | **Entrenamiento** | **Validación** | **Prueba** |
    |---|---|---|
    | Para ajustar los modelos | Estimar desempeño de cada modelo | Evaluación del modelo escogido

- Muchos/Pocos datos depende de la complejidad del modelo, razón señal a ruido de función generadora de los datos ...

## K-Fold cv

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

- Se ajusta el modelo con $K-1$ partes y se calcula el desempeño sobre la restante

---

- Sea $M_{\theta}$ un método de ML con vector de parámetros $\theta$
- Cada observación $i$ es mapeada a una partición mediante la función $$\pi : \{ 1\ldots N\}\longrightarrow\{1\ldots K\}$$
- Anotemos como $\hat{M}_{\theta}^{-k},\ k\in\{1\ldots K\},$ al método entrenado sin la $k$-ésima partición del conjunto de datos 
- Luego de los $K$ experimentos, el estimador de la desempeño $Q(\hat{M}_{\theta})$ es el promedio de los $K$ experimentos

---


#### Selección de Modelo usando k-fold cv


Si consideramos un conjunto de modelos $M_{\theta_1},M_{\theta_2},\ldots$ y sus estimaciones de desempeño 

El modelo seleccionado será aquel que corresponda al

$$\mathop{\arg \max}\limits_{\theta_i}\{Q(\hat{M}_{\theta_1}), Q(\hat{M}_{\theta_2}), \ldots\}$$


---

### Consideraciones generales

- Valor de $k$ generalmente está entre $5$ y $10$
- Algunos métodos pueden ser muy sensibles al tamaño del conjunto de entrenamiento, especialmente cuando hay pocos datos ($<100$)
- Usar información de la respuesta $Y$ antes de aplicar k-fold cv sobre los mismos datos es trampa
  - Se obtendrá una estimación optimista del error
  - Por ejemplo, seleccionar variables usando Información Mutua sobre todos los datos antes de aplicar CV.

# Conclusiones

- Análisis de sentimiento tiene múltiples aplicaciones en diversos dominios
- Existen métodos basados en lexicon, corpus y diccionarios (no abordado)
- Preprocesamiento del texto es clave
- Existe una cantidad considerable de colecciones con textos formales e informales
- Redes sociales es un *nicho* interesante, sobre todo si se consideran problemas como la detección de odio o sarcasmo
- Existe una brecha importante en el desarrollo de métodos para otros idiomas (castellano por ejemplo)


# Referencias {.allowframebreaks}