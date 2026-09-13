"""Animate the graphical solution of a scalar recurrence relation.

The left panel constructs the cobweb diagram for

    y[k+1] = f(y[k]) = 0.12 * (y[k]**3 + y[k]**2 + 2),

while the right panel records the corresponding time series.  The diagonal
y[k+1] = y[k] transfers each newly computed ordinate back to the horizontal
axis, where it becomes the argument used in the next iteration.

Example render command:

    python -m manim -pqh recurrence_relation_cobweb_manim.py RecurrenceRelationCobweb
"""

from manim import *


# ---------------------------------------------------------------------------
# Parameters that are convenient to change between renders
# ---------------------------------------------------------------------------
INITIAL_CONDITION = 2.0
NUMBER_OF_ITERATIONS = 8
STEP_RUN_TIME = 0.72


class RecurrenceRelationCobweb(Scene):
    def construct(self):
        def recurrence_map(y):
            return 0.12 * (y**3 + y**2 + 2)

        values = [INITIAL_CONDITION]
        for _ in range(NUMBER_OF_ITERATIONS):
            values.append(recurrence_map(values[-1]))

        title = Tex("Solving a recurrence relation graphically")
        title.scale(0.70).to_edge(UP, buff=0.14)

        equation = MathTex(
            r"y[k+1]=f(y[k]),",
            r"\qquad",
            r"f(y)=0.12\left(y^3+y^2+2\right)",
        ).scale(0.58)
        equation.next_to(title, DOWN, buff=0.10)
        equation[0].set_color(PINK)
        equation[2].set_color(BLUE_C)

        common_plane_style = {
            "background_line_style": {
                "stroke_color": GREY_B,
                "stroke_width": 1,
                "stroke_opacity": 0.28,
            },
            "axis_config": {
                "stroke_width": 1.8,
                "include_tip": True,
                "tip_width": 0.15,
                "tip_height": 0.15,
            },
        }

        recurrence_plane = NumberPlane(
            x_range=[-3, 2.2, 1],
            y_range=[-2.2, 2.2, 1],
            x_length=5.55,
            y_length=4.65,
            **common_plane_style,
        )

        trajectory_plane = NumberPlane(
            x_range=[0, NUMBER_OF_ITERATIONS + 1, 1],
            y_range=[-2.2, 2.2, 1],
            x_length=5.55,
            y_length=4.65,
            **common_plane_style,
        )

        planes = VGroup(recurrence_plane, trajectory_plane)
        planes.arrange(RIGHT, buff=0.85).shift(DOWN * 0.38)

        recurrence_plane.add_coordinates()
        trajectory_plane.add_coordinates()

        recurrence_axis_labels = recurrence_plane.get_axis_labels(
            MathTex(r"y[k]").scale(0.55),
            MathTex(r"y[k+1]").scale(0.55),
        )
        trajectory_axis_labels = trajectory_plane.get_axis_labels(
            MathTex(r"k").scale(0.55),
            MathTex(r"y[k]").scale(0.55),
        )

        recurrence_panel_title = Tex("recurrence map").scale(0.48)
        recurrence_panel_title.next_to(recurrence_plane, UP, buff=0.08)

        trajectory_panel_title = Tex("generated trajectory").scale(0.48)
        trajectory_panel_title.next_to(trajectory_plane, UP, buff=0.08)

        map_curve = recurrence_plane.plot(
            recurrence_map,
            x_range=[-3, 2, 0.025],
            color=BLUE_C,
            stroke_width=4,
            use_smoothing=True,
        )

        identity_line = recurrence_plane.plot(
            lambda y: y,
            x_range=[-2.2, 2, 0.025],
            color=GREY_A,
            stroke_width=2.2,
        ).set_stroke(opacity=0.85)
        identity_line = DashedVMobject(identity_line, num_dashes=42)

        map_label = MathTex(r"y^{+}=f(y)").scale(0.46).set_color(BLUE_C)
        map_label.move_to(recurrence_plane.c2p(-1.85, 1.70))

        identity_label = MathTex(r"y^{+}=y").scale(0.43).set_color(GREY_A)
        identity_label.move_to(recurrence_plane.c2p(1.42, 1.72))

        readout = MathTex(
            rf"y[0]={values[0]:.3f}"
        ).scale(0.61).to_edge(DOWN, buff=0.16)
        readout.set_color(PINK)

        self.play(Write(title), Write(equation), run_time=1.25)
        self.play(
            Create(recurrence_plane),
            Create(trajectory_plane),
            FadeIn(recurrence_axis_labels, trajectory_axis_labels),
            FadeIn(recurrence_panel_title, trajectory_panel_title),
            run_time=1.7,
        )
        self.play(
            Create(map_curve),
            Create(identity_line),
            FadeIn(map_label, identity_label),
            run_time=1.6,
        )

        # Initial condition on the horizontal axis of the recurrence panel.
        horizontal_marker = Dot(
            recurrence_plane.c2p(values[0], 0),
            radius=0.065,
            color=PINK,
        )
        cobweb_cursor = horizontal_marker.copy()

        # The same initial condition becomes the first time-series sample.
        first_stem = Line(
            trajectory_plane.c2p(0, 0),
            trajectory_plane.c2p(0, values[0]),
            color=GREY_B,
            stroke_width=1.6,
        )
        current_series_dot = Dot(
            trajectory_plane.c2p(0, values[0]),
            radius=0.070,
            color=PINK,
        )

        current_input_label = MathTex(r"y[0]").scale(0.46)
        current_input_label.next_to(horizontal_marker, DOWN, buff=0.10)
        current_input_label.set_color(PINK)

        self.play(
            FadeIn(horizontal_marker, cobweb_cursor),
            FadeIn(current_input_label),
            Create(first_stem),
            FadeIn(current_series_dot),
            FadeIn(readout),
            run_time=1.2,
        )
        self.wait(0.5)

        for k in range(NUMBER_OF_ITERATIONS):
            current_value = values[k]
            next_value = values[k + 1]

            # At the first iteration the construction starts on the horizontal
            # axis.  Later iterations start from the identity line.
            starting_height = 0 if k == 0 else current_value

            evaluation_segment = Line(
                recurrence_plane.c2p(current_value, starting_height),
                recurrence_plane.c2p(current_value, next_value),
                color=PINK,
                stroke_width=3.1,
            )

            transfer_segment = Line(
                recurrence_plane.c2p(current_value, next_value),
                recurrence_plane.c2p(next_value, next_value),
                color=PINK,
                stroke_width=3.1,
            )

            curve_point = recurrence_plane.c2p(current_value, next_value)
            diagonal_point = recurrence_plane.c2p(next_value, next_value)

            next_readout = MathTex(
                rf"y[{k + 1}]=f\!\left(y[{k}]\right)={next_value:.3f}"
            ).scale(0.61)
            next_readout.move_to(readout).set_color(PINK)

            # First evaluate f(y[k]): move vertically to the recurrence curve.
            self.play(
                Create(evaluation_segment),
                cobweb_cursor.animate.move_to(curve_point),
                Transform(readout, next_readout),
                run_time=STEP_RUN_TIME,
                rate_func=smooth,
            )

            # Then transfer y[k+1] to the next horizontal coordinate using the
            # identity line.  Simultaneously record it in the right panel.
            new_stem = Line(
                trajectory_plane.c2p(k + 1, 0),
                trajectory_plane.c2p(k + 1, next_value),
                color=GREY_B,
                stroke_width=1.6,
            )
            series_connector = Line(
                trajectory_plane.c2p(k, current_value),
                trajectory_plane.c2p(k + 1, next_value),
                color=BLUE_C,
                stroke_width=2.7,
            )
            new_series_dot = Dot(
                trajectory_plane.c2p(k + 1, next_value),
                radius=0.070,
                color=PINK,
            )
            next_input_label = MathTex(rf"y[{k + 1}]").scale(0.46)
            next_input_label.next_to(
                recurrence_plane.c2p(next_value, 0),
                DOWN,
                buff=0.10,
            ).set_color(PINK)

            self.play(
                Create(transfer_segment),
                cobweb_cursor.animate.move_to(diagonal_point),
                horizontal_marker.animate.move_to(
                    recurrence_plane.c2p(next_value, 0)
                ),
                Transform(current_input_label, next_input_label),
                current_series_dot.animate.set_color(BLUE_C),
                Create(series_connector),
                Create(new_stem),
                FadeIn(new_series_dot),
                run_time=STEP_RUN_TIME,
                rate_func=smooth,
            )

            current_series_dot = new_series_dot
            self.wait(0.12)

        fixed_point = values[-1]
        conclusion = MathTex(
            rf"y[k]\longrightarrow y^\star\approx {fixed_point:.3f},",
            r"\qquad f(y^\star)=y^\star",
        ).scale(0.59)
        conclusion.move_to(readout)
        conclusion[0].set_color(PINK)
        conclusion[1].set_color(GREY_A)

        self.play(
            Transform(readout, conclusion),
            cobweb_cursor.animate.set_color(YELLOW_C),
            current_series_dot.animate.set_color(YELLOW_C),
            FadeOut(current_input_label),
            run_time=1.1,
        )
        self.wait(2.0)
