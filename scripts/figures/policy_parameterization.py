"""Render the FLAG policy-parameterization figure for the project page.

Layout: small prior p_z on the left, flow map arrow, and the action-space
panel on the right showing the global policy as a black curve and the
per-latent local Gaussians stacked on top of each flow anchor T_theta(s, z_i).
"""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib import rcParams

rcParams["mathtext.fontset"] = "cm"
rcParams["font.family"] = "serif"
rcParams["font.size"] = 12
rcParams["axes.linewidth"] = 0.8

REPO = Path(__file__).resolve().parents[2]
OUT = REPO / "src" / "assets" / "policy_parameterization_v2.pdf"

RED = "#b8232a"
TEAL = "#0F766E"
TEAL_FILL = "#0F766E"
BLACK = "#111111"


def gauss(x, mu, sigma):
    return np.exp(-((x - mu) ** 2) / (2 * sigma**2)) / (np.sqrt(2 * np.pi) * sigma)


anchors = np.array([-2.6, -0.9, 0.6, 2.2])
weights = np.array([0.28, 0.22, 0.27, 0.23])
local_sigma = 0.36

x = np.linspace(-4.6, 4.2, 700)
global_density = np.zeros_like(x)
for mu, w in zip(anchors, weights):
    global_density += w * gauss(x, mu, local_sigma * 1.45)
global_density /= global_density.max()
global_density *= 0.60

fig = plt.figure(figsize=(9.2, 4.2))
gs = fig.add_gridspec(
    1, 3, width_ratios=[1.0, 1.1, 3.2], wspace=0.05
)

# --- prior over z ---
ax_prior = fig.add_subplot(gs[0, 0])
z = np.linspace(-3.2, 3.2, 300)
pz = gauss(z, 0.0, 1.0)
pz_n = pz / pz.max() * 0.55
ax_prior.fill_between(z, pz_n, color=RED, alpha=0.18)
ax_prior.plot(z, pz_n, color=RED, linewidth=1.6)
ax_prior.set_ylim(0, 0.78)
ax_prior.set_xlim(-3.2, 3.2)
ax_prior.set_yticks([])
ax_prior.set_xticks([-2, 0, 2])
ax_prior.tick_params(axis="x", labelsize=9)
ax_prior.set_xlabel(r"$z \sim p_z$", fontsize=12, color=RED, labelpad=6)
for s in ("top", "right", "left"):
    ax_prior.spines[s].set_visible(False)
ax_prior.spines["bottom"].set_color("#888")

# --- arrow / flow map label ---
ax_arrow = fig.add_subplot(gs[0, 1])
ax_arrow.set_xlim(0, 1)
ax_arrow.set_ylim(0, 1)
ax_arrow.axis("off")
ax_arrow.annotate(
    "",
    xy=(0.97, 0.5),
    xytext=(0.03, 0.5),
    arrowprops=dict(arrowstyle="-|>", color=RED, lw=1.8, mutation_scale=18),
)
ax_arrow.text(
    0.5, 0.66, r"flow map  $T_\theta(s, z)$",
    ha="center", va="center", fontsize=12, color=RED,
)

# --- action-space panel ---
ax = fig.add_subplot(gs[0, 2])
ax.plot(
    x, global_density,
    color=BLACK, linewidth=2.6,
    label=r"global policy  $\pi(a\mid s) = \int p_z(z)\,\hat\pi(a\mid s,z)\,dz$",
)

for mu in anchors:
    g = gauss(x, mu, local_sigma)
    g = g / g.max() * 0.22
    ax.fill_between(x, g, color=TEAL_FILL, alpha=0.32)
    ax.plot(x, g, color=TEAL, linewidth=1.3)
    ax.plot([mu, mu], [0, 0.22], color=TEAL, linewidth=0.8, linestyle=(0, (2, 2)), alpha=0.6)
    ax.scatter([mu], [0], marker="v", color=RED, s=42, zorder=4, clip_on=False)

# Legend handles
from matplotlib.lines import Line2D
from matplotlib.patches import Patch

handles = [
    Line2D([0], [0], color=BLACK, lw=2.6,
           label=r"global policy  $\pi(a\mid s)$"),
    Patch(facecolor=TEAL_FILL, alpha=0.32, edgecolor=TEAL,
          label=r"local Gaussian  $\hat\pi(a\mid s, z) = \mathcal{N}(T_\theta(s,z),\,\Sigma)$"),
    Line2D([0], [0], marker="v", color="w", markerfacecolor=RED, markersize=8,
           label=r"flow anchor  $T_\theta(s, z_i)$"),
]
ax.legend(
    handles=handles, loc="upper right", frameon=False, fontsize=9.5,
    handlelength=1.6, labelspacing=0.45,
)

ax.set_xlim(-4.6, 4.2)
ax.set_ylim(-0.02, 0.82)
ax.set_yticks([])
ax.set_xticks([])
ax.set_xlabel(r"action  $a$", fontsize=11, labelpad=4)
for s in ("top", "right", "left"):
    ax.spines[s].set_visible(False)
ax.spines["bottom"].set_color("#888")

fig.savefig(OUT, bbox_inches="tight", facecolor="white")
print(f"wrote {OUT}")
