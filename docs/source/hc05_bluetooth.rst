.. index:: hc-05, bluetooth
.. _hc-05:

**********************
HC-05 Bluetooth module
**********************


.. index:: module

Module
======

The HC-05 is a cheap and relatively small serial bluetooth device.

In both HC-05 and HC-06 modules, the hardware is exactly the same, the only
difference is the firmware. There are notable differences between both
firmwares as the HC-05 is more efficient, more configurable and has a much more
extended AT command set.

The serial baudrate (hardware dependent) can be configured from 4800 to
3686400, allowing a pretty decend communication speed (very convenient for
real-time communication with the robot).

Among all the available pins, the HC-05 firmware uses the following pins in a
minimum system:

- UART_TXD and UART_RXD for serial transmission (communication with the
  microcontroller).
- PIO8 usually connects with a LED. When the module is power on, LED will
  flicker. And the flicker style will indicate which work mode is in since
  different modes have different flicker patrons. It will blink fast in pairing
  mode, slow in AT mode and fill double-blink each couple of seconds after
  paired with another device.
- PIO9 also is usually connected with a LED. It indicates whether the
  connection is built or not. When the Bluetooth serial is paired, the LED will
  be turned on. It means the connection is built successfully.
- PIO11 is the work mode switch. When this PIN port is input high level, the
  work mode will become order-response work mode (AT mode). While this PIN port
  is input low level or suspended in air (high impedance), the work mode will
  become automatic connection work mode.
- PIO0 and PIO1 to enable RX and TX lines.
- RESET, VCC and GND for obvious purposes.

.. note:: Although not mentioned in the datasheet, PIO8 already has a different
   blinking patron when the module is paired, so PIO9 can be a bit redundant.

.. warning:: It is important to mention that the UART_RXD line has no pull-up
   resistor, and it should be added if the microcontroller TXD does not have
   pull-up function.

With the HC-05 not only you are able to properly configure the module as master
or slave, set the passkey or list nearby devices or recently connected devices,
but also, this firmware allows you to configure output pins: PIO2-PIO7 and
PIO10 (i.e.: to drive some LEDs or to set signals that do not need to switch
state fast).

The PCM pins could be used for echo cancellation if we were using this module
for audio transmission.

The SPI and USB pins can be used to change the firmware of the device. The
firmware is not free software (neither the application to upload new firmware),
and are both property of CSR. Buying CSR tools would allow us to use other pins
and even allow us to modify the firmware to make use of the ADCs already
available in the bluetooth device. But this would be interesting only if we did
not mind using propietary software for applications in which the bluetooth
device would work as a standalone device (i.e.: reading sensors, controlling
signals, communicating with other devices...).

Module current consumption (real tested parameters, as the datasheet for this
device is quite inaccurate):

- In AT mode, the consumption is under 3 mA.
- While pairing or searching for devices, the consumption is under 40 mA.
- After pairing, the current consumption is under 8 mA if there is no
  communication. While communicating, the consumption of the bluetooth device
  is about 20 mA.


.. index:: AT-mode

AT mode
=======

To enter AT mode simply:

#. Reset the device (input low level to pin 11 for at least 5 ms). Or power off
   the device.
#. Input high level to pin 34.
#. Input high level to pin 11 again (or high impedance). Or power on the
   device.

This way the module enters AT-mode with a well-known serial configuration,
which is very convenient:

- 38400 baud rate.
- 8-bits data.
- 1 stop bit.
- No parity.

On the other hand, this way we need to reset the module (and therefore lose all
bluetooth connections with other devices).

Alternatively, we can enter AT-mode as well without resetting the device by
simply inputting high level to pin 34. This is quite convenient, but we will
need to communicate with the device with the configured settings, rather than
fixed, well-known settings. As long as we know the current serial
communication, this is not a problem. Note that we can do this even if the
device is paired with another device.


.. index:: mounted

PCB-mounted devices
===================

Many times the HC-05 comes already mounted on a PCB in a very reduced working
system, just enough to use the serial communication. Note that:

- Although many of these mounted devices are compatible with 5 V logic levels,
  they do work just fine with 3.3 V.
- Some may have a small switch connected to pin 34. This is very convenient, as
  we can very easily enter AT-mode this way (just press the switch while you
  power on the device).


.. index:: configuration

Configuration
=============

Once you are in AT-mode, you should see the LED blinking less frequently,
indicating you have successfully entered this mode.

Now, supposing you are connected to the bluetooth with a serial interface at
``/dev/ttyUSB0`` in your computer, first you need to set the appropriate serial
configuration:

.. code:: bash

   stty -F /dev/ttyUSB0 38400 cs8 -cstopb -parenb -echo

Then you can open a terminal to display the received data:

.. code:: bash

   cat /dev/ttyUSB0

And send a simple command to test the connection:

.. code:: bash

   echo -en "at+version?\r\n" > /dev/ttyUSB0

Which should result in the version being displayed in the first terminal.

A typical, very basic configuration could look like this:

.. code:: bash

   echo -en "at+name=Theseus\r\n" > /dev/ttyUSB0
   echo -en "at+uart=921600,0,0\r\n" > /dev/ttyUSB0
   echo -en "at+role=0\r\n" > /dev/ttyUSB0


.. index:: connection

Connection
==========

Checking the connection is easy. If you have a smartphone, you can install
`Bluetooth terminal`_ and connect to the device. Then, supposing you are still
using a serial interface at ``/dev/ttyUSB0`` with a baud rate of 921600, no
parity, 1 stop bit and 8 bits data:

.. code:: bash

   stty -F /dev/ttyUSB0 921600 cs8 -cstopb -parenb -echo
   echo -e "Hello world!" > /dev/ttyUSB0

If everything went well you should see a ``Hello world!`` message displayed on
your phone screen! ^^

.. note:: Be sure to configure Bluetooth terminal application with ASCII input
   mode, no checksum and ``\n`` ending.


References
==========

.. target-notes::

.. _`Bluetooth terminal`:
  https://github.com/Sash0k/bluetooth-spp-terminal
