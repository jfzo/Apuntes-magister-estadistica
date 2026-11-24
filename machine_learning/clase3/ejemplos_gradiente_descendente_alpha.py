import matplotlib.pyplot as plt
import numpy as np

# 1. Definir la función de error y su derivada
def L(w):
  return (w - 3) ** 2

def dL(w):
  return 2 * (w - 3)

# 2. Configurar los 4 valores distintos de tasa de aprendizaje
alphas = [0.2, 0.4, 0.8, 1.0] 
# 0.1: Convergencia lenta
# 0.4: Convergencia rápida y directa
# 0.8: Convergencia con oscilación
# 1.05: Divergencia (el paso es muy grande)

pasos = 6
w_inicial = 0.0
w_vals = np.linspace(-2, 8, 200)
L_vals = L(w_vals)

# 3. Crear figura con 4 subgráficos (2x2)
fig, axs = plt.subplots(2, 2, figsize=(14, 10))
axs = axs.flatten()

for i, alpha in enumerate(alphas):
    w_actual = w_inicial
    historial_w = [w_actual]
    historial_L = [L(w_actual)]
    
    # Calcular pasos
    for _ in range(pasos):
        gradiente = dL(w_actual)
        w_actual = w_actual - alpha * gradiente
        historial_w.append(w_actual)
        historial_L.append(L(w_actual))
        
    ax = axs[i]
    
    # Graficar la curva de error base
    ax.plot(w_vals, L_vals, color='#2b5c8f', linewidth=2)
    
    # Graficar la trayectoria del gradiente
    ax.plot(historial_w, historial_L, 'o--', color='#d9534f', markersize=6, 
            label=f'Trayectoria')
    
    # Resaltar el mínimo global
    ax.scatter(3, 0, color='#2ca02c', s=80, zorder=5, label='Mínimo global (3,0)')
    
    # Ajustes estéticos de cada subgráfico
    ax.set_title(f'Tasa de aprendizaje α = {alpha}', fontsize=12, fontweight='bold')
    ax.set_xlabel('Peso ($w$)')
    ax.set_ylabel('Error $L(w)$')
    ax.grid(True, linestyle=':', alpha=0.6)
    
    # Ajustar límites de los ejes para mejor visualización (especialmente para divergencia)
    if alpha > 1:
        ax.set_xlim(-2, 8)
        ax.set_ylim(-1, 40)
    else:
        ax.set_xlim(-0.5, 6.5)
        ax.set_ylim(-1, 10)
        
    if i == 0:
        ax.legend()

plt.suptitle('Comparación de la Convergencia del Gradiente Descendente según α', fontsize=16, y=1.02)
plt.tight_layout()
plt.show()
