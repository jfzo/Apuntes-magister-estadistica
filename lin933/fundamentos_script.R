# =============================================================
# Soluciones - Prelectura: Fundamentos de R
# Modulo de Analisis Exploratorio de Datos
# Doctorado en Linguistica
#
# Nombre:
# Fecha:
#
# Ejecutar por secciones. En RStudio, Ctrl+Enter corre la linea
# o el bloque seleccionado.
# =============================================================


# --- Seccion 1: Nociones centrales ---------------------------

# 1.1 Tres objetos de tipos distintos

apellido <- "Zamora"
anio_inicio <- 2024
usa_corpus <- TRUE

class(apellido)      # "character"
class(anio_inicio)   # "numeric"
class(usa_corpus)    # "logical"

# Alternativa mas compacta para verificar los tres a la vez:
sapply(list(apellido, anio_inicio, usa_corpus), class)


# 1.2 Funcion type-token ratio

ttr <- function(types, tokens) {
  types / tokens
}

ttr(450, 1200)   # 0.375

# Version con redondeo, util para reportes:
ttr2 <- function(types, tokens, decimales = 3) {
  round(types / tokens, decimales)
}

ttr2(450, 1200)   # 0.375


# 1.3 El argumento na.rm de mean()

?mean

# Respuesta: na.rm es un valor logico con valor predeterminado FALSE.
# Si hay valores faltantes (NA) en el vector, mean() devuelve NA.
# Con na.rm = TRUE los NA se eliminan antes de calcular la media.

x <- c(10, 20, NA, 40)
mean(x)                # NA
mean(x, na.rm = TRUE)  # 23.33333


# --- Seccion 2: Vectores -------------------------------------

# 2.1 Vector de frecuencias POS e indexacion

pos_freq <- c(NOUN = 1250, VERB = 890, ADJ = 445, ADV = 312, PRON = 678)

pos_freq[3]           # tercer elemento: ADJ 445
pos_freq[-4]          # todos menos ADV
pos_freq["VERB"]      # por nombre: VERB 890

# Comprobaciones utiles:
length(pos_freq)      # 5
names(pos_freq)


# 2.2 Indexacion logica y conteo

pos_freq > 500                 # vector logico
pos_freq[pos_freq > 500]       # NOUN, VERB, PRON
sum(pos_freq > 500)            # 3

# Por que funciona sum(): TRUE vale 1 y FALSE vale 0,
# de modo que la suma cuenta los TRUE.


# 2.3 Frecuencias relativas y grafico

pos_pct <- round(pos_freq / sum(pos_freq) * 100, 2)
pos_pct
# NOUN  VERB   ADJ   ADV  PRON
# 35.31 25.14 12.57  8.81 19.15   (aprox.)

sum(pos_pct)   # cercano a 100

barplot(pos_pct,
        main = "Distribucion de etiquetas POS",
        ylab = "Porcentaje del total",
        xlab = "Etiqueta",
        col  = "steelblue",
        las  = 1)


# 2.4 Ordenamiento y etiqueta mas frecuente

sort(pos_freq, decreasing = TRUE)

# Nombre de la etiqueta mas frecuente, sin inspeccion visual:
names(pos_freq)[which.max(pos_freq)]   # "NOUN"

# Alternativa equivalente:
names(sort(pos_freq, decreasing = TRUE))[1]


# --- Seccion 3: Factores -------------------------------------

# 3.1 Factor de tiempo verbal y reordenamiento de niveles

tiempo <- factor(c("preterito", "presente", "futuro",
                   "presente", "preterito", "presente"))

levels(tiempo)        # orden alfabetico: futuro, presente, preterito
table(tiempo)

barplot(table(tiempo), main = "Orden alfabetico (predeterminado)")

# Reordenar segun la secuencia temporal:
tiempo <- factor(tiempo, levels = c("preterito", "presente", "futuro"))

levels(tiempo)        # ahora en orden temporal
table(tiempo)

barplot(table(tiempo), main = "Orden temporal")

# Los datos no cambiaron: solo el orden de las categorias.
# Eso afecta a la lectura de la tabla y al orden de las barras.


# 3.2 Factor ordinal con niveles del MCER

niveles_mcer <- c("A1", "A2", "B1", "B2", "C1", "C2")

nivel <- factor(c("B1", "A2", "C1", "B2", "A1", "B1", "C2", "B2"),
                levels  = niveles_mcer,
                ordered = TRUE)

nivel
# Levels: A1 < A2 < B1 < B2 < C1 < C2

median(nivel)   # B2

# Filtrar B2 o superior. La comparacion funciona porque el factor
# es ordinal; sobre un factor sin ordenar daria error.
nivel[nivel >= "B2"]     # B2, C1, C2, B2
sum(nivel >= "B2")       # 4

# Verificar que la media no es aplicable:
mean(nivel)              # NA con warning


# 3.3 La trampa de as.numeric() sobre factores

puntos <- factor(c(5, 8, 3, 8, 5))

# Conversion incorrecta: devuelve los codigos internos de los niveles
as.numeric(puntos)                    # 2 3 1 3 2
sum(as.numeric(puntos))               # 11, resultado erroneo

# Conversion correcta: pasando primero por character
as.numeric(as.character(puntos))      # 5 8 3 8 5
sum(as.numeric(as.character(puntos))) # 29


# --- Seccion 4: Marcos de datos ------------------------------

# 4.1 Construccion e inspeccion

hablantes <- data.frame(
  id          = c("H01", "H02", "H03", "H04", "H05", "H06"),
  edad        = c(24, 37, 52, 45, 29, 61),
  sexo        = c("F", "M", "F", "M", "F", "M"),
  ciudad      = c("Valparaiso", "Santiago", "Valparaiso",
                  "Concepcion", "Santiago", "Concepcion"),
  sujeto_nulo = c(0.72, 0.68, 0.61, 0.65, 0.74, 0.58)
)

str(hablantes)
dim(hablantes)
summary(hablantes)


# 4.2 Filtrado de menores de 40

# Con indexacion logica:
hablantes[hablantes$edad < 40, ]

# Con subset(), que evita repetir el nombre del marco de datos:
subset(hablantes, edad < 40)

# Verificar que ambos dan lo mismo:
identical(hablantes[hablantes$edad < 40, ],
          subset(hablantes, edad < 40))   # TRUE


# 4.3 Columna calculada con ifelse()

hablantes$grupo_etario <- ifelse(hablantes$edad < 40, "joven", "mayor")

hablantes
table(hablantes$grupo_etario)   # joven 3, mayor 3


# 4.4 Agregacion, guardado y recarga

# Media de sujeto nulo por ciudad:
aggregate(sujeto_nulo ~ ciudad, data = hablantes, FUN = mean)

# Por ciudad y sexo simultaneamente:
aggregate(sujeto_nulo ~ ciudad + sexo, data = hablantes, FUN = mean)

# Guardar. row.names = FALSE evita una columna espuria de indices.
write.csv(hablantes, "hablantes.csv",
          row.names = FALSE, fileEncoding = "UTF-8")

# Recargar y comparar estructura:
hablantes2 <- read.csv("hablantes.csv", encoding = "UTF-8")

str(hablantes)
str(hablantes2)

# Observacion: desde R 4.0 las columnas de texto se leen como
# character, no como factor. Si se necesitan factores hay que
# convertirlos de forma explicita:
hablantes2$ciudad <- factor(hablantes2$ciudad)
hablantes2$sexo   <- factor(hablantes2$sexo)

str(hablantes2)


# --- Seccion 5: Listas ---------------------------------------

# 5.1 Extraer componentes de un test estadistico

grupo_a <- c(12, 15, 9, 22, 18, 14, 11)
grupo_b <- c(19, 24, 17, 28, 25, 21, 20)

resultado <- t.test(grupo_a, grupo_b)

resultado              # salida impresa habitual
names(resultado)       # componentes disponibles en la lista

resultado$p.value      # valor p
resultado$statistic    # estadistico t
resultado$parameter    # grados de libertad
resultado$conf.int     # intervalo de confianza

# Uso practico: reportar sin copiar numeros a mano.
cat("t =", round(resultado$statistic, 3),
    ", gl =", round(resultado$parameter, 2),
    ", p =", format.pval(resultado$p.value, digits = 3), "\n")


# 5.2 Funcion que devuelve una lista

describir <- function(x) {
  list(
    media    = mean(x),
    mediana  = median(x),
    desv_est = sd(x),
    n        = length(x)
  )
}

d <- describir(c(23, 45, 12, 67, 34, 89, 21))

d              # la lista completa
d$media        # 41.57143
d$n            # 7


# 5.3 Aplicar una funcion a cada elemento de una lista

textos <- list(
  t1 = c("el", "gato", "come", "el", "pescado"),
  t2 = c("la", "casa", "es", "grande"),
  t3 = c("un", "perro", "corre", "por", "el", "parque", "verde"),
  t4 = c("llueve")
)

# Numero de ocurrencias (tokens) de cada texto:
sapply(textos, length)          # 5 4 7 1

# Numero de tipos lexicos (types), con unique():
sapply(textos, function(x) length(unique(x)))   # 4 4 7 1

# Razon tipo-ocurrencia de cada texto:
sapply(textos, function(x) round(length(unique(x)) / length(x), 3))


# --- Seccion 6: Programacion elemental -----------------------

# 6.1 Funcion con condicionales y aplicacion vectorizada

evaluar_ttr <- function(valor) {
  if (valor > 0.5) {
    "alta"
  } else if (valor >= 0.3) {
    "media"
  } else {
    "baja"
  }
}

# if evalua un solo valor, de modo que sobre un vector
# hay que aplicar la funcion elemento a elemento:
sapply(c(0.62, 0.41, 0.22), evaluar_ttr)    # "alta" "media" "baja"

# Pruebas de los limites:
evaluar_ttr(0.50)   # "media"
evaluar_ttr(0.30)   # "media"
evaluar_ttr(0.29)   # "baja"


# 6.2 Clasificacion en tres niveles con cut()

frec <- c(5, 120, 45, 890, 12, 340)

categoria <- cut(frec,
                 breaks = c(0, 50, 300, Inf),
                 labels = c("baja", "media", "alta"))

categoria
# baja media baja alta baja alta

class(categoria)    # "factor"
levels(categoria)   # "baja" "media" "alta", ya en orden

table(categoria)

# Nota: los intervalos de cut() son abiertos por la izquierda y
# cerrados por la derecha. El valor 50 cae en "baja" y el 51 en
# "media". Con right = FALSE se invierte ese comportamiento.


# 6.3 Busqueda de patrones en un vector de texto

corpus <- c("El gato duerme",
            "La casa grande",
            "Los gatos son independientes")

# Oraciones que contienen alguna palabra que empieza por "gat".
# \\b marca limite de palabra, de modo que no coincidiria con
# una palabra que contenga "gat" en posicion interna.
grepl("\\bgat", corpus)                     # TRUE FALSE TRUE
grep("\\bgat", corpus, value = TRUE)        # las dos oraciones
sum(grepl("\\bgat", corpus))                # 2

# Comparacion: sin el limite de palabra el resultado seria
# el mismo aqui, pero no en un corpus con palabras como
# "delgatado" o "regatear".
grep("gat", corpus, value = TRUE)


# 6.4 Funcion de perfil de un conjunto de oraciones

perfil <- function(oraciones) {
  # strsplit() devuelve una lista con un vector de palabras
  # por cada oracion
  palabras_por_oracion <- strsplit(oraciones, " ")
  longitudes <- sapply(palabras_por_oracion, length)

  list(
    n_oraciones    = length(oraciones),
    n_tokens       = sum(longitudes),
    long_media     = round(mean(longitudes), 2),
    oracion_larga  = oraciones[which.max(longitudes)]
  )
}

p <- perfil(corpus)

p$n_oraciones     # 3
p$n_tokens        # 11
p$long_media      # 3.67
p$oracion_larga   # "Los gatos son independientes"

p                 # la lista completa


# --- Comprobaciones ------------------------------------------
# Ejecutar este bloque al final. Si todo esta correcto,
# no debe aparecer ningun mensaje de error.

stopifnot(
  ttr(450, 1200) == 0.375,
  sum(pos_freq > 500) == 3,
  names(pos_freq)[which.max(pos_freq)] == "NOUN",
  sum(as.numeric(as.character(puntos))) == 29,
  sum(nivel >= "B2") == 4,
  nrow(subset(hablantes, edad < 40)) == 3,
  describir(c(23, 45, 12, 67, 34, 89, 21))$n == 7,
  all(sapply(textos, length) == c(5, 4, 7, 1)),
  sapply(c(0.62, 0.41, 0.22), evaluar_ttr)[1] == "alta",
  sum(grepl("\\bgat", corpus)) == 2,
  perfil(corpus)$n_tokens == 11
)

cat("Todas las comprobaciones pasaron correctamente.\n")


# --- Limpieza opcional ---------------------------------------
# Elimina el archivo CSV generado en la actividad 4.4.
# Descomentar si se desea:

# file.remove("hablantes.csv")