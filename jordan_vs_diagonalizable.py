from manim import *
import numpy as np


class JordanComparisonBase(Scene):
    LAMBDA = -0.12
    T_MAX = 25.0
    AXIS_RADIUS = 3.2
    REFERENCE_SCALE = 0.80
    FAMILY_RADII = (0.45, 0.90)
    CASE_TITLE = "Stable repeated eigenvalue"
    FINAL_MESSAGE = (
        r"t e^{\lambda t}\to0,\ \text{but the nilpotent part can create transient motion}"
    )

    def construct(self):
        lam = self.LAMBDA
        t_max = self.T_MAX
        radius = self.AXIS_RADIUS
        reference_scale = self.REFERENCE_SCALE

        DIAG_COLOR = BLUE_C
        JORDAN_COLOR = ORANGE
        EIGEN_COLOR = TEAL_C
        GENERALIZED_COLOR = PURPLE_C
        POINT_COLOR = YELLOW

        e1 = np.array([1.0, 0.0])
        e2 = np.array([0.0, 1.0])

        def transition_D(t):
            return np.exp(lam * t) * np.eye(2)

        def transition_J(t):
            return np.exp(lam * t) * np.array([
                [1.0, t],
                [0.0, 1.0],
            ])

        def make_plane(center):
            step = radius / 4
            return NumberPlane(
                x_range=[-radius, radius, step],
                y_range=[-radius, radius, step],
                x_length=5.3,
                y_length=5.3,
                background_line_style={
                    "stroke_color": GREY_B,
                    "stroke_opacity": 0.26,
                    "stroke_width": 1,
                },
                axis_config={
                    "include_numbers": False,
                    "include_ticks": False,
                    "stroke_width": 2,
                },
            ).move_to(center)

        def axis_labels(plane):
            xlab = MathTex("x_1").scale(0.48)
            ylab = MathTex("x_2").scale(0.48)
            xlab.next_to(plane.x_axis.get_end(), RIGHT, buff=0.04)
            ylab.next_to(plane.y_axis.get_end(), UP, buff=0.04)
            return VGroup(xlab, ylab)

        def vector_arrow(
            plane,
            vector,
            color,
            start=np.zeros(2),
            width=6,
            opacity=1.0,
        ):
            start = np.asarray(start, dtype=float)
            vector = np.asarray(vector, dtype=float)

            if np.linalg.norm(vector) < 1e-9:
                return Dot(
                    plane.c2p(*start),
                    radius=0.001,
                ).set_opacity(0)

            return Arrow(
                plane.c2p(*start),
                plane.c2p(*(start + vector)),
                buff=0,
                color=color,
                stroke_width=width,
                max_tip_length_to_length_ratio=0.16,
            ).set_opacity(opacity)

        def time_readout(tracker):
            content = VGroup(
                MathTex("t=").scale(0.50),
                DecimalNumber(
                    tracker.get_value(),
                    num_decimal_places=1,
                ).scale(0.50),
            ).arrange(RIGHT, buff=0.04)

            content.to_corner(UR, buff=0.25).shift(DOWN * 0.62)

            return VGroup(
                SurroundingRectangle(
                    content,
                    color=YELLOW,
                    buff=0.09,
                    stroke_width=2.5,
                ),
                content,
            )

        # ============================================================
        # 1. Same eigenvalue, different eigenvector structure
        # ============================================================
        title = Tex(self.CASE_TITLE).scale(0.67).to_edge(UP, buff=0.17)
        self.play(Write(title), run_time=1.1)

        matrix_formulas = VGroup(
            MathTex(
                r"D=\begin{bmatrix}"
                rf"{lam:.2f}&0\\0&{lam:.2f}"
                r"\end{bmatrix}"
            ).scale(0.55),
            MathTex(
                r"J=\begin{bmatrix}"
                rf"{lam:.2f}&1\\0&{lam:.2f}"
                r"\end{bmatrix}"
            ).scale(0.55),
        ).arrange(RIGHT, buff=3.7)
        matrix_formulas.next_to(title, DOWN, buff=0.13)

        self.play(Write(matrix_formulas), run_time=1.5)

        left_plane = make_plane(LEFT * 3.45 + DOWN * 0.65)
        right_plane = make_plane(RIGHT * 3.45 + DOWN * 0.65)
        left_labels = axis_labels(left_plane)
        right_labels = axis_labels(right_plane)

        left_caption = Tex("diagonalizable").scale(0.46)
        right_caption = Tex("Jordan block").scale(0.46)
        left_caption.next_to(left_plane, UP, buff=0.04)
        right_caption.next_to(right_plane, UP, buff=0.04)

        self.play(
            Create(left_plane), Create(right_plane),
            FadeIn(left_labels, right_labels),
            FadeIn(left_caption, right_caption),
            run_time=1.7,
        )

        whole_plane = SurroundingRectangle(
            left_plane,
            color=EIGEN_COLOR,
            buff=0.02,
            fill_color=EIGEN_COLOR,
            fill_opacity=0.045,
            stroke_width=2,
        )
        jordan_eigenspace = Line(
            right_plane.c2p(-radius, 0),
            right_plane.c2p(radius, 0),
            color=EIGEN_COLOR,
            stroke_width=4,
        )

        left_eigenspace_label = MathTex(
            r"E_\lambda(D)=\mathbb{R}^2"
        ).scale(0.43).set_color(EIGEN_COLOR)
        right_eigenspace_label = MathTex(
            r"E_\lambda(J)=\operatorname{span}(e_1)"
        ).scale(0.43).set_color(EIGEN_COLOR)
        left_eigenspace_label.to_corner(DL, buff=0.25).shift(UP * 0.15)
        right_eigenspace_label.to_corner(DR, buff=0.25).shift(UP * 0.15)

        self.play(
            FadeIn(whole_plane),
            FadeIn(left_eigenspace_label),
            run_time=1.0,
        )
        self.play(
            Create(jordan_eigenspace),
            FadeIn(right_eigenspace_label),
            run_time=1.0,
        )
        self.wait(0.6)

        # ============================================================
        # 2. Dynamic transition matrices
        # ============================================================
        transition_formulas = VGroup(
            MathTex(r"e^{Dt}=e^{\lambda t}I").scale(0.52),
            MathTex(
                r"e^{Jt}=e^{\lambda t}"
                r"\begin{bmatrix}1&t\\0&1\end{bmatrix}"
            ).scale(0.52),
        ).arrange(RIGHT, buff=2.5)
        transition_formulas.move_to(matrix_formulas)

        self.play(
            FadeOut(whole_plane),
            FadeTransform(matrix_formulas, transition_formulas),
            run_time=1.2,
        )

        t = ValueTracker(0.0)
        s = reference_scale

        left_column_1 = always_redraw(
            lambda: vector_arrow(
                left_plane,
                transition_D(t.get_value()) @ (s * e1),
                EIGEN_COLOR,
                width=7,
            )
        )
        left_column_2 = always_redraw(
            lambda: vector_arrow(
                left_plane,
                transition_D(t.get_value()) @ (s * e2),
                GENERALIZED_COLOR,
                width=7,
            )
        )
        right_column_1 = always_redraw(
            lambda: vector_arrow(
                right_plane,
                transition_J(t.get_value()) @ (s * e1),
                EIGEN_COLOR,
                width=7,
            )
        )
        right_column_2 = always_redraw(
            lambda: vector_arrow(
                right_plane,
                transition_J(t.get_value()) @ (s * e2),
                GENERALIZED_COLOR,
                width=7,
            )
        )

        left_square = always_redraw(
            lambda: Polygon(
                left_plane.c2p(0, 0),
                left_plane.c2p(*(transition_D(t.get_value()) @ (s * e1))),
                left_plane.c2p(*(transition_D(t.get_value()) @ (s * (e1 + e2)))),
                left_plane.c2p(*(transition_D(t.get_value()) @ (s * e2))),
                color=DIAG_COLOR,
                fill_color=DIAG_COLOR,
                fill_opacity=0.13,
                stroke_width=3,
            )
        )
        right_square = always_redraw(
            lambda: Polygon(
                right_plane.c2p(0, 0),
                right_plane.c2p(*(transition_J(t.get_value()) @ (s * e1))),
                right_plane.c2p(*(transition_J(t.get_value()) @ (s * (e1 + e2)))),
                right_plane.c2p(*(transition_J(t.get_value()) @ (s * e2))),
                color=JORDAN_COLOR,
                fill_color=JORDAN_COLOR,
                fill_opacity=0.13,
                stroke_width=3,
            )
        )

        time_display = always_redraw(lambda: time_readout(t))

        self.play(
            FadeIn(left_square, right_square),
            GrowArrow(left_column_1), GrowArrow(left_column_2),
            GrowArrow(right_column_1), GrowArrow(right_column_2),
            FadeIn(time_display),
            run_time=1.4,
        )
        self.play(
            t.animate.set_value(t_max),
            run_time=12,
            rate_func=linear,
        )
        self.wait(0.8)

        # ============================================================
        # 3. The eigenvector behaves identically
        # ============================================================
        self.play(
            FadeOut(
                left_square, right_square,
                left_column_1, left_column_2,
                right_column_1, right_column_2,
                time_display,
            ),
            run_time=0.9,
        )
        t.set_value(0)

        key_formula_1 = MathTex(
            r"e^{Dt}e_1=e^{Jt}e_1=e^{\lambda t}e_1"
        ).scale(0.57).move_to(transition_formulas)
        self.play(FadeTransform(transition_formulas, key_formula_1), run_time=1.1)

        left_e1_curve = ParametricFunction(
            lambda tau: left_plane.c2p(*(transition_D(tau) @ (s * e1))),
            t_range=[0, t_max, max(t_max / 250, 0.02)],
            color=EIGEN_COLOR,
            stroke_width=6,
        )
        right_e1_curve = ParametricFunction(
            lambda tau: right_plane.c2p(*(transition_J(tau) @ (s * e1))),
            t_range=[0, t_max, max(t_max / 250, 0.02)],
            color=EIGEN_COLOR,
            stroke_width=6,
        )

        e1_start_left = Dot(left_plane.c2p(*(s * e1)), radius=0.065, color=EIGEN_COLOR)
        e1_start_right = Dot(right_plane.c2p(*(s * e1)), radius=0.065, color=EIGEN_COLOR)
        self.play(FadeIn(e1_start_left, e1_start_right), run_time=0.5)
        self.play(
            Create(left_e1_curve),
            Create(right_e1_curve),
            run_time=3.0,
            rate_func=linear,
        )
        self.wait(0.5)

        # ============================================================
        # 4. The generalized eigenvector reveals the difference
        # ============================================================
        key_formula_2 = VGroup(
            MathTex(r"e^{Dt}e_2=e^{\lambda t}e_2").scale(0.51),
            MathTex(
                r"e^{Jt}e_2=e^{\lambda t}(te_1+e_2)"
            ).scale(0.51),
        ).arrange(RIGHT, buff=1.2).move_to(key_formula_1)

        self.play(
            FadeOut(left_e1_curve, right_e1_curve, e1_start_left, e1_start_right),
            FadeTransform(key_formula_1, key_formula_2),
            run_time=1.1,
        )

        left_e2_curve = ParametricFunction(
            lambda tau: left_plane.c2p(*(transition_D(tau) @ (s * e2))),
            t_range=[0, t_max, max(t_max / 250, 0.02)],
            color=GENERALIZED_COLOR,
            stroke_width=6,
        )
        right_e2_curve = ParametricFunction(
            lambda tau: right_plane.c2p(*(transition_J(tau) @ (s * e2))),
            t_range=[0, t_max, max(t_max / 250, 0.02)],
            color=GENERALIZED_COLOR,
            stroke_width=6,
        )

        e2_start_left = Dot(left_plane.c2p(*(s * e2)), radius=0.065, color=GENERALIZED_COLOR)
        e2_start_right = Dot(right_plane.c2p(*(s * e2)), radius=0.065, color=GENERALIZED_COLOR)

        moving_parameter = ValueTracker(0.0)
        moving_left = always_redraw(
            lambda: Dot(
                left_plane.c2p(
                    *(transition_D(moving_parameter.get_value()) @ (s * e2))
                ),
                radius=0.068,
                color=GENERALIZED_COLOR,
            )
        )
        moving_right = always_redraw(
            lambda: Dot(
                right_plane.c2p(
                    *(transition_J(moving_parameter.get_value()) @ (s * e2))
                ),
                radius=0.068,
                color=GENERALIZED_COLOR,
            )
        )

        self.play(FadeIn(e2_start_left, e2_start_right), run_time=0.5)
        self.play(
            Create(left_e2_curve),
            Create(right_e2_curve),
            FadeIn(moving_left, moving_right),
            moving_parameter.animate.set_value(t_max),
            run_time=8.0,
            rate_func=linear,
        )
        self.wait(0.8)

        # ============================================================
        # 5. Several initial conditions
        # ============================================================
        self.play(
            FadeOut(
                left_e2_curve, right_e2_curve,
                e2_start_left, e2_start_right,
                moving_left, moving_right,
                key_formula_2,
            ),
            run_time=0.9,
        )

        initial_conditions = []
        for family_radius in self.FAMILY_RADII:
            for angle in np.linspace(0, 2 * PI, 10, endpoint=False):
                initial_conditions.append(
                    family_radius * np.array([
                        np.cos(angle),
                        np.sin(angle),
                    ])
                )

        left_initial_dots = VGroup(
            *[
                Dot(left_plane.c2p(*x0), radius=0.032, color=GREY_A)
                for x0 in initial_conditions
            ]
        )
        right_initial_dots = VGroup(
            *[
                Dot(right_plane.c2p(*x0), radius=0.032, color=GREY_A)
                for x0 in initial_conditions
            ]
        )

        left_curves = VGroup(
            *[
                ParametricFunction(
                    lambda tau, x0=x0: left_plane.c2p(*(transition_D(tau) @ x0)),
                    t_range=[0, t_max, max(t_max / 220, 0.025)],
                    color=DIAG_COLOR,
                    stroke_width=2.0,
                    stroke_opacity=0.58,
                )
                for x0 in initial_conditions
            ]
        )
        right_curves = VGroup(
            *[
                ParametricFunction(
                    lambda tau, x0=x0: right_plane.c2p(*(transition_J(tau) @ x0)),
                    t_range=[0, t_max, max(t_max / 220, 0.025)],
                    color=JORDAN_COLOR,
                    stroke_width=2.0,
                    stroke_opacity=0.58,
                )
                for x0 in initial_conditions
            ]
        )

        comparison_caption = VGroup(
            Tex("every direction is an eigendirection").scale(0.40).set_color(DIAG_COLOR),
            Tex("only one eigendirection; all others are sheared").scale(0.40).set_color(JORDAN_COLOR),
        ).arrange(RIGHT, buff=1.3).to_edge(DOWN, buff=0.17)

        self.play(
            FadeIn(left_initial_dots, right_initial_dots),
            FadeIn(comparison_caption),
            run_time=0.9,
        )
        self.play(
            AnimationGroup(
                *[Create(curve) for curve in left_curves],
                *[Create(curve) for curve in right_curves],
                lag_ratio=0.015,
            ),
            run_time=10,
            rate_func=linear,
        )
        self.wait(0.8)

        # ============================================================
        # 6. Final message
        # ============================================================
        final_message = MathTex(self.FINAL_MESSAGE).scale(0.54)
        final_message.to_edge(UP, buff=0.25)

        self.play(
            FadeOut(title),
            FadeIn(final_message),
            run_time=1.1,
        )
        self.wait(3)


class StableJordanComparison(JordanComparisonBase):
    LAMBDA = -0.12
    T_MAX = 25.0
    AXIS_RADIUS = 3.2
    REFERENCE_SCALE = 0.80
    FAMILY_RADII = (0.45, 0.90)
    CASE_TITLE = "Stable repeated eigenvalue"
    FINAL_MESSAGE = (
        r"t e^{\lambda t}\to0,\ "
        r"\text{but the nilpotent part can create transient motion}"
    )


class ZeroJordanComparison(JordanComparisonBase):
    LAMBDA = 0.0
    T_MAX = 6.0
    AXIS_RADIUS = 3.8
    REFERENCE_SCALE = 0.55
    FAMILY_RADII = (0.28, 0.52)
    CASE_TITLE = "Zero repeated eigenvalue"
    FINAL_MESSAGE = (
        r"e^{Dt}=I,\qquad e^{Jt}=I+tN:\ "
        r"\text{the nilpotent part produces linear drift}"
    )


class UnstableJordanComparison(JordanComparisonBase):
    LAMBDA = 0.25
    T_MAX = 5.0
    AXIS_RADIUS = 5.7
    REFERENCE_SCALE = 0.25
    FAMILY_RADII = (0.12, 0.24)
    CASE_TITLE = "Unstable repeated eigenvalue"
    FINAL_MESSAGE = (
        r"e^{\lambda t}\text{ grows exponentially, while }"
        r"t e^{\lambda t}\text{ adds polynomial shear}"
    )

