from functools import partial
from math import asin
from math import cos

from matplotlib import pyplot as plt
from matplotlib.pyplot import Circle
from matplotlib.pyplot import Rectangle


def show_locomotion(motor_diameter, wheel_diameter, motor_shift, pcb_thick,
                    module, pinion_z, gear_z, shaft_diameter):
    pinion_reference_diameter = module * pinion_z
    pinion_external_diameter = module * (pinion_z + 2)
    gear_reference_diameter = module * gear_z
    gear_external_diameter = module * (gear_z + 2)

    ax = plt.gca()
    ax.cla()

    # Motor and pinion
    motor_height = wheel_diameter / 2. + motor_shift
    motor = Circle(
        (0, motor_height),
        radius=motor_diameter/2.,
        color='brown',
        linewidth=0,
    )
    shaft = Circle(
        (0, motor_height),
        radius=shaft_diameter/2.,
        color='blue',
        linewidth=0,
        alpha=0.8,
    )
    pinion = Circle(
        (0, motor_height),
        radius=pinion_external_diameter/2.,
        color='yellow',
        linewidth=0,
        alpha=0.8,
    )

    # PCB
    height = motor_height - motor_diameter / 2. - pcb_thick
    width = motor_diameter + 2 * wheel_diameter
    pcb = Rectangle(
        (-width/2., height),
        width=width,
        height=pcb_thick,
        color='green',
        linewidth=0,
    )

    # Gears and wheels
    wheel_shift = (pinion_reference_diameter + gear_reference_diameter) / 2.
    alpha = asin(motor_shift / wheel_shift)
    wheel_shift = wheel_shift * cos(alpha)
    height = wheel_diameter / 2.
    gear = partial(Circle,
        radius=gear_external_diameter/2.,
        color='white',
        linewidth=0,
        alpha=0.8,
    )
    wheel = partial(Circle,
        radius=wheel_diameter/2.,
        color='black',
        linewidth=0,
        alpha=0.7,
    )

    ax.add_artist(motor)
    ax.add_artist(pcb)
    ax.add_artist(pinion)
    ax.add_artist(wheel((-wheel_shift, height)))
    ax.add_artist(wheel((wheel_shift, height)))
    ax.add_artist(gear((-wheel_shift, height)))
    ax.add_artist(gear((wheel_shift, height)))
    ax.add_artist(shaft)

    # Change plot limits to fit everything
    x_limit = pinion_reference_diameter + wheel_diameter
    y_limit = max(wheel_diameter,
                  motor_height + motor_diameter / 2.)
    ax.set_xlim((-x_limit, x_limit))
    ax.set_ylim((0, y_limit))

    ax.set_aspect('equal')

    # Calculate free space between the PCB and the floor
    pcb_floor_space = min(
        motor_height - motor_diameter / 2. - pcb_thick,
        motor_height - motor_diameter / 2.
    )
    wheel_wheel_space = 2 * wheel_shift - wheel_diameter
    gear_wheel_space = (wheel_diameter - gear_external_diameter) / 2.
    ax.set_title('''PCB to floor: %.2f mm
Between wheels: %.2f mm
Gear (external diameter) to wheel: %.2f mm''' %
                 (pcb_floor_space, wheel_wheel_space, gear_wheel_space))

    plt.show()
