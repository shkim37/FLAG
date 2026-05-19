"""Render the latent-augmented MDP (z-MDP) graphical model for the project page.

Red edges = local-policy / parameter path (z, theta, s -> a_tilde).
Blue edges = marginalization to the global policy action (a_tilde, s -> a).
Black edges = environment dynamics (s, a -> s').
"""

from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib import rcParams
from matplotlib.patches import Circle, FancyArrowPatch, Rectangle

rcParams["mathtext.fontset"] = "cm"
rcParams["font.family"] = "serif"
rcParams["font.size"] = 14
rcParams["axes.linewidth"] = 0.0

REPO = Path(__file__).resolve().parents[2]
OUT = REPO / "src" / "assets" / "z_MDP_v2.pdf"

RED = "#c81e2a"
BLUE = "#1f4eb0"
BLACK = "#111111"

# Node positions (x, y)
P = {
    "z":     (0.5, 0.7),
    "theta": (0.5, 3.2),
    "s":     (2.7, 0.7),
    "tilde": (2.7, 3.2),
    "a":     (5.0, 3.2),
    "sp":    (5.0, 0.7),
}

R = 0.42  # node radius


def draw_circle(ax, xy, label, double=False, fontsize=18, label_offset=(0, 0)):
    x, y = xy
    ax.add_patch(Circle(xy, R, facecolor="white", edgecolor=BLACK, linewidth=1.6, zorder=3))
    if double:
        ax.add_patch(Circle(xy, R - 0.08, facecolor="white", edgecolor=BLACK, linewidth=1.4, zorder=4))
    ax.text(x + label_offset[0], y + label_offset[1], label,
            ha="center", va="center", fontsize=fontsize, zorder=5)


def draw_box(ax, xy, label, fontsize=18):
    x, y = xy
    w, h = 0.85, 0.7
    ax.add_patch(Rectangle((x - w / 2, y - h / 2), w, h,
                           facecolor="white", edgecolor=BLACK, linewidth=1.6, zorder=3))
    ax.text(x, y, label, ha="center", va="center", fontsize=fontsize, zorder=5)


def edge(ax, src, dst, color, shrink=R * 100, lw=2.2, rad=0.0):
    arrow = FancyArrowPatch(
        P[src], P[dst],
        arrowstyle="-|>",
        mutation_scale=18,
        color=color,
        lw=lw,
        shrinkA=22,
        shrinkB=22,
        connectionstyle=f"arc3,rad={rad}",
        zorder=2,
    )
    ax.add_patch(arrow)


fig, ax = plt.subplots(figsize=(7.6, 5.0))
ax.set_xlim(-0.3, 5.8)
ax.set_ylim(-0.3, 4.2)
ax.set_aspect("equal")
ax.axis("off")

# Nodes
draw_circle(ax, P["z"], r"$z$")
draw_box(ax, P["theta"], r"$\theta$")
draw_circle(ax, P["s"], r"$s$")
draw_circle(ax, P["tilde"], r"$\tilde a$", double=True)
draw_circle(ax, P["a"], r"$a$")
draw_circle(ax, P["sp"], r"$s'$")

# Red edges: local-policy / parameter path -> tilde a
edge(ax, "theta", "tilde", RED)
edge(ax, "z", "tilde", RED)
edge(ax, "s", "tilde", RED)

# Blue edges: tilde a + s -> a (marginalization to global policy)
edge(ax, "tilde", "a", BLUE)
edge(ax, "s", "a", BLUE)

# Black edges: dynamics
edge(ax, "a", "sp", BLACK)
edge(ax, "s", "sp", BLACK)

# Legend
from matplotlib.lines import Line2D

handles = [
    Line2D([0], [0], color=RED, lw=2.2,
           label=r"local policy  $\hat\pi(\tilde a \mid s, z;\,\theta)$"),
    Line2D([0], [0], color=BLUE, lw=2.2,
           label=r"global policy  $\pi(a\mid s) = \int p_z(z)\,\hat\pi(\cdot\mid s,z)\,dz$"),
    Line2D([0], [0], color=BLACK, lw=2.2,
           label=r"dynamics  $p(s'\mid s, a)$"),
]
ax.legend(
    handles=handles,
    loc="lower center",
    bbox_to_anchor=(0.5, -0.12),
    frameon=False,
    fontsize=11,
    ncol=1,
    handlelength=2.0,
    labelspacing=0.6,
)

fig.savefig(OUT, bbox_inches="tight", facecolor="white")
print(f"wrote {OUT}")
