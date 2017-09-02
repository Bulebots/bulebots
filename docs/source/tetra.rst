.. index:: tetra, locomotion

****************
Tetra locomotion
****************


.. index:: introduction

Introduction
============

A tetra design is composed with 2 motors, each driving two wheels. The motors
have a pinion that drives two gears attached to the wheels.

Both the pinion and the gear must have the same module. There is a simple
equation that relates the module, the number of teeth and the reference
diameter of the gear:

.. math:: M = \frac{D_r}{Z}

When working with gears there are 3 different diameter that we could refer to:
the internal, the reference and the external diameters.

.. figure:: figures/gear_diameters.svg
   :width: 30%
   :align: center

   External, reference and internal diameters in a gear.

The external diameter can be calculated with:

.. math:: D_e = M (Z + 2) = D_r + 2 M

The resulting locomotion in a tetra design looks like this:

.. figure:: figures/gears.svg
   :width: 50%
   :align: center

   Tetra locomotion design.


.. index:: restrictions

Restrictions
============

Note we have two important restrictions:

- The wheel must have a diameter greater than the external gear diameter
  :math:`D_e^{gear}`. Otherwise the gear would be in contact with the floor.
- The wheel must have a diameter smaller than the reference diameter of the
  gear plus the reference diameter of the pinion :math:`D_r^{gear} +
  D_r^{pinion}`. Otherwise the two wheels would be in contact with eachother.
- We will usually want to keep some space between the floor and the base of the
  robot (i.e.: the PCB).

In some cases, keeping that space between the floor and the PCB is not a
problem:

.. plot::
   :align: center

   from tetra import show_locomotion


   config = {
       'module': 0.3,
       'motor_diameter': 15,
       'pinion_z': 15,
       'motor_shift': 0,
       'wheel_diameter': 24,
       'gear_z': 70,
       'pcb_thick': 1.,
   }

   show_locomotion(**config)

If the configuration leaves too little space between the PCB and the floor then
we can always shift the motor a bit up:

.. plot::
   :align: center

   from tetra import show_locomotion


   config = {
       'module': 0.3,
       'motor_diameter': 15,
       'pinion_z': 15,
       'motor_shift': 1.5,
       'wheel_diameter': 21,
       'gear_z': 60,
       'pcb_thick': 1.,
   }

   show_locomotion(**config)

.. note:: Shifting the motor up will shift the center of mass of the robot a
   bit up as well. It will also compesate worse the forces generated because of
   the contact between the gears, although this might have a very little
   impact overall.

Of course, another alternative is to cut the base/PCB to allow the motor to
pass through it. As a downside, cutting the PCB might not be easy and might not
left much area connecting the front and the back parts of the robot.
