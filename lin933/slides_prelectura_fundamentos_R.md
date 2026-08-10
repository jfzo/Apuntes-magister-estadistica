---
title: LIN-933
subtitle: Métodos Cuantitativos Para Psicolingüistica
author: Juan Zamora O.
date: Fundamentos de R para lingüística de corpus
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

## Cómo funciona esta sesión

La prelectura ya cubrió el detalle. Aquí revisamos lo esencial y resolvemos dudas.

Seis bloques, cada uno con:

- Dos láminas de conceptos
- Una lámina de actividades para trabajar en clase

Ten RStudio abierto. Todo lo que aparece se ejecuta.

\note{Encuadre inicial de cinco minutos. Conviene preguntar de entrada quiénes alcanzaron a hacer la prelectura completa y quiénes no, porque eso determina cuánto detenerse en cada bloque. Si más de la mitad no la hizo, conviene ampliar las secciones 1 y 2 y dejar 5 y 6 como trabajo posterior.}

# 1. Nociones centrales

## Objetos, tipos y asignación

Asignación con `<-`. Los nombres distinguen mayúsculas de minúsculas (*case-sensitive*).

```r
frecuencia <- 42
class(frecuencia)
#> [1] "numeric"
```

Tres tipos de datos (*data types*) básicos:

| Tipo | Contenido | Ejemplo |
|---|---|---|
| `numeric` | Números | `42`, `3.14` |
| `character` | Texto entre comillas | `"sustantivo"` |
| `logical` | Valores de verdad | `TRUE`, `FALSE` |

\note{Punto crítico que conviene demostrar en vivo: escribir class(gato) sin comillas y mostrar el error "object not found". Es el error más frecuente de la primera semana y verlo produce más efecto que explicarlo. Segundo punto: TRUE y FALSE en mayúsculas y sin comillas; "TRUE" entrecomillado es texto.}

## Funciones y argumentos

Los argumentos (*arguments*) se pasan por posición o por nombre. Muchos tienen valor predeterminado (*default*).

```r
round(3.14159, digits = 2)
#> [1] 3.14
round(3.14159)          # digits vale 0 por defecto
#> [1] 3
```

Funciones propias:

```r
frec_norm <- function(f, tam_corpus, base = 1000) {
  (f / tam_corpus) * base
}
frec_norm(340, 85000)
#> [1] 4
```

Ayuda con `?round`. La sección *Arguments* es la que más se consulta.

\note{Enfatizar dos cosas. Primera: la función devuelve la última expresión evaluada, no hace falta return(). Segunda: recomendar el uso de proyectos de RStudio en lugar de setwd(), porque ancla el directorio de trabajo y hace el código portable. Este es el hábito que sostiene la reproducibilidad de la Semana 5.}

## Actividades 1

**1.1** Crea tres objetos: tu apellido (`character`), el año de inicio de tu doctorado (`numeric`) y si tu investigación usa corpus (`logical`). Verifica el tipo de cada uno.

**1.2** Escribe una función `ttr()` que reciba número de tipos léxicos (*types*) y de ocurrencias (*tokens*) y devuelva su cociente. Pruébala con 450 tipos y 1200 ocurrencias.

**1.3** Consulta `?mean` y anota para qué sirve el argumento `na.rm`.

\note{Diez minutos. La 1.3 suele generar la primera discusión interesante del curso: por qué R devuelve NA en lugar de ignorar los faltantes por defecto. La respuesta es que un promedio calculado sobre datos incompletos sin que el analista lo sepa es peor que un error visible.}

# 2. Vectores

## Creación, coerción e indexación

Un vector es una secuencia de elementos del mismo tipo. Si se mezclan, R convierte todo al más general sin avisar: es la coerción (*coercion*).

```r
frec <- c(el = 4521, de = 3890, que = 2103, y = 1987)
frec[3]        # por posición
frec["que"]    # por nombre
frec[-1]       # por exclusión
```

La indexación lógica (*logical indexing*) es la forma central:

```r
frec[frec > 2000]
#>   el   de  que
#> 4521 3890 2103
```

\note{Demostrar la coerción en vivo con c(1, 2, "tres") y mostrar que class() devuelve character. Es un error silencioso, no produce advertencia, y por eso hay que verlo. Mencionar también el caso útil: TRUE vale 1, así que sum() sobre un vector lógico cuenta cuántos cumplen la condición.}

## Vectorización y ordenamiento

Las operaciones son vectorizadas (*vectorized*): se aplican elemento a elemento sin bucles.

```r
(frec_abs / 85000) * 1000      # normaliza todo de una vez
```

Comparación: `==`, `!=`, `>`, `<`, `>=`, `<=`, `%in%`
Combinación: `&` (y), `|` (o), `!` (negación)

Dos funciones que se confunden:

- `sort()` devuelve el vector ordenado
- `order()` devuelve los índices que producirían ese orden

\note{El error más común del curso completo es comparar con = en lugar de ==. Vale la pena escribirlo en el pizarrón. Sobre sort y order: order parece inútil ahora, pero es imprescindible para ordenar marcos de datos en la sección 4; conviene anticiparlo para que no parezca gratuito.}

## Actividades 2

**2.1** Crea `pos_freq` con NOUN 1250, VERB 890, ADJ 445, ADV 312, PRON 678. Extrae el tercer elemento, todos menos ADV, y el elemento llamado VERB.

**2.2** Obtén con indexación lógica las etiquetas con frecuencia mayor a 500 y cuenta cuántas son usando `sum()`.

**2.3** Calcula la frecuencia relativa de cada etiqueta como porcentaje del total, redondeada a dos decimales, y grafícala con `barplot()`.

**2.4** Ordena `pos_freq` de mayor a menor y obtén el nombre de la etiqueta más frecuente con `which.max()`.

\note{Quince minutos, es el bloque más largo. La 2.4 tiene una trampa productiva: la mayoría mira el resultado ordenado y escribe el nombre a mano. Insistir en que la solución debe funcionar sin inspección visual, porque en un corpus real no se puede mirar. La respuesta es names(pos_freq)[which.max(pos_freq)].}

# 3. Factores

## Variables categóricas y niveles

Un factor representa variables categóricas. Sus categorías son los niveles (*levels*), ordenados alfabéticamente por defecto.

```r
pos <- factor(c("NOUN", "VERB", "ADJ", "NOUN", "VERB"))
table(pos)
#>  ADJ NOUN VERB
#>    1    2    2
```

- `table()` conserva niveles con frecuencia cero tras filtrar
- `droplevels()` los elimina si estorban
- El argumento `levels` controla el orden en tablas y gráficos

\note{Que table() conserve los niveles vacíos parece un defecto y es una virtud: al filtrar un subcorpus no se pierde la información de qué categorías eran posibles. Mostrar el contraste filtrando y volviendo a tabular.}

## Factores ordinales: la escala se vuelve código

```r
acept <- factor(c("marginal", "aceptable", "inaceptable"),
                levels = c("inaceptable", "marginal", "aceptable"),
                ordered = TRUE)
median(acept)
#> [1] marginal
mean(acept)
#> Warning: argument is not numeric or logical
```

Que la mediana funcione y la media no es la teoría de escalas de medición, verificada por el lenguaje.

**Trampa clásica:** `as.numeric()` sobre un factor devuelve códigos internos.
Usar siempre `as.numeric(as.character(x))`.

\note{Esta es la lámina que más rinde de toda la sesión. Conecta directamente con los fundamentos de muestreo: nominal, ordinal, intervalo, razón. Aquí el error lo produce R y no el profesor, lo que hace la lección memorable. Dedicarle tiempo aunque haya que recortar en otro lado.}

## Actividades 3

**3.1** Crea un factor con pretérito, presente y futuro (seis elementos). Reordena los niveles según la secuencia temporal y compara el `barplot(table(...))` antes y después.

**3.2** Construye un factor ordinal con niveles A1 a C2 del MCER para ocho aprendientes. Calcula la mediana y filtra los de nivel B2 o superior.

**3.3** Crea `puntos <- factor(c(5, 8, 3, 8, 5))`, aplica `as.numeric()` directamente, observa el error y corrígelo hasta que `sum()` devuelva 29.

\note{Doce minutos. La 3.3 debe hacerse en ese orden: primero el error, después la corrección. Si se les da la solución correcta de entrada, no retienen la trampa. El resultado incorrecto es 11; el correcto, 29. Advertir que median() sobre factor ordinal requiere R 4.0 o superior.}

# 4. Marcos de datos

## Estructura e inspección

Un marco de datos (*data frame*) es una tabla: columnas de igual longitud, cada una de un tipo posiblemente distinto.

```r
meta <- data.frame(
  texto  = c("T01", "T02", "T03"),
  genero = c("narrativo", "académico", "narrativo"),
  tokens = c(1250, 3400, 890)
)
str(meta)
```

Al abrir cualquier conjunto de datos, ejecutar siempre `str()`. Complementan `dim()`, `head()` y `summary()`.

\note{Convertir str() en reflejo automático. En una sola salida da dimensiones, nombres, tipos y muestra de valores, que es exactamente lo que se necesita saber antes de tocar nada. Advertir el cambio de R 4.0: el texto ya no se convierte en factor automáticamente, a diferencia de lo que asume Gries y toda la bibliografía anterior a 2020.}

## Filtrado, columnas y agregación

```r
meta[meta$tokens > 2000, ]        # indexación lógica
subset(meta, genero == "narrativo")

meta$ttr <- round(meta$types / meta$tokens, 3)   # columna nueva
meta[order(-meta$tokens), ]                      # ordenar

aggregate(tokens ~ genero, data = meta, FUN = mean)
```

La notación `y ~ x` se lee "y en función de x" y reaparecerá en los modelos estadísticos.

Guardar: `write.csv(..., row.names = FALSE, fileEncoding = "UTF-8")`

\note{Tres advertencias prácticas. La coma en meta[1, ] es obligatoria: sin ella se obtiene la primera columna, no la primera fila. El row.names = FALSE evita la columna espuria de índices. Y los CSV generados en configuración regional española usan punto y coma: read.csv con sep y dec explícitos.}

## Actividades 4

**4.1** Crea un marco de datos `hablantes` con seis filas y columnas id, edad, sexo, ciudad y sujeto_nulo. Inspecciónalo con `str()`.

**4.2** Filtra los menores de 40 años, primero con indexación lógica y luego con `subset()`.

**4.3** Añade una columna `grupo_etario` que valga "joven" bajo los 40 años y "mayor" en caso contrario, usando `ifelse()`.

**4.4** Calcula la media de sujeto_nulo por ciudad con `aggregate()`. Guarda el marco como CSV, recárgalo y verifica con `str()` que los tipos se conservaron.

\note{Quince minutos. La 4.3 usa ifelse() antes de explicarlo formalmente en la sección 6; si alguien pregunta, adelantar que es la versión vectorizada del condicional. La 4.4 es la que produce el descubrimiento sobre factores y codificación: al recargar, las columnas de texto vuelven como character.}

# 5. Listas

## Contenedores heterogéneos

Una lista aloja objetos de cualquier tipo y longitud, incluidos marcos de datos completos.

Distinción central:

- `[ ]` devuelve una **sublista**
- `[[ ]]` devuelve el **contenido** del elemento
- `$nombre` equivale al doble corchete

```r
analisis$frecuencias["que"]      # indexación encadenada
```

\note{Analogía útil: si la lista es un tren, el corchete simple devuelve un vagón que sigue siendo parte del tren, y el doble devuelve lo que hay dentro del vagón. Verificar en vivo con class() sobre ambos resultados, porque la diferencia no se ve en la salida impresa pero sí en el tipo.}

## Por qué importan

Los resultados de las pruebas estadísticas son listas:

```r
resultado <- t.test(grupo_a, grupo_b)
names(resultado)
resultado$p.value
```

Extraer `$p.value` directamente permite automatizar reportes sin copiar números a mano.

Aplicar funciones sin bucles:

```r
sapply(textos, length)     # simplifica a vector
lapply(textos, length)     # devuelve lista
```

\note{Este es el argumento que justifica la sección entera. Sin listas, las pruebas estadísticas son cajas negras cuya salida solo se puede leer. Con listas, sus componentes son accesibles y se pueden encadenar análisis. Mencionar que sapply es lapply más un intento de simplificación: para trabajo interactivo conviene sapply, para código robusto lapply.}

## Actividades 5

**5.1** Ejecuta un `t.test()` entre dos vectores numéricos inventados y extrae de la lista resultante el valor p (*p-value*) y el estadístico t.

**5.2** Escribe una función `describir()` que reciba un vector numérico y devuelva una lista con media, mediana y número de elementos.

**5.3** Crea una lista con cuatro vectores de palabras de distinta longitud y obtén con `sapply()` el número de ocurrencias de cada uno.

\note{Diez minutos. La 5.3 admite una extensión inmediata que vale la pena proponer a quien termine antes: calcular también los tipos léxicos con unique() y de ahí la razón tipo-ocurrencia de cada texto, en una sola línea con una función anónima.}

# 6. Programación elemental

## Condicionales y bucles

`if` evalúa **un solo valor**. Sobre vectores produce error.

Para condiciones elemento a elemento:

```r
ifelse(frec > 100, "alta", "baja")            # dos categorías
cut(frec, breaks = c(0, 50, 300, Inf),
    labels = c("baja", "media", "alta"))      # devuelve un factor
```

Bucle (*loop*) `for`: preasignar el contenedor y recorrer con `seq_along()`.

**Regla general:** si existe versión vectorizada, úsala. `nchar(palabras)` es mejor que un bucle.

\note{El punto de fondo es que los bucles se enseñan porque hay que entender qué ocurre, no porque sean la solución habitual. Reservarlos para procesos que dependen del paso anterior o que leen varios archivos. Advertir sobre while: si nada dentro del cuerpo modifica la condición, el bucle no termina.}

## Búsqueda de patrones

Instrumento central de la lingüística de corpus:

```r
grepl("gat", corpus)                    # devuelve lógicos
grep("gat", corpus)                     # devuelve posiciones
grep("gat", corpus, value = TRUE)       # devuelve los elementos
```

Ambas aceptan expresiones regulares (*regular expressions*) y `ignore.case = TRUE`.

Tres hábitos: comentar el porqué y no el qué, usar nombres descriptivos, fijar la semilla (*seed*) con `set.seed()` siempre que haya azar.

\note{Mostrar la diferencia entre "gat" y "\\\\bgat": el límite de palabra evita coincidencias internas como en "regatear". Es el primer contacto con expresiones regulares, que serán el instrumento principal cuando trabajen con corpus reales. Sobre set.seed: sin ella el análisis no es reproducible, y eso conecta con la Semana 5.}

## Actividades 6

**6.1** Escribe `evaluar_ttr()` que devuelva "alta" sobre 0.5, "media" entre 0.3 y 0.5, y "baja" bajo 0.3. Aplícala a `c(0.62, 0.41, 0.22)` con `sapply()`.

**6.2** Dado `frec <- c(5, 120, 45, 890, 12, 340)`, clasifica con `cut()` en tres niveles: baja (hasta 50), media (51 a 300), alta (sobre 300). Verifica que el resultado es un factor.

**6.3** Con el vector `corpus`, obtén las oraciones que contienen alguna palabra que empiece por "gat" y cuenta cuántas son.

**6.4** Escribe `perfil()` que reciba un vector de oraciones y devuelva una lista con número de oraciones, total de ocurrencias y longitud media por oración.

\note{Quince minutos. La 6.4 integra todo el curso: función propia, strsplit, sapply, lista de retorno. Si el tiempo aprieta, es la que puede quedar como trabajo posterior. En la 6.2, advertir que los intervalos de cut son abiertos por la izquierda: el 50 cae en baja y el 51 en media.}

# Cierre

## Qué deberías poder hacer

- Crear objetos, consultar su tipo y escribir funciones propias
- Indexar vectores por posición, nombre y condición lógica
- Reordenar niveles de un factor y declararlo ordinal
- Filtrar marcos de datos y agregar por grupos
- Extraer componentes de una lista de resultados
- Buscar patrones en texto con `grep()`

Si algo quedó en duda, es el momento de decirlo.

\note{Cierre de cinco minutos. Preguntar explícitamente por los tres puntos que suelen quedar flojos: la diferencia entre corchete simple y doble, la conversión de factores a numérico, y cuándo usar bucle. Si el grupo se ve seguro, se puede saltar directo a la siguiente lámina.}

## Lo que viene

La próxima sesión abre con datos reales, no con sintaxis.

Todo lo de hoy será herramienta, no contenido.

Trae tu script de soluciones y las dudas anotadas.

\note{Cerrar señalando la continuidad: la prelectura y esta sesión son andamiaje. A partir de aquí R desaparece como tema y aparece como instrumento. Recordar el material de referencia: Wickham y Grolemund disponible libremente en r4ds.hadley.nz, y las hojas de referencia de RStudio.}