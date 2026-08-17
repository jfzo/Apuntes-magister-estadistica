# =============================================================
# Sesion 2 - Analisis exploratorio de datos de lectura
# Modulo de Analisis Exploratorio de Datos
# Doctorado en Linguistica
#
# Corpus: MECO, lectura en lengua materna
# Datos: https://osf.io/3527a
#
# Este guion reune el codigo de demostracion del apunte y las
# soluciones de sus actividades. Los bloques marcados DEMO se
# ejecutan en clase; los marcados SOLUCION corresponden a las
# actividades numeradas.
#
# Nombre:
# Fecha:
# =============================================================


# =============================================================
# 0. PREPARACION
# =============================================================

# Descargar manualmente desde https://osf.io/3527a el archivo de
# medidas por palabra y dejarlo en la carpeta del proyecto.
#
# Comprobar que se esta en el componente correcto: el proyecto
# MECO agrupa varios componentes en OSF con nombres de archivo
# semejantes. Bajar el equivocado no produce un error inmediato,
# sino columnas que no coinciden con las esperadas.


# --- DEMO: carga de un archivo .rda --------------------------

# Un archivo .rda contiene objetos con su propio nombre, que hay
# que averiguar. No se asigna con <- como un CSV.

antes <- ls()
load("joint_data_trimmed.rda")
nuevos <- setdiff(ls(), antes)
nuevos

# Asignar un nombre corto y estable al objeto cargado.
# Ajustar segun lo que devuelva la linea anterior:
meco <- get(nuevos[1])

# Si el archivo descargado fuera un CSV:
# meco <- read.csv("archivo.csv", encoding = "UTF-8")


# --- DEMO: verificacion de la estructura ---------------------

str(meco)
dim(meco)
names(meco)

# Comprobar que estan las columnas que el apunte supone. Si
# alguna falta, identificar la correspondencia UNA vez y
# renombrar aqui, en lugar de reescribir el resto del guion.

esperadas <- c("ia", "ianum", "subid", "lang", "itemid",
               "skip", "firstrun.skip", "nfix", "refix",
               "reg.in", "reg.out",
               "firstfix.dur", "firstrun.dur", "dur")

setdiff(esperadas, names(meco))   # vacio si esta todo

# Ejemplo de renombrado, si hiciera falta:
# names(meco)[names(meco) == "trialid"] <- "itemid"


# =============================================================
# 1. INVENTARIO
# =============================================================

# --- DEMO ----------------------------------------------------

nrow(meco)                          # observaciones palabra-participante
length(unique(meco$subid))          # participantes
length(unique(meco$lang))           # lenguas
length(unique(meco$itemid))         # textos

table(meco$lang)

# La tabla anterior cuenta observaciones, no participantes.
# Para contar participantes hay que contar identificadores
# distintos dentro de cada lengua.

participantes_por_lengua <- tapply(meco$subid, meco$lang,
                                   function(x) length(unique(x)))
sort(participantes_por_lengua)


# --- SOLUCION 2.1 --------------------------------------------
# Inventario y observaciones por participante.

n_obs   <- nrow(meco)
n_part  <- length(unique(meco$subid))
n_leng  <- length(unique(meco$lang))
n_texto <- length(unique(meco$itemid))

c(observaciones = n_obs, participantes = n_part,
  lenguas = n_leng, textos = n_texto)

# Promedio de observaciones por participante:
round(n_obs / n_part, 1)

# Cuantas palabras tienen los doce textos en cada lengua:
palabras_por_lengua <- tapply(meco$ianum, meco$lang, max)
sort(palabras_por_lengua)

# Comprobacion mas directa: observaciones de un participante
# concreto frente al total de palabras de su lengua.
un_sujeto <- meco$subid[1]
sum(meco$subid == un_sujeto)

# Interpretacion: el promedio de observaciones por participante
# corresponde al numero total de palabras de los doce textos en
# su lengua. No es identico entre lenguas, porque la traduccion
# de un mismo texto produce un numero distinto de palabras: las
# lenguas de morfologia sintetica condensan en una palabra lo
# que otras expresan en varias. Esa diferencia es en si misma un
# dato sobre las lenguas y no un defecto del corpus.


# --- SOLUCION 2.2 --------------------------------------------
# Participantes por lengua y el problema de la desigualdad.

sort(participantes_por_lengua)

range(participantes_por_lengua)
round(max(participantes_por_lengua) /
      min(participantes_por_lengua), 2)

barplot(sort(participantes_por_lengua), las = 2, cex.names = 0.8,
        main = "Participantes por lengua",
        ylab = "Numero de lectores")

# Interpretacion: los laboratorios aportaron numeros distintos
# de participantes. La consecuencia es que las estimaciones no
# tienen la misma precision en todas las lenguas: una media
# calculada sobre treinta lectores es mas inestable que una
# calculada sobre sesenta, y una diferencia entre dos lenguas
# puede reflejar esa inestabilidad antes que un efecto real.
#
# En un analisis exploratorio no se corrige, pero se documenta,
# y se evita interpretar diferencias pequenas entre lenguas de
# muestra reducida.


# --- SOLUCION 2.3 --------------------------------------------
# Relacion de orden entre las tres duraciones.

# Solo tiene sentido sobre palabras que recibieron fijacion.
fijadas <- subset(meco, skip == 0)

nrow(fijadas)
round(nrow(fijadas) / nrow(meco) * 100, 2)   # porcentaje fijado

cumple <- with(fijadas,
               firstfix.dur <= firstrun.dur &
               firstrun.dur <= dur)

table(cumple, useNA = "ifany")
round(mean(cumple, na.rm = TRUE) * 100, 4)

# Examinar las que no cumplen, si las hay:
anomalas <- fijadas[!cumple & !is.na(cumple),
                    c("subid", "lang", "ia",
                      "firstfix.dur", "firstrun.dur", "dur")]
nrow(anomalas)
head(anomalas, 20)

# Interpretacion: la desigualdad debe cumplirse por construccion.
# La primera fijacion es una de las fijaciones de la primera
# pasada, y la primera pasada es parte del tiempo total. Una
# violacion no indica un hallazgo sino un problema: columnas
# confundidas, un archivo distinto del previsto, o un caso de
# borde en el preprocesamiento. Es una comprobacion que conviene
# incorporar como rutina al cargar cualquier version del corpus.


# --- SOLUCION 2.4 --------------------------------------------
# Correspondencia entre omision y valores faltantes.

tabla_skip_na <- table(meco$skip, is.na(meco$dur))
tabla_skip_na

# Casos que no encajan en el patron esperado:
# skip = 1 con duracion registrada, o skip = 0 sin duracion.
discordantes <- subset(meco,
                       (skip == 1 & !is.na(dur)) |
                       (skip == 0 &  is.na(dur)))
nrow(discordantes)

if (nrow(discordantes) > 0) {
  head(discordantes[, c("subid", "lang", "ia",
                        "skip", "nfix", "dur")], 20)
  table(discordantes$skip)
}

# Interpretacion: la asociacion es casi perfecta porque ambas
# columnas codifican el mismo hecho desde dos angulos. Una
# palabra omitida no tiene duracion de fijacion porque nunca fue
# fijada; el faltante no es un dato perdido sino la ausencia del
# evento que se mide.
#
# Los casos discordantes suelen deberse a parpadeos o perdidas
# de seguimiento durante una fijacion: la palabra fue mirada
# pero la duracion no es utilizable. Conviene identificarlos
# porque su tratamiento es distinto: no son omisiones, son datos
# perdidos en el sentido habitual.


# --- DEMO: por que importa como se descartan los faltantes ----

# ADVERTENCIA. La convencion de codificacion no es universal.
# Segun la configuracion del preprocesamiento, una palabra
# omitida puede recibir NA o puede recibir 0.

sum(meco$dur == 0, na.rm = TRUE)   # cuantos ceros hay

# Si las omisiones se codificaran con 0 en lugar de NA, la linea
# siguiente promediaria incluyendo miles de ceros: na.rm no
# elimina nada porque no hay nada que eliminar. El resultado
# seria una duracion media artificialmente baja que mezcla
# palabras leidas con palabras nunca miradas. El calculo no
# falla, no advierte, y devuelve una cifra plausible.

mean(meco$dur, na.rm = TRUE)   # sobre que poblacion promedia

# El subconjunto explicito es inmune a ese problema, porque
# filtra por el hecho sustantivo y no por la convencion de
# codificacion. Ademas deja verificable el denominador.

mean(fijadas$dur)
nrow(fijadas)

# na.rm = TRUE no es incorrecto en si mismo. Es apropiado una
# vez comprobado que representan los faltantes. El problema es
# el uso reflejo, antes de esa comprobacion.


# =============================================================
# 2. VARIABLES BINARIAS
# =============================================================

# --- DEMO ----------------------------------------------------

table(meco$skip)
round(prop.table(table(meco$skip)) * 100, 2)

# Si la variable esta codificada como 0 y 1, su media es
# directamente la proporcion de unos.
mean(meco$skip)
mean(meco$reg.in, na.rm = TRUE)

# Comparacion entre lenguas:
omision_por_lengua <- tapply(meco$skip, meco$lang, mean)
sort(omision_por_lengua)

barplot(sort(omision_por_lengua), las = 2, cex.names = 0.8,
        main = "Tasa de omision por lengua",
        ylab = "Proporcion de palabras omitidas")

# Antes de mirar el resultado, anotar la prediccion sobre que
# lenguas ocuparan cada extremo y por que.


# --- SOLUCION 3.1 --------------------------------------------
# Tasas globales frente al rango de la literatura.

tasa_omision   <- mean(meco$skip)
tasa_regresion <- mean(meco$reg.in, na.rm = TRUE)

round(c(omision = tasa_omision, regresion = tasa_regresion) * 100, 2)

# La literatura situa las regresiones entre el 5 % y el 20 % de
# todos los sacadicos.
tasa_regresion >= 0.05 & tasa_regresion <= 0.20

# Interpretacion: si el valor cae dentro del rango, es una
# validacion de que se esta midiendo lo esperado. Si cae muy
# fuera, conviene sospechar de la columna elegida antes que del
# corpus: reg.in cuenta regresiones HACIA la palabra, y reg.out
# regresiones DESDE ella, de modo que confundirlas cambia el
# resultado.
#
# Nota sobre la unidad de medida: la cifra de la literatura se
# expresa sobre el total de sacadicos, mientras que reg.in se
# calcula sobre palabras. No son exactamente la misma magnitud,
# y la comparacion es orientativa.


# --- SOLUCION 3.2 --------------------------------------------
# Tasa de omision por lengua.

omision_ord <- sort(omision_por_lengua)
round(omision_ord * 100, 2)

# Rango entre extremos:
round(range(omision_por_lengua) * 100, 2)
round((max(omision_por_lengua) - min(omision_por_lengua)) * 100, 2)

# La lengua que mas omite y la que menos:
names(which.max(omision_por_lengua))
names(which.min(omision_por_lengua))

# Interpretacion: la diferencia entre extremos suele ser
# considerable. La hipotesis razonable es que las lenguas de
# palabras mas largas omitan menos, porque una palabra larga
# rara vez cabe entera en la region de vision nitida y necesita
# una fijacion propia. Esa hipotesis se verifica en la
# actividad 4.2.


# --- SOLUCION 3.3 --------------------------------------------
# Omision total frente a omision de primera pasada.

tasa_total   <- mean(meco$skip)
tasa_primera <- mean(meco$firstrun.skip, na.rm = TRUE)

round(c(total = tasa_total, primera_pasada = tasa_primera) * 100, 2)

tasa_primera >= tasa_total   # debe ser TRUE

# Interpretacion, deducible sin mirar los datos: una palabra
# omitida durante la primera pasada puede ser fijada mas tarde,
# tras una regresion. Por tanto el conjunto de palabras omitidas
# en el recorrido completo es un subconjunto de las omitidas en
# primera pasada, y la tasa total es necesariamente menor o
# igual.
#
# La diferencia entre ambas tasas estima que proporcion de
# palabras se saltan inicialmente pero se recuperan despues.
round((tasa_primera - tasa_total) * 100, 2)


# --- SOLUCION 3.4 --------------------------------------------
# Refijacion y relectura por lengua.

refijacion <- tapply(meco$refix, meco$lang, mean, na.rm = TRUE)

# La variable reread puede no estar en todas las versiones:
if ("reread" %in% names(meco)) {
  relectura <- tapply(meco$reread, meco$lang, mean, na.rm = TRUE)
} else {
  relectura <- rep(NA, length(refijacion))
  names(relectura) <- names(refijacion)
}

comparacion <- data.frame(
  lengua     = names(omision_por_lengua),
  omision    = round(as.numeric(omision_por_lengua), 4),
  refijacion = round(as.numeric(refijacion), 4),
  relectura  = round(as.numeric(relectura), 4)
)

comparacion[order(-comparacion$omision), ]

# Relacion entre omision y refijacion:
plot(comparacion$omision, comparacion$refijacion,
     pch = 16,
     xlab = "Tasa de omision", ylab = "Tasa de refijacion",
     main = "Omision frente a refijacion por lengua")
text(comparacion$omision, comparacion$refijacion,
     labels = comparacion$lengua, pos = 4, cex = 0.7)

cor(comparacion$omision, comparacion$refijacion,
    method = "spearman", use = "complete.obs")

# Interpretacion: cabe esperar una relacion negativa. Las
# lenguas cuyos lectores omiten mas palabras tienden a refijar
# menos, porque ambas conductas dependen de la misma causa
# subyacente, la longitud de las palabras.
#
# ADVERTENCIA. La unidad de analisis aqui es la lengua, y hay
# alrededor de una docena. Una correlacion calculada sobre doce
# puntos es muy inestable: un solo valor extremo puede
# invertirla. Se describe el patron, no se afirma causalidad ni
# se reporta un contraste de significacion.


# --- SOLUCION 3.5 --------------------------------------------
# Contingencia entre omision y regresion entrante.

tabla_sr <- table(skip = meco$skip, reg_in = meco$reg.in)
tabla_sr

round(prop.table(tabla_sr, margin = 1) * 100, 2)

# margin = 1 divide cada celda por el total de su fila: dentro
# de las palabras omitidas, que porcentaje recibio una regresion,
# y lo mismo dentro de las fijadas.

# Interpretacion: entre las palabras omitidas la tasa de
# regresion entrante es muy baja, casi por definicion, porque
# una regresion hacia una palabra implica fijarla y por tanto
# deja de estar omitida en el recorrido completo. Los pocos
# casos que aparecen en esa celda merecen inspeccion, porque
# probablemente reflejan la discordancia identificada en la
# actividad 2.4.


# =============================================================
# 3. VARIABLES DERIVADAS
# =============================================================

# --- DEMO: longitud de palabra -------------------------------

meco$long_palabra <- nchar(meco$ia)

summary(meco$long_palabra)
table(meco$long_palabra)

tapply(meco$long_palabra, meco$lang, mean)

# En un corpus multilingue el recuento de caracteres depende de
# la codificacion. Si una lengua muestra una longitud media
# implausible, el problema esta en la codificacion y no en la
# lengua.


# --- DEMO: recodificar en grupos -----------------------------

meco$long_grupo <- cut(meco$long_palabra,
                       breaks = c(0, 3, 5, 8, Inf),
                       labels = c("muy corta", "corta",
                                  "media", "larga"))

table(meco$long_grupo)
class(meco$long_grupo)
levels(meco$long_grupo)

tapply(meco$skip, meco$long_grupo, mean)

# Los intervalos de cut() son abiertos por la izquierda: tres
# caracteres cae en la primera categoria y cuatro en la segunda.
# Los puntos de corte son una decision arbitraria que hay que
# documentar.


# --- DEMO: posicion relativa en el texto ---------------------

n_palabras <- tapply(meco$ianum, meco$itemid, max)
meco$pos_relativa <- meco$ianum /
                     n_palabras[as.character(meco$itemid)]

summary(meco$pos_relativa)

# El objeto n_palabras es un vector con nombres, y se indexa por
# el identificador del texto convertido a caracter. La
# conversion con as.character() es necesaria porque los nombres
# de un vector son siempre cadenas de texto, aunque provengan de
# valores numericos. Sin ella, R interpretaria el identificador
# como una posicion y devolveria el elemento equivocado.

# Rehacer el subconjunto de fijadas para que herede las columnas
# nuevas:
fijadas <- subset(meco, skip == 0)


# --- SOLUCION 4.1 --------------------------------------------
# Distribucion global de la longitud de palabra.

summary(meco$long_palabra)

hist(meco$long_palabra, breaks = 30,
     main = "Distribucion de la longitud de palabra",
     xlab = "Caracteres", ylab = "Frecuencia")

mean(meco$long_palabra)
median(meco$long_palabra)

# Interpretacion: la distribucion es asimetrica hacia la
# derecha. Predominan las palabras cortas, que en su mayoria son
# elementos funcionales, y hay una cola de palabras largas mucho
# menos numerosas. La media supera a la mediana, aunque la
# asimetria es mucho menos pronunciada que la de las duraciones
# que veremos en la seccion 4.


# --- SOLUCION 4.2 --------------------------------------------
# Longitud media por lengua y verificacion de plausibilidad.

long_por_lengua <- tapply(meco$long_palabra, meco$lang, mean)
round(sort(long_por_lengua), 2)

barplot(sort(long_por_lengua), las = 2, cex.names = 0.8,
        main = "Longitud media de palabra por lengua",
        ylab = "Caracteres")

# Verificacion de plausibilidad: valores fuera de un rango
# razonable sugieren un problema de codificacion.
long_por_lengua[long_por_lengua < 3 | long_por_lengua > 10]

# Contraste con la tasa de omision, que cierra la prediccion
# formulada en la seccion 2:
verificacion <- data.frame(
  lengua   = names(long_por_lengua),
  longitud = round(as.numeric(long_por_lengua), 2),
  omision  = round(as.numeric(omision_por_lengua), 4)
)

verificacion[order(verificacion$longitud), ]

plot(verificacion$longitud, verificacion$omision, pch = 16,
     xlab = "Longitud media de palabra (caracteres)",
     ylab = "Tasa de omision",
     main = "Longitud de palabra y omision por lengua")
text(verificacion$longitud, verificacion$omision,
     labels = verificacion$lengua, pos = 4, cex = 0.7)

cor(verificacion$longitud, verificacion$omision,
    method = "spearman")

# Interpretacion: se espera una relacion negativa. Las lenguas
# de palabras mas largas omiten menos. La relacion existe pero
# no es perfecta, porque intervienen tambien la frecuencia de
# las palabras y las convenciones ortograficas de cada lengua,
# por ejemplo el tratamiento de los compuestos como una palabra
# o como varias.
#
# Se aplica la misma advertencia de la actividad 3.4: la unidad
# es la lengua y son pocos puntos.


# --- SOLUCION 4.3 --------------------------------------------
# Omision por grupo de longitud.

omision_grupo <- tapply(meco$skip, meco$long_grupo, mean)
round(omision_grupo * 100, 2)

barplot(omision_grupo,
        main = "Tasa de omision por grupo de longitud",
        ylab = "Proporcion omitida", xlab = "")

# Interpretacion: la tasa de omision disminuye de forma
# monotona a medida que aumenta la longitud. Las palabras muy
# cortas se omiten con frecuencia porque suelen ser elementos
# funcionales muy predecibles y porque caben en la region de
# vision nitida de una fijacion vecina, de modo que se procesan
# sin necesidad de fijarlas.
#
# Este resultado replica uno de los hallazgos mas robustos de la
# investigacion sobre lectura.


# --- SOLUCION 4.4 --------------------------------------------
# El efecto de la longitud en dos lenguas contrastantes.

# Seleccionar las lenguas de longitud media extrema:
lengua_corta <- names(which.min(long_por_lengua))
lengua_larga <- names(which.max(long_por_lengua))
c(lengua_corta, lengua_larga)

sub_dos <- subset(meco, lang %in% c(lengua_corta, lengua_larga))

tabla_dos <- tapply(sub_dos$skip,
                    list(sub_dos$long_grupo, sub_dos$lang),
                    mean)
round(tabla_dos * 100, 2)

barplot(t(tabla_dos), beside = TRUE, legend.text = TRUE,
        main = "Omision por longitud en dos lenguas",
        ylab = "Proporcion omitida")

# Interpretacion: el patron descendente se mantiene en ambas
# lenguas, lo que indica que el efecto de la longitud es general
# y no un artefacto de una lengua concreta. Lo que puede variar
# es la magnitud del efecto y el nivel general de omision.
#
# Que un efecto se mantenga en direccion pero cambie en
# magnitud segun una tercera variable es una interaccion. Es el
# tipo de pregunta donde el analisis exploratorio resulta mas
# productivo.


# --- SOLUCION 4.5 --------------------------------------------
# Efectos de posicion en el texto.

meco$pos_tramo <- cut(meco$pos_relativa,
                      breaks = seq(0, 1, by = 0.2),
                      labels = c("inicio", "temprano", "medio",
                                 "tardio", "final"),
                      include.lowest = TRUE)

table(meco$pos_tramo)

# Sobre palabras fijadas, que es donde la duracion existe:
fijadas <- subset(meco, skip == 0)

dur_tramo <- tapply(fijadas$dur, fijadas$pos_tramo,
                    median, na.rm = TRUE)
round(dur_tramo, 1)

barplot(dur_tramo,
        main = "Tiempo mediano de lectura por tramo del texto",
        ylab = "Milisegundos", xlab = "")

# Tambien la omision, que se calcula sobre todas las palabras:
round(tapply(meco$skip, meco$pos_tramo, mean) * 100, 2)

# Interpretacion: pueden aparecer efectos de inicio, por la
# ausencia de contexto previo que facilite la prediccion, y de
# final, por la desaceleracion al cerrar el texto o por el
# efecto de la ultima linea.
#
# ADVERTENCIA. La posicion relativa esta confundida con el
# contenido: el inicio de un texto expositivo introduce el tema
# y suele contener terminos nuevos y poco frecuentes, mientras
# que el final recupera vocabulario ya presentado. Un efecto de
# posicion puede reflejar esa diferencia de contenido y no un
# efecto de la posicion en si.


# =============================================================
# 4. ASIMETRIA Y AGREGACION
# =============================================================

# --- DEMO: la forma antes del resumen ------------------------

hist(fijadas$dur, breaks = 100,
     main = "Tiempo total de lectura por palabra",
     xlab = "Milisegundos")

mean(fijadas$dur)
median(fijadas$dur)

boxplot(fijadas$dur, horizontal = TRUE,
        main = "Tiempo total de lectura por palabra",
        xlab = "Milisegundos")


# --- DEMO: transformacion logaritmica ------------------------

par(mfrow = c(1, 2))
hist(fijadas$dur, breaks = 100,
     main = "Escala original", xlab = "ms")
hist(log(fijadas$dur), breaks = 100,
     main = "Escala logaritmica", xlab = "log(ms)")
par(mfrow = c(1, 1))


# --- DEMO: agregacion por participante -----------------------

por_part <- aggregate(dur ~ subid + lang,
                      data = fijadas, FUN = mean)
names(por_part)[3] <- "dur_media"

nrow(por_part)                     # debe coincidir con n_part
nrow(por_part) == length(unique(meco$subid))

# Las tasas se calculan sobre meco completo, no sobre fijadas:
# la tasa de omision requiere conservar las palabras omitidas.
tasas <- aggregate(cbind(skip, reg.in) ~ subid + lang,
                   data = meco, FUN = mean)

lectores <- merge(por_part, tasas, by = c("subid", "lang"))
str(lectores)


# --- SOLUCION 5.1 --------------------------------------------
# Media y mediana del tiempo de lectura.

media_dur   <- mean(fijadas$dur)
mediana_dur <- median(fijadas$dur)

round(c(media = media_dur, mediana = mediana_dur), 1)
round(media_dur - mediana_dur, 1)

quantile(fijadas$dur, probs = c(0.5, 0.75, 0.9, 0.95, 0.99))

# Interpretacion: la media supera a la mediana de forma
# apreciable. La distribucion es fuertemente asimetrica hacia la
# derecha: la mayoria de las palabras recibe una unica fijacion
# de duracion breve, y una minoria acumula tiempos muy
# prolongados por refijaciones y visitas posteriores.
#
# La mediana describe mejor la palabra tipica. La media es
# sensible a la cola, y dos corpus con la misma mediana pueden
# tener medias muy distintas si difieren en la proporcion de
# palabras releidas.


# --- SOLUCION 5.2 --------------------------------------------
# Efecto de la transformacion logaritmica.

log_dur <- log(fijadas$dur)

round(c(media = mean(log_dur), mediana = median(log_dur)), 3)

par(mfrow = c(1, 2))
boxplot(fijadas$dur, main = "Original", ylab = "ms")
boxplot(log_dur, main = "Logaritmica", ylab = "log(ms)")
par(mfrow = c(1, 1))

# Comparacion de la asimetria mediante la distancia relativa
# entre media y mediana:
round((mean(fijadas$dur) - median(fijadas$dur)) /
        median(fijadas$dur), 4)
round((mean(log_dur) - median(log_dur)) / median(log_dur), 4)

# Interpretacion: tras la transformacion, media y mediana casi
# coinciden y la distribucion es aproximadamente simetrica.
#
# Que se gana: muchos procedimientos estadisticos suponen
# simetria de los residuos, y la transformacion es lo que hace
# aplicable ese supuesto.
#
# Que se pierde: la escala de interpretacion. Una diferencia de
# 0.1 en escala logaritmica no se lee como una diferencia en
# milisegundos, sino como una razon entre duraciones. Ese
# intercambio hay que hacerlo explicito en cualquier informe.


# --- SOLUCION 5.3 --------------------------------------------
# Las observaciones con mayor tiempo de lectura.

extremos <- fijadas[order(-fijadas$dur), ][1:20,
              c("subid", "lang", "itemid", "ia",
                "long_palabra", "nfix", "dur")]
extremos

# Se concentran en algun participante, lengua o texto?
table(extremos$subid)
table(extremos$lang)
table(extremos$itemid)

# Comparacion con el numero de fijaciones tipico:
median(fijadas$nfix)
summary(extremos$nfix)

# Interpretacion: si los valores extremos se concentran en unos
# pocos participantes, puede tratarse de lectores
# particularmente lentos o de problemas de calibracion del
# equipo. Si se concentran en un texto o en palabras concretas,
# apunta a dificultad lexica genuina.
#
# La distincion importa porque el tratamiento es distinto: un
# problema de equipo justifica excluir al participante, mientras
# que la dificultad lexica es precisamente el fenomeno que se
# quiere estudiar y excluirla seria eliminar la senal.


# --- SOLUCION 5.4 --------------------------------------------
# Tabla agregada por participante.

str(lectores)
nrow(lectores)
nrow(lectores) == length(unique(meco$subid))

head(lectores)
summary(lectores[, c("dur_media", "skip", "reg.in")])

# Si el numero de filas excede el de participantes, casi
# siempre es porque se incluyo una variable adicional en la
# formula de agregacion que subdivide a cada sujeto.


# --- SOLUCION 5.5 --------------------------------------------
# El nivel de agregacion cambia el resultado.

prom_palabras     <- mean(fijadas$dur)
prom_participante <- mean(por_part$dur_media)

round(c(sobre_palabras     = prom_palabras,
        sobre_participante = prom_participante), 2)
round(prom_palabras - prom_participante, 2)

# Numero de palabras fijadas por participante:
n_por_part <- table(fijadas$subid)
summary(as.numeric(n_por_part))

# Interpretacion: las dos cifras difieren porque ponderan
# distinto. El promedio sobre palabras pondera cada observacion
# por igual, de modo que los participantes que fijaron mas
# palabras pesan mas en el resultado. El promedio sobre
# participantes pondera cada lector por igual.
#
# Para comparar lenguas hay que usar el promedio sobre
# participantes. La razon es que la unidad de muestreo es el
# lector, no la palabra: si una lengua tiene mas participantes o
# si sus lectores omiten menos, el promedio sobre palabras
# refleja esa diferencia de composicion y no una diferencia en
# la conducta de lectura.
#
# El problema de fondo es la pseudorreplicacion: hay muchas
# observaciones por participante y no son independientes. La
# solucion completa son los modelos de efectos mixtos, que
# quedan fuera de este modulo. Lo que corresponde en un analisis
# exploratorio es ser explicito sobre el nivel al que se trabaja.


# =============================================================
# 5. RELACIONES ENTRE VARIABLES
# =============================================================

# --- DEMO: numerica por categorica ---------------------------

boxplot(dur_media ~ lang, data = por_part,
        las = 2, cex.axis = 0.8,
        main = "Tiempo medio de lectura por lengua",
        xlab = "", ylab = "Milisegundos")

medianas <- tapply(por_part$dur_media, por_part$lang, median)
round(sort(medianas), 1)


# --- DEMO: dos variables numericas ---------------------------

long_dur <- aggregate(dur ~ long_palabra,
                      data = fijadas, FUN = median)

plot(long_dur$long_palabra, long_dur$dur,
     pch = 16, type = "b",
     main = "Tiempo de lectura por longitud de palabra",
     xlab = "Caracteres", ylab = "Mediana del tiempo total (ms)")

cor(fijadas$long_palabra, fijadas$dur, method = "pearson")
cor(fijadas$long_palabra, fijadas$dur, method = "spearman")


# --- SOLUCION 6.1 --------------------------------------------
# Duracion media por lengua, a nivel de participante.

boxplot(dur_media ~ lang, data = por_part,
        las = 2, cex.axis = 0.8,
        main = "Tiempo medio de lectura por lengua",
        xlab = "", ylab = "Milisegundos")

resumen_lengua <- aggregate(dur_media ~ lang,
                            data = por_part,
                            FUN = function(x) {
                              c(mediana = median(x),
                                RIC     = IQR(x),
                                n       = length(x))
                            })
resumen_lengua <- do.call(data.frame, resumen_lengua)
names(resumen_lengua) <- c("lengua", "mediana", "RIC", "n")

resumen_lengua[order(-resumen_lengua$mediana), ]

# Lengua con mayor dispersion entre lectores:
resumen_lengua[order(-resumen_lengua$RIC), ][1:3, ]

# Interpretacion: la mediana indica el nivel tipico y el rango
# intercuartilico la heterogeneidad entre lectores de esa
# lengua. Son dos cosas distintas: una lengua puede tener
# tiempos medios altos con lectores muy homogeneos, u otra
# tiempos moderados con enorme variabilidad individual.
#
# Comprobar la columna n antes de interpretar: las lenguas con
# pocos participantes producen medianas inestables.


# --- SOLUCION 6.2 --------------------------------------------
# Forma de la relacion entre longitud y duracion.

plot(long_dur$long_palabra, long_dur$dur,
     pch = 16, type = "b",
     xlab = "Caracteres", ylab = "Mediana del tiempo (ms)",
     main = "Tiempo de lectura por longitud")

# Cuantas observaciones sostienen cada punto:
n_por_long <- table(fijadas$long_palabra)
n_por_long

# Restringir al rango con soporte suficiente:
longitudes_frecuentes <- as.numeric(
  names(n_por_long)[n_por_long >= 100])
sub_long <- subset(long_dur,
                   long_palabra %in% longitudes_frecuentes)

plot(sub_long$long_palabra, sub_long$dur, pch = 16, type = "b",
     xlab = "Caracteres", ylab = "Mediana del tiempo (ms)",
     main = "Restringido a longitudes con soporte suficiente")

# Distribuciones completas, no solo medianas:
boxplot(dur ~ long_palabra,
        data = subset(fijadas, long_palabra <= 15),
        main = "Distribucion del tiempo por longitud",
        xlab = "Caracteres", ylab = "Milisegundos")

# Interpretacion: la relacion es creciente pero no lineal en
# todo el rango. Suele aplanarse o volverse erratica en las
# longitudes mayores, y la razon es que hay muy pocas palabras
# de doce o mas caracteres, de modo que sus medianas se calculan
# sobre un puñado de observaciones.
#
# Un grafico de medianas oculta ese problema porque todos los
# puntos se ven igual de solidos. Mirar el numero de
# observaciones por punto es parte de la lectura del grafico.


# --- SOLUCION 6.3 --------------------------------------------
# Pearson frente a Spearman.

r_pearson  <- cor(fijadas$long_palabra, fijadas$dur,
                  method = "pearson")
r_spearman <- cor(fijadas$long_palabra, fijadas$dur,
                  method = "spearman")

round(c(pearson = r_pearson, spearman = r_spearman), 4)

# Efecto de la transformacion sobre el coeficiente de Pearson:
round(cor(fijadas$long_palabra, log(fijadas$dur),
          method = "pearson"), 4)

# Interpretacion: Pearson mide asociacion lineal sobre los
# valores originales y es sensible a los extremos. Con una
# variable tan asimetrica como la duracion, unos pocos valores
# muy altos influyen de forma desproporcionada.
#
# Spearman trabaja sobre rangos, de modo que solo le importa el
# orden y no la magnitud. Es robusto a los extremos y capta
# cualquier relacion monotona, sea lineal o no.
#
# Que ambos difieran es en si mismo un dato sobre la forma de la
# relacion. Notese ademas que Pearson sobre la duracion
# transformada se acerca al valor de Spearman: es otra manera de
# ver que la asimetria era lo que separaba a los dos
# coeficientes.


# --- SOLUCION 6.4 --------------------------------------------
# Interaccion entre longitud y lengua sobre la omision.

omision_int <- aggregate(skip ~ long_grupo + lang,
                         data = meco, FUN = mean)

# Cuatro lenguas: las dos de palabras mas cortas y las dos de
# palabras mas largas.
orden_long <- sort(long_por_lengua)
lenguas_sel <- c(names(head(orden_long, 2)),
                 names(tail(orden_long, 2)))
lenguas_sel

sub_int <- subset(omision_int, lang %in% lenguas_sel)

matriz <- xtabs(skip ~ long_grupo + lang, data = sub_int)
round(matriz * 100, 2)

barplot(matriz, beside = TRUE, legend.text = TRUE,
        args.legend = list(x = "topright", cex = 0.8),
        main = "Tasa de omision por longitud y lengua",
        ylab = "Proporcion omitida")

# Magnitud del efecto en cada lengua: diferencia entre el grupo
# de palabras muy cortas y el de largas.
apply(matriz, 2, function(x) round((x[1] - x[4]) * 100, 2))

# Interpretacion: la direccion del efecto se mantiene en las
# cuatro lenguas, lo que indica que es general. Lo que varia es
# la magnitud, y esa variacion es la interaccion.
#
# La pregunta que responde este grafico es si el efecto de la
# longitud sobre la omision es igual en todas las lenguas o si
# su intensidad depende de la lengua. Ese tipo de pregunta, si
# un efecto se modula segun una tercera variable, es donde el
# analisis exploratorio suele resultar mas productivo, porque
# las interacciones son dificiles de anticipar teoricamente.


# --- SOLUCION 6.5 --------------------------------------------
# Los lectores mas rapidos, regresan menos?

plot(lectores$dur_media, lectores$reg.in,
     pch = 16, col = rgb(0, 0, 0, 0.4),
     xlab = "Tiempo medio de lectura por palabra (ms)",
     ylab = "Tasa de regresiones entrantes",
     main = "Velocidad de lectura y regresiones")

abline(lm(reg.in ~ dur_media, data = lectores),
       col = "red", lwd = 2)

cor(lectores$dur_media, lectores$reg.in, method = "pearson")
cor(lectores$dur_media, lectores$reg.in, method = "spearman")

# Distinguiendo por lengua, para descartar que el patron global
# sea un artefacto de la composicion de la muestra:
plot(lectores$dur_media, lectores$reg.in,
     pch = 16, col = as.factor(lectores$lang),
     xlab = "Tiempo medio (ms)", ylab = "Tasa de regresion",
     main = "Velocidad y regresiones, por lengua")

# Interpretacion: cabe esperar una relacion positiva. Los
# lectores mas lentos tienden a regresar mas.
#
# ADVERTENCIA sobre causalidad. La asociacion no autoriza a
# concluir que regresar mas cause leer mas lento, y hay al
# menos tres explicaciones alternativas.
#
# Primera, dependencia mecanica: una regresion implica fijar de
# nuevo una palabra, y esas fijaciones adicionales entran en el
# calculo del tiempo total. Las dos variables comparten
# observaciones, de modo que parte de la asociacion es
# aritmetica y no conductual.
#
# Segunda, causa comun: una menor habilidad lectora o una menor
# competencia en el vocabulario del texto puede producir
# simultaneamente mayor lentitud y mas regresiones, sin que una
# cause la otra.
#
# Tercera, direccion inversa: la dificultad de comprension
# podria provocar tanto la desaceleracion como las regresiones,
# siendo ambas consecuencias de un tercer factor.
#
# Un diseno capaz de separar estas alternativas requeriria
# manipular experimentalmente la dificultad del texto y medir la
# comprension, que es exactamente lo que hacen los estudios
# experimentales de lectura.


# =============================================================
# 6. EXTENSION: TUS PROPIAS LENGUAS
# =============================================================
#
# Elegir dos lenguas del corpus y justificar la eleccion:
# relacionadas con la propia investigacion, tipologicamente
# contrastantes, o con sistemas de escritura distintos.

# mis_lenguas <- c("es", "fi")     # ajustar a los codigos reales
# mi_sub <- subset(meco, lang %in% mis_lenguas)
#
# table(mi_sub$lang)
# tapply(mi_sub$subid, mi_sub$lang,
#        function(x) length(unique(x)))
#
# A partir de aqui, todo el codigo de las secciones 2 a 5
# funciona sin cambios sobre mi_sub.

# Verificaciones obligatorias antes de interpretar:
#
# 1. Tamanos de muestra. Si una lengua tiene notablemente menos
#    participantes, sus estimaciones son mas inestables.
#
# 2. Materiales. Los doce textos fueron traducidos y adaptados,
#    no son identicos. Una diferencia entre lenguas puede
#    reflejar propiedades de la lengua, de la traduccion
#    concreta, o de la muestra de lectores de ese laboratorio.
#
# 3. Sistemas de escritura. Si la comparacion cruza alfabetos
#    distintos, el recuento de caracteres no mide lo mismo en
#    ambas lenguas y la variable de longitud no es comparable.


# =============================================================
# 7. REGISTRO DE LA SESION
# =============================================================
# Ejecutar al final y guardar la salida junto con el guion.

sessionInfo()