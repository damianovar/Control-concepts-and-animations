from manim import *
import numpy as np


class IntegratingAComplexSignal(ThreeDScene):
    def construct(self):

        # ============================================================
        # PARAMETERS
        # ============================================================
        T_MAX = 6.0
        T_SAMPLE = 1.0

        # Two-sided decaying signals, so that the integrals over R exist.
        def real_part(t):
            return np.exp(-0.22 * t**2) * np.cos(1.3 * t)

        def imag_part(t):
            return (
                0.8
                * np.exp(-0.28 * (t - 0.8) ** 2)
                * np.cos(t + 0.2)
            )

        # Register screen-fixed objects without showing them prematurely.
        def prepare_fixed(*mobjects):
            self.add_fixed_in_frame_mobjects(*mobjects)
            self.remove(*mobjects)

        # ============================================================
        # NUMERICAL CUMULATIVE INTEGRALS
        # ============================================================
        integration_grid = np.linspace(-T_MAX, T_MAX, 5001)

        real_samples = real_part(integration_grid)
        imag_samples = imag_part(integration_grid)

        integration_steps = np.diff(integration_grid)

        cumulative_real = np.concatenate(
            [
                [0.0],
                np.cumsum(
                    0.5
                    * (real_samples[:-1] + real_samples[1:])
                    * integration_steps
                ),
            ]
        )

        cumulative_imag = np.concatenate(
            [
                [0.0],
                np.cumsum(
                    0.5
                    * (imag_samples[:-1] + imag_samples[1:])
                    * integration_steps
                ),
            ]
        )

        def integral_real(upper_limit):
            return np.interp(
                upper_limit,
                integration_grid,
                cumulative_real,
            )

        def integral_imag(upper_limit):
            return np.interp(
                upper_limit,
                integration_grid,
                cumulative_imag,
            )

        final_real = cumulative_real[-1]
        final_imag = cumulative_imag[-1]

        # ============================================================
        # CAMERA
        # ============================================================
        self.set_camera_orientation(
            phi=70 * DEGREES,
            theta=-90 * DEGREES,
            gamma=0,
            zoom=0.95,
        )

        # ============================================================
        # TITLE
        # ============================================================
        title = Tex("Building a complex-valued signal")
        title.scale(0.68).to_edge(UP, buff=0.12)

        prepare_fixed(title)

        self.play(
            Write(title),
            run_time=1.2,
        )

        # ============================================================
        # FIRST PANEL: REAL COMPONENT
        # ============================================================
        axes_real = Axes(
            x_range=[-T_MAX, T_MAX, 2],
            y_range=[-1.15, 1.15, 1],
            x_length=8.1,
            y_length=1.45,
            axis_config={
                "include_ticks": False,
                "include_tip": True,
                "stroke_width": 1.5,
            },
        ).shift(UP * 2.25)

        real_t_label = MathTex("t").scale(0.52)
        real_t_label.next_to(
            axes_real.x_axis.get_end(),
            RIGHT,
            buff=0.06,
        )

        real_axis_label = MathTex(r"y_1(t)").scale(0.55)
        real_axis_label.next_to(
            axes_real.y_axis.get_end(),
            UP,
            buff=0.05,
        )

        real_equation = MathTex(
            r"y_1(t)=e^{-0.22t^2}\cos(1.3t)"
        ).scale(0.50)

        real_equation.next_to(
            axes_real,
            LEFT,
            buff=0.15,
        )

        real_graph = axes_real.plot(
            real_part,
            x_range=[-T_MAX, T_MAX, 0.02],
            color=BLUE_C,
            stroke_width=3.2,
        )

        prepare_fixed(
            axes_real,
            real_t_label,
            real_axis_label,
        )

        self.play(
            Create(axes_real),
            FadeIn(
                real_t_label,
                real_axis_label,
            ),
            run_time=1.4,
        )

        prepare_fixed(
            real_equation,
            real_graph,
        )

        self.play(
            Write(real_equation),
            run_time=0.8,
        )

        self.play(
            Create(real_graph),
            run_time=2.2,
        )

        # ============================================================
        # SECOND PANEL: IMAGINARY COMPONENT
        # ============================================================
        axes_imag = Axes(
            x_range=[-T_MAX, T_MAX, 2],
            y_range=[-1.15, 1.15, 1],
            x_length=8.1,
            y_length=1.45,
            axis_config={
                "include_ticks": False,
                "include_tip": True,
                "stroke_width": 1.5,
            },
        ).shift(UP * 0.35)

        imag_t_label = MathTex("t").scale(0.52)
        imag_t_label.next_to(
            axes_imag.x_axis.get_end(),
            RIGHT,
            buff=0.06,
        )

        imag_axis_label = MathTex(r"y_2(t)").scale(0.55)
        imag_axis_label.next_to(
            axes_imag.y_axis.get_end(),
            UP,
            buff=0.05,
        )

        imag_equation = MathTex(
            r"y_2(t)=0.8e^{-0.28(t-0.8)^2}\cos(t+0.2)"
        ).scale(0.48)

        imag_equation.next_to(
            axes_imag,
            LEFT,
            buff=0.15,
        )

        imag_graph = axes_imag.plot(
            imag_part,
            x_range=[-T_MAX, T_MAX, 0.02],
            color=GREEN_C,
            stroke_width=3.2,
        )

        prepare_fixed(
            axes_imag,
            imag_t_label,
            imag_axis_label,
        )

        self.play(
            Create(axes_imag),
            FadeIn(
                imag_t_label,
                imag_axis_label,
            ),
            run_time=1.4,
        )

        prepare_fixed(
            imag_equation,
            imag_graph,
        )

        self.play(
            Write(imag_equation),
            run_time=0.8,
        )

        self.play(
            Create(imag_graph),
            run_time=2.2,
        )

        # ============================================================
        # THIRD PANEL: COMPLEX SIGNAL IN 3D
        #
        # Manim coordinates:
        #
        #   x = t
        #   y = y_2(t), depth direction
        #   z = y_1(t), vertical direction
        # ============================================================
        axes_complex_3d = ThreeDAxes(
            x_range=[-T_MAX, T_MAX, 2],
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

        # Flip the y_2 axis and slant only this axis slightly.  The t and y_1
        # axes remain untouched.  The custom p3 mapping below uses this same
        # slanted direction, keeping the curve geometrically consistent with
        # the displayed axes.
        origin_3d = axes_complex_3d.c2p(0, 0, 0)

        axes_complex_3d.y_axis.rotate(
            PI,
            axis=OUT,
            about_point=origin_3d,
        )

        axes_complex_3d.y_axis.rotate(
            16 * DEGREES,
            axis=OUT,
            about_point=origin_3d,
        )

        time_unit_vector = (
            axes_complex_3d.c2p(1, 0, 0) - origin_3d
        )
        real_unit_vector = (
            axes_complex_3d.c2p(0, 0, 1) - origin_3d
        )
        imag_unit_vector = (
            axes_complex_3d.y_axis.get_end() - origin_3d
        ) / 1.2

        # Convert (t, Re, Im) into scene coordinates, using the independently
        # slanted direction for the imaginary component.
        def p3(t, value_real=0, value_imag=0):
            return (
                origin_3d
                + t * time_unit_vector
                + value_real * real_unit_vector
                + value_imag * imag_unit_vector
            )

        complex_t_label = MathTex("t").scale(0.52)
        complex_t_label.next_to(
            axes_complex_3d.x_axis.get_end(),
            RIGHT,
            buff=0.06,
        )

        complex_real_label = MathTex(r"y_1(t)").scale(0.48)
        complex_real_label.next_to(
            axes_complex_3d.z_axis.get_end(),
            UP,
            buff=0.04,
        )

        complex_imag_label = MathTex(r"y_2(t)").scale(0.48)
        complex_imag_label.next_to(
            axes_complex_3d.y_axis.get_end(),
            LEFT,
            buff=0.06,
        )

        self.add_fixed_orientation_mobjects(
            complex_t_label,
            complex_real_label,
            complex_imag_label,
        )

        self.play(
            Create(axes_complex_3d),
            FadeIn(
                complex_t_label,
                complex_real_label,
                complex_imag_label,
            ),
            run_time=1.8,
        )

        # ============================================================
        # SHOW ONE VALUE OF t
        # ============================================================
        sample_real_value = real_part(T_SAMPLE)
        sample_imag_value = imag_part(T_SAMPLE)

        real_sample_line = DashedLine(
            axes_real.c2p(T_SAMPLE, 0),
            axes_real.c2p(T_SAMPLE, sample_real_value),
            color=YELLOW,
            stroke_width=2,
            dash_length=0.07,
        )

        imag_sample_line = DashedLine(
            axes_imag.c2p(T_SAMPLE, 0),
            axes_imag.c2p(T_SAMPLE, sample_imag_value),
            color=YELLOW,
            stroke_width=2,
            dash_length=0.07,
        )

        real_sample_dot = Dot(
            axes_real.c2p(T_SAMPLE, sample_real_value),
            radius=0.065,
            color=BLUE_C,
        )

        imag_sample_dot = Dot(
            axes_imag.c2p(T_SAMPLE, sample_imag_value),
            radius=0.065,
            color=GREEN_C,
        )

        prepare_fixed(
            real_sample_line,
            imag_sample_line,
            real_sample_dot,
            imag_sample_dot,
        )

        sample_time_label = MathTex(r"t=1")
        sample_time_label.scale(0.50)
        sample_time_label.set_color(YELLOW)
        sample_time_label.to_corner(UR, buff=0.35).shift(DOWN * 0.55)

        prepare_fixed(sample_time_label)

        self.play(
            FadeIn(sample_time_label),
            Create(real_sample_line),
            FadeIn(real_sample_dot),
            run_time=1.3,
        )

        self.play(
            Create(imag_sample_line),
            FadeIn(imag_sample_dot),
            run_time=1.3,
        )

        intermediate_3d_point = p3(
            T_SAMPLE,
            sample_real_value,
            0,
        )

        final_3d_point = p3(
            T_SAMPLE,
            sample_real_value,
            sample_imag_value,
        )

        real_projection_3d = DashedLine(
            p3(T_SAMPLE),
            intermediate_3d_point,
            color=BLUE_C,
            stroke_width=2.5,
            dash_length=0.08,
        )

        imag_projection_3d = DashedLine(
            intermediate_3d_point,
            final_3d_point,
            color=GREEN_C,
            stroke_width=2.5,
            dash_length=0.08,
        )

        complex_sample_dot = Dot3D(
            final_3d_point,
            radius=0.075,
            color=PINK,
        )

        self.play(
            Create(real_projection_3d),
            run_time=1.1,
        )

        self.play(
            Create(imag_projection_3d),
            FadeIn(complex_sample_dot),
            run_time=1.1,
        )

        self.wait(0.6)

        # ============================================================
        # CONSTRUCT THE COMPLETE COMPLEX SIGNAL
        # ============================================================
        self.play(
            FadeOut(
                sample_time_label,
                real_sample_line,
                imag_sample_line,
                real_sample_dot,
                imag_sample_dot,
                real_projection_3d,
                imag_projection_3d,
                complex_sample_dot,
            ),
            run_time=0.8,
        )

        signal_time = ValueTracker(-T_MAX + 0.02)

        moving_real_dot = always_redraw(
            lambda: Dot(
                axes_real.c2p(
                    signal_time.get_value(),
                    real_part(signal_time.get_value()),
                ),
                radius=0.055,
                color=BLUE_C,
            )
        )

        moving_imag_dot = always_redraw(
            lambda: Dot(
                axes_imag.c2p(
                    signal_time.get_value(),
                    imag_part(signal_time.get_value()),
                ),
                radius=0.055,
                color=GREEN_C,
            )
        )

        moving_complex_dot = always_redraw(
            lambda: Dot3D(
                p3(
                    signal_time.get_value(),
                    real_part(signal_time.get_value()),
                    imag_part(signal_time.get_value()),
                ),
                radius=0.07,
                color=PINK,
            )
        )

        common_time_cursor = always_redraw(
            lambda: DashedLine(
                axes_real.c2p(
                    signal_time.get_value(),
                    1.08,
                ),
                axes_imag.c2p(
                    signal_time.get_value(),
                    -1.08,
                ),
                color=YELLOW,
                stroke_width=1.7,
                dash_length=0.08,
            )
        )

        partial_complex_curve = always_redraw(
            lambda: ParametricFunction(
                lambda tau: p3(
                    tau,
                    real_part(tau),
                    imag_part(tau),
                ),
                t_range=[
                    -T_MAX,
                    max(signal_time.get_value(), -T_MAX + 0.02),
                    0.025,
                ],
                color=PINK,
                stroke_width=4.5,
            )
        )

        prepare_fixed(
            moving_real_dot,
            moving_imag_dot,
            common_time_cursor,
        )

        self.play(
            FadeIn(
                moving_real_dot,
                moving_imag_dot,
                moving_complex_dot,
                common_time_cursor,
                partial_complex_curve,
            ),
            run_time=0.6,
        )

        self.play(
            signal_time.animate.set_value(T_MAX),
            run_time=10,
            rate_func=linear,
        )

        complete_complex_curve = ParametricFunction(
            lambda tau: p3(
                tau,
                real_part(tau),
                imag_part(tau),
            ),
            t_range=[-T_MAX, T_MAX, 0.025],
            color=PINK,
            stroke_width=4.5,
        )

        self.remove(partial_complex_curve)
        self.add(complete_complex_curve)

        self.play(
            FadeOut(
                moving_real_dot,
                moving_imag_dot,
                moving_complex_dot,
                common_time_cursor,
            ),
            run_time=0.8,
        )

        # ============================================================
        # RELABEL COMPONENTS AS REAL AND IMAGINARY PARTS
        # ============================================================
        new_real_axis_label = (
            MathTex(r"\operatorname{Re}\!\left\{s(t)\right\}")
            .scale(0.50)
            .move_to(real_axis_label)
        )

        new_imag_axis_label = (
            MathTex(r"\operatorname{Im}\!\left\{s(t)\right\}")
            .scale(0.50)
            .move_to(imag_axis_label)
        )

        new_complex_real_label = (
            MathTex(r"\operatorname{Re}\!\left\{s(t)\right\}")
            .scale(0.44)
            .move_to(complex_real_label)
        )

        new_complex_imag_label = (
            MathTex(r"\operatorname{Im}\!\left\{s(t)\right\}")
            .scale(0.44)
            .move_to(complex_imag_label)
        )

        complex_signal_identity = MathTex(
            r"s(t)",
            r"=",
            r"\operatorname{Re}\{s(t)\}",
            r"+i",
            r"\operatorname{Im}\{s(t)\}",
        ).scale(0.58)

        complex_signal_identity[0].set_color(PINK)
        complex_signal_identity[2].set_color(BLUE_C)
        complex_signal_identity[4].set_color(GREEN_C)

        complex_signal_identity.to_corner(
            DR,
            buff=0.25,
        )

        # Register the replacement labels directly in their final camera
        # modes.  Transforming a fixed-orientation MathTex object can leave
        # newly introduced glyphs with a 3D orientation, making individual
        # characters appear flattened or disappear.
        prepare_fixed(
            new_real_axis_label,
            new_imag_axis_label,
            complex_signal_identity,
        )
        self.add_fixed_orientation_mobjects(
            new_complex_real_label,
            new_complex_imag_label,
        )
        self.remove(
            new_complex_real_label,
            new_complex_imag_label,
        )

        self.play(
            FadeOut(
                real_axis_label,
                imag_axis_label,
                complex_real_label,
                complex_imag_label,
            ),
            FadeIn(
                new_real_axis_label,
                new_imag_axis_label,
                new_complex_real_label,
                new_complex_imag_label,
            ),
            FadeOut(
                real_equation,
                imag_equation,
            ),
            Write(complex_signal_identity),
            run_time=2.2,
        )

        self.wait(1)

        # ============================================================
        # TRANSITION TO INTEGRATION
        # ============================================================
        integration_title = Tex(
            "Integrating a complex-valued signal"
        ).scale(0.68)

        integration_title.move_to(title)
        prepare_fixed(integration_title)

        partial_integral_formula = MathTex(
            r"S(T)=\int_{-\infty}^{T}s(\tau)\,d\tau"
        ).scale(0.54)

        partial_integral_formula.to_corner(
            UR,
            buff=0.25,
        ).shift(DOWN * 0.55)

        prepare_fixed(partial_integral_formula)

        self.play(
            FadeOut(title),
            FadeIn(integration_title),
            FadeOut(complex_signal_identity),
            Write(partial_integral_formula),
            run_time=1.8,
        )

        # Fade the 3D panel away to make room for the accumulator.
        self.play(
            FadeOut(
                axes_complex_3d,
                complex_t_label,
                new_complex_real_label,
                new_complex_imag_label,
                complete_complex_curve,
            ),
            run_time=1.5,
        )

        # ============================================================
        # COMPLEX ACCUMULATOR PLANE
        # ============================================================
        accumulator_axes = Axes(
            x_range=[-1.2, 1.4, 0.5],
            y_range=[-1.2, 1.4, 0.5],
            x_length=3.8,
            y_length=2.8,
            axis_config={
                "include_ticks": False,
                "include_tip": True,
                "stroke_width": 1.5,
            },
        ).shift(LEFT * 1.55 + DOWN * 2.45)

        accumulator_real_label = MathTex(
            r"\operatorname{Re}\{S(T)\}"
        ).scale(0.43)

        accumulator_real_label.next_to(
            accumulator_axes.x_axis.get_end(),
            RIGHT,
            buff=0.04,
        )

        accumulator_imag_label = MathTex(
            r"\operatorname{Im}\{S(T)\}"
        ).scale(0.43)

        accumulator_imag_label.next_to(
            accumulator_axes.y_axis.get_end(),
            UP,
            buff=0.04,
        )

        accumulator_title = Tex(
            "complex accumulator"
        ).scale(0.46)

        accumulator_title.next_to(
            accumulator_axes,
            UP,
            buff=0.38,
        ).shift(LEFT * 1.20)

        prepare_fixed(
            accumulator_axes,
            accumulator_real_label,
            accumulator_imag_label,
            accumulator_title,
        )

        self.play(
            Create(accumulator_axes),
            FadeIn(
                accumulator_real_label,
                accumulator_imag_label,
                accumulator_title,
            ),
            run_time=1.5,
        )

        # ============================================================
        # MOVING UPPER INTEGRATION LIMIT
        # ============================================================
        upper_limit = ValueTracker(-T_MAX + 0.02)

        real_area = always_redraw(
            lambda: axes_real.get_area(
                real_graph,
                x_range=[
                    -T_MAX,
                    max(
                        upper_limit.get_value(),
                        -T_MAX + 0.02,
                    ),
                ],
                color=BLUE_C,
                opacity=0.28,
            )
        )

        imag_area = always_redraw(
            lambda: axes_imag.get_area(
                imag_graph,
                x_range=[
                    -T_MAX,
                    max(
                        upper_limit.get_value(),
                        -T_MAX + 0.02,
                    ),
                ],
                color=GREEN_C,
                opacity=0.28,
            )
        )

        integration_cursor = always_redraw(
            lambda: DashedLine(
                axes_real.c2p(
                    upper_limit.get_value(),
                    1.08,
                ),
                axes_imag.c2p(
                    upper_limit.get_value(),
                    -1.08,
                ),
                color=YELLOW,
                stroke_width=2.0,
                dash_length=0.08,
            )
        )

        upper_limit_label = always_redraw(
            lambda: MathTex("T")
            .scale(0.48)
            .set_color(YELLOW)
            .next_to(
                axes_real.c2p(
                    upper_limit.get_value(),
                    1.08,
                ),
                UP,
                buff=0.04,
            )
        )

        prepare_fixed(
            real_area,
            imag_area,
            integration_cursor,
            upper_limit_label,
        )

        # ============================================================
        # COMPLEX ACCUMULATOR COMPONENTS
        # ============================================================
        real_integral_line = always_redraw(
            lambda: Line(
                accumulator_axes.c2p(0, 0),
                accumulator_axes.c2p(
                    integral_real(upper_limit.get_value()),
                    0,
                ),
                color=BLUE_C,
                stroke_width=5,
            )
        )

        imag_integral_line = always_redraw(
            lambda: Line(
                accumulator_axes.c2p(
                    integral_real(upper_limit.get_value()),
                    0,
                ),
                accumulator_axes.c2p(
                    integral_real(upper_limit.get_value()),
                    integral_imag(upper_limit.get_value()),
                ),
                color=GREEN_C,
                stroke_width=5,
            )
        )

        resultant_integral_line = always_redraw(
            lambda: Line(
                accumulator_axes.c2p(0, 0),
                accumulator_axes.c2p(
                    integral_real(upper_limit.get_value()),
                    integral_imag(upper_limit.get_value()),
                ),
                color=PINK,
                stroke_width=6,
            )
        )

        accumulator_dot = always_redraw(
            lambda: Dot(
                accumulator_axes.c2p(
                    integral_real(upper_limit.get_value()),
                    integral_imag(upper_limit.get_value()),
                ),
                radius=0.07,
                color=PINK,
            )
        )

        accumulator_trail = TracedPath(
            accumulator_dot.get_center,
            stroke_color=PINK,
            stroke_width=2.5,
            stroke_opacity=0.45,
        )

        # ============================================================
        # NUMERICAL READOUT
        # ============================================================
        integral_readout = always_redraw(
            lambda: VGroup(
                VGroup(
                    MathTex(r"A_{\mathrm{R}}(T)=")
                    .scale(0.44)
                    .set_color(BLUE_C),
                    DecimalNumber(
                        integral_real(upper_limit.get_value()),
                        num_decimal_places=2,
                        include_sign=True,
                    )
                    .scale(0.44)
                    .set_color(BLUE_C),
                ).arrange(RIGHT, buff=0.06),
                VGroup(
                    MathTex(r"A_{\mathrm{I}}(T)=")
                    .scale(0.44)
                    .set_color(GREEN_C),
                    DecimalNumber(
                        integral_imag(upper_limit.get_value()),
                        num_decimal_places=2,
                        include_sign=True,
                    )
                    .scale(0.44)
                    .set_color(GREEN_C),
                ).arrange(RIGHT, buff=0.06),
            )
            .arrange(
                DOWN,
                aligned_edge=LEFT,
                buff=0.15,
            )
            .to_corner(DR, buff=0.55)
            .shift(UP * 1.15)
        )

        prepare_fixed(
            real_integral_line,
            imag_integral_line,
            resultant_integral_line,
            accumulator_dot,
            accumulator_trail,
            integral_readout,
        )

        signed_area_label = Tex(
            "signed areas accumulated up to $T$"
        ).scale(0.43)

        signed_area_label.to_edge(
            RIGHT,
            buff=0.35,
        ).shift(DOWN * 0.65)

        prepare_fixed(signed_area_label)

        # These objects are rebuilt continuously by always_redraw (and the
        # trail grows while the scene runs).  Applying FadeIn to them can make
        # their submobject families change during interpolation, which causes
        # recent Manim versions to raise a zip-length ValueError.  Add the
        # dynamic objects directly and animate only the static caption.
        self.add(
            real_area,
            imag_area,
            integration_cursor,
            upper_limit_label,
            accumulator_trail,
            real_integral_line,
            imag_integral_line,
            resultant_integral_line,
            accumulator_dot,
            integral_readout,
        )

        self.play(
            FadeIn(signed_area_label),
            run_time=1.2,
        )

        # ============================================================
        # SWEEP FROM -INFINITY TO +INFINITY
        # ============================================================
        self.play(
            upper_limit.animate.set_value(T_MAX),
            run_time=14,
            rate_func=linear,
        )

        self.wait(1)

        # ============================================================
        # FINAL CONVERGED COMPLEX NUMBER
        # ============================================================
        exact_integral = MathTex(
            r"\int_{-\infty}^{+\infty}s(t)\,dt",
            r"=",
            r"\int_{-\infty}^{+\infty}"
            r"\operatorname{Re}\{s(t)\}\,dt",
            r"+i",
            r"\int_{-\infty}^{+\infty}"
            r"\operatorname{Im}\{s(t)\}\,dt",
        ).scale(0.43)

        exact_integral[0].set_color(PINK)
        exact_integral[2].set_color(BLUE_C)
        exact_integral[4].set_color(GREEN_C)

        exact_integral.to_edge(
            RIGHT,
            buff=0.30,
        ).shift(DOWN * 1.55)

        numerical_integral = MathTex(
            rf"\approx {final_real:.2f}"
            rf"{final_imag:+.2f}i"
        ).scale(0.62)

        numerical_integral.set_color(PINK)

        numerical_integral.next_to(
            exact_integral,
            DOWN,
            buff=0.22,
        )

        convergence_label = Tex(
            "the accumulator converges to one complex number"
        ).scale(0.43)

        convergence_label.set_color(PINK)

        convergence_label.next_to(
            numerical_integral,
            DOWN,
            buff=0.18,
        )

        prepare_fixed(
            exact_integral,
            numerical_integral,
            convergence_label,
        )

        # For the same reason, do not FadeOut always_redraw objects.  Removing
        # them directly is visually unobtrusive here because the final formula
        # appears at the same moment.
        self.remove(
            integral_readout,
            upper_limit_label,
        )

        self.play(
            FadeOut(
                partial_integral_formula,
                signed_area_label,
            ),
            Write(exact_integral),
            run_time=2.5,
        )

        self.play(
            Write(numerical_integral),
            FadeIn(convergence_label),
            run_time=1.5,
        )

        self.wait(3)


