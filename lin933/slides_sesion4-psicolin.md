---
title: LIIN-933
subtitle: Análisis exploratorio de datos de lectura (continuación con el corpus)
author: Juan Zamora O.
date: Módulo de Análisis Exploratorio de Datos
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
toc: false
toc-depth: 1
toc-title: Estructura de la Presentación
---


## Qué haremos hoy

Anteriormente describimos la forma de una distribución mirando un histograma. Hoy la describimos numéricamente.

Cinco bloques: tendencia central, dispersión, posición relativa, diagrama de caja, medidas de asociación.

Seguimos con los datos de lectura de MECO. Cada medida se calcula sobre una variable que ya conocemos: `dur`, `long_palabra`, `nfix`.


\note{Encuadre de tres minutos. El hilo conductor de la sesión es que cada medida nueva responde a una pregunta que quedó abierta la clase pasada: por qué media y mediana difieren, cómo cuantificar cuánto difieren, y cómo comparar grupos de forma más rigurosa que mirando un histograma.}


# 1. Medidas de tendencia central

## Media, mediana y moda

```r
mean(fijadas$dur)
median(fijadas$dur)
```

La moda no tiene función incorporada en R. Se construye a partir de una tabla de frecuencias:

```r
moda <- function(x) {
  tabla <- table(x)
  as.numeric(names(tabla)[tabla == max(tabla)])
}

moda(fijadas$long_palabra)
```

Tres medidas: valor central por suma, valor central por posición, valor más repetido.

\note{Explicitar que la moda puede tener más de un valor si hay empate en la frecuencia máxima; por eso la función devuelve un vector y no un escalar. Aplicarla sobre long_palabra en lugar de dur, porque dur es continua y casi no tiene valores repetidos, mientras que la longitud de palabra sí.}

## Cuándo cada medida es apropiada

| **Medida** | Es apropiada cuando | No es apropiada cuando |
|---|---|---|
| Media | La distribución es simétrica | Hay asimetría marcada o valores extremos |
| Mediana | Hay asimetría o valores extremos | Se necesita usar la suma total de los datos |
| Moda | La variable es categórica o discreta | Hay muchos valores distintos con frecuencia similar |

```r
mean(fijadas$dur) - median(fijadas$dur)
```

Una diferencia notoria entre media y mediana da cuenta de asimetría.

\note{Retomar el resultado de la sesión anterior: la distribución de dur es asimétrica, por lo que la diferencia entre media y mediana debería ser grande en términos relativos. Pedir que calculen esa diferencia como proporción de la mediana antes de seguir: es la actividad 1.3.}

## Actividades del bloque 1

**1.1** Calcula la media, la mediana y la moda de `nfix` (número de fijaciones) sobre el objeto `fijadas`. Reporta los tres valores con dos decimales cuando corresponda.

**1.2** Calcula la media y la mediana de `dur` por separado para cada lengua, usando `tapply()`. Identifica la lengua donde la diferencia entre ambas medidas es mayor.

**1.3** Calcula la diferencia entre media y mediana de `dur` como proporción de la mediana: `(media - mediana) / mediana`. Expresa el resultado como porcentaje.

\note{Ocho minutos. La 1.2 exige aplicar tapply() dos veces o escribir una función que devuelva ambas medidas a la vez; ambas soluciones son válidas y conviene mostrarlas si el tiempo alcanza. La 1.3 da una cifra concreta de asimetría que se retomará en el bloque 2.}

# 2. Medidas de posición relativa

## Percentiles y cuantiles

Un percentil indica el valor por debajo del cual se encuentra un porcentaje determinado de las observaciones.

```r
quantile(fijadas$dur, probs = c(0.10, 0.25, 0.50, 0.75, 0.90))
```

El percentil 50 es la mediana. Los percentiles 25 y 75 son el primer y el tercer cuartil.

```r
quantile(fijadas$dur, probs = seq(0, 1, by = 0.1))   # deciles
```

\note{Mostrar que quantile() acepta cualquier vector de probabilidades, no solo cuartiles: eso permite calcular deciles o cualquier corte necesario para una pregunta específica. Señalar que el argumento se llama probs y recibe proporciones entre 0 y 1, no porcentajes.}

## Uso de percentiles para definir umbrales

Los percentiles permiten clasificar observaciones sin fijar un umbral arbitrario de antemano.

```r
umbral_90 <- quantile(fijadas$dur, probs = 0.90)
umbral_90

fijadas$lectura_lenta <- fijadas$dur > umbral_90

mean(fijadas$lectura_lenta)     # debe ser aproximadamente 0.10
```

El diez por ciento de las palabras con mayor tiempo de lectura quedan marcadas, sin necesidad de decidir un número fijo de milisegundos.

\note{El resultado de mean(fijadas$lectura_lenta) debe ser cercano a 0.10 por construcción: es una verificación de que el umbral se aplicó correctamente. Esta técnica se retomará en el bloque 4 al hablar de valores atípicos, que se definen con un criterio distinto pero relacionado.}

## Actividades del bloque 2

**2.1** Calcula los percentiles 10, 25, 50, 75 y 90 de `long_palabra` sobre `meco`. Interpreta el percentil 90: ¿qué significa ese valor en palabras simples?

**2.2** Define como "palabra larga" a toda palabra con longitud igual o superior al percentil 90 de `long_palabra`. Calcula qué proporción de las palabras del corpus cumple esa condición y verifica que el resultado es cercano al esperado.

**2.3** Calcula el percentil correspondiente a una duración de 300 milisegundos dentro de `fijadas$dur`, usando la función `ecdf()`. Redacta una frase que exprese ese resultado en términos de percentil.

\note{Nueve minutos. La 3.3 introduce ecdf(), que no se ha usado antes: `ecdf(fijadas$dur)(300)` devuelve la proporción de observaciones por debajo de 300. Es la operación inversa de quantile() y conviene mostrarla en la pizarra si nadie la resuelve de forma espontánea.}


# 3. Medidas de dispersión

## Rango y rango intercuartílico

```r
max(fijadas$dur) - min(fijadas$dur)     # rango

IQR(fijadas$dur)                        # rango intercuartílico
```

El rango depende únicamente de los dos valores extremos y es muy sensible a ellos.

El rango intercuartílico es la diferencia entre el tercer y el primer cuartil, y contiene el cincuenta por ciento central de los datos:

```r
quantile(fijadas$dur, probs = c(0.25, 0.75))
```

\note{Calcular el rango en vivo y preguntar qué pasaría si se elimina una sola observación extrema del conjunto de datos: el rango puede cambiar de forma drástica con un solo valor, mientras que el rango intercuartílico apenas se altera. Es el argumento a favor de preferir el segundo cuando hay asimetría.}

## Varianza y desviación estándar

```r
var(fijadas$dur)     # varianza
sd(fijadas$dur)      # desviación estándar
```

La desviación estándar se expresa en la misma unidad que la variable original; la varianza, en esa unidad al cuadrado.

Por esa razón, la desviación estándar es la que se reporta habitualmente.

```r
sqrt(var(fijadas$dur)) == sd(fijadas$dur)
```

\note{La equivalencia de la última línea rara vez se muestra y ayuda a fijar que sd() no es un cálculo distinto de var(), sino su raíz cuadrada. Mencionar que ambas funciones dividen por n menos uno, no por n, porque se están calculando sobre una muestra.}

## Coeficiente de variación

Varianza y desviación estándar no permiten comparar variables en escalas distintas. El coeficiente de variación sí, porque es adimensional:

$$CV = \frac{\text{desviación estándar}}{\text{media}} \times 100$$

```r
cv <- function(x) sd(x) / mean(x) * 100

cv(fijadas$dur)             # milisegundos
cv(fijadas$long_palabra)    # caracteres
```

Un CV mayor indica más dispersión relativa, sin importar la unidad de medida.

\note{Este es el punto donde se justifica por qué existe una medida más allá de la desviación estándar. Comparar directamente sd(dur) con sd(long_palabra) no tiene sentido porque están en unidades distintas; el CV sí permite decir cuál de las dos variables es relativamente más dispersa.}

## Actividades del bloque 3

**3.1** Calcula el rango, el rango intercuartílico, la varianza y la desviación estándar de `dur` sobre `fijadas`. Presenta los cuatro valores en una tabla.

**3.2** Calcula la desviación estándar de `dur` por separado para cada lengua con `tapply()`. Identifica la lengua con mayor y con menor dispersión.

**3.3** Calcula el coeficiente de variación de `dur` y el de `long_palabra`. ¿Cuál de las dos variables presenta mayor dispersión relativa?

**3.4** Repite el cálculo del coeficiente de variación de `dur`, mostrado en la lámina anterior, pero calculado por separado para cada lengua. Ordena el resultado de mayor a menor.

\note{Diez minutos. La 3.2 puede generar una discusión útil: la lengua con mayor desviación estándar no siempre es la de mayor media, y conviene señalar esa posible disociación explícitamente antes de que alguien la asuma sin comprobarla.}



# 4. Boxplot - Diagrama de caja y bigotes

## Construcción del diagrama

Resume cinco valores: el mínimo, el primer cuartil, la mediana, el tercer cuartil y el máximo, ajustando los dos últimos según un criterio de valores atípicos.

```r
boxplot(fijadas$dur,
        main = "Tiempo total de lectura por palabra",
        ylab = "Milisegundos")
```

```r
boxplot(dur ~ lang, data = fijadas,
        las = 2, cex.axis = 0.8,
        main = "Tiempo de lectura por lengua",
        ylab = "Milisegundos")
```

\note{Señalar en el gráfico cada elemento con el puntero: la caja es el rango intercuartílico, la línea interior es la mediana, y los bigotes se extienden hasta el valor observado más alejado que no se considera atípico. Esta lámina se limita a nombrar las partes; la definición exacta de los bigotes viene en la siguiente.}

## Criterio de valores atípicos

Un valor se considera atípico si está por debajo de $Q_1 - 1{,}5 \times IQR$ o por encima de $Q_3 + 1{,}5 \times IQR$.

```r
Q1 <- quantile(fijadas$dur, 0.25)
Q3 <- quantile(fijadas$dur, 0.75)
IQR <- Q3 - Q1

limite_inferior <- Q1 - 1.5 * IQR
limite_superior <- Q3 + 1.5 * IQR

c(limite_inferior, limite_superior)

atipicos <- subset(fijadas, dur < limite_inferior | dur > limite_superior)
nrow(atipicos)
round(nrow(atipicos) / nrow(fijadas) * 100, 2)
```

El valor 1,5 es una convención, no una regla derivada de los datos.

\note{Es importante decir explícitamente que 1,5 es una convención de Tukey y no un valor que se deduzca de la distribución. Con datos tan asimétricos como las duraciones de lectura, el límite inferior suele ser negativo, lo cual no elimina observaciones por ese lado porque las duraciones no pueden ser negativas.}

## Actividades del bloque 4

**4.1** Calcula los límites inferior y superior para valores atípicos de `dur` sobre `fijadas`, siguiendo el criterio de la lámina anterior. Indica cuántas observaciones caen fuera de esos límites y qué porcentaje representan del total.

**4.2** Construye el diagrama de caja de `dur` separado por `long_grupo`. Ordena las categorías del eje horizontal de menor a mayor longitud antes de graficar.

**4.3** A partir del diagrama de la actividad 4.2, indica qué grupo de longitud presenta la mayor cantidad de valores atípicos visibles en el gráfico.

**4.4** Calcula el límite superior de valores atípicos de `dur` por separado para dos lenguas distintas. Indica si el límite es el mismo o distinto entre ambas, y qué implica eso sobre la variabilidad de cada lengua.

\note{Doce minutos. La 4.2 requiere convertir long_grupo a factor con el orden correcto si no se hizo al crearlo con cut(); recordar que cut() ya devuelve los niveles en orden si breaks fue ascendente, así que no hace falta reordenar. La 4.4 conecta con la actividad 2.2 sobre desviación estándar por lengua: los límites deberían diferir en la misma dirección.}

# 5. Medidas de asociación

## Correlación entre dos variables numéricas

```r
cor(fijadas$long_palabra, fijadas$dur, method = "pearson")

cor.test(fijadas$long_palabra, fijadas$dur, method = "pearson")
```

`cor()` devuelve solo el coeficiente. `cor.test()` añade un intervalo de confianza y un valor p que evalúa si la correlación observada es distinguible de cero.

```r
cor.test(fijadas$long_palabra, fijadas$dur, method = "spearman")
```

Con un conjunto de datos de este tamaño, casi cualquier correlación distinta de cero resulta significativa. El valor p informa sobre la existencia de asociación, no sobre su magnitud.

\note{Este último punto es importante y suele pasarse por alto: con cientos de miles de observaciones, un coeficiente de 0.05 puede tener un valor p extremadamente bajo sin que la asociación sea de interés práctico. Distinguir significancia estadística de magnitud del efecto.}

## Asociación entre dos variables categóricas

Para variables categóricas se usa una tabla de contingencia y una prueba de independencia.

```r
tabla <- table(meco$skip, meco$long_grupo)
tabla

chisq.test(tabla)
```

La prueba evalúa si la distribución de una variable depende de las categorías de la otra.

```r
resultado <- chisq.test(tabla)
resultado$expected     # frecuencias esperadas bajo independencia
resultado$statistic     # estadístico chi-cuadrado
```

\note{Mostrar resultado$expected junto a la tabla observada ayuda a que la lógica de la prueba quede clara: se comparan las frecuencias que efectivamente se observaron con las que se esperarían si la omisión no dependiera de la longitud. Advertir que chisq.test() puede generar una advertencia si alguna celda esperada es menor a cinco, y en ese caso conviene agrupar categorías.}

## Actividades del bloque 5

**5.1** Calcula la correlación de Pearson y de Spearman entre `nfix` y `dur` sobre `fijadas`. Indica si ambos coeficientes son similares o difieren de forma apreciable.

**5.2** Ejecuta `cor.test()` entre `long_palabra` y `dur`. Reporta el coeficiente, el intervalo de confianza y el valor p en una sola frase.

**5.3** Construye la tabla de contingencia entre `meco$skip` y `meco$lang`. Ejecuta `chisq.test()` sobre esa tabla y reporta el estadístico y el valor p.

**5.4** A partir del resultado de la actividad 5.3, extrae las frecuencias esperadas con `resultado$expected` y compáralas con la tabla observada para dos lenguas cualesquiera. Señala en qué lengua la diferencia entre lo observado y lo esperado es mayor.

\note{Once minutos, es el bloque más denso. La 5.4 exige comparar visualmente dos matrices del mismo tamaño; sugerir restar una de la otra con resultado$expected - tabla para verlo de forma directa en lugar de comparar celda por celda a simple vista.}

# Cierre

## Qué deberías poder hacer

- Calcular media, mediana y moda, y decidir cuál reportar según la forma de la distribución
- Calcular rango, rango intercuartílico, varianza, desviación estándar y coeficiente de variación
- Obtener percentiles y usarlos para definir umbrales
- Identificar valores atípicos con el criterio de 1,5 veces el rango intercuartílico
- Calcular e interpretar correlaciones y pruebas de independencia


\note{Cierre de tres minutos. Preguntar explícitamente por el punto que suele quedar más débil: la diferencia entre significancia estadística y magnitud del efecto, que apareció en el bloque 5 y que reaparecerá en cualquier análisis inferencial posterior.}

## Referencias

\footnotesize

- Gries, S. Th. (2021). *Statistics for Linguistics with R* (3.ª ed.). Mouton de Gruyter.
- Baayen, R. H. (2008). *Analyzing Linguistic Data*. Cambridge University Press.
- Tukey, J. W. (1977). *Exploratory Data Analysis*. Addison-Wesley.
- Datos: <https://osf.io/3527a>

\note{Tukey (1977) es la referencia original del criterio de 1,5 veces el rango intercuartílico para valores atípicos, presentado en el bloque 4.}