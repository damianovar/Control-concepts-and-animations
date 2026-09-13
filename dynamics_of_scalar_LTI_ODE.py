"""Fixed-view geometric animation of why y_dot = a y is exponential.

The y--y_dot plane is kept as an ordinary two-dimensional Cartesian plane:
y is always horizontal and y_dot is always vertical. Time is represented by
a fixed oblique axis pointing out of that plane toward the viewer. No camera
rotation is used.

High-quality render:

    python -m manim -pqh scalar_ode_exponential_geometry_manim.py ScalarODEExponentialGeometry
"""

from manim import *
import numpy as np


A = -0.70
INITIAL_VALUE = 2.50
FINAL_TIME = 6.00
MOTION_RUN_TIME = 13.0
VELOCITY_ARROW_SCALE = 0.50

Y_MIN = -2.80
Y_MAX = 3.20
YDOT_MIN = -2.40
YDOT_MAX = 2.20


class ScalarODEExponentialGeometry(Scene):
    def construct(self):
        def solution(t):
            return INITIAL_VALUE * np.exp(A * t)

        def derivative(t):
            return A * solution(t)

        # Fixed oblique projection: y stays horizontal and y_dot vertical.
        # The diagonal direction represents time coming out of the page.
        origin = LEFT * 0.35 + UP * 0.72
        y_unit = 0.86 * RIGHT
        derivative_unit = 0.86 * UP
        time_unit = 0.22 * LEFT + 0.35 * DOWN

        def point(y=0.0, y_dot=0.0, t=0.0):
            return origin + y * y_unit + y_dot * derivative_unit + t * time_unit

        title = Tex("When the rate of change is proportional to the state")
        title.scale(0.66).to_edge(UP, buff=0.13)

        proportionality_message = MathTex(
            r"\dot y=ay,",
            rf"\qquad a={A:.2f}<0",
        ).scale(0.56)
        proportionality_message.to_corner(UL, buff=0.28).shift(DOWN * 0.62)
        proportionality_message[0].set_color(GREEN_C)

        # Light grid for the initial conventional two-dimensional plot.
        base_grid = VGroup()
        for y_value in np.arange(np.ceil(Y_MIN), np.floor(Y_MAX) + 1):
            base_grid.add(
                Line(
                    point(y_value, YDOT_MIN),
                    point(y_value, YDOT_MAX),
                    color=GREY_D,
                    stroke_width=1,
                ).set_opacity(0.25)
            )
        for derivative_value in np.arange(
            np.ceil(YDOT_MIN), np.floor(YDOT_MAX) + 1
        ):
            base_grid.add(
                Line(
                    point(Y_MIN, derivative_value),
                    point(Y_MAX, derivative_value),
                    color=GREY_D,
                    stroke_width=1,
                ).set_opacity(0.25)
            )

        y_axis = Arrow(
            point(Y_MIN, 0),
            point(Y_MAX, 0),
            buff=0,
            color=WHITE,
            stroke_width=2.2,
            max_tip_length_to_length_ratio=0.025,
        )
        derivative_axis = Arrow(
            point(0, YDOT_MIN),
            point(0, YDOT_MAX),
            buff=0,
            color=WHITE,
            stroke_width=2.2,
            max_tip_length_to_length_ratio=0.035,
        )

        y_label = MathTex(r"y").scale(0.58)
        y_label.next_to(y_axis.get_end(), RIGHT, buff=0.04)
        derivative_label = MathTex(r"\dot y").scale(0.58)
        derivative_label.next_to(derivative_axis.get_end(), UP, buff=0.04)

        # The ODE line spans the whole visible plane, including quadrant II.
        ode_graph = Line(
            point(Y_MIN, A * Y_MIN),
            point(Y_MAX, A * Y_MAX),
            color=GREEN_C,
            stroke_width=4.2,
        )
        ode_graph_label = MathTex(
            rf"\dot y={A:.2f}y"
        ).scale(0.48).set_color(GREEN_C)
        ode_graph_label.next_to(
            point(-1.90, A * (-1.90)),
            UL,
            buff=0.08,
        )

        time_axis = Arrow(
            point(0, 0, 0),
            point(0, 0, FINAL_TIME + 0.35),
            buff=0,
            color=WHITE,
            stroke_width=2.3,
            max_tip_length_to_length_ratio=0.065,
        )
        time_label = MathTex(r"t").scale(0.55)
        time_label.next_to(time_axis.get_end(), DL, buff=0.05)

        time_ticks = VGroup()
        tick_direction = 0.055 * (UP + RIGHT)
        for tick_time in range(1, int(FINAL_TIME) + 1):
            tick_center = point(0, 0, tick_time)
            time_ticks.add(
                Line(
                    tick_center - tick_direction,
                    tick_center + tick_direction,
                    color=GREY_B,
                    stroke_width=1.3,
                )
            )

        time = ValueTracker(0.0)

        # The violet state trajectory is the only curve lifted along time.
        state_trace = always_redraw(
            lambda: ParametricFunction(
                lambda t: point(solution(t), 0, t),
                t_range=[0, max(0.002, time.get_value()), 0.025],
                color=PINK,
                stroke_width=5.0,
            )
        )
        state_point = always_redraw(
            lambda: Dot(
                point(solution(time.get_value()), 0, time.get_value()),
                radius=0.075,
                color=PINK,
            )
        )

        # Moving markers in the original y--y_dot plane.
        base_state_point = always_redraw(
            lambda: Dot(
                point(solution(time.get_value()), 0, 0),
                radius=0.045,
                color=PINK,
            )
        )
        base_graph_point = always_redraw(
            lambda: Dot(
                point(solution(time.get_value()), derivative(time.get_value()), 0),
                radius=0.045,
                color=GREEN_C,
            )
        )
        derivative_axis_point = always_redraw(
            lambda: Dot(
                point(0, derivative(time.get_value()), 0),
                radius=0.045,
                color=ORANGE,
            )
        )

        state_to_time_axis = always_redraw(
            lambda: DashedLine(
                point(solution(time.get_value()), 0, time.get_value()),
                point(0, 0, time.get_value()),
                color=GREY_B,
                stroke_width=1.8,
                dash_length=0.10,
            ).set_stroke(opacity=0.60)
        )
        state_to_base = always_redraw(
            lambda: DashedLine(
                point(
                    solution(time.get_value()),
                    0,
                    max(0.001, time.get_value()),
                ),
                point(solution(time.get_value()), 0, 0),
                color=PINK,
                stroke_width=1.9,
                dash_length=0.10,
            ).set_stroke(opacity=0.48)
        )
        base_state_to_graph = always_redraw(
            lambda: DashedLine(
                point(solution(time.get_value()), 0, 0),
                point(solution(time.get_value()), derivative(time.get_value()), 0),
                color=GREEN_C,
                stroke_width=2.0,
                dash_length=0.10,
            ).set_stroke(opacity=0.70)
        )

        # Dashed horizontal read-off from the ODE graph to the y_dot axis.
        graph_to_derivative_axis = always_redraw(
            lambda: DashedLine(
                point(solution(time.get_value()), derivative(time.get_value()), 0),
                point(0, derivative(time.get_value()), 0),
                color=ORANGE,
                stroke_width=2.1,
                dash_length=0.10,
            ).set_stroke(opacity=0.76)
        )

        velocity_arrow = always_redraw(
            lambda: Arrow(
                start=point(solution(time.get_value()), 0, 0),
                end=point(
                    solution(time.get_value())
                    + VELOCITY_ARROW_SCALE * derivative(time.get_value()),
                    0,
                    0,
                ),
                buff=0,
                color=YELLOW_C,
                stroke_width=5,
                max_tip_length_to_length_ratio=0.22,
            )
        )
        velocity_label = MathTex(r"\text{velocity}").scale(0.40)
        velocity_label.set_color(YELLOW_C)
        velocity_label.add_updater(
            lambda label: label.next_to(
                point(
                    solution(time.get_value())
                    + 0.5 * VELOCITY_ARROW_SCALE * derivative(time.get_value()),
                    0,
                    0,
                ),
                UP,
                buff=0.06,
            )
        )

        time_readout = VGroup(
            MathTex(r"t=").scale(0.50),
            DecimalNumber(0, num_decimal_places=1).scale(0.50),
        ).arrange(RIGHT, buff=0.04)
        time_readout.to_corner(UR, buff=0.30).shift(DOWN * 0.62)
        time_readout[1].add_updater(
            lambda number: number.set_value(time.get_value())
        )

        legend = VGroup(
            VGroup(
                Line(LEFT * 0.20, RIGHT * 0.20, color=PINK, stroke_width=5),
                MathTex(r"y(t)").scale(0.43),
            ).arrange(RIGHT, buff=0.08),
            VGroup(
                Dot(radius=0.055, color=ORANGE),
                MathTex(r"\dot y(t)").scale(0.43),
            ).arrange(RIGHT, buff=0.08),
        ).arrange(RIGHT, buff=0.34)
        legend.to_corner(UR, buff=0.30).shift(DOWN * 1.18)

        final_formula = MathTex(
            r"y(t)=y(0)e^{at}",
            rf"={INITIAL_VALUE:.1f}e^{{{A:.2f}t}}",
        ).scale(0.62).to_edge(DOWN, buff=0.14)
        final_formula[0].set_color(PINK)

        self.play(FadeIn(title), run_time=0.7)

        # First present a completely standard two-dimensional ODE graph.
        self.play(Create(base_grid), run_time=0.8)
        self.play(Create(y_axis), FadeIn(y_label), run_time=1.0)
        self.play(Create(derivative_axis), FadeIn(derivative_label), run_time=1.0)
        self.play(
            Create(ode_graph),
            FadeIn(ode_graph_label),
            Write(proportionality_message),
            run_time=1.6,
        )
        self.wait(0.6)

        # Add time without moving or rotating the original axes.
        self.play(
            GrowArrow(time_axis),
            Create(time_ticks),
            FadeIn(time_label),
            run_time=1.5,
        )

        # Establish the chain y -> ODE graph -> y_dot axis.
        self.play(
            FadeIn(
                state_point,
                base_state_point,
                base_graph_point,
                derivative_axis_point,
            ),
            Create(state_to_time_axis),
            Create(base_state_to_graph),
            Create(graph_to_derivative_axis),
            FadeIn(velocity_arrow, velocity_label),
            run_time=1.5,
        )

        self.add(state_trace, state_to_base)
        self.play(FadeIn(time_readout, legend), run_time=0.8)
        self.wait(0.7)

        self.play(
            time.animate.set_value(FINAL_TIME),
            run_time=MOTION_RUN_TIME,
            rate_func=linear,
        )

        self.play(Write(final_formula), run_time=1.3)
        self.wait(2.0)



