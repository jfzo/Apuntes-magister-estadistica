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
- Clasificación con datos desbalanceados
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

# Introducción

<!--
  pandoc -t beamer ./clase05.md -o clase05.pdf --katex --slide-level=2
 -->


- Disponibilidad de datos en distintos dominios
  - Redes de comunicación
  - Finanzas
  - Vigilancia
- Técnicas existentes para la extracción de conocimiento  han mostrado ser útiles en diversas problemáticas reales
- Existencia de desbalances notorios en la distribución de los datos compromete el aprendizaje y desempeño

---

* Detección de fallas en sistemas productivos
* Identificación de intrusos en redes de computadores
* Detección automática de comentarios ofensivos en redes sociales
* Detección de tejido con cancer vs sano

**Cualquier problema cuyos datos exhiban una distribución desigual de  entre sus clases**

## El Problema de los datos desbalanceados

- La mayoría de los métodos de propósito general en clasificación basan su desempeño una proporción similar de las etiquetas de clase y un igual costo de clasificación por clase

**Por ejemplo:**

-  Dado que la SVM (soft-margin) intenta minimizar el error total, se encuentra inherentemente sesgada hacia la clase mayoritaria
   - Falta de datos representando a la clase minoritaria, también puede generar un desbalance en los vectores soporte representativos


---

Existen varias fuentes de desbalance en los datos:

- Intrinseco: Resultado de la naturaleza de los datos
- Extrinseco: Resultado de factores variables tales como el tiempo o el almacenamiento
  - Ej. Interrupciones en el funcionamiento de un dispositivo transmisor

- Adicionalmente, el desbalance puede ser denominado relativo el tamaño de la clase minoritaria es proporcional a la mayoritaria
  - Un aumento en esta última, también provoca un aumento de la primera
- En contraste al desbalance relativo, existe el desbalance debido a observaciones raras.
  - Ej. Una enfermedad rara de la que existen pocos pacientes.


## Soluciones actuales

Al aplicar métodos estándar o de propósito general sobre conjuntos de datos desbalanceados.

Existen principalmente, dos grandes familias de métodos:

- Basados en muestreo: Buscan balancear la distribución de los datos
- Sensibles al costo (costo asimétrico): Modifican su función objetivo incorporando un costo de clasificación mayor en instancias de la clase minoritaria 

## Métodos basados en muestreo

- Random oversampling

  Consiste en seleccionar al azar ejemplos de la clase minoritaria y **agregarlos** al conjunto de datos
  - Problema: Ejemplos repetidos pueden producir sobreajuste

- Random undersampling

  Consiste en seleccionar al azar ejemplos de la clase mayoritaria y **removerlos** del conjunto de datos

  - Problema: Pérdida de información

---

- Informed undersampling: EasyEnsemble, BalanceCascade, basados en KNN.

  El objetivo es resolver el problema de pérdida de información generado por random undersampling.

  Ejemplos de la clase mayoritaria son escogidos de "mejor" manera que en random undersampling.

---

- Synthetic sampling (Generan datos): **SMOTE** y derivados.

  Se crean ejemplos de manera artificial usando los ejemplos de la clase minoritaria

  Se escogen al azar puntos a partir del KNN de cada punto de la clase minoritaria. Cada uno de estos vecinos es perturbado para generar un nuevo ejemplo.

  Problema: Puede aumentar el traslape entre las clases.

- Adaptive Synthetic sampling: Borderline-SMOTE, ADASYN

  Intenta abordar el problema de traslape que genera en ocasiones SMOTE.

  Identifica puntos claves de la clase minoritaria para luego generar los ejemplos artificiales.

## Métodos sensibles al costo


- Consideran el costo asociado con la clasificación errónea de ejemplos

- SVM con costo asimétrico de clasificación [Wang and Japkowicz, 2010]
- GSVM [Gonzalez-Abril et al., 2014]
- One-Class Support Vector Classifier [Li et al., 2006]

## Evaluación de desempeño

Es vital contar con métricas para evaluar la efectividad de algoritmos sobre datos desbalanceados.

- Considere un problema de clasificación en dos clases
- Una representación del desempeño en la clasificación puede ser formulado como una matriz de confusión (considere como clase positiva a la minoritaria)

\begin{tikzpicture}[remember picture, overlay]
    
    \node[above=0.5cm] at (current page.south) 
    {
        \includegraphics[width=0.4\textwidth]{contingencia.png}
    };

\end{tikzpicture}


---

Es frecuente encontrar las siguientes métricas para medir desempeño en la tarea de clasificación:

$$\mbox{Accuracy} = \frac{TP+TN}{(TP+FN)+(FP+TN)}$$
$$\mbox{Error rate} = 1-\mbox{Accuracy}$$

---

Existe ciertas situaciones en que este tipo de medidas puee llevar a resultados bastante engañosos.

* Por ejemplo, si del total de los datos, un $\%5$ es de la clases minoritaria.
* Un método que clasifique todo como de la clase mayoritaria tendría Accuracy de $\% 95$.

Por lo tanto, la métrica Accuracy **no** provee de información adecuada respecto de la calidad de clasificador $\rightarrow$ *Medida sensible a la distribución de los datos* 

---

Otras medidas son adoptadas en lugar de la Accuracy cuando se está en presencia de datos desbalanceados.

$$
\begin{array}{rl} 
\mbox{Precision}=&\frac{TP}{TP+FP}\\
\mbox{Recall}=& \frac{TP}{TP+FN}\\
F_{\beta}=& \frac{(1+\beta^2)\times \mbox{Recall}\times \mbox{Precision}}{\beta^2 \times \mbox{Recall}+ \mbox{Precision}}\ , \ \mbox{usualmente }\beta=1\\
\mbox{G-mean}=&\sqrt{\frac{TP}{FP+FN}\times \frac{TN}{TN+FP}}
\end{array}
$$ 

---

- Precision es una medida de exactitud (de lo detectado, cuánto es correcto)
- Recall es una medidade completitud (cuánto de lo positivo fue detectado correctamente)
- Siempre usar Precision y Recall como parte de un criterio combinado

## Receiver Operating Characteristics

- Llamada generalmente Curva ROC [Fawcett, 2006]
- Provee de una representación visual del equilibrio relativo entre el beneficio y el costo de la clasificación, considerando la distribución de los datos.
- Compara dos cantidades extraídas a partir de la matriz de confusión: 
  $$\mbox{TP-rate}=\frac{TP}{(TP+FN)}\ \ ; \ \mbox{FP-rate}=\frac{FP}{(FP+TN)}$$

- El gráfico ROC consiste en $\mbox{TP-rate}$ vs $\mbox{FP-rate}$
- El método genera una curva para cada clasificador evaluado

---


\begin{tikzpicture}[remember picture, overlay]
    
    \node[above=1.0cm] at (current page.south) 
    {
        \includegraphics[width=0.5\textwidth]{roc.png}
    };
    \node[below=-0.9cm,font=\fontsize{5pt}{5pt}\selectfont] at (current page.south)  
    {
      Fuente \url{https://en.wikipedia.org/wiki/Receiver_operating_characteristic}
    };
\end{tikzpicture}


## Referencias

<style scoped>
{
  font-size: 22px
}
</style>

- Fawcett, T. (2006). An introduction to ROC analysis. Pattern recognition letters, 27(8), 861-874.

- Li, P., Chan, K. L., & Fang, W. (2006, August). Hybrid kernel machine ensemble for imbalanced data sets. In 18th International Conference on Pattern Recognition (ICPR'06) (Vol. 1, pp. 1108-1111). IEEE.

- Wang, B. X., & Japkowicz, N. (2010). Boosting support vector machines for imbalanced data sets. Knowledge and information systems, 25(1), 1-20.

- Gonzalez-Abril, L., Nunez, H., Angulo, C., & Velasco, F. (2014). GSVM: An SVM for handling imbalanced accuracy between classes inbi-classification problems. Applied Soft Computing, 17, 23-31.

- Chawla, N. V., Bowyer, K. W., Hall, L. O., & Kegelmeyer, W. P. (2002). SMOTE: synthetic minority over-sampling technique. Journal of artificial intelligence research, 16, 321-357.