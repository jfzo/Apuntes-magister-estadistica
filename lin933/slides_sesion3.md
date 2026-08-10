---
title: LIIN-933
subtitle: Análisis exploratorio morfosintáctico
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

## Agenda

Dejamos los datos inventados. A partir de ahora, corpus real y anotado.

La pregunta cambia: ya no es cómo funciona una función, sino **qué nos dicen estos datos sobre la lengua**.

Dos partes:

- Recorrido guiado sobre el treebank AnCora del español
- Extensión individual: anotar y analizar un texto propio

Ten RStudio abierto. Casi no mostraré resultados: los números salen de tu consola.

\note{Encuadre de cinco minutos. Conviene explicar de entrada por qué las láminas no traen resultados impresos: si los ven antes de ejecutar, dejan de mirar sus propios datos. El objetivo de la sesión no es que reproduzcan cifras sino que las descubran y las interpreten.}

## El arco de la sesión

| Bloque | Análisis | Tipo de variable |
|---|---|---|
| Categorías gramaticales | Univariado | Nominal |
| Rasgos morfológicos | Univariado y cruces | Nominal extraída de texto |
| Nivel oracional | Agregación | Conteo, sesgada |
| Dependencias | Bivariado | Numérica por categórica |

Cada bloque introduce un tipo de variable nuevo. La complejidad crece de forma deliberada.

\note{Mostrar esta tabla ayuda a que no perciban la sesión como una sucesión de recetas. La progresión es la misma de cualquier análisis exploratorio: inventario, distribuciones univariadas, agregación a otro nivel, relaciones entre variables. Vale la pena decirlo explícitamente aquí y repetirlo en el cierre.}

# 1. El corpus

## UD Spanish AnCora

Treebank del español dentro del proyecto Universal Dependencies.

- Texto periodístico y de ficción
- Anotación morfosintáctica **revisada manualmente**
- Versión completa: unas 17.700 oraciones, 547.000 ocurrencias

Trabajaremos con el archivo de desarrollo: 1.650 oraciones, 53.000 ocurrencias. Suficiente y rápido.

```r
url_base <- "https://raw.githubusercontent.com/UniversalDependencies/UD_Spanish-AnCora/master/"
download.file(paste0(url_base, "es_ancora-ud-dev.conllu"),
              destfile = "es_ancora-ud-dev.conllu")
```

\note{La revisión manual es el punto que justifica empezar por AnCora y no por texto anotado automáticamente. Volveremos sobre esto en la sección 7, cuando cada uno anote su propio texto y la calidad de la anotación deje de estar garantizada. Si la descarga automática falla por red institucional, que usen el navegador.}

## El formato CoNLL-U

Una línea por ocurrencia, diez campos separados por tabuladores, oraciones separadas por líneas en blanco.

| Campo | Contenido |
|---|---|
| `token`, `lemma` | Forma del texto y forma de diccionario |
| `upos` | Categoría gramatical universal |
| `feats` | Rasgos morfológicos, separados por barras |
| `head_token_id` | Posición del núcleo del que depende |
| `dep_rel` | Relación de dependencia |

Cuando `head_token_id` vale 0, la ocurrencia es la raíz de la oración.

```r
writeLines(head(readLines("es_ancora-ud-dev.conllu", n = 30)))
```

\note{Vale la pena mirar el archivo crudo una vez antes de cargarlo. Ver los tabuladores, las líneas de comentario con almohadilla y la separación por líneas en blanco hace que la estructura del marco de datos posterior no parezca arbitraria. El detalle del head igual a cero importará en la sección 6: hay que excluir las raíces al calcular distancias.}

## Carga e inventario

```r
library(udpipe)
ancora <- udpipe_read_conllu("es_ancora-ud-dev.conllu")
str(ancora)
```

Cuatro preguntas antes de preguntarle nada a los datos:

```r
nrow(ancora)                          # ocurrencias
length(unique(ancora$sentence_id))    # oraciones
length(unique(ancora$upos))           # categorías
colSums(is.na(ancora))                # faltantes
```

El campo `feats` estará vacío en categorías sin morfología flexiva. Eso no es un error del corpus, es una propiedad del sistema.

```r
table(ancora$upos, is.na(ancora$feats))
```

\note{El último cruce es importante y suele saltarse. Identificar ahora qué categorías carecen de rasgos morfológicos evita interpretar mal un promedio más adelante. Preguntar al grupo qué categorías esperan encontrar sin feats antes de ejecutar la tabla.}

## Actividades 1

**1.1** Carga el corpus y responde: ocurrencias, oraciones, tipos léxicos distintos en `token` y en `lemma`. ¿Por qué difieren los dos últimos, y en qué dirección?

**1.2** Con `table()` sobre `upos`, cuenta las categorías presentes. El inventario oficial de UD tiene diecisiete. ¿Falta alguna? Propón una explicación.

**1.3** Calcula la razón tipo-ocurrencia sobre `token` y sobre `lemma`. ¿Cuál responde mejor a la pregunta por la riqueza léxica?

\note{Diez minutos. La 1.1 tiene respuesta inmediata pero la justificación es lo que interesa: hay más tipos en token que en lemma porque la flexión multiplica las formas. La 1.3 abre la discusión sobre qué mide realmente el TTR y por qué depende del tamaño del texto, algo que retomaremos al hablar de medidas normalizadas.}

# 2. Categorías gramaticales

## Distribución univariada

Variable nominal: tablas de frecuencia y gráficos de barras.

```r
frec_upos <- table(ancora$upos)
round(prop.table(frec_upos) * 100, 2)

barplot(sort(frec_upos, decreasing = TRUE),
        las = 2, cex.names = 0.8,
        main = "Distribución de categorías gramaticales",
        ylab = "Ocurrencias")
```

Ordenar por frecuencia, no alfabéticamente: el orden alfabético no informa nada.

Dos cosas que discutir al ver el gráfico: dónde queda `PUNCT`, y cuán sesgada está la distribución pese a tratarse de un inventario pequeño y cerrado.

\note{La puntuación suele aparecer entre las categorías más frecuentes, lo que obliga a decidir si entra en el análisis. No hay respuesta correcta, pero la decisión debe ser explícita y quedar documentada. Es el primer ejemplo de la sesión de una decisión metodológica que afecta resultados.}

## Densidad léxica

Proporción de palabras de contenido sobre el total.

```r
contenido <- c("NOUN", "VERB", "ADJ", "ADV", "PROPN")
ancora$es_contenido <- ancora$upos %in% contenido
mean(ancora$es_contenido)
```

Recuerda el mecanismo: `%in%` devuelve lógicos, y la media de un vector lógico es la proporción de verdaderos.

La cifra no dice nada en abstracto. Cobra sentido al **comparar** entre textos o registros.

\note{Buen momento para conectar con la prelectura: es el mismo idioma que sum() sobre vector lógico, ahora con mean() en lugar de sum(). Sobre la medida en sí: la densidad léxica es alta en prosa académica y administrativa, baja en conversación espontánea. Anticipar que en la sección 7 podrán compararla entre sus propios textos.}

## Actividades 2

**2.1** Genera la tabla de proporciones de `upos` ordenada de mayor a menor. ¿Qué tres categorías concentran la mayor parte de las ocurrencias?

**2.2** Repite el gráfico excluyendo la puntuación. Compara ambas versiones: ¿cambia la interpretación?

**2.3** Calcula la densidad léxica global, y luego excluyendo `PUNCT` del denominador. ¿Cuál es más comparable con otro corpus?

**2.4** Calcula qué proporción del corpus ocupan `DET` y `ADP` juntos. Comenta el resultado a la luz de la ley de Zipf.

\note{Doce minutos. La 2.3 es la más sustantiva: si un corpus incluye puntuación y otro no, las densidades léxicas no son comparables. Es un problema real al contrastar corpus de distintas fuentes. La 2.4 conecta con lo que veremos sobre distribuciones sesgadas: unas pocas categorías cerradas concentran una fracción enorme del texto.}

# 3. Rasgos morfológicos

## El campo feats

Pares atributo-valor separados por barras verticales:

```
Mood=Ind|Number=Sing|Person=3|Tense=Pres|VerbForm=Fin
```

Presencia de un rasgo, con `grepl()`:

```r
ancora$femenino <- grepl("Gender=Fem", ancora$feats)
table(ancora$femenino)
```

Extraer el **valor**, no solo la presencia, requiere una expresión regular con captura. Lo haremos con una función propia.

\note{Este es el primer problema real de manipulación de datos de la sesión. Conviene mostrar primero grepl, que ya conocen de la prelectura, y desde ahí motivar por qué no basta: saber que algo es femenino es distinto de saber qué valor de género tiene, porque hay más de dos valores posibles en el esquema de UD.}

## Extraer valores

```r
extraer_rasgo <- function(feats, rasgo) {
  patron <- paste0(rasgo, "=([A-Za-z]+)")
  valor <- regmatches(feats, regexpr(patron, feats))
  valor <- sub(paste0(rasgo, "="), "", valor)
  resultado <- rep(NA_character_, length(feats))
  resultado[grepl(patron, feats)] <- valor
  resultado
}

ancora$genero <- extraer_rasgo(ancora$feats, "Gender")
ancora$modo   <- extraer_rasgo(ancora$feats, "Mood")

table(ancora$genero, useNA = "ifany")
```

`useNA = "ifany"` hace visibles los faltantes. Sin él, `table()` los oculta.

Atajo del paquete: `cbind_morphological(ancora, term = "feats")`

\note{Vale la pena haber escrito la función a mano antes de mencionar el atajo. El problema de extraer información estructurada desde un campo de texto reaparece con cualquier corpus sin paquete dedicado. Sobre useNA: ocultar los faltantes en una tabla de frecuencias es una de las formas más fáciles de malinterpretar una distribución.}

## Preguntas específicamente lingüísticas

```r
sust <- subset(ancora, upos == "NOUN")
table(sust$genero, sust$numero)

verbos <- subset(ancora, upos == "VERB")
sort(table(verbos$modo), decreasing = TRUE)
```

**Antes de ejecutar la última línea:** anota tu estimación de la proporción de subjuntivo sobre indicativo.

Después compárala con el dato.

\note{Este es el momento pedagógicamente más valioso del bloque. La estimación intuitiva casi siempre sobrestima el subjuntivo, porque es una forma saliente y muy discutida en la enseñanza. Es el argumento de la primera sesión sobre la intuición lingüística, ahora verificado con un dato propio. Pedir que escriban la cifra en papel antes de correr el código.}

## Actividades 3

**3.1** Extrae `Person` y tabula su distribución en formas finitas (`VerbForm=Fin`). ¿Qué persona domina y qué relación tiene con el tipo de texto?

**3.2** Tabla de contingencia género por número en adjetivos. Conviértela a proporciones por filas con `margin = 1` e interprétala.

**3.3** Proporción de subjuntivo sobre el total de formas con modo marcado. Contrasta con tu estimación previa.

**3.4** Compara la distribución de número entre sustantivos y adjetivos. ¿Son similares? Explica la diferencia si la hay.

**3.5** Tabula `VerbForm` y calcula qué proporción de las formas verbales son no finitas.

\note{Quince minutos, es el bloque más largo. La 3.1 conecta con el género textual: un corpus de prensa favorece la tercera persona. La 3.4 tiene una respuesta interesante: la concordancia hace que las distribuciones se parezcan, pero no son idénticas porque los adjetivos también concuerdan con sujetos que no son sustantivos.}

# 4. Del token a la oración

## Longitud de oración

Muchas preguntas se formulan a nivel de oración, no de ocurrencia. Eso requiere agregar.

```r
long_oracion <- aggregate(token_id ~ sentence_id,
                          data = ancora, FUN = length)
names(long_oracion)[2] <- "n_tokens"

hist(long_oracion$n_tokens, breaks = 40,
     main = "Longitud de oración", xlab = "Ocurrencias")

mean(long_oracion$n_tokens)
median(long_oracion$n_tokens)
```

Mira la forma antes de resumirla con un número. Si media y mediana difieren, la cola está arrastrando la media.

\note{La longitud de oración es una variable de conteo y su distribución está sesgada a la derecha: muchas oraciones cortas y medianas, cola larga de oraciones muy largas. Esta lámina anticipa toda la discusión sobre medidas de tendencia central de la próxima sesión, pero con un dato que ellos acaban de generar.}

## Valores atípicos y composición

```r
boxplot(long_oracion$n_tokens, horizontal = TRUE)

# Inspeccionar el caso extremo
oracion_larga <- long_oracion$sentence_id[which.max(long_oracion$n_tokens)]
paste(subset(ancora, sentence_id == oracion_larga)$token, collapse = " ")
```

Composición gramatical por oración:

```r
comp <- as.data.frame.matrix(table(ancora$sentence_id, ancora$upos))
comp$n_tokens <- rowSums(comp)
comp$ratio_nom_verb <- comp$NOUN / comp$VERB
```

Cuidado: si una oración no tiene verbos, la razón es infinita. Verifícalo antes de promediar.

\note{Inspeccionar los extremos es siempre informativo y aquí tiene una razón concreta: una oración de doscientas ocurrencias puede ser legítima o puede ser un error de segmentación. Distinguirlo requiere leerla. La razón sustantivo sobre verbo separa estilo nominal, propio de prosa académica y administrativa, de estilo verbal, propio de la narración.}

## Actividades 4

**4.1** Calcula longitud media y mediana de oración. Interpreta la diferencia.

**4.2** Histograma de la longitud, y luego el mismo restringido a oraciones de menos de cincuenta ocurrencias. ¿Qué se ve mejor en cada uno?

**4.3** Identifica las cinco oraciones más largas y reconstruye su texto. ¿Son legítimas o hay problemas de segmentación?

**4.4** Calcula la densidad léxica por oración y compara su distribución con la cifra global. ¿Por qué pueden diferir?

**4.5** Razón sustantivo sobre verbo por oración, excluyendo las oraciones sin verbos. Examina las cinco más altas: ¿qué tienen en común?

\note{Quince minutos. La 4.4 encierra un punto sutil: la media de las densidades por oración no equivale a la densidad global, porque las oraciones tienen distinto peso. Es un caso concreto de por qué el nivel de agregación importa. Si alguien pregunta, ese es el fenómeno detrás de la paradoja de Simpson.}

# 5. Relaciones de dependencia

## Distribución de relaciones

La anotación establece qué depende de qué. Esto no está disponible en un corpus etiquetado solo por categoría.

```r
frec_dep <- sort(table(ancora$dep_rel), decreasing = TRUE)
head(frec_dep, 15)
round(prop.table(frec_dep)[1:10] * 100, 2)
```

\note{Antes de mostrar el resultado, pedir que predigan cuáles serán las tres relaciones más frecuentes. La respuesta suele contener det y case, que no son las que primero vienen a la mente porque no son relaciones argumentales, pero son las más numerosas por razones estructurales del español.}

## Distancia de dependencia

Número de posiciones entre una palabra y su núcleo. Medida con respaldo empírico en psicolingüística: distancias mayores implican mayor carga de memoria de trabajo.

```r
ancora$tok_num  <- as.numeric(ancora$token_id)
ancora$head_num <- as.numeric(ancora$head_token_id)

ancora$dist_dep <- ifelse(ancora$head_num == 0, NA,
                          abs(ancora$head_num - ancora$tok_num))

hist(ancora$dist_dep[!is.na(ancora$dist_dep)], breaks = 50,
     main = "Distancia de dependencia", xlab = "Distancia")
```

La distribución es fuertemente asimétrica: casi todas las dependencias son cortas. Ese es el hallazgo que sostiene la hipótesis de minimización de distancia.

\note{Los identificadores vienen como texto y hay que convertirlos: es un error silencioso frecuente, porque abs() sobre character falla con un mensaje poco claro. La exclusión de las raíces con head igual a cero es obligatoria: sin ella se obtienen distancias espurias enormes. Liu (2008) es la referencia si alguien quiere profundizar.}

## El primer análisis bivariado

¿Depende la distancia del tipo de relación?

```r
relaciones <- c("det", "amod", "nsubj", "obj", "obl", "advmod")
sub_rel <- subset(ancora, dep_rel %in% relaciones)

boxplot(dist_dep ~ dep_rel, data = sub_rel,
        main = "Distancia por tipo de relación",
        xlab = "", ylab = "Distancia", las = 2)
```

También la dirección:

```r
ancora$direccion <- ifelse(ancora$head_num > ancora$tok_num,
                           "núcleo a la derecha", "núcleo a la izquierda")
table(ancora$direccion)
```

\note{Este es el primer gráfico de la sesión que cruza una variable numérica con una categórica, y conviene señalarlo como tal: es el paso del análisis univariado al bivariado, que estructura las próximas sesiones. Comparar distribuciones completas con cajas es mejor que comparar medianas sueltas, porque muestra dispersión y atípicos.}

## Actividades 5

**5.1** Diez relaciones más frecuentes con sus proporciones. ¿Cuáles esperabas arriba y cuáles te sorprenden?

**5.2** Distancia media y mediana del corpus. Interpreta la diferencia según la forma de la distribución.

**5.3** Proporción de núcleo a la izquierda frente a la derecha. Relaciónalo con el orden de constituyentes del español.

**5.4** Diagrama de cajas de distancia por tipo de relación. ¿Qué relaciones muestran distancias más largas? Explicación sintáctica.

**5.5** ¿Se relaciona la distancia con la longitud de la oración? Agrega por oración, une con `merge()` y haz un diagrama de dispersión. Describe el patrón **sin afirmar causalidad**.

\note{Quince minutos. La 5.5 es la más completa y la que más se parece a un análisis real: agregación, unión de tablas y visualización bivariada. La advertencia sobre causalidad no es retórica: oraciones largas tienen distancias mayores casi por definición geométrica, lo que no significa que la longitud cause la distancia.}

# 6. Tu propio texto

## Anotar con udpipe

Todo lo anterior funciona sobre cualquier texto en español, porque `udpipe` produce la misma estructura de datos.

```r
# Solo la primera vez
modelo_archivo <- udpipe_download_model(language = "spanish-ancora")
modelo <- udpipe_load_model(modelo_archivo$file_model)

mi_texto <- readLines("mi_texto.txt", encoding = "UTF-8")
anotado <- as.data.frame(udpipe_annotate(modelo, x = mi_texto))

str(anotado)
```

Compara la estructura con `ancora`. Las columnas son las mismas: **todo el código de hoy funciona sin cambios**.

\note{El modelo pesa unos quince megabytes y queda guardado en la carpeta del proyecto, no hace falta descargarlo cada vez. Si van a comparar varios textos, conviene pasarlos como vector con nombres y usar el argumento doc_id, que permite después agregar por documento.}

## La anotación automática tiene errores

En AnCora la anotación fue revisada a mano. En tu texto, no.

- La precisión en categoría gramatical suele ser alta, pero no perfecta
- En dependencias sintácticas es menor
- El modelo se entrenó con prensa y ficción **escritas**

Registros distantes de ese entrenamiento tendrán más errores: habla espontánea, redes sociales, textos históricos.

```r
set.seed(42)
anotado[sample(nrow(anotado), 30), c("token", "lemma", "upos", "dep_rel")]
```

Inspecciona una muestra antes de confiar en cifras agregadas.

\note{Esta lámina es más importante de lo que parece. Varios trabajarán con transcripciones de habla o con textos de registro no estándar, y ahí la tasa de error sube de forma apreciable. No invalida el análisis exploratorio, pero cambia lo que se puede afirmar y debe aparecer en la sección de limitaciones del informe.}

## Qué entregar

Un guion de código y un informe de máximo dos páginas:

- **Descripción del texto**: qué es, de dónde viene, por qué lo elegiste, tamaño
- **Tres preguntas exploratorias**, formuladas **antes** de mirar resultados
- **Análisis**: al menos un univariado categórico, uno numérico y un cruce, con gráficos
- **Hallazgos**: incluyendo lo que no esperabas
- **Limitaciones**: qué no puedes concluir y qué haría falta para concluirlo

Si algo contradijo tu intuición inicial, dilo. Es el resultado más valioso.

\note{Insistir en que las preguntas se formulen antes: es la diferencia entre exploración honesta y selección de resultados favorables, que discutimos en la primera sesión. En limitaciones deben aparecer al menos dos cosas: la calidad de la anotación automática y la representatividad del texto elegido.}

# Cierre

## La estructura que se repite

1. **Inventario**: qué hay, cuánto hay, qué falta
2. **Distribuciones univariadas**: primero categóricas, luego numéricas, mirando la forma antes de resumir
3. **Agregación**: cambiar de nivel de análisis
4. **Relaciones entre variables**

Esta secuencia se aplica a cualquier corpus, con independencia del contenido.

\note{Cerrar señalando que hoy recorrieron el ciclo completo por primera vez. Las próximas sesiones profundizan cada paso, pero la arquitectura ya está. Si alguien pregunta qué cambia con datos que no sean lingüísticos, la respuesta es que nada: cambian las variables, no el procedimiento.}

## Lo que hay que documentar

Decisiones tomadas hoy, ninguna de ellas obvia:

- ¿Entra la puntuación en el análisis?
- ¿Qué hacer con las oraciones sin verbos?
- ¿Qué categorías cuentan como palabras de contenido?
- ¿Se excluyen las raíces al calcular distancias?

> La diferencia entre un análisis exploratorio y una serie de gráficos sueltos está, en buena medida, en si esas decisiones quedaron registradas.

\note{Esta es la idea final de la sesión. Cada decisión afecta los resultados y ninguna tiene respuesta única correcta. Lo que se exige no es acertar, sino documentar. Conecta directamente con la sesión sobre reproducibilidad del final del módulo.}

## Referencias

\footnotesize

- Nivre, J. et al. (2020). Universal Dependencies v2. *Proceedings of LREC 2020*. universaldependencies.org
- Taulé, M., Martí, M. A. y Recasens, M. (2008). AnCora: Multilevel Annotated Corpora for Catalan and Spanish. *LREC 2008*.
- Wijffels, J. (2023). *udpipe*. Paquete de R. bnosac.github.io/udpipe
- Liu, H. (2008). Dependency distance as a metric of language comprehension difficulty. *Journal of Cognitive Science*, 9(2), 159-191.
- Gries, S. Th. (2009). *Quantitative Corpus Linguistics with R*. Routledge.

\note{Liu (2008) es la lectura recomendada para quien quiera profundizar en distancia de dependencia. La documentación de udpipe tiene viñetas con ejemplos que van más allá de lo visto hoy, en particular sobre extracción de colocaciones y de relaciones sintácticas específicas.}