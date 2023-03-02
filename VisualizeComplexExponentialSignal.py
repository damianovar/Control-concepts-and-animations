from manim import *

class VisualizeComplexExponential(ThreeDScene):
    def construct(self):

        # define how long the animation should last in seconds
        runtime = 5

        # define the parameters for the function
        [alpha, theta] = [-0.4, 10]

        # define also the domain of the function
        [t_min, t_max] = [-5, 5]

        # define the actual function
        expt = ParametricFunction(
            lambda t: np.array([
                t,
                np.exp(alpha * t) * np.cos(theta * t),
                np.exp(alpha * t) * np.sin(theta * t),
            ]), color=RED, t_range = np.array([t_min, t_max, 0.01])
        ).set_shade_in_3d(True)
        
        # set the axes and labels
        axes = ThreeDAxes(
            x_range=[t_min, t_max, 1],
            y_range=[-6, 6, 1],
            z_range=[-6, 6, 1],
            x_length=10,
            y_length=6,
            z_length=6,
        )
        x_label = axes.get_x_axis_label(Tex("$t$"))
        y_label = axes.get_y_axis_label(Tex("$\\textrm{Re}[f(t)]$"))
        z_label = axes.get_z_axis_label(Tex("$\\textrm{Im}[f(t)]$"))
        f_label = Tex("$f(t) = \\textrm{exp} \\left( \\sigma + i \\omega \\right)$").next_to(z_label, UP, buff = 0.5)
        self.add(f_label)

        # define the parametric point (T, 0, 0), that will be dynamically redrawn
        T = ValueTracker(t_min) 
        dot = always_redraw(
            lambda: Dot().move_to(
                axes.c2p(T.get_value(), 0, 0 )
            )
        )
        self.add(dot)

        # set how the visualization should look like
        self.set_camera_orientation(theta=-45 * DEGREES, phi=60 * DEGREES)
        self.add(axes, x_label, y_label, z_label)
        self.begin_ambient_camera_rotation(
            rate=PI / 10, about="theta"
        )  # note: make it rotate at a rate of PI/10 radians per second

        # make the animation
        self.play(T.animate.set_value(t_max), Create(expt), run_time=runtime, rate_func=linear)

        # do not close the video at its end
        self.wait()

