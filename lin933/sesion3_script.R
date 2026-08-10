# =============================================================
# Sesion 2 - Analisis exploratorio morfosintactico
# Modulo de Analisis Exploratorio de Datos
# Doctorado en Linguistica
#
# Corpus: UD Spanish AnCora (archivo de desarrollo)
#
# Este guion reune el codigo de demostracion de las laminas
# y las soluciones de las actividades. Los bloques marcados
# como DEMO se ejecutan en clase; los marcados como SOLUCION
# corresponden a las actividades numeradas de las laminas.
#
# Nombre:
# Fecha:
# =============================================================


# =============================================================
# 0. PREPARACION
# =============================================================

# install.packages("udpipe")   # solo la primera vez
library(udpipe)

# Descarga del corpus. Si falla por restricciones de red,
# descargar manualmente desde:
# https://github.com/UniversalDependencies/UD_Spanish-AnCora

archivo <- "es_ancora-ud-dev.conllu"

if (!file.exists(archivo)) {
  url_base <- paste0("https://raw.githubusercontent.com/",
                     "UniversalDependencies/UD_Spanish-AnCora/master/")
  download.file(paste0(url_base, archivo), destfile = archivo)
}


# =============================================================
# 1. EL CORPUS: CARGA E INVENTARIO
# =============================================================

# --- DEMO: mirar el archivo crudo antes de cargarlo -----------

writeLines(head(readLines(archivo, n = 30)))

# Se observan: lineas de comentario que empiezan con almohadilla,
# diez campos separados por tabuladores, y lineas en blanco que
# separan oraciones.


# --- DEMO: carga ---------------------------------------------

ancora <- udpipe_read_conllu(archivo)

str(ancora)
dim(ancora)
names(ancora)

head(ancora[, c("sentence_id", "token_id", "token",
                "lemma", "upos", "feats")], 15)


# --- DEMO: limpieza previa necesaria -------------------------

# CoNLL-U representa las palabras multipalabra (contracciones
# como "del", "al", y verbos con cliticos) con una linea de
# rango cuyo token_id es del tipo "12-13", seguida de las lineas
# de sus componentes. Esas lineas de rango no tienen anotacion
# morfosintactica y duplicarian el conteo.

sum(grepl("-", ancora$token_id))   # cuantas lineas de rango hay

# Se conservan solo las palabras sintacticas:
ancora <- subset(ancora, !grepl("-", ancora$token_id))

# Verificacion:
sum(grepl("-", ancora$token_id))   # debe ser 0


# --- DEMO: inventario ----------------------------------------

nrow(ancora)                          # ocurrencias
length(unique(ancora$sentence_id))    # oraciones
length(unique(ancora$upos))           # categorias gramaticales
colSums(is.na(ancora))                # valores faltantes

# Que categorias carecen de rasgos morfologicos:
table(ancora$upos, is.na(ancora$feats))

# La ausencia de feats en categorias sin flexion no es un error
# del corpus sino una propiedad del sistema. Conviene
# identificarla ahora y no cuando un promedio salga extrano.


# --- SOLUCION 1.1 --------------------------------------------
# Ocurrencias, oraciones, tipos lexicos en token y en lemma.

n_ocurrencias <- nrow(ancora)
n_oraciones   <- length(unique(ancora$sentence_id))
n_tipos_token <- length(unique(ancora$token))
n_tipos_lemma <- length(unique(ancora$lemma))

c(ocurrencias = n_ocurrencias,
  oraciones   = n_oraciones,
  tipos_token = n_tipos_token,
  tipos_lemma = n_tipos_lemma)

# Interpretacion: los tipos de token superan a los de lemma
# porque la flexion multiplica las formas de una misma entrada
# lexica (canto, cantas, canta comparten el lemma "cantar").
# La diferencia es una medida indirecta de la riqueza flexiva
# del texto.

n_tipos_token - n_tipos_lemma
round(n_tipos_token / n_tipos_lemma, 2)


# --- SOLUCION 1.2 --------------------------------------------
# Categorias presentes frente al inventario oficial de UD.

categorias_presentes <- sort(unique(ancora$upos))
categorias_presentes
length(categorias_presentes)

inventario_ud <- c("ADJ", "ADP", "ADV", "AUX", "CCONJ", "DET",
                   "INTJ", "NOUN", "NUM", "PART", "PRON",
                   "PROPN", "PUNCT", "SCONJ", "SYM", "VERB", "X")

setdiff(inventario_ud, categorias_presentes)   # ausentes

# Interpretacion: las categorias ausentes suelen ser INTJ
# (interjecciones) y PART (particulas). La primera es rara en
# prensa y ficcion escrita; la segunda no se usa en la
# anotacion del espanol, donde no hay una clase de particulas
# equivalente a la del ingles o el aleman. SYM y X pueden
# aparecer con frecuencia muy baja.


# --- SOLUCION 1.3 --------------------------------------------
# Razon tipo-ocurrencia sobre token y sobre lemma.

ttr_token <- n_tipos_token / n_ocurrencias
ttr_lemma <- n_tipos_lemma / n_ocurrencias

round(c(ttr_token = ttr_token, ttr_lemma = ttr_lemma), 4)

# Interpretacion: el TTR sobre lemma mide mejor la riqueza
# lexica, porque cuenta entradas de diccionario distintas y no
# variantes flexivas de una misma palabra. El TTR sobre token
# mezcla riqueza lexica con complejidad morfologica, de modo
# que una lengua muy flexiva parece mas rica solo por su
# morfologia.
#
# Advertencia adicional: ambas medidas dependen del tamano del
# texto, porque los tipos crecen mas lento que las ocurrencias.
# Comparar TTR entre textos de distinta extension es invalido
# sin normalizacion.


# =============================================================
# 2. CATEGORIAS GRAMATICALES
# =============================================================

# --- DEMO: distribucion univariada ---------------------------

frec_upos <- table(ancora$upos)
frec_upos

prop_upos <- round(prop.table(frec_upos) * 100, 2)
sort(prop_upos, decreasing = TRUE)

barplot(sort(frec_upos, decreasing = TRUE),
        las = 2, cex.names = 0.8,
        main = "Distribucion de categorias gramaticales",
        ylab = "Ocurrencias")

# Ordenar por frecuencia y no alfabeticamente: el orden
# alfabetico no transmite informacion.


# --- DEMO: densidad lexica -----------------------------------

contenido <- c("NOUN", "VERB", "ADJ", "ADV", "PROPN")

ancora$es_contenido <- ancora$upos %in% contenido

mean(ancora$es_contenido)

# El mecanismo es el mismo de la prelectura: %in% devuelve un
# vector logico y la media de un vector logico es la proporcion
# de valores verdaderos.


# --- SOLUCION 2.1 --------------------------------------------
# Tabla de proporciones ordenada.

prop_ordenada <- sort(round(prop.table(frec_upos) * 100, 2),
                      decreasing = TRUE)
prop_ordenada

# Las tres categorias mayores:
head(prop_ordenada, 3)

# Proporcion acumulada por las tres primeras:
sum(head(prop_ordenada, 3))

# Interpretacion esperada: NOUN, ADP, DET y PUNCT ocupan las
# primeras posiciones. Las categorias cerradas y funcionales
# concentran una fraccion del texto muy superior a su peso en
# el inventario, que es el patron general de las distribuciones
# linguisticas.


# --- SOLUCION 2.2 --------------------------------------------
# Grafico sin puntuacion.

sin_punt <- subset(ancora, upos != "PUNCT")
frec_sin_punt <- table(droplevels(factor(sin_punt$upos)))

# Comparacion visual de ambas versiones:
par(mfrow = c(1, 2))

barplot(sort(frec_upos, decreasing = TRUE),
        las = 2, cex.names = 0.7,
        main = "Con puntuacion", ylab = "Ocurrencias")

barplot(sort(frec_sin_punt, decreasing = TRUE),
        las = 2, cex.names = 0.7,
        main = "Sin puntuacion", ylab = "Ocurrencias")

par(mfrow = c(1, 1))   # restaurar el area de graficos

# Interpretacion: excluir la puntuacion no altera el orden
# relativo de las categorias lexicas, pero si cambia todas las
# proporciones, porque cambia el denominador. La decision debe
# tomarse de forma explicita y quedar documentada.


# --- SOLUCION 2.3 --------------------------------------------
# Densidad lexica con y sin puntuacion en el denominador.

dens_global <- mean(ancora$es_contenido)

dens_sin_punt <- mean(sin_punt$upos %in% contenido)

round(c(con_puntuacion = dens_global,
        sin_puntuacion = dens_sin_punt), 4)

# Interpretacion: la version sin puntuacion es la comparable
# entre corpus, porque los criterios de tokenizacion de signos
# de puntuacion varian entre proyectos de anotacion. Si un
# corpus tokeniza la puntuacion y otro no, las densidades
# calculadas sobre el total no son comparables.


# --- SOLUCION 2.4 --------------------------------------------
# Peso conjunto de determinantes y adposiciones.

prop_det_adp <- sum(prop_upos[c("DET", "ADP")])
prop_det_adp

# Numero de lemas distintos en cada una de esas categorias:
det_adp <- subset(ancora, upos %in% c("DET", "ADP"))
length(unique(det_adp$lemma))

# Interpretacion: dos categorias cerradas, con un inventario de
# unas pocas decenas de lemas, ocupan alrededor de un cuarto de
# las ocurrencias del corpus. Es la manifestacion categorial del
# mismo fenomeno que describe la ley de Zipf en el nivel lexico:
# un numero muy pequeno de elementos concentra una fraccion
# enorme del texto.


# =============================================================
# 3. RASGOS MORFOLOGICOS
# =============================================================

# --- DEMO: presencia de un rasgo -----------------------------

ancora$femenino <- grepl("Gender=Fem", ancora$feats)
table(ancora$femenino)


# --- DEMO: extraer el valor de un rasgo ----------------------

# Nota importante: el patron incluye digitos porque algunos
# valores del esquema UD son numericos, como Person=3.

extraer_rasgo <- function(feats, rasgo) {
  feats[is.na(feats)] <- ""
  patron <- paste0(rasgo, "=([A-Za-z0-9]+)")
  tiene <- grepl(patron, feats)
  resultado <- rep(NA_character_, length(feats))
  encontrados <- regmatches(feats[tiene], regexpr(patron, feats[tiene]))
  resultado[tiene] <- sub(paste0(rasgo, "="), "", encontrados)
  resultado
}

ancora$genero   <- extraer_rasgo(ancora$feats, "Gender")
ancora$numero   <- extraer_rasgo(ancora$feats, "Number")
ancora$modo     <- extraer_rasgo(ancora$feats, "Mood")
ancora$tiempo   <- extraer_rasgo(ancora$feats, "Tense")
ancora$persona  <- extraer_rasgo(ancora$feats, "Person")
ancora$formaverb <- extraer_rasgo(ancora$feats, "VerbForm")

table(ancora$genero, useNA = "ifany")

# useNA = "ifany" hace visibles los faltantes. Sin ese
# argumento, table() los oculta y la distribucion se
# interpreta mal.

# Atajo equivalente del paquete, util una vez comprendido
# el procedimiento manual:
# ancora_morf <- cbind_morphological(ancora, term = "feats")


# --- DEMO: preguntas linguisticas ----------------------------

sust <- subset(ancora, upos == "NOUN")
table(sust$genero, sust$numero)

verbos <- subset(ancora, upos == "VERB")
sort(table(verbos$modo), decreasing = TRUE)

# Antes de ejecutar la linea anterior, anotar la estimacion
# intuitiva de la proporcion de subjuntivo sobre indicativo.


# --- SOLUCION 3.1 --------------------------------------------
# Distribucion de persona en formas finitas.

finitas <- subset(ancora, grepl("VerbForm=Fin", ancora$feats))

nrow(finitas)
tabla_persona <- table(finitas$persona, useNA = "ifany")
tabla_persona
round(prop.table(tabla_persona) * 100, 2)

# Interpretacion esperada: domina ampliamente la tercera
# persona. El corpus es de prensa y ficcion, generos que
# refieren a terceros y evitan la interaccion directa con el
# lector. En un corpus de conversacion espontanea o de
# correspondencia la distribucion seria muy distinta, con un
# peso mucho mayor de primera y segunda persona.


# --- SOLUCION 3.2 --------------------------------------------
# Genero por numero en adjetivos, en proporciones por filas.

adj <- subset(ancora, upos == "ADJ")

tabla_adj <- table(adj$genero, adj$numero)
tabla_adj

round(prop.table(tabla_adj, margin = 1) * 100, 2)

# margin = 1 divide cada celda por el total de su fila, de modo
# que cada fila suma 100. Se lee: dentro de los adjetivos de
# genero X, que porcentaje es singular y que porcentaje plural.
#
# Interpretacion: si las proporciones de singular y plural son
# similares en ambos generos, el numero es independiente del
# genero, lo que es lo esperable porque son rasgos flexivos
# que responden a la concordancia con el sustantivo y no
# guardan relacion entre si.


# --- SOLUCION 3.3 --------------------------------------------
# Proporcion de subjuntivo.

modos <- table(ancora$modo)
modos

round(prop.table(modos) * 100, 2)

prop_subjuntivo <- modos["Sub"] / sum(modos)
round(prop_subjuntivo * 100, 2)

# Interpretacion: la estimacion intuitiva suele sobrestimar el
# subjuntivo, porque es una forma saliente y muy trabajada en
# la ensenanza de la lengua. Su frecuencia real en texto
# escrito es bastante menor que la percibida. Es un ejemplo
# concreto de por que la intuicion linguistica requiere
# verificacion empirica.


# --- SOLUCION 3.4 --------------------------------------------
# Numero en sustantivos frente a adjetivos.

num_sust <- prop.table(table(sust$numero))
num_adj  <- prop.table(table(adj$numero))

comparacion <- rbind(sustantivos = round(num_sust * 100, 2),
                     adjetivos    = round(num_adj * 100, 2))
comparacion

barplot(comparacion, beside = TRUE, legend.text = TRUE,
        main = "Distribucion de numero por categoria",
        ylab = "Porcentaje")

# Interpretacion: ambas distribuciones se parecen porque la
# concordancia obliga al adjetivo a copiar el numero del
# sustantivo al que modifica. No son identicas porque los
# adjetivos tambien concuerdan con sujetos que no son
# sustantivos (pronombres, oraciones sustantivadas) y porque
# no todos los sustantivos van acompanados de adjetivo.


# --- SOLUCION 3.5 --------------------------------------------
# Formas verbales finitas y no finitas.

formas <- table(ancora$formaverb)
formas
round(prop.table(formas) * 100, 2)

no_finitas <- sum(formas[names(formas) != "Fin"])
prop_no_finitas <- no_finitas / sum(formas)
round(prop_no_finitas * 100, 2)

# Interpretacion: las formas no finitas (infinitivo, gerundio,
# participio) representan una proporcion apreciable del total.
# El participio suele ser el mas frecuente de los tres por su
# doble funcion, como componente de tiempos compuestos y de
# pasivas perifrasticas, y como modificador adjetival.


# =============================================================
# 4. DEL TOKEN A LA ORACION
# =============================================================

# --- DEMO: longitud de oracion -------------------------------

long_oracion <- aggregate(token_id ~ sentence_id,
                          data = ancora, FUN = length)
names(long_oracion)[2] <- "n_tokens"

summary(long_oracion$n_tokens)

hist(long_oracion$n_tokens, breaks = 40,
     main = "Distribucion de la longitud de oracion",
     xlab = "Ocurrencias por oracion", ylab = "Frecuencia")

mean(long_oracion$n_tokens)
median(long_oracion$n_tokens)

boxplot(long_oracion$n_tokens, horizontal = TRUE,
        main = "Longitud de oracion", xlab = "Ocurrencias")


# --- DEMO: composicion gramatical por oracion ----------------

comp <- as.data.frame.matrix(table(ancora$sentence_id,
                                   ancora$upos))
comp$n_tokens <- rowSums(comp)
comp$sentence_id <- rownames(comp)

head(comp[, c("sentence_id", "NOUN", "VERB", "ADJ", "n_tokens")])

sum(comp$VERB == 0)   # oraciones sin verbos


# --- SOLUCION 4.1 --------------------------------------------
# Media y mediana de la longitud de oracion.

media_long   <- mean(long_oracion$n_tokens)
mediana_long <- median(long_oracion$n_tokens)

round(c(media = media_long, mediana = mediana_long), 2)
round(media_long - mediana_long, 2)

# Interpretacion: la media supera a la mediana, lo que indica
# asimetria positiva. La longitud de oracion es una variable de
# conteo con una cola larga a la derecha: unas pocas oraciones
# muy largas arrastran la media hacia arriba. La mediana
# describe mejor la oracion tipica del corpus.


# --- SOLUCION 4.2 --------------------------------------------
# Histograma completo frente a histograma restringido.

par(mfrow = c(1, 2))

hist(long_oracion$n_tokens, breaks = 40,
     main = "Todas las oraciones",
     xlab = "Ocurrencias", ylab = "Frecuencia")

hist(long_oracion$n_tokens[long_oracion$n_tokens < 50],
     breaks = 40,
     main = "Menos de 50 ocurrencias",
     xlab = "Ocurrencias", ylab = "Frecuencia")

par(mfrow = c(1, 1))

# Cuantas oraciones quedan excluidas:
sum(long_oracion$n_tokens >= 50)
round(mean(long_oracion$n_tokens >= 50) * 100, 2)

# Interpretacion: el histograma completo muestra la extension
# real de la cola, informacion necesaria para decidir que
# estadistico de resumen usar. El restringido muestra la forma
# del grueso de la distribucion, que en el primero queda
# comprimida contra el eje. Ninguno sustituye al otro:
# responden a preguntas distintas.


# --- SOLUCION 4.3 --------------------------------------------
# Las cinco oraciones mas largas.

mas_largas <- long_oracion[order(-long_oracion$n_tokens), ][1:5, ]
mas_largas

# Reconstruir el texto de cada una:
for (sid in mas_largas$sentence_id) {
  texto <- paste(subset(ancora, sentence_id == sid)$token,
                 collapse = " ")
  cat("\n--- Oracion", sid, "---\n")
  cat(substr(texto, 1, 500), "\n")
}

# Que buscar al leerlas: si son oraciones genuinamente largas
# (coordinacion extensa, subordinacion multiple, enumeraciones)
# o si hay problemas de segmentacion, es decir, dos o mas
# oraciones que el anotador no separo. En corpus periodisticos
# suelen aparecer titulares, sumarios y listados que la
# segmentacion automatica no divide correctamente.


# --- SOLUCION 4.4 --------------------------------------------
# Densidad lexica por oracion.

dens_oracion <- aggregate(es_contenido ~ sentence_id,
                          data = ancora, FUN = mean)
names(dens_oracion)[2] <- "densidad"

summary(dens_oracion$densidad)

hist(dens_oracion$densidad, breaks = 30,
     main = "Densidad lexica por oracion",
     xlab = "Proporcion de palabras de contenido")

# Comparacion con la cifra global:
round(c(global = dens_global,
        media_por_oracion = mean(dens_oracion$densidad)), 4)

# Interpretacion: las dos cifras difieren porque se calculan
# sobre unidades distintas. La densidad global pondera cada
# ocurrencia por igual, de modo que las oraciones largas pesan
# mas. La media de las densidades por oracion pondera cada
# oracion por igual, sin importar su extension. Si las
# oraciones cortas tienen una densidad sistematicamente
# distinta de las largas, ambas medidas divergen.
#
# Es un caso concreto de por que el nivel de agregacion importa,
# y el mecanismo que subyace a la paradoja de Simpson.


# --- SOLUCION 4.5 --------------------------------------------
# Razon sustantivo sobre verbo por oracion.

comp_con_verbo <- subset(comp, VERB > 0)

comp_con_verbo$ratio_nv <- comp_con_verbo$NOUN / comp_con_verbo$VERB

summary(comp_con_verbo$ratio_nv)
median(comp_con_verbo$ratio_nv)

# Las cinco razones mas altas:
top_nominal <- comp_con_verbo[order(-comp_con_verbo$ratio_nv), ][1:5, ]
top_nominal[, c("sentence_id", "NOUN", "VERB", "n_tokens", "ratio_nv")]

for (sid in top_nominal$sentence_id) {
  texto <- paste(subset(ancora, sentence_id == sid)$token,
                 collapse = " ")
  cat("\n--- Oracion", sid, "---\n")
  cat(substr(texto, 1, 400), "\n")
}

# Que buscar: las oraciones con razon mas alta suelen ser
# enumeraciones, listados de nombres propios y entidades, o
# construcciones de estilo nominal caracteristicas del lenguaje
# administrativo y periodistico. La razon sustantivo sobre verbo
# es una medida clasica para distinguir estilo nominal de estilo
# verbal.


# =============================================================
# 5. RELACIONES DE DEPENDENCIA
# =============================================================

# --- DEMO: distribucion de relaciones ------------------------

frec_dep <- sort(table(ancora$dep_rel), decreasing = TRUE)
head(frec_dep, 15)

round(prop.table(frec_dep)[1:10] * 100, 2)


# --- DEMO: distancia de dependencia --------------------------

# Los identificadores vienen como texto y hay que convertirlos.
ancora$tok_num  <- as.numeric(ancora$token_id)
ancora$head_num <- as.numeric(ancora$head_token_id)

# La raiz de cada oracion tiene head 0 y debe excluirse: no
# depende de ninguna otra palabra.
ancora$dist_dep <- ifelse(ancora$head_num == 0, NA,
                          abs(ancora$head_num - ancora$tok_num))

summary(ancora$dist_dep)

hist(ancora$dist_dep[!is.na(ancora$dist_dep)], breaks = 50,
     main = "Distribucion de la distancia de dependencia",
     xlab = "Distancia en ocurrencias")


# --- DEMO: direccion de la dependencia -----------------------

ancora$direccion <- ifelse(is.na(ancora$dist_dep), NA,
                    ifelse(ancora$head_num > ancora$tok_num,
                           "nucleo a la derecha",
                           "nucleo a la izquierda"))

table(ancora$direccion)


# --- DEMO: cruce con el tipo de relacion ---------------------

relaciones <- c("det", "amod", "nsubj", "obj", "obl", "advmod")
sub_rel <- subset(ancora, dep_rel %in% relaciones)

boxplot(dist_dep ~ dep_rel, data = sub_rel,
        main = "Distancia de dependencia por tipo de relacion",
        xlab = "", ylab = "Distancia", las = 2)


# --- SOLUCION 5.1 --------------------------------------------
# Diez relaciones mas frecuentes con proporciones.

top_dep <- head(frec_dep, 10)
top_dep

round(prop.table(frec_dep)[1:10] * 100, 2)
round(sum(prop.table(frec_dep)[1:10]) * 100, 2)   # acumulado

# Interpretacion esperada: las primeras posiciones suelen
# corresponder a "case" (adposiciones), "det" (determinantes) y
# "punct" (puntuacion), es decir, relaciones estructurales y no
# argumentales. La intuicion tiende a anticipar "nsubj" y "obj",
# que son las relaciones de las que se habla en la descripcion
# gramatical, pero son mucho menos numerosas porque cada oracion
# tiene pocos argumentos y muchos determinantes y preposiciones.


# --- SOLUCION 5.2 --------------------------------------------
# Media y mediana de la distancia.

media_dist   <- mean(ancora$dist_dep, na.rm = TRUE)
mediana_dist <- median(ancora$dist_dep, na.rm = TRUE)

round(c(media = media_dist, mediana = mediana_dist), 3)

quantile(ancora$dist_dep, probs = c(0.5, 0.75, 0.9, 0.99),
         na.rm = TRUE)

# Interpretacion: la mediana es muy baja, tipicamente 1 o 2
# posiciones, mientras que la media es sensiblemente mayor. La
# distribucion esta fuertemente sesgada a la derecha: la enorme
# mayoria de las dependencias son adyacentes o casi adyacentes,
# y unas pocas muy largas elevan la media.
#
# Ese patron es el hallazgo empirico que sostiene la hipotesis
# de minimizacion de la distancia de dependencia: las lenguas
# tienden a ordenar sus constituyentes de modo que los
# elementos sintacticamente relacionados queden proximos, lo
# que reduce la carga de memoria de trabajo en el procesamiento.


# --- SOLUCION 5.3 --------------------------------------------
# Direccion de la dependencia.

tabla_dir <- table(ancora$direccion)
tabla_dir
round(prop.table(tabla_dir) * 100, 2)

# Direccion por tipo de relacion, para las mas frecuentes:
round(prop.table(table(sub_rel$dep_rel, sub_rel$direccion),
                 margin = 1) * 100, 2)

# Interpretacion: el espanol es una lengua de nucleo inicial en
# la frase nominal y en la preposicional, de modo que los
# dependientes suelen seguir a su nucleo. Pero determinantes y
# adposiciones lo preceden, y son justamente las relaciones mas
# frecuentes, de modo que el balance global no es tan
# desequilibrado como podria esperarse. El cruce por tipo de
# relacion muestra que la direccion depende fuertemente de la
# relacion concreta y que el promedio global oculta esa
# variacion.


# --- SOLUCION 5.4 --------------------------------------------
# Distancia por tipo de relacion.

dist_por_rel <- aggregate(dist_dep ~ dep_rel,
                          data = ancora, FUN = median)

dist_por_rel[order(-dist_por_rel$dist_dep), ][1:10, ]

# Version ampliada del grafico, con mas relaciones:
relaciones_amplias <- names(head(frec_dep, 12))
sub_amplio <- subset(ancora, dep_rel %in% relaciones_amplias)

boxplot(dist_dep ~ dep_rel, data = sub_amplio,
        main = "Distancia por tipo de relacion",
        xlab = "", ylab = "Distancia", las = 2,
        cex.axis = 0.8)

# Interpretacion: las distancias mas cortas corresponden a
# relaciones dentro de la frase nominal, como "det" y "amod",
# donde el dependiente es adyacente al nucleo. Las mas largas
# corresponden a relaciones oracionales, como "conj" (segundo
# miembro de una coordinacion), "advcl" y "obl", donde el
# dependiente puede estar separado del nucleo por constituyentes
# completos. La explicacion es estructural: cuanto mas alto en
# el arbol se establece la relacion, mas material puede
# interponerse.


# --- SOLUCION 5.5 --------------------------------------------
# Distancia frente a longitud de oracion.

dist_oracion <- aggregate(dist_dep ~ sentence_id,
                          data = ancora, FUN = mean)
names(dist_oracion)[2] <- "dist_media"

# Union de las dos tablas por la columna comun:
oraciones <- merge(long_oracion, dist_oracion, by = "sentence_id")

nrow(long_oracion)
nrow(dist_oracion)
nrow(oraciones)

plot(oraciones$n_tokens, oraciones$dist_media,
     pch = 16, col = rgb(0, 0, 0, 0.25),
     main = "Distancia media frente a longitud de oracion",
     xlab = "Ocurrencias por oracion",
     ylab = "Distancia de dependencia media")

# Linea de tendencia, solo como ayuda visual:
abline(lm(dist_media ~ n_tokens, data = oraciones),
       col = "red", lwd = 2)

cor(oraciones$n_tokens, oraciones$dist_media,
    use = "complete.obs")

cor(oraciones$n_tokens, oraciones$dist_media,
    method = "spearman", use = "complete.obs")

# Interpretacion: se observa una relacion positiva. Las
# oraciones mas largas presentan distancias medias mayores.
#
# ADVERTENCIA sobre causalidad. Esta asociacion no autoriza a
# concluir que la longitud "cause" distancias mayores. La
# relacion es en buena medida geometrica: en una oracion de
# cinco palabras ninguna distancia puede superar cuatro, de
# modo que el rango posible de la variable dependiente esta
# acotado por la independiente. Es un artefacto estructural
# antes que un hallazgo linguistico.
#
# Un analisis serio de esta pregunta requeriria comparar la
# distancia observada con la esperada bajo ordenamientos
# aleatorios de la misma oracion, que es exactamente el diseno
# que emplea la literatura sobre minimizacion de distancia.


# =============================================================
# 6. EXTENSION: TEXTO PROPIO
# =============================================================
#
# Esta seccion es individual. Reemplazar "mi_texto.txt" por el
# archivo propio y ejecutar. Todo el codigo de las secciones
# 2 a 5 funciona sin cambios sobre el objeto "anotado".

# --- Descarga y carga del modelo -----------------------------

# Solo la primera vez. El modelo pesa unos 15 MB y queda
# guardado en la carpeta del proyecto.

# modelo_archivo <- udpipe_download_model(language = "spanish-ancora")
# modelo <- udpipe_load_model(modelo_archivo$file_model)

# En sesiones posteriores, cargar directamente el archivo:
# modelo <- udpipe_load_model("spanish-ancora-ud-2.5-191206.udpipe")


# --- Anotacion de un texto -----------------------------------

# mi_texto <- readLines("mi_texto.txt", encoding = "UTF-8")
# anotado <- as.data.frame(udpipe_annotate(modelo, x = mi_texto))
# str(anotado)


# --- Anotacion de varios textos, conservando su identidad ----

# textos <- c(t1 = "Primer texto completo...",
#             t2 = "Segundo texto completo...")
#
# anotado <- as.data.frame(udpipe_annotate(modelo,
#                                          x = textos,
#                                          doc_id = names(textos)))
#
# La columna doc_id permite comparar textos con aggregate():
# aggregate(es_contenido ~ doc_id, data = anotado, FUN = mean)


# --- Verificacion obligatoria de la anotacion ----------------

# La anotacion automatica tiene errores. Inspeccionar una
# muestra antes de confiar en cualquier cifra agregada.

# set.seed(42)
# muestra <- anotado[sample(nrow(anotado), 30),
#                    c("token", "lemma", "upos", "dep_rel")]
# muestra

# Registrar cuantos errores se detectan en la muestra y de que
# tipo. Esa cifra debe aparecer en la seccion de limitaciones
# del informe.


# =============================================================
# 7. REGISTRO DE LA SESION
# =============================================================
# Ejecutar al final y guardar la salida junto con el guion.
# Permite reproducir el analisis con las mismas versiones.

sessionInfo()