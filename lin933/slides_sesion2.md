---
title: LIIN-933
subtitle: Conceptos Básicos y Tipos de Muestreo
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


# Marco general
 
## El problema que organiza todo el curso
 
Casi nunca podemos observar la población completa. Trabajamos con una parte y queremos afirmar algo sobre el todo.
 
Tres preguntas encadenadas:
 
1. ¿Cómo **describimos** lo que tenemos delante?
2. ¿Cómo **exploramos** su estructura?
3. ¿Cómo **generalizamos** a lo que no observamos?
Cada pregunta corresponde a una rama de la estadística —y el muestreo es lo que hace posible la tercera.
 
\note{Slide de encuadre añadida para dar unidad a la presentación. La idea es que los estudiantes vean desde el principio que los conceptos básicos (población, muestra, parámetro, estadístico) y los métodos de muestreo no son dos temas separados, sino dos mitades del mismo problema: cómo pasar legítimamente de la parte al todo.}
 
## Agenda
 
**Parte I — Conceptos básicos**
 
- Las tres ramas de la estadística y el papel de la probabilidad
- Población, muestra, censo, parámetro y estadístico
- Variables: tipos y escalas de medición

**Parte II — Métodos de muestreo**
 
- La distinción fundamental: probabilístico vs. no probabilístico
- Cinco diseños probabilísticos
- Cuatro diseños no probabilísticos
- Limitaciones y criterio de elección

\note{La presentación original tiene 22 diapositivas; esta versión mantiene todo el contenido pero lo reorganiza en dos partes explícitas y añade slides de articulación al inicio, en las transiciones y al cierre.}
 
# Parte I — Conceptos básicos
 
## Las tres ramas de la estadística
 
La estadística es un conjunto de métodos de análisis de datos que se agrupan en tres categorías:
 
| Rama | Qué hace |
|---|---|
| **Descriptiva** | Resume grandes volúmenes de datos mediante medidas de resumen, tablas y gráficos calculados a partir de ellos |
|----|----|
| **Análisis exploratorio** | Busca estructuras en la masa de datos que revelen las características de la fuente que los originó |
| **Inferencia** | Confirma o concluye propiedades de la población conociendo solo una parte representativa: la muestra |
 
\note{La distinción es de propósito, no de técnica: una misma media aritmética puede usarse descriptivamente (resumir lo observado) o inferencialmente (estimar un parámetro poblacional). El análisis exploratorio ocupa un lugar intermedio: no se limita a resumir, pero tampoco pretende generalizar formalmente. Es el terreno del módulo de EDA.}
 
## El puente: teoría de probabilidades
 
La teoría de probabilidades es la teoría matemática que modela el azar.
 
Su función en este esquema es precisa: **permite el paso desde la muestra hacia la población.**
 
\begin{center}
Estadística descriptiva $\longrightarrow$ \textbf{Probabilidad} $\longrightarrow$ Inferencia estadística
\end{center}
 
\note{Esta es la pieza que articula las tres ramas y que conviene subrayar. Sin un modelo del azar no hay forma de cuantificar cuánto puede alejarse un estadístico de su parámetro. Por eso el muestreo probabilístico —donde el azar interviene de manera controlada— es la condición que habilita toda la inferencia posterior.}
 
## Población y muestra
 
**Población (estadística):** cualquier colección o agrupación de objetos que comparten características básicas comunes. Sus objetos se denominan **unidades** o **elementos de la población**.
 
**Muestra:** cualquier subconjunto de elementos poblacionales. Sus miembros son **elementos** o **unidades muestrales**.
 
Para propósitos estadísticos, ese subconjunto debe obtenerse mediante **procedimientos objetivos**.
 
\note{La definición de población es deliberadamente amplia: no son solo personas. Pueden ser textos, enunciados, mediciones acústicas, transacciones. Lo que la constituye es el conjunto de características comunes que el investigador define, y esa definición es una decisión, no un dato.}
 
## Muestra aleatoria: el calificativo que importa
 
Para distinguir una muestra **subjetiva** de una **objetiva** se añade el calificativo *aleatoria*.
 
> Una **muestra aleatoria** es un subconjunto de elementos poblacionales seleccionados mediante alguna metodología objetiva.
 
Toda la Parte II de esta presentación desarrolla qué significa "metodología objetiva".
 
\note{El adjetivo "aleatoria" no es decorativo: marca la frontera entre una muestra sobre la que se puede hacer inferencia formal y una que solo permite descripción. Esta slide anticipa la distinción probabilístico/no probabilístico que estructura la segunda mitad.}
 
## Censo, parámetro y estadístico
 
**Censo:** observar la población completa; equivale a tomar una muestra igual a la población.
 
| | **Parámetro** | **Estadístico** |
|---|---|---|
| Se refiere a | La población | La muestra |
| ¿Se conoce? | En general, **no** | Sí, es un valor conocido |
| Estabilidad | Fijo | Varía de una muestra a otra |
| Ejemplo | Edad promedio de los habitantes de una región | Edad promedio de los habitantes seleccionados en la muestra |
 
El estadístico se utiliza para **estimar** el parámetro y obtener conclusiones sobre la población.
 
\note{Esta tabla es el núcleo conceptual de la Parte I. La asimetría es lo esencial: conocemos el estadístico pero nos interesa el parámetro, y la única vía entre ambos es la inferencia probabilística. La variabilidad del estadístico entre muestras es exactamente lo que la teoría de probabilidades permite cuantificar.}
 
## Variables
 
**Variables:** características o atributos —de interés para el investigador— presentes en cada uno de los elementos que conforman la población.
 
Primera gran división:
 
- **Cualitativas (categóricas):** los elementos se clasifican en categorías o clases excluyentes
    - *Ejemplos:* estado civil, lugar de procedencia, marca de un artículo
- **Cuantitativas (numéricas):** los valores posibles son cantidades o números
    - *Ejemplos:* tiempo que demora un alumno en madurar un concepto, cantidad de palabras escritas por una secretaria en un minuto, porcentaje de impurezas en una jeringa
\note{El criterio de exclusividad en las categóricas es importante: las clases deben ser mutuamente excluyentes y, idealmente, exhaustivas. Los ejemplos de la presentación original son deliberadamente variados —del ámbito educativo, laboral e industrial— para mostrar que el mismo esquema se aplica en cualquier dominio.}
 
## Subclasificación de las variables cuantitativas
 
**Discretas:** el conjunto de valores posibles es finito o infinito numerable.
 
- *Ejemplos:* cantidad de consultas atendidas por un profesor, cantidad de crías por camada
**Continuas:** pueden asumir infinitos valores.
 
- *Ejemplos:* el sueldo de una persona, tiempo que tarda un animal en alcanzar un peso previamente determinado
\note{La distinción tiene consecuencias prácticas directas: los datos discretos suelen ser conteos y requieren modelos específicos (Poisson, binomial), mientras que los continuos admiten el tratamiento gaussiano habitual. En la práctica, un conteo con valores altos suele tratarse como continuo sin gran pérdida.}
 
## Escalas de medición: variables categóricas
 
**Nominal:** las categorías no admiten ordenación por magnitud.
 
- *Ejemplos:* colores, sexo, actividad profesional (químico, agrónomo, etc.)
**Ordinal:** las categorías admiten una ordenación —no alfabética.
 
- *Ejemplos:* nivel socioeconómico (alto, medio, bajo); sistema de evaluación en los primeros años de enseñanza básica (muy bueno, bueno, suficiente, insuficiente)
\note{La precisión "no alfabética" es fina y vale la pena señalarla: cualquier conjunto de etiquetas puede ordenarse alfabéticamente, pero eso no lo convierte en ordinal. Lo que define la escala ordinal es que el orden refleje una magnitud subyacente del atributo medido.}
 
## Escalas de medición: variables numéricas
 
**Intervalos:** poseen un punto de referencia (cero) **relativo** —relativo en el sentido de que al cambiar la unidad de medición, el punto de referencia difiere.
 
- Solo permiten comparaciones por **diferencias**
**Razones:** poseen un cero **absoluto**, es decir, único.
 
- Permiten además comparaciones por **cocientes**
\note{El ejemplo clásico: 20 °C no es "el doble de calor" que 10 °C, porque el cero de la escala Celsius es convencional. En cambio 10 segundos sí es exactamente el doble de 5, porque el cero de la duración es absoluto. La consecuencia práctica es qué operaciones aritméticas tienen sentido sobre los datos.}
 
## Síntesis de la Parte I
 
\begin{center}
Población $\longrightarrow$ \textbf{muestra} $\longrightarrow$ estadístico $\longrightarrow$ estimación del parámetro
\end{center}
 
En cada elemento de la población medimos **variables**, cuyo tipo y escala determinan qué análisis es legítimo.
 
La calidad de todo el proceso depende del segundo paso: **cómo se obtuvo la muestra**.
 
\note{Slide de articulación añadida para cerrar la Parte I y abrir la Parte II. El mensaje es que los conceptos vistos hasta aquí describen la arquitectura del problema, pero la validez de la inferencia se juega íntegramente en el método de selección de la muestra, que es lo que viene a continuación.}
 
# Parte II — Métodos de muestreo
 
## La distinción fundamental
 
**Muestreo probabilístico:** se puede calcular la probabilidad que tiene cada muestra posible de ser sorteada durante el proceso.
 
- El **azar siempre está presente** en la selección
- Eso tiende a garantizar que la muestra sea **representativa** de la población bajo estudio
**Muestreo no probabilístico:** no es posible conocer la probabilidad de sortear cada una de las muestras posibles.
 
\note{Esta es la bisagra de toda la Parte II. Todo lo que sigue —los nueve diseños— se ordena bajo esta dicotomía, y la razón de fondo aparecerá en la slide de limitaciones: sin probabilidades conocidas no hay forma de estimar el error muestral. Conviene anticiparlo aquí brevemente.}
 
## Diseños probabilísticos: panorama
 
Cinco procedimientos, ordenados de menor a mayor complejidad estructural:
 
| Diseño | Idea central |
|---|---|
| **Aleatorio simple** | Sorteo directo sobre la lista completa |
| **Sistemático** | Sorteo del punto de partida y recorrido regular |
| **Estratificado** | Dividir en grupos homogéneos y muestrear en cada uno |
| **Conglomerados** | Muestrear grupos completos y censarlos |
| **Bietápico** | Muestrear grupos y luego muestrear dentro de ellos |
 
\note{Tabla de panorama añadida para dar estructura antes del detalle. La progresión no es arbitraria: estratificado y conglomerados son opuestos conceptuales (homogeneidad interna versus grupos completos), y el bietápico surge como refinamiento del muestreo por conglomerados.}
 
## Muestreo aleatorio simple
 
Procedimiento en el que **todas las muestras posibles de un tamaño fijo tienen igual probabilidad** de ser seleccionadas.
 
Ejecución:
 
1. Enumerar todas las unidades muestrales
2. Sortear unidades hasta completar el número requerido
\note{Es el diseño de referencia contra el cual se comparan todos los demás, y el supuesto que asume la mayoría de las fórmulas estadísticas estándar. Su exigencia práctica es fuerte: requiere un marco muestral completo, es decir, una lista de todos los elementos de la población, que rara vez existe.}
 
## Muestreo sistemático
 
Se aplica cuando existe una lista de todas las unidades muestrales **en un orden independiente de la variable que se desea medir**.
 
Sea $N$ el tamaño de la población y $n$ el tamaño de la muestra. Se define:
 
$$M = \text{entero más cercano a } \frac{N}{n}$$
 
Procedimiento:
 
1. Seleccionar al azar un número entre 1 y $M$: será el orden de la primera unidad
2. Recorrer la lista seleccionando **una de cada $M$** hasta completar las $n$ unidades
\note{La condición sobre el orden de la lista es crítica y suele pasarse por alto. Si el orden guarda relación con la variable de interés —por ejemplo, una lista de empleados ordenada por antigüedad cuando estudiamos salarios—, el muestreo sistemático introduce sesgo. Con una lista en orden neutro, en cambio, resulta más simple de ejecutar que el aleatorio simple.}
 
## Muestreo estratificado
 
Consiste en dividir la población en grupos **homogéneos**, o **estratos**, según los valores de una variable relacionada con la característica bajo estudio, y aplicar muestreo aleatorio simple **dentro de cada estrato**.
 
*Ejemplo:* para medir las preferencias de una población de consumidores, se separa la población en estratos según nivel socioeconómico y se muestrea cada estrato por separado.
 
\note{La clave está en la palabra "homogéneos": los estratos deben ser internamente similares y diferentes entre sí. Cuando eso se cumple, el estratificado reduce la varianza de las estimaciones respecto del aleatorio simple del mismo tamaño. Es el diseño natural cuando ya se conocen las variables que estructuran la población.}
 
## Muestreo por conglomerados
 
Consiste en dividir la población en pequeños grupos, o **conglomerados**, obtener una muestra aleatoria simple **de conglomerados**, y practicar un **censo dentro de cada conglomerado seleccionado**.
 
*Ejemplo:* para una encuesta de hogares en una ciudad, en lugar de muestrear hogares se muestrean **manzanas**. Se envía un encuestador a cada manzana seleccionada para encuestar todos sus hogares, lo que resulta más eficiente.
 
\note{Contraste con el estratificado: allí muestreamos DENTRO de todos los grupos; aquí seleccionamos ALGUNOS grupos y los censamos completos. Y los criterios de conformación son opuestos: los estratos deben ser homogéneos internamente, los conglomerados idealmente heterogéneos —cada conglomerado debería ser una miniatura de la población. La ventaja del diseño es logística: concentra el trabajo de campo.}
 
## Muestreo en dos etapas (bietápico)
 
La muestra se toma en **dos pasos**:
 
1. Seleccionar una muestra de **unidades primarias**
2. Seleccionar una muestra de **elementos dentro de cada unidad primaria** escogida
\note{Es el muestreo por conglomerados sin el censo interno: en lugar de encuestar todos los hogares de la manzana seleccionada, se sortea una submuestra de ellos. Resuelve el problema del conglomerado cuando los grupos son demasiado grandes para censarlos, y se generaliza al muestreo polietápico con tres o más niveles.}
 
## Diseños no probabilísticos: panorama
 
Cuatro procedimientos donde la selección depende del criterio del investigador:
 
| Diseño | Criterio de selección |
|---|---|
| **Por cuotas** | Proporciones fijadas por el investigador, sin sorteo interno |
| **Bola de nieve** | Los propios sujetos reclutan a los siguientes |
| **Por conveniencia** | Proximidad, facilidad de acceso, disponibilidad |
| **Juicio experto** | Filtrado por alguien con conocimiento del dominio |
 
\note{Tabla de panorama añadida. Vale la pena notar que estos diseños no son "malos" en abstracto: cada uno responde a una circunstancia donde el muestreo probabilístico es imposible o desproporcionadamente costoso. El problema es que sus resultados no admiten inferencia formal, como veremos en la slide de limitaciones.}
 
## Muestreo por cuotas
 
El investigador construye una muestra con individuos que representan a la población, elegidos según rasgos o cualidades que él mismo define.
 
- Es similar al **estratificado**, salvo que los elementos de cada estrato **no se seleccionan aleatoriamente**
- Exige que el investigador comprenda muy bien los elementos constitutivos de la población
*Ejemplo:* dividir la muestra por sexo, grupo etario o actividad laboral; decidir qué proporción corresponde a cada grupo y reclutar según su criterio.
 
\note{Es el diseño no probabilístico más cercano a uno probabilístico, y por eso el más frecuente en estudios de mercado y opinión. La diferencia con el estratificado es exactamente un paso —el sorteo dentro de cada grupo— pero ese paso es el que habilita o impide la inferencia formal.}
 
## Muestreo por bola de nieve o en cadena
 
Se utiliza para estudiar grupos muy pequeños o individuos difíciles de encontrar.
 
Procedimiento: seleccionar unos pocos sujetos iniciales —uno o dos— y pedirles que **recluten a otras personas** del mismo grupo o con las mismas características.
 
- *Ejemplos:* personas sin hogar, integrantes de grupos clandestinos, personas con comportamientos socialmente no aceptados como el consumo de drogas
- **Inconveniente:** el investigador tiene poco control sobre la muestra obtenida, y los sujetos finales dependen fuertemente de los seleccionados inicialmente
\note{La dependencia de las semillas iniciales es el problema técnico central: si los primeros sujetos pertenecen a una subred particular, toda la muestra heredará ese sesgo. Existen variantes con correcciones estadísticas (respondent-driven sampling) que intentan mitigarlo, pero el diseño básico no lo resuelve.}
 
## Muestreo intencionado o por conveniencia
 
La selección la hace el investigador por **proximidad, facilidad de acceso o disponibilidad** de las personas para formar parte de la muestra.
 
*Ejemplos:*
 
- Investigadores que se ubican a la salida de una clase y solicitan voluntarios para responder un cuestionario
- Periodistas que entrevistan transeúntes para conocer y difundir su opinión sobre un hecho de actualidad
Los seleccionados comparten características comunes, lo que introduce un **fuerte sesgo** en los resultados.
 
\note{Es el diseño más común en la práctica académica —y el menos defendible. El ejemplo de los estudiantes universitarios es especialmente pertinente para investigación en ciencias sociales y del lenguaje, donde buena parte de la evidencia proviene de muestras de estudiantes de pregrado de la propia universidad del investigador.}
 
## Muestreo por juicio experto
 
Involucra a alguien con **conocimiento acabado** de las características de ciertos miembros de la población de interés.
 
- Esa persona ejecuta un **filtrado** de los sujetos para seleccionar solo los elegibles
- *Ejemplo:* en un estudio médico, seleccionar individuos que presentan cierta patología y están sometidos a un tratamiento determinado
- Generalmente las muestras resultantes son **muy pequeñas**
\note{Es el diseño apropiado cuando el fenómeno de interés es raro y la población objetivo, difícil de definir operacionalmente. El conocimiento experto sustituye al marco muestral inexistente. El costo es que la representatividad descansa por completo en el criterio de esa persona.}
 
## Limitaciones del muestreo
 
**En el muestreo probabilístico** es posible estimar la magnitud del error que se puede estar cometiendo, porque se conoce la probabilidad de obtener cada muestra.
 
**En el muestreo no probabilístico**, al no poder determinarse esa probabilidad:
 
- Es **imposible estimar el error muestral**
- Se producen **sesgos importantes**, porque la muestra depende fuertemente del criterio de quien la selecciona
> Por eso el muestreo probabilístico siempre será mejor que el no probabilístico.
 
\note{Esta es la conclusión de la presentación original y conviene presentarla como tal. Un matiz que puede añadirse en la discusión: la superioridad es en cuanto a capacidad inferencial. Cuando el muestreo probabilístico es materialmente imposible —poblaciones ocultas, fenómenos raros—, un diseño no probabilístico bien documentado sigue siendo preferible a no investigar, siempre que las conclusiones se presenten con el alcance limitado que corresponde.}
 
# Cierre
 
## Mapa integrador
 
\begin{center}
\textbf{POBLACIÓN} (parámetro desconocido)
\end{center}
 
\begin{center}
$\downarrow$ \emph{método de muestreo}
\end{center}
 
\begin{center}
\textbf{MUESTRA} (estadístico conocido)
\end{center}
 
\begin{center}
$\downarrow$ \emph{teoría de probabilidades}
\end{center}
 
\begin{center}
\textbf{INFERENCIA} (estimación con error cuantificable)
\end{center}
 
La flecha central solo funciona si la primera fue **probabilística**.
 
\note{Slide de cierre añadida. Condensa la presentación completa: los conceptos de la Parte I definen los extremos del esquema, los métodos de la Parte II determinan la primera flecha, y la probabilidad habilita la segunda. El mensaje final es que la elección del método de muestreo no es un detalle operativo sino la condición de posibilidad de toda la inferencia.}
 
## Tres ideas para retener
 
> Un **estadístico** es conocido y variable; un **parámetro** es fijo y desconocido. Toda la estadística inferencial vive en esa asimetría.
 
> El **tipo y la escala** de una variable determinan qué análisis es legítimo aplicarle.
 
> Solo el **muestreo probabilístico** permite cuantificar el error; los demás diseños describen, pero no autorizan a generalizar formalmente.
 
\note{Si los estudiantes se llevan una sola de las tres, que sea la última: es la que gobierna las decisiones de diseño en cualquier investigación empírica y la que más frecuentemente se pasa por alto al justificar una metodología.}
 
## Referencia
 
\footnotesize
 
Videla J., Patricio. *Conceptos básicos y tipos de muestreo.* Material del curso Estadística 2.
 
\vspace{1em}
 
Esta versión reorganiza el contenido original en dos partes, añade slides de articulación (marco general, panoramas de diseños, síntesis y mapa integrador) y parafrasea las definiciones buscando mayor precisión, sin suprimir contenido.
 
\note{Nota de procedencia para uso académico. Todas las definiciones, ejemplos y la conclusión sobre limitaciones provienen de la presentación original; las slides añadidas tienen función estructural y están señaladas como tales.}
 

