#!/home/eko/.venvs/proots/bin/python
#Replace your user at the top 

import argparse
import sys

import matplotlib.pyplot as plt
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr


class Args(argparse.Namespace):
    expr: str
    out: str
    save: bool
    transparent: bool
    # close_terminal: bool


def configure_plot_style(theme):
    plt.rcParams.update(
        {
            "font.family": "Noto Sans",
            "font.serif": ["STIXGeneral", "Times New Roman", "DejaVu Serif"],
            "mathtext.fontset": "stix",
            "axes.linewidth": 2,
            "axes.labelsize": 16,
            "axes.labelweight": "semibold",
            "xtick.labelsize": 14,
            "ytick.labelsize": 14,
            "figure.facecolor": theme["bg"],
            "axes.facecolor": theme["bg"],
            "text.color": theme["fg"],
            "axes.labelcolor": theme["fg"],
            "axes.edgecolor": theme["fg"],
            "xtick.color": theme["fg"],
            "ytick.color": theme["fg"],
            "toolbar": "none",
        }
    )


def build_parser():
    p = argparse.ArgumentParser(description="Plot complex roots of a polynomial in z.")
    p.add_argument("expr", help="Polynomial in z, e.g. z**3-1 (or z^3-1)")
    p.add_argument("--save","-s", action="store_true", help="Save image instead of showing GUI")
    p.add_argument("--out","-o", default="roots.png", help="Output image path (with --save)")
    p.add_argument("--transparent","-t", action="store_true", help="Save with transparent background")
    # p.add_argument('--close-terminal', '-ct', action='store_true',help='Close terminal after launching plot')
    return p # Returns the parser object


def compute_poly(expr_text):
    z = sp.symbols("z")
    expr_src = expr_text.replace("^", "**")
    # Type checking here with expr:
    # You can make a dictionary that only lives in the function call only
    expr: sp.Expr = parse_expr(expr_src, local_dict={"z": z})
    extra_symbols = expr.free_symbols - {z}
    if extra_symbols:
        extras = ", ".join(sorted(str(sym) for sym in extra_symbols))
        raise ValueError(f"expression must use only z; extra symbols: {extras}")
    if not expr.is_polynomial(z):
        raise ValueError("expression must be a polynomial in z (no negative powers or functions like sin)")
    poly = sp.Poly(expr, z)
    if poly.degree() <= 0:
        raise ValueError("polynomial must have degree >= 1")
    roots = [complex(r.evalf()) for r in poly.nroots()]
    return poly, roots


def set_symmetric_limits(ax, xs, ys, pad=1.1):
    lim = max(max(abs(x) for x in xs), max(abs(y) for y in ys))
    ax.set_xlim(-pad * lim, pad * lim)
    ax.set_ylim(-pad * lim, pad * lim)


def plot_roots(ax, xs, ys, poly, theme):
    ax.axhline(0, color=theme["axis_grey"], lw=2.0, zorder=0)
    ax.axvline(0, color=theme["axis_grey"], lw=2.0, zorder=0)

    set_symmetric_limits(ax, xs, ys)

    for x, y in zip(xs, ys):
        ax.plot([0, x], [0, y], color=theme["ray_color"], lw=2.4, zorder=1)
    ax.scatter(
        xs,
        ys,
        s=110,
        color=theme["point_color"],
        edgecolors=theme["bg"],
        linewidths=1.0,
        zorder=2,
    )
    ax.set_aspect("auto")
    ax.set_xlabel("Re")
    ax.set_ylabel("Im")
    ax.set_title(fr"Roots of ${sp.latex(poly.as_expr())}$", fontsize=20, pad=10)
    ax.minorticks_on()
    ax.tick_params(which="major", direction="in", top=True, right=True, length=7.5, width=1.8)
    ax.tick_params(which="minor", direction="in", top=True, right=True, length=4.0, width=1.2)
    ax.set_axisbelow(True)
    ax.grid(which="major", color=theme["grid_major"], linewidth=0.9, alpha=0.5)
    ax.grid(which="minor", color=theme["grid_minor"], linewidth=0.6, alpha=0.5)
    for spine in ax.spines.values():
        spine.set_linewidth(2.0)
    ax.margins(x=0, y=0)
    ax.set_anchor("C")


def attach_resize_scaling(fig, ax):
    base_w, base_h = fig.get_size_inches()
    base_title = ax.title.get_size()
    base_label = ax.xaxis.label.get_size()
    tick_labels = ax.get_xticklabels()
    base_tick = tick_labels[0].get_size() if tick_labels else base_label * 0.875

    def on_resize(event):
        w, h = fig.get_size_inches()
        scale = min(w / base_w, h / base_h)
        ax.title.set_fontsize(base_title * scale)
        ax.xaxis.label.set_size(base_label * scale)
        ax.yaxis.label.set_size(base_label * scale)
        ax.tick_params(labelsize=base_tick * scale)
        fig.canvas.draw_idle()

    fig.canvas.mpl_connect("resize_event", on_resize)


def main():
    theme = {
        "bg": "#0e1117",
        "fg": "#e6e6e6",
        "axis_grey": "#7a8597",
        "ray_color": "#8b5cf6",
        "point_color": "#4cc9f0",
        "grid_major": "#2b2f3a",
        "grid_minor": "#1f2430",
    }

    configure_plot_style(theme)

    # Method Chaining: cursed recomendation for refactor
    args = build_parser().parse_args(namespace=Args())

    # Equivalent to
    # parser = build_parser()
    # args = parser.parse_args(namespace=Args())

    # Apparently we gotta fork it before any matplotib gets to work
    # if args.close_terminal:
    import os
    pid = os.fork()
    if pid > 0:
        sys.exit(0)

    try:
        poly, roots = compute_poly(args.expr)
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        raise SystemExit(2)
    xs = [r.real for r in roots]
    ys = [r.imag for r in roots]

    fig, ax = plt.subplots()
    plot_roots(ax, xs, ys, poly, theme)
    attach_resize_scaling(fig, ax)
    fig.subplots_adjust(left=0.12, right=0.98, bottom=0.14, top=0.86)

    if args.save:
        fig.savefig(args.out, dpi=180, transparent=args.transparent)
        print(args.out)
    else:
        plt.show()


if __name__ == "__main__":
    main()
