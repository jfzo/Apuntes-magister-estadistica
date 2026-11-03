"""Genera las figuras de clase04.md (Métodos de Kernel y SVM).

Uso:  python3 figuras.py   ->  crea fig_*.png en el directorio actual.
Requiere numpy, matplotlib y scikit-learn.
"""
import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from sklearn.datasets import make_moons
from sklearn.svm import SVC

plt.rcParams.update({
    "font.size": 13,
    "axes.titlesize": 14,
    "axes.labelsize": 13,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "figure.dpi": 150,
    "savefig.dpi": 200,
    "savefig.bbox": "tight",
    "mathtext.fontset": "cm",
})
POS, NEG = "#0072B2", "#D55E00"  # clase +1 (círculos) / clase -1 (cuadrados)


# ----------------------------------------------------------------- utilidades
def datos_blobs(m, centro, std, seed):
    rng = np.random.RandomState(seed)
    Xp = rng.randn(m, 2) * std + np.array(centro)
    Xn = rng.randn(m, 2) * std - np.array(centro)
    X = np.vstack([Xp, Xn])
    y = np.r_[np.ones(m), -np.ones(m)]
    return X, y


def datos_separables():
    return datos_blobs(14, (1.6, 1.2), 0.55, 3)


def datos_traslapados():
    return datos_blobs(30, (1.3, 1.0), 0.85, 6)


def puntos(ax, X, y, s=48, alpha=1.0, etiquetas=True):
    ax.scatter(X[y == 1, 0], X[y == 1, 1], c=POS, s=s, marker="o", alpha=alpha,
               edgecolor="white", linewidth=0.6,
               label="Clase $+1$" if etiquetas else None, zorder=3)
    ax.scatter(X[y == -1, 0], X[y == -1, 1], c=NEG, s=s, marker="s", alpha=alpha,
               edgecolor="white", linewidth=0.6,
               label="Clase $-1$" if etiquetas else None, zorder=3)


def recta(ax, w, b, v=0.0, t=8, **kw):
    """Dibuja la recta <w,x> + b = v."""
    n2 = w @ w
    x0 = (v - b) * w / n2
    d = np.array([-w[1], w[0]]) / np.sqrt(n2)
    p = np.array([x0 - t * d, x0 + t * d])
    ax.plot(p[:, 0], p[:, 1], **kw)


def banda(ax, w, b, t=8, **kw):
    """Sombrea la región -1 <= <w,x> + b <= 1."""
    n2 = w @ w
    d = np.array([-w[1], w[0]]) / np.sqrt(n2)
    p1, p2 = (1 - b) * w / n2, (-1 - b) * w / n2
    poly = np.array([p1 - t * d, p1 + t * d, p2 + t * d, p2 - t * d])
    ax.fill(poly[:, 0], poly[:, 1], **kw)


def ejes(ax, xl, yl):
    ax.set_xlim(*xl)
    ax.set_ylim(*yl)
    ax.set_aspect("equal")
    ax.set_xticks([])
    ax.set_yticks([])


# ------------------------------------------------------------------- figuras
def fig_centroides():
    X, y = datos_blobs(25, (1.5, 1.0), 0.7, 1)
    cp, cn = X[y == 1].mean(0), X[y == -1].mean(0)
    c = (cp + cn) / 2
    w = cp - cn
    x = np.array([0.5, 1.3])

    fig, ax = plt.subplots(figsize=(7.2, 4.6))
    puntos(ax, X, y, alpha=0.55)
    recta(ax, w, -w @ c, 0.0, color="black", lw=1.6, ls="--", zorder=2)
    ax.annotate("", xy=cp, xytext=cn,
                arrowprops=dict(arrowstyle="->", lw=2, color="#444444"), zorder=4)
    ax.annotate("", xy=x, xytext=c,
                arrowprops=dict(arrowstyle="->", lw=2, color="#009E73"), zorder=4)
    for p, nombre, off in [(cp, r"$\mathbf{c}_+$", (0.12, -0.35)),
                           (cn, r"$\mathbf{c}_-$", (0.12, 0.2)),
                           (c, r"$\mathbf{c}$", (0.15, -0.38))]:
        ax.scatter(*p, marker="*", s=260, c="gold", edgecolor="black", zorder=5)
        ax.text(p[0] + off[0], p[1] + off[1], nombre, fontsize=15, zorder=6)
    ax.scatter(*x, marker="D", s=90, c="#009E73", edgecolor="black", zorder=5)
    ax.text(x[0] + 0.12, x[1] + 0.1, r"$\mathbf{x}$", fontsize=15, zorder=6)
    nrm = np.array([w[1], -w[0]]) / np.linalg.norm(w)
    m1 = cn + 0.25 * w + 0.42 * nrm
    ax.text(m1[0], m1[1], r"$\mathbf{c}_+-\mathbf{c}_-$", color="#444444", fontsize=13)
    m2 = (c + x) / 2
    ax.text(m2[0] - 0.95, m2[1] - 0.05, r"$\mathbf{x}-\mathbf{c}$", color="#009E73",
            fontsize=13)
    ejes(ax, (-3.4, 3.4), (-2.6, 2.6))
    ax.legend(loc="lower right", frameon=False, fontsize=11)
    fig.savefig("fig_centroides.png")
    plt.close(fig)


def fig_hiperplanos():
    X, y = datos_separables()
    clf = SVC(kernel="linear", C=1e6).fit(X, y)
    assert (clf.predict(X) == y).all()
    w, b = clf.coef_[0], clf.intercept_[0]
    th0 = np.arctan2(w[1], w[0])

    rng = np.random.RandomState(0)
    lineas = []
    for dth in np.linspace(-0.9, 0.9, 6):
        th = th0 + dth
        wn = np.array([np.cos(th), np.sin(th)])
        pp, pn = (X[y == 1] @ wn).min(), (X[y == -1] @ wn).max()
        if pp <= pn:
            continue
        c = (pp + pn) / 2 + rng.uniform(-0.25, 0.25) * (pp - pn)
        lineas.append((wn, c))
    assert len(lineas) >= 4

    fig, axs = plt.subplots(1, 2, figsize=(11, 4.6))
    ax = axs[0]
    puntos(ax, X, y)
    for wn, c in lineas:
        recta(ax, wn, -c, 0.0, color="gray", lw=1.6)
    ax.set_title("Hiperplanos que separan sin error")
    ejes(ax, (-3.6, 3.6), (-3.2, 3.2))

    ax = axs[1]
    banda(ax, w, b, color="#999999", alpha=0.18, lw=0)
    puntos(ax, X, y)
    recta(ax, w, b, 0, color="black", lw=2)
    recta(ax, w, b, 1, color="black", lw=1.2, ls="--")
    recta(ax, w, b, -1, color="black", lw=1.2, ls="--")
    ax.scatter(*clf.support_vectors_.T, s=230, facecolor="none", edgecolor="black",
               linewidth=1.8, zorder=4)
    ax.set_title("Hiperplano de margen máximo")
    ejes(ax, (-3.6, 3.6), (-3.2, 3.2))
    fig.tight_layout()
    fig.savefig("fig_hiperplanos.png")
    plt.close(fig)


def fig_margen():
    X, y = datos_separables()
    clf = SVC(kernel="linear", C=1e6).fit(X, y)
    w, b = clf.coef_[0], clf.intercept_[0]
    n2 = w @ w
    d = np.array([-w[1], w[0]]) / np.sqrt(n2)
    x0 = -b * w / n2

    fig, ax = plt.subplots(figsize=(7.4, 4.8))
    banda(ax, w, b, color="#999999", alpha=0.18, lw=0)
    puntos(ax, X, y, etiquetas=False)
    recta(ax, w, b, 0, color="black", lw=2)
    recta(ax, w, b, 1, color="black", lw=1.2, ls="--")
    recta(ax, w, b, -1, color="black", lw=1.2, ls="--")
    ax.scatter(*clf.support_vectors_.T, s=230, facecolor="none", edgecolor="black",
               linewidth=1.8, zorder=4)

    s = 2.6
    p1, p2 = x0 + s * d + w / n2, x0 + s * d - w / n2
    ax.annotate("", xy=p1, xytext=p2,
                arrowprops=dict(arrowstyle="<->", lw=1.8, color="black"), zorder=5)
    mid = (p1 + p2) / 2
    ax.text(mid[0] + 0.15, mid[1] + 0.15, r"$2/\|\mathbf{w}\|$", fontsize=15)

    s2 = -2.4
    q = x0 + s2 * d
    u = w / np.sqrt(n2)
    ax.annotate("", xy=q + 1.0 * u, xytext=q,
                arrowprops=dict(arrowstyle="->", lw=2, color="#009E73"), zorder=5)
    ax.text(q[0] + 0.1, q[1] + 1.0 * u[1] + 0.15, r"$\mathbf{w}$", fontsize=15,
            color="#009E73")

    ax.legend(handles=[
        Line2D([], [], color="black", lw=2, label=r"$f(\mathbf{x})=0$"),
        Line2D([], [], color="black", lw=1.2, ls="--", label=r"$f(\mathbf{x})=\pm1$"),
        Line2D([], [], marker="o", ls="", mfc="none", mec="black", mew=1.8, ms=13,
               label="Vectores soporte"),
    ], loc="upper center", bbox_to_anchor=(0.5, -0.02), ncol=3, frameon=False,
        fontsize=11)
    ejes(ax, (-3.6, 3.6), (-3.2, 3.2))
    fig.savefig("fig_margen.png")
    plt.close(fig)


def fig_mapeo():
    rng = np.random.RandomState(2)
    P = rng.uniform(-2, 2, size=(900, 2))
    g = P[:, 0] ** 2 + 2 * P[:, 1] ** 2
    keep = np.abs(g - 1.8) > 0.5
    P, g = P[keep], g[keep]
    y = np.where(g > 1.8, 1, -1)
    # submuestreo para que la figura sea legible
    idx = rng.choice(len(P), size=min(75, len(P)), replace=False)
    P, y = P[idx], y[idx]
    Z = np.column_stack([P[:, 0] ** 2, np.sqrt(2) * P[:, 0] * P[:, 1], P[:, 1] ** 2])

    fig = plt.figure(figsize=(11, 4.8))
    ax = fig.add_subplot(121)
    puntos(ax, P, y, s=40)
    th = np.linspace(0, 2 * np.pi, 300)
    ax.plot(np.sqrt(1.8) * np.cos(th), np.sqrt(0.9) * np.sin(th), "k--", lw=1.6)
    ax.set_title(r"Espacio de entrada $\mathbb{R}^2$")
    ax.set_xlabel(r"$x_1$")
    ax.set_ylabel(r"$x_2$")
    ax.set_xlim(-2.1, 2.1)
    ax.set_ylim(-2.1, 2.1)
    ax.set_aspect("equal")
    ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.16), ncol=2, frameon=False,
              fontsize=11)

    ax3 = fig.add_subplot(122, projection="3d")
    z1, z2 = np.meshgrid(np.linspace(0, 1.8, 10), np.linspace(-4, 4, 10))
    ax3.plot_surface(z1, z2, (1.8 - z1) / 2, color="gray", alpha=0.35, linewidth=0)
    ax3.set_yticks([-4, 0, 4])
    ax3.scatter(Z[y == 1, 0], Z[y == 1, 1], Z[y == 1, 2], c=POS, marker="o", s=38)
    ax3.scatter(Z[y == -1, 0], Z[y == -1, 1], Z[y == -1, 2], c=NEG, marker="s", s=38)
    ax3.set_xlabel(r"$z_1=x_1^2$", labelpad=8)
    ax3.set_ylabel(r"$z_2=\sqrt{2}\,x_1x_2$", labelpad=10)
    ax3.set_zlabel(r"$z_3=x_2^2$", labelpad=6)
    ax3.set_title(r"Espacio de características $\mathbb{R}^3$")
    ax3.view_init(elev=20, azim=-58)
    fig.tight_layout()
    fig.savefig("fig_mapeo.png")
    plt.close(fig)


def fig_hinge():
    z = np.linspace(-2, 2.6, 600)
    fig, ax = plt.subplots(figsize=(7.4, 4.4))
    ax.plot(z[z < 0], np.ones((z < 0).sum()), color="gray", lw=2, label="0-1")
    ax.plot(z[z >= 0], np.zeros((z >= 0).sum()), color="gray", lw=2)
    ax.plot(z, np.maximum(0, 1 - z), color=POS, lw=2.6, label="Hinge (SVM)")
    ax.plot(z, np.log2(1 + np.exp(-z)), color=NEG, lw=2.6, ls="--",
            label=r"Logística ($\log_2$)")
    ax.axvline(1, color="black", lw=1, ls=":")
    ax.text(1.06, 1.6, "margen", fontsize=12)
    ax.set_xlabel(r"$y\,f(\mathbf{x})$")
    ax.set_ylabel("Pérdida")
    ax.set_ylim(-0.1, 3.0)
    ax.legend(frameon=False, loc="upper right", fontsize=12)
    fig.savefig("fig_hinge.png")
    plt.close(fig)


def fig_tipos_puntos():
    X, y = datos_traslapados()
    C = 1.0
    clf = SVC(kernel="linear", C=C).fit(X, y)
    w, b = clf.coef_[0], clf.intercept_[0]
    alfa = np.abs(clf.dual_coef_[0])
    sv = clf.support_
    en_C = np.isclose(alfa, C, rtol=1e-6)

    fig, ax = plt.subplots(figsize=(7.4, 4.8))
    banda(ax, w, b, color="#999999", alpha=0.18, lw=0)
    puntos(ax, X, y, s=42, etiquetas=False)
    recta(ax, w, b, 0, color="black", lw=2)
    recta(ax, w, b, 1, color="black", lw=1.2, ls="--")
    recta(ax, w, b, -1, color="black", lw=1.2, ls="--")
    ax.scatter(*X[sv[~en_C]].T, s=210, facecolor="none", edgecolor="black",
               linewidth=2, zorder=4)
    ax.scatter(*X[sv[en_C]].T, s=330, facecolor="none", edgecolor="#CC79A7",
               linewidth=2.4, zorder=4)
    ax.legend(handles=[
        Line2D([], [], marker="o", ls="", mfc="gray", mec="none", ms=7,
               label=r"$\alpha_i=0$ (sin influencia)"),
        Line2D([], [], marker="o", ls="", mfc="none", mec="black", mew=2, ms=13,
               label=r"$0<\alpha_i<C$ (sobre el margen)"),
        Line2D([], [], marker="o", ls="", mfc="none", mec="#CC79A7", mew=2.4, ms=17,
               label=r"$\alpha_i=C$ (dentro del margen o mal clasificado)"),
    ], loc="upper center", bbox_to_anchor=(0.5, -0.02), frameon=False, fontsize=11)
    ejes(ax, (-3.6, 3.6), (-3.2, 3.2))
    fig.savefig("fig_tipos_puntos.png")
    plt.close(fig)


def fig_C():
    X, y = datos_traslapados()
    fig, axs = plt.subplots(1, 3, figsize=(12, 4.4))
    for ax, C in zip(axs, [0.01, 1, 100]):
        clf = SVC(kernel="linear", C=C).fit(X, y)
        w, b = clf.coef_[0], clf.intercept_[0]
        banda(ax, w, b, color="#999999", alpha=0.18, lw=0)
        puntos(ax, X, y, s=30, etiquetas=False)
        recta(ax, w, b, 0, color="black", lw=2)
        recta(ax, w, b, 1, color="black", lw=1.2, ls="--")
        recta(ax, w, b, -1, color="black", lw=1.2, ls="--")
        ax.scatter(*clf.support_vectors_.T, s=130, facecolor="none",
                   edgecolor="black", linewidth=1.2, zorder=4)
        ax.set_title(rf"$C={C:g}$" + "\n"
                     + f"{len(clf.support_)} VS, margen $={2 / np.linalg.norm(w):.2f}$",
                     fontsize=13)
        ejes(ax, (-3.6, 3.6), (-3.2, 3.2))
    fig.tight_layout()
    fig.savefig("fig_C.png")
    plt.close(fig)


def fig_grid_C_gamma():
    X, y = make_moons(200, noise=0.3, random_state=0)
    y = 2 * y - 1
    xx, yy = np.meshgrid(np.linspace(-2.2, 3.2, 250), np.linspace(-1.6, 2.2, 250))
    malla = np.c_[xx.ravel(), yy.ravel()]
    fig, axs = plt.subplots(3, 3, figsize=(10, 7.4))
    for i, C in enumerate([0.1, 1, 100]):
        for j, gam in enumerate([0.1, 1, 10]):
            clf = SVC(kernel="rbf", C=C, gamma=gam).fit(X, y)
            f = clf.decision_function(malla).reshape(xx.shape)
            ax = axs[i, j]
            ax.contourf(xx, yy, f, levels=[-np.inf, 0, np.inf], colors=[NEG, POS],
                        alpha=0.18)
            ax.contour(xx, yy, f, levels=[0], colors="black", linewidths=1.6)
            puntos(ax, X, y, s=16, etiquetas=False)
            ax.set_title(rf"$C={C:g},\ \gamma={gam:g}$ ({len(clf.support_)} VS)",
                         fontsize=12)
            ax.set_xticks([])
            ax.set_yticks([])
    fig.tight_layout()
    fig.savefig("fig_grid_C_gamma.png")
    plt.close(fig)


if __name__ == "__main__":
    for f in [fig_centroides, fig_hiperplanos, fig_margen, fig_mapeo, fig_hinge,
              fig_tipos_puntos, fig_C, fig_grid_C_gamma]:
        f()
        print("ok", f.__name__)
