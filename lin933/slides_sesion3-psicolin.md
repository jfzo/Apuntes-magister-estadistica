---
title: LIIN-933
subtitle: Análisis exploratorio de datos de lectura
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

Usamos una base de datos real (MECO).

Buscaremos explorar qué nos dicen estos datos sobre la lectura.

La idea es ir avanzando juntos en el análisis del conjunto de datos.


# El conjunto de datos
## MECO

Corpus Multilingüe de Movimientos Oculares (*Multilingual Eye-movement Corpus*).

- Esfuerzo internacional coordinado de laboratorios de seguimiento ocular
- Los participantes leen en su lengua materna con registro infrarrojo de video
- Doce textos expositivos, traducidos y adaptados a cada lengua
- Más de veinte lenguas entre sus distintas versiones

Estructura cruzada: cada palabra fue leída por muchos participantes, cada participante leyó muchas palabras.

Datos: <https://osf.io/3527a>

\note{Insistir en la estructura cruzada porque determina todo el bloque 4. Advertir también que el proyecto MECO agrupa varios componentes en OSF con nombres de archivo semejantes: hay que comprobar que se está en el componente correcto antes de descargar, porque bajar el conjunto equivocado no produce un error inmediato sino columnas que no coinciden.}

## Las medidas oculomotoras

| Variable | Contenido |
|---|---|
| `ia`, `ianum` | La palabra y su posición en el texto |
| `subid`, `lang` | Participante y lengua |
| `skip`, `firstrun.skip` | Omisión total y de primera pasada |
| `nfix`, `refix` | Número de fijaciones, refijación |
| `reg.in`, `reg.out` | Regresión hacia y desde la palabra |
| `firstfix.dur` | Duración de la primera fijación |
| `firstrun.dur` | Duración de primera pasada |
| `dur` | Tiempo total de lectura |



\note{Por construcción: `firstfix.dur` $\leq$ `firstrun.dur` $\leq$ `dur`
    Explicar la diferencia entre las tres duraciones antes de analizarlas, porque responden a preguntas distintas: procesamiento temprano, primera pasada completa incluyendo refijaciones inmediatas, y tiempo total incluyendo visitas posteriores tras una regresión. La desigualdad de la última línea es la comprobación de que se cargaron las columnas correctas, y es la actividad 1.2.}

## Carga de datos de Eye-tracking

Los archivos vienen en formato `.rda`, que contiene objetos con su propio nombre:

```r
load("joint_data_trimmed.rda")
```

```r
str(meco); names(meco); dim(meco)

length(unique(meco$subid))     # participantes
length(unique(meco$lang))      # lenguas
table(meco$lang)
```

Las muestras **no** son de igual tamaño: el número de participantes varía entre laboratorios.

\note{El paso de averiguar el nombre del objeto cargado es una operación que no aparece con CSV y suele desconcertar. La desigualdad de tamaños muestrales condiciona toda comparación posterior y conviene señalarla ahora, no cuando aparezca una diferencia entre lenguas que podría ser solo ruido de la muestra menor.}

## Valores Faltantes (*Missing values*)

```r
colSums(is.na(meco[, c("firstfix.dur", "firstrun.dur", "dur")]))
table(meco$skip, is.na(meco$dur))
```

¡No son un defecto! 

**Una palabra omitida no tiene duración porque nunca fue fijada.**

Dos preguntas distintas, dos cálculos distintos:

```r
mean(meco$dur, na.rm = TRUE)        # ¿sobre qué población promedia?
fijadas <- subset(meco, skip == 0)
mean(fijadas$dur)                   # explícito
```

`na.rm = TRUE` usado mecánicamente oculta la decisión.

\note{Este es el punto metodológico central del bloque. En la mayoría de los contextos estadísticos un faltante es un dato que existía y se perdió; aquí el faltante y la variable skip codifican el mismo hecho. Ambos cálculos pueden ser correctos: lo que no es correcto es hacerlos sin saber cuál se está haciendo. Crear el objeto fijadas ahora, porque se usa en los bloques 4 y 5.}

## Actividades del bloque 1


**1.1** Construye la tabla de participantes por lengua y ordénala. ¿Cuál tiene más y cuál menos? ¿Qué problema plantea esa desigualdad para comparar lenguas?

**1.2** Verifica la relación de orden entre las tres duraciones sobre palabras fijadas. Si alguna observación la incumple, examínala.


\note{Ocho minutos. La 1.1 corresponde a la actividad 2.2 del apunte y la 1.2 a la 2.3. En la 1.2, lo interesante no es que la desigualdad se cumpla sino qué hacer si no: una violación indica que se confundió una columna o que el archivo no es el previsto. Es una comprobación que conviene incorporar como rutina.}

# 2. Variables binarias

## Omisión y regresión

Variables codificadas como 0 y 1. Su media es directamente la proporción de unos.

```r
mean(meco$skip)                    # tasa global de omisión
mean(meco$reg.in, na.rm = TRUE)    # tasa de regresiones entrantes
```

Las regresiones son frecuentes en la lectura: la literatura las sitúa entre el cinco y el veinte por ciento de todos los sacádicos.

Comprobar dónde cae este corpus en ese rango es la primera verificación empírica de la sesión.

\note{Que la media de un vector binario sea una proporción ahorra calcular tablas y es el idioma habitual en este tipo de análisis. Sobre el rango de la literatura: pedir que lo comparen antes de seguir, porque si el valor cae muy fuera hay que sospechar de la columna elegida antes que del corpus.}

## Comparación entre lenguas

```r
omision <- tapply(meco$skip, meco$lang, mean)
sort(omision)

barplot(sort(omision), las = 2, cex.names = 0.8,
        main = "Tasa de omisión por lengua",
        ylab = "Proporción de palabras omitidas")
```

¿Qué lenguas esperas en cada extremo?¿por qué?


\note{La explicación tiene que ver con la longitud media de palabra, que construiremos en el bloque siguiente.
    Pedir la predicción por escrito antes de correr el código. La hipótesis razonable es que las lenguas de palabras más largas omitan menos, porque las palabras largas rara vez caben en una sola fijación. Dejar la verificación para el bloque 3, cuando tengan la variable de longitud: así el bloque 2 termina con una pregunta abierta que el siguiente cierra.}

## Actividades del bloque 2

**2.1** Calcula la tasa global de omisión y la de regresiones entrantes. Contrasta la segunda con el rango del cinco al veinte por ciento de la literatura.

**2.2** Compara la tasa de omisión total (`skip`) con la de primera pasada (`firstrun.skip`). ¿Cuál es mayor y por qué tiene que ser así necesariamente?


\note{Siete minutos. La 2.2 tiene una respuesta deducible sin mirar los datos: una palabra omitida en primera pasada puede ser fijada más tarde tras una regresión, de modo que la omisión total es necesariamente menor o igual. Quien lo razone antes de calcular ha entendido la diferencia entre las dos medidas.}

# 3. Longitud de palabra

## Construir un predictor

```r
meco$long_palabra <- nchar(meco$ia)
summary(meco$long_palabra)

tapply(meco$long_palabra, meco$lang, mean)
```

La columna `ia` contiene la palabra como texto

Usndo `nchar()` obtiene de ella una variable numérica.


\note{Este es el procedimiento básico para construir un predictor desde un campo de texto. La advertencia sobre codificación es real: lenguas con diacríticos frecuentes o con sistemas de escritura no alfabéticos pueden producir recuentos inesperados según cómo se guardó el archivo. Verificar la plausibilidad de los promedios es parte del trabajo, no un extra.}

## Recodificar en grupos

```r
meco$long_grupo <- cut(meco$long_palabra,
                       breaks = c(0, 3, 5, 8, Inf),
                       labels = c("muy corta", "corta", "media", "larga"))

table(meco$long_grupo)
tapply(meco$skip, meco$long_grupo, mean)
```

`cut()` devuelve un factor con los niveles ya ordenados. Los intervalos son abiertos por la izquierda: tres caracteres cae en la primera categoría, cuatro en la segunda.


\note{El resultado esperado es que la omisión disminuya monótonamente con la longitud. Vale la pena detenerse en que un análisis de tres líneas sobre datos públicos replica un efecto establecido: es el argumento a favor de trabajar con corpus abiertos. Los puntos de corte son una decisión arbitraria que hay que documentar, y conviene decirlo.}

## Actividades del bloque 3


**3.1** Calcula la longitud media de palabra por lengua y ordénala. Contrástala con la tasa de omisión del bloque 2: ¿se confirma tu predicción?

**3.2** Recodifica la longitud en cuatro grupos y calcula la tasa de omisión por grupo. Describe la relación en una frase.


\note{Siete minutos. La 3.1 cierra la pregunta abierta del bloque 2 y es el momento en que la sesión adquiere continuidad narrativa. Si la predicción de alguien falló, ese es material de discusión más valioso que si acertó: la relación existe pero no es perfecta, porque intervienen la frecuencia de la palabra y las convenciones ortográficas de cada lengua.}

# 4. Asimetría y agregación

## Miremos la "forma" de tiempos de lectura

```r
fijadas <- subset(meco, skip==0)
hist(fijadas$dur, breaks = 100,
     main = "Tiempo total de lectura por palabra", xlab = "ms")

mean(fijadas$dur)
median(fijadas$dur)
```

---

Asimetría marcada hacia la derecha: muchas duraciones breves y una cola larga de duraciones prolongadas.

La media y la mediana difieren de forma sustantiva. La media está siendo desplazada hacia arriba por los valores de la cola.

Debemos mirar la forma antes de resumirla con un número (media, mediana...)

\note{Este es el punto conceptual central de la sesión. Aquí la asimetría es mucho más marcada y las consecuencias más visibles. Pedir que anoten ambos valores: la diferencia entre ellos es el dato, no cada uno por separado.}

## Transformación logarítmica

```r
par(mfrow = c(1, 2))
hist(fijadas$dur, breaks = 100, main = "Escala original", xlab = "ms")
hist(log(fijadas$dur), breaks = 100, main = "Escala log", xlab = "log(ms)")
par(mfrow = c(1, 1))
```

La versión transformada es aproximadamente simétrica.

Cambia la escala de interpretación, y las conclusiones deben formularse en consecuencia.

\note{No es un ajuste cosmético: muchos procedimientos suponen simetría de los residuos, y la transformación es lo que hace aplicable ese supuesto.
    La respuesta habitual en la literatura sobre lectura es transformar. Lo que se gana es la aplicabilidad de los supuestos; lo que se pierde es que una diferencia en escala logarítmica no se lee como una diferencia en milisegundos. Ese intercambio hay que hacerlo explícito en cualquier informe.}

## Agregar por participante

```r
por_part <- aggregate(dur ~ subid + lang, data = fijadas, FUN = mean)
names(por_part)[3] <- "dur_media"

nrow(por_part)        # debe coincidir con el número de participantes
```

Incluir `lang` en la fórmula conserva la lengua de cada participante.

```r
tasas <- aggregate(cbind(skip, reg.in) ~ subid + lang,
                   data = meco, FUN = mean)
lectores <- merge(por_part, tasas, by = c("subid", "lang"))
```

\note{Verificar que el número de filas coincide con el de participantes es la comprobación de que la agregación hizo lo previsto. Nótese que las tasas se calculan sobre meco completo, no sobre fijadas: la tasa de omisión requiere conservar todas las palabras, incluidas las omitidas. Es la decisión del bloque 1 aplicada de nuevo.}

## Por qué importa el nivel (Pseudo-replicación)

```r
mean(fijadas$dur)              # promedio sobre palabras
mean(por_part$dur_media)       # promedio sobre participantes
```

Un análisis a nivel de palabra que trate todas las observaciones como independientes está mal especificado

Hay muchas observaciones por participante y no son independientes.

\note{En un análisis exploratorio lo que corresponde no es resolver el problema sino ser explícito sobre el nivel al que se trabaja. Mencionar los modelos mixtos como el destino, sin desarrollarlos, sitúa el módulo en su lugar: preparamos el terreno para ese tipo de análisis, no lo sustituimos.}

## Actividades del bloque 4


**4.1** Construye el histograma de `dur` sobre palabras fijadas, calcula media y mediana e interpreta la diferencia. Repite con la transformación logarítmica.

**4.2** Agrega por participante la duración media, la tasa de omisión y la tasa de regresión. Verifica que el número de filas coincide con el número de participantes.


\note{Ocho minutos. La 4.2 produce el objeto que se usa en el bloque 5, de modo que conviene asegurarse de que todos lo tengan antes de avanzar. Si alguien obtiene más filas de las esperadas, casi siempre es porque incluyó una variable adicional en la fórmula de agregación.}

# 5. Relaciones entre variables

## Numérica por categórica

```r
boxplot(dur_media ~ lang, data = por_part,
        las = 2, cex.axis = 0.8,
        main = "Tiempo medio de lectura por lengua",
        xlab = "", ylab = "Milisegundos")
```

Agregamos primero por participante y comparamos *después*.

Hacer el diagrama directamente sobre las palabras produciría cajas basadas en decenas de miles de observaciones no independientes, con una dispersión que refleja variabilidad entre palabras y no entre lectores.

\note{Es la aplicación práctica de lo discutido en el bloque 4. Vale la pena mostrar ambas versiones si hay tiempo: la diferencia visual es notable y el diagrama sobre palabras parece más preciso justamente porque es engañoso, con cajas estrechas que sugieren certeza inexistente.}

## Dos variables numéricas

```r
long_dur <- aggregate(dur ~ long_palabra, data = fijadas, FUN = median)
plot(long_dur$long_palabra, long_dur$dur, pch = 16, type = "b",
     xlab = "Caracteres", ylab = "Mediana del tiempo total (ms)")

cor(fijadas$long_palabra, fijadas$dur, method = "pearson")
cor(fijadas$long_palabra, fijadas$dur, method = "spearman")
```

_Pearson_ supone linealidad y es sensible a los extremos. Con una variable tan asimétrica, _Spearman_ es más informativo.

Que ambos difieran es en sí mismo un dato sobre la forma de la relación.

\note{Agregar antes de graficar oculta la dispersión pero hace legible la tendencia; un diagrama con todas las observaciones sería una nube ilegible. Ambas cosas importan, de modo que conviene mirar también el boxplot de dur por longitud, que está en el apunte. La elección del coeficiente es una decisión que hay que reportar.}

## Actividades del bloque 5


**5.1** Construye el diagrama de cajas de la duración media por lengua a nivel de participante. ¿Qué lenguas muestran los tiempos más largos y cuáles la mayor dispersión entre lectores?

**5.2** Elige dos lenguas del corpus ojalá con sistemas de escritura distintos, y repite los análisis.

```r
mis_lenguas <- c("es", "fi")
mi_sub <- subset(meco, lang %in% mis_lenguas)
```

\note{Cuatro minutos, es el bloque más breve. Si el tiempo se agotó, esta actividad puede quedar como demostración del profesor y pasar directamente al cierre. La 6.5 del apunte, sobre si los lectores más rápidos regresan menos, es la más interesante de las pendientes y conviene mencionarla como anticipo del trabajo posterior.}

# Conclusiones

- ¿El análisis se hace sobre todas las palabras o solo sobre las fijadas?
- ¿Se transforman las duraciones o no?
- ¿En qué puntos se cortan los grupos de longitud?
- ¿A qué nivel se agrega antes de comparar?
- ¿Qué coeficiente de correlación se reporta?


\note{Cierre de tres minutos. Cada una de esas decisiones afecta los resultados y ninguna tiene respuesta única correcta. Lo que se exige no es acertar sino documentar. Conecta con la sesión sobre reproducibilidad del final del módulo.}

## Referencias

\footnotesize

- Siegelman, N., Schroeder, S., Acartürk, C. et al. (2022). Expanding horizons of cross-linguistic research on reading: The Multilingual Eye-movement Corpus (MECO). *Behavior Research Methods*, 54, 2843-2863.
- Siegelman, N. et al. (2025). Wave 2 of the Multilingual Eye-Movement Corpus (MECO): New text reading data across languages. *Scientific Data*.
- Schroeder, S. *popEye: An R package to analyze eye-tracking data from reading experiments*. github.com/sascha2schroeder/popEye
- Datos: <https://osf.io/3527a>

\note{La documentación de popEye es la referencia para el significado exacto de cada medida oculomotora, y conviene señalarla para quien vaya a trabajar con estos datos más allá de la sesión.}