"""Animate sinusoidal fidelity as a sliding, rotating weighted helix.

The impulse-response family is selected near the beginning of construct().
Three choices are provided: a first-order exponential, an underdamped
second-order response matched to the input frequency, and an underdamped
response oscillating substantially faster than the input.

and the causal input exp(j*omega*t) H(t).  At the current convolution
time t0, the convolution integrand is

    h(t0-t) exp(j*omega*t)
      = exp(j*omega*t0) [h(s) exp(-j*omega*s)],  s=t0-t.

Because the input starts at t=0, the overlap initially grows and produces
a transient.  Once the impulse-response tail has effectively entered the
overlap, the weighted helix approaches a fixed shape undergoing only rigid
complex-plane rotation.  The exact transient response is

    y(t0) = exp(j*omega*t0) integral_0^t0 h(s) exp(-j*omega*s) ds,

and it approaches H(j*omega) exp(j*omega*t0).
"""

from manim import *
import numpy as np


class SinusoidalFidelity(ThreeDScene):
    def construct(self):
        omega = 1.20

        # ------------------------------------------------------------
        # Select exactly one impulse response by commenting/uncommenting.
        # ------------------------------------------------------------
#         IMPULSE_RESPONSE = "first_order_exponential"
#         IMPULSE_RESPONSE = "underdamped_matched"
        IMPULSE_RESPONSE = "underdamped_faster"

        if IMPULSE_RESPONSE == "first_order_exponential":
            decay = 0.55
            omega_d = None
            impulse_case_tex = r"h(t_0-t):\ \mathrm{first\ order}"
        elif IMPULSE_RESPONSE == "underdamped_matched":
            decay = 0.32
            omega_d = omega
            impulse_case_tex = r"h(t_0-t):\ \omega_d=\omega"
        elif IMPULSE_RESPONSE == "underdamped_faster":
            decay = 0.32
            omega_d = 2.5 * omega
            impulse_case_tex = r"h(t_0-t):\ \omega_d=2.5\omega"
        else:
            raise ValueError(f"Unknown impulse response: {IMPULSE_RESPONSE}")

        def impulse_response(s):
            """Causal impulse-response value for s>=0."""
            envelope = np.exp(-decay * s)
            if IMPULSE_RESPONSE == "first_order_exponential":
                return envelope
            return envelope * np.sin(omega_d * s)

        def integral_of_exponential(q, upper_limit):
            return (1.0 - np.exp(-q * upper_limit)) / q

        def truncated_frequency_response(t0):
            """Integral from 0 to t0 of h(s) exp(-j*omega*s) ds."""
            if t0 <= 0:
                return 0j
            if IMPULSE_RESPONSE == "first_order_exponential":
                return integral_of_exponential(decay + 1j * omega, t0)

            q_minus = decay + 1j * (omega - omega_d)
            q_plus = decay + 1j * (omega + omega_d)
            return (
                integral_of_exponential(q_minus, t0)
                - integral_of_exponential(q_plus, t0)
            ) / (2j)

        if IMPULSE_RESPONSE == "first_order_exponential":
            frequency_response = 1.0 / (decay + 1j * omega)
        else:
            frequency_response = omega_d / (
                (decay + 1j * omega) ** 2 + omega_d**2
            )

        time_axis_min = -7.0
        time_axis_max = 19.0
        transient_end = 7.0
        initial_time = -5.5
        final_time = 18.0

        self.set_camera_orientation(
            phi=68 * DEGREES,
            theta=-56 * DEGREES,
            zoom=0.88,
        )

        axes = ThreeDAxes(
            x_range=[time_axis_min, time_axis_max, 4],
            y_range=[-1.25, 1.25, 1],
            z_range=[-1.25, 1.25, 1],
            x_length=11.6,
            y_length=3.15,
            z_length=3.15,
            axis_config={
                "stroke_width": 1.4,
                "include_ticks": False,
            },
        ).shift(LEFT * 0.65 + DOWN * 0.35)

        time_axis_label = MathTex(r"t").scale(0.65)
        time_axis_label.next_to(axes.x_axis.get_end(), RIGHT, buff=0.08)
        re_label = MathTex(r"\Re").scale(0.60)
        re_label.next_to(axes.y_axis.get_end(), UP, buff=0.08)
        im_label = MathTex(r"\Im").scale(0.60)
        im_label.next_to(axes.z_axis.get_end(), UP, buff=0.08)

        # The causal sinusoidal input is explicitly drawn as zero before
        # t=0, rather than merely omitting its negative-time portion.
        input_zero = Line(
            axes.c2p(time_axis_min, 0, 0),
            axes.c2p(0, 0, 0),
            color=BLUE_C,
            stroke_width=3.2,
        )

        # Graphical jump connector at t=0.  This is the conventional visual
        # representation of the discontinuity from 0 to exp(j*omega*0)=1.
        input_jump = Line(
            axes.c2p(0, 0, 0),
            axes.c2p(0, 1, 0),
            color=BLUE_C,
            stroke_width=3.2,
        )

        input_helix = ParametricFunction(
            lambda t: axes.c2p(
                t,
                np.cos(omega * t),
                np.sin(omega * t),
            ),
            t_range=[0, time_axis_max - 0.5, 0.035],
            color=BLUE_C,
            stroke_width=3.2,
        )

        time = ValueTracker(initial_time)

        # A translucent cross-section marks the current convolution time t0.
        moving_section = always_redraw(
            lambda: Polygon(
                axes.c2p(time.get_value(), -1.05, -1.05),
                axes.c2p(time.get_value(), 1.05, -1.05),
                axes.c2p(time.get_value(), 1.05, 1.05),
                axes.c2p(time.get_value(), -1.05, 1.05),
                color=GREEN_C,
                fill_color=GREEN_C,
                fill_opacity=0.07,
                stroke_opacity=0.45,
                stroke_width=1.4,
            )
        )

        # Complete graph of h(t0-t), parameterized by s=t0-t.  The causal
        # tail is drawn all the way to the left edge.  The negative-argument
        # part, t0-t<0 (that is, t>t0), is explicitly drawn as zero.  When
        # h(0) is nonzero, a vertical segment connects the two branches.
        def shifted_impulse_response_mobject():
            t0 = time.get_value()
            tail = ParametricFunction(
                lambda s: axes.c2p(
                    t0 - s,
                    impulse_response(s),
                    0,
                ),
                t_range=[
                    0,
                    max(0.06, t0 - time_axis_min),
                    0.06,
                ],
                color=GREEN_C,
                stroke_width=4.0,
            )

            zero_branch = Line(
                axes.c2p(t0, 0, 0),
                axes.c2p(time_axis_max, 0, 0),
                color=GREEN_C,
                stroke_width=4.0,
            )

            pieces = VGroup(tail)
            h_at_zero = impulse_response(0.0)
            if abs(h_at_zero) > 1e-10:
                jump = Line(
                    axes.c2p(t0, h_at_zero, 0),
                    axes.c2p(t0, 0, 0),
                    color=GREEN_C,
                    stroke_width=4.0,
                )
                pieces.add(jump)
            pieces.add(zero_branch)
            return pieces

        sliding_weight = always_redraw(shifted_impulse_response_mobject)

        # h(t0-t)e^{j omega t}.  Since the input begins at t=0, there is no
        # product while t0<0.  For t0>=0, the full overlap 0<=t<=t0 is drawn;
        # equivalently, 0<=s<=t0.  No artificial tail truncation is used.
        weighted_helix = always_redraw(
            lambda: VGroup()
            if time.get_value() <= 0
            else ParametricFunction(
                lambda s: axes.c2p(
                    time.get_value() - s,
                    impulse_response(s)
                    * np.cos(omega * (time.get_value() - s)),
                    impulse_response(s)
                    * np.sin(omega * (time.get_value() - s)),
                ),
                t_range=[
                    0,
                    time.get_value(),
                    0.04,
                ],
                color=PINK,
                stroke_width=5.0,
            )
        )

        leading_point = always_redraw(
            lambda: VGroup()
            if time.get_value() <= 0
            else Dot3D(
                axes.c2p(
                    time.get_value(),
                    np.cos(omega * time.get_value()),
                    np.sin(omega * time.get_value()),
                ),
                radius=0.065,
                color=PINK,
            )
        )

        # A larger screen-fixed complex plane for the convolution integral.
        output_axes = Axes(
            # The same scale is used for all three impulse-response choices,
            # so their steady-state amplitudes can be compared directly.
            x_range=[-2.0, 2.0, 1],
            y_range=[-2.0, 2.0, 1],
            x_length=3.35,
            y_length=3.35,
            axis_config={
                "stroke_width": 1.6,
                "include_ticks": False,
                "include_tip": True,
                "tip_width": 0.12,
                "tip_height": 0.12,
            },
        ).to_corner(DR, buff=0.22).shift(UP * 0.30)

        output_title = Tex("convolution integral").scale(0.52)
        output_title.next_to(output_axes, UP, buff=0.05)
        output_re = MathTex(r"\Re").scale(0.42)
        output_re.next_to(output_axes.x_axis.get_end(), RIGHT, buff=0.03)
        output_im = MathTex(r"\Im").scale(0.42)
        output_im.next_to(output_axes.y_axis.get_end(), UP, buff=0.03)

        def transient_output(t0):
            """Exact response to exp(j*omega*t)H(t) at time t0."""
            return (
                np.exp(1j * omega * t0)
                * truncated_frequency_response(t0)
            )

        # The dashed circle is the limiting steady-state orbit.
        steady_radius = np.linalg.norm(
            output_axes.c2p(abs(frequency_response), 0)
            - output_axes.c2p(0, 0)
        )
        steady_orbit = DashedVMobject(
            Circle(
                radius=steady_radius,
                color=GRAY_B,
                stroke_width=1.6,
            ).move_to(output_axes.c2p(0, 0)),
            num_dashes=36,
        ).set_stroke(opacity=0.65)

        def output_vector_mobject():
            value = transient_output(time.get_value())
            origin = output_axes.c2p(0, 0)
            endpoint = output_axes.c2p(np.real(value), np.imag(value))
            if abs(value) < 1e-8:
                return Dot(endpoint, radius=0.035, color=PINK)
            # Building the vector as a Line with an attached tip avoids the
            # length-dependent shortening performed internally by Arrow.
            vector = Arrow(
                start=origin,
                end=endpoint,
                buff=0,
                color=PINK,
                stroke_width=5,
            )
            return vector

        output_arrow = always_redraw(output_vector_mobject)

        output_label = MathTex(r"y(t_0)").scale(0.48).set_color(PINK)
        output_label.add_updater(
            lambda mob: mob.next_to(
                output_axes.c2p(
                    np.real(transient_output(time.get_value())),
                    np.imag(transient_output(time.get_value())),
                ),
                UR,
                buff=0.05,
            )
        )

        output_trace = TracedPath(
            lambda: output_axes.c2p(
                np.real(transient_output(time.get_value())),
                np.imag(transient_output(time.get_value())),
            ),
            stroke_color=PINK,
            stroke_width=2.0,
            stroke_opacity=0.65,
        )

        title = Tex("From transient overlap to sinusoidal fidelity")
        title.scale(0.64).to_edge(UP, buff=0.12)

        time_readout = always_redraw(
            lambda: VGroup(
                MathTex("t_0=").scale(0.50),
                DecimalNumber(
                    time.get_value(),
                    num_decimal_places=1,
                    include_sign=False,
                ).scale(0.50),
            )
            .arrange(RIGHT, buff=0.04)
            .to_corner(UL, buff=0.30)
            .shift(DOWN * 0.78)
        )

        input_legend = VGroup(
            Line(LEFT * 0.22, RIGHT * 0.22, color=BLUE_C, stroke_width=4),
            MathTex(r"u(t)=e^{j\omega t}H(t)").scale(0.43),
        ).arrange(RIGHT, buff=0.10)
        impulse_legend = VGroup(
            Line(LEFT * 0.22, RIGHT * 0.22, color=GREEN_C, stroke_width=4),
            MathTex(impulse_case_tex).scale(0.40),
        ).arrange(RIGHT, buff=0.10)
        product_legend = VGroup(
            Line(LEFT * 0.22, RIGHT * 0.22, color=PINK, stroke_width=5),
            MathTex(r"h(t_0-t)e^{j\omega t}").scale(0.43),
        ).arrange(RIGHT, buff=0.10)

        legend = VGroup(input_legend, impulse_legend, product_legend)
        legend.arrange(RIGHT, buff=0.48)
        legend.to_edge(UP, buff=0.63)

        pre_input_caption = Tex("before the input starts: no overlap, output zero")
        pre_input_caption.scale(0.46).to_corner(DL, buff=0.28).shift(UP * 0.20)
        pre_input_caption.set_color(YELLOW_C)

        transient_caption = Tex("transient: the overlap is still growing")
        transient_caption.scale(0.46).to_corner(DL, buff=0.28).shift(UP * 0.20)
        transient_caption.set_color(YELLOW_C)

        steady_caption = Tex(
            "asymptotic regime: approximately fixed shape, pure rotation"
        )
        steady_caption.scale(0.46).move_to(transient_caption)
        steady_caption.set_color(YELLOW_C)

        # Construct the geometry in the same order in which it is introduced
        # conceptually: time, complex plane, input, impulse response, product.
        self.add_fixed_in_frame_mobjects(title)
        self.add_fixed_orientation_mobjects(time_axis_label)

        self.play(
            Create(axes.x_axis),
            FadeIn(time_axis_label),
            FadeIn(title),
            run_time=1.6,
        )

        self.add_fixed_orientation_mobjects(re_label, im_label)
        self.play(
            Create(axes.y_axis),
            Create(axes.z_axis),
            FadeIn(re_label, im_label),
            run_time=1.6,
        )

        self.add_fixed_in_frame_mobjects(input_legend)
        self.play(
            Create(input_zero),
            Create(input_jump),
            Create(input_helix),
            FadeIn(input_legend),
            run_time=2.3,
        )

        self.add_fixed_in_frame_mobjects(impulse_legend)
        self.play(
            FadeIn(moving_section),
            Create(sliding_weight),
            FadeIn(impulse_legend),
            run_time=2.0,
        )

        self.add_fixed_in_frame_mobjects(product_legend)
        self.play(
            FadeIn(weighted_helix),
            FadeIn(leading_point),
            FadeIn(product_legend),
            run_time=2.0,
        )

        self.add_fixed_in_frame_mobjects(
            time_readout,
            output_axes,
            output_title,
            output_re,
            output_im,
            steady_orbit,
            output_trace,
            output_arrow,
            output_label,
        )
        self.play(
            FadeIn(time_readout),
            FadeIn(output_axes, output_title, output_re, output_im),
            Create(steady_orbit),
            FadeIn(output_arrow),
            FadeIn(output_label),
            run_time=1.8,
        )

        self.add_fixed_in_frame_mobjects(pre_input_caption)
        self.play(FadeIn(pre_input_caption), run_time=0.6)
        self.play(
            time.animate.set_value(0.0),
            run_time=5,
            rate_func=linear,
        )

        self.add_fixed_in_frame_mobjects(transient_caption)
        self.play(
            ReplacementTransform(pre_input_caption, transient_caption),
            run_time=0.8,
        )
        self.play(
            time.animate.set_value(transient_end),
            run_time=10,
            rate_func=linear,
        )

        self.add_fixed_in_frame_mobjects(steady_caption)
        self.play(
            ReplacementTransform(transient_caption, steady_caption),
            run_time=0.8,
        )
        self.play(
            time.animate.set_value(final_time),
            run_time=14,
            rate_func=linear,
        )
        self.wait(2)




