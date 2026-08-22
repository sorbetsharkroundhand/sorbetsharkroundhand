from manim import *
import numpy as np

GREEN_L = "#39d353"
GREEN_M = "#26a641"
SAGE = "#a8d5ba"

FW = 14.2222
FH = FW * 396 / 1584


def make_leaf(direction, length=0.44, width_deg=95):
    tip = RIGHT * length
    upper = ArcBetweenPoints(ORIGIN, tip, angle=-width_deg * DEGREES)
    lower = ArcBetweenPoints(tip, ORIGIN, angle=-width_deg * DEGREES)
    lf = VGroup(upper, lower)
    lf.set_fill(GREEN_M, 1.0).set_stroke(GREEN_L, 1.3)
    u = np.array(direction, dtype=float)
    u /= max(float(np.linalg.norm(u)), 1e-6)
    lf.rotate(np.arctan2(u[1], u[0]), about_point=ORIGIN)
    return lf


class HubHerbBanner(Scene):
    def construct(self):
        self.camera.background_opacity = 0

        seed_c = np.array([0.0, -0.45, 0.0])
        seed = Circle(
            radius=0.17,
            fill_color=SAGE,
            fill_opacity=1.0,
            stroke_color=GREEN_M,
            stroke_width=2.2,
        ).move_to(seed_c)

        tips = [
            (-5.75, 0.35),
            (-3.35, 0.92),
            (-0.05, 1.12),
            (3.25, 0.88),
            (5.80, 0.32),
        ]

        stems = VGroup()
        mid_leaves = VGroup()
        tip_nodes = VGroup()
        tip_leaves = VGroup()
        rng = np.random.default_rng(5)

        for i, (tx, ty) in enumerate(tips):
            end = np.array([tx, ty, 0.0])
            dirv = end - seed_c
            L = float(np.linalg.norm(dirv))
            u = dirv / L
            perp = np.array([-u[1], u[0], 0.0])
            sgn = 1.0 if i % 2 == 0 else -1.0

            c1 = seed_c + u * (L * 0.32) + perp * (L * 0.10 * sgn)
            c2 = end - u * (L * 0.34) - perp * (L * 0.13 * sgn)
            stem = CubicBezier(
                seed_c, c1, c2, end,
                stroke_color=GREEN_L,
                stroke_width=3.0,
            )
            stems.add(stem)

            pm = stem.point_from_proportion(0.58)
            pt = stem.point_from_proportion(0.66)
            tang = pt - pm
            ml = make_leaf(tang, length=0.34 + 0.05 * (i % 2))
            ml.shift(pm)
            mid_leaves.add(ml)

            node = Circle(
                radius=0.085,
                fill_color=GREEN_M,
                fill_opacity=1.0,
                stroke_width=0,
            ).move_to(end)
            tip_nodes.add(node)

            tl = make_leaf(u, length=0.46)
            tl.shift(end)
            tip_leaves.add(tl)

            tl2 = make_leaf(-u + UP * 0.35, length=0.30)
            tl2.shift(end)
            tip_leaves.add(tl2)

        plant = VGroup(stems, mid_leaves, tip_nodes, tip_leaves)
        garden = VGroup(seed, plant)
        garden.move_to(UP * 0.02)
        seed_c = seed.get_center()

        self.play(GrowFromCenter(seed), run_time=0.5)
        self.play(LaggedStartMap(Create, stems, lag_ratio=0.3), run_time=1.8)
        self.play(
            LaggedStartMap(GrowFromPoint, mid_leaves, arg_creator=lambda m: (m, m.get_right())),
            run_time=0.7,
        )
        self.play(
            LaggedStartMap(GrowFromCenter, tip_nodes, lag_ratio=0.25),
            LaggedStartMap(
                GrowFromPoint, tip_leaves,
                arg_creator=lambda m: (m, m.get_corner(DOWN)),
            ),
            run_time=1.0,
        )

        def wobble(m, alpha):
            m.restore()
            m.rotate(0.045 * np.sin(alpha * TAU * 2), about_point=seed_c)
            m.rotate(0.02 * np.sin(alpha * TAU * 3 + 1.3), about_point=seed_c)

        plant.save_state()
        self.play(UpdateFromAlphaFunc(plant, wobble), run_time=1.8)
        self.wait(0.4)

        folded = plant.copy().scale(0.01).move_to(seed_c)
        self.play(
            Transform(plant, folded),
            FadeOut(seed, scale=0.2),
            run_time=0.8,
            rate_func=rush_into,
        )
        self.remove(plant)
