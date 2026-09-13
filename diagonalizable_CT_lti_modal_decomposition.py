"""Animate modal decomposition of a continuous-time autonomous LTI system.

The animation considers a real diagonalizable two-dimensional system

    x_dot(t) = A x(t)

with two real, negative eigenvalues.  An initial condition that does not lie on
either eigenspace is decomposed as

    x(0) = c1*v1 + c2*v2.

The modal components then evolve independently,

    x1(t) = c1*exp(lambda1*t)*v1,
    x2(t) = c2*exp(lambda2*t)*v2,

and their moving parallelogram reconstructs the total trajectory

    x(t) = x1(t) + x2(t).

Preview render:

    python -m manim -pql continuous_time_modal_decomposition_manim.py ContinuousTimeModalDecomposition

High-quality render:

    python -m manim -pqh continuous_time_modal_decomposition_manim.py ContinuousTimeModalDecomposition
"""

from manim import *
import numpy as np


# ---------------------------------------------------------------------------
# Parameters that are convenient to change between renders
# ---------------------------------------------------------------------------
LAMBDA_1 = -0.35          # slow mode
LAMBDA_2 = -1.10          # fast mode
COEFFICIENT_1 = 1.10
COEFFICIENT_2 = 0.50
FINAL_TIME = 7.0

# The first part of the motion is slow enough to discuss the construction.
FIRST_MOTION_RUN_TIME = 3.2
SECOND_MOTION_RUN_TIME = 2.8
REMAINING_MOTION_RUN_TIME = 6.5


class ContinuousTimeModalDecomposition(Scene):
    def construct(self):
        eigenvector_1 = np.array([2.0, 1.0])
        eigenvector_2 = np.array([1.0, 3.0])

        initial_component_1 = COEFFICIENT_1 * eigenvector_1
        initial_component_2 = COEFFICIENT_2 * eigenvector_2
        initial_state = initial_component_1 + initial_component_2

        def component_1(t):
            return np.exp(LAMBDA_1 * t) * initial_component_1

        def component_2(t):
            return np.exp(LAMBDA_2 * t) * initial_component_2

        def total_state(t):
            return component_1(t) + component_2(t)

        # ------------------------------------------------------------------
        # Opening assumption: this is the exact condition that allows a
        # decomposition into two independent real modal motions.
        # ------------------------------------------------------------------
        opening_assumption = VGroup(
            Tex("Assume that the autonomous LTI system is diagonalizable"),
            MathTex(
                r"\dot{\mathbf{x}}=A\mathbf{x},"
                r"\qquad A\mathbf{v}_i=\lambda_i\mathbf{v}_i,"
                r"\qquad \lambda_1,\lambda_2\in\mathbb{R}_{<0}"
            ),
        ).arrange(DOWN, buff=0.28)
        opening_assumption[0].scale(0.72)
        opening_assumption[1].scale(0.65)

        self.play(Write(opening_assumption[0]), run_time=1.2)
        self.play(Write(opening_assumption[1]), run_time=1.7)
        self.wait(1.1)
        self.play(FadeOut(opening_assumption), run_time=0.8)

        title = Tex("Free evolution from a generic initial condition")
        title.scale(0.70).to_edge(UP, buff=0.13)

        system_equation = MathTex(
            r"\dot{\mathbf{x}}(t)=A\mathbf{x}(t),"
            r"\qquad A\text{ diagonalizable over }\mathbb{R}"
        ).scale(0.57)
        system_equation.next_to(title, DOWN, buff=0.09)

        plane = NumberPlane(
            x_range=[-3.7, 3.7, 1],
            y_range=[-3.7, 3.7, 1],
            x_length=6.55,
            y_length=6.55,
            background_line_style={
                "stroke_color": GREY_B,
                "stroke_width": 1,
                "stroke_opacity": 0.25,
            },
            axis_config={
                "stroke_width": 1.8,
                "include_tip": True,
                "tip_width": 0.14,
                "tip_height": 0.14,
                "include_ticks": False,
            },
        ).shift(DOWN * 0.65)

        axis_labels = VGroup(
            MathTex(r"x_1").scale(0.50).next_to(
                plane.x_axis.get_end(), RIGHT, buff=0.03
            ),
            MathTex(r"x_2").scale(0.50).next_to(
                plane.y_axis.get_end(), UP, buff=0.03
            ),
        )

        def full_eigenspace(direction, color):
            unit_direction = direction / np.linalg.norm(direction)
            extent = 5.2
            return DashedLine(
                plane.c2p(
                    *(extent * unit_direction)
                ),
                plane.c2p(
                    *(-extent * unit_direction)
                ),
                color=color,
                stroke_width=2.7,
                dash_length=0.14,
            )

        eigenspace_1 = full_eigenspace(eigenvector_1, GREEN_C)
        eigenspace_2 = full_eigenspace(eigenvector_2, BLUE_C)

        def vector_arrow(vector, color, width=4.2, opacity=1.0):
            arrow = Arrow(
                plane.c2p(0, 0),
                plane.c2p(vector[0], vector[1]),
                buff=0,
                color=color,
                stroke_width=width,
                max_tip_length_to_length_ratio=0.13,
            )
            arrow.set_opacity(opacity)
            return arrow

        def vector_dot(vector, color, radius=0.075, opacity=1.0):
            dot = Dot(
                plane.c2p(vector[0], vector[1]),
                radius=radius,
                color=color,
            )
            dot.set_opacity(opacity)
            return dot

        # A compact horizontal legend remains visible during the motion.
        def legend_entry(color, formula):
            sample = Line(
                LEFT * 0.18,
                RIGHT * 0.18,
                color=color,
                stroke_width=5,
            )
            label = MathTex(formula).scale(0.44)
            return VGroup(sample, label).arrange(RIGHT, buff=0.08)

        legend = VGroup(
            legend_entry(GREEN_C, r"\mathbf{x}_1(t)"),
            legend_entry(BLUE_C, r"\mathbf{x}_2(t)"),
            legend_entry(PINK, r"\mathbf{x}(t)"),
        ).arrange(RIGHT, buff=0.32)
        legend.to_corner(UR, buff=0.28).shift(DOWN * 1.08)

        self.play(Write(title), Write(system_equation), run_time=1.2)
        self.play(
            Create(plane),
            FadeIn(axis_labels),
            run_time=1.6,
        )

        # ------------------------------------------------------------------
        # 1. Introduce the two eigenspaces and their different decay rates.
        # ------------------------------------------------------------------
        eigenvector_arrow_1 = vector_arrow(eigenvector_1, GREEN_C)
        eigenvector_dot_1 = vector_dot(eigenvector_1, GREEN_C)
        eigenvector_label_1 = MathTex(r"\mathbf{v}_1").scale(0.47)
        eigenvector_label_1.set_color(GREEN_C)
        eigenvector_label_1.next_to(eigenvector_dot_1, UR, buff=0.07)

        eigenvector_arrow_2 = vector_arrow(eigenvector_2, BLUE_C)
        eigenvector_dot_2 = vector_dot(eigenvector_2, BLUE_C)
        eigenvector_label_2 = MathTex(r"\mathbf{v}_2").scale(0.47)
        eigenvector_label_2.set_color(BLUE_C)
        eigenvector_label_2.next_to(eigenvector_dot_2, UR, buff=0.07)

        first_eigenpair = MathTex(
            r"A\mathbf{v}_1=",
            rf"{LAMBDA_1:.2f}",
            r"\mathbf{v}_1"
        ).scale(0.56).to_edge(DOWN, buff=0.13)
        first_eigenpair.set_color(GREEN_C)

        second_eigenpair = MathTex(
            r"A\mathbf{v}_2=",
            rf"{LAMBDA_2:.2f}",
            r"\mathbf{v}_2"
        ).scale(0.56).move_to(first_eigenpair)
        second_eigenpair.set_color(BLUE_C)

        self.play(Create(eigenspace_1), run_time=1.0)
        self.play(
            GrowArrow(eigenvector_arrow_1),
            FadeIn(eigenvector_dot_1, eigenvector_label_1),
            Write(first_eigenpair),
            run_time=1.2,
        )

        self.play(Create(eigenspace_2), run_time=1.0)
        self.play(
            GrowArrow(eigenvector_arrow_2),
            FadeIn(eigenvector_dot_2, eigenvector_label_2),
            Transform(first_eigenpair, second_eigenpair),
            run_time=1.2,
        )
        self.wait(0.6)
        self.play(
            FadeOut(
                eigenvector_arrow_1,
                eigenvector_dot_1,
                eigenvector_label_1,
                eigenvector_arrow_2,
                eigenvector_dot_2,
                eigenvector_label_2,
                first_eigenpair,
            ),
            FadeIn(legend),
            run_time=0.8,
        )

        # ------------------------------------------------------------------
        # 2. Choose x(0) outside both eigenspaces and decompose it.
        # ------------------------------------------------------------------
        initial_state_arrow = vector_arrow(initial_state, PINK, width=5.0)
        initial_state_dot = vector_dot(initial_state, PINK, radius=0.100)
        initial_state_label = MathTex(r"\mathbf{x}(0)").scale(0.49)
        initial_state_label.set_color(PINK)
        initial_state_label.next_to(initial_state_dot, UR, buff=0.07)

        generic_initial_condition = MathTex(
            r"\mathbf{x}(0)\notin E_{\lambda_1}\cup E_{\lambda_2}"
        ).scale(0.57).to_edge(DOWN, buff=0.13)
        generic_initial_condition.set_color(PINK)

        self.play(
            GrowArrow(initial_state_arrow),
            FadeIn(initial_state_dot, initial_state_label),
            Write(generic_initial_condition),
            run_time=1.3,
        )
        self.wait(0.6)

        component_arrow_1 = vector_arrow(initial_component_1, GREEN_C)
        component_dot_1 = vector_dot(
            initial_component_1, GREEN_C, radius=0.080
        )
        component_label_1 = MathTex(r"c_1\mathbf{v}_1").scale(0.45)
        component_label_1.set_color(GREEN_C)
        component_label_1.next_to(component_dot_1, DR, buff=0.07)

        component_arrow_2 = vector_arrow(initial_component_2, BLUE_C)
        component_dot_2 = vector_dot(
            initial_component_2, BLUE_C, radius=0.080
        )
        component_label_2 = MathTex(r"c_2\mathbf{v}_2").scale(0.45)
        component_label_2.set_color(BLUE_C)
        component_label_2.next_to(component_dot_2, UL, buff=0.07)

        parallelogram_side_1 = DashedLine(
            plane.c2p(initial_component_1[0], initial_component_1[1]),
            plane.c2p(initial_state[0], initial_state[1]),
            color=BLUE_C,
            stroke_width=2.5,
            dash_length=0.11,
        )
        parallelogram_side_2 = DashedLine(
            plane.c2p(initial_component_2[0], initial_component_2[1]),
            plane.c2p(initial_state[0], initial_state[1]),
            color=GREEN_C,
            stroke_width=2.5,
            dash_length=0.11,
        )

        decomposition_formula = MathTex(
            r"\mathbf{x}(0)=",
            r"c_1\mathbf{v}_1",
            r"+",
            r"c_2\mathbf{v}_2",
        ).scale(0.60).move_to(generic_initial_condition)
        decomposition_formula[0].set_color(PINK)
        decomposition_formula[1].set_color(GREEN_C)
        decomposition_formula[3].set_color(BLUE_C)

        self.play(
            GrowArrow(component_arrow_1),
            FadeIn(component_dot_1, component_label_1),
            run_time=1.5,
        )
        self.play(
            GrowArrow(component_arrow_2),
            FadeIn(component_dot_2, component_label_2),
            run_time=1.5,
        )
        self.play(
            Create(parallelogram_side_1),
            Create(parallelogram_side_2),
            Transform(generic_initial_condition, decomposition_formula),
            run_time=1.8,
        )
        self.wait(1.0)

        # ------------------------------------------------------------------
        # 3. Evolve both modes and reconstruct their sum continuously.
        # ------------------------------------------------------------------
        time = ValueTracker(0.0)

        moving_component_arrow_1 = always_redraw(
            lambda: vector_arrow(component_1(time.get_value()), GREEN_C)
        )
        moving_component_dot_1 = always_redraw(
            lambda: vector_dot(
                component_1(time.get_value()),
                GREEN_C,
                radius=0.080,
            )
        )

        moving_component_arrow_2 = always_redraw(
            lambda: vector_arrow(component_2(time.get_value()), BLUE_C)
        )
        moving_component_dot_2 = always_redraw(
            lambda: vector_dot(
                component_2(time.get_value()),
                BLUE_C,
                radius=0.080,
            )
        )

        moving_total_arrow = always_redraw(
            lambda: vector_arrow(
                total_state(time.get_value()),
                PINK,
                width=5.0,
            )
        )
        moving_total_dot = always_redraw(
            lambda: vector_dot(
                total_state(time.get_value()),
                PINK,
                radius=0.100,
            )
        )

        moving_parallelogram_side_1 = always_redraw(
            lambda: DashedLine(
                plane.c2p(*component_1(time.get_value())),
                plane.c2p(*total_state(time.get_value())),
                color=BLUE_C,
                stroke_width=2.4,
                dash_length=0.10,
            )
        )
        moving_parallelogram_side_2 = always_redraw(
            lambda: DashedLine(
                plane.c2p(*component_2(time.get_value())),
                plane.c2p(*total_state(time.get_value())),
                color=GREEN_C,
                stroke_width=2.4,
                dash_length=0.10,
            )
        )

        mode_1_trace = TracedPath(
            moving_component_dot_1.get_center,
            stroke_color=GREEN_C,
            stroke_width=5.0,
            stroke_opacity=0.62,
            dissipating_time=None,
        )
        mode_2_trace = TracedPath(
            moving_component_dot_2.get_center,
            stroke_color=BLUE_C,
            stroke_width=5.0,
            stroke_opacity=0.62,
            dissipating_time=None,
        )
        total_trace = TracedPath(
            moving_total_dot.get_center,
            stroke_color=PINK,
            stroke_width=5.5,
            stroke_opacity=0.90,
            dissipating_time=None,
        )

        time_readout = always_redraw(
            lambda: VGroup(
                MathTex(r"t=").scale(0.52),
                DecimalNumber(
                    time.get_value(),
                    num_decimal_places=1,
                ).scale(0.52),
            )
            .arrange(RIGHT, buff=0.04)
            .next_to(system_equation, DOWN, buff=0.08)
        )

        evolution_formula = MathTex(
            r"\mathbf{x}(t)=",
            r"c_1e^{\lambda_1t}\mathbf{v}_1",
            r"+",
            r"c_2e^{\lambda_2t}\mathbf{v}_2",
        ).scale(0.56).move_to(generic_initial_condition)
        evolution_formula[0].set_color(PINK)
        evolution_formula[1].set_color(GREEN_C)
        evolution_formula[3].set_color(BLUE_C)

        self.play(
            FadeOut(component_label_1, component_label_2, initial_state_label),
            Transform(generic_initial_condition, evolution_formula),
            FadeIn(time_readout),
            run_time=1.0,
        )

        # Replace the static construction with an identical dynamic one.
        self.remove(
            initial_state_arrow,
            initial_state_dot,
            component_arrow_1,
            component_dot_1,
            component_arrow_2,
            component_dot_2,
            parallelogram_side_1,
            parallelogram_side_2,
        )
        self.add(
            mode_1_trace,
            mode_2_trace,
            total_trace,
            moving_component_arrow_1,
            moving_component_dot_1,
            moving_component_arrow_2,
            moving_component_dot_2,
            moving_parallelogram_side_1,
            moving_parallelogram_side_2,
            moving_total_arrow,
            moving_total_dot,
        )

        self.wait(0.5)

        # Slow first interval: both modal contractions and the changing
        # parallelogram are clearly visible.
        self.play(
            time.animate.set_value(1.5),
            run_time=FIRST_MOTION_RUN_TIME,
            rate_func=linear,
        )
        self.wait(0.45)

        # By this stage the faster blue component is visibly smaller.
        self.play(
            time.animate.set_value(3.0),
            run_time=SECOND_MOTION_RUN_TIME,
            rate_func=linear,
        )
        self.wait(0.45)

        self.play(
            time.animate.set_value(FINAL_TIME),
            run_time=REMAINING_MOTION_RUN_TIME,
            rate_func=linear,
        )

        conclusion = MathTex(
            r"|\lambda_2|>|\lambda_1|",
            r"\quad\Longrightarrow\quad",
            r"\text{the fast mode disappears first}",
        ).scale(0.56).move_to(generic_initial_condition)
        conclusion[0].set_color(BLUE_C)
        conclusion[2].set_color(GREEN_C)

        self.play(
            Transform(generic_initial_condition, conclusion),
            eigenspace_1.animate.set_stroke(width=4.0, opacity=0.95),
            eigenspace_2.animate.set_stroke(opacity=0.35),
            run_time=1.3,
        )
        self.wait(2.0)


