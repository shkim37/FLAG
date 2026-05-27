# FLAG: Flow Policy MaxEnt-RL by Latent Augmented Guidance

**Sungha Kim\*, Gawon Lee\*, Jusuk Lee, Jonghae Park, H. Jin Kim, Daesol Cho**

*Lab for Autonomous Robotics Research, Seoul National University / Georgia Institute of Technology*

\* Equal contribution

---

Project page for our paper **FLAG**, which trains expressive flow policies for MaxEnt-RL through supervised target matching with latent-conditioned local importance sampling, enabling scalable high-dimensional control.

**[[Project Page](https://shkim37.github.io/FLAG)] [[arXiv](https://arxiv.org/abs/2506.00000)]**

## Overview

Prior diffusion/flow-based policy methods use **global importance sampling (IS)** to match a MaxEnt-RL target distribution, which fails in high-dimensional action spaces due to sparse supervision. FLAG introduces **local IS**: by conditioning both the proposal and target on the same flow latent variable, reweighting happens inside a shared local region, yielding dense and informative supervision at scale.

## Repository

This repository contains the source code for the FLAG project page, built with [Astro](https://astro.build/), [Tailwind CSS](https://tailwindcss.com/), [MDX](https://mdxjs.com/), and [React](https://react.dev/).

```bash
npm install      # install dependencies
npm run dev      # dev server → http://localhost:4321
npm run build    # build → ./dist/
```
