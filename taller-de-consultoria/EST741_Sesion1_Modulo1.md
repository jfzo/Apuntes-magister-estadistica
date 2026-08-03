---
title: EST-741
subtitle: Módulo Capstone 1, Sesión 1
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


# Organización de la sesión
 
 - Plenario con:
  - Organización del curso
  - Lanzamiento del trabajo
- Trabajo en salas para generar SoW
- Plenario: Conclusiones y siguiente etapa

 
---
  
## Antes de elegir un modelo, hay que elegir la pregunta
 
- El error más caro de la Semana 1 no es técnico: es empezar a modelar sin haber fijado la pregunta
- **Analogía:** no se ordena una resonancia antes de precisar la pregunta clínica
- Elegir el modelo antes de fijar la pregunta y la métrica es pedir el examen antes del diagnóstico

::: notes
Abrir con la analogía médica y dejar que resuene unos segundos antes de avanzar. Enfatizar que esto no es teoría abstracta: es exactamente lo que van a necesitar para el Statement of Work de esta misma semana.
:::
 

## Organización de las sesiones

Qué ocurre en cada sesión y entre sesiones.

---
 
## Cuatro decisiones antes de tocar un modelo
 
1. **Tarea predictiva** — ¿qué tipo de problema es?
2. **Variable objetivo** — ¿qué exactamente se predice?
3. **Unidad de análisis** — ¿sobre qué se hace cada predicción?
4. **Métrica de éxito** — ¿cómo sabremos si el modelo sirve?
> Marco basado en Provost & Fawcett (2013), *Data Science for Business*, O'Reilly — referencia estándar de la industria para este paso.
 
::: notes
Estas cuatro decisiones son el hilo conductor del resto del bloque; cada una se profundiza en la diapositiva siguiente. Mencionar que el orden importa: variable objetivo depende de la unidad de análisis, no al revés.
:::
 
---
 
## 1. Tarea predictiva
 
- **Clasificación**: ¿va a ocurrir un evento? (ej.: ¿el cliente cancelará?)
- **Regresión**: ¿cuánto va a valer una cantidad continua?
- **Forecasting (series temporales)**: ¿cuánto va a valer algo *en el futuro*, dado su historial?
- **Datos no estructurados**: texto o imágenes como insumo de cualquiera de las anteriores
*El prompt del cliente rara vez lo dice explícitamente — hay que inferirlo de la pregunta de negocio.*
 
::: notes
Pedir a un par de estudiantes que traten de ubicar su propio prompt en una de estas categorías, en voz alta, sin resolverlo del todo — solo para activar el pensamiento antes de pasar a salas.
:::
 
---
 
## 2. Variable objetivo y unidad de análisis
 
- **Variable objetivo**: la columna exacta que el modelo va a predecir
  - Cuidado con variables "proxy" que filtran información del futuro (*data leakage*)
- **Unidad de análisis**: la fila sobre la que se predice
  - ¿Por cliente? ¿por día? ¿por tienda-día? ¿por producto-semana?
*Un error frecuente: definir la variable objetivo antes de definir la unidad de análisis, en vez de al revés.*
 
::: notes
Si el tiempo lo permite, dar un ejemplo breve de data leakage con una variable que solo se conoce después del evento que se quiere predecir. Este es el punto donde más dudas suelen surgir.
:::
 
---
 
## 3. Métrica de éxito
 
- La métrica estadística debe **traducirse** a una métrica de negocio
- Ejemplos:
  - MAE vs. RMSE → ¿los errores grandes son mucho más costosos que los pequeños?
  - Precisión vs. recall → ¿es peor una falsa alarma o una detección perdida?
- La métrica se fija **antes** de ver el desempeño del primer modelo, no después

::: notes
Insistir en el "antes, no después": es la garantía metodológica contra el ajuste retroactivo de criterios de éxito una vez que ya se conoce el resultado del modelo.
:::
 
---
 
## 4. Protocolo de validación
 
- **En series temporales, nunca validación cruzada ingenua**
- El futuro no puede usarse para predecir el pasado durante el entrenamiento
- Alternativas correctas:
  - Partición temporal simple (train = pasado, test = futuro)
  - *Walk-forward validation* (ventana deslizante)
> Este protocolo se declara en el Statement of Work y se verifica en la demo del pipeline (Semana 2).
 
::: notes
Conectar explícitamente con el entregable de la Semana 2: lo que se declara aquí se audita en vivo en la demo del pipeline. Esto da peso real a la decisión, no es un ejercicio teórico.
:::
 
---
 
## Checklist de cierre del Momento 1
 
- [ ] Tipo de tarea predictiva identificado
- [ ] Variable objetivo definida sin fuga de información
- [ ] Unidad de análisis explícita
- [ ] Métrica de éxito ligada a una decisión de negocio
- [ ] Protocolo de validación temporal elegido
*Estas cinco líneas son el esqueleto del Statement of Work de 2 páginas.*
 
::: notes
Dejar esta diapositiva proyectada mientras se hace la transición al Momento 2; sirve como referencia visual constante durante el ejemplo resuelto.
:::
 
---
 
# Momento 2: Ejemplo resuelto en vivo
 
::: notes
Duración: 10 minutos, en plenario. El objetivo es modelar el razonamiento del Momento 1 con un caso ajeno, para no condicionar la respuesta de ningún equipo sobre su propio prompt.
:::
 
---
 
## Caso ilustrativo (no es el prompt del Cliente 1)
 
**Contexto:** una cadena de comercio minorista quiere anticipar cuánto va a vender cada tienda la próxima semana, para ajustar su dotación de personal.
 
*Se usa un caso distinto al de cada equipo para modelar el razonamiento sin condicionar la respuesta de nadie sobre su propio caso.*
 
::: notes
Aclarar en voz alta que este caso es deliberadamente distinto al del Cliente 1, para que nadie intente copiar la solución literal en vez de el razonamiento.
:::
 
---
 
## Aplicando las cuatro decisiones
 
| Decisión | Respuesta en este caso |
|---|---|
| Tarea predictiva | Forecasting (serie temporal) |
| Variable objetivo | Ventas totales (\$) por tienda y semana |
| Unidad de análisis | Tienda-semana |
| Métrica de éxito | MAE en \$, ponderado por el costo de sub-dotación de personal |
 
::: notes
Recorrer la tabla fila por fila, señalando en cada una a qué pregunta del Momento 1 responde. Es el momento de cerrar el círculo entre marco teórico y aplicación concreta.
:::
 
---
 
## Protocolo de validación del ejemplo
 
- Historial: 3 años de ventas semanales por tienda
- Partición: últimas 8 semanas como test, resto como entrenamiento
- Línea base ingenua: "esta semana = misma semana el año anterior"
- Cualquier modelo candidato debe **superar** esa línea base para justificarse
::: notes
Enfatizar la línea base ingenua como criterio de justificación: un modelo complejo que no supera esto no se justifica, sin importar cuán sofisticado sea.
:::
 
---
 
## Resultado: mini-SOW del ejemplo
 
> **Pregunta de negocio:** ¿Cuánta dotación de personal necesita cada tienda la próxima semana?
>
> **Tarea:** forecasting semanal por tienda
> **Métrica de éxito:** MAE en \$, mejora ≥ 15% sobre la línea base ingenua
> **Validación:** partición temporal, últimas 8 semanas como test
 
*Esto es exactamente el formato que cada equipo debe producir para su propio prompt.*
 
::: notes
Señalar que este bloque de cuatro líneas es literalmente la plantilla que van a llenar con su propio caso en la sala. No hay nada oculto o adicional que se espere del Statement of Work más allá de esto, bien argumentado.
:::
 
---
 
## Transición al trabajo en salas
 
- Cada equipo aplica este mismo marco a los datos y el prompt del Cliente 1
- Producto esperado al cierre de la sesión: borrador de las cuatro decisiones
- Producto evaluado en la Sesión B de esta semana: Statement of Work de 2 páginas
**A trabajar.**
 
::: notes
Antes de enviar a salas, recordar la regla del issue con etiqueta blocker: cualquier duda que surja en la sala y no se resuelva entre el equipo debe quedar registrada ahí para la visita del profesor.
:::