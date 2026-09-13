"""Animate a discrete-time autonomous LTI trajectory on an eigenspace.

The animation considers

    x[k+1] = A x[k]

and an eigenspace span([2, 1]^T) associated with a real eigenvalue satisfying
0 < lambda < 1.  A state on this eigenspace is mapped to a shorter state on
the same line.  Repeating the operation produces

    x[k] = lambda**k x[0].

The final part varies lambda while keeping the eigenspace and initial
condition fixed.

High-quality render:

    python -m manim -pqh evolution_along_eigenspace_manim.py EvolutionAlongEigenspace
"""

from manim import *
import numpy as np


# ---------------------------------------------------------------------------
# Parameters that are convenient to change between renders
# ---------------------------------------------------------------------------
BASE_EIGENVALUE = 0.72
INITIAL_SCALE = 1.60
NUMBER_OF_STEPS = 7
STEP_RUN_TIME = 0.72
EARLY_STEP_RUN_TIME = 1.30


class EvolutionAlongEigenspace(Scene):
    def construct(self):
        eigenvector = np.array([2.0, 1.0])
        initial_state = INITIAL_SCALE * eigenvector

        def modal_state(k, eigenvalue=BASE_EIGENVALUE):
            return eigenvalue**k * initial_state

        title = Tex("Free evolution along an eigenspace")
        title.scale(0.70).to_edge(UP, buff=0.14)

        system_equation = MathTex(
            r"\mathbf{x}[k+1]=A\mathbf{x}[k]"
        ).scale(0.62)
        system_equation.next_to(title, DOWN, buff=0.10)

        plane_style = {
            "background_line_style": {
                "stroke_color": GREY_B,
                "stroke_width": 1,
                "stroke_opacity": 0.27,
            },
            "axis_config": {
                "stroke_width": 1.7,
                "include_tip": True,
                "tip_width": 0.14,
                "tip_height": 0.14,
            },
        }

        current_plane = NumberPlane(
            x_range=[-3.5, 3.5, 1],
            y_range=[-3.5, 3.5, 1],
            x_length=5.05,
            y_length=5.05,
            **plane_style,
        )
        next_plane = NumberPlane(
            x_range=[-3.5, 3.5, 1],
            y_range=[-3.5, 3.5, 1],
            x_length=5.05,
            y_length=5.05,
            **plane_style,
        )

        planes = VGroup(current_plane, next_plane)
        planes.arrange(RIGHT, buff=1.50).shift(DOWN * 0.65)

        # Position the labels manually so that they remain close to the tips.
        current_axis_labels = VGroup(
            MathTex(r"x_1").scale(0.50).next_to(
                current_plane.x_axis.get_end(), RIGHT, buff=0.03
            ),
            MathTex(r"x_2").scale(0.50).next_to(
                current_plane.y_axis.get_end(), UP, buff=0.03
            ),
        )
        next_axis_labels = VGroup(
            MathTex(r"x_1^{+}").scale(0.50).next_to(
                next_plane.x_axis.get_end(), RIGHT, buff=0.03
            ),
            MathTex(r"x_2^{+}").scale(0.50).next_to(
                next_plane.y_axis.get_end(), UP, buff=0.03
            ),
        )

        current_title = MathTex(r"\mathbf{x}[k]").scale(0.56)
        current_title.next_to(current_plane, UP, buff=0.25)
        current_title.align_to(current_plane, LEFT).shift(RIGHT * 0.20)
        next_title = MathTex(r"\mathbf{x}[k+1]").scale(0.56)
        next_title.next_to(next_plane, UP, buff=0.25)
        next_title.align_to(next_plane, LEFT).shift(RIGHT * 0.20)

        map_arrow = Arrow(
            current_plane.get_right() + RIGHT * 0.12,
            next_plane.get_left() + LEFT * 0.12,
            buff=0.08,
            color=WHITE,
            stroke_width=3,
            max_tip_length_to_length_ratio=0.18,
        )
        map_label = MathTex(r"A").scale(0.64)
        map_label.next_to(map_arrow, UP, buff=0.06)

        def eigenspace_line(plane):
            return DashedLine(
                plane.c2p(-3.5, -1.75),
                plane.c2p(3.5, 1.75),
                color=GREEN_C,
                stroke_width=2.8,
                dash_length=0.14,
            )

        current_eigenspace = eigenspace_line(current_plane)
        next_eigenspace = eigenspace_line(next_plane)

        def state_arrow(plane, state, color=PINK, opacity=1.0, width=4.4):
            arrow = Arrow(
                plane.c2p(0, 0),
                plane.c2p(state[0], state[1]),
                buff=0,
                color=color,
                stroke_width=width,
                max_tip_length_to_length_ratio=0.13,
            )
            arrow.set_opacity(opacity)
            return arrow

        def state_dot(plane, state, color=PINK, opacity=1.0, radius=0.065):
            dot = Dot(
                plane.c2p(state[0], state[1]),
                radius=radius,
                color=color,
            )
            dot.set_opacity(opacity)
            return dot

        def indexed_state_dot(
            plane,
            state,
            index,
            color=PINK,
            opacity=1.0,
            radius=0.115,
        ):
            """A larger state marker with its discrete-time index inside."""
            circle = Dot(
                plane.c2p(state[0], state[1]),
                radius=radius,
                color=color,
            )
            label = Text(str(index), font_size=15, color=BLACK)
            label.move_to(circle)
            marker = VGroup(circle, label)
            marker.set_opacity(opacity)
            return marker

        self.play(Write(title), Write(system_equation), run_time=1.2)
        self.play(
            Create(current_plane),
            Create(next_plane),
            FadeIn(current_axis_labels, next_axis_labels),
            FadeIn(current_title, next_title),
            GrowArrow(map_arrow),
            FadeIn(map_label),
            run_time=1.8,
        )

        # ------------------------------------------------------------------
        # First show the defining property of an eigenvector.
        # ------------------------------------------------------------------
        self.play(
            Create(current_eigenspace),
            Create(next_eigenspace),
            run_time=1.4,
        )

        demonstration_state = eigenvector
        demonstration_image = BASE_EIGENVALUE * demonstration_state

        demonstration_left = state_arrow(
            current_plane, demonstration_state, color=YELLOW_C
        )
        demonstration_left_dot = state_dot(
            current_plane, demonstration_state, color=YELLOW_C
        )
        demonstration_right = state_arrow(
            next_plane, demonstration_image, color=YELLOW_C
        )
        demonstration_right_dot = state_dot(
            next_plane, demonstration_image, color=YELLOW_C
        )

        eigenvector_label = MathTex(r"\mathbf{v}").scale(0.48).set_color(YELLOW_C)
        eigenvector_label.next_to(demonstration_left_dot, UR, buff=0.08)
        image_label = MathTex(r"\lambda\mathbf{v}").scale(0.48).set_color(YELLOW_C)
        image_label.next_to(demonstration_right_dot, UR, buff=0.08)

        eigenvector_identity = MathTex(
            r"A\mathbf{v}=\lambda\mathbf{v},",
            rf"\qquad \lambda={BASE_EIGENVALUE:.2f}\in(0,1)",
        ).scale(0.58).to_edge(DOWN, buff=0.14)
        eigenvector_identity[0].set_color(YELLOW_C)

        self.play(
            GrowArrow(demonstration_left),
            FadeIn(demonstration_left_dot, eigenvector_label),
            run_time=0.9,
        )
        self.play(
            TransformFromCopy(demonstration_left, demonstration_right),
            TransformFromCopy(demonstration_left_dot, demonstration_right_dot),
            FadeIn(image_label),
            Write(eigenvector_identity),
            map_arrow.animate.set_color(YELLOW_C),
            run_time=1.2,
        )
        self.play(map_arrow.animate.set_color(WHITE), run_time=0.35)
        self.wait(0.7)
        self.play(
            FadeOut(
                demonstration_left,
                demonstration_left_dot,
                demonstration_right,
                demonstration_right_dot,
                eigenvector_label,
                image_label,
                eigenvector_identity,
            ),
            run_time=0.8,
        )

        # ------------------------------------------------------------------
        # Select x[0] on the eigenspace and repeatedly apply A.
        # ------------------------------------------------------------------
        current_state = modal_state(0)
        current_left_arrow = state_arrow(current_plane, current_state)
        current_left_dot = indexed_state_dot(
            current_plane, current_state, index=0
        )

        status = MathTex(
            r"\mathbf{x}[0]\in\operatorname{span}\!\left(\begin{bmatrix}2\\1\end{bmatrix}\right)"
        ).scale(0.55).to_edge(DOWN, buff=0.14)
        status.set_color(PINK)

        history_dots = VGroup()

        self.play(
            GrowArrow(current_left_arrow),
            FadeIn(current_left_dot),
            Write(status),
            run_time=1.15,
        )
        self.wait(0.45)

        for k in range(NUMBER_OF_STEPS):
            current_state = modal_state(k)
            following_state = modal_state(k + 1)
            iteration_run_time = (
                EARLY_STEP_RUN_TIME if k < 2 else STEP_RUN_TIME
            )

            next_right_arrow = state_arrow(next_plane, following_state)
            next_right_dot = indexed_state_dot(
                next_plane, following_state, index=k + 1
            )

            mapping_status = MathTex(
                rf"\mathbf{{x}}[{k + 1}]",
                r"=A\mathbf{x}[" + str(k) + r"]",
                rf"={BASE_EIGENVALUE:.2f}\,\mathbf{{x}}[{k}]",
            ).scale(0.56).move_to(status)
            mapping_status[0].set_color(PINK)

            # Apply A: the current vector on the left generates the next one
            # on the right, without leaving the eigenspace.
            self.play(
                TransformFromCopy(current_left_arrow, next_right_arrow),
                TransformFromCopy(current_left_dot, next_right_dot),
                Transform(status, mapping_status),
                map_arrow.animate.set_color(PINK),
                run_time=iteration_run_time,
                rate_func=smooth,
            )
            self.play(map_arrow.animate.set_color(WHITE), run_time=0.20)

            # Preserve the old sample as a faded point.
            old_left_history = current_left_dot.copy()
            old_left_history[0].set_color(BLUE_C)
            old_left_history.set_opacity(0.68)
            history_dots.add(old_left_history)
            self.add(old_left_history)

            # The right-hand next state becomes the current state for the next
            # update.  This is the graphical meaning of the recurrence.
            new_left_arrow = state_arrow(current_plane, following_state)
            new_left_dot = indexed_state_dot(
                current_plane, following_state, index=k + 1
            )

            self.play(
                FadeOut(current_left_arrow, current_left_dot),
                TransformFromCopy(next_right_arrow, new_left_arrow),
                TransformFromCopy(next_right_dot, new_left_dot),
                next_right_dot[0].animate.set_color(BLUE_C),
                next_right_dot[1].animate.set_opacity(0.75),
                FadeOut(next_right_arrow),
                run_time=iteration_run_time,
                rate_func=smooth,
            )

            history_dots.add(next_right_dot)
            current_left_arrow = new_left_arrow
            current_left_dot = new_left_dot
            self.wait(0.10)

        conclusion = MathTex(
            r"\mathbf{x}[k]=\lambda^k\mathbf{x}[0]",
            r"\longrightarrow",
            r"\mathbf{0}",
        ).scale(0.61).move_to(status)
        conclusion[0].set_color(PINK)
        conclusion[2].set_color(YELLOW_C)

        self.play(
            Transform(status, conclusion),
            current_left_arrow.animate.set_color(YELLOW_C),
            current_left_dot[0].animate.set_color(YELLOW_C),
            run_time=1.0,
        )
        self.wait(1.0)

        # ------------------------------------------------------------------
        # Keep the eigenspace and x[0] fixed while varying its eigenvalue.
        # This corresponds to a family A(lambda) sharing this eigenvector.
        # ------------------------------------------------------------------
        self.play(
            FadeOut(current_left_arrow, current_left_dot, history_dots, status),
            run_time=0.8,
        )

        eigenvalue = ValueTracker(BASE_EIGENVALUE)

        def sequence_on_plane(plane, first_index):
            group = VGroup()
            for offset in range(NUMBER_OF_STEPS + 1):
                k = first_index + offset
                state = eigenvalue.get_value() ** k * initial_state
                color = YELLOW_C if k == 0 else PINK
                opacity = max(0.38, 1.0 - 0.07 * k)
                group.add(
                    indexed_state_dot(
                        plane,
                        state,
                        index=k,
                        color=color,
                        opacity=opacity,
                        radius=0.110,
                    )
                )
            return group

        dynamic_current_sequence = always_redraw(
            lambda: sequence_on_plane(current_plane, first_index=0)
        )
        dynamic_next_sequence = always_redraw(
            lambda: sequence_on_plane(next_plane, first_index=1)
        )

        lambda_readout = always_redraw(
            lambda: VGroup(
                MathTex(r"\lambda=").scale(0.58),
                DecimalNumber(
                    eigenvalue.get_value(),
                    num_decimal_places=2,
                ).scale(0.58),
            )
            .arrange(RIGHT, buff=0.04)
            .to_edge(DOWN, buff=0.14)
        )

        comparison_caption = MathTex(
            r"A(\lambda)\mathbf{v}=\lambda\mathbf{v}:",
            r"\quad\text{same eigenspace and same }\mathbf{x}[0]",
        ).scale(0.50)
        comparison_caption.next_to(system_equation, DOWN, buff=0.09)
        comparison_caption[0].set_color(GREEN_C)

        self.play(
            FadeIn(comparison_caption),
            FadeIn(dynamic_current_sequence, dynamic_next_sequence),
            FadeIn(lambda_readout),
            run_time=1.1,
        )
        self.wait(0.5)

        # Smaller positive eigenvalue: faster contraction.
        self.play(
            eigenvalue.animate.set_value(0.40),
            run_time=3.0,
            rate_func=smooth,
        )
        self.wait(0.8)

        # Eigenvalue closer to one: slower contraction.
        self.play(
            eigenvalue.animate.set_value(0.85),
            run_time=3.0,
            rate_func=smooth,
        )
        self.wait(1.5)




