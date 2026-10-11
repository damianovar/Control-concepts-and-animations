from manim import *
import numpy as np


class DiagonalizationAndTransitionMatrix(Scene):
    def construct(self):
        # ============================================================
        # A = P D P^{-1}, with a deliberately nonorthogonal eigenbasis
        # ============================================================
        v1 = np.array([2.0, 1.0])
        v2 = np.array([1.0, 3.0])

        lambda_1 = 0.08
        lambda_2 = -0.12

        P = np.column_stack((v1, v2))
        P_inv = np.linalg.inv(P)
        D = np.diag([lambda_1, lambda_2])
        A = P @ D @ P_inv

        E1_COLOR = TEAL_C
        E2_COLOR = PURPLE_C
        STATE_COLOR = YELLOW
        GRID_COLOR = GREY_B

        def exp_D(t):
            return np.diag([
                np.exp(lambda_1 * t),
                np.exp(lambda_2 * t),
            ])

        def exp_A(t):
            return P @ exp_D(t) @ P_inv

        def make_plane(center, radius, length=5.2):
            step = radius / 4
            return NumberPlane(
                x_range=[-radius, radius, step],
                y_range=[-radius, radius, step],
                x_length=length,
                y_length=length,
                background_line_style={
                    "stroke_color": GRID_COLOR,
                    "stroke_opacity": 0.27,
                    "stroke_width": 1,
                },
                axis_config={
                    "include_numbers": False,
                    "include_ticks": False,
                    "stroke_width": 2,
                },
            ).move_to(center)

        def plane_labels(plane, horizontal, vertical):
            xlab = MathTex(horizontal).scale(0.52)
            ylab = MathTex(vertical).scale(0.52)
            xlab.next_to(plane.x_axis.get_end(), RIGHT, buff=0.05)
            ylab.next_to(plane.y_axis.get_end(), UP, buff=0.05)
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

        def eigenspace_line(plane, direction, radius, color, opacity=0.72):
            direction = np.asarray(direction, dtype=float)
            end = direction * radius / np.max(np.abs(direction))
            return Line(
                plane.c2p(*(-end)),
                plane.c2p(*end),
                color=color,
                stroke_width=3,
            ).set_opacity(opacity)

        def time_readout(tracker):
            content = VGroup(
                MathTex("t=").scale(0.50),
                DecimalNumber(
                    tracker.get_value(),
                    num_decimal_places=1,
                ).scale(0.50),
            ).arrange(RIGHT, buff=0.04)

            content.to_corner(UR, buff=0.27).shift(DOWN * 0.64)

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
        # 1. Original and modal coordinate systems
        # ============================================================
        title = MathTex(
            r"A=PDP^{-1}",
            r"\qquad",
            r"z=P^{-1}x",
        ).scale(0.70).to_edge(UP, buff=0.20)

        self.play(Write(title), run_time=1.4)

        x_plane = make_plane(LEFT * 3.45 + DOWN * 0.48, 3.5)
        z_plane = make_plane(RIGHT * 3.45 + DOWN * 0.48, 2.6)

        x_labels = plane_labels(x_plane, "x_1", "x_2")
        z_labels = plane_labels(z_plane, "z_1", "z_2")

        x_title = Tex("original coordinates").scale(0.47)
        z_title = Tex("modal coordinates").scale(0.47)
        x_title.next_to(x_plane, UP, buff=0.04)
        z_title.next_to(z_plane, UP, buff=0.04)

        self.play(
            Create(x_plane),
            FadeIn(x_labels, x_title),
            run_time=1.5,
        )
        self.play(
            Create(z_plane),
            FadeIn(z_labels, z_title),
            run_time=1.5,
        )

        coordinate_arrow = Arrow(
            x_plane.get_right() + RIGHT * 0.08,
            z_plane.get_left() + LEFT * 0.08,
            buff=0.12,
            color=WHITE,
        )
        coordinate_label = MathTex(r"P^{-1}").scale(0.55)
        coordinate_label.next_to(coordinate_arrow, UP, buff=0.05)

        self.play(
            GrowArrow(coordinate_arrow),
            FadeIn(coordinate_label),
            run_time=0.9,
        )

        # ============================================================
        # 2. Eigenspaces become coordinate axes
        # ============================================================
        x_E1 = eigenspace_line(x_plane, v1, 3.5, E1_COLOR)
        x_E2 = eigenspace_line(x_plane, v2, 3.5, E2_COLOR)

        z_E1 = Line(
            z_plane.c2p(-2.6, 0),
            z_plane.c2p(2.6, 0),
            color=E1_COLOR,
            stroke_width=4,
        ).set_opacity(0.72)

        z_E2 = Line(
            z_plane.c2p(0, -2.6),
            z_plane.c2p(0, 2.6),
            color=E2_COLOR,
            stroke_width=4,
        ).set_opacity(0.72)

        x_E1_label = MathTex(r"E_{\lambda_1}").scale(0.40).set_color(E1_COLOR)
        x_E2_label = MathTex(r"E_{\lambda_2}").scale(0.40).set_color(E2_COLOR)
        x_E1_label.move_to(x_plane.c2p(2.25, 1.40))
        x_E2_label.move_to(x_plane.c2p(0.95, 2.80))

        z_E1_label = MathTex(r"z_1\text{-axis}").scale(0.37).set_color(E1_COLOR)
        z_E2_label = MathTex(r"z_2\text{-axis}").scale(0.37).set_color(E2_COLOR)
        z_E1_label.move_to(z_plane.c2p(1.75, 0.28))
        z_E2_label.move_to(z_plane.c2p(0.48, 1.85))

        self.play(
            Create(x_E1),
            Create(z_E1),
            FadeIn(x_E1_label, z_E1_label),
            run_time=1.2,
        )
        self.play(
            Create(x_E2),
            Create(z_E2),
            FadeIn(x_E2_label, z_E2_label),
            run_time=1.2,
        )

        eigenvalue_labels = VGroup(
            MathTex(r"\lambda_1=0.08>0").scale(0.42).set_color(E1_COLOR),
            MathTex(r"\lambda_2=-0.12<0").scale(0.42).set_color(E2_COLOR),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.09)
        eigenvalue_labels.to_corner(DR, buff=0.22)
        self.play(FadeIn(eigenvalue_labels), run_time=0.7)

        # Map the eigenvectors to the standard basis vectors.
        v1_arrow = vector_arrow(x_plane, v1, E1_COLOR)
        v2_arrow = vector_arrow(x_plane, v2, E2_COLOR)
        ez1_arrow = vector_arrow(z_plane, np.array([1.0, 0.0]), E1_COLOR)
        ez2_arrow = vector_arrow(z_plane, np.array([0.0, 1.0]), E2_COLOR)

        v1_label = MathTex(r"v_1").scale(0.43).set_color(E1_COLOR)
        v2_label = MathTex(r"v_2").scale(0.43).set_color(E2_COLOR)
        ez1_label = MathTex(r"e_1").scale(0.43).set_color(E1_COLOR)
        ez2_label = MathTex(r"e_2").scale(0.43).set_color(E2_COLOR)
        v1_label.next_to(v1_arrow.get_end(), DR, buff=0.04)
        v2_label.next_to(v2_arrow.get_end(), UL, buff=0.04)
        ez1_label.next_to(ez1_arrow.get_end(), DR, buff=0.04)
        ez2_label.next_to(ez2_arrow.get_end(), UL, buff=0.04)

        self.play(
            GrowArrow(v1_arrow),
            GrowArrow(v2_arrow),
            FadeIn(v1_label, v2_label),
            run_time=1.2,
        )
        self.play(
            TransformFromCopy(v1_arrow, ez1_arrow),
            TransformFromCopy(v2_arrow, ez2_arrow),
            FadeIn(ez1_label, ez2_label),
            run_time=1.4,
        )
        self.wait(0.5)

        self.play(
            FadeOut(v1_arrow, v2_arrow, ez1_arrow, ez2_arrow),
            FadeOut(v1_label, v2_label, ez1_label, ez2_label),
            run_time=0.8,
        )

        # ============================================================
        # 3. Dynamics become decoupled in modal coordinates
        # ============================================================
        derivation_1 = MathTex(
            r"\dot z=P^{-1}\dot x=P^{-1}APz"
        ).scale(0.58).next_to(title, DOWN, buff=0.12)
        derivation_2 = MathTex(
            r"\dot z=Dz"
        ).scale(0.62).move_to(derivation_1)

        self.play(Write(derivation_1), run_time=1.2)
        self.play(FadeTransform(derivation_1, derivation_2), run_time=1.1)

        D_formula = MathTex(
            r"D=\begin{bmatrix}"
            r"0.08&0\\0&-0.12"
            r"\end{bmatrix}"
        ).scale(0.52).to_corner(DR, buff=0.22).shift(UP * 0.65)
        self.play(FadeTransform(eigenvalue_labels, D_formula), run_time=1.0)

        # ============================================================
        # 4. Decompose a generic initial condition
        # ============================================================
        modal_initial = np.array([0.60, 0.40])
        x_initial = P @ modal_initial

        x_component_1 = vector_arrow(
            x_plane,
            modal_initial[0] * v1,
            E1_COLOR,
            width=6,
        )
        x_component_2 = vector_arrow(
            x_plane,
            modal_initial[1] * v2,
            E2_COLOR,
            start=modal_initial[0] * v1,
            width=6,
        )
        x_initial_dot = Dot(
            x_plane.c2p(*x_initial),
            radius=0.075,
            color=STATE_COLOR,
        )
        x_initial_label = MathTex(r"x_0").scale(0.43).set_color(STATE_COLOR)
        x_initial_label.next_to(x_initial_dot, UR, buff=0.04)

        decomposition = MathTex(
            r"x_0=c_1v_1+c_2v_2"
        ).scale(0.50).to_corner(DL, buff=0.22).shift(UP * 0.16)

        self.play(
            GrowArrow(x_component_1),
            GrowArrow(x_component_2),
            FadeIn(x_initial_dot, x_initial_label),
            Write(decomposition),
            run_time=1.7,
        )

        z_initial_dot = Dot(
            z_plane.c2p(*modal_initial),
            radius=0.075,
            color=STATE_COLOR,
        )
        z_initial_label = MathTex(
            r"z_0=\begin{bmatrix}c_1\\c_2\end{bmatrix}"
        ).scale(0.40).set_color(STATE_COLOR)
        z_initial_label.next_to(z_initial_dot, UR, buff=0.04)

        z_component_1 = vector_arrow(
            z_plane,
            np.array([modal_initial[0], 0]),
            E1_COLOR,
            width=6,
        )
        z_component_2 = vector_arrow(
            z_plane,
            np.array([0, modal_initial[1]]),
            E2_COLOR,
            width=6,
        )

        projection_1 = DashedLine(
            z_plane.c2p(modal_initial[0], 0),
            z_plane.c2p(*modal_initial),
            color=E2_COLOR,
            dash_length=0.08,
        )
        projection_2 = DashedLine(
            z_plane.c2p(0, modal_initial[1]),
            z_plane.c2p(*modal_initial),
            color=E1_COLOR,
            dash_length=0.08,
        )

        self.play(
            TransformFromCopy(x_initial_dot, z_initial_dot),
            GrowArrow(z_component_1),
            GrowArrow(z_component_2),
            Create(projection_1),
            Create(projection_2),
            FadeIn(z_initial_label),
            run_time=1.5,
        )

        # ============================================================
        # 5. Simultaneous evolution in x and z coordinates
        # ============================================================
        time = ValueTracker(0.0)

        modal_component_1 = always_redraw(
            lambda: vector_arrow(
                z_plane,
                np.array([
                    modal_initial[0] * np.exp(lambda_1 * time.get_value()),
                    0,
                ]),
                E1_COLOR,
                width=7,
            )
        )
        modal_component_2 = always_redraw(
            lambda: vector_arrow(
                z_plane,
                np.array([
                    0,
                    modal_initial[1] * np.exp(lambda_2 * time.get_value()),
                ]),
                E2_COLOR,
                width=7,
            )
        )
        modal_point = always_redraw(
            lambda: Dot(
                z_plane.c2p(
                    modal_initial[0] * np.exp(lambda_1 * time.get_value()),
                    modal_initial[1] * np.exp(lambda_2 * time.get_value()),
                ),
                radius=0.075,
                color=STATE_COLOR,
            )
        )
        modal_projection_1 = always_redraw(
            lambda: DashedLine(
                z_plane.c2p(
                    modal_initial[0] * np.exp(lambda_1 * time.get_value()), 0
                ),
                modal_point.get_center(),
                color=E2_COLOR,
                dash_length=0.08,
            )
        )
        modal_projection_2 = always_redraw(
            lambda: DashedLine(
                z_plane.c2p(
                    0, modal_initial[1] * np.exp(lambda_2 * time.get_value())
                ),
                modal_point.get_center(),
                color=E1_COLOR,
                dash_length=0.08,
            )
        )

        physical_component_1 = always_redraw(
            lambda: vector_arrow(
                x_plane,
                modal_initial[0]
                * np.exp(lambda_1 * time.get_value())
                * v1,
                E1_COLOR,
                width=7,
            )
        )
        physical_component_2 = always_redraw(
            lambda: vector_arrow(
                x_plane,
                modal_initial[1]
                * np.exp(lambda_2 * time.get_value())
                * v2,
                E2_COLOR,
                start=(
                    modal_initial[0]
                    * np.exp(lambda_1 * time.get_value())
                    * v1
                ),
                width=7,
            )
        )
        physical_point = always_redraw(
            lambda: Dot(
                x_plane.c2p(
                    *(
                        modal_initial[0]
                        * np.exp(lambda_1 * time.get_value())
                        * v1
                        + modal_initial[1]
                        * np.exp(lambda_2 * time.get_value())
                        * v2
                    )
                ),
                radius=0.075,
                color=STATE_COLOR,
            )
        )

        time_display = always_redraw(lambda: time_readout(time))

        modal_solution = MathTex(
            r"z(t)=\begin{bmatrix}"
            r"e^{\lambda_1t}c_1\\"
            r"e^{\lambda_2t}c_2"
            r"\end{bmatrix}"
        ).scale(0.46).to_corner(DR, buff=0.22).shift(UP * 0.72)

        physical_solution = MathTex(
            r"x(t)=e^{\lambda_1t}c_1v_1"
            r"+e^{\lambda_2t}c_2v_2"
        ).scale(0.46).to_corner(DL, buff=0.22).shift(UP * 0.18)

        self.play(
            FadeOut(
                x_component_1, x_component_2,
                x_initial_dot, x_initial_label,
                z_initial_dot, z_initial_label,
                z_component_1, z_component_2,
                projection_1, projection_2,
                decomposition,
            ),
            FadeIn(
                modal_component_1, modal_component_2,
                modal_point, modal_projection_1, modal_projection_2,
                physical_component_1, physical_component_2,
                physical_point, time_display,
            ),
            FadeIn(modal_solution, physical_solution),
            run_time=1.4,
        )

        self.play(
            time.animate.set_value(10),
            run_time=12,
            rate_func=linear,
        )
        self.wait(0.8)

        # ============================================================
        # 6. Transition matrices in the two coordinate systems
        # ============================================================
        self.play(
            FadeOut(
                modal_component_1, modal_component_2,
                modal_point, modal_projection_1, modal_projection_2,
                physical_component_1, physical_component_2,
                physical_point,
                modal_solution, physical_solution,
                derivation_2, D_formula,
            ),
            run_time=1.0,
        )
        time.set_value(0)

        transition_formula = MathTex(
            r"e^{Dt}=\begin{bmatrix}"
            r"e^{\lambda_1t}&0\\"
            r"0&e^{\lambda_2t}"
            r"\end{bmatrix}",
            r"\qquad ",
            r"e^{At}=Pe^{Dt}P^{-1}",
        ).scale(0.52).to_edge(UP, buff=0.20)
        self.play(FadeTransform(title, transition_formula), run_time=1.3)

        square_scale = 0.45

        modal_rectangle = always_redraw(
            lambda: Polygon(
                z_plane.c2p(0, 0),
                z_plane.c2p(
                    square_scale * np.exp(lambda_1 * time.get_value()), 0
                ),
                z_plane.c2p(
                    square_scale * np.exp(lambda_1 * time.get_value()),
                    square_scale * np.exp(lambda_2 * time.get_value()),
                ),
                z_plane.c2p(
                    0, square_scale * np.exp(lambda_2 * time.get_value())
                ),
                color=YELLOW,
                fill_color=YELLOW,
                fill_opacity=0.12,
                stroke_width=3,
            )
        )

        physical_parallelogram = always_redraw(
            lambda: Polygon(
                x_plane.c2p(0, 0),
                x_plane.c2p(
                    *(square_scale * np.exp(lambda_1 * time.get_value()) * v1)
                ),
                x_plane.c2p(
                    *(
                        square_scale * np.exp(lambda_1 * time.get_value()) * v1
                        + square_scale * np.exp(lambda_2 * time.get_value()) * v2
                    )
                ),
                x_plane.c2p(
                    *(square_scale * np.exp(lambda_2 * time.get_value()) * v2)
                ),
                color=YELLOW,
                fill_color=YELLOW,
                fill_opacity=0.12,
                stroke_width=3,
            )
        )

        modal_side_1 = always_redraw(
            lambda: vector_arrow(
                z_plane,
                np.array([
                    square_scale * np.exp(lambda_1 * time.get_value()), 0
                ]),
                E1_COLOR,
                width=6,
            )
        )
        modal_side_2 = always_redraw(
            lambda: vector_arrow(
                z_plane,
                np.array([
                    0, square_scale * np.exp(lambda_2 * time.get_value())
                ]),
                E2_COLOR,
                width=6,
            )
        )
        physical_side_1 = always_redraw(
            lambda: vector_arrow(
                x_plane,
                square_scale * np.exp(lambda_1 * time.get_value()) * v1,
                E1_COLOR,
                width=6,
            )
        )
        physical_side_2 = always_redraw(
            lambda: vector_arrow(
                x_plane,
                square_scale * np.exp(lambda_2 * time.get_value()) * v2,
                E2_COLOR,
                width=6,
            )
        )

        self.play(
            FadeIn(modal_rectangle, physical_parallelogram),
            GrowArrow(modal_side_1), GrowArrow(modal_side_2),
            GrowArrow(physical_side_1), GrowArrow(physical_side_2),
            run_time=1.4,
        )
        self.play(
            time.animate.set_value(10),
            run_time=12,
            rate_func=linear,
        )
        self.wait(0.8)

        # ============================================================
        # 7. Commutative diagram and conclusion
        # ============================================================
        self.play(
            FadeOut(
                modal_rectangle, physical_parallelogram,
                modal_side_1, modal_side_2,
                physical_side_1, physical_side_2,
                time_display,
            ),
            FadeOut(
                x_plane, z_plane,
                x_labels, z_labels,
                x_title, z_title,
                x_E1, x_E2, z_E1, z_E2,
                x_E1_label, x_E2_label,
                z_E1_label, z_E2_label,
                coordinate_arrow, coordinate_label,
            ),
            run_time=1.2,
        )

        diagram = VGroup(
            MathTex(r"x(0)"),
            MathTex(r"x(t)"),
            MathTex(r"z(0)"),
            MathTex(r"z(t)"),
        )
        diagram[0].move_to(LEFT * 2.6 + UP * 0.8)
        diagram[1].move_to(RIGHT * 2.6 + UP * 0.8)
        diagram[2].move_to(LEFT * 2.6 + DOWN * 1.2)
        diagram[3].move_to(RIGHT * 2.6 + DOWN * 1.2)

        top_arrow = Arrow(
            diagram[0].get_right(), diagram[1].get_left(), buff=0.20
        )
        bottom_arrow = Arrow(
            diagram[2].get_right(), diagram[3].get_left(), buff=0.20
        )
        left_down = Arrow(
            diagram[0].get_bottom(), diagram[2].get_top(), buff=0.16
        )
        right_down = Arrow(
            diagram[1].get_bottom(), diagram[3].get_top(), buff=0.16
        )

        top_label = MathTex(r"e^{At}").scale(0.52).next_to(top_arrow, UP, buff=0.06)
        bottom_label = MathTex(r"e^{Dt}").scale(0.52).next_to(bottom_arrow, UP, buff=0.06)
        left_label = MathTex(r"P^{-1}").scale(0.48).next_to(left_down, LEFT, buff=0.06)
        right_label = MathTex(r"P^{-1}").scale(0.48).next_to(right_down, RIGHT, buff=0.06)

        self.play(FadeIn(diagram), run_time=0.8)
        self.play(
            GrowArrow(top_arrow), GrowArrow(bottom_arrow),
            GrowArrow(left_down), GrowArrow(right_down),
            FadeIn(top_label, bottom_label, left_label, right_label),
            run_time=1.5,
        )

        conclusion = VGroup(
            MathTex(
                r"Av_i=\lambda_i v_i"
                r"\quad\Longrightarrow\quad "
                r"e^{At}v_i=e^{\lambda_i t}v_i"
            ).scale(0.62),
            Tex(
                "eigenvectors determine the invariant directions; "
                "eigenvalues determine the motion along them"
            ).scale(0.46),
        ).arrange(DOWN, buff=0.18).to_edge(DOWN, buff=0.35)

        self.play(Write(conclusion[0]), run_time=1.4)
        self.play(FadeIn(conclusion[1]), run_time=1.0)
        self.wait(3)

