---
title: EST-741
subtitle: Módulo Capstone 1, El Baseline
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
---



# ¿Qué es un modelo línea base?

::: notes
Diapositiva de apertura. Preguntar al plenario: "¿alguien ya calculó un baseline para su proyecto?" antes de dar la definición formal.
:::

---

## Definición

- La regla de predicción **más simple, honesta y barata** de construir para un problema dado
- Es el punto de comparación obligatorio contra el cual se justifica cualquier modelo más sofisticado
- Su función **no es predecir bien**: es fijar el umbral mínimo de valor que un modelo debe superar

::: notes
Insistir en "no es predecir bien" — es un punto de referencia, no un competidor serio. Esto suele generar confusión al principio.
:::

---

## Analogía con el grupo control

- Sin grupo control, no se puede saber si el tratamiento causó una mejora real
- Sin baseline, no se puede saber si el modelo avanzado aporta valor real
- Reportar un modelo sin baseline es el mismo error metodológico que reportar un experimento sin grupo control

::: notes
Esta analogía suele ser la que más queda. Dar tiempo para que se asimile antes de avanzar a las condiciones.
:::

---

## Dos condiciones de un buen baseline

1. **No debe usar el conocimiento que el modelo avanzado intenta capturar**
   - Si ya usa relaciones complejas, deja de ser un punto de referencia útil
2. **Debe ser trivial de calcular y de explicar a un cliente no técnico**
   - Si necesita justificación técnica, no cumple su rol de ancla

::: notes
Pedir ejemplos de baselines "tramposos" — que en realidad ya incorporan la señal que se quiere medir. Es un buen chequeo de comprensión.
:::

---

## El baseline depende del tipo de tarea

| Tipo de tarea | Baseline típico |
|---|---|
| Regresión | Predecir siempre la media (o mediana) de la variable objetivo |
| Clasificación | Predecir siempre la clase mayoritaria |
| Forecasting | Persistencia: "mañana = hoy" o "esta semana = misma semana del año pasado" |
| Datos no estructurados | Reglas simples o frecuencia de palabras, antes de un modelo de lenguaje complejo |

::: notes
No es necesario memorizar la tabla; el criterio detrás de cada fila es lo importante: ¿cuál es la apuesta más simple que ya usa la estructura evidente del fenómeno?
:::

---

## Ejemplo: ventas semanales por tienda

**Paso 1 — Identificar candidatos**

- Persistencia simple: ventas de esta semana = ventas de la semana pasada
- Persistencia estacional: ventas de esta semana = misma semana, año anterior
- Media histórica de la tienda

::: notes
Recordar que este es el mismo caso usado en la Sesión 1. Conecta ambos contenidos y refuerza la continuidad del framing.
:::

---

## Ejemplo: elegir el baseline correcto

**Paso 2 — Elegir el más razonable dado el fenómeno**

- Las ventas retail tienen estacionalidad fuerte (Navidad, vuelta a clases)
- La persistencia estacional es más justa que la simple
- Usar un baseline "demasiado fácil de vencer" infla artificialmente el mérito del modelo avanzado

::: notes
Este es el punto donde más se equivocan los equipos: eligen el baseline más simple posible sin pensar si es representativo del fenómeno.
:::

---

## Ejemplo: fijar el umbral

**Paso 3 — Declarar el umbral de mejora, antes de entrenar nada más**

> El modelo candidato debe lograr un error ≥ 15% mejor que el baseline estacional para justificarse.

- Si el modelo avanzado apenas iguala este número, la complejidad adicional no se justifica
- Esa es la conclusión honesta que se comunica al cliente, no un fracaso del proyecto

::: notes
Enfatizar: "no superar el baseline" es un resultado válido y reportable, no un fallo que hay que esconder. Es parte de la honestidad profesional que exige el curso.
:::

---

## Un error frecuente a evitar

- Elegir un baseline débil a propósito (por ejemplo, predecir siempre cero)
- Así el modelo avanzado "luce mejor" en la comparación
- Es una forma sutil de sesgo de reporte que compromete la credibilidad del informe

::: notes
Cerrar con esta advertencia como puente hacia la ética profesional de la consultoría: el cliente confía en que la comparación fue justa.
:::

