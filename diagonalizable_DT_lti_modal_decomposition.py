"""Animate modal decomposition for a diagonalizable 2D autonomous LTI system.

The system is

    x[k+1] = A x[k]

with two linearly independent real eigenvectors

    v1 = [2, 1]^T,      lambda1 = 0.72,
    v2 = [1, 3]^T,      lambda2 = 0.40.

The initial condition is chosen as

    x[0] = v1 + 0.5 v2 = [2.5, 2.5]^T.

Each animation step decomposes x[k], maps the two modal components
independently, adds them to obtain x[k+1], and transfers the result back to
the current-state plane.  Because lambda2 < lambda1, the second mode decays
faster and the trajectory progressively aligns with span(v1).

High-quality render:

    python -m manim -pqh diagonalizable_lti_modal_decomposition_manim.py DiagonalizableLTIModalDecomposition
"""

from manim import *
import numpy as np


# ---------------------------------------------------------------------------
# Parameters that are convenient to change between renders
# ---------------------------------------------------------------------------
LAMBDA_1 = 0.72
LAMBDA_2 = 0.40
COEFFICIENT_1 = 1.00
COEFFICIENT_2 = 0.50
NUMBER_OF_STEPS = 5

EARLY_DECOMPOSITION_RUN_TIME = 1.45
EARLY_MAPPING_RUN_TIME = 1.30
EARLY_SUM_RUN_TIME = 1.15
EARLY_TRANSFER_RUN_TIME = 1.35
LATER_STEP_RUN_TIME = 0.52

MODE_1_COLOR = GREEN_C
MODE_2_COLOR = ORANGE
STATE_COLOR = PINK
HISTORY_COLOR = BLUE_C


class DiagonalizableLTIModalDecomposition(Scene):
    def construct(self):
        v1 = np.array([2.0, 1.0])
        v2 = np.array([1.0, 3.0])

        def component_1(k):
            return COEFFICIENT_1 * LAMBDA_1**k * v1

        def component_2(k):
            return COEFFICIENT_2 * LAMBDA_2**k * v2

        def state(k):
            return component_1(k) + component_2(k)

        # This is the concrete matrix associated with the selected eigenpairs:
        # A = [[ 0.784, -0.128],
        #      [ 0.192,  0.336]].

        # ------------------------------------------------------------------
        # Opening assumption: the two eigenvectors form a basis of R^2.
        # ------------------------------------------------------------------
        assumption_title = Tex(
            "Assumption: $A$ is diagonalizable over $\\mathbb{R}$"
        ).scale(0.78).to_edge(UP, buff=0.55)

        eigenpair_statement = MathTex(
            r"A\mathbf{v}_1=\lambda_1\mathbf{v}_1,",
            r"\qquad",
            r"A\mathbf{v}_2=\lambda_2\mathbf{v}_2",
        ).scale(0.72)
        eigenpair_statement[0].set_color(MODE_1_COLOR)
        eigenpair_statement[2].set_color(MODE_2_COLOR)

        real_eigenvalues_statement = MathTex(
            r"\lambda_1,\lambda_2\in\mathbb{R}"
        ).scale(0.68)
        real_eigenvalues_statement.next_to(
            eigenpair_statement, DOWN, buff=0.28
        )

        basis_statement = MathTex(
            r"\mathbf{v}_1,\mathbf{v}_2",
            r"\text{ are linearly independent}",
        ).scale(0.68)
        basis_statement.next_to(real_eigenvalues_statement, DOWN, buff=0.32)
        basis_statement[0].set_color(YELLOW_C)

        decomposition_statement = MathTex(
            r"\Longrightarrow",
            r"\quad",
            r"\mathbf{x}[0]=c_1\mathbf{v}_1+c_2\mathbf{v}_2",
        ).scale(0.78)
        decomposition_statement.next_to(basis_statement, DOWN, buff=0.38)
        decomposition_statement[2].set_color(STATE_COLOR)

        assumption_group = VGroup(
            assumption_title,
            eigenpair_statement,
            real_eigenvalues_statement,
            basis_statement,
            decomposition_statement,
        )

        self.play(Write(assumption_title), run_time=1.0)
        self.play(Write(eigenpair_statement), run_time=1.2)
        self.play(Write(real_eigenvalues_statement), run_time=0.8)
        self.play(Write(basis_statement), run_time=1.0)
        self.play(Write(decomposition_statement), run_time=1.1)
        self.wait(1.3)
        self.play(FadeOut(assumption_group), run_time=0.9)

        # ------------------------------------------------------------------
        # Two copies of the same state space: current and next state.
        # ------------------------------------------------------------------
        title = Tex("Free evolution as a superposition of modes")
        title.scale(0.70).to_edge(UP, buff=0.12)

        system_equation = MathTex(
            r"\mathbf{x}[k+1]=A\mathbf{x}[k]"
        ).scale(0.60)
        system_equation.next_to(title, DOWN, buff=0.08)

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
        planes.arrange(RIGHT, buff=1.65).shift(DOWN * 0.65)

        def axis_labels(plane, use_pluses=False):
            if use_pluses:
                horizontal = r"x_1^{+}"
                vertical = r"x_2^{+}"
            else:
                horizontal = r"x_1"
                vertical = r"x_2"

            return VGroup(
                MathTex(horizontal).scale(0.50).next_to(
                    plane.x_axis.get_end(), RIGHT, buff=0.03
                ),
                MathTex(vertical).scale(0.50).next_to(
                    plane.y_axis.get_end(), UP, buff=0.03
                ),
            )

        current_axis_labels = axis_labels(current_plane)
        next_axis_labels = axis_labels(next_plane, use_pluses=True)

        current_title = MathTex(r"\mathbf{x}[k]").scale(0.55)
        current_title.next_to(current_plane, UP, buff=0.25)
        current_title.align_to(current_plane, LEFT).shift(RIGHT * 0.20)

        next_title = MathTex(r"\mathbf{x}[k+1]").scale(0.55)
        next_title.next_to(next_plane, UP, buff=0.25)
        next_title.align_to(next_plane, LEFT).shift(RIGHT * 0.20)

        map_center = 0.5 * (
            current_plane.get_right() + next_plane.get_left()
        )
        map_arrow = Arrow(
            map_center + LEFT * 0.38,
            map_center + RIGHT * 0.38,
            buff=0.08,
            color=WHITE,
            stroke_width=3,
            max_tip_length_to_length_ratio=0.18,
        )
        map_label = MathTex(r"A").scale(0.64)
        map_label.next_to(map_arrow, UP, buff=0.06)

        mode_legend = VGroup(
            VGroup(
                Line(LEFT * 0.20, RIGHT * 0.20, color=MODE_1_COLOR, stroke_width=4),
                MathTex(
                    rf"\mathbf{{v}}_1=\begin{{bmatrix}}2\\1\end{{bmatrix}},\ "
                    rf"\lambda_1={LAMBDA_1:.2f}"
                ).scale(0.42),
            ).arrange(RIGHT, buff=0.09),
            VGroup(
                Line(LEFT * 0.20, RIGHT * 0.20, color=MODE_2_COLOR, stroke_width=4),
                MathTex(
                    rf"\mathbf{{v}}_2=\begin{{bmatrix}}1\\3\end{{bmatrix}},\ "
                    rf"\lambda_2={LAMBDA_2:.2f}"
                ).scale(0.42),
            ).arrange(RIGHT, buff=0.09),
        ).arrange(RIGHT, buff=0.55)
        mode_legend.next_to(system_equation, DOWN, buff=0.07)

        def eigenspace_1(plane):
            return DashedLine(
                plane.c2p(-3.5, -1.75),
                plane.c2p(3.5, 1.75),
                color=MODE_1_COLOR,
                stroke_width=2.8,
                dash_length=0.14,
            )

        def eigenspace_2(plane):
            return DashedLine(
                plane.c2p(-3.5 / 3.0, -3.5),
                plane.c2p(3.5 / 3.0, 3.5),
                color=MODE_2_COLOR,
                stroke_width=2.8,
                dash_length=0.14,
            )

        current_mode_1_line = eigenspace_1(current_plane)
        next_mode_1_line = eigenspace_1(next_plane)
        current_mode_2_line = eigenspace_2(current_plane)
        next_mode_2_line = eigenspace_2(next_plane)

        def vector_arrow(plane, start, end, color, opacity=1.0, width=4.0):
            arrow = Arrow(
                plane.c2p(start[0], start[1]),
                plane.c2p(end[0], end[1]),
                buff=0,
                color=color,
                stroke_width=width,
                max_tip_length_to_length_ratio=0.13,
            )
            arrow.set_opacity(opacity)
            return arrow

        def indexed_state_dot(
            plane,
            point,
            index,
            color=STATE_COLOR,
            opacity=1.0,
            radius=0.115,
        ):
            circle = Dot(
                plane.c2p(point[0], point[1]),
                radius=radius,
                color=color,
            )
            label = Text(str(index), font_size=15, color=BLACK)
            label.move_to(circle)
            marker = VGroup(circle, label)
            marker.set_opacity(opacity)
            return marker

        def parallelogram_lines(plane, first_component, second_component, total):
            return VGroup(
                DashedLine(
                    plane.c2p(first_component[0], first_component[1]),
                    plane.c2p(total[0], total[1]),
                    color=MODE_2_COLOR,
                    stroke_width=2.0,
                    dash_length=0.10,
                ),
                DashedLine(
                    plane.c2p(second_component[0], second_component[1]),
                    plane.c2p(total[0], total[1]),
                    color=MODE_1_COLOR,
                    stroke_width=2.0,
                    dash_length=0.10,
                ),
            )

        self.play(Write(title), Write(system_equation), run_time=1.1)
        self.play(
            Create(current_plane),
            Create(next_plane),
            FadeIn(current_axis_labels, next_axis_labels),
            FadeIn(current_title, next_title),
            GrowArrow(map_arrow),
            FadeIn(map_label),
            run_time=1.7,
        )

        # Introduce each eigenspace first on the left and then on the right.
        self.play(
            Create(current_mode_1_line),
            FadeIn(mode_legend[0]),
            run_time=1.0,
        )
        self.play(
            TransformFromCopy(current_mode_1_line, next_mode_1_line),
            run_time=0.9,
        )
        self.play(
            Create(current_mode_2_line),
            FadeIn(mode_legend[1]),
            run_time=1.0,
        )
        self.play(
            TransformFromCopy(current_mode_2_line, next_mode_2_line),
            run_time=0.9,
        )

        # ------------------------------------------------------------------
        # Initial condition and repeated modal updates.
        # ------------------------------------------------------------------
        initial_state = state(0)
        current_state_arrow = vector_arrow(
            current_plane,
            np.zeros(2),
            initial_state,
            STATE_COLOR,
            width=4.8,
        )
        current_state_dot = indexed_state_dot(current_plane, initial_state, 0)

        initial_status = MathTex(
            r"\mathbf{x}[0]",
            r"=\mathbf{v}_1+\frac{1}{2}\mathbf{v}_2",
            r"=\begin{bmatrix}2.5\\2.5\end{bmatrix}",
        ).scale(0.52).to_edge(DOWN, buff=0.11)
        initial_status[0].set_color(STATE_COLOR)

        self.play(
            GrowArrow(current_state_arrow),
            FadeIn(current_state_dot),
            Write(initial_status),
            run_time=1.2,
        )
        self.wait(0.7)

        status = initial_status
        history_dots = VGroup()

        for k in range(NUMBER_OF_STEPS):
            first = component_1(k)
            second = component_2(k)
            total = state(k)
            next_first = component_1(k + 1)
            next_second = component_2(k + 1)
            next_total = state(k + 1)

            early_iteration = k < 2
            decomposition_run_time = (
                EARLY_DECOMPOSITION_RUN_TIME
                if early_iteration
                else LATER_STEP_RUN_TIME
            )
            mapping_run_time = (
                EARLY_MAPPING_RUN_TIME
                if early_iteration
                else LATER_STEP_RUN_TIME
            )
            sum_run_time = (
                EARLY_SUM_RUN_TIME
                if early_iteration
                else LATER_STEP_RUN_TIME
            )
            transfer_run_time = (
                EARLY_TRANSFER_RUN_TIME
                if early_iteration
                else LATER_STEP_RUN_TIME
            )

            left_first_arrow = vector_arrow(
                current_plane, np.zeros(2), first, MODE_1_COLOR
            )
            left_second_arrow = vector_arrow(
                current_plane, np.zeros(2), second, MODE_2_COLOR
            )
            left_parallelogram = parallelogram_lines(
                current_plane, first, second, total
            )

            decomposition_status = MathTex(
                rf"\mathbf{{x}}[{k}]",
                rf"={LAMBDA_1:.2f}^{{{k}}}\mathbf{{v}}_1",
                rf"+\frac{{1}}{{2}}{LAMBDA_2:.2f}^{{{k}}}\mathbf{{v}}_2",
            ).scale(0.51).move_to(status)
            decomposition_status[0].set_color(STATE_COLOR)
            decomposition_status[1].set_color(MODE_1_COLOR)
            decomposition_status[2].set_color(MODE_2_COLOR)

            self.play(
                current_state_arrow.animate.set_opacity(0.24),
                Create(left_first_arrow),
                Create(left_second_arrow),
                Create(left_parallelogram),
                Transform(status, decomposition_status),
                run_time=decomposition_run_time,
            )

            # Map the first modal component independently.
            right_first_arrow = vector_arrow(
                next_plane, np.zeros(2), next_first, MODE_1_COLOR
            )
            first_mapping_status = MathTex(
                r"A\!left(c_1\lambda_1^k\mathbf{v}_1\right)",
                r"=c_1\lambda_1^{k+1}\mathbf{v}_1",
            ).scale(0.51).move_to(status)
            first_mapping_status.set_color(MODE_1_COLOR)

            self.play(
                TransformFromCopy(left_first_arrow, right_first_arrow),
                Transform(status, first_mapping_status),
                map_arrow.animate.set_color(MODE_1_COLOR),
                run_time=mapping_run_time,
            )
            self.play(map_arrow.animate.set_color(WHITE), run_time=0.18)

            # Map the second modal component independently.
            right_second_arrow = vector_arrow(
                next_plane, np.zeros(2), next_second, MODE_2_COLOR
            )
            second_mapping_status = MathTex(
                r"A\!\left(c_2\lambda_2^k\mathbf{v}_2\right)",
                r"=c_2\lambda_2^{k+1}\mathbf{v}_2",
            ).scale(0.51).move_to(status)
            second_mapping_status.set_color(MODE_2_COLOR)

            self.play(
                TransformFromCopy(left_second_arrow, right_second_arrow),
                Transform(status, second_mapping_status),
                map_arrow.animate.set_color(MODE_2_COLOR),
                run_time=mapping_run_time,
            )
            self.play(map_arrow.animate.set_color(WHITE), run_time=0.18)

            # Superpose the mapped components in the next-state plane.
            right_parallelogram = parallelogram_lines(
                next_plane, next_first, next_second, next_total
            )
            next_state_arrow = vector_arrow(
                next_plane,
                np.zeros(2),
                next_total,
                STATE_COLOR,
                width=4.8,
            )
            next_state_dot = indexed_state_dot(
                next_plane, next_total, index=k + 1
            )

            sum_status = MathTex(
                rf"\mathbf{{x}}[{k + 1}]",
                r"=c_1\lambda_1^{k+1}\mathbf{v}_1",
                r"+c_2\lambda_2^{k+1}\mathbf{v}_2",
            ).scale(0.51).move_to(status)
            sum_status[0].set_color(STATE_COLOR)
            sum_status[1].set_color(MODE_1_COLOR)
            sum_status[2].set_color(MODE_2_COLOR)

            self.play(
                Create(right_parallelogram),
                GrowArrow(next_state_arrow),
                FadeIn(next_state_dot),
                Transform(status, sum_status),
                run_time=sum_run_time,
            )

            # Preserve x[k] as a faded indexed sample.
            old_left_dot = current_state_dot.copy()
            old_left_dot[0].set_color(HISTORY_COLOR)
            old_left_dot.set_opacity(0.68)
            history_dots.add(old_left_dot)
            self.add(old_left_dot)

            # The sum on the right becomes the next current state on the left.
            new_current_arrow = vector_arrow(
                current_plane,
                np.zeros(2),
                next_total,
                STATE_COLOR,
                width=4.8,
            )
            new_current_dot = indexed_state_dot(
                current_plane, next_total, index=k + 1
            )

            self.play(
                FadeOut(
                    current_state_arrow,
                    current_state_dot,
                    left_first_arrow,
                    left_second_arrow,
                    left_parallelogram,
                ),
                TransformFromCopy(next_state_arrow, new_current_arrow),
                TransformFromCopy(next_state_dot, new_current_dot),
                next_state_dot[0].animate.set_color(HISTORY_COLOR),
                next_state_dot[1].animate.set_opacity(0.75),
                FadeOut(
                    right_first_arrow,
                    right_second_arrow,
                    right_parallelogram,
                    next_state_arrow,
                ),
                run_time=transfer_run_time,
            )

            history_dots.add(next_state_dot)
            current_state_arrow = new_current_arrow
            current_state_dot = new_current_dot
            self.wait(0.10 if k > 0 else 0.35)

        # ------------------------------------------------------------------
        # The slower-decaying mode determines the asymptotic direction.
        # ------------------------------------------------------------------
        conclusion = MathTex(
            rf"{LAMBDA_2:.2f}^k\text{{ decays faster than }}{LAMBDA_1:.2f}^k",
            r"\quad\Longrightarrow\quad",
            r"\mathbf{x}[k]\text{ aligns with }\mathbf{v}_1",
        ).scale(0.50).move_to(status)
        conclusion[0].set_color(MODE_2_COLOR)
        conclusion[2].set_color(MODE_1_COLOR)

        self.play(
            Transform(status, conclusion),
            current_mode_2_line.animate.set_opacity(0.22),
            next_mode_2_line.animate.set_opacity(0.22),
            current_mode_1_line.animate.set_stroke(width=4.0),
            next_mode_1_line.animate.set_stroke(width=4.0),
            current_state_arrow.animate.set_color(YELLOW_C),
            current_state_dot[0].animate.set_color(YELLOW_C),
            run_time=1.3,
        )
        self.wait(1.5)

        # ------------------------------------------------------------------
        # Vary only lambda_2 while keeping lambda_1, both eigenspaces, and
        # x[0] fixed.  Light connecting segments expose the changing shape of
        # the discrete trajectory without representing continuous motion.
        # ------------------------------------------------------------------
        self.play(
            FadeOut(
                current_state_arrow,
                current_state_dot,
                history_dots,
                status,
                mode_legend,
            ),
            current_mode_1_line.animate.set_stroke(width=2.8, opacity=1.0),
            next_mode_1_line.animate.set_stroke(width=2.8, opacity=1.0),
            current_mode_2_line.animate.set_stroke(width=2.8, opacity=1.0),
            next_mode_2_line.animate.set_stroke(width=2.8, opacity=1.0),
            run_time=0.9,
        )

        lambda_2_tracker = ValueTracker(LAMBDA_2)
        comparison_steps = 4

        def state_with_variable_lambda_2(k):
            return (
                COEFFICIENT_1 * LAMBDA_1**k * v1
                + COEFFICIENT_2 * lambda_2_tracker.get_value() ** k * v2
            )

        def indexed_trajectory(plane, first_index, last_index):
            samples = [
                state_with_variable_lambda_2(k)
                for k in range(first_index, last_index + 1)
            ]

            connecting_segments = VGroup()
            for first_sample, second_sample in zip(samples[:-1], samples[1:]):
                segment = Line(
                    plane.c2p(first_sample[0], first_sample[1]),
                    plane.c2p(second_sample[0], second_sample[1]),
                    color=STATE_COLOR,
                    stroke_width=2.2,
                ).set_opacity(0.55)
                connecting_segments.add(segment)

            markers = VGroup()
            for offset, sample in enumerate(samples):
                k = first_index + offset
                marker_color = YELLOW_C if k == 0 else STATE_COLOR
                markers.add(
                    indexed_state_dot(
                        plane,
                        sample,
                        index=k,
                        color=marker_color,
                        radius=0.105,
                    )
                )

            return VGroup(connecting_segments, markers)

        current_dynamic_trajectory = always_redraw(
            lambda: indexed_trajectory(
                current_plane,
                first_index=0,
                last_index=comparison_steps,
            )
        )
        next_dynamic_trajectory = always_redraw(
            lambda: indexed_trajectory(
                next_plane,
                first_index=1,
                last_index=comparison_steps + 1,
            )
        )

        comparison_caption = MathTex(
            rf"\lambda_1={LAMBDA_1:.2f}\text{{ fixed}},",
            r"\qquad",
            r"\lambda_2\text{ varies},",
            r"\qquad",
            r"\mathbf{x}[0]\text{ fixed}",
        ).scale(0.45)
        comparison_caption.next_to(system_equation, DOWN, buff=0.07)
        comparison_caption[0].set_color(MODE_1_COLOR)
        comparison_caption[2].set_color(MODE_2_COLOR)
        comparison_caption[4].set_color(STATE_COLOR)

        lambda_2_number = DecimalNumber(
            LAMBDA_2,
            num_decimal_places=2,
            color=MODE_2_COLOR,
        ).scale(0.58)
        lambda_2_number.add_updater(
            lambda number: number.set_value(lambda_2_tracker.get_value())
        )
        lambda_2_readout = VGroup(
            MathTex(r"\lambda_2=").scale(0.58).set_color(MODE_2_COLOR),
            lambda_2_number,
        ).arrange(RIGHT, buff=0.04).to_edge(DOWN, buff=0.11)

        self.play(
            FadeIn(comparison_caption),
            FadeIn(current_dynamic_trajectory, next_dynamic_trajectory),
            FadeIn(lambda_2_readout),
            run_time=1.1,
        )
        self.wait(0.7)

        # A smaller lambda_2 makes the second mode disappear more quickly,
        # producing a sharper turn toward the first eigenspace.
        self.play(
            lambda_2_tracker.animate.set_value(0.18),
            run_time=3.2,
            rate_func=smooth,
        )
        self.wait(0.9)

        # Bringing lambda_2 closer to lambda_1 makes the relative modal
        # weighting change more slowly and the trajectory less curved.
        self.play(
            lambda_2_tracker.animate.set_value(0.62),
            run_time=3.2,
            rate_func=smooth,
        )
        self.wait(1.8)




