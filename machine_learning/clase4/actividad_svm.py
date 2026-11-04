#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
EST852 Machine Learning | Actividad práctica: SVM para diagnóstico de cáncer de mama
=====================================================================================

Datos: Breast Cancer Wisconsin (Diagnostic), incluido en scikit-learn
       (569 casos, 30 variables; y = 0 maligno, y = 1 benigno).

CÓMO LEER ESTE ARCHIVO
----------------------
El archivo tiene tres tipos de bloque. Se distinguen a simple vista:

  1. ENUNCIADO      Recuadro de signos "=" con el título "ENUNCIADO <paso>".
                    Es lo que lee el estudiante: qué hacer y qué responder.

  2. CÓDIGO DADO    Línea "# [CÓDIGO DADO]". Preparación que se entrega ya
                    escrita a los estudiantes (no es una solución).

  3. SOLUCIÓN       Todo lo que está entre las líneas
                        # >>>>>>>>>> SOLUCIÓN <paso> >>>>>>>>>>
                        # <<<<<<<<<< FIN SOLUCIÓN <paso> <<<<<<<<<<
                    Es solo para el docente. Para obtener la versión de los
                    estudiantes se borra cada bloque de solución y se deja el
                    enunciado (cada paso queda con su recuadro y sin código).

ESTRUCTURA
----------
  Parte A (en clase, 25 min, en parejas):  A1, A2, A3, A4
  Parte B (tarea, entrega la próxima sesión): B1, B2, B3, B4, B5

  Los pasos siguen el ciclo "predecir, ejecutar, explicar": la pareja anota su
  predicción ANTES de correr el código.

EJECUCIÓN
---------
  python actividad_svm.py

  También funciona por celdas (marcadores "# %%") en VS Code, Spyder o Jupytext.
  Requiere numpy, scikit-learn y matplotlib. Probado con scikit-learn 1.9.1.
  Las figuras se guardan en la carpeta DIR_FIGURAS; con MOSTRAR_FIGURAS = True
  también se abren en pantalla.

REFERENCIAS DEL PLAN
--------------------
  Cada resultado de la solución se contrasta con la cifra de referencia del plan
  de la sesión mediante `chequear(...)`. Las líneas "[OK ]" coinciden y las
  "[DIF]" difieren. Diferencias de uno o dos casos entre versiones de
  scikit-learn son normales; no detienen la ejecución.
"""

# %% ---------------------------------------------------------------------------
# [CÓDIGO DADO] Configuración, importaciones y utilidades (común a todos los pasos)
# ------------------------------------------------------------------------------
import os

import matplotlib
import numpy as np

SEMILLA = 0                    # misma partición que las cifras de referencia
MOSTRAR_FIGURAS = False        # True: además de guardar, abre cada figura
DIR_FIGURAS = "figuras_actividad"

if not MOSTRAR_FIGURAS:
    matplotlib.use("Agg")      # sin ventana: sirve en servidores y en Colab
import matplotlib.pyplot as plt  # noqa: E402

from sklearn.datasets import load_breast_cancer, make_moons  # noqa: E402
from sklearn.metrics import confusion_matrix, recall_score  # noqa: E402
from sklearn.metrics.pairwise import euclidean_distances, rbf_kernel  # noqa: E402
from sklearn.model_selection import (GridSearchCV, cross_val_score,  # noqa: E402
                                     train_test_split)
from sklearn.pipeline import make_pipeline  # noqa: E402
from sklearn.preprocessing import StandardScaler  # noqa: E402
from sklearn.svm import SVC  # noqa: E402

RESULTADOS = []                # (nombre, coincide) de cada contraste con el plan


def titulo(texto):
    print("\n" + "=" * 78 + f"\n{texto}\n" + "=" * 78)


def chequear(nombre, obtenido, esperado, tol=5e-4):
    """Contrasta un resultado con la cifra de referencia del plan (tolerancia absoluta)."""
    obt = np.asarray(obtenido, dtype=float)
    esp = np.asarray(esperado, dtype=float)
    ok = obt.shape == esp.shape and bool(np.allclose(obt, esp, atol=tol, rtol=0))
    RESULTADOS.append((nombre, ok))
    print(f"  [{'OK ' if ok else 'DIF'}] {nombre}: obtenido={np.round(obt, 4).tolist()}"
          f" | referencia={esp.tolist()}")
    return ok


def guardar(fig, nombre):
    os.makedirs(DIR_FIGURAS, exist_ok=True)
    ruta = os.path.join(DIR_FIGURAS, nombre)
    fig.savefig(ruta, dpi=150, bbox_inches="tight")
    if MOSTRAR_FIGURAS:
        plt.show()
    plt.close(fig)
    print(f"  figura guardada en {ruta}")


# ##############################################################################
# ##############################################################################
#                       PARTE A  |  EN CLASE (25 MIN, EN PAREJAS)
# ##############################################################################
# ##############################################################################


# %% ---------------------------------------------------------------------------
# ==============================================================================
# ENUNCIADO A1  |  5 min  |  Datos, partición y escalas
# ==============================================================================
#   1. Cargue el conjunto Breast Cancer Wisconsin con `load_breast_cancer`.
#   2. Particione en entrenamiento y prueba: 70 % / 30 %, estratificado por la
#      clase y con `random_state=0`.
#   3. Imprima cuántos casos quedan en cada conjunto.
#   4. Calcule el rango (máximo menos mínimo) de cada variable e imprima el
#      menor y el mayor, con el nombre de la variable.
#
#   PREGUNTA: el kernel RBF depende de la distancia euclídea entre puntos.
#   ¿Qué le pasa a esa distancia si una variable tiene un rango miles de veces
#   mayor que otra?
# ==============================================================================

# >>>>>>>>>> SOLUCIÓN A1 >>>>>>>>>>
titulo("A1. Datos, partición y escalas")
datos = load_breast_cancer()
X, y = datos.data, datos.target            # y: 0 = maligno, 1 = benigno
Xtr, Xte, ytr, yte = train_test_split(
    X, y, test_size=0.3, stratify=y, random_state=SEMILLA)
print(f"casos: entrenamiento={len(ytr)}, prueba={len(yte)}; variables={X.shape[1]}")
print(f"clases en el total (maligno, benigno) = {np.bincount(y).tolist()}")

rangos = np.ptp(X, axis=0)
i_min, i_max = int(rangos.argmin()), int(rangos.argmax())
print(f"rango menor: {rangos[i_min]:.4f}  ({datos.feature_names[i_min]})")
print(f"rango mayor: {rangos[i_max]:.1f}  ({datos.feature_names[i_max]})")
chequear("A1 casos de entrenamiento y prueba", [len(ytr), len(yte)], [398, 171], tol=0)
chequear("A1 rango menor y mayor", [rangos.min(), rangos.max()], [0.0289, 4068.8], tol=0.05)

# Respuesta: en la distancia euclídea la variable de rango ~4000 domina por completo
# y las variables de rango ~0,03 casi no cuentan. El kernel RBF "ve" entonces una
# sola variable. Por eso el paso A2 compara con y sin estandarizar.
# <<<<<<<<<< FIN SOLUCIÓN A1 <<<<<<<<<<


# %% ---------------------------------------------------------------------------
# ==============================================================================
# ENUNCIADO A2  |  7 min  |  Kernel RBF: sin escalar frente a escalado
# ==============================================================================
#   ANTES DE EJECUTAR, anote su predicción: ¿cuál de los dos modelos tendrá
#   mejor exactitud en prueba y por cuánto?
#
#   1. Ajuste `SVC(kernel="rbf")` con los datos de entrenamiento SIN escalar.
#   2. Ajuste un `Pipeline` con `StandardScaler()` y `SVC(kernel="rbf")`.
#   3. Imprima la exactitud de ambos modelos sobre el conjunto de prueba.
#
#   PREGUNTA: ¿por qué se escala dentro de un `Pipeline` y no se aplica
#   `StandardScaler` a todo X antes de particionar?
# ==============================================================================

# >>>>>>>>>> SOLUCIÓN A2 >>>>>>>>>>
titulo("A2. RBF sin escalar frente a escalado")
sin_escalar = SVC(kernel="rbf").fit(Xtr, ytr)
escalado = make_pipeline(StandardScaler(), SVC(kernel="rbf")).fit(Xtr, ytr)
acc_sin = sin_escalar.score(Xte, yte)
acc_esc = escalado.score(Xte, yte)
print(f"exactitud en prueba, sin escalar: {acc_sin:.3f}")
print(f"exactitud en prueba, escalado:    {acc_esc:.3f}")
chequear("A2 exactitud sin escalar y escalado", [acc_sin, acc_esc], [0.906, 0.953])

# Respuesta: si se escalara todo X antes de particionar, la media y la desviación
# estándar usarían información del conjunto de prueba (fuga de información). En el
# Pipeline, StandardScaler se ajusta solo con los datos de entrenamiento y, dentro
# de la validación cruzada, solo con cada pliegue de entrenamiento.
# <<<<<<<<<< FIN SOLUCIÓN A2 <<<<<<<<<<


# %% ---------------------------------------------------------------------------
# ==============================================================================
# ENUNCIADO A3  |  6 min  |  Kernel lineal frente a RBF
# ==============================================================================
#   ANTES DE EJECUTAR, anote su predicción: ¿cuál kernel tendrá más vectores
#   soporte y cuál mejor exactitud de validación cruzada?
#
#   Para `kernel` en ["linear", "rbf"], con `StandardScaler` dentro de un
#   `Pipeline`:
#     1. Calcule la exactitud media de validación cruzada de 5 pliegues sobre
#        el conjunto de entrenamiento (`cross_val_score`).
#     2. Ajuste el modelo e imprima el número total de vectores soporte
#        (`n_support_` del paso "svc").
#
#   PREGUNTA: con estos resultados, ¿se justifica el kernel RBF?
# ==============================================================================

# >>>>>>>>>> SOLUCIÓN A3 >>>>>>>>>>
titulo("A3. Kernel lineal frente a RBF")
cv_acc, n_vs = {}, {}
for kernel in ["linear", "rbf"]:
    modelo = make_pipeline(StandardScaler(), SVC(kernel=kernel))
    cv_acc[kernel] = cross_val_score(modelo, Xtr, ytr, cv=5).mean()
    n_vs[kernel] = int(modelo.fit(Xtr, ytr)["svc"].n_support_.sum())
    print(f"{kernel:>6}: validación cruzada = {cv_acc[kernel]:.3f}, "
          f"vectores soporte = {n_vs[kernel]}")
chequear("A3 validación cruzada lineal y RBF", [cv_acc["linear"], cv_acc["rbf"]],
         [0.975, 0.980])
chequear("A3 vectores soporte lineal y RBF", [n_vs["linear"], n_vs["rbf"]], [27, 96],
         tol=0)

# Respuesta: el RBF usa más vectores soporte (96 frente a 27) y su ventaja en
# validación cruzada es de medio punto porcentual, dentro del ruido. En este
# conjunto el kernel lineal basta. El paso B5(b) lo comprueba con 30 particiones.
# <<<<<<<<<< FIN SOLUCIÓN A3 <<<<<<<<<<


# %% ---------------------------------------------------------------------------
# ==============================================================================
# ENUNCIADO A4  |  7 min  |  Grilla gruesa de C y gamma
# ==============================================================================
#   ANTES DE EJECUTAR, anote su predicción: ¿qué combinación de (C, gamma) ganará
#   y qué pasará con los valores grandes de gamma?
#
#   1. Defina la grilla  C in [0.1, 1, 10, 100]  y  gamma in [0.001, 0.01, 0.1, 1].
#   2. Ejecute `GridSearchCV` con un `Pipeline` (StandardScaler + SVC), 5 pliegues,
#      sobre el conjunto de entrenamiento.
#   3. Imprima los mejores parámetros y su exactitud de validación cruzada.
#   4. Imprima la matriz 4x4 de exactitudes medias (filas: C; columnas: gamma).
#
#   PREGUNTA GUÍA: ¿por qué toda la columna gamma = 1 vale lo mismo (0,628)?
#   Pista: calcule la distancia al cuadrado esperada entre dos puntos
#   estandarizados con 30 variables y evalúe exp(-gamma * distancia^2).
# ==============================================================================

# >>>>>>>>>> SOLUCIÓN A4 >>>>>>>>>>
titulo("A4. Grilla gruesa de C y gamma")
valores_C = [0.1, 1, 10, 100]
valores_gamma = [0.001, 0.01, 0.1, 1]
grilla = {"svc__C": valores_C, "svc__gamma": valores_gamma}
gs = GridSearchCV(make_pipeline(StandardScaler(), SVC()), grilla, cv=5)
gs.fit(Xtr, ytr)
print(f"mejores parámetros: {gs.best_params_}, validación cruzada = {gs.best_score_:.3f}")

matriz = gs.cv_results_["mean_test_score"].reshape(len(valores_C), len(valores_gamma))
print("matriz (filas: C = 0.1, 1, 10, 100; columnas: gamma = 0.001, 0.01, 0.1, 1):")
print(np.round(matriz, 3))
chequear("A4 mejor C y gamma", [gs.best_params_["svc__C"], gs.best_params_["svc__gamma"]],
         [100, 0.001], tol=0)
chequear("A4 validación cruzada del mejor", gs.best_score_, 0.985)
chequear("A4 columna gamma=1 (los 4 valores)", matriz[:, -1], [0.628] * 4)

fig, ax = plt.subplots(figsize=(5.6, 4.4))
im = ax.imshow(matriz, vmin=0.6, vmax=1.0, cmap="viridis")
ax.set_xticks(range(len(valores_gamma)), [str(g) for g in valores_gamma])
ax.set_yticks(range(len(valores_C)), [str(c) for c in valores_C])
ax.set_xlabel("gamma")
ax.set_ylabel("C")
ax.set_title("Exactitud de validación cruzada (5 pliegues)")
for i in range(len(valores_C)):
    for j in range(len(valores_gamma)):
        ax.text(j, i, f"{matriz[i, j]:.3f}", ha="center", va="center",
                color="white" if matriz[i, j] < 0.85 else "black", fontsize=9)
fig.colorbar(im, ax=ax, label="exactitud")
guardar(fig, "A4_grilla_C_gamma.png")

# Respuesta a la pregunta guía, con evidencia numérica:
esc_a4 = StandardScaler().fit(Xtr)
Ztr_a4, Zte_a4 = esc_a4.transform(Xtr), esc_a4.transform(Xte)
d2 = euclidean_distances(Ztr_a4, squared=True)
d2_medio = d2[~np.eye(len(d2), dtype=bool)].mean()
K1 = rbf_kernel(Ztr_a4, gamma=1.0)
K1_fuera = K1[~np.eye(len(K1), dtype=bool)]
print(f"\ndistancia^2 media entre pares distintos = {d2_medio:.1f} "
      f"(esperada 2 x 30 = 60)")
print(f"exp(-1 x 60) = {np.exp(-60):.1e};  kernel RBF con gamma=1 entre pares "
      f"distintos: media = {K1_fuera.mean():.1e}, máximo = {K1_fuera.max():.2f}")
modelo_gamma1 = SVC(C=10, gamma=1).fit(Ztr_a4, ytr)
pred = modelo_gamma1.predict(Zte_a4)
print(f"predicciones de prueba con gamma=1 (maligno, benigno): "
      f"{np.bincount(pred, minlength=2).tolist()}")
print(f"benignos en entrenamiento = {int(ytr.sum())} de {len(ytr)} "
      f"= {ytr.mean():.3f} (el 0,628 de la matriz)")

# Respuesta: con 30 variables estandarizadas la distancia^2 esperada entre dos
# puntos es 60 y exp(-gamma x 60) es prácticamente cero para gamma=1. La matriz de
# Gram queda casi igual a la identidad: fuera de la diagonal su media es ~3e-4 (solo
# unos pocos pares muy cercanos llegan a 0,33), es decir, cada punto solo se parece
# a sí mismo. Un punto nuevo no se parece a casi ningún vector soporte y el modelo
# predice casi siempre la clase mayoritaria (170 de 171 benignos en prueba). El
# 0,628 de la matriz es la proporción de benignos del entrenamiento.
# <<<<<<<<<< FIN SOLUCIÓN A4 <<<<<<<<<<


# ##############################################################################
# ##############################################################################
#                    PARTE B  |  TAREA (ENTREGA LA PRÓXIMA SESIÓN)
# ##############################################################################
# ##############################################################################


# %% ---------------------------------------------------------------------------
# [CÓDIGO DADO] Preparación común de la parte B
# ------------------------------------------------------------------------------
# Para inspeccionar el modelo SVC sin Pipeline (necesario en B1 a B4) se
# estandarizan los datos "a mano". El escalador se ajusta SOLO con entrenamiento.
datos = load_breast_cancer()
X, y = datos.data, datos.target
Xtr, Xte, ytr, yte = train_test_split(
    X, y, test_size=0.3, stratify=y, random_state=SEMILLA)
escalador = StandardScaler().fit(Xtr)
Ztr, Zte = escalador.transform(Xtr), escalador.transform(Xte)


# %% ---------------------------------------------------------------------------
# ==============================================================================
# ENUNCIADO B1  |  Reconstruir el dual
# ==============================================================================
#   Ajuste `SVC(kernel="rbf", C=10, gamma=0.01)` con (Ztr, ytr).
#
#   1. Reconstruya la función de decisión del dual,
#          f(x) = suma_i  alpha_i y_i k(x_i, x) + b,
#      usando `dual_coef_`, `support_vectors_` e `intercept_`, para los puntos
#      de prueba. Nota: `dual_coef_` ya contiene alpha_i multiplicado por y_i.
#      Compare con `decision_function` e imprima la diferencia máxima.
#   2. Clasifique los vectores soporte en LIBRES (0 < alpha_i < C) y ACOTADOS
#      (alpha_i = C). Imprima cuántos hay de cada tipo.
#   3. Verifique dos propiedades del dual:
#        a) suma_i alpha_i y_i = 0;
#        b) los libres cumplen y_i f(x_i) = 1 (están sobre el margen) y los
#           acotados cumplen y_i f(x_i) <= 1.
#
#   PREGUNTA: ¿qué condición KKT explica la propiedad (b)?
# ==============================================================================

# >>>>>>>>>> SOLUCIÓN B1 >>>>>>>>>>
titulo("B1. Reconstrucción del dual (RBF, C=10, gamma=0.01)")
C_B1, GAMMA_B1 = 10, 0.01
svm = SVC(kernel="rbf", C=C_B1, gamma=GAMMA_B1).fit(Ztr, ytr)

# (1) f(x) = suma_i (alpha_i y_i) k(x_i, x) + b
K = rbf_kernel(Zte, svm.support_vectors_, gamma=GAMMA_B1)   # (n_prueba, n_vs)
f_manual = K @ svm.dual_coef_.ravel() + svm.intercept_[0]
dif_max = np.abs(f_manual - svm.decision_function(Zte)).max()
mismas_clases = np.array_equal((f_manual > 0).astype(int), svm.predict(Zte))
print(f"diferencia máxima |f_manual - decision_function| = {dif_max:.2e}")
print(f"el signo de f_manual reproduce predict(): {mismas_clases}")
chequear("B1 diferencia máxima < 1e-9", dif_max < 1e-9, True, tol=0)

# (2) libres y acotados
alfa = np.abs(svm.dual_coef_.ravel())          # |alpha_i y_i| = alpha_i
acotado = np.isclose(alfa, C_B1)
n_vs, n_acot = len(alfa), int(acotado.sum())
print(f"vectores soporte: {n_vs} (acotados, alpha = C: {n_acot}; "
      f"libres: {n_vs - n_acot})")
chequear("B1 total, acotados y libres", [n_vs, n_acot, n_vs - n_acot], [50, 21, 29], tol=0)

# (3) propiedades del dual
y_pm = np.where(ytr == 1, 1, -1)               # etiquetas {-1, +1} del dual
y_vs = y_pm[svm.support_]
margen_func = y_vs * svm.decision_function(svm.support_vectors_)   # y_i f(x_i)
print(f"(a) suma alpha_i y_i = {svm.dual_coef_.sum():.1e}  (debe ser ~0)")
print(f"(b) libres:   y f(x) entre {margen_func[~acotado].min():.4f} "
      f"y {margen_func[~acotado].max():.4f}  (debe ser ~1)")
print(f"    acotados: y f(x) máximo = {margen_func[acotado].max():.4f}  (debe ser <= 1)")
chequear("B1 (a) suma alpha_i y_i ~ 0", abs(svm.dual_coef_.sum()) < 1e-6, True, tol=0)
chequear("B1 (b) libres sobre el margen (|y f - 1| < 1e-2)",
         bool(np.all(np.abs(margen_func[~acotado] - 1) < 1e-2)), True, tol=0)
chequear("B1 (b) acotados con y f <= 1",
         bool(np.all(margen_func[acotado] <= 1 + 1e-2)), True, tol=0)

# Respuesta: la holgura complementaria alpha_i [ y_i f(x_i) - 1 + xi_i ] = 0 y la
# condición (C - alpha_i) xi_i = 0. Si 0 < alpha_i < C, entonces xi_i = 0 e
# y_i f(x_i) = 1 (sobre el margen). Si alpha_i = C, xi_i puede ser positivo y
# y_i f(x_i) <= 1 (dentro del margen o mal clasificado).
# <<<<<<<<<< FIN SOLUCIÓN B1 <<<<<<<<<<


# %% ---------------------------------------------------------------------------
# ==============================================================================
# ENUNCIADO B2  |  Curva de validación en gamma
# ==============================================================================
#   Con C = 10 fijo y kernel RBF, para gamma in [0.001, 0.01, 0.1, 1, 10]:
#     1. Ajuste el modelo con (Ztr, ytr).
#     2. Registre exactitud de entrenamiento, exactitud de prueba y número de
#        vectores soporte.
#   Imprima una tabla y grafique exactitud (entrenamiento y prueba) y vectores
#   soporte contra gamma, en escala logarítmica.
#
#   PREGUNTA: ¿a partir de qué gamma empieza el sobreajuste? Justifique con la
#   diferencia entre entrenamiento y prueba y con el número de vectores soporte.
# ==============================================================================

# >>>>>>>>>> SOLUCIÓN B2 >>>>>>>>>>
titulo("B2. Curva de validación en gamma (C=10)")
gammas = [0.001, 0.01, 0.1, 1, 10]
acc_tr, acc_te, nvs = [], [], []
for g in gammas:
    m = SVC(kernel="rbf", C=10, gamma=g).fit(Ztr, ytr)
    acc_tr.append(m.score(Ztr, ytr))
    acc_te.append(m.score(Zte, yte))
    nvs.append(len(m.support_))
print(f"{'gamma':>8} {'entren.':>8} {'prueba':>8} {'brecha':>8} {'n_VS':>6}")
for g, a, b, n in zip(gammas, acc_tr, acc_te, nvs):
    print(f"{g:>8g} {a:>8.3f} {b:>8.3f} {a - b:>8.3f} {n:>6d}")
chequear("B2 exactitud de prueba", acc_te, [0.965, 0.965, 0.936, 0.632, 0.626])
chequear("B2 exactitud de entrenamiento", acc_tr, [0.982, 0.992, 1.0, 1.0, 1.0])
chequear("B2 vectores soporte", nvs, [75, 50, 163, 397, 398], tol=0)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 3.8))
ax1.semilogx(gammas, acc_tr, "o-", label="entrenamiento")
ax1.semilogx(gammas, acc_te, "s--", label="prueba")
ax1.set_xlabel("gamma")
ax1.set_ylabel("exactitud")
ax1.set_title("Exactitud frente a gamma (C=10)")
ax1.legend()
ax2.semilogx(gammas, nvs, "o-", color="tab:green")
ax2.axhline(len(ytr), color="gray", ls=":")
ax2.text(gammas[0], len(ytr) * 0.93, "todos los casos de entrenamiento", fontsize=8)
ax2.set_xlabel("gamma")
ax2.set_ylabel("vectores soporte")
ax2.set_title("Vectores soporte frente a gamma")
guardar(fig, "B2_curva_gamma.png")

# Criterio usado: primer gamma con brecha entrenamiento-prueba mayor que 0,05.
primer = next(g for g, a, b in zip(gammas, acc_tr, acc_te) if a - b > 0.05)
print(f"\nprimer gamma con brecha > 0.05: {primer}")
chequear("B2 el sobreajuste empieza en gamma", primer, 0.1, tol=0)

# Respuesta: hasta gamma=0,01 la brecha es de ~0,03 o menos. Desde gamma=0,1 el
# entrenamiento llega a 1,000 y la prueba cae (0,936); con gamma>=1 el modelo memoriza
# (casi todos los casos son vectores soporte) y en prueba se reduce a la clase
# mayoritaria (~0,63). Es el mismo colapso de la columna gamma=1 de A4.
# <<<<<<<<<< FIN SOLUCIÓN B2 <<<<<<<<<<


# %% ---------------------------------------------------------------------------
# ==============================================================================
# ENUNCIADO B3  |  Efecto de C con kernel lineal
# ==============================================================================
#   Con `SVC(kernel="linear")` y (Ztr, ytr), para
#   C in [0.001, 0.01, 0.1, 1, 10, 100]:
#     1. Registre el número de vectores soporte y la exactitud de prueba.
#     2. Grafique el número de vectores soporte contra C (eje C logarítmico).
#
#   PREGUNTA: ¿cómo cambia el número de vectores soporte cuando C aumenta?
#   Relaciónelo con el ancho del margen y con la hinge loss.
# ==============================================================================

# >>>>>>>>>> SOLUCIÓN B3 >>>>>>>>>>
titulo("B3. Efecto de C con kernel lineal")
Cs = [0.001, 0.01, 0.1, 1, 10, 100]
nvs_C, acc_C, margen_C = [], [], []
for c in Cs:
    m = SVC(kernel="linear", C=c).fit(Ztr, ytr)
    nvs_C.append(len(m.support_))
    acc_C.append(m.score(Zte, yte))
    margen_C.append(2 / np.linalg.norm(m.coef_))
print(f"{'C':>8} {'n_VS':>6} {'exactitud prueba':>17} {'margen 2/||w||':>15}")
for c, n, a, mg in zip(Cs, nvs_C, acc_C, margen_C):
    print(f"{c:>8g} {n:>6d} {a:>17.3f} {mg:>15.3f}")
chequear("B3 vectores soporte", nvs_C, [195, 92, 44, 27, 25, 25], tol=0)

fig, ax = plt.subplots(figsize=(5.6, 3.8))
ax.semilogx(Cs, nvs_C, "o-")
ax.set_xlabel("C")
ax.set_ylabel("vectores soporte")
ax.set_title("Vectores soporte frente a C (kernel lineal)")
guardar(fig, "B3_vectores_soporte_vs_C.png")

# Respuesta: el número de vectores soporte decrece al aumentar C (195 -> 25) y el
# margen 2/||w|| se estrecha (6,4 con C=0,001; 0,09 con C=100). Con C pequeño la
# penalización por violar el margen pesa poco frente a ||w||^2: se prefiere un w de
# norma pequeña, es decir un margen muy ancho donde caen muchos puntos (alpha_i = C),
# y todos ellos son vectores soporte. Con C grande cada violación de la hinge loss
# se castiga más, el margen se estrecha y quedan pocos puntos sobre él o dentro. Desde
# C=10 el número de vectores soporte se estabiliza en 25, pero el margen sigue
# estrechándose. La exactitud de prueba varía entre 0,930 y 0,959: diferencias de
# hasta cinco casos sobre 171 que no bastan para elegir C. Eso lo decide la
# validación cruzada (paso A4).
# <<<<<<<<<< FIN SOLUCIÓN B3 <<<<<<<<<<


# %% ---------------------------------------------------------------------------
# ==============================================================================
# ENUNCIADO B4  |  Métricas clínicas y desbalance de clases
# ==============================================================================
#   Con `SVC(kernel="rbf", C=10, gamma=0.01)` y (Ztr, ytr), ajuste dos modelos:
#   uno sin `class_weight` y otro con `class_weight="balanced"`.
#     1. Imprima la matriz de confusión de prueba de cada uno (filas: clase real;
#        columnas: clase predicha; 0 = maligno, 1 = benigno).
#     2. Calcule la exactitud y el recall de la clase maligna (`pos_label=0`).
#
#   PREGUNTA: en diagnóstico, ¿qué error es más costoso: un maligno clasificado
#   como benigno o al revés? ¿Qué métrica lo refleja? ¿Es significativa la
#   diferencia entre los dos modelos con este tamaño de prueba?
# ==============================================================================

# >>>>>>>>>> SOLUCIÓN B4 >>>>>>>>>>
titulo("B4. Métricas clínicas y class_weight (C=10, gamma=0.01)")
res_b4 = {}
for cw in [None, "balanced"]:
    m = SVC(kernel="rbf", C=10, gamma=0.01, class_weight=cw).fit(Ztr, ytr)
    pred = m.predict(Zte)
    res_b4[cw] = ((pred == yte).mean(), recall_score(yte, pred, pos_label=0))
    print(f"\nclass_weight = {cw}")
    print("matriz de confusión (filas: real; columnas: predicha; 0=maligno, 1=benigno):")
    print(confusion_matrix(yte, pred))
    print(f"exactitud = {res_b4[cw][0]:.3f}   recall maligno = {res_b4[cw][1]:.3f}")
chequear("B4 exactitud sin ponderar y ponderado", [res_b4[None][0], res_b4["balanced"][0]],
         [0.965, 0.959])
chequear("B4 recall maligno sin ponderar y ponderado",
         [res_b4[None][1], res_b4["balanced"][1]], [0.938, 0.953])

n_mal = int((yte == 0).sum())
print(f"\nmalignos en prueba = {n_mal}; un caso equivale a {100 / n_mal:.1f} puntos "
      f"porcentuales de recall.")

# Respuesta: clasificar como benigno un tumor maligno (falso negativo) puede retrasar
# el tratamiento y suele considerarse el error más costoso; lo mide el recall de la
# clase maligna. La ponderación sube el recall de 0,938 a 0,953 (detecta 61 en vez de
# 60 de los 64 malignos) a costa de marcar como malignos 2 benignos más (2 -> 4),
# así que en total hay un error más y la exactitud baja de 0,965 a 0,959. Es una
# diferencia de uno o dos casos con 64 malignos y 171 casos de prueba: no es
# evidencia de que un modelo sea mejor. La decisión debería apoyarse en validación
# cruzada y en el costo relativo de cada tipo de error.
# <<<<<<<<<< FIN SOLUCIÓN B4 <<<<<<<<<<


# %% ---------------------------------------------------------------------------
# ==============================================================================
# ENUNCIADO B5  |  Respuesta teórica (media página)
# ==============================================================================
#   (a) Muestre que  k(x, x') = (<x, x'> + 1)^2  en dos dimensiones corresponde a
#       un mapeo explícito  Phi : R^2 -> R^6.  Escriba Phi y compruebe
#       numéricamente que  <Phi(x), Phi(x')> = k(x, x')  con vectores aleatorios.
#
#   (b) Explique por qué en este conjunto el kernel lineal iguala al RBF y
#       cuándo se esperaría ventaja del RBF. Respalde la respuesta con una
#       comparación sobre 30 particiones aleatorias (70/30, estratificadas) en
#       este conjunto y en `make_moons(300, noise=0.3, random_state=0)`,
#       ambos con StandardScaler dentro de un Pipeline.
# ==============================================================================

# >>>>>>>>>> SOLUCIÓN B5 >>>>>>>>>>
titulo("B5. Respuesta teórica")

# --- (a) Mapeo explícito del kernel polinomial (grado 2) en R^2 ----------------
# (<x,x'> + 1)^2 = (x1 x1' + x2 x2' + 1)^2
#   = 1 + 2 x1 x1' + 2 x2 x2' + x1^2 x1'^2 + 2 x1 x2 x1' x2' + x2^2 x2'^2
# lo que equivale al producto interno de
#   Phi(x) = (1, sqrt(2) x1, sqrt(2) x2, x1^2, sqrt(2) x1 x2, x2^2)  en R^6.
def phi(x):
    x1, x2 = x
    r2 = np.sqrt(2.0)
    return np.array([1.0, r2 * x1, r2 * x2, x1 ** 2, r2 * x1 * x2, x2 ** 2])


rng = np.random.default_rng(SEMILLA)
dif_a = max(abs(phi(a) @ phi(b) - (a @ b + 1) ** 2)
            for a, b in rng.normal(size=(1000, 2, 2)))
print(f"(a) máxima diferencia |<Phi(x),Phi(x')> - (<x,x'>+1)^2| en 1000 pares = {dif_a:.1e}")
chequear("B5(a) el mapeo reproduce el kernel (dif < 1e-9)", dif_a < 1e-9, True, tol=0)


# --- (b) Lineal frente a RBF en dos conjuntos -----------------------------------
def comparar_lineal_rbf(X_, y_, n_particiones=30):
    """Exactitud de prueba de lineal y RBF en n particiones 70/30 estratificadas."""
    acc = {"linear": [], "rbf": []}
    for semilla in range(n_particiones):
        a, b, c, d = train_test_split(X_, y_, test_size=0.3, stratify=y_,
                                      random_state=semilla)
        for kernel in acc:
            m = make_pipeline(StandardScaler(), SVC(kernel=kernel)).fit(a, c)
            acc[kernel].append(m.score(b, d))
    lin, rbf = np.array(acc["linear"]), np.array(acc["rbf"])
    return lin, rbf


Xm, ym = make_moons(300, noise=0.3, random_state=0)
resumen_b5 = {}
for nombre, (X_, y_) in {"cáncer de mama": (X, y), "make_moons": (Xm, ym)}.items():
    lin, rbf = comparar_lineal_rbf(X_, y_)
    d = rbf - lin
    resumen_b5[nombre] = (lin.mean(), rbf.mean())
    print(f"\n(b) {nombre}: 30 particiones")
    print(f"    lineal: media {lin.mean():.3f} (sd {lin.std():.3f})")
    print(f"    RBF:    media {rbf.mean():.3f} (sd {rbf.std():.3f})")
    print(f"    RBF - lineal: media {d.mean():+.3f} (sd {d.std():.3f}); "
          f"RBF mejor en {(d > 0).sum()}, empate en {(d == 0).sum()}, "
          f"peor en {(d < 0).sum()} de {len(d)} particiones")

chequear("B5(b) cáncer de mama: media lineal y RBF", resumen_b5["cáncer de mama"],
         [0.974, 0.971])
chequear("B5(b) make_moons: media lineal y RBF", resumen_b5["make_moons"],
         [0.809, 0.909])

# Respuesta (b): en cáncer de mama el RBF no mejora al lineal: la diferencia media
# (RBF - lineal = -0,003, con desviación 0,010) es menor que la variación entre
# particiones, y el RBF gana solo en 6 de 30. El resultado es compatible con una
# frontera casi lineal en el espacio de 30 variables estandarizadas: el RBF no mejora
# la exactitud y usa más vectores soporte (96 frente a 27 en A3). En make_moons, donde
# la frontera es curva, el RBF supera al lineal por unos 10 puntos porcentuales
# (0,909 frente a 0,809) en las 30 particiones. Regla práctica: partir del kernel
# lineal como línea base y pasar al RBF solo si la validación cruzada muestra una
# mejora que supere el ruido entre particiones.
# <<<<<<<<<< FIN SOLUCIÓN B5 <<<<<<<<<<


# %% ---------------------------------------------------------------------------
# [CÓDIGO DADO] Resumen del contraste con las cifras de referencia del plan
# ------------------------------------------------------------------------------
if RESULTADOS:   # vacío en la versión de estudiantes (sin bloques de solución)
    titulo("RESUMEN: contraste con las cifras de referencia del plan")
    n_ok = sum(ok for _, ok in RESULTADOS)
    for nombre, ok in RESULTADOS:
        print(f"  [{'OK ' if ok else 'DIF'}] {nombre}")
    print(f"\n{n_ok} de {len(RESULTADOS)} resultados coinciden con la referencia.")
    print(f"Figuras en la carpeta '{DIR_FIGURAS}'.")
