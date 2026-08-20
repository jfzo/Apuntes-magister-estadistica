# =============================================================
# Semana 3 - Medidas estadisticas y resumen de datos
# Modulo de Analisis Exploratorio de Datos
# Doctorado en Linguistica
#
# Continuacion de la sesion sobre el corpus MECO.
# Este guion reune el codigo de demostracion de las laminas y
# las soluciones de sus actividades, numeradas por bloque.
#
# Nombre:
# Fecha:
# =============================================================


# =============================================================
# 0. PREPARACION: recuperar los objetos de la sesion anterior
# =============================================================

load("joint_data_trimmed.rda")   # ajustar al nombre real del archivo
meco <- get(ls()[1])             # ajustar al nombre del objeto cargado

meco$long_palabra <- nchar(meco$ia)
meco$long_grupo <- cut(meco$long_palabra,
                       breaks = c(0, 3, 5, 8, Inf),
                       labels = c("muy corta", "corta",
                                  "media", "larga"))

fijadas <- subset(meco, skip == 0)

# Verificacion de continuidad con la sesion anterior:
nrow(fijadas)
length(unique(meco$lang))


# =============================================================
# 1. MEDIDAS DE TENDENCIA CENTRAL
# =============================================================

# --- DEMO ------------------------------------------------------

mean(fijadas$dur)
median(fijadas$dur)

# R no tiene funcion incorporada para la moda.
moda <- function(x) {
  tabla <- table(x)
  as.numeric(names(tabla)[tabla == max(tabla)])
}

moda(fijadas$long_palabra)

mean(fijadas$dur) - median(fijadas$dur)


# --- SOLUCION 1.1 -----------------------------------------------
# Media, mediana y moda de nfix.

media_nfix   <- mean(fijadas$nfix)
mediana_nfix <- median(fijadas$nfix)
moda_nfix    <- moda(fijadas$nfix)

round(c(media = media_nfix, mediana = mediana_nfix), 2)
moda_nfix

# Interpretacion: nfix es una variable de conteo con rango
# reducido, de modo que la moda suele coincidir con el valor mas
# bajo posible entre las palabras fijadas, que es 1. La mayoria
# de las palabras reciben una sola fijacion, y por eso media y
# mediana tienden a estar cerca de ese valor, aunque la media
# queda algo por encima debido a las palabras con varias
# fijaciones.


# --- SOLUCION 1.2 -----------------------------------------------
# Media y mediana de dur por lengua, y donde difieren mas.

media_lengua   <- tapply(fijadas$dur, fijadas$lang, mean)
mediana_lengua <- tapply(fijadas$dur, fijadas$lang, median)

tabla_centrales <- data.frame(
  lengua  = names(media_lengua),
  media   = round(as.numeric(media_lengua), 1),
  mediana = round(as.numeric(mediana_lengua), 1)
)
tabla_centrales$diferencia <- tabla_centrales$media -
                              tabla_centrales$mediana

tabla_centrales[order(-tabla_centrales$diferencia), ]

# Lengua con la mayor diferencia:
tabla_centrales$lengua[which.max(tabla_centrales$diferencia)]

# Interpretacion: una diferencia mayor entre media y mediana
# indica una cola mas larga de duraciones extremas en esa
# lengua, no necesariamente una lectura mas lenta en general.
# Dos lenguas pueden compartir mediana y diferir en cuanto
# elevan la media unos pocos valores muy prolongados.


# --- SOLUCION 1.3 -----------------------------------------------
# Diferencia entre media y mediana como proporcion de la mediana.

media_global   <- mean(fijadas$dur)
mediana_global <- median(fijadas$dur)

diferencia_relativa <- (media_global - mediana_global) /
                        mediana_global

round(diferencia_relativa * 100, 2)   # como porcentaje

# Interpretacion: una diferencia relativa grande, del orden de
# varias decenas por ciento, confirma numericamente lo que ya se
# observaba en el histograma de la sesion anterior: la
# distribucion de dur esta lejos de ser simetrica. Este numero
# se retoma en el bloque 2 al calcular medidas de dispersion.



# =============================================================
# 2. MEDIDAS DE POSICION RELATIVA
# =============================================================

# --- DEMO ------------------------------------------------------

quantile(fijadas$dur, probs = c(0.10, 0.25, 0.50, 0.75, 0.90))
quantile(fijadas$dur, probs = seq(0, 1, by = 0.1))

umbral_90 <- quantile(fijadas$dur, probs = 0.90)
umbral_90

fijadas$lectura_lenta <- fijadas$dur > umbral_90
mean(fijadas$lectura_lenta)


# --- SOLUCION 2.1 -----------------------------------------------
# Percentiles de long_palabra sobre meco.

percentiles_long <- quantile(meco$long_palabra,
                             probs = c(0.10, 0.25, 0.50, 0.75, 0.90))
percentiles_long

p90_long <- percentiles_long["90%"]
p90_long

# Interpretacion: el percentil 90 de long_palabra es el valor de
# longitud por debajo del cual se encuentra el noventa por
# ciento de las palabras del corpus. En terminos simples: solo
# una de cada diez palabras tiene esa longitud en caracteres o
# mas. Es una forma de expresar que tan larga es una palabra
# "larga" para este conjunto de textos, sin recurrir a un
# numero de caracteres fijado de antemano.


# --- SOLUCION 2.2 -----------------------------------------------
# Proporcion de palabras largas segun el percentil 90.

meco$palabra_larga <- meco$long_palabra >= p90_long

proporcion_larga <- mean(meco$palabra_larga)
round(proporcion_larga * 100, 2)

# Interpretacion: el resultado deberia acercarse a diez por
# ciento por construccion, pero no coincide de forma exacta.
# La razon es que long_palabra es una variable discreta con
# muchos valores repetidos: si varias palabras comparten
# exactamente la longitud del percentil 90, todas quedan
# incluidas en el grupo "larga" a la vez, lo que puede desplazar
# la proporcion observada por encima del diez por ciento
# teorico. Esto no ocurre con variables continuas como dur, que
# rara vez tienen empates exactos en el valor de corte.


# --- SOLUCION 2.3 -----------------------------------------------
# Percentil correspondiente a una duracion de 300 ms.

funcion_distribucion <- ecdf(fijadas$dur)

percentil_300 <- funcion_distribucion(300)
round(percentil_300 * 100, 2)

# Interpretacion: el resultado indica que porcentaje de las
# palabras fijadas tuvo un tiempo total de lectura igual o
# menor a 300 milisegundos. Redactado como frase: "una duracion
# de 300 ms corresponde aproximadamente al percentil [valor]
# de la distribucion de tiempos de lectura", lo que significa
# que esa duracion esta por encima (o por debajo, segun el
# resultado) de la mayoria de las observaciones del corpus.
#
# ecdf() es la operacion inversa de quantile(): quantile() va
# de una proporcion a un valor, y ecdf() va de un valor a una
# proporcion.


# =============================================================
# 3. MEDIDAS DE DISPERSION
# =============================================================

# --- DEMO ------------------------------------------------------

max(fijadas$dur) - min(fijadas$dur)
IQR(fijadas$dur)
quantile(fijadas$dur, probs = c(0.25, 0.75))

var(fijadas$dur)
sd(fijadas$dur)
sqrt(var(fijadas$dur)) == sd(fijadas$dur)

cv <- function(x) sd(x) / mean(x) * 100

cv(fijadas$dur)
cv(fijadas$long_palabra)


# --- SOLUCION 3.1 -----------------------------------------------
# Rango, RIC, varianza y desviacion estandar de dur.

rango_dur <- max(fijadas$dur) - min(fijadas$dur)
ric_dur   <- IQR(fijadas$dur)
var_dur   <- var(fijadas$dur)
sd_dur    <- sd(fijadas$dur)

tabla_dispersion <- data.frame(
  medida = c("rango", "RIC", "varianza", "desviacion estandar"),
  valor  = round(c(rango_dur, ric_dur, var_dur, sd_dur), 2)
)
tabla_dispersion

# Interpretacion: el rango suele ser mucho mayor que el RIC en
# proporcion, porque unos pocos valores extremos lo determinan
# por completo. El RIC describe la dispersion del cincuenta por
# ciento central sin verse afectado por esos extremos. La
# varianza esta en milisegundos al cuadrado, unidad sin
# interpretacion directa; por eso se reporta la desviacion
# estandar, que vuelve a la escala original.


# --- SOLUCION 3.2 -----------------------------------------------
# Desviacion estandar de dur por lengua.

sd_por_lengua <- tapply(fijadas$dur, fijadas$lang, sd)
round(sort(sd_por_lengua), 2)

names(which.max(sd_por_lengua))   # mayor dispersion
names(which.min(sd_por_lengua))   # menor dispersion

# Contraste con la media por lengua, para comprobar si van
# de la mano:
comparacion_sd <- data.frame(
  lengua = names(media_lengua),
  media  = round(as.numeric(media_lengua), 1),
  sd     = round(as.numeric(sd_por_lengua), 1)
)
comparacion_sd[order(-comparacion_sd$sd), ]

# Interpretacion: la lengua con mayor desviacion estandar no
# tiene que coincidir con la de mayor media. Una lengua puede
# tener lectores relativamente rapidos en promedio pero con
# mucha variabilidad entre ellos, y otra puede ser mas lenta en
# promedio con lectores mas homogeneos entre si. Conviene
# verificar esta posible disociacion en lugar de asumir que
# ambas medidas coinciden.


# --- SOLUCION 3.3 -----------------------------------------------
# Coeficiente de variacion de dur y de long_palabra.

cv_dur    <- cv(fijadas$dur)
cv_long   <- cv(fijadas$long_palabra)

round(c(dur_ms = cv_dur, long_palabra_car = cv_long), 2)

cv_dur > cv_long

# Interpretacion: al ser un coeficiente adimensional, ambos
# valores son comparables aunque las variables esten en
# unidades distintas, milisegundos y caracteres. Se espera que
# dur presente un coeficiente de variacion sensiblemente mayor,
# porque su distribucion es muy asimetrica con una cola de
# valores extremos, mientras que la longitud de palabra varia
# en un rango mucho mas acotado.


# --- SOLUCION 3.4 -----------------------------------------------
# Coeficiente de variacion de dur por lengua.

cv_por_lengua <- tapply(fijadas$dur, fijadas$lang, cv)
round(sort(cv_por_lengua, decreasing = TRUE), 2)

# Interpretacion: ordenar de mayor a menor permite identificar
# en que lenguas la dispersion relativa de los tiempos de
# lectura es mas pronunciada. Una lengua con CV alto tiene
# lectores muy heterogeneos entre si en relacion con su propia
# media, independientemente de si esa media es alta o baja.


# =============================================================
# 4. DIAGRAMA DE CAJA Y BIGOTES
# =============================================================

# --- DEMO ------------------------------------------------------

boxplot(fijadas$dur,
        main = "Tiempo total de lectura por palabra",
        ylab = "Milisegundos")

boxplot(dur ~ lang, data = fijadas,
        las = 2, cex.axis = 0.8,
        main = "Tiempo de lectura por lengua",
        ylab = "Milisegundos")

Q1  <- quantile(fijadas$dur, 0.25)
Q3  <- quantile(fijadas$dur, 0.75)
RIC <- Q3 - Q1

limite_inferior <- Q1 - 1.5 * RIC
limite_superior <- Q3 + 1.5 * RIC
c(limite_inferior, limite_superior)


# --- SOLUCION 4.1 -----------------------------------------------
# Limites de valores atipicos y conteo.

atipicos <- subset(fijadas,
                   dur < limite_inferior | dur > limite_superior)

nrow(atipicos)
round(nrow(atipicos) / nrow(fijadas) * 100, 2)

# El limite inferior suele ser negativo con esta distribucion,
# lo cual no elimina observaciones por ese lado porque las
# duraciones no pueden ser negativas:
limite_inferior < 0

sum(fijadas$dur < limite_inferior)   # deberia ser 0 si el limite es negativo
sum(fijadas$dur > limite_superior)   # atipicos por el lado superior

# Interpretacion: dado que la distribucion de dur esta sesgada
# hacia la derecha, practicamente todos los valores atipicos
# detectados por este criterio se ubican por encima del limite
# superior. El limite inferior, al resultar negativo, no
# excluye ninguna observacion real. Esto es consistente con lo
# discutido en el bloque 1 sobre la asimetria de la variable.


# --- SOLUCION 4.2 -----------------------------------------------
# Diagrama de caja de dur por grupo de longitud, ordenado.

# cut() ya devuelve los niveles en el orden correcto si los
# breaks se dieron de forma ascendente, de modo que no hace
# falta reordenar el factor.
levels(fijadas$long_grupo)

boxplot(dur ~ long_grupo, data = fijadas,
        main = "Tiempo de lectura por grupo de longitud",
        xlab = "", ylab = "Milisegundos")


# --- SOLUCION 4.3 -----------------------------------------------
# Grupo de longitud con mas valores atipicos.

# En lugar de contarlos a simple vista en el grafico, se
# calculan de forma programatica para cada grupo por separado.

contar_atipicos <- function(x) {
  q1  <- quantile(x, 0.25, na.rm = TRUE)
  q3  <- quantile(x, 0.75, na.rm = TRUE)
  ric <- q3 - q1
  lim_inf <- q1 - 1.5 * ric
  lim_sup <- q3 + 1.5 * ric
  sum(x < lim_inf | x > lim_sup, na.rm = TRUE)
}

atipicos_por_grupo <- tapply(fijadas$dur, fijadas$long_grupo,
                             contar_atipicos)
atipicos_por_grupo

# En proporcion al tamano de cada grupo, para una comparacion
# justa entre grupos de tamanos distintos:
n_por_grupo <- table(fijadas$long_grupo)
prop_atipicos <- atipicos_por_grupo / n_por_grupo
round(sort(prop_atipicos, decreasing = TRUE) * 100, 2)

# Interpretacion: el grupo con mayor cantidad absoluta de
# valores atipicos no es necesariamente el que tiene mayor
# proporcion, si ese grupo tambien es el mas numeroso. La
# comparacion en terminos de proporcion es la que responde a la
# pregunta de si un grupo de longitud especifico es
# proporcionalmente mas propenso a producir tiempos de lectura
# extremos, y no solo mas numeroso en terminos absolutos.


# --- SOLUCION 4.4 -----------------------------------------------
# Limite superior de valores atipicos en dos lenguas.

dos_lenguas <- names(sort(sd_por_lengua, decreasing = TRUE))[c(1,
               length(sd_por_lengua))]
dos_lenguas   # la de mayor y la de menor dispersion, de 2.2

limite_por_lengua <- function(lengua) {
  x   <- subset(fijadas, lang == lengua)$dur
  q1  <- quantile(x, 0.25)
  q3  <- quantile(x, 0.75)
  q3 + 1.5 * (q3 - q1)
}

limites <- sapply(dos_lenguas, limite_por_lengua)
round(limites, 1)

# Interpretacion: se espera que la lengua con mayor desviacion
# estandar, identificada en la actividad 2.2, tenga tambien un
# limite superior de valores atipicos mas alto, porque un RIC
# mayor desplaza ese limite hacia arriba. Si ambos limites
# resultaran similares pese a tener desviaciones estandar muy
# distintas, eso indicaria que la diferencia en dispersion se
# concentra en unos pocos valores muy extremos y no en el
# cuerpo central de la distribucion, que es lo que capta el RIC.


# =============================================================
# 5. MEDIDAS DE ASOCIACION
# =============================================================

# --- DEMO ------------------------------------------------------

cor(fijadas$long_palabra, fijadas$dur, method = "pearson")
cor.test(fijadas$long_palabra, fijadas$dur, method = "pearson")
cor.test(fijadas$long_palabra, fijadas$dur, method = "spearman")

tabla_chi <- table(meco$skip, meco$long_grupo)
tabla_chi
chisq.test(tabla_chi)

resultado_chi <- chisq.test(tabla_chi)
resultado_chi$expected
resultado_chi$statistic


# --- SOLUCION 5.1 -----------------------------------------------
# Correlacion de Pearson y Spearman entre nfix y dur.

r_pearson_nfix  <- cor(fijadas$nfix, fijadas$dur, method = "pearson")
r_spearman_nfix <- cor(fijadas$nfix, fijadas$dur, method = "spearman")

round(c(pearson = r_pearson_nfix, spearman = r_spearman_nfix), 4)

# Interpretacion: se espera una correlacion positiva y fuerte
# entre ambas variables, porque el tiempo total de lectura de
# una palabra se construye en buena medida a partir del numero
# de fijaciones que recibio; mas fijaciones implican, casi por
# definicion, mas tiempo acumulado. Los dos coeficientes deberian
# ser similares entre si en este caso, a diferencia de lo
# observado entre longitud y duracion, porque la relacion entre
# nfix y dur es mas cercana a lineal.


# --- SOLUCION 5.2 -----------------------------------------------
# cor.test() entre long_palabra y dur, reportado en una frase.

prueba_cor <- cor.test(fijadas$long_palabra, fijadas$dur,
                       method = "pearson")

prueba_cor$estimate       # coeficiente
prueba_cor$conf.int       # intervalo de confianza
prueba_cor$p.value        # valor p

# Frase de reporte (ajustar los valores segun el resultado real):
cat(sprintf(
  "La correlacion entre longitud de palabra y tiempo de lectura fue r = %.3f (IC 95%% [%.3f, %.3f]), p %s.\n",
  prueba_cor$estimate,
  prueba_cor$conf.int[1], prueba_cor$conf.int[2],
  ifelse(prueba_cor$p.value < 0.001, "< 0.001",
         paste("=", round(prueba_cor$p.value, 3)))
))

# Interpretacion: con un conjunto de datos de cientos de miles
# de observaciones, el valor p sera practicamente cero incluso
# si el coeficiente es modesto en magnitud. El intervalo de
# confianza sera muy estrecho por la misma razon. Lo que aporta
# informacion sustantiva es el valor del coeficiente en si, no
# la significacion estadistica.


# --- SOLUCION 5.3 -----------------------------------------------
# Tabla de contingencia y chi-cuadrado entre skip y lang.

tabla_skip_lang <- table(meco$skip, meco$lang)
tabla_skip_lang

resultado_skip_lang <- chisq.test(tabla_skip_lang)
resultado_skip_lang$statistic
resultado_skip_lang$parameter    # grados de libertad
resultado_skip_lang$p.value

# Reporte:
cat(sprintf(
  "Chi-cuadrado(%d) = %.2f, p %s.\n",
  resultado_skip_lang$parameter,
  resultado_skip_lang$statistic,
  ifelse(resultado_skip_lang$p.value < 0.001, "< 0.001",
         paste("=", round(resultado_skip_lang$p.value, 3)))
))

# Interpretacion: dado el tamano de la muestra, es esperable que
# la prueba resulte significativa, lo que indica que la tasa de
# omision no es igual entre lenguas. Esto ya se habia visto de
# forma descriptiva en la sesion anterior con tapply(); lo que
# aporta esta prueba es una cuantificacion formal de que esa
# diferencia no es atribuible unicamente al azar muestral.


# --- SOLUCION 5.4 -----------------------------------------------
# Frecuencias esperadas frente a observadas, para dos lenguas.

esperadas <- resultado_skip_lang$expected
observadas <- tabla_skip_lang

# Diferencia directa entre ambas matrices:
diferencia_obs_esp <- observadas - esperadas
round(diferencia_obs_esp, 1)

# Para dos lenguas especificas (ajustar los codigos):
dos_lenguas_chi <- colnames(tabla_skip_lang)[1:2]

round(diferencia_obs_esp[, dos_lenguas_chi], 1)

# Lengua con la mayor discrepancia absoluta en la fila skip = 1:
fila_omitidas <- abs(diferencia_obs_esp["1", ])
names(which.max(fila_omitidas))

# Interpretacion: una diferencia positiva grande en la fila de
# palabras omitidas indica que esa lengua omite mas de lo que
# se esperaria si la omision fuera independiente de la lengua;
# una diferencia negativa indica que omite menos de lo
# esperado. La lengua con la mayor discrepancia absoluta es la
# que mas contribuye al estadistico chi-cuadrado global, es
# decir, la que mas aleja a la tabla completa de la hipotesis
# de independencia.


# =============================================================
# 6. REGISTRO DE LA SESION
# =============================================================

sessionInfo()
