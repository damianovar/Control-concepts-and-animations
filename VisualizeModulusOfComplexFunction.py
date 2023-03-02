from manim import *
import numpy as np

class ModulusGraphRealZero(ThreeDScene):
    def construct(self):
        
        # define how long the animation should last in seconds
        runtime = 5

        # define how smooth the surface should look like
        resolution_factor = 32

        # create the function
        transfer_function = Surface(
            lambda u, v: np.array([
                u,
                v,
                np.sqrt( (u - 1)**2 + (v - 0)**2 )
            ]),
            u_range = [-5, 5],
            v_range = [-5, 5], 
            resolution=(resolution_factor, resolution_factor)
        )
        transfer_function.set_fill_by_checkerboard(RED_D, RED_E, opacity=0.5)
        
        # add the subject of the video
        text3d = Text("modulus of a real zero")
        self.add_fixed_in_frame_mobjects(text3d)
        text3d.to_corner(UL)
        
        # set the axes and labels
        axes = ThreeDAxes(
            x_range=[-6, 6, 1],
            y_range=[-6, 6, 1],
            x_length=6,
            y_length=6,
            z_length=6,
        )
        x_label = axes.get_x_axis_label(Tex("$\\textrm{Re}(s)$"))
        y_label = axes.get_y_axis_label(Tex("$\\textrm{Im}(s)$"))
        z_label = axes.get_z_axis_label(Tex("$\\left| H(s) \\right|$"))

        # add the opportune objects to the scene
        self.add(axes, x_label, y_label, z_label, transfer_function)
        self.set_camera_orientation(theta=-45 * DEGREES, phi=60 * DEGREES)
        self.begin_ambient_camera_rotation(
            rate=PI / 10, about="theta"
        )  # note: make it rotate at a rate of PI/10 radians per second

        # do not close the video at its end
        self.begin_3dillusion_camera_rotation(rate=2)
        self.wait(runtime)



class ModulusGraphComplexConjugateZeros(ThreeDScene):
    def construct(self):
        
        # define how long the animation should last in seconds
        runtime = 5

        # define how smooth the surface should look like
        resolution_factor = 32

        # create the function
        transfer_function = Surface(
            lambda u, v: np.array([
                u,
                v,
                np.sqrt( ( (u - 1)**2 + (v - 1)**2 ) * ( (u - 1)**2 + (v + 1)**2 ) )
            ]),
            u_range = [-2, 2],
            v_range = [-2, 2], 
            resolution=(resolution_factor, resolution_factor)
        )
        transfer_function.set_fill_by_checkerboard(RED_D, RED_E, opacity=0.5)
        
        # add the subject of the video
        text3d = Text("modulus of a pair of complex conjugate zeros")
        self.add_fixed_in_frame_mobjects(text3d)
        text3d.to_corner(UL)
        
        # set the axes and labels
        axes = ThreeDAxes(
            x_range=[-6, 6, 1],
            y_range=[-6, 6, 1],
            x_length=6,
            y_length=6,
            z_length=6,
        )
        x_label = axes.get_x_axis_label(Tex("$\\textrm{Re}(s)$"))
        y_label = axes.get_y_axis_label(Tex("$\\textrm{Im}(s)$"))
        z_label = axes.get_z_axis_label(Tex("$\\left| H(s) \\right|$"))

        # add the opportune objects to the scene
        self.add(axes, x_label, y_label, z_label, transfer_function)
        self.set_camera_orientation(theta=-45 * DEGREES, phi=60 * DEGREES)
        self.begin_ambient_camera_rotation(
            rate=PI / 10, about="theta"
        )  # note: make it rotate at a rate of PI/10 radians per second

        # do not close the video at its end
        self.begin_3dillusion_camera_rotation(rate=2)
        self.wait(runtime)


class ModulusGraphRealPole(ThreeDScene):
    def construct(self):
        
        # define how long the animation should last in seconds
        runtime = 5

        # define how smooth the surface should look like
        resolution_factor = 32

        # create the function
        transfer_function = Surface(
            lambda u, v: np.array([
                u,
                v,
                1 / np.sqrt( (u - 1)**2 + (v - 0)**2 )
            ]),
            u_range = [-5, 5],
            v_range = [-5, 5], 
            resolution=(resolution_factor, resolution_factor)
        )
        transfer_function.set_fill_by_checkerboard(RED_D, RED_E, opacity=0.5)
        
        # add the subject of the video
        text3d = Text("modulus of a real pole")
        self.add_fixed_in_frame_mobjects(text3d)
        text3d.to_corner(UL)
        
        # set the axes and labels
        axes = ThreeDAxes(
            x_range=[-6, 6, 1],
            y_range=[-6, 6, 1],
            x_length=6,
            y_length=6,
            z_length=6,
        )
        x_label = axes.get_x_axis_label(Tex("$\\textrm{Re}(s)$"))
        y_label = axes.get_y_axis_label(Tex("$\\textrm{Im}(s)$"))
        z_label = axes.get_z_axis_label(Tex("$\\left| H(s) \\right|$"))

        # add the opportune objects to the scene
        self.add(axes, x_label, y_label, z_label, transfer_function)
        self.set_camera_orientation(theta=-45 * DEGREES, phi=60 * DEGREES)
        self.begin_ambient_camera_rotation(
            rate=PI / 10, about="theta"
        )  # note: make it rotate at a rate of PI/10 radians per second

        # do not close the video at its end
        self.begin_3dillusion_camera_rotation(rate=2)
        self.wait(runtime)


class ModulusGraphComplexConjugatePoles(ThreeDScene):
    def construct(self):
        
        # define how long the animation should last in seconds
        runtime = 5

        # define how smooth the surface should look like
        resolution_factor = 32

        # create the function
        transfer_function = Surface(
            lambda u, v: np.array([
                u,
                v,
                1 / np.sqrt( ( (u - 1)**2 + (v - 2)**2 ) * ( (u - 1)**2 + (v + 2)**2 ) )
            ]),
            u_range = [-3, 3],
            v_range = [-3, 3], 
            resolution=(resolution_factor, resolution_factor)
        )
        transfer_function.set_fill_by_checkerboard(RED_D, RED_E, opacity=0.5)
        
        # add the subject of the video
        text3d = Text("modulus of a pair of complex conjugate poles")
        self.add_fixed_in_frame_mobjects(text3d)
        text3d.to_corner(UL)
        
        # set the axes and labels
        axes = ThreeDAxes(
            x_range=[-6, 6, 1],
            y_range=[-6, 6, 1],
            x_length=6,
            y_length=6,
            z_length=6,
        )
        x_label = axes.get_x_axis_label(Tex("$\\textrm{Re}(s)$"))
        y_label = axes.get_y_axis_label(Tex("$\\textrm{Im}(s)$"))
        z_label = axes.get_z_axis_label(Tex("$\\left| H(s) \\right|$"))

        # add the opportune objects to the scene
        self.add(axes, x_label, y_label, z_label, transfer_function)
        self.set_camera_orientation(theta=-45 * DEGREES, phi=60 * DEGREES)
        self.begin_ambient_camera_rotation(
            rate=PI / 10, about="theta"
        )  # note: make it rotate at a rate of PI/10 radians per second

        # do not close the video at its end
        self.begin_3dillusion_camera_rotation(rate=2)
        self.wait(runtime)

