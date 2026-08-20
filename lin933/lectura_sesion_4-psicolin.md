# Semana 3. Medidas estadísticas y resumen de datos

Módulo de Análisis Exploratorio de Datos, Doctorado en Lingüística.

En la sesión anterior describimos la forma de una distribución mediante histogramas y diagramas de dispersión. Esa descripción visual es indispensable, pero es imprecisa: dos personas pueden mirar el mismo histograma y describir su asimetría con palabras distintas. El objetivo de esta sesión es sustituir esas descripciones cualitativas por números que se calculan de una forma establecida y que, por lo tanto, permiten comparar resultados entre corpus, entre lenguas y entre estudios distintos.

El apunte sigue trabajando con el corpus MECO. No se introduce un conjunto de datos nuevo: cada medida que se presenta se aplica sobre variables que ya se exploraron visualmente en la sesión anterior, en particular `dur`, el tiempo total de lectura de una palabra, y `long_palabra`, su longitud en caracteres. Esto tiene un propósito deliberado. Al calcular una medida sobre una variable cuya forma ya se conoce, es posible verificar si el número obtenido es coherente con lo que el histograma mostraba, y detectar así un error de cálculo o de interpretación antes de que se propague al resto del análisis.

El apunte tiene siete partes. Las primeras cinco corresponden a otras tantas familias de medidas: tendencia central, dispersión, posición relativa, resumen gráfico mediante el diagrama de caja, y asociación entre variables. La sexta es una extensión que retoma las dos lenguas que cada estudiante seleccionó al final de la sesión anterior, y aplica sobre ellas el conjunto completo de medidas presentadas aquí. La séptima cierra la sesión.

Como en el apunte anterior, los bloques de código no muestran los resultados que producirán. Los valores exactos dependen de la versión del archivo descargado y deben obtenerse ejecutando el código.

## Antes de empezar: recuperar los objetos

El siguiente bloque reconstruye los objetos que se usaron en la sesión anterior, por si la sesión de R no se mantuvo abierta entre una clase y la otra.

```r
load("joint_data_trimmed.rda")   # ajustar al nombre real del archivo
meco <- get(ls()[1])             # ajustar al nombre del objeto cargado

meco$long_palabra <- nchar(meco$ia)
meco$long_grupo <- cut(meco$long_palabra,
                       breaks = c(0, 3, 5, 8, Inf),
                       labels = c("muy corta", "corta",
                                  "media", "larga"))

fijadas <- subset(meco, skip == 0)
```

`fijadas` contiene únicamente las observaciones de palabras que recibieron al menos una fijación. Todas las medidas que involucran duraciones de lectura se calculan sobre este subconjunto, por la razón discutida en la sesión anterior: una palabra omitida no tiene duración porque nunca fue mirada, y promediar sobre `NA` sin filtrar antes oculta esa decisión.

## 1. Medidas de tendencia central

Las medidas de tendencia central resumen un conjunto de datos con un único valor que representa su centro. Existen tres medidas de uso común, y no son intercambiables: cada una responde a una pregunta distinta y es sensible a distintos aspectos de los datos.

### 1.1 Media aritmética

La media aritmética es la suma de todas las observaciones dividida por su número:

$$\bar{x} = \frac{1}{n} \sum_{i=1}^{n} x_i$$

```r
mean(fijadas$dur)
```

La media utiliza el valor exacto de cada observación, lo que la hace sensible a valores extremos. Una sola observación con un valor muy alto desplaza la media hacia arriba, incluso si el resto de las observaciones está concentrado en valores mucho menores. Esta sensibilidad no es un defecto de la media en sí misma, sino una consecuencia directa de su definición: si se busca un resumen que use la información completa de cada dato, incluyendo su magnitud exacta, la media es la medida apropiada. El problema surge cuando se usa la media como si fuera un valor típico en una distribución donde no lo es.

### 1.2 Mediana

La mediana es el valor que ocupa la posición central cuando las observaciones se ordenan de menor a mayor. Si el número de observaciones es impar, es el valor central; si es par, es el promedio de los dos valores centrales.

```r
median(fijadas$dur)
```

A diferencia de la media, la mediana no utiliza la magnitud exacta de las observaciones, sino únicamente su posición relativa. Por esa razón, es robusta frente a valores extremos: mover el valor máximo de un conjunto de datos a un valor aún más alto no cambia la mediana, porque su posición dentro del ordenamiento sigue siendo la misma.

### 1.3 Moda

La moda es el valor que aparece con mayor frecuencia. Es la única de las tres medidas que tiene sentido aplicar directamente sobre variables categóricas, y también es aplicable sobre variables numéricas discretas con pocos valores distintos.

R no incluye una función para calcular la moda; la función `mode()` del lenguaje base cumple un propósito distinto, relacionado con el tipo de almacenamiento de un objeto, y no debe confundirse con la moda estadística. Es necesario construir la función:

```r
moda <- function(x) {
  tabla <- table(x)
  as.numeric(names(tabla)[tabla == max(tabla)])
}

moda(fijadas$long_palabra)
```

La función devuelve un vector, no un único valor, porque una distribución puede tener más de un valor con la frecuencia máxima. Aplicada sobre `long_palabra`, la moda identifica la longitud de palabra más común en el corpus. Aplicarla sobre `dur` sería poco informativo, porque al tratarse de una variable con precisión de milisegundos, es infrecuente que dos observaciones coincidan exactamente, y la tabla de frecuencias tendría muchos valores empatados en una frecuencia mínima.

### 1.4 Cuándo cada medida es apropiada

La elección entre media, mediana y moda depende de la forma de la distribución y del tipo de variable.

| Medida | Apropiada cuando | Poco apropiada cuando |
|---|---|---|
| Media | La distribución es razonablemente simétrica | Hay asimetría marcada o valores extremos influyentes |
| Mediana | Hay asimetría o valores extremos | Se necesita preservar la suma total de los datos |
| Moda | La variable es categórica o discreta con pocos valores | Hay muchos valores distintos con frecuencias similares |

Una forma de cuantificar, de manera informal, cuánto se aparta una distribución de la simetría es comparar la media con la mediana:

```r
mean(fijadas$dur) - median(fijadas$dur)
```

Cuando la media supera claramente a la mediana, la distribución tiene una cola hacia valores altos, que es exactamente lo que se observó en el histograma de `dur` en la sesión anterior. Cuando ambas medidas son similares, no hay razón para preferir una sobre otra por motivos de asimetría, aunque la elección puede seguir dependiendo de otros criterios, como la facilidad de interpretación para la audiencia del informe.

### Actividades 1

**1.1** Calcula la media, la mediana y la moda de `nfix`, el número de fijaciones por palabra, sobre el objeto `fijadas`. Presenta los tres valores con dos decimales cuando corresponda.

**1.2** Calcula la media y la mediana de `dur` por separado para cada lengua, usando `tapply()`. Construye una tabla con ambas medidas y su diferencia, y ordénala para identificar la lengua donde esa diferencia es mayor.

**1.3** Calcula la diferencia entre media y mediana de `dur` como proporción de la mediana, mediante la expresión `(media - mediana) / mediana`. Expresa el resultado como porcentaje.

## 2. Medidas de dispersión

Una medida de tendencia central, por sí sola, no informa sobre cuánto varían los datos alrededor de ese centro. Dos conjuntos de datos pueden compartir la misma media y tener una dispersión completamente distinta. Las medidas de dispersión cuantifican esa variabilidad.

### 2.1 Rango

El rango es la diferencia entre el valor máximo y el valor mínimo:

$$R = x_{max} - x_{min}$$

```r
max(fijadas$dur) - min(fijadas$dur)
```

El rango es la medida de dispersión más simple, pero también la más inestable: depende únicamente de dos observaciones, las más extremas, y por tanto puede cambiar de manera drástica si se agrega o elimina un solo dato del conjunto.

### 2.2 Rango intercuartílico

El rango intercuartílico, abreviado RIC, es la diferencia entre el tercer cuartil y el primer cuartil:

$$RIC = Q_3 - Q_1$$

```r
IQR(fijadas$dur)
quantile(fijadas$dur, probs = c(0.25, 0.75))
```

El primer cuartil es el valor por debajo del cual se encuentra el veinticinco por ciento de las observaciones, y el tercer cuartil, el valor por debajo del cual se encuentra el setenta y cinco por ciento. El RIC contiene, por definición, al cincuenta por ciento central de los datos, y no se ve afectado por lo que ocurra en los extremos de la distribución. Es, en este sentido, el equivalente en dispersión de lo que la mediana es en tendencia central: una medida basada en posiciones relativas y no en magnitudes exactas.

### 2.3 Varianza y desviación estándar

La varianza mide la dispersión mediante el promedio de las distancias al cuadrado entre cada observación y la media:

$$s^2 = \frac{1}{n-1} \sum_{i=1}^{n} (x_i - \bar{x})^2$$

```r
var(fijadas$dur)
```

El denominador es $n - 1$ y no $n$ porque la varianza se está estimando a partir de una muestra, no calculando sobre una población completa; dividir por $n - 1$ produce un estimador sin sesgo del parámetro poblacional. Esta corrección no cambia de forma apreciable el resultado cuando el número de observaciones es grande, como ocurre en este corpus, pero es la razón formal de por qué R divide por $n - 1$ y no por $n$.

Elevar las distancias al cuadrado tiene una consecuencia práctica sobre la unidad de la varianza: si `dur` se mide en milisegundos, la varianza se expresa en milisegundos al cuadrado, una unidad sin interpretación directa. La desviación estándar corrige este problema tomando la raíz cuadrada de la varianza, y devuelve el resultado a la escala original:

$$s = \sqrt{s^2}$$

```r
sd(fijadas$dur)
sqrt(var(fijadas$dur)) == sd(fijadas$dur)
```

Por esta razón, la desviación estándar es la medida que se reporta habitualmente, mientras que la varianza suele aparecer como un paso intermedio del cálculo o en contextos donde su propiedad de aditividad resulta útil, por ejemplo, en el análisis de varianza.

### 2.4 Coeficiente de variación

La desviación estándar no permite comparar la dispersión de dos variables que están en unidades distintas, porque una desviación de veinte milisegundos y una desviación de dos caracteres no son magnitudes comparables entre sí. El coeficiente de variación resuelve este problema al expresar la desviación estándar como proporción de la media:

$$CV = \frac{s}{\bar{x}} \times 100$$

```r
cv <- function(x) sd(x) / mean(x) * 100

cv(fijadas$dur)
cv(fijadas$long_palabra)
```

Al ser una razón entre dos cantidades que comparten unidad, el coeficiente de variación resulta adimensional, y por lo tanto comparable entre variables medidas de formas distintas. Un coeficiente de variación mayor indica una dispersión relativa más grande con respecto a la propia escala de la variable, con independencia de cuál sea esa escala.

Una limitación del coeficiente de variación conviene señalarla aquí: no está definido, o resulta poco interpretable, cuando la media de la variable es cero o cercana a cero, y tampoco tiene una interpretación clara sobre variables que pueden tomar valores negativos, porque el signo de la media puede invertir el signo del coeficiente sin que eso refleje un cambio real en la dispersión.

### Actividades 2

**2.1** Calcula el rango, el rango intercuartílico, la varianza y la desviación estándar de `dur` sobre `fijadas`. Presenta los cuatro valores en una tabla.

**2.2** Calcula la desviación estándar de `dur` por separado para cada lengua, usando `tapply()`. Identifica la lengua con mayor dispersión y la de menor dispersión, y compara ese resultado con las medias por lengua calculadas en la actividad 1.2 para comprobar si ambas medidas van en la misma dirección.

**2.3** Calcula el coeficiente de variación de `dur` y el de `long_palabra`. Indica cuál de las dos variables presenta mayor dispersión relativa.

**2.4** Calcula el coeficiente de variación de `dur` por separado para cada lengua. Ordena el resultado de mayor a menor y señala qué lengua presenta la dispersión relativa más alta.

## 3. Medidas de posición relativa

Las medidas de posición relativa ubican una observación, o un valor arbitrario, dentro de la distribución completa de los datos, expresando esa ubicación en términos de proporción de observaciones por debajo o por encima.

### 3.1 Percentiles y cuantiles

Un percentil es el valor por debajo del cual se encuentra un porcentaje determinado de las observaciones. El percentil 50 coincide, por definición, con la mediana; los percentiles 25 y 75 son el primer y el tercer cuartil, ya presentados en la sección anterior.

```r
quantile(fijadas$dur, probs = c(0.10, 0.25, 0.50, 0.75, 0.90))
```

El argumento `probs` de la función `quantile()` recibe proporciones entre 0 y 1, no porcentajes entre 0 y 100. Puede recibir cualquier vector de proporciones, lo que permite calcular deciles, dividiendo la distribución en diez partes:

```r
quantile(fijadas$dur, probs = seq(0, 1, by = 0.1))
```

o cualquier otro corte que una pregunta particular requiera. Cuando el número de observaciones no permite dividir la distribución en partes exactas, existen varios métodos de interpolación entre observaciones adyacentes; R implementa nueve de ellos y usa uno por defecto, adecuado para la gran mayoría de los usos exploratorios.

### 3.2 Uso de percentiles para definir umbrales

Una aplicación directa de los percentiles es la definición de umbrales sin recurrir a un valor arbitrario fijado de antemano. En lugar de decidir, por ejemplo, que una lectura "lenta" corresponde a toda duración superior a cierto número de milisegundos elegido sin justificación, se puede definir en términos relativos a la propia distribución:

```r
umbral_90 <- quantile(fijadas$dur, probs = 0.90)
umbral_90

fijadas$lectura_lenta <- fijadas$dur > umbral_90

mean(fijadas$lectura_lenta)
```

La proporción de observaciones marcadas como verdaderas debe acercarse a diez por ciento, porque esa es exactamente la definición del percentil elegido como corte; calcular esa proporción después de aplicar el umbral es una forma sencilla de verificar que el procedimiento se aplicó de manera correcta.

Este mismo procedimiento, aplicado con un vector de proporciones en lugar de una sola, es la base para construir la variable `long_grupo` que se usó en la sesión anterior y que se retomará en la sección 4 de este apunte, aunque en ese caso los puntos de corte se fijaron a mano en lugar de derivarse de percentiles.

### 3.3 Función de distribución empírica

La pregunta inversa a la que responde `quantile()` es: dado un valor concreto, ¿qué proporción de las observaciones se encuentra por debajo de él? Esa pregunta la responde la función de distribución empírica, disponible en R mediante `ecdf()`:

```r
funcion_distribucion <- ecdf(fijadas$dur)
funcion_distribucion(300)
```

`ecdf()` no devuelve directamente un número: devuelve una función, que luego se evalúa en el valor de interés. El resultado de esa evaluación es la proporción de observaciones menores o iguales a ese valor, expresada como un número entre 0 y 1.

`quantile()` y `ecdf()` son funciones inversas entre sí: la primera va de una proporción a un valor, la segunda va de un valor a una proporción. Encadenarlas debería devolver, de manera aproximada, el valor original:

```r
funcion_distribucion(quantile(fijadas$dur, 0.75))   # cercano a 0.75
```

Las pequeñas discrepancias que puedan aparecer se deben a los métodos de interpolación mencionados en la sección 3.1 y no indican un error de cálculo.

### Actividades 3

**3.1** Calcula los percentiles 10, 25, 50, 75 y 90 de `long_palabra` sobre `meco`, el conjunto completo de observaciones, no solo las fijadas. Redacta una frase que explique en términos simples qué significa el percentil 90 obtenido.

**3.2** Define como "palabra larga" a toda palabra cuya longitud sea igual o superior al percentil 90 calculado en la actividad 3.1. Calcula qué proporción de las palabras del corpus cumple esa condición. Si el resultado no es exactamente diez por ciento, explica por qué puede ocurrir esa discrepancia, considerando que `long_palabra` es una variable discreta con valores repetidos.

**3.3** Usando `ecdf()` sobre `fijadas$dur`, calcula el percentil que corresponde a una duración de 300 milisegundos. Redacta el resultado como una frase que indique qué proporción de las palabras fijadas tuvo una duración igual o menor a ese valor.

## 4. Diagrama de caja y bigotes

El diagrama de caja y bigotes, comúnmente llamado por su nombre en inglés, *boxplot*, condensa en una sola representación gráfica cinco valores de una distribución: el mínimo, el primer cuartil, la mediana, el tercer cuartil y el máximo, ajustando los dos últimos según un criterio explícito de valores atípicos que se detalla más adelante.

### 4.1 Elementos del diagrama

```r
boxplot(fijadas$dur,
        main = "Tiempo total de lectura por palabra",
        ylab = "Milisegundos")
```

La caja central se extiende desde el primer cuartil hasta el tercer cuartil, de modo que su altura es exactamente el rango intercuartílico definido en la sección 2.2. Una línea interior marca la mediana. Dos líneas, llamadas bigotes, se extienden desde los bordes de la caja hasta el valor observado más alejado que aún se considera dentro de un rango razonable, según el criterio que se define en la sección siguiente. Las observaciones que quedan fuera de ese rango se representan como puntos individuales.

El diagrama de caja es especialmente útil para comparar varios grupos en un mismo gráfico:

```r
boxplot(dur ~ lang, data = fijadas,
        las = 2, cex.axis = 0.8,
        main = "Tiempo de lectura por lengua",
        ylab = "Milisegundos")
```

La notación `dur ~ lang` indica que se debe construir un diagrama de caja de `dur` separado para cada nivel de la variable `lang`. Esta misma notación reaparecerá en modelos estadísticos posteriores del módulo, y conviene familiarizarse con su lectura: la variable a la izquierda de la virgulilla es la que se resume, y la de la derecha define los grupos.

### 4.2 Criterio de valores atípicos

El criterio más extendido para marcar una observación como atípica en un diagrama de caja fue propuesto por John Tukey. Una observación se considera atípica si cae por debajo de:

$$Q_1 - 1{,}5 \times RIC$$

o por encima de:

$$Q_3 + 1{,}5 \times RIC$$

```r
Q1  <- quantile(fijadas$dur, 0.25)
Q3  <- quantile(fijadas$dur, 0.75)
RIC <- Q3 - Q1

limite_inferior <- Q1 - 1.5 * RIC
limite_superior <- Q3 + 1.5 * RIC
c(limite_inferior, limite_superior)
```

El valor 1,5 que multiplica al rango intercuartílico es una convención adoptada por Tukey y no se deriva matemáticamente de ninguna propiedad de los datos. Existen otras convenciones, como usar un factor de 3 para distinguir entre valores atípicos moderados y extremos, pero 1,5 es, con diferencia, la más utilizada en la práctica y la que aplican por defecto tanto la función `boxplot()` como la mayoría del software estadístico.

Un criterio basado en el rango intercuartílico funciona de manera razonable sobre distribuciones aproximadamente simétricas, pero produce resultados que conviene interpretar con cautela sobre distribuciones muy asimétricas, como la de `dur`. En ese caso, es habitual que el límite inferior resulte negativo, lo cual no elimina ninguna observación por ese lado porque una duración de lectura no puede ser negativa, mientras que el límite superior sí produce un número considerable de observaciones marcadas como atípicas. Esto no significa que el criterio esté mal aplicado: significa que, en distribuciones asimétricas, la definición de Tukey identifica sobre todo valores extremos en la dirección de la cola, que es precisamente donde se concentra la información menos habitual de esa distribución.

### 4.3 Comparación entre grupos

Cuando se compara un diagrama de caja entre varios grupos, conviene resistir la tentación de reducir la comparación a la posición de las medianas. Dos grupos pueden compartir una mediana casi idéntica y diferir sustancialmente en la altura de la caja, es decir, en su dispersión, o en la cantidad de valores marcados como atípicos. Toda esa información está disponible en el gráfico y forma parte de la comparación, no solo la posición de la línea central.

Una limitación práctica de comparar diagramas de caja construidos sobre una variable como `dur`, calculada a nivel de palabra, es la que ya se discutió en la sesión anterior a propósito del nivel de agregación: cada caja se construye sobre decenas de miles de observaciones no independientes entre sí, provenientes de un número mucho menor de participantes. La dispersión visible en el gráfico mezcla la variabilidad entre palabras dentro de un mismo lector con la variabilidad entre lectores distintos, y ambas fuentes de variación no quedan separadas en una representación de este tipo.

### Actividades 4

**4.1** Calcula los límites inferior y superior para valores atípicos de `dur` sobre `fijadas`, siguiendo el criterio de Tukey presentado en la sección 4.2. Indica cuántas observaciones caen fuera de esos límites y qué porcentaje representan sobre el total de palabras fijadas.

**4.2** Construye el diagrama de caja de `dur` separado por `long_grupo`. Verifica antes de graficar que los niveles de `long_grupo` están en el orden esperado, de menor a mayor longitud, con la función `levels()`.

**4.3** Calcula, para cada nivel de `long_grupo`, el número de observaciones marcadas como atípicas según el criterio de la sección 4.2. Presenta el resultado tanto en cantidad absoluta como en proporción sobre el tamaño de cada grupo, e indica cuál de los dos criterios de comparación resulta más informativo para responder si algún grupo de longitud es particularmente propenso a producir tiempos de lectura extremos.

**4.4** Calcula el límite superior de valores atípicos de `dur`, definido en la sección 4.2, por separado para dos lenguas: la de mayor desviación estándar y la de menor desviación estándar, identificadas en la actividad 2.2. Indica si el límite superior difiere entre ambas lenguas en la misma dirección que sus desviaciones estándar.

## 5. Medidas de asociación

Las medidas anteriores describen una variable a la vez. Las medidas de asociación describen la relación entre dos variables, y son el primer paso hacia el análisis bivariado que se desarrollará con mayor profundidad en las próximas sesiones del módulo.

### 5.1 Correlación de Pearson

El coeficiente de correlación de Pearson mide el grado de asociación lineal entre dos variables numéricas:

$$r = \frac{\sum_{i=1}^{n}(x_i - \bar{x})(y_i - \bar{y})}{\sqrt{\sum_{i=1}^{n}(x_i - \bar{x})^2} \sqrt{\sum_{i=1}^{n}(y_i - \bar{y})^2}}$$

```r
cor(fijadas$long_palabra, fijadas$dur, method = "pearson")
```

El coeficiente toma valores entre -1 y 1. Un valor cercano a 1 indica una asociación lineal positiva fuerte, un valor cercano a -1 indica una asociación lineal negativa fuerte, y un valor cercano a 0 indica ausencia de asociación lineal, aunque esto último no descarta la existencia de una asociación no lineal entre las variables.

El coeficiente de Pearson tiene dos limitaciones que conviene tener presentes. Primero, únicamente captura relaciones lineales: una relación en forma de U, por ejemplo, puede producir un coeficiente cercano a 0 pese a que las dos variables estén claramente relacionadas entre sí. Segundo, es sensible a valores extremos, porque su fórmula involucra las mismas distancias a la media, elevadas de forma implícita al multiplicarse entre sí, que ya se discutieron a propósito de la media y la varianza.

### 5.2 Correlación de Spearman

El coeficiente de correlación de Spearman resuelve ambas limitaciones al calcularse no sobre los valores originales de las variables, sino sobre sus rangos, es decir, sobre la posición que ocupa cada observación al ordenar la variable de menor a mayor.

```r
cor(fijadas$long_palabra, fijadas$dur, method = "spearman")
```

Al trabajar con rangos en lugar de valores, el coeficiente de Spearman resulta robusto frente a valores extremos y es capaz de detectar cualquier relación monótona entre las dos variables, no únicamente relaciones lineales. El costo de esta robustez es que, si la relación entre las variables es efectivamente lineal, el coeficiente de Spearman suele ser algo menos informativo que el de Pearson, porque descarta información sobre la magnitud exacta de las observaciones para retener únicamente su orden.

Cuando ambos coeficientes se calculan sobre el mismo par de variables y producen valores similares, es razonable asumir que la relación entre ellas es aproximadamente lineal. Cuando difieren de manera apreciable, esa diferencia es en sí misma informativa: sugiere que existe una asociación monótona más fuerte de lo que el coeficiente de Pearson por sí solo permite apreciar, probablemente debido a la influencia de valores extremos o a una relación de forma no lineal.

### 5.3 La prueba de significancia: cor.test()

La función `cor()` devuelve únicamente el valor del coeficiente. La función `cor.test()` realiza, además, una prueba de hipótesis sobre si la correlación observada en la muestra es distinguible de una correlación nula en la población de la que esa muestra proviene:

```r
cor.test(fijadas$long_palabra, fijadas$dur, method = "pearson")
```

El resultado incluye, entre otros componentes, un intervalo de confianza para el coeficiente y un valor p. El valor p indica la probabilidad de observar una correlación tan extrema como la obtenida, o más extrema, si la correlación real en la población fuera exactamente cero. Un valor p pequeño lleva a rechazar esa hipótesis de correlación nula.

Es necesario advertir sobre una interpretación errónea frecuente de este resultado. Con un número de observaciones tan grande como el de este corpus, del orden de cientos de miles, prácticamente cualquier correlación distinta de cero resultará estadísticamente significativa, incluso si su magnitud es tan pequeña que carece de interés práctico. El valor p informa sobre la existencia de una asociación distinguible del azar; la magnitud del coeficiente informa sobre la fuerza de esa asociación. Ambas piezas de información son necesarias y ninguna sustituye a la otra. Reportar únicamente que una correlación fue "significativa" sin indicar su magnitud es, con muestras de este tamaño, una afirmación de escaso valor informativo.

### 5.4 Prueba de independencia chi-cuadrado

Cuando ambas variables son categóricas, el coeficiente de correlación no es aplicable, porque su cálculo requiere valores numéricos ordenables. La herramienta equivalente para dos variables categóricas es la tabla de contingencia y la prueba de independencia chi-cuadrado.

```r
tabla <- table(meco$skip, meco$long_grupo)
tabla

chisq.test(tabla)
```

La prueba compara las frecuencias observadas en cada celda de la tabla con las frecuencias que se esperarían si las dos variables fueran independientes entre sí. Esas frecuencias esperadas se calculan, para cada celda, como el producto del total de su fila por el total de su columna, dividido por el total general:

$$E_{ij} = \frac{(\text{total fila } i) \times (\text{total columna } j)}{\text{total general}}$$

```r
resultado <- chisq.test(tabla)
resultado$expected
```

El estadístico chi-cuadrado acumula, sobre todas las celdas de la tabla, el cuadrado de la diferencia entre lo observado y lo esperado, ponderado por lo esperado:

$$\chi^2 = \sum_{i,j} \frac{(O_{ij} - E_{ij})^2}{E_{ij}}$$

```r
resultado$statistic
resultado$parameter    # grados de libertad
resultado$p.value
```

Cuanto mayor es la discrepancia entre las frecuencias observadas y las esperadas bajo independencia, mayor es el valor del estadístico, y menor el valor p asociado. Un valor p pequeño indica que la distribución de una variable no es independiente de las categorías de la otra.

La prueba chi-cuadrado requiere que las frecuencias esperadas en cada celda no sean demasiado pequeñas; una convención habitual exige que ninguna frecuencia esperada sea inferior a cinco. Cuando esta condición no se cumple, R emite una advertencia al ejecutar `chisq.test()`, y en ese caso conviene agrupar categorías con pocas observaciones antes de repetir la prueba, en lugar de ignorar la advertencia.

### Actividades 5

**5.1** Calcula la correlación de Pearson y de Spearman entre `nfix` y `dur` sobre `fijadas`. Indica si ambos coeficientes resultan similares o difieren de forma apreciable, y relaciona esa comparación con lo explicado en la sección 5.2 sobre la interpretación de esa diferencia.

**5.2** Ejecuta `cor.test()` entre `long_palabra` y `dur`. Extrae el coeficiente, el intervalo de confianza y el valor p de los componentes del resultado, y redacta una sola frase que reporte los tres de forma conjunta, siguiendo un formato adecuado para un informe de investigación.

**5.3** Construye la tabla de contingencia entre `meco$skip` y `meco$lang`. Ejecuta `chisq.test()` sobre esa tabla y reporta el estadístico, los grados de libertad y el valor p.

**5.4** A partir del resultado de la actividad 5.3, extrae las frecuencias esperadas con `resultado$expected` y calcula la diferencia entre la tabla observada y la tabla esperada, celda por celda. Identifica la lengua donde esa diferencia es mayor en valor absoluto, dentro de la fila correspondiente a las palabras omitidas, y redacta una interpretación de ese resultado.

## 6. Extensión: aplicar las medidas a tus lenguas

Esta parte retoma el subconjunto de dos lenguas que cada estudiante seleccionó al final de la sesión anterior. El objetivo es aplicar sobre ese subconjunto el repertorio completo de medidas presentadas en este apunte, no solo alguna de ellas de manera aislada.

```r
mis_lenguas <- c("es", "fi")     # ajustar a los codigos y lenguas propias
mi_sub <- subset(meco, lang %in% mis_lenguas)
mis_fijadas <- subset(fijadas, lang %in% mis_lenguas)
```

El informe de esta extensión debe incluir, como mínimo, los siguientes elementos, calculados sobre las dos lenguas seleccionadas y presentados de forma comparativa entre ambas:

**Tendencia central.** Media, mediana y, si corresponde a alguna de las variables elegidas, moda, con una justificación explícita de cuál de las tres medidas resulta más adecuada para reportar como resumen principal.

**Dispersión.** Rango intercuartílico y desviación estándar, junto con el coeficiente de variación si se desea comparar la dispersión relativa de más de una variable medida en escalas distintas.

**Posición relativa.** Al menos un percentil de interés propio, distinto de la mediana, con una justificación de por qué ese percentil resulta relevante para la pregunta que se está planteando.

**Diagrama de caja.** Un diagrama de caja que compare las dos lenguas en la variable de interés, con un recuento explícito de los valores atípicos en cada una según el criterio de Tukey.

**Asociación.** Al menos una medida de asociación, coeficiente de correlación o prueba chi-cuadrado según corresponda al tipo de las variables involucradas, con su interpretación acompañada del valor p y de la magnitud del coeficiente, no solo de uno de los dos.

El informe debe retomar, además, las tres advertencias planteadas en la sesión anterior sobre la comparación entre lenguas de este corpus: los tamaños de muestra desiguales entre laboratorios, la falta de identidad exacta entre los materiales traducidos, y la posible incomparabilidad del recuento de caracteres cuando los sistemas de escritura difieren. Cada medida calculada en esta extensión debe leerse a la luz de esas limitaciones, y no de manera aislada como si el corpus no las tuviera.

## 7. Cierre

Cada medida presentada en esta sesión responde a una pregunta específica sobre un conjunto de datos, y ninguna de ellas sustituye a las demás. La media y la mediana pueden ofrecer una imagen distinta del centro de una distribución; el rango intercuartílico y la desviación estándar cuantifican la dispersión de maneras que responden de forma distinta ante los valores extremos; los percentiles permiten fijar umbrales sin recurrir a números arbitrarios; el diagrama de caja resume en un solo gráfico buena parte de esta información, con un criterio explícito y documentado para señalar observaciones inusuales; y las medidas de asociación son el primer paso hacia preguntas sobre cómo se relacionan dos variables entre sí.

A lo largo del apunte aparecieron varias decisiones que, igual que en la sesión anterior, deben quedar documentadas en cualquier análisis: qué medida de tendencia central se reporta y por qué, si se usa la desviación estándar o el coeficiente de variación según se comparen variables en la misma escala o en escalas distintas, en qué percentil se fija un umbral, si se sigue la convención de 1,5 veces el rango intercuartílico para valores atípicos o una convención distinta, y qué coeficiente de correlación se elige según la forma esperada de la relación entre las variables. Ninguna de esas decisiones tiene una única respuesta correcta aplicable a cualquier conjunto de datos, y la calidad de un análisis exploratorio depende, en buena medida, de que esas decisiones se tomen de forma consciente y se comuniquen con claridad.

## Referencias

Tukey, J. W. (1977). *Exploratory Data Analysis*. Addison-Wesley.

Gries, S. Th. (2021). *Statistics for Linguistics with R* (3.ª ed.). Mouton de Gruyter.

Baayen, R. H. (2008). *Analyzing Linguistic Data: A Practical Introduction to Statistics using R*. Cambridge University Press.

Siegelman, N., Schroeder, S., Acartürk, C. et al. (2022). Expanding horizons of cross-linguistic research on reading: The Multilingual Eye-movement Corpus (MECO). *Behavior Research Methods*, 54, 2843-2863.

Datos: <https://osf.io/3527a>