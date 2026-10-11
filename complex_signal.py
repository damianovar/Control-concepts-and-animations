from manim import *
import numpy as np


class BuildingAComplexSignal(ThreeDScene):
    def construct(self):

        # ------------------------------------------------------------
        # Parameters and signals
        # ------------------------------------------------------------
        T_MAX = 8.0
        T_INITIAL = 1.0

        def y1(t):
            return np.exp(-0.18 * t) * np.sin(2.0 * t)

        def y2(t):
            return np.exp(-0.12 * t) * np.cos(3.0 * t)

        # Register an object as screen-fixed without displaying it yet.
        def prepare_fixed(*mobjects):
            self.add_fixed_in_frame_mobjects(*mobjects)
            self.remove(*mobjects)

        # ------------------------------------------------------------
        # Camera
        # ------------------------------------------------------------
        self.set_camera_orientation(
            phi=70 * DEGREES,
            theta=-90 * DEGREES,
            gamma=0,
            zoom=0.95,
        )

        # ------------------------------------------------------------
        # Title
        # ------------------------------------------------------------
        title = Tex("Building a complex-valued signal")
        title.scale(0.68).to_edge(UP, buff=0.12)

        prepare_fixed(title)
        self.play(Write(title), run_time=1.2)

        # ------------------------------------------------------------
        # First real-valued signal
        # ------------------------------------------------------------
        axes1 = Axes(
            x_range=[0, T_MAX, 2],
            y_range=[-1.15, 1.15, 1],
            x_length=8.1,
            y_length=1.45,
            axis_config={
                "include_ticks": False,
                "include_tip": True,
                "stroke_width": 1.5,
            },
        ).shift(UP * 2.25)

        t_label1 = MathTex("t").scale(0.52)
        t_label1.next_to(
            axes1.x_axis.get_end(),
            RIGHT,
            buff=0.06,
        )

        y1_label = MathTex(r"y_1(t)").scale(0.55)
        y1_label.next_to(
            axes1.y_axis.get_end(),
            UP,
            buff=0.05,
        )

        y1_equation = MathTex(
            r"y_1(t)=e^{-0.18t}\sin(2t)"
        ).scale(0.45)

        y1_equation.next_to(
            axes1,
            LEFT,
            buff=0.18,
        )

        graph1 = axes1.plot(
            y1,
            x_range=[0, T_MAX, 0.02],
            color=BLUE_C,
            stroke_width=3.2,
        )

        # Only the axes and their labels are registered initially.
        prepare_fixed(
            axes1,
            t_label1,
            y1_label,
        )

        self.play(
            Create(axes1),
            FadeIn(t_label1, y1_label),
            run_time=1.4,
        )

        # The equation and signal appear only after the axes.
        prepare_fixed(
            y1_equation,
            graph1,
        )

        self.play(
            Write(y1_equation),
            run_time=0.8,
        )

        self.play(
            Create(graph1),
            run_time=2.0,
        )

        # ------------------------------------------------------------
        # Second real-valued signal
        # ------------------------------------------------------------
        axes2 = Axes(
            x_range=[0, T_MAX, 2],
            y_range=[-1.15, 1.15, 1],
            x_length=8.1,
            y_length=1.45,
            axis_config={
                "include_ticks": False,
                "include_tip": True,
                "stroke_width": 1.5,
            },
        ).shift(UP * 0.35)

        t_label2 = MathTex("t").scale(0.52)
        t_label2.next_to(
            axes2.x_axis.get_end(),
            RIGHT,
            buff=0.06,
        )

        y2_label = MathTex(r"y_2(t)").scale(0.55)
        y2_label.next_to(
            axes2.y_axis.get_end(),
            UP,
            buff=0.05,
        )

        y2_equation = MathTex(
            r"y_2(t)=e^{-0.12t}\cos(3t)"
        ).scale(0.45)

        y2_equation.next_to(
            axes2,
            LEFT,
            buff=0.18,
        )

        graph2 = axes2.plot(
            y2,
            x_range=[0, T_MAX, 0.02],
            color=GREEN_C,
            stroke_width=3.2,
        )

        # Again, draw the axes first.
        prepare_fixed(
            axes2,
            t_label2,
            y2_label,
        )

        self.play(
            Create(axes2),
            FadeIn(t_label2, y2_label),
            run_time=1.4,
        )

        # Then draw the equation and signal.
        prepare_fixed(
            y2_equation,
            graph2,
        )

        self.play(
            Write(y2_equation),
            run_time=0.8,
        )

        self.play(
            Create(graph2),
            run_time=2.0,
        )

        # ------------------------------------------------------------
        # Three-dimensional representation
        #
        # Manim coordinates:
        #
        #   x = t
        #   y = y_2(t), with the axis direction reversed
        #   z = y_1(t)
        # ------------------------------------------------------------
        axes3 = ThreeDAxes(
            x_range=[0, T_MAX, 2],
            y_range=[-1.2, 1.2, 1],
            z_range=[-1.2, 1.2, 1],
            x_length=8.1,
            y_length=2.2,
            z_length=2.2,
            axis_config={
                "include_ticks": False,
                "include_tip": True,
                "stroke_width": 1.4,
            },
        ).shift(DOWN * 3.55 + IN * 0.45)

        # Flip the direction of the y_2 axis.
        origin3 = axes3.c2p(0, 0, 0)

        axes3.y_axis.rotate(
            PI,
            axis=OUT,
            about_point=origin3,
        )

        # Convert the mathematical coordinates (t,y_1,y_2)
        # into the displayed Manim coordinates.
        def p3(t, value_y1=0, value_y2=0):
            return axes3.c2p(
                t,
                value_y2,
                value_y1,
            )

        t_label3 = MathTex("t").scale(0.52)
        t_label3.next_to(
            axes3.x_axis.get_end(),
            RIGHT,
            buff=0.06,
        )

        y1_label_3d = MathTex(r"y_1(t)").scale(0.50)
        y1_label_3d.next_to(
            axes3.z_axis.get_end(),
            UP,
            buff=0.04,
        )

        y2_label_3d = MathTex(r"y_2(t)").scale(0.50)
        y2_label_3d.next_to(
            axes3.y_axis.get_end(),
            LEFT,
            buff=0.06,
        )

        self.add_fixed_orientation_mobjects(
            t_label3,
            y1_label_3d,
            y2_label_3d,
        )

        self.play(
            Create(axes3),
            FadeIn(
                t_label3,
                y1_label_3d,
                y2_label_3d,
            ),
            run_time=1.8,
        )

        self.wait(0.5)

        # ------------------------------------------------------------
        # Common time variable
        # ------------------------------------------------------------
        time = ValueTracker(T_INITIAL)

        time_dot1 = always_redraw(
            lambda: Dot(
                axes1.c2p(time.get_value(), 0),
                radius=0.055,
                color=YELLOW,
            )
        )

        time_dot2 = always_redraw(
            lambda: Dot(
                axes2.c2p(time.get_value(), 0),
                radius=0.055,
                color=YELLOW,
            )
        )

        time_dot3 = always_redraw(
            lambda: Dot3D(
                p3(time.get_value()),
                radius=0.055,
                color=YELLOW,
            )
        )

        signal_dot1 = always_redraw(
            lambda: Dot(
                axes1.c2p(
                    time.get_value(),
                    y1(time.get_value()),
                ),
                radius=0.065,
                color=BLUE_C,
            )
        )

        signal_dot2 = always_redraw(
            lambda: Dot(
                axes2.c2p(
                    time.get_value(),
                    y2(time.get_value()),
                ),
                radius=0.065,
                color=GREEN_C,
            )
        )

        projection1 = always_redraw(
            lambda: DashedLine(
                axes1.c2p(
                    time.get_value(),
                    0,
                ),
                axes1.c2p(
                    time.get_value(),
                    y1(time.get_value()),
                ),
                color=YELLOW,
                stroke_width=2,
                dash_length=0.07,
            )
        )

        projection2 = always_redraw(
            lambda: DashedLine(
                axes2.c2p(
                    time.get_value(),
                    0,
                ),
                axes2.c2p(
                    time.get_value(),
                    y2(time.get_value()),
                ),
                color=YELLOW,
                stroke_width=2,
                dash_length=0.07,
            )
        )

        prepare_fixed(
            time_dot1,
            time_dot2,
            signal_dot1,
            signal_dot2,
            projection1,
            projection2,
        )

        # ------------------------------------------------------------
        # Highlight t = 1
        # ------------------------------------------------------------
        time_value_label = MathTex(r"t=1")
        time_value_label.scale(0.52)
        time_value_label.set_color(YELLOW)

        time_value_label.to_corner(
            UR,
            buff=0.35,
        ).shift(DOWN * 0.55)

        prepare_fixed(time_value_label)

        self.play(
            FadeIn(
                time_dot1,
                time_dot2,
                time_dot3,
                time_value_label,
            ),
            run_time=1.0,
        )

        # ------------------------------------------------------------
        # Highlight y_1(1)
        # ------------------------------------------------------------
        y1_value_label = MathTex(
            rf"y_1(1)\approx {y1(T_INITIAL):.2f}"
        ).scale(0.46)

        y1_value_label.set_color(BLUE_C)

        y1_value_label.next_to(
            axes1.c2p(
                T_INITIAL,
                y1(T_INITIAL),
            ),
            RIGHT,
            buff=0.12,
        )

        prepare_fixed(y1_value_label)

        self.play(
            Create(projection1),
            FadeIn(signal_dot1),
            Write(y1_value_label),
            run_time=1.5,
        )

        # ------------------------------------------------------------
        # Highlight y_2(1)
        # ------------------------------------------------------------
        y2_value_label = MathTex(
            rf"y_2(1)\approx {y2(T_INITIAL):.2f}"
        ).scale(0.46)

        y2_value_label.set_color(GREEN_C)

        y2_value_label.next_to(
            axes2.c2p(
                T_INITIAL,
                y2(T_INITIAL),
            ),
            RIGHT,
            buff=0.12,
        )

        prepare_fixed(y2_value_label)

        self.play(
            Create(projection2),
            FadeIn(signal_dot2),
            Write(y2_value_label),
            run_time=1.5,
        )

        # ------------------------------------------------------------
        # Construct the corresponding point in 3D
        # ------------------------------------------------------------
        intermediate_point = p3(
            T_INITIAL,
            y1(T_INITIAL),
            0,
        )

        complex_point = p3(
            T_INITIAL,
            y1(T_INITIAL),
            y2(T_INITIAL),
        )

        y1_projection_3d = DashedLine(
            p3(T_INITIAL),
            intermediate_point,
            color=BLUE_C,
            stroke_width=2.5,
            dash_length=0.08,
        )

        y2_projection_3d = DashedLine(
            intermediate_point,
            complex_point,
            color=GREEN_C,
            stroke_width=2.5,
            dash_length=0.08,
        )

        complex_dot = always_redraw(
            lambda: Dot3D(
                p3(
                    time.get_value(),
                    y1(time.get_value()),
                    y2(time.get_value()),
                ),
                radius=0.075,
                color=PINK,
            )
        )

        self.play(
            Create(y1_projection_3d),
            run_time=1.1,
        )

        self.play(
            Create(y2_projection_3d),
            FadeIn(complex_dot),
            run_time=1.1,
        )

        self.wait(0.7)

        # ------------------------------------------------------------
        # Replace the static projections with moving projections
        # ------------------------------------------------------------
        self.remove(
            y1_projection_3d,
            y2_projection_3d,
        )

        moving_y1_projection_3d = always_redraw(
            lambda: DashedLine(
                p3(time.get_value()),
                p3(
                    time.get_value(),
                    y1(time.get_value()),
                    0,
                ),
                color=BLUE_C,
                stroke_width=2,
                dash_length=0.07,
            )
        )

        moving_y2_projection_3d = always_redraw(
            lambda: DashedLine(
                p3(
                    time.get_value(),
                    y1(time.get_value()),
                    0,
                ),
                p3(
                    time.get_value(),
                    y1(time.get_value()),
                    y2(time.get_value()),
                ),
                color=GREEN_C,
                stroke_width=2,
                dash_length=0.07,
            )
        )

        time_slice = always_redraw(
            lambda: Polygon(
                p3(
                    time.get_value(),
                    -1.05,
                    -1.05,
                ),
                p3(
                    time.get_value(),
                    1.05,
                    -1.05,
                ),
                p3(
                    time.get_value(),
                    1.05,
                    1.05,
                ),
                p3(
                    time.get_value(),
                    -1.05,
                    1.05,
                ),
                color=YELLOW,
                fill_color=YELLOW,
                fill_opacity=0.045,
                stroke_opacity=0.30,
                stroke_width=1.0,
            )
        )

        traced_complex_signal = always_redraw(
            lambda: ParametricFunction(
                lambda tau: p3(
                    tau,
                    y1(tau),
                    y2(tau),
                ),
                t_range=[
                    0,
                    max(time.get_value(), 0.02),
                    0.025,
                ],
                color=PINK,
                stroke_width=4.5,
            )
        )

        self.play(
            FadeOut(
                y1_value_label,
                y2_value_label,
                time_value_label,
            ),
            FadeIn(
                moving_y1_projection_3d,
                moving_y2_projection_3d,
                time_slice,
                traced_complex_signal,
            ),
            run_time=1.0,
        )

        # ------------------------------------------------------------
        # Moving time readout
        # ------------------------------------------------------------
        moving_time_label = always_redraw(
            lambda: VGroup(
                MathTex("t=").scale(0.46),
                DecimalNumber(
                    time.get_value(),
                    num_decimal_places=1,
                ).scale(0.46),
            )
            .arrange(RIGHT, buff=0.04)
            .set_color(YELLOW)
            .to_corner(UR, buff=0.35)
            .shift(DOWN * 0.55)
        )

        prepare_fixed(moving_time_label)

        self.play(
            FadeIn(moving_time_label),
            run_time=0.5,
        )

        # ------------------------------------------------------------
        # Move time and construct the complex signal
        # ------------------------------------------------------------
        self.play(
            time.animate.set_value(T_MAX),
            run_time=12,
            rate_func=linear,
        )

        self.wait(0.8)

        complete_complex_signal = ParametricFunction(
            lambda tau: p3(
                tau,
                y1(tau),
                y2(tau),
            ),
            t_range=[0, T_MAX, 0.025],
            color=PINK,
            stroke_width=4.5,
        )

        self.remove(traced_complex_signal)
        self.add(complete_complex_signal)

        self.play(
            FadeOut(
                time_dot1,
                time_dot2,
                time_dot3,
                signal_dot1,
                signal_dot2,
                projection1,
                projection2,
                moving_y1_projection_3d,
                moving_y2_projection_3d,
                time_slice,
                complex_dot,
                moving_time_label,
            ),
            run_time=1.0,
        )

        # ------------------------------------------------------------
        # Interpret the components as real and imaginary parts
        # ------------------------------------------------------------
        new_y1_label = (
            MathTex(r"\operatorname{Re}\{y(t)\}")
            .scale(0.52)
            .move_to(y1_label)
        )

        new_y2_label = (
            MathTex(r"\operatorname{Im}\{y(t)\}")
            .scale(0.52)
            .move_to(y2_label)
        )

        new_y1_label_3d = (
            MathTex(r"\operatorname{Re}\{y(t)\}")
            .scale(0.46)
            .move_to(y1_label_3d)
        )

        new_y2_label_3d = (
            MathTex(r"\operatorname{Im}\{y(t)\}")
            .scale(0.46)
            .move_to(y2_label_3d)
        )

        self.play(
            Transform(
                y1_label,
                new_y1_label,
            ),
            Transform(
                y2_label,
                new_y2_label,
            ),
            Transform(
                y1_label_3d,
                new_y1_label_3d,
            ),
            Transform(
                y2_label_3d,
                new_y2_label_3d,
            ),
            FadeOut(
                y1_equation,
                y2_equation,
            ),
            run_time=2.0,
        )

        # ------------------------------------------------------------
        # Complex-signal identity
        # ------------------------------------------------------------
        complex_identity = MathTex(
            r"y(t)",
            r"=",
            r"\operatorname{Re}\{y(t)\}",
            r"+\,i\,",
            r"\operatorname{Im}\{y(t)\}",
        ).scale(0.62)

        complex_identity[0].set_color(PINK)
        complex_identity[2].set_color(BLUE_C)
        complex_identity[4].set_color(GREEN_C)

        complex_identity.to_corner(
            DR,
            buff=0.25,
        )

        prepare_fixed(complex_identity)

        self.play(
            Write(complex_identity),
            run_time=2.0,
        )

        # ------------------------------------------------------------
        # Final camera movement
        #
        # theta remains fixed so that the time axis stays horizontal.
        # ------------------------------------------------------------
        self.move_camera(
            phi=58 * DEGREES,
            theta=-90 * DEGREES,
            gamma=0,
            zoom=1.02,
            run_time=3.0,
        )

        self.wait(2)
    

