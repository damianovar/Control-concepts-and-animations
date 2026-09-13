from manim import *
import numpy as np


class StackedSinusoidsSum(Scene):
    def construct(self):
        # ------------------------------------------------------------
        # signal definitions
        # ------------------------------------------------------------
        def s1(x):
            return 1.0 * np.sin(x)

        def s2(x):
            return 0.5 * np.sin(3 * x)

        def s3(x):
            return 0.25 * np.sin(6 * x)

        def ssum(x):
            return s1(x) + s2(x) + s3(x)

        # ------------------------------------------------------------
        # formula
        # ------------------------------------------------------------
        formula = MathTex(
            r"y(t)",
            r"=",
            r"\sin(t)",
            r"+",
            r"0.5\sin(3t)",
            r"+",
            r"0.25\sin(6t)"
        )
        formula.scale(0.85)
        formula.to_edge(UP, buff=0.35)

        self.play(Write(formula))
        self.wait(0.5)

        # ------------------------------------------------------------
        # common plotting parameters
        # ------------------------------------------------------------
        x_range = [0, 2 * PI, PI / 2]

        component_axes_config = dict(
            x_range=x_range,
            y_range=[-1.2, 1.2, 1],
            x_length=8,
            y_length=1.0,
            tips=False,
            axis_config={"include_numbers": False}
        )

        sum_axes_config = dict(
            x_range=x_range,
            y_range=[-1.8, 1.8, 1],
            x_length=8,
            y_length=1.45,
            tips=False,
            axis_config={"include_numbers": False}
        )

        # ------------------------------------------------------------
        # stacked axes
        # ------------------------------------------------------------
        ax1 = Axes(**component_axes_config)
        ax2 = Axes(**component_axes_config)
        ax3 = Axes(**component_axes_config)
        ax_sum = Axes(**sum_axes_config)

        stacked_axes = VGroup(ax1, ax2, ax3, ax_sum)
        stacked_axes.arrange(DOWN, buff=0.28)
        stacked_axes.next_to(formula, DOWN, buff=0.30)

        # ------------------------------------------------------------
        # curves
        # ------------------------------------------------------------
        g1 = ax1.plot(s1)
        g2 = ax2.plot(s2)
        g3 = ax3.plot(s3)
        gsum = ax_sum.plot(ssum)

        # ------------------------------------------------------------
        # labels
        # ------------------------------------------------------------
        label1 = MathTex(r"\sin(t)").scale(0.65)
        label2 = MathTex(r"0.5\sin(3t)").scale(0.65)
        label3 = MathTex(r"0.25\sin(6t)").scale(0.65)
        label_sum = MathTex(r"y(t)").scale(0.65)

        label1.next_to(ax1, LEFT, buff=0.25)
        label2.next_to(ax2, LEFT, buff=0.25)
        label3.next_to(ax3, LEFT, buff=0.25)
        label_sum.next_to(ax_sum, LEFT, buff=0.25)

        plus1 = MathTex("+").scale(0.9)
        plus2 = MathTex("+").scale(0.9)
        equals = MathTex("=").scale(0.9)

        plus1.move_to((ax1.get_bottom() + ax2.get_top()) / 2)
        plus2.move_to((ax2.get_bottom() + ax3.get_top()) / 2)
        equals.move_to((ax3.get_bottom() + ax_sum.get_top()) / 2)

        plus1.shift(LEFT * 4.5)
        plus2.shift(LEFT * 4.5)
        equals.shift(LEFT * 4.5)

        # ------------------------------------------------------------
        # draw the components
        # ------------------------------------------------------------
        self.play(Create(ax1), FadeIn(label1))
        self.play(Create(g1))
        self.wait(0.3)

        self.play(FadeIn(plus1), Create(ax2), FadeIn(label2))
        self.play(Create(g2))
        self.wait(0.3)

        self.play(FadeIn(plus2), Create(ax3), FadeIn(label3))
        self.play(Create(g3))
        self.wait(0.3)

        # ------------------------------------------------------------
        # reveal the sum
        # ------------------------------------------------------------
        self.play(FadeIn(equals), Create(ax_sum), FadeIn(label_sum))
        self.play(Create(gsum), run_time=2)
        self.wait(1)

        # ------------------------------------------------------------
        # emphasize the final summed signal
        # ------------------------------------------------------------
        box = SurroundingRectangle(
            VGroup(ax_sum, gsum, label_sum),
            buff=0.12
        )

        self.play(Create(box))
        self.wait(1.5)

