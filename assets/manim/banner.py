from manim import *
import numpy as np
import random

BG = "#0d1117"
SOIL = "#30363d"
GREENS = ["#7ee787", "#56d364", "#3fb950", "#2ea043"]
NAME_COL = "#e6edf3"
SUB_COL = "#8b949e"

FW = 14.2222
FH = 14.2222 * 400 / 1280
BASE_Y = -FH / 2 + 0.32


def grow_vine(start, angle_deg, length, depth, levels, rng):
    if depth <= 0 or length < 0.12:
        return
    angle = np.deg2rad(angle_deg)
    end = start + length * np.array([np.cos(angle), np.sin(angle), 0])
    c1 = start + length * 0.38 * np.array(
        [np.cos(np.deg2rad(angle_deg - 14)), np.sin(np.deg2rad(angle_deg - 14)), 0]
    )
    c2 = end + length * 0.30 * np.array(
        [np.cos(np.deg2rad(angle_deg + 18)), np.sin(np.deg2rad(angle_deg + 18)), 0]
    )
    seg = CubicBezier(start, c1, c2, end,
                      stroke_width=max(1.8, depth * 1.6),
                      color=GREENS[min(depth % len(GREENS), len(GREENS) - 1)])
    levels[depth].add(seg)

    if depth <= 2:
        leaf = Ellipse(width=0.30 * (depth + 2) / 4, height=0.13 * (depth + 2) / 4,
                       fill_color=GREENS[0], fill_opacity=0.95, stroke_width=0)
        leaf.move_to(end).rotate(angle + PI / 2)
        levels[depth].add(leaf)

    spread = rng.uniform(24, 36)
    grow_vine(end, angle_deg + spread, length * rng.uniform(0.66, 0.74), depth - 1, levels, rng)
    grow_vine(end, angle_deg - spread, length * rng.uniform(0.66, 0.74), depth - 1, levels, rng)


class HerbBanner(Scene):
    def construct(self):
        self.camera.background_color = BG
        rng = random.Random(11)

        soil = Line(LEFT * FW / 2, RIGHT * FW / 2,
                    color=SOIL, stroke_width=5).shift(DOWN * FH / 2 + UP * 0.32)

        name = Text("sorbetsharkroundhand", font="Helvetica Neue",
                    weight=BOLD, font_size=58, color=NAME_COL)
        if name.width > 10.5:
            name.scale_to_fit_width(10.5)
        name.move_to(UP * 0.45)

        sub = Text("data analysis · AI · Python · parsing",
                   font="Helvetica Neue", slant=ITALIC,
                   font_size=28, color=SUB_COL)
        sub.next_to(name, DOWN, buff=0.30)

        left_levels = {d: VGroup() for d in range(1, 7)}
        right_levels = {d: VGroup() for d in range(1, 7)}
        grow_vine(np.array([-FW / 2 + 0.15, BASE_Y, 0]), 62, 1.55, 6, left_levels, random.Random(4))
        grow_vine(np.array([FW / 2 - 0.15, BASE_Y, 0]), 118, 1.45, 6, right_levels, random.Random(9))

        def anim(levels):
            groups = [levels[d] for d in sorted(levels, reverse=True) if len(levels[d]) > 0]
            return LaggedStart(*[Create(g) for g in groups], lag_ratio=0.35)

        self.play(Create(soil), run_time=0.6)
        self.play(anim(left_levels), anim(right_levels), run_time=2.4)
        self.play(Write(name), run_time=1.3)
        self.play(FadeIn(sub, shift=UP * 0.2), run_time=0.7)
        self.wait(1.0)
