---
title: Clasificador Naive-Bayes
topic: EST852 -- Machine Learning
author: Juan Zamora O.
date: 
fonttheme: "professionalfonts"
fontsize: 11pt
theme: default
innertheme: circles
urlcolor: blue
linkstyle: bold
aspectratio: 169
titlegraphic: logosAzul.png
logo: logoAzul.png
toc: true
toc-title: Estructura de la Presentación
section-titles: false
---

# Introducción

<!--
  make clase02.pdf
 -->

- Los métodos bayesianos combinan conocimiento previo (probabilidades apriori) con datos observados
- Posibilitan la creación de algoritmos de aprendizaje:
  - Aprendizaje bayesiano ingenuo
  - Aprendizaje de redes bayesianas (belief networks)
- Proveen de un marco conceptual muy útil

# Teorema de Bayes

$$P(h|D)=\frac{P(D|h)P(h)}{P(D)}$$

- $P(h)$: probabilidad apriori 
de hipotesis $h$
- $P(D)$: probabilidad apriori de datos de entrenamiento $D$
- $P(h|D)$: probabilidad de que se cumpla $h$ cuando se  observa $D$
- $P(D|h)$: probabilidad de observar $D$ cuando se cumple $h$

## Elección de una hipotesis


$$P(h|D)=\frac{P(D|h)P(h)}{P(D)}$$

**En general**, se desea encontrar la hipotesis más probable luego de observar los datos de entrenamiento.

- Hipotesis máxima a posteriori ($h_{MAP}$):  
$$h_{MAP}=\underset{h\in H}{\operatorname{argmax}} P(h|D)$$

---

### Hipotesis máxima a posteriori

$$h_{MAP}=\underset{h\in H}{\operatorname{argmax}} P(h|D)$$

$$= \underset{h\in H}{\operatorname{argmax}} \frac{P(D|h)P(h)}{P(D)}$$
$$= \underset{h\in H}{\operatorname{argmax}} P(D|h)P(h)$$
- *Nota*: Si se asume que $P(h_i)=P(h_j), \forall h_i, h_j\in H$, entonces 
$$h_{ML}=\underset{h_i\in H}{\operatorname{argmax}} P(D|h_i)$$


## Ejemplo

\only<1,2>{Un paciente se somete un examen de cáncer y el resultado es positivo. Este test entrega positivo de manera correcta en solo el $98\%$ de los casos en la enfermedad está realmente presente, y un negativo correcto en solo el $97\%$ de los casos en que la enfermedad \textbf{no} está presente.
Adicionalmente, el $0.8\%$ de toda la población tiene esta enfermedad. }

\only<1>{
$$
\begin{array}{cc} 
P(\mbox{cancer})= & P(\neg\mbox{cancer})=\\
P(\oplus|\mbox{cancer})= & P(\ominus|\mbox{cancer})=\\
P(\oplus|\neg\mbox{cancer})= & P(\ominus|\neg\mbox{cancer})=
\end{array}
$$ 
}


\only<2>{
$$
\begin{array}{cc} 
P(\mbox{cancer})= .008& P(\neg\mbox{cancer})= .992\\
P(\oplus|\mbox{cancer})=.98 & P(\ominus|\mbox{cancer})=.02\\
P(\oplus|\neg\mbox{cancer})= .03& P(\ominus|\neg\mbox{cancer})= .97
\end{array}
$$ 
}

---


Suponga que se observa un nuevo paciente para quien el test indicó un resultado positivo. ¿Deberíamos diagnosticar al paciente como con cancer o no?

Para responder debemos encontrar la hipotesis máxima aposteriori, es decir:

$$P(\mbox{cancer}|\oplus)$$
$$P(\neg\mbox{cancer}|\oplus)$$

---

$$
\begin{array}{c}
P(\mbox{cancer}|\oplus)=\frac{P(\oplus|\mbox{cancer})P(\mbox{cancer})}{P(\oplus)}\\
P(\neg\mbox{cancer}|\oplus)=\frac{P(\oplus|\neg\mbox{cancer})P(\neg\mbox{cancer})}{P(\oplus)}
\end{array}
$$

Podemos ignorar $P(\oplus)$, ya que no afectará la conclusión.
Entonces,

$$
\begin{array}{c}
P(\mbox{cancer}|\oplus)\simeq P(\oplus|\mbox{cancer})P(\mbox{cancer})\\
P(\neg\mbox{cancer}|\oplus)\simeq P(\oplus|\neg\mbox{cancer})P(\neg\mbox{cancer})
\end{array}
$$


---

Usando las cantidades calculadas anteriormente:

$$P(\oplus|\mbox{cancer})P(\mbox{cancer})=(0.98)0.008=0.0078$$

$$P(\oplus|\neg\mbox{cancer})P(\neg\mbox{cancer})=(0.03)0.992=0.0298$$

Aún cuando es posible calcular $P(\oplus)$ para un cálculo exacto, los valores anteriores nos indican que es muy poco probable (aún con un positivo) tener la enfermedad.

Por lo tanto, $h_{MAP}=\neg\mbox{cancer}$ .


<!--

## Aprendizaje de hipotesis MAP por fuerza bruta

- Para cada hipotesis $h\in H$, calcular la probabilidad a posteriori:

$$P(h|D)=\frac{P(D|h)P(h)}{P(D)}$$

- Reportar la hipotesis $h_{MAP}$ con la mayor probabilidad a posteriori:
$$h_{MAP}=\underset{h\in H}{\operatorname{argmax}}P(h|D)$$
-->

## Clasificación de una nueva instancia

- Nos hemos enfocado en la **hipotesis más probable**, dados los datos de entrenamiento ($h_{MAP}$)

- Dada una nueva instancia $x$, ¿cual es la **clasificación más probable**?

La clasificación más probable se obtiene combinando todas las hipotesis, ponderadas por sus probabilidades a posteriori.

## Clasificador Bayesiano Óptimo

$$\underset{v_j\in V}{\operatorname{argmax}} \sum_{h_i\in H}P(v_j|h_i)P(h_i|D)$$

- $v_j$ son las posibles clases en que puede ser etiquetada la instancia
- Las hipotesis son funciones, en nuestro caso, de clasificación (e.g. hiperplanos).

## Ejemplo

$$
\begin{array}{ccc} 
P(h_1|D)=0.4,& P(\ominus|h_1)=0,& P(\oplus|h_1)=1\\
P(h_2|D)=0.3,& P(\ominus|h_2)=1,& P(\oplus|h_2)=0\\
P(h_3|D)=0.3,& P(\ominus|h_3)=1,& P(\oplus|h_3)=0
\end{array}
$$ 

Entonces

$$\sum_{h_i\in H}P(\oplus|h_i)P(h_i|D)=0.4$$

$$\sum_{h_i\in H}P(\ominus|h_i)P(h_i|D)=0.6$$

---

$$\underset{v_j\in V}{\operatorname{argmax}} \sum_{h_i\in H}P(v_j|h_i)P(h_i|D)=\ominus$$

mientras que la $h_{MAP}$ indicaría que la instancia es etiquetada como $\oplus$ 

## Clasificador Bayesiano Ingenuo

Cuando usar:

- Tamaños de datasets medianos o grandes
- Atributos que describen a cada instancia son condicionalmente independientes dada la etiqueta o clasificación

Aplicaciones exitosas:

- Diagnostico de enfermedades
- Clasificación de textos (SPAM)

---

- Función de respuesta es $f:X\rightarrow V$
- Cada instancia $x$ es descrita por atributos $\{a_1,a_2,\ldots , a_n\}$
- Valor más probable de $f(x)$ es:

$$v_{MAP}=\underset{v_j\in V}{\operatorname{argmax}}P(v_j|a_1,a_2,\ldots , a_n)$$

$$=\underset{v_j\in V}{\operatorname{argmax}}\dfrac{P(a_1,a_2,\ldots , a_n|v_j)P(v_j)}{P(a_1,a_2,\ldots , a_n)}$$

$$=\underset{v_j\in V}{\operatorname{argmax}}P(a_1,a_2,\ldots , a_n|v_j)P(v_j)$$

## Supuesto de Bayes Ingenuo

$$P(a_1,a_2,\ldots , a_n)=\Pi_i P(a_i|v_j)$$

Lo que lleva al clasificador bayesiano ingenuo

$$v_{NB}=\underset{v_j\in V}{\operatorname{argmax}}P(v_j)\Pi_i P(a_i|v_j)$$

---

- Cada $P(a_i|v_j)$ puede tener una distribución de probabilidad específica.
- Generalmente se utilizan la Normal, Bernoulli y Multinomial.
