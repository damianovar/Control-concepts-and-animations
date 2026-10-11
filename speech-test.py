from manim import *
from manim_voiceover import VoiceoverScene
from manim_voiceover.services.gtts import GTTSService


class ModulusGraphRealZero(ThreeDScene, VoiceoverScene):
    def construct(self):

        # Automatically generate speech from the supplied text.
        self.set_speech_service(GTTSService())

        axes = ThreeDAxes()
        title = Text("Modulus of a real zero").to_corner(UL)

        self.add_fixed_in_frame_mobjects(title)

        with self.voiceover(
            text=(
                "Consider a transfer function having one real zero. "
                "The magnitude becomes zero precisely at the location "
                "of that zero in the complex plane."
            )
        ) as tracker:

            self.play(
                Write(title),
                Create(axes),
                run_time=tracker.duration,
            )

        surface = Surface(
            lambda sigma, omega: axes.c2p(
                sigma,
                omega,
                np.sqrt((sigma - 1) ** 2 + omega**2),
            ),
            u_range=[-3, 3],
            v_range=[-3, 3],
            resolution=(32, 32),
        ).set_fill(RED_D, opacity=0.6)

        with self.voiceover(
            text=(
                "In ordinary magnitude coordinates, the surface therefore "
                "looks like a cone whose tip touches the complex plane."
            )
        ) as tracker:

            self.play(
                Create(surface),
                run_time=tracker.duration,
            )

        self.wait()


