# Sesión 3. Análisis exploratorio de datos de lectura

Módulo de Análisis Exploratorio de Datos, Doctorado en Lingüística.

En la sesión anterior repasamos las estructuras de R sobre datos inventados. Ahora trabajamos con un corpus real, y la pregunta deja de ser cómo funciona una función para pasar a ser qué nos dicen estos datos sobre la lectura.

El apunte tiene dos partes. La primera es un recorrido guiado sobre datos de movimientos oculares de lectura en varias lenguas, que haremos en clase. La segunda es una extensión que cada uno aplicará a un subconjunto de lenguas de su propio interés, repitiendo el análisis. El objetivo de esa segunda parte no es solo practicar: es que el procedimiento quede disponible para sus propias investigaciones.

Una advertencia sobre el formato. A diferencia de la prelectura, aquí casi no se muestran resultados. El código está para ejecutarlo, y los números deben salir de la consola de cada uno. Cuando una pregunta aparece en el texto, es una pregunta genuina cuya respuesta está en los datos.

## 1. El corpus: MECO

MECO, el Corpus Multilingüe de Movimientos Oculares (*Multilingual Eye-movement Corpus*), es un esfuerzo internacional coordinado de laboratorios de seguimiento ocular. Los participantes leen textos en su lengua materna mientras un rastreador infrarrojo de video registra sus movimientos oculares. Es el conjunto de datos de movimientos oculares multilingües más completo disponible, con más de veinte lenguas representadas entre sus distintas versiones.

Los materiales son doce textos expositivos de estilo enciclopédico, traducidos y adaptados a cada lengua. Cada participante lee los doce textos y responde después preguntas de comprensión. Eso significa que la estructura de los datos es la de un diseño cruzado: cada palabra fue leída por muchos participantes, y cada participante leyó muchas palabras.

### 1.1 Por qué este corpus para una sesión de EDA

Tres razones.

Primero, contiene los cuatro tipos de variable simultáneamente. Hay variables nominales (la lengua, el participante, el texto), variables binarias (si una palabra fue omitida, si hubo una regresión hacia ella), variables de conteo (número de fijaciones) y variables continuas (duraciones en milisegundos). Cubre el repertorio completo de herramientas exploratorias sin necesidad de un segundo conjunto de datos.

Segundo, las duraciones de fijación presentan una asimetría marcada. Discutir por qué la media no es un buen resumen deja de ser un ejercicio abstracto y pasa a tener consecuencias verificables.

Tercero, la estructura está anidada: palabras dentro de participantes dentro de lenguas. Eso obliga a decidir a qué nivel se hace cada análisis, y las decisiones tienen consecuencias visibles. Es el problema central del análisis de datos experimentales y aquí aparece de forma natural.

### 1.2 Descarga

Los datos de lectura en lengua materna están disponibles públicamente en OSF:

<https://osf.io/3527a>

Descarga el archivo de medidas por palabra y guárdalo en la carpeta de tu proyecto de RStudio. La navegación en OSF requiere hacerlo desde el navegador; no hay descarga programática directa.

Comprueba que estás en el componente correcto antes de descargar. El proyecto MECO agrupa varios componentes en OSF y los archivos tienen nombres semejantes entre ellos, de modo que es fácil bajar un conjunto de datos distinto del previsto y no notarlo hasta que las columnas no coinciden con las esperadas.

### 1.3 Carga e inspección de la estructura

Los archivos de MECO se distribuyen habitualmente en formato `.rda`, el formato nativo de R. A diferencia de un CSV, un archivo `.rda` contiene objetos con su propio nombre, que hay que averiguar:

```r
antes <- ls()
load("joint_data_trimmed.rda")
setdiff(ls(), antes)      # nombres de los objetos cargados
```

Si el archivo que descargaste es un CSV, la carga es la habitual:

```r
meco <- read.csv("archivo.csv", encoding = "UTF-8")
```

Antes de cualquier análisis, hay que averiguar qué columnas hay. Esto no es un trámite: los nombres de las medidas oculomotoras son numerosos y poco intuitivos, y equivocarse de columna produce resultados plausibles pero falsos.

```r
str(meco)
names(meco)
dim(meco)
```

### 1.4 Las medidas oculomotoras

MECO se preprocesa con el paquete popEye, cuyos nombres de variable son estables entre versiones del proyecto. Las medidas por palabra que usaremos son estas:

| Variable | Contenido |
|---|---|
| `ia` | La palabra, como cadena de texto |
| `ianum` | Posición de la palabra en el texto |
| `subid` | Identificador del participante |
| `lang` | Lengua del participante |
| `itemid` o `trialid` | Identificador del texto |
| `skip` | Si la palabra no recibió ninguna fijación |
| `firstrun.skip` | Si fue omitida durante la primera pasada |
| `nfix` | Número de fijaciones sobre la palabra |
| `refix` | Si fue refijada al menos una vez |
| `reg.in` | Si hubo una regresión hacia la palabra |
| `reg.out` | Si hubo una regresión desde la palabra |
| `firstfix.dur` | Duración de la primera fijación, en milisegundos |
| `firstrun.dur` | Duración de la primera pasada (*gaze duration*) |
| `dur` | Tiempo total de lectura de la palabra |
| `gopast` | Tiempo hasta pasar definitivamente la palabra |

Vale la pena entender la relación entre las tres duraciones antes de analizarlas, porque miden cosas distintas y responden a preguntas distintas.

La duración de la primera fijación captura el procesamiento más temprano: cuánto tiempo se detuvo el ojo la primera vez que aterrizó en la palabra. La duración de primera pasada suma todas las fijaciones consecutivas sobre la palabra antes de abandonarla, de modo que incluye las refijaciones inmediatas. El tiempo total suma todo el tiempo dedicado a la palabra durante la lectura completa, incluyendo las visitas posteriores tras una regresión.

Por construcción, `firstfix.dur` es menor o igual que `firstrun.dur`, que es menor o igual que `dur`. Verificar esa desigualdad es una buena comprobación de que se cargaron las columnas correctas.

Si los nombres de tu archivo difieren de los de la tabla, no reescribas el resto del apunte: identifica la correspondencia una vez y renombra las columnas al inicio del guion.

## 2. Primera inspección y el problema de los faltantes

Cuatro preguntas de inventario:

```r
nrow(meco)                            # observaciones palabra por participante
length(unique(meco$subid))            # participantes
length(unique(meco$lang))             # lenguas
length(unique(meco$itemid))           # textos

table(meco$lang)
```

La tabla por lengua merece atención. Las muestras no son de igual tamaño: el número de participantes varía entre laboratorios. Eso condicionará cualquier comparación posterior y hay que tenerlo presente desde el principio.

```r
# Participantes por lengua, no observaciones
participantes_por_lengua <- tapply(meco$subid, meco$lang,
                                   function(x) length(unique(x)))
sort(participantes_por_lengua)
```

### 2.1 Faltantes informativos

Ahora el punto metodológico central de la sesión.

```r
colSums(is.na(meco[, c("firstfix.dur", "firstrun.dur", "dur")]))
```

Habrá valores faltantes, y muchos. No son un defecto de los datos: **una palabra que fue omitida no tiene duración de fijación porque nunca fue fijada.** El faltante codifica información sustantiva.

Esto es distinto del caso habitual en estadística, donde un faltante suele ser un dato que existía y se perdió. Aquí el faltante y la variable `skip` son dos caras del mismo hecho.

```r
table(meco$skip, is.na(meco$dur))
```

La consecuencia práctica es que hay dos preguntas distintas y no se pueden responder con el mismo cálculo. Preguntar cuánto tiempo se dedica a una palabra exige condicionar en que haya sido fijada. Preguntar con qué probabilidad se omite una palabra exige conservar todas las observaciones.

```r
# Incorrecto si lo que se quiere es la duración típica de una fijación:
mean(meco$dur, na.rm = TRUE)   # ¿sobre qué población está promediando?

# Explícito: solo palabras fijadas
fijadas <- subset(meco, skip == 0)
mean(fijadas$dur)
```

Ambos cálculos pueden ser correctos. Lo que no es correcto es hacerlos sin saber cuál se está haciendo. Usar `na.rm = TRUE` de forma mecánica oculta esa decisión.

### Actividades 2

**2.1** Carga los datos y responde: número de observaciones, de participantes, de lenguas y de textos. ¿Cuántas observaciones tiene en promedio cada participante, y coincide con el número de palabras de los doce textos?

**2.2** Construye la tabla de participantes por lengua y ordénala. ¿Cuál es la lengua con más participantes y cuál con menos? ¿Qué problema plantea esa desigualdad para comparar lenguas?

**2.3** Verifica la relación de orden entre las tres duraciones. Calcula qué proporción de las palabras fijadas cumple que `firstfix.dur <= firstrun.dur <= dur`. Si alguna observación la incumple, examínala.

**2.4** Cruza `skip` con `is.na(dur)` y explica en una frase por qué la asociación es casi perfecta. Identifica las observaciones que no encajan en el patrón y propón una explicación.

## 3. Variables binarias: omisión y regresión

Las medidas oculomotoras binarias son variables nominales, y las herramientas son las mismas que usamos con cualquier variable categórica: tablas de frecuencia, proporciones y gráficos de barras.

```r
table(meco$skip)
round(prop.table(table(meco$skip)) * 100, 2)
```

Si la variable está codificada como 0 y 1, su media es directamente la proporción de unos, de modo que no hace falta calcular la tabla para obtener una tasa.

```r
mean(meco$skip)                # tasa global de omisión
mean(meco$reg.in, na.rm = TRUE)  # tasa de regresiones entrantes
```

Las regresiones, o sacádicos retrógrados, son frecuentes en la lectura: la literatura las sitúa entre el cinco y el veinte por ciento de todos los sacádicos. Comprobar dónde cae este corpus dentro de ese rango es la primera verificación empírica de la sesión.

### 3.1 Comparación entre lenguas

```r
omision_por_lengua <- tapply(meco$skip, meco$lang, mean)
sort(omision_por_lengua)

barplot(sort(omision_por_lengua),
        las = 2, cex.names = 0.8,
        main = "Tasa de omisión por lengua",
        ylab = "Proporción de palabras omitidas")
```

Antes de mirar el resultado, anota tu predicción sobre qué lenguas tendrán las tasas más altas y por qué. La respuesta tiene que ver con la longitud media de palabra, que veremos en la sección siguiente, pero conviene formular la hipótesis antes de tener el dato.

El mismo procedimiento aplica a cualquier medida binaria:

```r
regresion_por_lengua <- tapply(meco$reg.in, meco$lang, mean, na.rm = TRUE)
sort(regresion_por_lengua, decreasing = TRUE)
```

### Actividades 3

**3.1** Calcula la tasa global de omisión y la de regresiones entrantes. Contrasta la segunda con el rango del cinco al veinte por ciento que reporta la literatura.

**3.2** Obtén la tasa de omisión por lengua, ordenada, y su gráfico de barras. ¿Cuál es el rango entre la lengua con mayor y menor tasa?

**3.3** Compara la tasa de omisión global (`skip`) con la de primera pasada (`firstrun.skip`). ¿Cuál es mayor y por qué tiene que ser así necesariamente?

**3.4** Calcula la tasa de refijación (`refix`) y de relectura (`reread`) por lengua. ¿Las lenguas que más omiten son también las que menos refijan? Describe el patrón sin afirmar causalidad.

**3.5** Construye la tabla de contingencia entre `skip` y `reg.in`. Conviértela a proporciones por filas con `margin = 1` e interpreta el resultado.

## 4. Derivar predictores de la palabra

Hasta aquí las variables venían dadas. Ahora las construiremos. Los dos predictores canónicos del comportamiento ocular durante la lectura son la longitud y la frecuencia de la palabra, y el primero se deriva directamente del texto.

### 4.1 Longitud de palabra

```r
meco$long_palabra <- nchar(meco$ia)

summary(meco$long_palabra)
table(meco$long_palabra)
```

La columna `ia` contiene la palabra como cadena de texto, y `nchar()` obtiene de ella una variable numérica nueva. Es el procedimiento básico para construir un predictor a partir de un campo de texto.

Un detalle que importa en un corpus multilingüe. El recuento de caracteres depende de la codificación, y las lenguas con diacríticos frecuentes o con sistemas de escritura no alfabéticos pueden comportarse de forma inesperada. Verifícalo antes de confiar en los promedios:

```r
tapply(meco$long_palabra, meco$lang, mean)
```

Si una lengua muestra una longitud media muy alejada de lo plausible, el problema está probablemente en la codificación y no en la lengua.

### 4.2 Recodificar una variable continua

Muchas preguntas se formulan mejor con una variable agrupada que con la variable continua original. La función `cut()` divide un vector numérico en intervalos etiquetados y devuelve un factor:

```r
meco$long_grupo <- cut(meco$long_palabra,
                       breaks = c(0, 3, 5, 8, Inf),
                       labels = c("muy corta", "corta", "media", "larga"))

table(meco$long_grupo)
class(meco$long_grupo)
levels(meco$long_grupo)
```

Recuerda que los intervalos de `cut()` son abiertos por la izquierda y cerrados por la derecha: una palabra de tres caracteres cae en la primera categoría y una de cuatro en la segunda.

Con la variable agrupada, la relación con la omisión se hace legible de inmediato:

```r
tapply(meco$skip, meco$long_grupo, mean)
```

Este resultado replica uno de los hallazgos más robustos de la investigación sobre lectura: la omisión aumenta para palabras cortas. Vale la pena detenerse en que un análisis de tres líneas sobre datos públicos recupera un efecto establecido en la literatura.

### 4.3 Posición relativa en el texto

Otra variable derivada, útil para detectar efectos de posición:

```r
n_palabras <- tapply(meco$ianum, meco$itemid, max)
meco$pos_relativa <- meco$ianum / n_palabras[as.character(meco$itemid)]

summary(meco$pos_relativa)
```

Presta atención al mecanismo de la última línea. El objeto `n_palabras` es un vector con nombres, y se indexa por el identificador del texto convertido a carácter. La conversión con `as.character()` es necesaria porque los nombres de un vector son siempre cadenas de texto, aunque provengan de valores numéricos.

### Actividades 4

**4.1** Crea la variable de longitud de palabra y obtén su distribución global con `summary()` y un histograma. ¿Es simétrica?

**4.2** Calcula la longitud media de palabra por lengua y ordénala. Verifica que los valores son plausibles y señala cualquier anomalía que sugiera un problema de codificación.

**4.3** Recodifica la longitud en cuatro grupos con `cut()`. Calcula la tasa de omisión por grupo y describe la relación en una frase.

**4.4** Repite el análisis anterior por separado para dos lenguas de longitud media de palabra muy distinta. ¿Se mantiene el patrón en ambas?

**4.5** Construye la posición relativa en el texto. Divídela en cinco tramos con `cut()` y calcula la duración media de lectura en cada uno, sobre palabras fijadas. ¿Hay efectos de inicio o de final de texto?

## 5. Del nivel de la palabra al del participante

Hasta aquí cada fila era una palabra leída por un participante. Muchas preguntas, sin embargo, se formulan sobre el lector: cuán rápido lee, con qué frecuencia regresa, cuánto comprende. Eso requiere agregar (*aggregate*).

### 5.1 La forma de la distribución

Antes de agregar, conviene mirar la distribución de la variable que vamos a resumir.

```r
fijadas <- subset(meco, skip == 0)

hist(fijadas$dur, breaks = 100,
     main = "Distribución del tiempo total de lectura por palabra",
     xlab = "Milisegundos")

mean(fijadas$dur)
median(fijadas$dur)
```

La distribución es fuertemente asimétrica hacia la derecha: muchas palabras con duraciones breves y una cola larga de duraciones muy prolongadas. La media y la mediana difieren de forma sustantiva, y la media está siendo desplazada hacia arriba por los valores de la cola.

El diagrama de caja hace visible el volumen de valores atípicos:

```r
boxplot(fijadas$dur, horizontal = TRUE,
        main = "Tiempo total de lectura por palabra",
        xlab = "Milisegundos")
```

Una transformación logarítmica es la respuesta habitual en la literatura sobre lectura, precisamente por esta razón:

```r
par(mfrow = c(1, 2))
hist(fijadas$dur, breaks = 100, main = "Escala original", xlab = "ms")
hist(log(fijadas$dur), breaks = 100, main = "Escala logarítmica", xlab = "log(ms)")
par(mfrow = c(1, 1))
```

La versión transformada es aproximadamente simétrica. Esto no es un truco cosmético: muchos procedimientos estadísticos suponen simetría de los residuos, y la transformación es lo que hace aplicable ese supuesto. Pero cambia la escala de interpretación, y las conclusiones deben formularse en consecuencia.

### 5.2 Agregación por participante

```r
por_participante <- aggregate(dur ~ subid + lang,
                              data = fijadas,
                              FUN = mean)
names(por_participante)[3] <- "dur_media"

head(por_participante)
nrow(por_participante)     # debe coincidir con el número de participantes
```

Incluir `lang` en la fórmula de agregación conserva la lengua de cada participante, que necesitaremos para comparar. Como cada participante pertenece a una sola lengua, no se crean combinaciones espurias.

Otras medidas por participante:

```r
tasas <- aggregate(cbind(skip, reg.in) ~ subid + lang,
                   data = meco, FUN = mean)

lectores <- merge(por_participante, tasas, by = c("subid", "lang"))
str(lectores)
```

### 5.3 Por qué importa el nivel de agregación

Compara estas dos cifras:

```r
mean(fijadas$dur)                    # promedio sobre palabras
mean(por_participante$dur_media)     # promedio sobre participantes
```

Difieren, y la razón es que la primera pondera cada palabra por igual, mientras la segunda pondera cada participante por igual. Si los participantes leyeron cantidades distintas de palabras fijadas, ambas medidas divergen.

Esto no es una curiosidad aritmética. Es la razón por la que un análisis a nivel de palabra que trate todas las observaciones como independientes está mal especificado: hay muchas observaciones por participante, y no son independientes entre sí. El término técnico es pseudorreplicación, y la solución completa son los modelos de efectos mixtos, que quedan fuera de este módulo. Lo que corresponde en un análisis exploratorio es ser explícito sobre el nivel al que se está trabajando.

### Actividades 5

**5.1** Construye el histograma de `dur` sobre palabras fijadas y calcula media y mediana. Interpreta la diferencia.

**5.2** Repite el histograma con la transformación logarítmica. Compara ambas formas y explica qué se gana y qué se pierde con la transformación.

**5.3** Identifica las veinte observaciones con mayor `dur`. ¿Se concentran en algún participante, texto o lengua? ¿Qué sugiere eso?

**5.4** Agrega por participante la duración media, la tasa de omisión y la tasa de regresión. Verifica que el número de filas coincide con el número de participantes.

**5.5** Compara el promedio de `dur` calculado sobre palabras con el calculado sobre participantes. Explica la diferencia y decide cuál usarías para comparar lenguas.

## 6. Relaciones entre variables

Ahora las preguntas cruzan dos variables. Es el paso del análisis univariado al bivariado, que estructura el resto del módulo.

### 6.1 Una variable numérica por una categórica

```r
boxplot(dur_media ~ lang, data = por_participante,
        las = 2, cex.axis = 0.8,
        main = "Tiempo medio de lectura por lengua",
        xlab = "", ylab = "Milisegundos")
```

Nota que agregamos primero por participante y comparamos después. Hacer el diagrama de cajas directamente sobre las palabras produciría cajas basadas en decenas de miles de observaciones no independientes, con una dispersión que refleja la variabilidad entre palabras y no entre lectores.

```r
medianas <- tapply(por_participante$dur_media, por_participante$lang, median)
sort(medianas)
```

### 6.2 Dos variables numéricas

La relación entre longitud de palabra y tiempo de lectura es el efecto más establecido de la literatura sobre lectura.

```r
long_dur <- aggregate(dur ~ long_palabra, data = fijadas, FUN = median)

plot(long_dur$long_palabra, long_dur$dur,
     pch = 16, type = "b",
     main = "Tiempo de lectura por longitud de palabra",
     xlab = "Caracteres", ylab = "Mediana del tiempo total (ms)")
```

Agregar antes de graficar es una decisión con consecuencias. Un diagrama de dispersión con todas las observaciones sería una nube ilegible de cientos de miles de puntos. Agregando por longitud se ve la tendencia central, al precio de ocultar la dispersión. Ambas cosas importan, de modo que conviene mirar también las distribuciones completas:

```r
boxplot(dur ~ long_palabra,
        data = subset(fijadas, long_palabra <= 15),
        main = "Distribución del tiempo por longitud",
        xlab = "Caracteres", ylab = "Milisegundos")
```

La correlación cuantifica la asociación, pero elige el coeficiente con criterio:

```r
cor(fijadas$long_palabra, fijadas$dur, method = "pearson")
cor(fijadas$long_palabra, fijadas$dur, method = "spearman")
```

El coeficiente de Pearson supone una relación lineal y es sensible a los valores extremos. Con una variable tan asimétrica como la duración, el de Spearman, que trabaja sobre rangos, es más informativo. Que ambos difieran es en sí mismo un dato sobre la forma de la relación.

### 6.3 Interacciones

La pregunta se vuelve más interesante cuando se cruzan tres variables:

```r
omision <- aggregate(skip ~ long_grupo + lang, data = meco, FUN = mean)

lenguas_sel <- c("en", "es", "fi", "he")   # ajustar a los códigos del corpus
sub_om <- subset(omision, lang %in% lenguas_sel)

matriz <- xtabs(skip ~ long_grupo + lang, data = sub_om)
barplot(matriz, beside = TRUE, legend.text = TRUE,
        main = "Tasa de omisión por longitud y lengua",
        ylab = "Proporción omitida")
```

La pregunta que responde este gráfico es si el efecto de la longitud sobre la omisión es igual en todas las lenguas o si su magnitud varía. Ese tipo de pregunta, sobre si un efecto se modula según una tercera variable, es una interacción, y es donde el análisis exploratorio suele resultar más productivo.

### Actividades 6

**6.1** Construye el diagrama de cajas de la duración media por lengua, a nivel de participante. ¿Qué lenguas muestran los tiempos más largos y cuáles la mayor dispersión entre lectores?

**6.2** Grafica la mediana del tiempo de lectura por longitud de palabra. Describe la forma de la relación: ¿es lineal en todo el rango?

**6.3** Calcula la correlación entre longitud y duración con los métodos de Pearson y Spearman. Explica la diferencia entre ambos valores.

**6.4** Construye el gráfico de barras agrupadas de la tasa de omisión por longitud y lengua, para cuatro lenguas. ¿El efecto de la longitud tiene la misma magnitud en todas?

**6.5** Examina si los participantes que leen más rápido regresan menos. Usa la tabla agregada por participante, construye un diagrama de dispersión y calcula la correlación. Describe el patrón **sin afirmar causalidad** y propón al menos una explicación alternativa a la causal.

## 7. Extensión: tus propias lenguas

Todo lo anterior se aplica a cualquier subconjunto del corpus, porque la estructura de los datos es la misma para todas las lenguas.

Esta parte es individual y se entrega junto con las actividades. Elige dos lenguas del corpus y justifica la elección con un criterio explícito: pueden ser lenguas relacionadas con tu investigación, tipológicamente contrastantes, o con sistemas de escritura distintos. El criterio importa porque determina qué comparación tiene sentido: contrastar dos lenguas emparentadas responde a una pregunta distinta que contrastar dos lenguas de morfología muy diferente.

### 7.1 Preparar el subconjunto

```r
mis_lenguas <- c("es", "fi")     # ajustar
mi_sub <- subset(meco, lang %in% mis_lenguas)

table(mi_sub$lang)
length(unique(mi_sub$subid))
```

A partir de aquí, todo el código de las secciones 3 a 6 funciona sin cambios sobre `mi_sub`.

### 7.2 Tres advertencias necesarias

La primera es sobre el tamaño de muestra. Los laboratorios aportaron números distintos de participantes. Si una de tus lenguas tiene treinta lectores y la otra cincuenta, cualquier comparación tiene precisión desigual, y las estimaciones de la muestra menor serán más inestables. Comprueba los tamaños antes de interpretar cualquier diferencia.

La segunda es sobre la comparabilidad de los materiales. Los doce textos fueron traducidos y adaptados, no son idénticos. Una diferencia entre lenguas puede reflejar propiedades de la lengua, propiedades de la traducción concreta, o características de la muestra de lectores de ese laboratorio. Separar esas fuentes no es posible con un análisis exploratorio, y conviene decirlo explícitamente en las conclusiones.

La tercera es sobre los sistemas de escritura. Si comparas lenguas con alfabetos distintos, el recuento de caracteres no mide lo mismo en ambas. La longitud en caracteres de una palabra en hebreo, que no escribe habitualmente las vocales, no es comparable a la de una palabra en finés. Si tu comparación cruza sistemas de escritura, discute esta limitación.

### 7.3 Qué entregar

Un guion de código (*script*) y un informe breve, de no más de dos páginas, con esta estructura:

**Descripción del subconjunto.** Qué lenguas elegiste y por qué, cuántos participantes y observaciones tiene cada una.

**Tres preguntas exploratorias.** Formuladas antes de mirar los resultados, no después.

**Análisis.** Al menos un análisis univariado de una variable categórica o binaria, uno de una variable numérica atendiendo a la forma de su distribución, y un cruce entre dos variables. Con sus gráficos correspondientes.

**Hallazgos.** Qué encontraste, incluyendo lo que no esperabas. Si algo contradijo tu intuición inicial, dilo explícitamente: ese es el resultado más valioso de un análisis exploratorio.

**Limitaciones.** Qué no puedes concluir a partir de estos datos, y qué haría falta para poder concluirlo. Menciona aquí al menos el problema del tamaño de muestra desigual y el de la comparabilidad de los materiales traducidos.

## 8. Cierre

Lo que hicimos en esta sesión responde a una estructura que se repetirá en cualquier análisis exploratorio, con independencia de los datos.

Primero, inventario: qué hay, cuánto hay, qué falta y por qué falta. Segundo, distribuciones univariadas, empezando por las categóricas y binarias y siguiendo por las numéricas, atendiendo siempre a la forma de la distribución antes de resumirla con un solo número. Tercero, construcción de variables derivadas a partir de las disponibles. Cuarto, agregación a otro nivel de análisis, decidiendo explícitamente cuál corresponde a la pregunta. Quinto, relaciones entre variables.

Y a lo largo de todo el proceso, decisiones que hay que documentar. En esta sesión fueron al menos estas: si el análisis se hace sobre todas las palabras o solo sobre las fijadas, si las duraciones se transforman o no, en qué puntos se cortan los grupos de longitud, a qué nivel se agrega antes de comparar y qué coeficiente de correlación se reporta. Ninguna de esas decisiones es obvia y todas afectan los resultados.

La diferencia entre un análisis exploratorio y una serie de gráficos sueltos está, en buena medida, en si esas decisiones quedaron registradas.

## Referencias

Siegelman, N., Schroeder, S., Acartürk, C. et al. (2022). Expanding horizons of cross-linguistic research on reading: The Multilingual Eye-movement Corpus (MECO). *Behavior Research Methods*, 54, 2843-2863.

Siegelman, N. et al. (2025). Wave 2 of the Multilingual Eye-Movement Corpus (MECO): New text reading data across languages. *Scientific Data*.

Schroeder, S. popEye: An R package to analyze eye-tracking data from reading experiments. <https://github.com/sascha2schroeder/popEye>

Repositorio de datos de lectura en lengua materna del proyecto MECO: <https://osf.io/3527a>