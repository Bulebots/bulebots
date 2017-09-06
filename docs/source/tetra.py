from math import asin
from math import cos

from matplotlib import pyplot as plt
from matplotlib.pyplot import Circle
from matplotlib.pyplot import Rectangle


def show_locomotion(motor_diameter, wheel_diameter, motor_shift, pcb_thick,
                    module, pinion_z, gear_z):
    pinion_reference_diameter = module * pinion_z
    gear_reference_diameter = module * gear_z
    gear_external_diameter = module * (gear_z + 2)

    ax = plt.gca()
    ax.cla()

    # Motor and pinion
    motor_height = wheel_diameter / 2. + motor_shift
    motor = Circle(
        (0, motor_height),
        radius=motor_diameter/2.,
        color='black',
        linewidth=0,
    )
    pinion = Circle(
        (0, motor_height),
        radius=pinion_reference_diameter/2.,
        color='yellow',
        linewidth=0,
    )
    ax.add_artist(motor)
    ax.add_artist(pinion)

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
    ax.add_artist(pcb)

    # Gears and wheels
    wheel_shift = (pinion_reference_diameter + gear_reference_diameter) / 2.
    alpha = asin(motor_shift / wheel_shift)
    wheel_shift = wheel_shift * cos(alpha)
    height = wheel_diameter / 2.
    gear0 = Circle(
        (-wheel_shift, height),
        radius=gear_reference_diameter/2.,
        color='gray',
        linewidth=0,
    )
    gear1 = Circle(
        (wheel_shift, height),
        radius=gear_reference_diameter/2.,
        color='gray',
        linewidth=0,
    )
    wheel0 = Circle(
        (-wheel_shift, height),
        radius=wheel_diameter/2.,
        color='blue',
        linewidth=0,
        alpha=0.5
    )
    wheel1 = Circle(
        (wheel_shift, height),
        radius=wheel_diameter/2.,
        color='blue',
        linewidth=0,
        alpha=0.5
    )
    ax.add_artist(gear0)
    ax.add_artist(gear1)
    ax.add_artist(wheel0)
    ax.add_artist(wheel1)

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
