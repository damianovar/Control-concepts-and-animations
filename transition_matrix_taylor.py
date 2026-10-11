from manim import *
import numpy as np
from math import factorial


class TransitionMatrixTaylor(Scene):
    def construct(self):
        # A has eigendirections span([2,1]) and span([-1,2]).
        # The eigenvalues are kept small so that 0 <= t <= 10
        # remains graphically manageable.
        v1 = np.array([2.0, 1.0])
        v1 /= np.linalg.norm(v1)

        v2 = np.array([-1.0, 2.0])
        v2 /= np.linalg.norm(v2)

        Q = np.column_stack((v1, v2))
        A = Q @ np.diag([0.08, -0.12]) @ Q.T

        # Taylor coefficient matrices T_k = A^k/k!
        N = 7
        C = [
            np.linalg.matrix_power(A, k) / factorial(k)
            for k in range(N)
        ]

        time = ValueTracker(1.0)

        BLUE_COL = BLUE_C
        ORANGE_COL = ORANGE

        # ============================================================
        # Helpers
        # ============================================================
        def framed(mob, color=YELLOW, buff=0.055):
            return SurroundingRectangle(
                mob,
                color=color,
                buff=buff,
                stroke_width=3,
            )

        def formula(parts, scale=0.76):
            return MathTex(
                *parts,
                arg_separator=r"\,",
            ).scale(scale)

        def make_plane(radius=2.6):
            step = radius / 4

            return NumberPlane(
                x_range=[-radius, radius, step],
                y_range=[-radius, radius, step],
                x_length=6.1,
                y_length=5.1,
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
            ).shift(DOWN * 1.15)

        def axis_labels(plane):
            xlab = MathTex("x_1").scale(0.50)
            ylab = MathTex("x_2").scale(0.50)

            xlab.next_to(
                plane.x_axis.get_end(),
                RIGHT,
                buff=0.05,
            )

            ylab.next_to(
                plane.y_axis.get_end(),
                UP,
                buff=0.05,
            )

            return VGroup(xlab, ylab)

        def arrow(
            plane,
            start,
            end,
            color,
            width=5,
            opacity=1.0,
        ):
            start = np.asarray(start, dtype=float)
            end = np.asarray(end, dtype=float)

            if np.linalg.norm(end - start) < 1e-9:
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

        def segment(
            plane,
            start,
            end,
            color,
        ):
            start = np.asarray(start, dtype=float)
            end = np.asarray(end, dtype=float)

            if np.linalg.norm(end - start) < 1e-9:
                return Dot(
                    plane.c2p(*start),
                    radius=0.001,
                ).set_opacity(0)

            return Line(
                plane.c2p(*start),
                plane.c2p(*end),
                color=color,
                stroke_width=5,
            )

        def weighted(k, column):
            return (
                C[k][:, column]
                * time.get_value() ** k
            )

        def partial(column, k):
            return sum(
                (
                    weighted(j, column)
                    for j in range(k + 1)
                ),
                np.zeros(2),
            )

        def live_readout(anchor):
            group = VGroup(
                MathTex("t=").scale(0.53),
                DecimalNumber(
                    time.get_value(),
                    num_decimal_places=1,
                ).scale(0.53),
            ).arrange(
                RIGHT,
                buff=0.04,
            )

            group.next_to(
                anchor,
                RIGHT,
                buff=0.25,
            ).align_to(
                anchor,
                UP,
            )

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
        # 1. Definition of the exponential
        # ============================================================
        f0 = formula(
            [
                r"e^{\star}",
                r":=",
                r"\frac{\star^0}{0!}",
                "+",
                r"\frac{\star^1}{1!}",
                "+",
                r"\frac{\star^2}{2!}",
                "+",
                r"\frac{\star^3}{3!}",
                r"+\cdots",
            ],
            0.80,
        ).to_edge(
            UP,
            buff=0.38,
        )

        self.play(
            Write(f0),
            run_time=2,
        )

        star_boxes = VGroup(
            *[
                framed(f0[i])
                for i in (2, 4, 6, 8)
            ]
        )

        self.play(
            AnimationGroup(
                *[
                    Create(b)
                    for b in star_boxes
                ],
                lag_ratio=0.12,
            ),
            run_time=1.4,
        )

        self.wait(0.5)

        # ============================================================
        # 2. Substitute star with At
        # ============================================================
        f1 = formula(
            [
                r"e^{At}",
                r":=",
                r"\frac{(At)^0}{0!}",
                "+",
                r"\frac{(At)^1}{1!}",
                "+",
                r"\frac{(At)^2}{2!}",
                "+",
                r"\frac{(At)^3}{3!}",
                r"+\cdots",
            ],
            0.77,
        ).move_to(f0)

        self.play(
            FadeOut(star_boxes),
            FadeTransform(f0, f1),
            run_time=1.7,
        )

        # ============================================================
        # 3. Remove 0! and 1!
        # ============================================================
        first_denominators = VGroup(
            framed(f1[2]),
            framed(f1[4]),
        )

        facts = MathTex(
            r"0!=1,\qquad 1!=1"
        ).scale(0.63)

        facts.next_to(
            f1,
            DOWN,
            buff=0.38,
        )

        self.play(
            Create(first_denominators[0]),
            Create(first_denominators[1]),
            FadeIn(facts),
            run_time=1.2,
        )

        self.wait(0.6)

        f2 = formula(
            [
                r"e^{At}",
                r":=",
                r"(At)^0",
                "+",
                r"(At)^1",
                "+",
                r"\frac{(At)^2}{2!}",
                "+",
                r"\frac{(At)^3}{3!}",
                r"+\cdots",
            ],
            0.77,
        ).move_to(f1)

        self.play(
            FadeOut(first_denominators),
            FadeOut(facts),
            FadeTransform(f1, f2),
            run_time=1.6,
        )

        # ============================================================
        # 4. Transform (At)^0 into I
        # ============================================================
        b0 = framed(f2[2])

        self.play(
            Create(b0),
            run_time=0.6,
        )

        f3 = formula(
            [
                r"e^{At}",
                r":=",
                "I",
                "+",
                r"(At)^1",
                "+",
                r"\frac{(At)^2}{2!}",
                "+",
                r"\frac{(At)^3}{3!}",
                r"+\cdots",
            ],
            0.77,
        ).move_to(f2)

        self.play(
            FadeOut(b0),
            FadeTransform(f2, f3),
            run_time=1.4,
        )

        # ============================================================
        # 5. Transform (At)^1 into At
        # ============================================================
        b1 = framed(f3[4])

        self.play(
            Create(b1),
            run_time=0.6,
        )

        f4 = formula(
            [
                r"e^{At}",
                r":=",
                "I",
                "+",
                "At",
                "+",
                r"\frac{(At)^2}{2!}",
                "+",
                r"\frac{(At)^3}{3!}",
                r"+\cdots",
            ],
            0.77,
        ).move_to(f3)

        self.play(
            FadeOut(b1),
            FadeTransform(f3, f4),
            run_time=1.4,
        )

        # ============================================================
        # 6. Bring the powers of t outside
        # ============================================================
        parentheses = VGroup(
            framed(f4[6]),
            framed(f4[8]),
        )

        self.play(
            Create(parentheses[0]),
            Create(parentheses[1]),
            run_time=0.9,
        )

        main = formula(
            [
                r"e^{At}",
                r":=",
                "I",
                "+",
                "A",
                "t",
                "+",
                r"\frac{A^2}{2!}",
                r"t^2",
                "+",
                r"\frac{A^3}{3!}",
                r"t^3",
                r"+\cdots",
            ],
            0.65,
        ).to_edge(
            UP,
            buff=0.30,
        ).shift(
            LEFT * 0.65
        )

        self.play(
            FadeOut(parentheses),
            FadeTransform(f4, main),
            run_time=1.7,
        )

        identity = MathTex(
            r"T_k:=\frac{A^k}{k!},"
            r"\qquad "
            r"e^{At}=\sum_{k=0}^{\infty}T_k t^k"
        ).scale(0.56)

        identity.next_to(
            main,
            DOWN,
            buff=0.28,
        )

        self.play(
            Write(identity),
            run_time=1.4,
        )

        self.wait(0.8)

        self.play(
            FadeOut(identity),
            run_time=0.6,
        )

        # ============================================================
        # 7. Plot the columns of T_k using adapted zoom levels
        # ============================================================
        # ============================================================
        # Show the coefficient matrices
        #
        # Every coefficient is first shown at zoom factor 1.
        # Only A and A^2/2! are temporarily magnified.
        # ============================================================
        base_radius = 2.6

        plane = make_plane(base_radius)
        labels = axis_labels(plane)

        self.play(
            Create(plane),
            FadeIn(labels),
            run_time=1.5,
        )

        first_leg = VGroup(
            Line(
                LEFT * 0.18,
                RIGHT * 0.18,
                color=BLUE_COL,
                stroke_width=5,
            ),
            MathTex(
                r"\text{first column of }e^{At}"
            ).scale(0.39),
        ).arrange(
            RIGHT,
            buff=0.08,
        )

        second_leg = VGroup(
            Line(
                LEFT * 0.18,
                RIGHT * 0.18,
                color=ORANGE_COL,
                stroke_width=5,
            ),
            MathTex(
                r"\text{second column of }e^{At}"
            ).scale(0.39),
        ).arrange(
            RIGHT,
            buff=0.08,
        )

        legend = VGroup(
            first_leg,
            second_leg,
        ).arrange(
            DOWN,
            aligned_edge=LEFT,
            buff=0.07,
        )

        legend.to_corner(
            DL,
            buff=0.23,
        )

        self.play(
            FadeIn(legend),
            run_time=0.6,
        )

        # Positions of I, A, A^2/2!, and A^3/3!
        # inside the main formula.
        coefficient_indices = [2, 4, 7, 10]

        # Temporary zoom factors:
        #
        # k = 1  -> A
        # k = 2  -> A^2/2!
        zoom_factors = {
            1: 8,
            2: 100,
        }

        for k in range(N):
            # --------------------------------------------------------
            # Highlight the current coefficient in the formula
            # --------------------------------------------------------
            if k <= 3:
                highlight = framed(
                    main[coefficient_indices[k]]
                )

                caption = None

            else:
                # T_4, T_5, ... are represented by the ellipsis.
                highlight = framed(
                    main[12]
                )

                caption = MathTex(
                    rf"T_{k}="
                    rf"\frac{{A^{k}}}{{{k}!}}"
                ).scale(0.46)

                caption.next_to(
                    main,
                    RIGHT,
                    buff=0.25,
                ).align_to(
                    main,
                    UP,
                )

            # --------------------------------------------------------
            # First show the columns at zoom factor 1
            # --------------------------------------------------------
            first_column = arrow(
                plane,
                np.zeros(2),
                C[k][:, 0],
                BLUE_COL,
                width=6,
            )

            second_column = arrow(
                plane,
                np.zeros(2),
                C[k][:, 1],
                ORANGE_COL,
                width=6,
            )

            animations = [
                Create(highlight)
            ]

            if caption is not None:
                animations.append(
                    FadeIn(caption)
                )

            self.play(
                *animations,
                run_time=0.5,
            )

            self.play(
                GrowArrow(first_column),
                GrowArrow(second_column),
                run_time=1.0,
            )

            # Let students first observe the true relative size.
            self.wait(0.65)

            # --------------------------------------------------------
            # Temporarily zoom in for A and A^2/2!
            # --------------------------------------------------------
            if k in zoom_factors:
                zoom_factor = zoom_factors[k]

                zoom_plane = make_plane(
                    base_radius / zoom_factor
                )

                zoom_labels = axis_labels(
                    zoom_plane
                )

                zoomed_first_column = arrow(
                    zoom_plane,
                    np.zeros(2),
                    C[k][:, 0],
                    BLUE_COL,
                    width=6,
                )

                zoomed_second_column = arrow(
                    zoom_plane,
                    np.zeros(2),
                    C[k][:, 1],
                    ORANGE_COL,
                    width=6,
                )

                zoom_note = VGroup(
                    Tex(
                        "temporary zoom"
                    ).scale(0.43),

                    MathTex(
                        rf"\times {zoom_factor}"
                    ).scale(0.50),
                ).arrange(
                    DOWN,
                    buff=0.06,
                )

                zoom_note.to_corner(
                    DR,
                    buff=0.28,
                ).shift(
                    UP * 0.28
                )

                # Zoom in while keeping the columns visible.
                self.play(
                    Transform(
                        plane,
                        zoom_plane,
                    ),
                    Transform(
                        labels,
                        zoom_labels,
                    ),
                    Transform(
                        first_column,
                        zoomed_first_column,
                    ),
                    Transform(
                        second_column,
                        zoomed_second_column,
                    ),
                    FadeIn(zoom_note),
                    run_time=1.4,
                )

                self.wait(1.2)

                # ----------------------------------------------------
                # Return to zoom factor 1
                # ----------------------------------------------------
                restored_plane = make_plane(
                    base_radius
                )

                restored_labels = axis_labels(
                    restored_plane
                )

                restored_first_column = arrow(
                    restored_plane,
                    np.zeros(2),
                    C[k][:, 0],
                    BLUE_COL,
                    width=6,
                )

                restored_second_column = arrow(
                    restored_plane,
                    np.zeros(2),
                    C[k][:, 1],
                    ORANGE_COL,
                    width=6,
                )

                self.play(
                    Transform(
                        plane,
                        restored_plane,
                    ),
                    Transform(
                        labels,
                        restored_labels,
                    ),
                    Transform(
                        first_column,
                        restored_first_column,
                    ),
                    Transform(
                        second_column,
                        restored_second_column,
                    ),
                    FadeOut(zoom_note),
                    run_time=1.4,
                )

                self.wait(0.5)

            # --------------------------------------------------------
            # Remove this coefficient's columns before proceeding
            # --------------------------------------------------------
            fade_animations = [
                FadeOut(first_column),
                FadeOut(second_column),
                FadeOut(highlight),
            ]

            if caption is not None:
                fade_animations.append(
                    FadeOut(caption)
                )

            self.play(
                *fade_animations,
                run_time=0.5,
            )

        # ============================================================
        # 9. Dynamic Taylor terms
        # ============================================================
        origin_1 = []
        origin_2 = []
        chain_1 = []
        chain_2 = []

        for k in range(N):
            origin_1.append(
                always_redraw(
                    lambda k=k: arrow(
                        plane,
                        np.zeros(2),
                        weighted(k, 0),
                        BLUE_COL,
                        width=4,
                        opacity=0.35,
                    )
                )
            )

            origin_2.append(
                always_redraw(
                    lambda k=k: arrow(
                        plane,
                        np.zeros(2),
                        weighted(k, 1),
                        ORANGE_COL,
                        width=4,
                        opacity=0.35,
                    )
                )
            )

            chain_1.append(
                always_redraw(
                    lambda k=k: segment(
                        plane,
                        partial(0, k - 1)
                        if k > 0
                        else np.zeros(2),
                        partial(0, k),
                        BLUE_COL,
                    )
                )
            )

            chain_2.append(
                always_redraw(
                    lambda k=k: segment(
                        plane,
                        partial(1, k - 1)
                        if k > 0
                        else np.zeros(2),
                        partial(1, k),
                        ORANGE_COL,
                    )
                )
            )

        result_1 = always_redraw(
            lambda: arrow(
                plane,
                np.zeros(2),
                partial(0, N - 1),
                BLUE_D,
                width=8,
            )
        )

        result_2 = always_redraw(
            lambda: arrow(
                plane,
                np.zeros(2),
                partial(1, N - 1),
                ORANGE,
                width=8,
            )
        )

        self.play(
            AnimationGroup(
                *[
                    FadeIn(a)
                    for a in origin_1 + origin_2
                ],
                lag_ratio=0.04,
            ),
            run_time=1.2,
        )

        # ============================================================
        # 10. Head-to-tail sums, already at t = 1
        # ============================================================
        sum_caption = Tex(
            "head-to-tail sums"
        ).scale(0.46)

        sum_caption.to_corner(
            DR,
            buff=0.30,
        ).shift(
            UP * 0.20
        )

        time_readout = always_redraw(
            lambda: live_readout(main)
        )

        # The time readout now appears immediately when the
        # head-to-tail construction begins.
        self.play(
            FadeIn(sum_caption),
            FadeIn(time_readout),
            run_time=0.7,
        )

        self.play(
            AnimationGroup(
                *[
                    Create(s)
                    for s in chain_1
                ],
                lag_ratio=0.12,
            ),
            run_time=2.2,
        )

        self.play(
            GrowArrow(result_1),
            run_time=0.8,
        )

        self.play(
            AnimationGroup(
                *[
                    Create(s)
                    for s in chain_2
                ],
                lag_ratio=0.12,
            ),
            run_time=2.2,
        )

        self.play(
            GrowArrow(result_2),
            run_time=0.8,
        )

        # ============================================================
        # 11. Highlight the explicit time powers
        # ============================================================
        time_boxes = VGroup(
            *[
                framed(main[i])
                for i in (5, 8, 11, 12)
            ]
        )

        self.play(
            AnimationGroup(
                *[
                    Create(b)
                    for b in time_boxes
                ],
                lag_ratio=0.12,
            ),
            run_time=1.1,
        )

        self.play(
            FadeOut(time_boxes),
            run_time=0.5,
        )

        # ============================================================
        # 12. Animate t: 1 -> 0
        # ============================================================
        zero_message = MathTex(
            r"e^{A0}=I"
        ).scale(0.58)

        zero_message.to_corner(
            UR,
            buff=0.34,
        ).shift(
            DOWN * 0.85
        )

        self.play(
            time.animate.set_value(0),
            run_time=5,
            rate_func=smooth,
        )

        self.play(
            FadeIn(zero_message),
            run_time=0.7,
        )

        self.wait(1)

        self.play(
            FadeOut(zero_message),
            run_time=0.4,
        )

        # ============================================================
        # 13. Animate t: 0 -> 10
        # ============================================================
        self.play(
            time.animate.set_value(10),
            run_time=12,
            rate_func=linear,
        )

        self.wait(0.8)

        # ============================================================
        # 14. Return to t = 1
        # ============================================================
        self.play(
            time.animate.set_value(1),
            run_time=6,
            rate_func=smooth,
        )

        self.wait(3)

