from manim import *
import numpy as np
from math import factorial


class MatrixExponentialTaylor(Scene):
    def construct(self):
        # ============================================================
        # Numerical example
        # ============================================================
        v1 = np.array([2.0, 1.0])
        v1 /= np.linalg.norm(v1)

        v2 = np.array([-1.0, 2.0])
        v2 /= np.linalg.norm(v2)

        lambda_1 = 0.8
        lambda_2 = -0.6

        Q = np.column_stack((v1, v2))
        A = Q @ np.diag([lambda_1, lambda_2]) @ Q.T

        number_of_terms = 7  # T_0,...,T_6

        powers = [
            np.linalg.matrix_power(A, k)
            for k in range(number_of_terms)
        ]

        terms = [
            powers[k] / factorial(k)
            for k in range(number_of_terms)
        ]

        approximation = sum(terms)

        # ============================================================
        # Helpers
        # ============================================================
        def fraction(numerator, denominator, scale=1.0):
            """
            Construct a fraction explicitly.

            This avoids relying on get_parts_by_tex(), whose behavior
            changed in recent Manim versions.
            """
            num = MathTex(numerator).scale(scale)
            den = MathTex(denominator).scale(scale)

            width = max(num.width, den.width) + 0.10

            bar = Line(
                LEFT * width / 2,
                RIGHT * width / 2,
                stroke_width=2,
            )

            frac = VGroup(
                num,
                bar,
                den,
            ).arrange(
                DOWN,
                buff=0.035,
            )

            return frac, num, den

        def plus(scale=1.0):
            return MathTex("+").scale(scale)

        def make_definition(
            symbol=r"\star",
            simplified=False,
            scale=0.82,
        ):
            lhs = MathTex(
                rf"e^{{{symbol}}}",
                r":=",
            ).scale(scale)

            if simplified:
                t0 = MathTex(rf"{symbol}^0").scale(scale)
                t1 = MathTex(rf"{symbol}^1").scale(scale)

                n0 = t0
                n1 = t1
                d0 = None
                d1 = None

            else:
                t0, n0, d0 = fraction(
                    rf"{symbol}^0",
                    "0!",
                    scale,
                )

                t1, n1, d1 = fraction(
                    rf"{symbol}^1",
                    "1!",
                    scale,
                )

            t2, n2, d2 = fraction(
                rf"{symbol}^2",
                "2!",
                scale,
            )

            t3, n3, d3 = fraction(
                rf"{symbol}^3",
                "3!",
                scale,
            )

            dots = MathTex(r"+\cdots").scale(scale)

            formula = VGroup(
                lhs,
                t0,
                plus(scale),
                t1,
                plus(scale),
                t2,
                plus(scale),
                t3,
                dots,
            ).arrange(
                RIGHT,
                buff=0.13,
            )

            data = {
                "lhs": lhs,
                "terms": [t0, t1, t2, t3],
                "numerators": [n0, n1, n2, n3],
                "denominators": [d0, d1, d2, d3],
                "dots": dots,
            }

            return formula, data

        def make_matrix_series(scale=0.70):
            lhs = MathTex(
                r"e^A",
                r":=",
            ).scale(scale)

            t0 = MathTex("I").scale(scale)
            t1 = MathTex("A").scale(scale)

            t2, n2, d2 = fraction(
                r"A^2",
                "2!",
                scale,
            )

            t3, n3, d3 = fraction(
                r"A^3",
                "3!",
                scale,
            )

            dots = MathTex(r"+\cdots").scale(scale)

            formula = VGroup(
                lhs,
                t0,
                plus(scale),
                t1,
                plus(scale),
                t2,
                plus(scale),
                t3,
                dots,
            ).arrange(
                RIGHT,
                buff=0.12,
            )

            data = {
                "lhs": lhs,
                "terms": [t0, t1, t2, t3],
                "numerators": [t0, t1, n2, n3],
                "denominators": [None, None, d2, d3],
                "dots": dots,
            }

            return formula, data

        def box(mobject, color=YELLOW, buff=0.055):
            return SurroundingRectangle(
                mobject,
                color=color,
                buff=buff,
                stroke_width=3,
            )

        def arrow_from_vector(
            plane,
            vector,
            color,
            width=5,
            opacity=1.0,
        ):
            arrow = Arrow(
                plane.c2p(0, 0),
                plane.c2p(
                    float(vector[0]),
                    float(vector[1]),
                ),
                buff=0,
                color=color,
                stroke_width=width,
                max_tip_length_to_length_ratio=0.18,
            )

            arrow.set_opacity(opacity)
            return arrow

        def arrow_between(
            plane,
            start,
            end,
            color,
            width=5,
        ):
            return Arrow(
                plane.c2p(
                    float(start[0]),
                    float(start[1]),
                ),
                plane.c2p(
                    float(end[0]),
                    float(end[1]),
                ),
                buff=0,
                color=color,
                stroke_width=width,
                max_tip_length_to_length_ratio=0.18,
            )

        def term_caption(k, anchor):
            caption = MathTex(
                rf"T_{k}=\frac{{A^{k}}}{{{k}!}}"
            ).scale(0.50)

            caption.next_to(
                anchor,
                RIGHT,
                buff=0.35,
            )

            caption.align_to(anchor, UP)
            return caption

        # ============================================================
        # 1. Definition of the exponential
        # ============================================================
        definition, definition_data = make_definition()

        definition.to_edge(
            UP,
            buff=0.40,
        )

        self.play(
            Write(definition),
            run_time=2.0,
        )

        self.wait(0.5)

        factorial_facts = VGroup(
            MathTex("0!=1"),
            MathTex("1!=1"),
        ).arrange(
            RIGHT,
            buff=1.10,
        ).next_to(
            definition,
            DOWN,
            buff=0.65,
        )

        denominator_boxes = VGroup(
            box(definition_data["denominators"][0]),
            box(definition_data["denominators"][1]),
        )

        self.play(
            FadeIn(
                factorial_facts,
                shift=UP * 0.10,
            ),
            Create(denominator_boxes[0]),
            Create(denominator_boxes[1]),
            run_time=1.5,
        )

        self.wait(1.0)

        simplified_stars, simplified_star_data = make_definition(
            simplified=True,
        )

        simplified_stars.move_to(definition)

        self.play(
            FadeOut(factorial_facts),
            FadeOut(denominator_boxes),
            FadeTransform(
                definition,
                simplified_stars,
            ),
            run_time=1.6,
        )

        definition = simplified_stars

        # ------------------------------------------------------------
        # Show A before replacing the stars
        # ------------------------------------------------------------
        A_formula = MathTex(
            r"A="
            r"\begin{bmatrix}"
            r"0.52&0.56\\"
            r"0.56&-0.32"
            r"\end{bmatrix}"
        ).scale(0.78)

        A_formula.next_to(
            definition,
            DOWN,
            buff=0.55,
        )

        self.play(
            Write(A_formula),
            run_time=1.4,
        )

        self.wait(0.7)

        star_boxes = VGroup(
            box(simplified_star_data["numerators"][0]),
            box(simplified_star_data["numerators"][1]),
            box(simplified_star_data["numerators"][2]),
            box(simplified_star_data["numerators"][3]),
        )

        self.play(
            AnimationGroup(
                Create(star_boxes[0]),
                Create(star_boxes[1]),
                Create(star_boxes[2]),
                Create(star_boxes[3]),
                lag_ratio=0.12,
            ),
            run_time=1.4,
        )

        self.wait(0.7)

        definition_A, definition_A_data = make_definition(
            symbol="A",
            simplified=True,
        )

        definition_A.move_to(definition)

        self.play(
            FadeOut(star_boxes),
            FadeTransform(
                definition,
                definition_A,
            ),
            run_time=1.7,
        )

        definition = definition_A

        self.wait(0.5)

        # ------------------------------------------------------------
        # A^0 = I
        # ------------------------------------------------------------
        A0_fact = MathTex(
            r"A^0=I"
        ).scale(0.82)

        A0_fact.move_to(A_formula)

        self.play(
            FadeTransform(
                A_formula,
                A0_fact,
            ),
            run_time=1.2,
        )

        self.wait(0.9)

        series_formula, series_data = make_matrix_series()

        series_formula.to_edge(
            UP,
            buff=0.34,
        ).shift(
            LEFT * 1.20
        )

        self.play(
            FadeOut(A0_fact),
            FadeTransform(
                definition,
                series_formula,
            ),
            run_time=1.7,
        )

        self.wait(0.5)

        # ============================================================
        # 2. Taylor terms as columns in a Cartesian plane
        # ============================================================
        plane = NumberPlane(
            x_range=[-2.5, 2.8, 0.5],
            y_range=[-1.8, 2.3, 0.5],
            x_length=6.4,
            y_length=4.9,
            background_line_style={
                "stroke_color": GREY_B,
                "stroke_opacity": 0.28,
                "stroke_width": 1,
            },
            axis_config={
                "include_numbers": False,
                "include_ticks": False,
                "stroke_width": 2,
            },
        ).shift(
            DOWN * 1.22
            + LEFT * 0.25
        )

        x_label = MathTex(
            "x_1"
        ).scale(0.55)

        x_label.next_to(
            plane.x_axis.get_end(),
            RIGHT,
            buff=0.08,
        )

        y_label = MathTex(
            "x_2"
        ).scale(0.55)

        y_label.next_to(
            plane.y_axis.get_end(),
            UP,
            buff=0.08,
        )

        first_legend = VGroup(
            Line(
                LEFT * 0.22,
                RIGHT * 0.22,
                color=BLUE_C,
                stroke_width=5,
            ),
            Tex("first column").scale(0.43),
        ).arrange(
            RIGHT,
            buff=0.10,
        )

        second_legend = VGroup(
            Line(
                LEFT * 0.22,
                RIGHT * 0.22,
                color=ORANGE,
                stroke_width=5,
            ),
            Tex("second column").scale(0.43),
        ).arrange(
            RIGHT,
            buff=0.10,
        )

        legend = VGroup(
            first_legend,
            second_legend,
        ).arrange(
            DOWN,
            aligned_edge=LEFT,
            buff=0.10,
        )

        legend.to_corner(
            DL,
            buff=0.28,
        )

        self.play(
            Create(plane),
            FadeIn(x_label),
            FadeIn(y_label),
            FadeIn(legend),
            run_time=1.8,
        )

        first_column_arrows = []
        second_column_arrows = []

        # ------------------------------------------------------------
        # T_0 = I and T_1 = A
        # ------------------------------------------------------------
        for k in [0, 1]:
            highlight = box(
                series_data["terms"][k]
            )

            first = arrow_from_vector(
                plane,
                terms[k][:, 0],
                BLUE_C,
            )

            second = arrow_from_vector(
                plane,
                terms[k][:, 1],
                ORANGE,
            )

            self.play(
                Create(highlight),
                run_time=0.45,
            )

            self.play(
                GrowArrow(first),
                GrowArrow(second),
                run_time=1.15,
            )

            self.play(
                FadeOut(highlight),
                run_time=0.35,
            )

            first_column_arrows.append(first)
            second_column_arrows.append(second)

        # ------------------------------------------------------------
        # T_2 and T_3:
        # show A^k first, then divide by k!
        # ------------------------------------------------------------
        for k in [2, 3]:
            numerator_highlight = box(
                series_data["numerators"][k]
            )

            raw_first = arrow_from_vector(
                plane,
                powers[k][:, 0],
                BLUE_C,
            )

            raw_second = arrow_from_vector(
                plane,
                powers[k][:, 1],
                ORANGE,
            )

            self.play(
                Create(numerator_highlight),
                run_time=0.45,
            )

            self.play(
                GrowArrow(raw_first),
                GrowArrow(raw_second),
                run_time=1.05,
            )

            denominator_highlight = box(
                series_data["denominators"][k],
                color=YELLOW,
            )

            scaled_first = arrow_from_vector(
                plane,
                terms[k][:, 0],
                BLUE_C,
            )

            scaled_second = arrow_from_vector(
                plane,
                terms[k][:, 1],
                ORANGE,
            )

            self.play(
                ReplacementTransform(
                    numerator_highlight,
                    denominator_highlight,
                ),
                Transform(
                    raw_first,
                    scaled_first,
                ),
                Transform(
                    raw_second,
                    scaled_second,
                ),
                run_time=1.25,
            )

            self.play(
                FadeOut(denominator_highlight),
                run_time=0.35,
            )

            first_column_arrows.append(raw_first)
            second_column_arrows.append(raw_second)

        # ------------------------------------------------------------
        # Terms hidden inside the ellipsis
        # ------------------------------------------------------------
        tail_highlight = box(
            series_data["dots"]
        )

        self.play(
            Create(tail_highlight),
            run_time=0.5,
        )

        current_caption = None

        for k in range(4, number_of_terms):
            new_caption = term_caption(
                k,
                series_formula,
            )

            first = arrow_from_vector(
                plane,
                terms[k][:, 0],
                BLUE_C,
            )

            second = arrow_from_vector(
                plane,
                terms[k][:, 1],
                ORANGE,
            )

            if current_caption is None:
                self.play(
                    FadeIn(
                        new_caption,
                        shift=LEFT * 0.10,
                    ),
                    run_time=0.55,
                )

            else:
                self.play(
                    FadeTransform(
                        current_caption,
                        new_caption,
                    ),
                    run_time=0.55,
                )

            self.play(
                GrowArrow(first),
                GrowArrow(second),
                run_time=0.85,
            )

            current_caption = new_caption

            first_column_arrows.append(first)
            second_column_arrows.append(second)

        # The terms inside the ellipsis have now been explained.
        self.play(
            FadeOut(tail_highlight),
            FadeOut(current_caption),
            run_time=0.65,
        )

        self.wait(0.6)

        # ============================================================
        # 3. Add the first columns head-to-tail
        # ============================================================
        first_caption = Tex(
            r"first column of $e^A$"
        ).scale(0.52)

        first_caption.next_to(
            series_formula,
            RIGHT,
            buff=0.35,
        ).align_to(
            series_formula,
            UP,
        )

        self.play(
            FadeIn(first_caption),
            *[
                arrow.animate.set_opacity(0.12)
                for arrow in second_column_arrows
            ],
            run_time=1.0,
        )

        cumulative = np.zeros(2)
        first_chain_targets = []

        for k in range(number_of_terms):
            new_cumulative = (
                cumulative
                + terms[k][:, 0]
            )

            target = arrow_between(
                plane,
                cumulative,
                new_cumulative,
                BLUE_C,
            )

            first_chain_targets.append(target)
            cumulative = new_cumulative

        self.play(
            AnimationGroup(
                *[
                    Transform(
                        first_column_arrows[k],
                        first_chain_targets[k],
                    )
                    for k in range(number_of_terms)
                ],
                lag_ratio=0.18,
            ),
            run_time=3.0,
        )

        first_result = arrow_from_vector(
            plane,
            approximation[:, 0],
            YELLOW,
            width=7,
        )

        self.play(
            GrowArrow(first_result),
            run_time=1.2,
        )

        self.wait(0.7)

        first_matrix = MathTex(
            r"e^A\approx"
            r"\begin{bmatrix}"
            rf"{approximation[0, 0]:.2f}"
            r"&\phantom{0.00}\\"
            rf"{approximation[1, 0]:.2f}"
            r"&\phantom{0.00}"
            r"\end{bmatrix}"
        ).scale(0.56)

        first_matrix.next_to(
            series_formula,
            RIGHT,
            buff=0.28,
        ).align_to(
            series_formula,
            UP,
        )

        self.play(
            FadeOut(first_caption),
            FadeIn(first_matrix),
            *[
                FadeOut(arrow)
                for arrow in first_column_arrows
            ],
            FadeOut(first_result),
            run_time=1.2,
        )

        # ============================================================
        # 4. Add the second columns head-to-tail
        # ============================================================
        second_caption = Tex(
            r"second column of $e^A$"
        ).scale(0.52)

        second_caption.next_to(
            series_formula,
            RIGHT,
            buff=0.35,
        ).align_to(
            series_formula,
            UP,
        )

        self.play(
            FadeOut(first_matrix),
            FadeIn(second_caption),
            *[
                arrow.animate.set_opacity(1.0)
                for arrow in second_column_arrows
            ],
            run_time=1.0,
        )

        cumulative = np.zeros(2)
        second_chain_targets = []

        for k in range(number_of_terms):
            new_cumulative = (
                cumulative
                + terms[k][:, 1]
            )

            target = arrow_between(
                plane,
                cumulative,
                new_cumulative,
                ORANGE,
            )

            second_chain_targets.append(target)
            cumulative = new_cumulative

        self.play(
            AnimationGroup(
                *[
                    Transform(
                        second_column_arrows[k],
                        second_chain_targets[k],
                    )
                    for k in range(number_of_terms)
                ],
                lag_ratio=0.18,
            ),
            run_time=3.0,
        )

        second_result = arrow_from_vector(
            plane,
            approximation[:, 1],
            YELLOW,
            width=7,
        )

        self.play(
            GrowArrow(second_result),
            run_time=1.2,
        )

        self.wait(0.7)

        complete_matrix = MathTex(
            r"e^A\approx"
            r"\begin{bmatrix}"
            rf"{approximation[0, 0]:.2f}"
            rf"&{approximation[0, 1]:.2f}\\"
            rf"{approximation[1, 0]:.2f}"
            rf"&{approximation[1, 1]:.2f}"
            r"\end{bmatrix}"
        ).scale(0.58)

        complete_matrix.next_to(
            series_formula,
            RIGHT,
            buff=0.28,
        ).align_to(
            series_formula,
            UP,
        )

        self.play(
            FadeOut(second_caption),
            FadeIn(complete_matrix),
            *[
                FadeOut(arrow)
                for arrow in second_column_arrows
            ],
            FadeOut(second_result),
            run_time=1.2,
        )

        self.wait(1.4)

        # ============================================================
        # 5. Why are the eigendirections preserved?
        # ============================================================
        self.play(
            FadeOut(series_formula),
            FadeOut(complete_matrix),
            FadeOut(plane),
            FadeOut(x_label),
            FadeOut(y_label),
            FadeOut(legend),
            run_time=1.3,
        )

        modal_title = Tex(
            "Why are the eigendirections preserved?"
        ).scale(0.72)

        modal_title.to_edge(
            UP,
            buff=0.25,
        )

        self.play(
            Write(modal_title),
            run_time=1.2,
        )

        modal_plane = NumberPlane(
            x_range=[-2.8, 2.8, 0.5],
            y_range=[-2.2, 2.2, 0.5],
            x_length=7.0,
            y_length=4.8,
            background_line_style={
                "stroke_color": GREY_B,
                "stroke_opacity": 0.25,
                "stroke_width": 1,
            },
            axis_config={
                "include_numbers": False,
                "include_ticks": False,
                "stroke_width": 2,
            },
        ).shift(
            DOWN * 1.15
        )

        eigenspace_1 = Line(
            modal_plane.c2p(
                -2.7 * v1[0],
                -2.7 * v1[1],
            ),
            modal_plane.c2p(
                2.7 * v1[0],
                2.7 * v1[1],
            ),
            color=BLUE_C,
            stroke_width=3,
        ).set_opacity(0.55)

        eigenspace_2 = Line(
            modal_plane.c2p(
                -2.1 * v2[0],
                -2.1 * v2[1],
            ),
            modal_plane.c2p(
                2.1 * v2[0],
                2.1 * v2[1],
            ),
            color=ORANGE,
            stroke_width=3,
        ).set_opacity(0.55)

        eigenspace_labels = VGroup(
            MathTex(
                r"\lambda_1=0.8\in\mathbb{R}"
            ).scale(0.48).set_color(BLUE_C),

            MathTex(
                r"\lambda_2=-0.6\in\mathbb{R}"
            ).scale(0.48).set_color(ORANGE),
        ).arrange(
            DOWN,
            aligned_edge=LEFT,
            buff=0.12,
        )

        eigenspace_labels.to_corner(
            DR,
            buff=0.30,
        )

        self.play(
            Create(modal_plane),
            Create(eigenspace_1),
            Create(eigenspace_2),
            FadeIn(eigenspace_labels),
            run_time=1.8,
        )

        # ------------------------------------------------------------
        # Av = lambda v
        # ------------------------------------------------------------
        eigen_formula = MathTex(
            r"Av=\lambda v"
        ).scale(0.78)

        eigen_formula.next_to(
            modal_title,
            DOWN,
            buff=0.20,
        )

        v1_arrow = arrow_from_vector(
            modal_plane,
            1.65 * v1,
            BLUE_C,
            width=6,
        )

        v2_arrow = arrow_from_vector(
            modal_plane,
            1.35 * v2,
            ORANGE,
            width=6,
        )

        v1_label = MathTex(
            "v_1"
        ).scale(0.48).set_color(BLUE_C)

        v1_label.next_to(
            v1_arrow.get_end(),
            UR,
            buff=0.05,
        )

        v2_label = MathTex(
            "v_2"
        ).scale(0.48).set_color(ORANGE)

        v2_label.next_to(
            v2_arrow.get_end(),
            UL,
            buff=0.05,
        )

        v_labels = VGroup(
            v1_label,
            v2_label,
        )

        self.play(
            Write(eigen_formula),
            run_time=1.0,
        )

        self.play(
            GrowArrow(v1_arrow),
            GrowArrow(v2_arrow),
            FadeIn(v_labels),
            run_time=1.5,
        )

        self.wait(0.6)

        Av1 = arrow_from_vector(
            modal_plane,
            lambda_1 * 1.65 * v1,
            BLUE_C,
            width=8,
        )

        Av2 = arrow_from_vector(
            modal_plane,
            lambda_2 * 1.35 * v2,
            ORANGE,
            width=8,
        )

        self.play(
            TransformFromCopy(
                v1_arrow,
                Av1,
            ),
            TransformFromCopy(
                v2_arrow,
                Av2,
            ),
            run_time=1.8,
        )

        self.wait(1.0)

        # ------------------------------------------------------------
        # AAv = A lambda v
        # ------------------------------------------------------------
        intermediate_2 = MathTex(
            r"AAv=A\lambda v"
        ).scale(0.78)

        intermediate_2.move_to(eigen_formula)

        self.play(
            FadeTransform(
                eigen_formula,
                intermediate_2,
            ),
            run_time=1.3,
        )

        self.wait(0.8)

        # ------------------------------------------------------------
        # A^2 v = lambda^2 v
        # ------------------------------------------------------------
        power_2 = MathTex(
            r"A^2v=\lambda^2v"
        ).scale(0.78)

        power_2.move_to(intermediate_2)

        self.play(
            FadeTransform(
                intermediate_2,
                power_2,
            ),
            run_time=1.3,
        )

        A2v1_target = arrow_from_vector(
            modal_plane,
            lambda_1**2 * 1.65 * v1,
            BLUE_C,
            width=8,
        )

        A2v2_target = arrow_from_vector(
            modal_plane,
            lambda_2**2 * 1.35 * v2,
            ORANGE,
            width=8,
        )

        self.play(
            Transform(
                Av1,
                A2v1_target,
            ),
            Transform(
                Av2,
                A2v2_target,
            ),
            run_time=1.7,
        )

        self.wait(0.9)

        # ------------------------------------------------------------
        # AA^2v = A lambda^2 v
        # ------------------------------------------------------------
        intermediate_3 = MathTex(
            r"AA^2v=A\lambda^2v"
        ).scale(0.78)

        intermediate_3.move_to(power_2)

        self.play(
            FadeTransform(
                power_2,
                intermediate_3,
            ),
            run_time=1.3,
        )

        self.wait(0.8)

        # ------------------------------------------------------------
        # A^3v = lambda^3v
        # ------------------------------------------------------------
        power_3 = MathTex(
            r"A^3v=\lambda^3v"
        ).scale(0.78)

        power_3.move_to(intermediate_3)

        self.play(
            FadeTransform(
                intermediate_3,
                power_3,
            ),
            run_time=1.3,
        )

        A3v1_target = arrow_from_vector(
            modal_plane,
            lambda_1**3 * 1.65 * v1,
            BLUE_C,
            width=8,
        )

        A3v2_target = arrow_from_vector(
            modal_plane,
            lambda_2**3 * 1.35 * v2,
            ORANGE,
            width=8,
        )

        self.play(
            Transform(
                Av1,
                A3v1_target,
            ),
            Transform(
                Av2,
                A3v2_target,
            ),
            run_time=1.7,
        )

        self.wait(0.9)

        # ------------------------------------------------------------
        # General power
        # ------------------------------------------------------------
        general_power = MathTex(
            r"A^kv=\lambda^kv"
        ).scale(0.78)

        general_power.move_to(power_3)

        self.play(
            FadeTransform(
                power_3,
                general_power,
            ),
            run_time=1.3,
        )

        self.wait(0.8)

        # ------------------------------------------------------------
        # Division by k! changes length, not direction
        # ------------------------------------------------------------
        divided_power = MathTex(
            r"\frac{A^k}{k!}v"
            r"="
            r"\frac{\lambda^k}{k!}v"
        ).scale(0.78)

        divided_power.move_to(general_power)

        self.play(
            FadeTransform(
                general_power,
                divided_power,
            ),
            run_time=1.4,
        )

        self.wait(1.0)

        # ------------------------------------------------------------
        # e^A v = e^lambda v
        # ------------------------------------------------------------
        conclusion = MathTex(
            r"e^Av"
            r"="
            r"\left("
            r"\sum_{k=0}^{\infty}"
            r"\frac{\lambda^k}{k!}"
            r"\right)v"
            r"="
            r"e^\lambda v"
        ).scale(0.75)

        conclusion.move_to(divided_power)

        final_v1 = arrow_from_vector(
            modal_plane,
            np.exp(lambda_1) * 0.75 * v1,
            BLUE_C,
            width=8,
        )

        final_v2 = arrow_from_vector(
            modal_plane,
            np.exp(lambda_2) * 1.35 * v2,
            ORANGE,
            width=8,
        )

        self.play(
            FadeTransform(
                divided_power,
                conclusion,
            ),
            run_time=1.7,
        )

        self.play(
            Transform(
                Av1,
                final_v1,
            ),
            Transform(
                Av2,
                final_v2,
            ),
            run_time=1.8,
        )

        final_message = Tex(
            r"$e^A$ keeps the eigendirections of $A$\\"
            r"and maps each eigenvalue $\lambda$ to $e^\lambda$."
        ).scale(0.56)

        final_message.to_corner(
            UL,
            buff=0.28,
        ).shift(
            DOWN * 0.75
        )

        self.play(
            FadeIn(
                final_message,
                shift=RIGHT * 0.12,
            ),
            run_time=1.2,
        )

        self.wait(3.0)



