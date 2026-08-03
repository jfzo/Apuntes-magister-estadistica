---
title: LIIN-933
subtitle: Módulo de Análisis Exploratorio de Datos
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


# Introducción

## ¿Por qué empezar por aquí?

Antes de aprender *cómo* explorar datos, conviene entender *por qué* debemos hacerlo de forma metódica.

La respuesta es incómoda:

- **La cognición humana es sistemáticamente poco fiable**
- Vemos patrones donde no los hay
- Buscamos confirmar lo que ya creemos
- Razonamos mal con probabilidades

El método científico no es una formalidad: es un conjunto de **salvaguardas contra nuestros propios errores**.

\note{La idea central del módulo introductorio. No se trata de desconfiar de los estudiantes, sino de reconocer que todos —expertos incluidos— compartimos un aparato cognitivo con sesgos predecibles. El EDA será, más adelante, la aplicación práctica de estas salvaguardas. Conviene enfatizar el hilo conductor: distinguir entre lo que *parece* verdadero y lo que *es* contrastable.}

## Hoja de ruta

Tres bloques:

1. **¿Por qué necesitamos ciencia?** — límites de la lógica pura y la intuición
2. **Errare humanum est** — sesgos cognitivos y falacias
3. **¿Qué es la ciencia?** — falsación y método científico en lingüística

\note{Estructura tomada del capítulo 1 de SLAT7855 (Schweinberger). Cada bloque construye sobre el anterior: primero establecemos que necesitamos evidencia empírica, luego por qué la intuición no basta, y finalmente qué procedimiento nos protege.}

# 1. ¿Por qué necesitamos ciencia?

## Una definición mínima

> La ciencia es un proceso metódico para adquirir conocimiento sobre el mundo basado en **evidencia empírica**.

La palabra clave es *empírica*.

Para entender su peso, contrastemos dos familias de disciplinas.

\note{Definición deliberadamente simple para arrancar. El énfasis en "empírica" prepara el contraste con las ciencias formales, que es el argumento de la próxima slide.}

## Ciencias formales vs. empíricas

| | **Formales** | **Empíricas** |
|---|---|---|
| Ejemplos | Lógica, matemáticas | Sociolingüística, biología |
| Punto de partida | Axiomas | Observaciones |
| Método | Inferencia lógica | Observación / experimentación |
| Conocimiento | Demostrable | Provisional, revisable |

Las formales son poderosas para la **coherencia lógica**:

- *Sócrates es humano* + *todos los humanos son mortales* $\Rightarrow$ *Sócrates es mortal*

\note{La lingüística formal pertenece a la columna izquierda; la lingüística empírica (de corpus, experimental) a la derecha. Este módulo se sitúa firmemente en la segunda. El silogismo ilustra el poder de la inferencia formal: dado que las premisas son verdaderas, la conclusión se sigue con necesidad.}

## El límite de la lógica pura

La lógica construye representaciones **coherentes**, pero no puede decidir **cuál** corresponde a la realidad.

> ¿Levantaré el brazo izquierdo o el derecho al contar hasta tres?

- Ambos mundos son igualmente coherentes
- Solo la observación resuelve cuál ocurre
- Hay infinitos mundos lógicamente posibles

**La coherencia interna no garantiza adecuación al mundo.**

\note{Ejemplo de Schweinberger. El punto para lingüistas: un modelo gramatical elegante y formalmente impecable puede ser internamente coherente y aun así describir mal una lengua real. Por eso existe la lingüística empírica. Aquí conviene invitar a la reflexión: ¿cuántas teorías lingüísticas "bonitas" han caído ante datos de corpus?}

# 2. Errare Humanum Est

## El concepto ancla: sesgo de confirmación

**Sesgo de confirmación:** tendencia a buscar, notar y recordar información que confirma lo que ya creemos —e ignorar la que la contradice.

- Uno de los sesgos mejor documentados
- Afecta a expertos tanto como a legos
- El método científico existe, en su núcleo, para contrarrestarlo

En lugar de buscar confirmación, intentamos **falsar** nuestras hipótesis.

\note{Este es el concepto que unifica toda la sección. Las subsecciones siguientes son ilustraciones de distintas formas de falibilidad, pero el sesgo de confirmación es el eje. Anticipar aquí que la respuesta metodológica —falsar en vez de confirmar— se desarrollará en el bloque 3 con Popper.}

## Somos malos con probabilidades: Monty Hall

Tres puertas: dos cabras, un premio.

1. Eliges la puerta 1
2. El presentador abre una puerta con cabra (la 3)
3. ¿Cambias a la puerta 2?

. . .

**Sí: cambiar eleva tu probabilidad de 1/3 a 2/3.**

- Tu puerta: 1/3. Las otras dos juntas: 2/3
- Al abrir una perdedora, esos 2/3 se concentran en la que queda

\note{El `. . .` genera una pausa incremental en Beamer (pausa entre el planteo y la respuesta). Truco pedagógico: si la intuición se resiste, escalar a 20 puertas. Eliges una (1/20); el presentador abre 18 con cabras; queda una sola cerrada además de la tuya. Ahí es evidente que conviene cambiar. El caso de 3 es idéntico, solo menos obvio. Pueden verificarlo en simuladores online.}

## Subestimamos lo exponencial: cumpleaños

**En una clase de 23, ¿probabilidad de un cumpleaños compartido?**

. . .

Aproximadamente **50%** (la intuición dice ~6%).

El error: pensar en individuos, no en **pares**.

$$\frac{23 \cdot 22}{2} = 253 \text{ pares} \qquad \left(\frac{364}{365}\right)^{253} \approx 0.50$$

\note{El punto es la combinatoria: 253 pares posibles, no 23 personas. Cada par tiene alta probabilidad de NO coincidir (364/365), pero compuesta sobre 253 pares, la probabilidad de que nadie coincida cae a ~50%. Relevante en lingüística: cualquier análisis con comparaciones múltiples es terreno donde la intuición engaña —conecta con el problema de comparaciones múltiples en estadística inferencial.}

## Verificación en R

```r
n <- 73                          # estudiantes
days_in_year <- 365
prob_all_different <-
  prod((days_in_year - 0:(n-1)) / days_in_year)
prob_at_least_one_shared <- 1 - prob_all_different
prob_at_least_one_shared
#> [1] 0.9995608
```

Con 73 estudiantes: probabilidad $\approx$ 99.96%.

\note{Buen momento para el primer contacto con R del curso. El código calcula la probabilidad complementaria (todos distintos) y la resta de 1. Vale la pena ejecutarlo en vivo si hay RStudio disponible. Nótese el uso de `prod()` sobre un vector: idioma R idiomático.}

## Pensamiento rápido y lento

**Bate + pelota = 1.10. El bate cuesta 1.00 más. ¿La pelota?**

. . .

No es 0.10, sino **0.05** (0.05 + 1.05 = 1.10).

| **Rápido (Sistema 1)** | **Lento (Sistema 2)** |
|---|---|
| Intuitivo, automático | Deliberado, esforzado |
| Económico | Costoso |
| Propenso a errores | Más preciso |

La ciencia = aplicar **pensamiento lento** a problemas que resolveríamos por reflejo.

\note{Kahneman (2011). El EDA y la estadística son "pensamiento lento institucionalizado". El error del bate y la pelota es universal —incluso estudiantes de matemáticas caen. La lección no es que seamos tontos, sino que el Sistema 1 es económico y por eso lo usamos por defecto, aun cuando el problema exige Sistema 2.}

## Vemos patrones en el ruido

**Las palomas de Skinner:** alimentadas a intervalos aleatorios, desarrollaron rituales (girar, picotear) asociando por azar conducta y recompensa.

- Superstición: relación causal donde solo hay coincidencia
- Pareidolia: caras en Marte, en tostadas
- Sobreatribución de agencia (ruido nocturno $\to$ "alguien me sigue")

\note{Evolutivamente, sobreatribuir agencia era barato; no detectar un depredador real era fatal. De ahí el sesgo. Los rituales de atletas ("gané la última vez que no me afeité") son el equivalente humano de las palomas de Skinner. La lección para EDA: distinguir un patrón genuino de una fluctuación aleatoria del corpus es exactamente el problema central.}

## La tarea de Wason

Cuatro cartas (letra en una cara, número en la otra):

$$\boxed{A} \quad \boxed{K} \quad \boxed{2} \quad \boxed{7}$$

Regla: *si hay vocal en una cara, hay número par en la otra.*
¿Qué cartas voltear?

. . .

Respuesta correcta: **A y 7** (no "A y 2").

- **7** (impar): si detrás hay vocal, rompe la regla
- **2** es irrelevante: la regla no dice nada sobre los pares

\note{El error revela nuestra tendencia a buscar casos que CONFIRMAN (la carta "2", que "encaja" con par) en lugar de casos que podrían FALSAR (la carta "7"). Es el sesgo de confirmación en estado puro, en una tarea puramente lógica. La mayoría de la gente —incluidos académicos— falla en la versión abstracta.}

## El juego 1-2-4

El instructor tiene una regla y da tres números que la cumplen: **1, 2, 4**.
Propón un número; te digo si cumple.

- Típico: proponer 8 (cumple) $\to$ "duplicar el anterior" **X**
- Luego 16 (cumple) $\to$ "elevar al cuadrado" **X**
- Regla real: **"cada número mayor que el anterior"**

Solo proponiendo números que **contradicen** la hipótesis nos acercamos a la verdad.

\note{Esta es la lección epistemológica central del bloque. Intuitivamente probamos si nuestra hipótesis es correcta; la ciencia prueba si es falsa. El apoyo a una teoría viene de intentos FALLIDOS de refutarla, no de hallazgos que la confirman. Transición perfecta hacia Popper. Vale la pena hacerlo interactivo: proponer la regla en vivo y dejar que los estudiantes propongan números.}

## Percepción dependiente del contexto

El mismo trazo se lee distinto según el entorno:

\begin{center}
\texttt{A ? C} $\to$ "B" \qquad\qquad \texttt{12 ? 14} $\to$ "13"
\end{center}

- Estímulo idéntico, interpretación distinta
- La ilusión de Thatcher (rostros invertidos): el cerebro autocorrige
- **La categorización depende del contexto**

\note{Relevancia directa para lingüistas: este es el fenómeno que subyace a la percepción categorial del habla. El mismo continuo acústico se percibe como una u otra categoría fonológica según el contexto. Que el aparato perceptual "autocorrija" según expectativas es dato central para fonética y psicolingüística, y una advertencia sobre confiar en la introspección como evidencia.}

## Falacias lógicas: un catálogo defensivo

Argumentos defectuosos frecuentes; la defensa es reconocerlos:

- **Cherry-picking** — seleccionar solo evidencia favorable
- **Ad hominem** — atacar a la persona, no al argumento
- **Apelación a la autoridad** — la persona en lugar de su investigación
- **Hombre de paja** — refutar una versión debilitada del argumento
- **Argumento desde la ignorancia** — "no se ha probado falso, luego es verdad"
- **Falsa dicotomía** — solo dos extremos cuando hay más opciones
- **Pendiente resbaladiza / circular / pista falsa / costo hundido**

\note{No hace falta detenerse en cada una; el objetivo es que reconozcan las más frecuentes en discurso académico y público. Matiz importante en "apelación a la autoridad": citar a una autoridad es válido como sustituto de la investigación que representa; es falacia cuando lo que justifica es la persona, no lo que demostró. La defensa general es el pensamiento crítico, que hay que entrenar.}

# 3. ¿Qué es la ciencia?

## El método científico

Procedimiento cíclico para conocimiento fiable:

1. Observar un fenómeno
2. Formular una hipótesis **contrastable**
3. Derivar predicciones
4. Contrastar con datos sistemáticos
5. Revisar o rechazar según el resultado

Su poder no está en garantizar la verdad, sino en hacer las afirmaciones **contrastables** y los errores **corregibles**.

\note{Definición operativa del método. Enfatizar el punto final: la ciencia no promete certeza, promete corregibilidad. Esto contrasta con las ciencias formales (que sí demuestran) y con los sistemas de creencias no falsables (que nunca se corrigen).}

## Clever Hans

Caballo que "resolvía" aritmética golpeando el casco (c. 1900).

- **Más de una docena de científicos** lo observaron y no vieron truco
- Pfungst (1904): Hans respondía a **señales musculares involuntarias**
- Si nadie conocía la respuesta, Hans tampoco
- Si no veía a quien la sabía, fallaba

\note{Doble lección. Primera: las habilidades aparentes pueden deberse a señales no intencionadas; hay que probar bajo condiciones controladas. Segunda, más importante: usamos la ciencia porque nos protege de ser engañados por otros (malo) y sobre todo por nosotros mismos (mucho peor). El testimonio de múltiples observadores expertos no garantiza nada. Analogía moderna: el efecto del experimentador en estudios lingüísticos, que motiva diseños doble ciego.}

## Popper y la falsación

**En las ciencias empíricas nada se prueba; las hipótesis solo se falsan.**

$$\text{10.000 cisnes blancos} \not\Rightarrow \text{"todos los cisnes son blancos"}$$
$$\text{1 cisne negro} \Rightarrow \text{refutación inmediata}$$

- Asimetría entre verificación y falsación
- **Falsable ≠ falso**: significa que *podría* mostrarse falso
- Criterio de demarcación: una teoría es científica *sii* es falsable

\note{Popper rechazaba el estatus científico del psicoanálisis y el marxismo porque, por su formulación, acomodan cualquier observación y no arriesgan nada. Insistir en que "falsable" no es peyorativo: es una virtud, no un defecto. Una teoría que no puede fallar tampoco puede enseñarnos nada sobre el mundo.}

## El progreso como evolución

\begin{center}
Conjeturas $\to$ Intentos de refutación $\to$ Eliminación de errores $\to$ Teorías más aptas
\end{center}

- La falsación cumple para la ciencia lo que la selección natural para la biología
- Las teorías que sobreviven no son "más verdaderas", sino más **aptas**
- Ninguna prueba superada protege de una refutación futura
- El conocimiento empírico es siempre **provisional**

\note{Analogía popperiana con la evolución. Punto clave para gestionar expectativas de doctorandos: ningún hallazgo es definitivo. Esto no es debilidad de la ciencia, sino su motor. Conecta con la naturaleza acumulativa e iterativa de la investigación lingüística.}

## La lingüística empírica

**Lingüística:** el estudio científico del lenguaje y las lenguas.

- Descubrir, describir y modelar los sistemas del lenguaje
- La lingüística empírica investiga basándose en **observaciones de la realidad**
- Es **descriptiva, no prescriptiva**: cómo se usa la lengua, no cómo "debería" usarse

\note{Distinción descriptivo/prescriptivo fundamental. La lingüística empírica describe el uso real —incluyendo variación, cambio, "errores"— sin juzgarlo. Esto sitúa el módulo: exploraremos datos de lengua tal como es, no como la norma dice que debería ser.}

## El círculo científico: buscar las llaves

| **Paso** | **Llaves** | **Lingüística** |
|---|---|---|
| Observación | ¡No están! | Los jóvenes usan menos sujeto nulo |
| Pregunta | ¿Dónde están? | ¿Varía el sujeto nulo con la edad? |
| Hipótesis (H1) | En la mesa del TV | Los jóvenes usan menos sujeto nulo |
| H nula (H0) | NO en esa mesa | No hay relación edad–sujeto nulo |
| Diseño | Voy a mirar | Corpus estratificado por edad |
| Análisis | — | Test de asociación |
| Interpretación | No están; otro lado | Rechazar o no H0 |

\note{La analogía de las llaves (Schweinberger) traduce cada paso abstracto a algo cotidiano, y la columna lingüística lo aterriza en un problema real. Lo esencial: la investigación no termina con un resultado, sino que alimenta la siguiente iteración. Cada H0 no rechazada estrecha el espacio de búsqueda. El conocimiento avanza por eliminación de errores —de nuevo, Popper.}


# La Estadística

## ¿Qué es la estadística y para qué sirve?
 
La estadística es una forma de conocer el mundo en **términos cuantitativos**.
 
Tres propósitos:
 
1. **Resumir** datos — estadística descriptiva
2. **Explorar** datos — estadística exploratoria
3. **Relacionar** variables — estadística inferencial
Schweinberger añade una definición pragmática: un **dispositivo para ahorrar trabajo**.
 
\note{Los tres propósitos anticipan la estructura de cualquier curso de métodos. La definición pragmática ("labor-saving device") desmitifica: la estadística minimiza el esfuerzo de reportar resultados y de averiguar cómo se relacionan varias cosas. Vale la pena señalar que nuestro módulo se sitúa en el punto 2, aunque necesita el 1 como base.}
 
## La hipótesis en el centro
 
Retomando a Wilson (1999), la ciencia es:
 
> Una empresa sistemática que construye y organiza conocimiento en forma de **explicaciones y predicciones contrastables**.
 
Reformulado: **ciencia = testeo metódico de hipótesis**.
 
\note{Wilson, E.O. (1999), Consilience. La reformulación de Schweinberger es deliberadamente cruda pero eficaz: si el corazón de la ciencia son las explicaciones contrastables, y otro nombre para eso es "hipótesis", entonces hacer ciencia es testear hipótesis metódicamente. Esto justifica que el capítulo empiece por ahí.}
 
## Hoja de ruta
 
1. **Hipótesis** — nula vs. alternativa, dirigida vs. no dirigida, falsabilidad
2. **Datos y diseños** — experimental vs. observacional
3. **Variables y validez** — operacionalización y escalas de medición
4. **Relaciones entre variables** — correlación y causalidad
\note{El capítulo 1 justificaba por qué necesitamos método; este entrega el andamiaje concreto. La sección 3 es la más directamente útil para el EDA, porque la escala de medición determina qué visualizaciones y qué estadísticos tienen sentido.}
 
# 1. Hipótesis
 
## H0 y H1: el concepto ancla
 
- **Hipótesis alternativa (H1):** existe un efecto o relación
- **Hipótesis nula (H0):** no existe efecto
El testeo funciona de forma **indirecta**:
 
- Nunca probamos H1
- Evaluamos cuán **incompatibles** son los datos con H0
- Solo si los datos serían muy improbables bajo H0, la rechazamos
**Por eso las hipótesis se formulan *antes* de mirar los datos.**
 
\note{Este es el punto más contraintuitivo del capítulo y conviene insistir. La lógica del testeo es por reducción al absurdo probabilístico: asumimos que no hay efecto y vemos si los datos son compatibles con esa asunción. La advertencia final conecta directo con el cherry-picking del capítulo 1: formular hipótesis después de ver los datos (HARKing) invalida el procedimiento.}
 
## Falsabilidad
 
> *Las manzanas siempre caen hacia abajo.*
 
Un solo contraejemplo la falsa. Ninguna cantidad de evidencia a favor la prueba.
 
- **Es imposible probar una hipótesis empírica**
- Basta una observación refutadora
- Por eso buscamos falsar, no confirmar
\note{Retoma la asimetría popperiana del capítulo 1, ahora aplicada al trabajo concreto con hipótesis. El ejemplo de las manzanas admite reformulación para acomodar contraejemplos (en el espacio no caen): "las manzanas caen hacia el centro de gravedad dominante". Buen ejercicio en clase: pedir que reformulen hipótesis para hacerlas más robustas sin volverlas invulnerables.}
 
## La frontera: hipótesis vs. especulación
 
Enunciados que **no** pueden falsarse:
 
- *Hay formas de vida en la galaxia de Andrómeda* (razones técnicas)
- *Prefiero el helado de chocolate al de vainilla* (subjetivo)
Esto es **especulación**: fuera del alcance de la ciencia empírica.
 
No es algo negativo — el arte, la literatura, la música y la filosofía viven ahí.
 
\note{Importante el matiz final: Schweinberger insiste en que la especulación no es despreciable, solo pertenece a otro dominio. Para lingüistas es relevante porque buena parte de la teoría gramatical del siglo XX operaba en un régimen difícil de falsar, y eso motivó el giro empírico de los años 90.}
 
## Los cuatro criterios
 
Una hipótesis debe ser:
 
1. **Falsable** — sobre la realidad empírica
2. **Contrastable** — sobre el mundo empírico
3. **Inequívoca** — sin ambigüedad
4. **Internamente consistente**
La **universalidad no es requisito**: una hipótesis puede referirse a un evento singular y seguir siendo válida.
 
\note{Contraejemplo del texto: "si encontramos ciertos artefactos en cierta capa de tierra, el modelo arqueológico X es correcto" es singular pero falsable, y por tanto una hipótesis legítima. Contrasta con "fumar podría tener efectos negativos": el modal 'podría' la vuelve compatible con cualquier observación, y por eso NO es hipótesis.}
 
## Tipologías de hipótesis
 
| Distinción | Formulación |
|---|---|
| **No dirigida** | Los grupos A y B *difieren* ($\mu_A \neq \mu_B$) |
| **Dirigida** | A obtiene resultados *mayores* que B ($\mu_A > \mu_B$) |
| **Determinista** | La palabra corta *siempre* precede a la larga |
| **Probabilística** | Es *más probable* que la corta preceda a la larga |
 
\note{La distinción determinista/probabilística es especialmente pertinente en lingüística: casi ninguna regularidad lingüística es categórica. Trabajamos con preferencias, no con leyes sin excepción. Esto conecta con el argumento de Schneider y Lauber sobre por qué los lingüistas necesitan estadística: las diferencias son sutiles y graduales.}
 
## Por qué testeamos H0
 
En términos no técnicos: evaluamos **cuán probable es que el resultado se deba al azar**.
 
- $p > .05$ — probable que sea aleatorio $\to$ **no** descartamos H0
- $p < .05$ — improbable que sea aleatorio $\to$ descartamos H0, asumimos H1
\note{Bisagra hacia el capítulo 3 del curso original (probabilidad y distribución normal). Conviene anticipar aquí que el umbral .05 es una convención, no una ley natural, y que su uso mecánico está siendo cuestionado en la literatura metodológica reciente. Pero para efectos operativos, es el estándar que encontrarán en la bibliografía.}
 
# 2. Datos y diseños de investigación
 
## Muestra y población
 
Una **muestra** es una selección de **una** población —no de *la* población.
 
> Si la muestra incluye solo alemanes de 20 a 30 años, la población no es "todos los alemanes", sino los alemanes de esa franja etaria en ese momento.
 
Debemos ser conscientes sobre **qué población podemos realmente inferir**.
 
\note{El artículo indefinido no es un detalle gramatical: es una precisión conceptual. Cada decisión muestral define implícitamente una población distinta, y las conclusiones solo aplican a esa. Es exactamente el punto que desarrollamos en la sección de fundamentos de muestreo del módulo.}
 
## Diseño ≠ análisis
 
Dos pasos separados:
 
- **Diseño de investigación:** cómo se *recogen* los datos
- **Análisis de datos:** cómo se *analizan*
Por eso **no tiene sentido** hablar de "diseño cualitativo" o "diseño cuantitativo".
 
Cualquier diseño admite ambos enfoques analíticos.
 
\note{Error frecuente en propuestas de tesis. Un estudio de corpus (diseño observacional) puede analizarse cualitativa o cuantitativamente. Dicho eso, hay afinidades de hecho: los experimentos suelen analizarse cuantitativamente y las entrevistas cualitativamente, pero eso es costumbre disciplinar, no necesidad lógica.}
 
## La distinción central
 
**Experimental vs. observacional**, y el criterio que los separa es la causalidad:
 
- **Observacional:** solo confirma **correlaciones** (X e Y coocurren)
- **Experimental:** puede determinar **causalidad** (X causa Y)
\note{Esta es la razón de fondo por la que los diseños experimentales tienen el estatus que tienen. La asignación aleatoria a condiciones es lo que rompe la confusión con terceras variables. Sin ella, siempre queda abierta la posibilidad de un confounder no observado.}
 
## Diseños en ciencias del lenguaje
 
| Diseño | Ejemplo | V. interna | V. externa | Costo |
|---|---|---|---|---|
| **Experimental** | Tiempos de reacción | Alta | Baja | Alto |
| **Corpus** | Estudio variacionista | Baja/var. | Alta | Bajo* |
| **Archivo** | Revisión sistemática | Media | Baja | Bajo |
| **Introspección** | Juicios de gramaticalidad | Alta | Baja/var. | Bajo |
| **Cuestionario** | Encuesta de uso | Media | Media | Bajo |
 
\* Si el corpus ya existe; alto si hay que compilarlo.
 
\note{La tabla resume el compromiso fundamental: validez interna (precisión del control) versus validez externa (generalizabilidad al mundo real). Los experimentos ganan lo primero y pierden lo segundo; los corpus, al revés. No hay diseño superior en abstracto: depende de la pregunta.}
 
## Experimental y cuasi-experimental
 
**Experimental (true experiment):** asignación **aleatoria** a grupos de test y control.
 
**Cuasi-experimental:** sin asignación aleatoria $\to$ vulnerable a *confounding*.
 
Caen aquí:
 
- Estudios variacionistas de corpus
- Análisis de datos históricos (ya recogidos)
- Estudios de diferencias por sexo o edad
\note{Punto crítico para lingüistas: casi toda la sociolingüística variacionista y la lingüística de corpus es cuasi-experimental. No podemos asignar hablantes aleatoriamente a "ser mujer" o "haber nacido en 1950". Esto impone cautela permanente al interpretar causalidad, y conviene decirlo explícitamente en las secciones de limitaciones de las tesis.}
 
## Observacional: corpus
 
Los sujetos se observan en su **"hábitat natural"**.
 
- Alta **validez externa**: resultados transferibles al mundo real
- Precio: **sin control** sobre factores contextuales y de confusión
- Costo variable: mínimo si el corpus existe, alto si hay que grabar y transcribir
\note{El estudio de corpus típico busca patrones lingüísticos en textos (escritos o habla transcrita) y los correlaciona con otra característica: un sufijo, una construcción fija, dos períodos o dos dialectos. La ventaja de naturalidad es real, pero los factores no controlados pueden ser factores que ni siquiera sabemos que existen.}
 
## Introspección
 
La vieja **"lingüística de sillón"** (*armchair linguistics*).
 
- Dominante en el siglo XX
- La forma más barata y fácil de "recoger datos"
- **Subjetiva** y sesgada por expectativas y marco teórico
Desde los 90, relegada a **generación de hipótesis**, no como fuente única.
 
\note{Matiz importante: Schweinberger no la descarta. La introspección sigue siendo muy útil para generar hipótesis y detectar predictores potenciales que luego se testean empíricamente. Lo que cambió es su estatus: de fuente única de evidencia a paso preliminar dentro de un diseño más amplio.}
 
## Cuestionarios y elicitación
 
Métodos donde los informantes proveen información consciente:
 
- **Escalas Likert** (5 o 7 puntos): de *muy en desacuerdo* a *muy de acuerdo*
- **Discourse Completion Tasks (DCT):** imaginar un contexto y responder
Salvaguardas metodológicas:
 
- **Fillers** — ítems distractores contra *agreeability effects*
- **Aleatorización** de ítems contra *fatigue effects*
\note{Los DCT reflejan razonablemente el comportamiento real, pero son menos fiables que datos de corpus: los hablantes no siempre pueden informar con precisión sobre su propia conducta lingüística. Las dos salvaguardas son estándar y conviene exigirlas en cualquier diseño de cuestionario que revisen o propongan.}
 
# 3. Variables y validez
 
## Operacionalización: el concepto ancla
 
**Operacionalización:** traducir un concepto abstracto en algo concretamente medible.
 
| Concepto | Operacionalización posible |
|---|---|
| Competencia lingüística | Puntaje de un ensayo |
| Complejidad | Longitud media de enunciado |
| Cortesía | Frecuencia de atenuadores |
 
**Cada operacionalización es una elección.**
 
\note{Y su calidad determina la validez del estudio. La advertencia dura: si la medida no captura realmente el concepto, incluso un análisis estadístico impecable producirá resultados sin sentido. Ninguna sofisticación estadística rescata una mala operacionalización.}
 
## Dos tipos de validez
 
**Validez intrínseca:** correspondencia entre el concepto y la variable que lo mide.
 
- *Ej.:* complejidad $\to$ número de nodos sintácticos
**Validez externa:** aplicabilidad de los hallazgos al mundo real.
 
- *Ej.:* recordar sílabas sin sentido en laboratorio $\to$ ¿aprender vocabulario real?
\note{El ejemplo de las sílabas sin sentido es útil: se puede investigar experimentalmente qué método mejora su recuerdo, pero eso no garantiza que los hallazgos se transfieran a tareas de memoria del mundo real, como el aprendizaje de vocabulario. La validez externa es la pregunta de "¿y esto para qué sirve fuera del laboratorio?".}
 
## Variables dependientes e independientes
 
- **Independiente:** el predictor (lo que manipulamos o registramos como causa potencial)
- **Dependiente:** el resultado (lo que medimos como efecto)
*Ejemplo médico:* el fármaco (independiente) $\to$ presencia de síntomas (dependiente).
 
*Ejemplo lingüístico:* la edad del hablante (independiente) $\to$ frecuencia de sujeto nulo (dependiente).
 
\note{Ejercicio rápido del texto: "cuando llueve, más gente se moja". Dependiente = número de personas mojadas; independiente = lluvia. Suena trivial pero los estudiantes lo invierten con frecuencia cuando la relación no es obvia.}
 
## Escalas de medición
 
| Escala | Propiedad | Ejemplo lingüístico |
|---|---|---|
| **Nominal / categórica** | Solo pertenencia a clase | Parte del discurso |
| **Ordinal** | Orden sin distancias cuantificables | Juicios Likert, rangos |
| **Intervalo** | Diferencias sí, razones no | Juicios de aceptabilidad |
| **Razón** | Diferencias y razones | Duración, nº de sílabas |
| **Conteos** | Enteros positivos, frecuencias | Errores por 1000 palabras |
 
\note{20 °C no es "el doble de calor" que 10 °C: eso es intervalo. En cambio 10 segundos sí es exactamente el doble de 5: eso es razón. Los conteos son un subtipo de razón, pero requieren modelos propios (Poisson, binomial negativa) en vez de gaussianos, lo cual importa cuando lleguemos a modelado.}
 
## La escala dicta el test
 
Consecuencia práctica directa:
 
- $\chi^2$ $\to$ solo variables **nominales/categóricas**
- $t$-test $\to$ solo variables **numéricas**
**Elegir mal la operacionalización cierra puertas analíticas.**
 
\note{Este es el argumento más operativo del capítulo para nuestro módulo. La escala determina no solo qué test es posible, sino también qué visualización tiene sentido: un histograma requiere numérico, un gráfico de barras funciona con categórico, un box plot compara numérico entre grupos. Conecta directamente con la Semana 2 del módulo.}
 
## La jerarquía es unidireccional
 
$$\text{nominal/categórica} < \text{ordinal} < \text{intervalo/razón}$$
 
Se puede **degradar** una variable, **nunca ascender**.
 
*Ejemplo:* demasiados hablantes con cero palabrotas $\to$ se viola la normalidad de residuos.
 
- Opción A: rankear hablantes $\to$ Mann-Whitney U
- Opción B: dicotomizar (usa / no usa) $\to$ $\chi^2$
\note{Transformar categórico en numérico equivaliría a inventar información que no está en los datos. El ejemplo del texto es elegante porque muestra una salida real ante un supuesto violado: en vez de forzar una regresión lineal inadecuada, se degrada la variable a un nivel donde existen tests apropiados. Se pierde potencia, pero se gana validez.}
 
# 4. Relaciones entre variables
 
## Cuatro dimensiones de una correlación
 
- **Fuerza** — ¿cuánto explica una variable la variabilidad de la otra?
- **Dirección** — ¿positiva o negativa?
- **Linealidad** — ¿es constante la relación?
- **Homogeneidad** — ¿es consistente?
Fuerza y dirección son **ortogonales**: una correlación negativa puede ser tan fuerte como una positiva.
 
\note{La fuerza se lee visualmente en la dispersión respecto de la recta de regresión: cuanto más pegados los puntos a la línea, más fuerte. Correlación positiva = "a mayor X, mayor Y"; negativa = "a mayor X, menor Y". El signo no dice nada sobre la magnitud.}
 
## Correlación espuria
 
> *Los estudiantes que beben más café sacan mejores notas.*
 
¿Causa el café las buenas notas?
 
. . .
 
**No necesariamente.** El **tiempo de estudio** puede causar ambas cosas.
 
Una tercera variable explica la asociación observada.
 
\note{El `. . .` genera la pausa incremental. Este es el cierre lógico del capítulo: conecta de vuelta con por qué los diseños observacionales no pueden establecer causalidad. Si no controlamos la tercera variable, la correlación observada no autoriza ninguna inferencia causal. Advertencia permanente para trabajo con corpus.}
 
## Cierre
 
 
| Concepto del capítulo | En nuestro módulo |
|---|---|
| Hipótesis previas a los datos | El EDA explora; no reemplaza el preregistro |
| Diseño y muestra | Fundamentos de muestreo (Semana 0) |
| Escalas de medición | Tipología de datos (Semana 1) |
| Correlación y dirección | Medidas de asociación (Semana 3–4) |
| Correlación espuria | Interpretación cautelosa (Semana 5) |
 
\note{Cierre que tiende el puente al resto del módulo. La sección de variables es la que alimenta más directamente nuestro trabajo: sin clasificar bien las variables, ni las visualizaciones ni los estadísticos descriptivos tienen sentido.}
 
---
 
> Una hipótesis es un enunciado **falsable**; el testeo evalúa la compatibilidad de los datos con **H0**, no la verdad de H1.
 
> La **operacionalización** es una elección que determina la validez: ningún análisis rescata una mala medida.
 
> La **escala de medición** decide qué análisis y qué visualización son posibles.
 
\note{Las tres ideas que deben quedar. Si los estudiantes se llevan solo una, que sea la del medio: la calidad de la medida antecede a la calidad del análisis, y es donde más frecuentemente fallan los diseños de tesis.}

---


| **Fundamento** | **En el EDA** |
|---|---|
| Sesgo de confirmación | No quedarse solo con la visualización que confirma |
| Falsación | El EDA sugiere; validar exige refutar en datos nuevos |
| Patrones en el ruido | Distinguir patrón genuino de azar del corpus |
| Correlación ≠ causalidad | Una asociación no establece mecanismo causal |
| Pensamiento lento | El EDA es "pensamiento lento" sobre los datos |

\note{Cierre que tiende el puente hacia el resto del módulo. El EDA no es un procedimiento para confirmar sospechas, sino para VER lo que hay —sobre todo lo inesperado y lo que contradice la intuición. Su valor está en su capacidad de sorprendernos y corregirnos.}

## Para retener

> El **EDA no confirma** lo que ya sospechas.
>
> Es un procedimiento para **ver lo que hay** —incluyendo lo que no esperabas y lo que contradice tu intuición.

Su valor está precisamente en su capacidad de **sorprenderte y corregirte**.

\note{La idea que debe quedar. Si los estudiantes se llevan una sola frase, que sea esta. Prepara el terreno para las semanas siguientes, donde la disciplina de "mirar antes de concluir" será el hábito central.}

## Referencias


- Evans, V., & Green, M. (2006). *Cognitive Linguistics: An Introduction.* Edinburgh UP.
- Hood, B. M. (2009). *SuperSense.* HarperOne.
- Kahneman, D. (2011). *Thinking, Fast and Slow.* Farrar, Straus and Giroux.
- Popper, K. R. (1959). *The Logic of Scientific Discovery.* Hutchinson.
- Sagan, C. (1995). *The Demon-Haunted World.* Ballantine Books.
- Schweinberger, M. *Statistics for Linguists* (SLAT7855), cap. 1. University of Queensland.

\note{Bibliografía en cuerpo reducido para que quepa en una slide. Las fuentes primarias para profundizar son Kahneman (sesgos) y Popper (falsación).}


---


## Referencias
 
 
- Schweinberger, M. *Statistics for Linguists* (SLAT7855), cap. 2: Hypotheses and Variables. University of Queensland.
- Wilson, E. O. (1999). "The Natural Sciences". En *Consilience: The Unity of Knowledge*, 49–71.
- Popper, K. R. (1959). *The Logic of Scientific Discovery.* Hutchinson.
- Gries, S. T. (2021). *Statistics for Linguistics with R* (3ª ed.). Mouton de Gruyter.
\note{Para profundizar en operacionalización y escalas aplicadas a datos lingüísticos, Gries (2021) es la referencia más directa y con ejemplos en R.}

