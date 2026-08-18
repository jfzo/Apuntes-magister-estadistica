---
title: EST-741
subtitle: Módulo Capstone 1, Modelación y Validación
author: Juan Zamora O.
date: Taller de Consultoría
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
linespread: 1.2
---

## Dónde estamos

- Semana 1: definieron su Statement of Work 
    - pregunta, tarea, métrica, protocolo de validación
- Semana 2: construyeron un modelo base (baseline) 
- Semana 3 (**Hoy:**) Diseñan pipeline, iteran con métodos de aprendizaje automático, avanzan su tabla de experimentos, y revisan su código en equipo

::: notes
Conectar explícitamente con las dos sesiones anteriores da continuidad. Recordar brevemente qué baseline usó cada equipo, si el tiempo lo permite, antes de avanzar.
:::


## Objetivo de la sesión

Que cada equipo llegue al final de la sesión con:

1. Métodos de aprendizaje automático aplicados y justificados
2. Código actual revisado en equipo, con registro de hallazgos a la fecha
3. Tabla de experimentos en construcción, aunque no esté completa
4. Riesgos identificados, con una idea concreta de cómo abordarlos


::: {.special-note .warning}
### Importante
*No se espera un modelo final ni resultados definitivos. Se espera evidencia de avance en trabajo metodológico.*
:::

::: notes
Enfatizar la última línea: esto suele generar ansiedad en los equipos si no se dice explícitamente. El hito no premia tener el mejor número, premia el rigor del proceso.
:::


# Estructura de la sesión

::: notes
Transición a la agenda operativa. Proyectar esta diapositiva y la siguiente tabla mientras se explica el flujo completo, antes de que los equipos pasen a trabajar.
:::


## Agenda

1. Inicio de la sesión (Apertura)
1. Revisión de código: Lectura individual y luego discusión en equipo. 
1. Pipeline de modelos y experimentos más elaboración de tabla con experimentos
1. Exposiciones (hito evaluado): Cada equipo presenta su avance (6-8 mins máximo)


::: notes
Si el curso tiene más de 4 equipos, ajustar la duración de las exposiciones o dividir en dos bloques con receso, manteniendo fijos los minutos por equipo.
:::


## Etapa 1: Revisión de código en equipo

- Revisión individual de código por cada integrante
- Discusión de los hallazgos en equipo y clasificación como **obstaculizantes** o **por-mejorar**
- Todo hallazgo obstaculizante se registra como _issue_ en el repositorio  (en caso que lo tengan ya creado)

**Resultados esperados**: Hallazgos y sus clasificaciones

::: notes
Los obstaculizantes son factores, condiciones o acciones que dificultan, retrasan o impiden lograr una meta, resolver un problema o avanzar en un proceso.

Recordar brevemente por qué el orden importa: la lectura silenciosa primero evita que la opinión del primero en hablar contamine el juicio del resto del equipo.
:::


## Etapa 2: Pipeline de modelos y experimentos

- Probar los métodos de aprendizaje automático pertinentes a su tarea respectiva
- Cada experimento se registra en la tabla: modelo, hiperparámetros, semilla, mecanismo de validación (crossvalidation u otro), resultado frente al baseline
- No es necesario cerrar la tabla hoy, pero sí es necesario que lo registrado sea comparable y reproducible

::: notes
El profesor rota entre salas durante este bloque, como en sesiones anteriores, con una pregunta preparada para cada equipo en vez de simplemente observar.
:::


# Hito evaluado

::: notes
Transición al bloque evaluado. Aquí conviene bajar el ritmo y asegurarse de que la instrucción quede clara antes de que empiecen a trabajar, porque después no habrá otra oportunidad de aclarar dudas sobre el formato antes de exponer.
:::


## Acerca de la exposición

- Cada equipo dispone de **8 minutos**
- Expone quien el equipo decida, ojalá no hable la misma persona que en la Semana anterior.

*No se evalúa qué tan bueno es el modelo. Se evalúa qué tan bien pueden explicar y defender su avance.*

::: notes
Repetir esta última línea es intencional — es el mensaje que más ansiedad reduce en los equipos antes de exponer.
:::


## Checklist: qué debe incluir su presentación

- [ ] **Métodos aplicados**: cuáles probaron y por qué son pertinentes para su tarea (no solo que funcionan)
- [ ] **Estado del código**: el pipeline corre de forma reproducible; validación respeta el orden temporal
- [ ] **Tabla de experimentos**: lo que llevan hasta ahora, comparable frente al mismo baseline y métrica
- [ ] **Qué falta**: qué experimentos tienen pendientes y por qué, si la tabla no está cerrada
- [ ] **Riesgos identificados**: al menos uno o dos riesgos concretos de su enfoque (no genéricos)
- [ ] **Cómo piensan abordarlos**: una idea concreta por riesgo, no solo nombrarlo

::: notes
Esta diapositiva es la más importante de toda la presentación — sugerir dejarla proyectada o compartida en el chat durante todo el bloque de trabajo, para que los equipos la usen como pauta de armado mientras preparan su exposición.
:::


## Antes de exponer, revisen esto

Si un ítem del checklist no está listo, no esconderlo. Lo **relevante** es evidenciarlo y tener claro cómo abordarlo.

- La honestidad metodológica es parte de lo que se evalúa
- Mejor mostrar un riesgo bien identificado que un resultado forzado para parecer más avanzado

::: notes
Conectar con la ética profesional de la consultoría: un consultor que oculta un riesgo para parecer más avanzado pierde la confianza del cliente apenas se descubre.
:::


## Próxima sesión (último hito)

- Riesgos mitigados
- Pipeline completo
- Reporte de la solución y resultados al cliente (EL profe.)


::: notes
Cierre operativo. Recordar el horario exacto de inicio de las exposiciones para que los equipos administren bien su tiempo de trabajo en los dos primeros bloques.
:::