"""Render the latent-augmented MDP (z-MDP) graphical model for the project page.

Red edges = local-policy / parameter path (z, theta, s -> local action node).
Blue edges = marginalization to the global policy action.
Black edges = environment dynamics.
"""

from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib import rcParams
from matplotlib.lines import Line2D
from matplotlib.patches import Circle, FancyArrowPatch, Rectangle

rcParams["mathtext.fontset"] = "cm"
rcParams["font.family"] = "serif"
rcParams["font.size"] = 14
rcParams["axes.linewidth"] = 0.0

REPO = Path(__file__).resolve().parents[2]
OUT = REPO / "src" / "assets" / "zMDP.pdf"

RED = "#c81e2a"
BLUE = "#1f4eb0"
BLACK = "#111111"
GRAY = "#9b9b9b"

# Node positions (x, y)
P = {
    "z":     (0.85, 0.75),
    "theta": (0.85, 3.35),
    "s":     (3.35, 0.75),
    "tilde": (3.35, 3.35),
    "a":     (5.9, 3.35),
    "sp":    (5.9, 0.75),
}

R = 0.55  # node radius


def draw_circle(ax, xy, label, double=False, fontsize=18, label_offset=(0, 0)):
    x, y = xy
    ax.add_patch(Circle(xy, R, facecolor="white", edgecolor=BLACK, linewidth=3.0, zorder=3))
    if double:
        ax.add_patch(Circle(xy, R - 0.10, facecolor="white", edgecolor=BLACK, linewidth=2.5, zorder=4))
    ax.text(x + label_offset[0], y + label_offset[1], label,
            ha="center", va="center", fontsize=fontsize, zorder=5)


def draw_box(ax, xy, label, fontsize=18):
    x, y = xy
    w, h = 1.05, 0.85
    ax.add_patch(Rectangle((x - w / 2, y - h / 2), w, h,
                           facecolor="white", edgecolor=BLACK, linewidth=3.0, zorder=3))
    ax.text(x, y, label, ha="center", va="center", fontsize=fontsize, zorder=5)


def edge(ax, src, dst, color, lw=4.8, rad=0.0):
    arrow = FancyArrowPatch(
        P[src], P[dst],
        arrowstyle="-|>",
        mutation_scale=32,
        color=color,
        lw=lw,
        shrinkA=34,
        shrinkB=34,
        connectionstyle=f"arc3,rad={rad}",
        zorder=2,
    )
    ax.add_patch(arrow)


def label_row(ax, y, title, color, formula, formula_x=10.35):
    ax.text(
        7.2, y, title,
        ha="left", va="center", fontsize=20, zorder=2,
        bbox=dict(boxstyle="square,pad=0.05", facecolor=color,
                  edgecolor="none", alpha=0.30),
    )
    ax.text(formula_x, y, formula, ha="left", va="center", fontsize=24, zorder=2)


fig, ax = plt.subplots(figsize=(18.9, 4.7))
ax.set_xlim(-0.1, 18.8)
ax.set_ylim(-0.25, 4.25)
ax.set_aspect("equal")
ax.axis("off")

# Nodes
draw_circle(ax, P["z"], r"$z$", fontsize=27)
draw_box(ax, P["theta"], r"$\theta$", fontsize=27)
draw_circle(ax, P["s"], r"$s$", fontsize=27)
draw_circle(ax, P["tilde"], r"$\tilde a$", double=True, fontsize=27)
draw_circle(ax, P["a"], r"$a$", fontsize=27)
draw_circle(ax, P["sp"], r"$s'$", fontsize=27)

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

# Labels
ax.text(10.35, 3.78, r"$\hat s=(s,z)$", ha="left", va="center", fontsize=24, zorder=2)
label_row(ax, 3.12, "Local Policy", RED,
          r"$\hat\pi(a\mid s,z;\theta)$")
label_row(ax, 2.22, "Global Policy", BLUE,
          r"$\pi(a\mid s)=\int\quad p_z(z)\,\hat\pi(a\mid s,z;\theta)\,dz$")
label_row(ax, 1.22, "Dynamics", GRAY,
          r"$\hat p(\hat s'\mid \hat s,a)=p(s'\mid s,a)p_z(z')$")
label_row(ax, 0.32, "Reward", GRAY,
          r"$r(\hat s,a)=r(s,a)$")

for y, color in [(3.12, RED), (2.22, BLUE), (1.22, BLACK), (0.32, BLACK)]:
    ax.add_line(Line2D([6.85, 7.12], [y, y], color=color, lw=4.8, zorder=2))

fig.savefig(OUT, bbox_inches="tight", facecolor="white")
print(f"wrote {OUT}")
