# Given ODE / system dynamics
# Laplace transform -> Use table to get h(t)
# Given a system impulse response, h(t), and the input f(t), the output y(t) is the convolution of h(t) and f(t)
# Output y(t) = f(t)*h(t), f(t): Input for example a unit step


## Go to folder with file and run with: python convolution.py ##
import scipy.integrate
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation


def showConvolution(t0,f1, f2):
    # Calculate the overall convolution result using Simpson integration
    convolution = np.zeros(len(t))
    for n, t_ in enumerate(t):
        prod = lambda tau: f1(tau) * f2(t_-tau)
        convolution[n] = scipy.integrate.simps(prod(t), t)

    # Create the shifted and flipped function
    f_shift = lambda t: f2(t0-t)
    prod = lambda tau: f1(tau) * f2(t0-tau)

    # Plot the curves
    axes[0].clear() 
    axes[1].clear()
    
    axes[0].set_xlim(-5, 5)
    axes[0].set_ylim(-2.0, 2.0)
   
    axes[0].plot(t, f1(t), label=r'$f_1(\tau)$')
    axes[0].plot(t, f_shift(t), label=r'$f_2(t_0-\tau)$')
    
    axes[0].plot(t, prod(t), 'r-', label=r'$f_1(\tau)f_2(t_0-\tau)$')

    # plot the convolution curve
    axes[1].set_xlim(-5, 5)
    axes[1].set_ylim(-3, -3)
    axes[1].plot(t, convolution, label='$(f_1*f_2)(t)$')

    # recalculate the value of the convolution integral at the current time-shift t0
    current_value = scipy.integrate.simps(prod(t), t)
    axes[1].plot(t0, current_value, 'ro')  # plot the point

Fs = 50  # our sampling frequency for the plotting
T = 5    # the time range we are interested in
t = np.arange(-T, T, 1/Fs)  # the time samples
f1 = lambda t: np.maximum(0, 1-abs(t)) 
f2 = lambda t: (t>0) * np.exp(-3*t)
# f1 = lambda t: (t>0) * np.sin(20*t)
# f2 = lambda t: (t>0) * np.sin(20*t)

t0 = np.arange(-2.0,2.0, 0.05)

fig = plt.figure(figsize=(8,3))
axes= fig.subplots(2, 1)
anim = animation.FuncAnimation(fig, showConvolution, frames=t0, fargs=(f1,f2),interval=80)

plt.show()
plt.close()
