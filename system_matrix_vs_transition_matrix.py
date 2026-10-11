from manim import *
import numpy as np


class SystemMatrixVsTransitionMatrix(Scene):
    def construct(self):
        # ============================================================
        # System definition
        # ============================================================
        # Eigenspaces: span([2,1]) and span([-1,2]).
        # lambda_1 > 0 gives slow divergence.
        # lambda_2 < 0 gives moderate convergence.
        v1 = np.array([2.0, 1.0])
        v1 /= np.linalg.norm(v1)

        v2 = np.array([-1.0, 2.0])
        v2 /= np.linalg.norm(v2)

        lambda_1 = 0.08
        lambda_2 = -0.12

        Q = np.column_stack((v1, v2))
        A = Q @ np.diag([lambda_1, lambda_2]) @ Q.T

        E1_COLOR = TEAL_C
        E2_COLOR = PURPLE_C
        COL1_COLOR = BLUE_C
        COL2_COLOR = ORANGE
        STATE_COLOR = YELLOW

        def phi(t):
            return Q @ np.diag(
                [np.exp(lambda_1 * t), np.exp(lambda_2 * t)]
            ) @ Q.T

        def state(t, x0):
            return phi(t) @ np.asarray(x0, dtype=float)

        def make_plane(center, radius, length=5.2):
            step = radius / 4
            return NumberPlane(
                x_range=[-radius, radius, step],
                y_range=[-radius, radius, step],
                x_length=length,
                y_length=length,
                background_line_style={
                    "stroke_color": GREY_B,
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
            end = start + vector

            if np.linalg.norm(vector) < 1e-9:
                return Dot(
                    plane.c2p(*start),
                    radius=0.001,
                ).set_opacity(0)

            return Arrow(
                plane.c2p(*start),
                plane.c2p(*end),
                buff=0,
                color=color,
                stroke_width=width,
                max_tip_length_to_length_ratio=0.16,
            ).set_opacity(opacity)

        def eigenspace_line(plane, direction, radius, color, opacity=0.75):
            direction = np.asarray(direction, dtype=float)
            scale = radius / np.max(np.abs(direction))
            endpoint = scale * direction
            return Line(
                plane.c2p(*(-endpoint)),
                plane.c2p(*endpoint),
                color=color,
                stroke_width=3,
            ).set_opacity(opacity)

        def time_readout(tracker, corner=UR):
            group = VGroup(
                MathTex("t=").scale(0.52),
                DecimalNumber(
                    tracker.get_value(),
                    num_decimal_places=1,
                ).scale(0.52),
            ).arrange(RIGHT, buff=0.04)
            group.to_corner(corner, buff=0.28).shift(DOWN * 0.55)
            return VGroup(
                SurroundingRectangle(
                    group,
                    color=YELLOW,
                    buff=0.09,
                    stroke_width=2.5,
                ),
                group,
            )

        # ============================================================
        # 1. Two spaces: states and instantaneous velocities
        # ============================================================
        title_A = MathTex(
            r"\dot{x}=Ax",
            r"\qquad",
            r"A:\;x\mapsto\dot{x}",
        ).scale(0.68).to_edge(UP, buff=0.20)
        self.play(Write(title_A), run_time=1.3)

        left_plane = make_plane(LEFT * 3.45 + DOWN * 0.45, 2.0)
        left_labels = plane_labels(left_plane, "x_1", "x_2")

        right_plane = make_plane(RIGHT * 3.45 + DOWN * 0.45, 0.18)
        right_labels = plane_labels(right_plane, r"\dot{x}_1", r"\dot{x}_2")

        left_title = Tex("state space").scale(0.48)
        left_title.next_to(left_plane, UP, buff=0.05)

        right_title = VGroup(
            Tex("velocity space").scale(0.48),
            Tex("magnified scale").scale(0.34).set_color(GREY_B),
        ).arrange(DOWN, buff=0.03)
        right_title.next_to(right_plane, UP, buff=0.03)

        self.play(
            Create(left_plane),
            FadeIn(left_labels, left_title),
            run_time=1.5,
        )
        self.play(
            Create(right_plane),
            FadeIn(right_labels, right_title),
            run_time=1.5,
        )

        map_symbol = MathTex("A").scale(0.68)
        map_arrow = Arrow(
            left_plane.get_right() + RIGHT * 0.10,
            right_plane.get_left() + LEFT * 0.10,
            buff=0.12,
            color=WHITE,
        )
        map_symbol.next_to(map_arrow, UP, buff=0.06)
        self.play(GrowArrow(map_arrow), FadeIn(map_symbol), run_time=0.9)

        # Standard basis vectors and the corresponding columns of A.
        e1 = np.array([1.0, 0.0])
        e2 = np.array([0.0, 1.0])
        a1 = A[:, 0]
        a2 = A[:, 1]

        e1_arrow = vector_arrow(left_plane, e1, COL1_COLOR)
        e2_arrow = vector_arrow(left_plane, e2, COL2_COLOR)
        e1_label = MathTex(r"e_1").scale(0.48).set_color(COL1_COLOR)
        e2_label = MathTex(r"e_2").scale(0.48).set_color(COL2_COLOR)
        e1_label.next_to(e1_arrow.get_end(), DR, buff=0.05)
        e2_label.next_to(e2_arrow.get_end(), UL, buff=0.05)

        self.play(
            GrowArrow(e1_arrow),
            GrowArrow(e2_arrow),
            FadeIn(e1_label, e2_label),
            run_time=1.3,
        )

        a1_arrow = vector_arrow(right_plane, a1, COL1_COLOR)
        a2_arrow = vector_arrow(right_plane, a2, COL2_COLOR)
        a1_label = MathTex(r"a_1=Ae_1").scale(0.42).set_color(COL1_COLOR)
        a2_label = MathTex(r"a_2=Ae_2").scale(0.42).set_color(COL2_COLOR)
        a1_label.next_to(a1_arrow.get_end(), UR, buff=0.04)
        a2_label.next_to(a2_arrow.get_end(), DR, buff=0.04)

        self.play(
            TransformFromCopy(e1_arrow, a1_arrow),
            TransformFromCopy(e2_arrow, a2_arrow),
            FadeIn(a1_label, a2_label),
            run_time=1.5,
        )

        # ============================================================
        # 2. Eigenspaces are invariant directions of A
        # ============================================================
        left_E1 = eigenspace_line(left_plane, v1, 2.0, E1_COLOR)
        left_E2 = eigenspace_line(left_plane, v2, 2.0, E2_COLOR)
        right_E1 = eigenspace_line(right_plane, v1, 0.18, E1_COLOR)
        right_E2 = eigenspace_line(right_plane, v2, 0.18, E2_COLOR)

        left_E1_label = MathTex(r"E_{\lambda_1}").scale(0.40).set_color(E1_COLOR)
        left_E2_label = MathTex(r"E_{\lambda_2}").scale(0.40).set_color(E2_COLOR)
        left_E1_label.move_to(left_plane.c2p(1.40, 0.86))
        left_E2_label.move_to(left_plane.c2p(-0.90, 1.60))

        eigenvalue_labels = VGroup(
            MathTex(r"\lambda_1=0.08>0").scale(0.43).set_color(E1_COLOR),
            MathTex(r"\lambda_2=-0.12<0").scale(0.43).set_color(E2_COLOR),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.10)
        eigenvalue_labels.to_corner(DR, buff=0.22)

        self.play(
            Create(left_E1), Create(right_E1),
            FadeIn(left_E1_label),
            run_time=1.0,
        )
        self.play(
            Create(left_E2), Create(right_E2),
            FadeIn(left_E2_label),
            FadeIn(eigenvalue_labels),
            run_time=1.0,
        )
        self.wait(0.6)

        self.play(
            FadeOut(e1_arrow, e2_arrow, e1_label, e2_label),
            FadeOut(a1_arrow, a2_arrow, a1_label, a2_label),
            run_time=0.9,
        )

        # ============================================================
        # 3. Move x0 and display Ax0 in both spaces
        # ============================================================
        theta = ValueTracker(-0.35)
        circle_radius = 1.32
        velocity_gain = 4.0

        def current_x0():
            return circle_radius * np.array([
                np.cos(theta.get_value()),
                np.sin(theta.get_value()),
            ])

        orbit = Circle(
            radius=left_plane.x_axis.get_unit_size() * circle_radius,
            color=GREY_B,
            stroke_width=1.5,
            stroke_opacity=0.42,
        ).move_to(left_plane.c2p(0, 0))

        x0_dot = always_redraw(
            lambda: Dot(
                left_plane.c2p(*current_x0()),
                radius=0.075,
                color=STATE_COLOR,
            )
        )
        x0_label = always_redraw(
            lambda: MathTex(r"x_0").scale(0.43).set_color(STATE_COLOR).next_to(
                x0_dot, UR, buff=0.04
            )
        )
        Ax_right = always_redraw(
            lambda: vector_arrow(
                right_plane,
                A @ current_x0(),
                STATE_COLOR,
                width=7,
            )
        )
        Ax_right_label = always_redraw(
            lambda: MathTex(r"Ax_0").scale(0.42).set_color(STATE_COLOR).next_to(
                Ax_right.get_end(), UR, buff=0.04
            )
        )
        velocity_left = always_redraw(
            lambda: vector_arrow(
                left_plane,
                velocity_gain * (A @ current_x0()),
                STATE_COLOR,
                start=current_x0(),
                width=6,
            )
        )

        velocity_caption = Tex(
            "instantaneous velocity (magnified)"
        ).scale(0.43).to_corner(DL, buff=0.22).shift(UP * 0.20)

        self.play(Create(orbit), FadeIn(x0_dot, x0_label), run_time=1.0)
        self.play(GrowArrow(Ax_right), FadeIn(Ax_right_label), run_time=1.0)
        self.play(GrowArrow(velocity_left), FadeIn(velocity_caption), run_time=1.0)

        angle_v1 = np.arctan2(v1[1], v1[0])
        angle_v2 = np.arctan2(v2[1], v2[0])

        self.play(theta.animate.set_value(angle_v1), run_time=2.5, rate_func=smooth)
        eigen_relation_1 = MathTex(r"Ax_0=\lambda_1x_0").scale(0.55).set_color(E1_COLOR)
        eigen_relation_1.next_to(title_A, DOWN, buff=0.12)
        self.play(Indicate(left_E1, color=E1_COLOR), FadeIn(eigen_relation_1), run_time=1.0)
        self.wait(0.8)
        self.play(FadeOut(eigen_relation_1), run_time=0.4)

        self.play(theta.animate.set_value(angle_v2), run_time=3.0, rate_func=smooth)
        eigen_relation_2 = MathTex(r"Ax_0=\lambda_2x_0").scale(0.55).set_color(E2_COLOR)
        eigen_relation_2.next_to(title_A, DOWN, buff=0.12)
        self.play(Indicate(left_E2, color=E2_COLOR), FadeIn(eigen_relation_2), run_time=1.0)
        self.wait(0.8)
        self.play(FadeOut(eigen_relation_2), run_time=0.4)

        self.play(
            theta.animate.set_value(2 * PI - 0.35),
            run_time=7.0,
            rate_func=linear,
        )
        self.wait(0.6)

        # ============================================================
        # 4. Focus on state space
        # ============================================================
        self.play(
            FadeOut(x0_dot, x0_label, Ax_right, Ax_right_label, velocity_left),
            FadeOut(orbit, velocity_caption),
            FadeOut(right_plane, right_labels, right_title, right_E1, right_E2),
            FadeOut(map_arrow, map_symbol, eigenvalue_labels),
            run_time=1.2,
        )

        focus_plane = make_plane(DOWN * 0.35, 2.8, length=6.6)
        focus_labels = plane_labels(focus_plane, "x_1", "x_2")
        focus_E1 = eigenspace_line(focus_plane, v1, 2.8, E1_COLOR, 0.60)
        focus_E2 = eigenspace_line(focus_plane, v2, 2.8, E2_COLOR, 0.60)
        focus_E1_label = MathTex(r"E_{\lambda_1}").scale(0.43).set_color(E1_COLOR)
        focus_E2_label = MathTex(r"E_{\lambda_2}").scale(0.43).set_color(E2_COLOR)
        focus_E1_label.move_to(focus_plane.c2p(1.85, 1.15))
        focus_E2_label.move_to(focus_plane.c2p(-1.05, 2.10))

        self.play(
            ReplacementTransform(left_plane, focus_plane),
            ReplacementTransform(left_labels, focus_labels),
            ReplacementTransform(left_E1, focus_E1),
            ReplacementTransform(left_E2, focus_E2),
            ReplacementTransform(left_E1_label, focus_E1_label),
            ReplacementTransform(left_E2_label, focus_E2_label),
            FadeOut(left_title),
            run_time=1.6,
        )
        plane = focus_plane

        # ============================================================
        # 5. From infinitesimal updates to a finite-time map
        # ============================================================
        bridge_1 = MathTex(
            r"x(t+\Delta t)\approx(I+A\Delta t)x(t)"
        ).scale(0.62).to_edge(UP, buff=0.24)
        self.play(FadeTransform(title_A, bridge_1), run_time=1.2)

        bridge_x0 = np.array([0.85, -1.15])
        dt = 1.0
        steps = 10
        Euler_matrix = np.eye(2) + A * dt
        Euler_points = [bridge_x0]
        for _ in range(steps):
            Euler_points.append(Euler_matrix @ Euler_points[-1])

        step_dots = VGroup(
            *[
                Dot(plane.c2p(*p), radius=0.045, color=STATE_COLOR)
                for p in Euler_points
            ]
        )
        step_segments = VGroup(
            *[
                Line(
                    plane.c2p(*Euler_points[k]),
                    plane.c2p(*Euler_points[k + 1]),
                    color=STATE_COLOR,
                    stroke_width=3,
                )
                for k in range(steps)
            ]
        )

        self.play(FadeIn(step_dots[0]), run_time=0.4)
        self.play(
            LaggedStart(
                *[
                    AnimationGroup(
                        Create(step_segments[k]),
                        FadeIn(step_dots[k + 1]),
                    )
                    for k in range(steps)
                ],
                lag_ratio=0.15,
            ),
            run_time=4.0,
        )

        bridge_2 = MathTex(
            r"\left(I+A\frac{t}{n}\right)^n"
            r"\longrightarrow e^{At}"
        ).scale(0.66).move_to(bridge_1)
        exact_curve = ParametricFunction(
            lambda tau: plane.c2p(*state(tau, bridge_x0)),
            t_range=[0, 10, 0.04],
            color=YELLOW,
            stroke_width=5,
        )
        self.play(FadeTransform(bridge_1, bridge_2), run_time=1.2)
        self.play(
            FadeOut(step_segments, step_dots),
            Create(exact_curve),
            run_time=2.2,
        )
        self.wait(0.6)
        self.play(FadeOut(exact_curve), run_time=0.6)

        # ============================================================
        # 6. Columns of e^(At) and deformation of the unit square
        # ============================================================
        flow_title = MathTex(
            r"e^{At}:\;x(0)\mapsto x(t)"
        ).scale(0.68).move_to(bridge_2)
        self.play(FadeTransform(bridge_2, flow_title), run_time=1.1)

        t = ValueTracker(0.0)

        column_1 = always_redraw(
            lambda: vector_arrow(
                plane,
                phi(t.get_value()) @ e1,
                COL1_COLOR,
                width=7,
            )
        )
        column_2 = always_redraw(
            lambda: vector_arrow(
                plane,
                phi(t.get_value()) @ e2,
                COL2_COLOR,
                width=7,
            )
        )
        column_1_label = always_redraw(
            lambda: MathTex(r"e^{At}e_1").scale(0.43).set_color(COL1_COLOR).next_to(
                column_1.get_end(), UR, buff=0.04
            )
        )
        column_2_label = always_redraw(
            lambda: MathTex(r"e^{At}e_2").scale(0.43).set_color(COL2_COLOR).next_to(
                column_2.get_end(), UR, buff=0.04
            )
        )
        image_square = always_redraw(
            lambda: Polygon(
                plane.c2p(0, 0),
                plane.c2p(*(phi(t.get_value()) @ e1)),
                plane.c2p(*(phi(t.get_value()) @ (e1 + e2))),
                plane.c2p(*(phi(t.get_value()) @ e2)),
                color=YELLOW,
                fill_color=YELLOW,
                fill_opacity=0.10,
                stroke_width=2.5,
            )
        )
        t_display = always_redraw(lambda: time_readout(t))

        self.play(
            FadeIn(image_square),
            GrowArrow(column_1), GrowArrow(column_2),
            FadeIn(column_1_label, column_2_label, t_display),
            run_time=1.4,
        )
        self.play(t.animate.set_value(10), run_time=12, rate_func=linear)
        self.wait(0.7)
        self.play(t.animate.set_value(0), run_time=7, rate_func=smooth)
        self.wait(0.7)

        # ============================================================
        # 7. Use the two columns to move a generic initial condition
        # ============================================================
        x_initial = np.array([0.95, 0.65])
        x_initial_dot = Dot(
            plane.c2p(*x_initial),
            radius=0.075,
            color=STATE_COLOR,
        )
        x_initial_label = MathTex(r"x(0)").scale(0.44).set_color(STATE_COLOR)
        x_initial_label.next_to(x_initial_dot, UR, buff=0.04)

        solution_formula = MathTex(
            r"x(t)=e^{At}x(0)"
        ).scale(0.60).to_corner(DR, buff=0.28).shift(UP * 0.20)

        component_1 = always_redraw(
            lambda: vector_arrow(
                plane,
                x_initial[0] * (phi(t.get_value()) @ e1),
                COL1_COLOR,
                width=5,
            )
        )
        component_2 = always_redraw(
            lambda: vector_arrow(
                plane,
                x_initial[1] * (phi(t.get_value()) @ e2),
                COL2_COLOR,
                start=x_initial[0] * (phi(t.get_value()) @ e1),
                width=5,
            )
        )
        moving_state = always_redraw(
            lambda: Dot(
                plane.c2p(*state(t.get_value(), x_initial)),
                radius=0.075,
                color=STATE_COLOR,
            )
        )

        self.play(
            FadeIn(x_initial_dot, x_initial_label),
            Write(solution_formula),
            run_time=1.0,
        )
        self.play(
            GrowArrow(component_1),
            GrowArrow(component_2),
            FadeIn(moving_state),
            run_time=1.2,
        )
        self.play(t.animate.set_value(10), run_time=10, rate_func=linear)
        self.wait(0.8)

        self.play(
            FadeOut(column_1, column_2, column_1_label, column_2_label),
            FadeOut(image_square, component_1, component_2),
            FadeOut(moving_state, x_initial_dot, x_initial_label),
            FadeOut(solution_formula),
            run_time=1.0,
        )
        t.set_value(0)

        # ============================================================
        # 8. A second initial condition: show its complete trajectory
        # ============================================================
        second_x0 = np.array([-0.70, 1.05])
        second_dot = Dot(
            plane.c2p(*second_x0),
            radius=0.075,
            color=STATE_COLOR,
        )
        second_curve = ParametricFunction(
            lambda tau: plane.c2p(*state(tau, second_x0)),
            t_range=[0, 10, 0.035],
            color=STATE_COLOR,
            stroke_width=5,
        )
        moving_second = always_redraw(
            lambda: Dot(
                plane.c2p(*state(t.get_value(), second_x0)),
                radius=0.075,
                color=STATE_COLOR,
            )
        )

        self.play(FadeIn(second_dot), run_time=0.6)
        self.play(
            Create(second_curve),
            FadeIn(moving_second),
            t.animate.set_value(10),
            run_time=10,
            rate_func=linear,
        )
        self.wait(0.8)
        self.play(FadeOut(second_curve, second_dot, moving_second), run_time=0.8)
        t.set_value(0)
        self.play(FadeOut(t_display), run_time=0.5)

        # ============================================================
        # 9. Family of trajectories: the phase portrait
        # ============================================================
        initial_conditions = []
        for radius in [0.48, 0.85, 1.18]:
            for angle in np.linspace(0, 2 * PI, 8, endpoint=False):
                initial_conditions.append(
                    radius * np.array([np.cos(angle), np.sin(angle)])
                )

        initial_dots = VGroup(
            *[
                Dot(
                    plane.c2p(*x0),
                    radius=0.035,
                    color=GREY_A,
                )
                for x0 in initial_conditions
            ]
        )

        family_curves = VGroup(
            *[
                ParametricFunction(
                    lambda tau, x0=x0: plane.c2p(*state(tau, x0)),
                    t_range=[0, 10, 0.05],
                    color=BLUE_B,
                    stroke_width=2.0,
                    stroke_opacity=0.55,
                )
                for x0 in initial_conditions
            ]
        )

        unstable_curve = ParametricFunction(
            lambda tau: plane.c2p(*state(tau, 0.72 * v1)),
            t_range=[0, 10, 0.04],
            color=E1_COLOR,
            stroke_width=5,
        )
        stable_curve = ParametricFunction(
            lambda tau: plane.c2p(*state(tau, 1.30 * v2)),
            t_range=[0, 10, 0.04],
            color=E2_COLOR,
            stroke_width=5,
        )

        portrait_title = Tex(
            "the flow generated by the same matrix $A$"
        ).scale(0.50).to_corner(DR, buff=0.28).shift(UP * 0.18)

        self.play(FadeIn(initial_dots), FadeIn(portrait_title), run_time=1.0)
        self.play(
            AnimationGroup(
                *[Create(curve) for curve in family_curves],
                lag_ratio=0.02,
            ),
            Create(unstable_curve),
            Create(stable_curve),
            run_time=11,
            rate_func=linear,
        )
        self.wait(3)

