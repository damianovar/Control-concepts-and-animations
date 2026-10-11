from manim import *
import numpy as np


class JordanAsLimitOfDiagonalizable(Scene):
    def construct(self):
        # ============================================================
        # Parameters
        # ============================================================
        lam = -0.12
        epsilon = ValueTracker(0.08)
        horizon = 20.0

        JORDAN_COLOR = ORANGE
        DIAG_COLOR = BLUE_C
        EIGEN_COLOR = TEAL_C
        SECOND_EIGEN_COLOR = PURPLE_C
        STATE_COLOR = YELLOW

        e1 = np.array([1.0, 0.0])
        e2 = np.array([0.0, 1.0])

        def A_eps(eps):
            return np.array([
                [lam, 1.0],
                [0.0, lam + eps],
            ])

        def jordan_transition(t):
            return np.exp(lam * t) * np.array([
                [1.0, t],
                [0.0, 1.0],
            ])

        def diagonalizable_transition(t, eps):
            if abs(eps) < 1e-8:
                return jordan_transition(t)

            e_lam = np.exp(lam * t)
            e_shifted = np.exp((lam + eps) * t)

            return np.array([
                [e_lam, (e_shifted - e_lam) / eps],
                [0.0, e_shifted],
            ])

        def eigenvector_matrix(eps):
            return np.array([
                [1.0, 1.0],
                [0.0, eps],
            ])

        def make_plane(center, radius=4.0, length=5.25):
            step = radius / 4
            return NumberPlane(
                x_range=[-radius, radius, step],
                y_range=[-radius, radius, step],
                x_length=length,
                y_length=length,
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
            xlab = MathTex("x_1").scale(0.47)
            ylab = MathTex("x_2").scale(0.47)
            xlab.next_to(plane.x_axis.get_end(), RIGHT, buff=0.04)
            ylab.next_to(plane.y_axis.get_end(), UP, buff=0.04)
            return VGroup(xlab, ylab)

        def eigenspace_line(plane, direction, radius, color, opacity=0.80):
            direction = np.asarray(direction, dtype=float)
            end = direction * radius / np.max(np.abs(direction))
            return Line(
                plane.c2p(*(-end)),
                plane.c2p(*end),
                color=color,
                stroke_width=3.5,
            ).set_opacity(opacity)

        def epsilon_readout():
            eps = epsilon.get_value()
            content = VGroup(
                MathTex(r"\varepsilon=").scale(0.48),
                DecimalNumber(eps, num_decimal_places=3).scale(0.48),
            ).arrange(RIGHT, buff=0.04)

            content.to_corner(UR, buff=0.25).shift(DOWN * 0.55)

            return VGroup(
                SurroundingRectangle(
                    content,
                    color=YELLOW,
                    buff=0.08,
                    stroke_width=2.5,
                ),
                content,
            )

        # ============================================================
        # 1. Jordan block and nearby diagonalizable family
        # ============================================================
        title = Tex(
            "A Jordan block is the limit of diagonalizable matrices"
        ).scale(0.65).to_edge(UP, buff=0.17)

        self.play(Write(title), run_time=1.4)

        matrix_formulas = VGroup(
            MathTex(
                r"J=\begin{bmatrix}"
                r"\lambda&1\\0&\lambda"
                r"\end{bmatrix}"
            ).scale(0.55),
            MathTex(
                r"A_\varepsilon=\begin{bmatrix}"
                r"\lambda&1\\0&\lambda+\varepsilon"
                r"\end{bmatrix}"
            ).scale(0.55),
        ).arrange(RIGHT, buff=3.0)
        matrix_formulas.next_to(title, DOWN, buff=0.12)

        self.play(Write(matrix_formulas), run_time=1.4)

        left_plane = make_plane(LEFT * 3.45 + DOWN * 0.68)
        right_plane = make_plane(RIGHT * 3.45 + DOWN * 0.68)
        left_labels = axis_labels(left_plane)
        right_labels = axis_labels(right_plane)

        left_caption = Tex("defective: one eigenspace").scale(0.43)
        right_caption = Tex("diagonalizable: two eigenspaces").scale(0.43)
        left_caption.next_to(left_plane, UP, buff=0.04)
        right_caption.next_to(right_plane, UP, buff=0.04)

        self.play(
            Create(left_plane), Create(right_plane),
            FadeIn(left_labels, right_labels),
            FadeIn(left_caption, right_caption),
            run_time=1.7,
        )

        # Jordan block: only span(e1).
        left_eigenspace = eigenspace_line(
            left_plane, e1, 4.0, EIGEN_COLOR
        )

        # A_epsilon: span(e1) and span([1,epsilon]).
        right_eigenspace_1 = eigenspace_line(
            right_plane, e1, 4.0, EIGEN_COLOR
        )
        right_eigenspace_2 = always_redraw(
            lambda: eigenspace_line(
                right_plane,
                np.array([1.0, epsilon.get_value()]),
                4.0,
                SECOND_EIGEN_COLOR,
            )
        )

        left_eigen_label = MathTex(
            r"E_\lambda(J)=\operatorname{span}(e_1)"
        ).scale(0.40).set_color(EIGEN_COLOR)
        left_eigen_label.to_corner(DL, buff=0.23).shift(UP * 0.14)

        right_eigen_label = MathTex(
            r"v_1=e_1,\qquad v_2=\begin{bmatrix}1\\\varepsilon\end{bmatrix}"
        ).scale(0.38)
        right_eigen_label.to_corner(DR, buff=0.23).shift(UP * 0.14)
        right_eigen_label[0].set_color(EIGEN_COLOR)

        eps_display = always_redraw(epsilon_readout)

        self.play(
            Create(left_eigenspace),
            Create(right_eigenspace_1),
            Create(right_eigenspace_2),
            FadeIn(left_eigen_label, right_eigen_label, eps_display),
            run_time=1.4,
        )

        # ============================================================
        # 2. Magnified inset for the collapsing eigenspaces
        # ============================================================
        inset_axes = Axes(
            x_range=[-1.0, 1.0, 0.5],
            y_range=[-1.1, 1.1, 0.5],
            x_length=2.25,
            y_length=1.65,
            axis_config={
                "include_numbers": False,
                "include_ticks": False,
                "stroke_width": 1.5,
            },
        ).to_corner(DR, buff=0.27).shift(UP * 0.72)

        inset_background = BackgroundRectangle(
            inset_axes,
            color=BLACK,
            fill_opacity=0.78,
            buff=0.12,
        )
        inset_title = Tex("vertical magnification $\times 12$").scale(0.32)
        inset_title.next_to(inset_axes, UP, buff=0.04)

        inset_line_1 = Line(
            inset_axes.c2p(-1, 0),
            inset_axes.c2p(1, 0),
            color=EIGEN_COLOR,
            stroke_width=3,
        )
        inset_line_2 = always_redraw(
            lambda: Line(
                inset_axes.c2p(-1, -12 * epsilon.get_value()),
                inset_axes.c2p(1, 12 * epsilon.get_value()),
                color=SECOND_EIGEN_COLOR,
                stroke_width=3,
            )
        )

        self.play(
            FadeIn(inset_background, inset_axes, inset_title),
            Create(inset_line_1),
            Create(inset_line_2),
            run_time=1.1,
        )

        # ============================================================
        # 3. Same initial conditions, increasingly similar trajectories
        # ============================================================
        initial_conditions = [
            0.72 * e2,
            np.array([0.45, 0.55]),
            np.array([-0.35, 0.62]),
        ]

        left_trajectories = VGroup(
            *[
                ParametricFunction(
                    lambda tau, x0=x0: left_plane.c2p(
                        *(jordan_transition(tau) @ x0)
                    ),
                    t_range=[0, horizon, 0.06],
                    color=JORDAN_COLOR,
                    stroke_width=4,
                    stroke_opacity=0.82,
                )
                for x0 in initial_conditions
            ]
        )

        right_trajectories = always_redraw(
            lambda: VGroup(
                *[
                    ParametricFunction(
                        lambda tau, x0=x0: right_plane.c2p(
                            *(
                                diagonalizable_transition(
                                    tau, epsilon.get_value()
                                ) @ x0
                            )
                        ),
                        t_range=[0, horizon, 0.08],
                        color=DIAG_COLOR,
                        stroke_width=4,
                        stroke_opacity=0.82,
                    )
                    for x0 in initial_conditions
                ]
            )
        )

        left_starting_points = VGroup(
            *[
                Dot(left_plane.c2p(*x0), radius=0.05, color=STATE_COLOR)
                for x0 in initial_conditions
            ]
        )
        right_starting_points = VGroup(
            *[
                Dot(right_plane.c2p(*x0), radius=0.05, color=STATE_COLOR)
                for x0 in initial_conditions
            ]
        )

        self.play(
            FadeIn(left_starting_points, right_starting_points),
            Create(left_trajectories),
            FadeIn(right_trajectories),
            run_time=3.0,
        )

        condition_readout = always_redraw(
            lambda: VGroup(
                MathTex(r"\operatorname{cond}(P_\varepsilon)\approx").scale(0.39),
                DecimalNumber(
                    np.linalg.cond(
                        eigenvector_matrix(epsilon.get_value())
                    ),
                    num_decimal_places=1,
                ).scale(0.39),
            ).arrange(RIGHT, buff=0.04).to_corner(UL, buff=0.25).shift(DOWN * 0.62)
        )
        self.play(FadeIn(condition_readout), run_time=0.6)

        # The diagonalizable trajectories converge toward the Jordan ones.
        self.play(
            epsilon.animate.set_value(0.01),
            run_time=10,
            rate_func=smooth,
        )
        self.wait(1.0)

        # ============================================================
        # 4. The divided difference becomes t exp(lambda t)
        # ============================================================
        limit_formula = MathTex(
            r"\frac{e^{(\lambda+\varepsilon)t}-e^{\lambda t}}{\varepsilon}"
            r"\longrightarrow "
            r"t e^{\lambda t}"
        ).scale(0.64).to_edge(UP, buff=0.22)

        self.play(
            FadeOut(title, matrix_formulas),
            FadeIn(limit_formula),
            run_time=1.1,
        )

        transition_formulas = VGroup(
            MathTex(
                r"e^{Jt}=\begin{bmatrix}"
                r"e^{\lambda t}&te^{\lambda t}\\"
                r"0&e^{\lambda t}"
                r"\end{bmatrix}"
            ).scale(0.45),
            MathTex(
                r"e^{A_\varepsilon t}=\begin{bmatrix}"
                r"e^{\lambda t}&"
                r"\frac{e^{(\lambda+\varepsilon)t}-e^{\lambda t}}{\varepsilon}\\"
                r"0&e^{(\lambda+\varepsilon)t}"
                r"\end{bmatrix}"
            ).scale(0.42),
        ).arrange(RIGHT, buff=1.15)
        transition_formulas.next_to(limit_formula, DOWN, buff=0.10)

        self.play(FadeIn(transition_formulas), run_time=1.0)
        self.wait(1.0)

        # ============================================================
        # 5. Nearly parallel eigenvectors require large cancellation
        # ============================================================
        self.play(
            FadeOut(
                left_plane, right_plane,
                left_labels, right_labels,
                left_caption, right_caption,
                left_eigenspace, right_eigenspace_1, right_eigenspace_2,
                left_eigen_label, right_eigen_label,
                left_trajectories, right_trajectories,
                left_starting_points, right_starting_points,
                inset_background, inset_axes, inset_title,
                inset_line_1, inset_line_2,
                eps_display, condition_readout,
                transition_formulas,
            ),
            run_time=1.2,
        )

        epsilon.set_value(0.20)

        decomposition_formula = MathTex(
            r"e_2=-\frac{1}{\varepsilon}v_1"
            r"+\frac{1}{\varepsilon}v_2"
        ).scale(0.72).next_to(limit_formula, DOWN, buff=0.25)
        self.play(Write(decomposition_formula), run_time=1.2)

        coefficient_axes = Axes(
            x_range=[-22, 22, 5],
            y_range=[-1.7, 1.7, 1],
            x_length=10.0,
            y_length=3.2,
            axis_config={
                "include_numbers": False,
                "include_ticks": False,
                "stroke_width": 1.6,
            },
        ).shift(DOWN * 1.0)

        zero_line = DashedLine(
            coefficient_axes.c2p(0, -1.5),
            coefficient_axes.c2p(0, 1.5),
            color=GREY_B,
            dash_length=0.08,
        )

        negative_bar = always_redraw(
            lambda: Arrow(
                coefficient_axes.c2p(0, 0.72),
                coefficient_axes.c2p(-1 / epsilon.get_value(), 0.72),
                buff=0,
                color=EIGEN_COLOR,
                stroke_width=8,
                max_tip_length_to_length_ratio=0.10,
            )
        )
        positive_bar = always_redraw(
            lambda: Arrow(
                coefficient_axes.c2p(0, -0.72),
                coefficient_axes.c2p(1 / epsilon.get_value(), -0.72),
                buff=0,
                color=SECOND_EIGEN_COLOR,
                stroke_width=8,
                max_tip_length_to_length_ratio=0.10,
            )
        )

        negative_label = MathTex(r"-\frac1\varepsilon v_1").scale(0.50).set_color(EIGEN_COLOR)
        positive_label = MathTex(r"+\frac1\varepsilon v_2").scale(0.50).set_color(SECOND_EIGEN_COLOR)
        negative_label.next_to(coefficient_axes.c2p(0, 0.72), RIGHT, buff=0.12)
        positive_label.next_to(coefficient_axes.c2p(0, -0.72), LEFT, buff=0.12)

        coefficient_readout = always_redraw(
            lambda: VGroup(
                MathTex(r"1/\varepsilon=").scale(0.46),
                DecimalNumber(
                    1 / epsilon.get_value(),
                    num_decimal_places=1,
                ).scale(0.46),
            ).arrange(RIGHT, buff=0.04).to_corner(DR, buff=0.30)
        )

        cancellation_caption = Tex(
            "two large modal contributions produce one small resultant"
        ).scale(0.46).to_edge(DOWN, buff=0.25)

        self.play(
            Create(coefficient_axes), Create(zero_line),
            FadeIn(negative_bar, positive_bar),
            FadeIn(negative_label, positive_label),
            FadeIn(coefficient_readout, cancellation_caption),
            run_time=1.4,
        )

        self.play(
            epsilon.animate.set_value(0.05),
            run_time=8,
            rate_func=smooth,
        )
        self.wait(0.8)

        # ============================================================
        # 6. At epsilon=0 the second eigenvector is lost
        # ============================================================
        self.play(
            FadeOut(
                coefficient_axes, zero_line,
                negative_bar, positive_bar,
                negative_label, positive_label,
                coefficient_readout, cancellation_caption,
                decomposition_formula,
            ),
            run_time=1.0,
        )

        final_comparison = VGroup(
            VGroup(
                MathTex(r"\varepsilon\neq0").scale(0.62),
                MathTex(r"v_1=e_1,\qquad v_2=\begin{bmatrix}1\\\varepsilon\end{bmatrix}").scale(0.54),
                Tex("two eigenvectors, but increasingly ill-conditioned").scale(0.43),
            ).arrange(DOWN, buff=0.18),
            VGroup(
                MathTex(r"\varepsilon=0").scale(0.62),
                MathTex(r"(J-\lambda I)e_2=e_1").scale(0.58),
                Tex("one eigenvector and one generalized eigenvector").scale(0.43),
            ).arrange(DOWN, buff=0.18),
        ).arrange(RIGHT, buff=1.5)

        self.play(FadeIn(final_comparison), run_time=1.4)

        final_message = Tex(
            "Trajectories can be arbitrarily similar, "
            "while the eigenstructure is fundamentally different."
        ).scale(0.54).to_edge(DOWN, buff=0.35)

        self.play(Write(final_message), run_time=1.4)
        self.wait(3)

