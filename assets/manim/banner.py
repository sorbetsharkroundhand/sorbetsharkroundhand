from manim import *
import numpy as np

BG = "#0d1117"
SOIL = "#30363d"
GREENS = ["#7ee787", "#56d364", "#3fb950"]
NAME_COL = "#e6edf3"
SUB_COL = "#8b949e"

FW = 14.2222
FH = 14.2222 * 400 / 1280


def make_sprout(base_x, scale=1.0, flip=False):
    s = -scale if flip else scale
    base = np.array([base_x, -FH / 2 + 0.32, 0])
    tip_y = 1.55 * scale
    stem = CubicBezier(
        base,
        base + UP * 0.55 * scale + RIGHT * 0.18 * s,
        base + UP * 1.1 * scale + RIGHT * 0.06 * s,
        base + UP * tip_y,
        color=GREENS[2],
        stroke_width=max(3, 5 * scale),
    )

    leaves = VGroup()
    specs = [(0.38, 52), (0.62, -48), (0.82, 45)]
    for i, (t, ang) in enumerate(specs):
        p = stem.point_from_proportion(t)
        side = 1 if i % 2 == 0 else -1
        leaf = Ellipse(
            width=0.62 * scale,
            height=0.26 * scale,
            fill_color=GREENS[i % 3],
            fill_opacity=0.95,
            stroke_width=0,
        )
        leaf.rotate(side * ang * DEGREES)
        leaf.move_to(p + np.array([side * 0.28 * scale, 0.13 * scale, 0]))
        leaves.add(leaf)

    top_pair = VGroup()
    for side in [-1, 1]:
        tl = Ellipse(
            width=0.42 * scale,
            height=0.19 * scale,
            fill_color=GREENS[0],
            fill_opacity=1.0,
            stroke_width=0,
        )
        tl.rotate(side * 38 * DEGREES)
        tl.move_to(base + UP * tip_y + RIGHT * side * 0.16 * scale + UP * 0.07 * scale)
        top_pair.add(tl)

    plant = VGroup(stem, leaves, top_pair)
    return plant


class HerbBanner(Scene):
    def construct(self):
        self.camera.background_color = BG

        soil = Line(
            LEFT * FW / 2,
            RIGHT * FW / 2,
            color=SOIL,
            stroke_width=5,
        ).shift(DOWN * FH / 2 + UP * 0.32)

        grass = VGroup()
        rng = np.random.default_rng(7)
        for _ in range(26):
            x = rng.uniform(-FW / 2 + 0.3, FW / 2 - 0.3)
            h = rng.uniform(0.08, 0.22)
            tick = Line(
                [x, -FH / 2 + 0.32, 0],
                [x + rng.uniform(-0.08, 0.08), -FH / 2 + 0.32 + h, 0],
                color=SOIL,
                stroke_width=2.5,
            )
            grass.add(tick)

        left_plant = make_sprout(-4.6, scale=1.15)
        right_plant = make_sprout(4.6, scale=0.95, flip=True)

        name = Text("Jekyung Ryu", font="Helvetica Neue", weight=BOLD, font_size=76, color=NAME_COL)
        name.move_to(UP * 0.42)

        sub = Text(
            "on-device AI · Swift · Python",
            font="Helvetica Neue",
            slant=ITALIC,
            font_size=30,
            color=SUB_COL,
        )
        sub.next_to(name, DOWN, buff=0.34)

        self.play(Create(soil), FadeIn(grass), run_time=0.7)
        self.play(LaggedStartMap(GrowFromPoint, left_plant, arg_creator=lambda m: (m, m.get_corner(DOWN))), run_time=1.1)
        self.play(LaggedStartMap(GrowFromPoint, right_plant, arg_creator=lambda m: (m, m.get_corner(DOWN))), run_time=1.1)
        self.play(Write(name), run_time=1.2)
        self.play(FadeIn(sub, shift=UP * 0.2), run_time=0.7)
        self.wait(1.1)
