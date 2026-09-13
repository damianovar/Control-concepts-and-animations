"""Animate continuous-time autonomous LTI evolution along one eigenspace.

The animation considers

    x_dot(t) = A x(t)

and an eigenspace span([2, 1]^T) associated with a real, negative eigenvalue.
If x(0) belongs to that eigenspace, then

    x_dot(t) = lambda x(t),
    x(t)     = exp(lambda*t) x(0).

The left plane contains the state, while the right plane contains its velocity.
For lambda < 0 the two vectors are collinear and point in opposite directions;
the state therefore moves continuously toward the origin without leaving the
eigenspace.

Preview render:

    python -m manim -pql continuous_time_eigenspace_manim.py ContinuousTimeAlongEigenspace

High-quality render:

    python -m manim -pqh continuous_time_eigenspace_manim.py ContinuousTimeAlongEigenspace
"""

from manim import *
import numpy as np


# ---------------------------------------------------------------------------
# Parameters that are convenient to change between renders
# ---------------------------------------------------------------------------
EIGENVALUE = -0.55
INITIAL_SCALE = 1.55
FINAL_TIME = 6.0

# The first seconds are deliberately slower, to leave time for explanation.
FIRST_INTERVAL_RUN_TIME = 2.8
SECOND_INTERVAL_RUN_TIME = 2.4
REMAINING_RUN_TIME = 6.5


class ContinuousTimeAlongEigenspace(Scene):
    def construct(self):
        eigenvector = np.array([2.0, 1.0])
        initial_state = INITIAL_SCALE * eigenvector

        def state_at(t):
            return np.exp(EIGENVALUE * t) * initial_state

        def velocity_at(t):
            return EIGENVALUE * state_at(t)

        title = Tex("Continuous-time free evolution along an eigenspace")
        title.scale(0.69).to_edge(UP, buff=0.13)

        system_equation = MathTex(
            r"\dot{\mathbf{x}}(t)=A\mathbf{x}(t)"
        ).scale(0.62)
        system_equation.next_to(title, DOWN, buff=0.09)

        plane_style = {
            "background_line_style": {
                "stroke_color": GREY_B,
                "stroke_width": 1,
                "stroke_opacity": 0.25,
            },
            "axis_config": {
                "stroke_width": 1.7,
                "include_tip": True,
                "tip_width": 0.14,
                "tip_height": 0.14,
                "include_ticks": False,
            },
        }

        state_plane = NumberPlane(
            x_range=[-3.5, 3.5, 1],
            y_range=[-3.5, 3.5, 1],
            x_length=5.0,
            y_length=5.0,
            **plane_style,
        )
        velocity_plane = NumberPlane(
            x_range=[-3.5, 3.5, 1],
            y_range=[-3.5, 3.5, 1],
            x_length=5.0,
            y_length=5.0,
            **plane_style,
        )

        planes = VGroup(state_plane, velocity_plane)
        planes.arrange(RIGHT, buff=1.55).shift(DOWN * 0.68)

        state_axis_labels = VGroup(
            MathTex(r"x_1").scale(0.48).next_to(
                state_plane.x_axis.get_end(), RIGHT, buff=0.03
            ),
            MathTex(r"x_2").scale(0.48).next_to(
                state_plane.y_axis.get_end(), UP, buff=0.03
            ),
        )
        velocity_axis_labels = VGroup(
            MathTex(r"\dot{x}_1").scale(0.48).next_to(
                velocity_plane.x_axis.get_end(), RIGHT, buff=0.03
            ),
            MathTex(r"\dot{x}_2").scale(0.48).next_to(
                velocity_plane.y_axis.get_end(), UP, buff=0.03
            ),
        )

        state_plane_title = MathTex(r"\mathbf{x}(t)").scale(0.57)
        state_plane_title.next_to(state_plane, UP, buff=0.24)
        state_plane_title.align_to(state_plane, LEFT).shift(RIGHT * 0.18)

        velocity_plane_title = MathTex(r"\dot{\mathbf{x}}(t)").scale(0.57)
        velocity_plane_title.next_to(velocity_plane, UP, buff=0.24)
        velocity_plane_title.align_to(velocity_plane, LEFT).shift(RIGHT * 0.18)

        map_arrow = Arrow(
            state_plane.get_right() + RIGHT * 0.10,
            velocity_plane.get_left() + LEFT * 0.10,
            buff=0.09,
            color=WHITE,
            stroke_width=3.0,
            max_tip_length_to_length_ratio=0.18,
        )
        map_label = MathTex(r"A").scale(0.62)
        map_label.next_to(map_arrow, UP, buff=0.06)

        def eigenspace_line(plane):
            return DashedLine(
                plane.c2p(-3.5, -1.75),
                plane.c2p(3.5, 1.75),
                color=GREEN_C,
                stroke_width=2.8,
                dash_length=0.14,
            )

        state_eigenspace = eigenspace_line(state_plane)
        velocity_eigenspace = eigenspace_line(velocity_plane)

        def vector_arrow(plane, vector, color, width=4.2):
            return Arrow(
                plane.c2p(0, 0),
                plane.c2p(vector[0], vector[1]),
                buff=0,
                color=color,
                stroke_width=width,
                max_tip_length_to_length_ratio=0.13,
            )

        def vector_dot(plane, vector, color, radius=0.075):
            return Dot(
                plane.c2p(vector[0], vector[1]),
                radius=radius,
                color=color,
            )

        # ------------------------------------------------------------------
        # 1. Establish the two spaces and the defining eigenvector property.
        # ------------------------------------------------------------------
        self.play(Write(title), Write(system_equation), run_time=1.2)
        self.play(
            Create(state_plane),
            Create(velocity_plane),
            FadeIn(state_axis_labels, velocity_axis_labels),
            FadeIn(state_plane_title, velocity_plane_title),
            GrowArrow(map_arrow),
            FadeIn(map_label),
            run_time=1.8,
        )

        self.play(Create(state_eigenspace), run_time=1.0)
        self.play(Create(velocity_eigenspace), run_time=1.0)

        demonstration_state = eigenvector
        demonstration_velocity = EIGENVALUE * demonstration_state

        demonstration_state_arrow = vector_arrow(
            state_plane, demonstration_state, YELLOW_C
        )
        demonstration_state_dot = vector_dot(
            state_plane, demonstration_state, YELLOW_C
        )
        demonstration_velocity_arrow = vector_arrow(
            velocity_plane, demonstration_velocity, ORANGE
        )
        demonstration_velocity_dot = vector_dot(
            velocity_plane, demonstration_velocity, ORANGE
        )

        state_label = MathTex(r"\mathbf{v}").scale(0.48).set_color(YELLOW_C)
        state_label.next_to(demonstration_state_dot, UR, buff=0.08)

        velocity_label = MathTex(r"\lambda\mathbf{v}").scale(0.48)
        velocity_label.set_color(ORANGE)
        velocity_label.next_to(demonstration_velocity_dot, DL, buff=0.08)

        eigenvector_identity = MathTex(
            r"A\mathbf{v}=\lambda\mathbf{v},",
            rf"\qquad \lambda={EIGENVALUE:.2f}<0",
        ).scale(0.58).to_edge(DOWN, buff=0.14)
        eigenvector_identity[0].set_color(YELLOW_C)

        self.play(
            GrowArrow(demonstration_state_arrow),
            FadeIn(demonstration_state_dot, state_label),
            run_time=1.0,
        )
        self.play(
            TransformFromCopy(
                demonstration_state_arrow,
                demonstration_velocity_arrow,
            ),
            TransformFromCopy(
                demonstration_state_dot,
                demonstration_velocity_dot,
            ),
            FadeIn(velocity_label),
            Write(eigenvector_identity),
            map_arrow.animate.set_color(ORANGE),
            run_time=1.5,
        )
        self.play(map_arrow.animate.set_color(WHITE), run_time=0.30)
        self.wait(0.8)
        self.play(
            FadeOut(
                demonstration_state_arrow,
                demonstration_state_dot,
                demonstration_velocity_arrow,
                demonstration_velocity_dot,
                state_label,
                velocity_label,
                eigenvector_identity,
            ),
            run_time=0.8,
        )

        # ------------------------------------------------------------------
        # 2. Choose x(0), map it to x_dot(0), and expose the direction field.
        # ------------------------------------------------------------------
        initial_velocity = velocity_at(0)

        initial_state_arrow = vector_arrow(state_plane, initial_state, PINK)
        initial_state_dot = vector_dot(
            state_plane, initial_state, PINK, radius=0.095
        )
        initial_velocity_arrow = vector_arrow(
            velocity_plane, initial_velocity, ORANGE
        )
        initial_velocity_dot = vector_dot(
            velocity_plane, initial_velocity, ORANGE, radius=0.075
        )

        status = MathTex(
            r"\mathbf{x}(0)\in E_{\lambda}",
            r"\quad\Longrightarrow\quad",
            r"\dot{\mathbf{x}}(0)=\lambda\mathbf{x}(0)",
        ).scale(0.55).to_edge(DOWN, buff=0.14)
        status[0].set_color(PINK)
        status[2].set_color(ORANGE)

        self.play(
            GrowArrow(initial_state_arrow),
            FadeIn(initial_state_dot),
            Write(status[0]),
            run_time=1.2,
        )
        self.play(
            TransformFromCopy(initial_state_arrow, initial_velocity_arrow),
            TransformFromCopy(initial_state_dot, initial_velocity_dot),
            Write(status[1:]),
            map_arrow.animate.set_color(ORANGE),
            run_time=1.6,
        )
        self.play(map_arrow.animate.set_color(WHITE), run_time=0.30)
        self.wait(0.7)

        # ------------------------------------------------------------------
        # 3. Let time flow continuously.
        # ------------------------------------------------------------------
        time = ValueTracker(0.0)

        moving_state_arrow = always_redraw(
            lambda: vector_arrow(
                state_plane,
                state_at(time.get_value()),
                PINK,
            )
        )
        moving_state_dot = always_redraw(
            lambda: vector_dot(
                state_plane,
                state_at(time.get_value()),
                PINK,
                radius=0.095,
            )
        )

        moving_velocity_arrow = always_redraw(
            lambda: vector_arrow(
                velocity_plane,
                velocity_at(time.get_value()),
                ORANGE,
            )
        )
        moving_velocity_dot = always_redraw(
            lambda: vector_dot(
                velocity_plane,
                velocity_at(time.get_value()),
                ORANGE,
                radius=0.065,
            )
        )

        # The thick segment records the continuously travelled part of the
        # state trajectory.  It overlays the eigenspace only after being
        # traversed, making the direction of time visually explicit.
        travelled_path = always_redraw(
            lambda: Line(
                state_plane.c2p(initial_state[0], initial_state[1]),
                state_plane.c2p(
                    state_at(time.get_value())[0],
                    state_at(time.get_value())[1],
                ),
                color=BLUE_C,
                stroke_width=5.0,
                stroke_opacity=0.75,
            )
        )

        # A local velocity arrow on the state plane links this animation to
        # the preliminary scalar-ODE animation: it always points toward the
        # origin and shrinks as the state approaches equilibrium.
        def local_velocity_arrow():
            current_state = state_at(time.get_value())
            displayed_tip = current_state + 0.62 * velocity_at(time.get_value())
            return Arrow(
                state_plane.c2p(current_state[0], current_state[1]),
                state_plane.c2p(displayed_tip[0], displayed_tip[1]),
                buff=0,
                color=ORANGE,
                stroke_width=3.8,
                max_tip_length_to_length_ratio=0.20,
            )

        moving_local_velocity = always_redraw(local_velocity_arrow)

        time_readout = always_redraw(
            lambda: VGroup(
                MathTex(r"t=").scale(0.52),
                DecimalNumber(
                    time.get_value(),
                    num_decimal_places=1,
                ).scale(0.52),
            )
            .arrange(RIGHT, buff=0.04)
            .next_to(system_equation, DOWN, buff=0.08)
        )

        dynamic_status = MathTex(
            r"\dot{\mathbf{x}}(t)=\lambda\mathbf{x}(t)"
        ).scale(0.58).move_to(status)
        dynamic_status.set_color(ORANGE)

        # Small ghosts make the first two elapsed seconds easy to discuss,
        # while the actual motion between them remains continuous.
        state_ghosts = VGroup(
            vector_dot(state_plane, state_at(0), BLUE_C, radius=0.060)
        )
        velocity_ghosts = VGroup(
            vector_dot(velocity_plane, velocity_at(0), BLUE_C, radius=0.050)
        )
        state_ghosts.set_opacity(0.60)
        velocity_ghosts.set_opacity(0.50)

        self.play(
            FadeOut(
                initial_state_arrow,
                initial_state_dot,
                initial_velocity_arrow,
                initial_velocity_dot,
            ),
            FadeIn(
                travelled_path,
                moving_state_arrow,
                moving_state_dot,
                moving_velocity_arrow,
                moving_velocity_dot,
                moving_local_velocity,
                time_readout,
                state_ghosts,
                velocity_ghosts,
            ),
            Transform(status, dynamic_status),
            run_time=1.0,
        )

        self.play(
            time.animate.set_value(1.0),
            map_arrow.animate.set_color(ORANGE),
            run_time=FIRST_INTERVAL_RUN_TIME,
            rate_func=linear,
        )
        self.play(map_arrow.animate.set_color(WHITE), run_time=0.25)

        first_state_ghost = vector_dot(
            state_plane, state_at(1.0), BLUE_C, radius=0.060
        ).set_opacity(0.60)
        first_velocity_ghost = vector_dot(
            velocity_plane, velocity_at(1.0), BLUE_C, radius=0.050
        ).set_opacity(0.50)
        state_ghosts.add(first_state_ghost)
        velocity_ghosts.add(first_velocity_ghost)
        self.play(
            FadeIn(first_state_ghost, first_velocity_ghost),
            run_time=0.35,
        )

        self.play(
            time.animate.set_value(2.0),
            map_arrow.animate.set_color(ORANGE),
            run_time=SECOND_INTERVAL_RUN_TIME,
            rate_func=linear,
        )
        self.play(map_arrow.animate.set_color(WHITE), run_time=0.25)

        second_state_ghost = vector_dot(
            state_plane, state_at(2.0), BLUE_C, radius=0.055
        ).set_opacity(0.55)
        second_velocity_ghost = vector_dot(
            velocity_plane, velocity_at(2.0), BLUE_C, radius=0.045
        ).set_opacity(0.45)
        state_ghosts.add(second_state_ghost)
        velocity_ghosts.add(second_velocity_ghost)
        self.play(
            FadeIn(second_state_ghost, second_velocity_ghost),
            run_time=0.35,
        )

        self.play(
            time.animate.set_value(FINAL_TIME),
            run_time=REMAINING_RUN_TIME,
            rate_func=linear,
        )

        conclusion = MathTex(
            r"\mathbf{x}(t)=e^{\lambda t}\mathbf{x}(0)",
            r"\longrightarrow",
            r"\mathbf{0}",
            r"\qquad (\lambda<0)",
        ).scale(0.58).move_to(status)
        conclusion[0].set_color(PINK)
        conclusion[2].set_color(YELLOW_C)

        self.play(
            Transform(status, conclusion),
            moving_state_dot.animate.set_color(YELLOW_C),
            run_time=1.2,
        )
        self.wait(2.0)



