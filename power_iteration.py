from manim import *
import numpy as np


class PowerIteration(Scene):
    """Visual introduction to the power iteration method.

    Render with:
        manim -pqh power_iteration.py PowerIteration
    """

    def construct(self):
        # A symmetric matrix: its dominant eigenpair is real and easy to see.
        A = np.array([[3.0, 1.0], [1.0, 2.0]])
        eigenvalues, eigenvectors = np.linalg.eigh(A)
        dominant_index = np.argmax(eigenvalues)
        lam = eigenvalues[dominant_index]
        v = eigenvectors[:, dominant_index]
        if v[0] < 0:
            v = -v

        title = Text("Power iteration", font_size=46, weight=BOLD).to_edge(UP)
        subtitle = Text("Repeated multiplication reveals the dominant eigenvector", font_size=25)
        subtitle.next_to(title, DOWN, buff=0.12)
        self.play(Write(title), FadeIn(subtitle, shift=DOWN))

        matrix = Matrix([[3, 1], [1, 2]], left_bracket="[", right_bracket="]", element_to_mobject_config={"font_size": 36})
        matrix_label = MathTex("A =").scale(0.9)
        matrix_group = VGroup(matrix_label, matrix).arrange(RIGHT, buff=0.18)
        matrix_group.to_corner(UL).shift(DOWN * 1.35 + RIGHT * 0.3)
        self.play(FadeIn(matrix_group, shift=RIGHT))

        plane = NumberPlane(
            x_range=[-2.0, 2.8, 1], y_range=[-1.5, 2.5, 1],
            x_length=6.6, y_length=5.1,
            background_line_style={"stroke_opacity": 0.32},
        ).to_edge(LEFT, buff=0.45).shift(DOWN * 0.55)
        axes_label = MathTex("x_1, x_2").scale(0.55).next_to(plane, DOWN, buff=0.1)
        self.play(Create(plane), FadeIn(axes_label))

        # The eigendirection is shown before the iterations begin.
        eig_line = Line(plane.c2p(-2*v[0], -2*v[1]), plane.c2p(2*v[0], 2*v[1]),
                        color=YELLOW, stroke_width=5, stroke_opacity=0.55)
        eig_label = MathTex(r"\mathrm{span}(v_1)", color=YELLOW).scale(0.7)
        eig_label.next_to(eig_line.get_end(), UP + RIGHT, buff=0.08)
        self.play(Create(eig_line), FadeIn(eig_label))

        formula = MathTex(r"x_{k+1}=\frac{Ax_k}{\|Ax_k\|}").scale(0.95)
        formula.to_corner(UR).shift(DOWN * 1.45 + LEFT * 0.35)
        rayleigh = MathTex(r"\widehat{\lambda}_k = x_k^\top A x_k").scale(0.78)
        rayleigh.next_to(formula, DOWN, aligned_edge=LEFT, buff=0.35)
        self.play(Write(formula), FadeIn(rayleigh, shift=DOWN))

        x = np.array([1.0, -0.65])
        x /= np.linalg.norm(x)
        arrow = Arrow(plane.c2p(0, 0), plane.c2p(*x), buff=0, color=BLUE, stroke_width=7)
        vector_label = MathTex("x_0", color=BLUE).scale(0.75).next_to(arrow.get_end(), RIGHT, buff=0.05)
        self.play(GrowArrow(arrow), FadeIn(vector_label))

        iteration_text = MathTex("k=0").scale(0.85)
        iteration_text.next_to(rayleigh, DOWN, aligned_edge=LEFT, buff=0.4)
        estimate = DecimalNumber(float(x @ A @ x), num_decimal_places=3, font_size=31, color=TEAL)
        estimate_label = MathTex(r"\widehat{\lambda}_0 =").scale(0.72)
        estimate_group = VGroup(estimate_label, estimate).arrange(RIGHT, buff=0.1)
        estimate_group.next_to(iteration_text, DOWN, aligned_edge=LEFT, buff=0.18)
        self.play(Write(iteration_text), FadeIn(estimate_group))

        # A faint trace makes the rotation/convergence visible.
        trace = VGroup()
        for k in range(1, 9):
            y = A @ x
            x_next = y / np.linalg.norm(y)
            raw_arrow = Arrow(plane.c2p(0, 0), plane.c2p(*(0.72 * y / np.linalg.norm(y))),
                              buff=0, color=GRAY_B, stroke_width=3, stroke_opacity=0.65)
            multiply = MathTex(r"Ax_" + str(k-1), color=GRAY_B).scale(0.55)
            multiply.next_to(raw_arrow.get_end(), UP, buff=0.04)
            next_arrow = Arrow(plane.c2p(0, 0), plane.c2p(*x_next), buff=0, color=BLUE, stroke_width=7)
            next_label = MathTex("x_" + str(k), color=BLUE).scale(0.75).next_to(next_arrow.get_end(), RIGHT, buff=0.05)
            next_iteration = MathTex("k=" + str(k)).scale(0.85).move_to(iteration_text)
            next_value = DecimalNumber(float(x_next @ A @ x_next), num_decimal_places=3, font_size=31, color=TEAL)
            next_estimate = VGroup(estimate_label.copy(), next_value).arrange(RIGHT, buff=0.1).move_to(estimate_group)

            self.play(GrowArrow(raw_arrow), FadeIn(multiply), run_time=0.38)
            self.play(
                ReplacementTransform(arrow, next_arrow),
                ReplacementTransform(vector_label, next_label),
                Transform(iteration_text, next_iteration),
                Transform(estimate_group, next_estimate),
                FadeOut(raw_arrow), FadeOut(multiply),
                run_time=0.62,
            )
            trace.add(Dot(next_arrow.get_end(), radius=0.035, color=BLUE_E))
            self.add(trace[-1])
            arrow, vector_label, x = next_arrow, next_label, x_next

        conclusion = VGroup(
            MathTex(r"x_k \longrightarrow v_1", color=YELLOW),
            MathTex(r"\widehat{\lambda}_k \longrightarrow \lambda_1 = " + f"{lam:.3f}", color=TEAL),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).scale(0.85)
        conclusion.to_corner(DR).shift(UP * 0.35 + LEFT * 0.28)
        box = SurroundingRectangle(conclusion, color=WHITE, buff=0.22, corner_radius=0.12)
        self.play(FadeIn(box), Write(conclusion))
        self.wait(2)
