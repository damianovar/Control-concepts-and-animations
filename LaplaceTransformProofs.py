from manim import *

class ConvolutionInTime(Scene):
    def construct(self):
        
        # Set the font size
        font = 36

        # Create the equations
        equations = [
            MathTex(r"\mathcal{L}(f * g; s) = \int_{0}^{+\infty} (f * g)(t) e^{-s t} dt \qquad \text{with } f, g \text{ causal}").set_font_size(font),
            MathTex(r"= \int_{0}^{+\infty} \left( \int_{0}^{+\infty} f(t - \tau) g(\tau) d\tau \right) e^{-s t} dt \quad \text{(because } f, g \text{ causal)}").set_font_size(font),
            MathTex(r"\text{(change of variables: } u = t - \tau \quad \implies \quad du = dt, \quad t = u + \tau \text{)}").set_font_size(font),
            MathTex(r"= \int_{0}^{+\infty} \left( \int_{0}^{+\infty} f(u) g(\tau) e^{-s (u + \tau)} du \right) d\tau").set_font_size(font),
            MathTex(r"= \int_{0}^{+\infty} \left( \int_{0}^{+\infty} f(u) g(\tau) e^{-s u} e^{-s \tau} du \right) d\tau").set_font_size(font),
            MathTex(r"= \int_{0}^{+\infty} f(u) e^{-s u} du \int_{0}^{+\infty} g(\tau) e^{-s \tau} d\tau \quad \text{(thanks to Fubini-Tonelli)}").set_font_size(font),
            MathTex(r"= F(s) G(s)").set_font_size(font)
        ]

        # Position them - the first 'up' and the next ones below
        equations[0].to_edge(UP + LEFT)
        for k in range(1, len(equations)):
            equations[k].next_to(equations[k - 1], DOWN, aligned_edge=LEFT)

        # Animate the equations
        for equation in equations:
            self.play(Write(equation))
            self.wait()

        # Pause at the end of the animation
        self.wait(3)


class TimeDerivative(Scene):
    def construct(self):
        
        # Set the font size
        font = 36

        # Create the equations
        equations = [
            MathTex(r"\text{Preliminary: integration by parts:}").set_font_size(font),
            MathTex(r"uv = \int u \, dv + \int v \, du \quad \implies \quad \int u \, dv = uv - \int v \, du").set_font_size(font),
            MathTex(r"\text{Actual computation:}").set_font_size(font),
            MathTex(r"\mathcal{L}(f'(t); s) = \int_{0}^{+\infty} f'(t) e^{-s t} dt").set_font_size(font),
            MathTex(r"= f(t) e^{-s t} \bigg|_0^{+\infty} + s \int_{0}^{+\infty} f(t) e^{-s t} dt").set_font_size(font),
            MathTex(r"= - f(0) + s F(s)").set_font_size(font)
        ]

        # Position them - the first 'up' and the next ones below
        equations[0].to_edge(UP + LEFT)
        for k in range(1, len(equations)):
            equations[k].next_to(equations[k - 1], DOWN, aligned_edge=LEFT)

        # Animate the equations
        for equation in equations:
            self.play(Write(equation))
            self.wait()

        # Pause at the end of the animation
        self.wait(3)


class TimeSecondDerivative(Scene):
    def construct(self):
        
        # Set the font size
        font = 36

        # Create the equations
        equations = [
            MathTex(r"\mathcal{L}(f''(t); s) = \int_{0}^{+\infty} f''(t) e^{-s t} dt").set_font_size(font),
            MathTex(r"= \left[ f'(t) e^{-s t} \right]_0^{+\infty} - \int_{0}^{+\infty} f'(t) (-s) e^{-s t} dt \qquad \text{(integrating by parts)}").set_font_size(font),
            MathTex(r"= \left[ f'(t) e^{-s t} \right]_0^{+\infty} + s \int_{0}^{+\infty} f'(t) e^{-s t} dt").set_font_size(font),
            MathTex(r"= \left[ f'(t) e^{-s t} \right]_0^{+\infty} + s \left[ f(t) e^{-s t} \right]_0^{+\infty} - s \int_{0}^{+\infty} f(t) (-s) e^{-s t} dt \text{(again by parts)}").set_font_size(font),
            MathTex(r"= \left[ f'(t) e^{-s t} \right]_0^{+\infty} + s \left[ f(t) e^{-s t} \right]_0^{+\infty} + s^2 \int_{0}^{+\infty} f(t) e^{-s t} dt").set_font_size(font),
            MathTex(r"= -f'(0) - s f(0) + s^2 \mathcal{L}(f(t); s)").set_font_size(font)
        ]

        # Position them - the first 'up' and the next ones below
        equations[0].to_edge(UP + LEFT)
        for k in range(1, len(equations)):
            equations[k].next_to(equations[k - 1], DOWN, aligned_edge=LEFT)

        # Animate the equations
        for equation in equations:
            self.play(Write(equation))
            self.wait()

        # Pause at the end of the animation
        self.wait(3)


class TimeScaling(Scene):
    def construct(self):
        
        # Set the font size
        font = 36

        # Create the equations
        equations = [
            MathTex(r"\mathcal{L}(f(at); s) = \int_{0}^{+\infty} f(at) e^{-s t} dt").set_font_size(font),
            MathTex(r"\text{(change of variables: } u = at \quad \implies \quad du = a \, dt \text{)}").set_font_size(font),
            MathTex(r"= \frac{1}{a} \int_{0}^{+\infty} f(u) e^{-\frac{s}{a} u} du").set_font_size(font),
            MathTex(r"= \frac{1}{a} F\left(\frac{s}{a}\right)").set_font_size(font)
        ]

        # Position them - the first 'up' and the next ones below
        equations[0].to_edge(UP + LEFT)
        for k in range(1, len(equations)):
            equations[k].next_to(equations[k - 1], DOWN, aligned_edge=LEFT)

        # make an exception for the second line
        equations[1].next_to(equations[0], DOWN, aligned_edge=RIGHT)

        # Animate the equations
        for equation in equations:
            self.play(Write(equation))
            self.wait()

        # Pause at the end of the animation
        self.wait(3)


class TimeShift(Scene):
    def construct(self):
        
        # Set the font size
        font = 36

        # Create the equations
        equations = [
            MathTex(r"\mathcal{L} \big( u(t-a) f(t-a) ; s \big) = \int_{0}^{+\infty} u(t-a) f(t-a) e^{-s t} dt").set_font_size(font),
            MathTex(r"= \int_a^{+\infty} f(t-a) e^{-s t} dt \quad (u(t-a)=0 \text{ for } t<a)").set_font_size(font),
            MathTex(r"\text{(change of variables: }\tau=t-a \quad \implies \quad d \tau = dt \text{)}").set_font_size(font),
            MathTex(r"= \int_{0}^{+\infty} f(\tau) e^{-s(\tau+a)} d\tau").set_font_size(font),
            MathTex(r"= e^{-a s} \int_{0}^{+\infty} f(\tau) e^{-s \tau} d\tau").set_font_size(font),
            MathTex(r"= e^{-a s} F(s)").set_font_size(font)
        ]

        # Position them - the first 'up' and the next ones below 
        equations[0].to_edge(UP + LEFT)
        for k in range(1, len(equations)):
            equations[k].next_to(equations[k-1], DOWN, aligned_edge=LEFT)

        # Animate the equations
        for equation in equations:
            self.play(Write(equation))
            self.wait()

        # Pause at the end of the animation
        self.wait(3)


class FrequencyDerivative(Scene):
    def construct(self):
        
        # Set the font size
        font = 30

        # Create the equations
        equations = [
            MathTex(r"\text{Preliminary: Leibniz integral rule:}").set_font_size(font),
            MathTex(r"\frac{d}{dx} \left( \int_{a(x)}^{b(x)} f(x,t) dt \right) = f\big(x,b(x)\big) \frac{db(x)}{dx} - f\big(x,a(x)\big) \frac{da(x)}{dx} + \int_{a(x)}^{b(x)} \frac{\partial f(x,t)}{\partial x} dt").set_font_size(font),
            MathTex(r"\text{Actual computation:}").set_font_size(font),
            MathTex(r"\frac{d F}{d s}=\frac{d}{d s} \int_{0}^{+\infty} f(t) e^{-s t} dt").set_font_size(font),
            MathTex(r"=\int_{0}^{+\infty} \frac{\partial \left( e^{-s t} f(t) \right)}{\partial s} dt \qquad \text{(Leibniz)}").set_font_size(font),
            MathTex(r"=\int_{0}^{+\infty} \frac{\partial e^{-s t}}{\partial s} f(t) dt").set_font_size(font),
            MathTex(r"=\int_{0}^{+\infty}\left(-t e^{-s t}\right) f(t) dt").set_font_size(font),
            MathTex(r"=-\int_{0}^{+\infty} e^{-s t}[t f(t)] dt = -\mathcal{L}\{t f(t)\}").set_font_size(font)
        ]

        # Position them - the first 'up' and the next ones below 
        equations[0].to_edge(UP + LEFT)
        for k in range(1, len(equations)):
            equations[k].next_to(equations[k-1], DOWN, aligned_edge=LEFT)

        # Animate the equations
        for equation in equations:
            self.play(Write(equation))
            self.wait()

        # Pause at the end of the animation
        self.wait(3)


#########################


class Exponential(Scene):
    def construct(self):
        
        # Set the font size
        font = 36

        # Create the equations
        equations = [
            MathTex(r"\mathcal{L}(e^{at}; s) = \int_{0}^{+\infty} e^{at} e^{-s t} dt").set_font_size(font),
            MathTex(r"= \int_{0}^{+\infty} e^{(a-s)t} dt").set_font_size(font),
            MathTex(r"= \left[ \frac{e^{(a-s)t}}{a-s} \right]_0^{+\infty}").set_font_size(font),
            MathTex(r"= \frac{1}{s-a} \qquad \text{if} \textrm{Re}(s) > \textrm{Re}(a)").set_font_size(font)
        ]

        # Position them - the first 'up' and the next ones below
        equations[0].to_edge(UP + LEFT)
        for k in range(1, len(equations)):
            equations[k].next_to(equations[k - 1], DOWN, aligned_edge=LEFT)

        # Animate the equations
        for equation in equations:
            self.play(Write(equation))
            self.wait()

        # Pause at the end of the animation
        self.wait(3)


class ExponentialTimesCosine(Scene):
    def construct(self):
        
        # Set the font size
        font = 36

        # Create the equations
        equations = [
            MathTex(r"\mathcal{L} \big( e^{\sigma t} \cos(\omega t) ; s \big) = \int_{0}^{+\infty} e^{\sigma t} \cos(\omega t) \cdot e^{-st} dt = \int_{0}^{+\infty} e^{(\sigma -s)t} \cos(\omega t) dt").set_font_size(font),
            MathTex(r"\text{(Euler's formula: } \cos(\omega t) = \frac{1}{2} \big( e^{i\omega t} + e^{-i\omega t} \big) \text{)}").set_font_size(font),
            MathTex(r"= \frac{1}{2} \int_{0}^{+\infty} e^{(\sigma -s)t} \cdot \big( e^{i\omega t} + e^{-i\omega t} \big) dt").set_font_size(font),
            MathTex(r"= \frac{1}{2} \left( \int_{0}^{+\infty} e^{(\sigma - s + i \omega)t} dt + \int_{0}^{+\infty} e^{(\sigma - s - i \omega)t} dt \right)").set_font_size(font),
            MathTex(r"= \frac{1}{2} \left( \frac{1}{\sigma - s + i \omega} + \frac{1}{\sigma - s - i \omega} \right)").set_font_size(font),
            MathTex(r"= \frac{1}{2} \left( \frac{\sigma - s - i \omega + \sigma - s + i \omega}{(\sigma - s + i \omega)(\sigma - s - i \omega)} \right)").set_font_size(font),
            MathTex(r"= \frac{1}{2} \cdot \frac{2\sigma  - 2s}{(\sigma - s)^2 + \omega^2} = \frac{\sigma  - s}{(s - \sigma)^2 + \omega^2}").set_font_size(font)
            ]

        # Position them - the first 'up' and the next ones below 
        equations[0].to_edge(UP + LEFT)
        for k in range(1, len(equations)):
            equations[k].next_to(equations[k-1], DOWN, aligned_edge=LEFT)

        # Animate the equations
        for equation in equations:
            self.play(Write(equation))
            self.wait()

        # Pause at the end of the animation
        self.wait(3)


class StepFunction(Scene):
    def construct(self):
        
        # Set the font size
        font = 36

        # Create the equations
        equations = [
            MathTex(r"\mathcal{L} \big( u(t - a) ; s \big) \qquad \text{with } a > 0").set_font_size(font),
            MathTex(r"= \int_{0}^{+\infty} u(t - a) \cdot e^{-st} dt").set_font_size(font),
            MathTex(r"= \int_{a}^{+\infty} e^{-st} dt").set_font_size(font),
            MathTex(r"= \left[ \frac{e^{-st}}{-s} \right]_{a}^{+\infty}").set_font_size(font),
            MathTex(r"= \frac{e^{-sa}}{-s}").set_font_size(font),
            MathTex(r"= \frac{1}{s} \cdot \frac{1}{e^{sa}}").set_font_size(font),
            MathTex(r"= \frac{1}{s} \cdot e^{-sa}").set_font_size(font)
        ]

        # Position them - the first 'up' and the next ones below 
        equations[0].to_edge(UP + LEFT)
        for k in range(1, len(equations)):
            equations[k].next_to(equations[k-1], DOWN, aligned_edge=LEFT)

        # Animate the equations
        for equation in equations:
            self.play(Write(equation))
            self.wait()

        # Pause at the end of the animation
        self.wait(3)

