.. index:: hc-05, bluetooth

***************
HC-05 Bluetooth
***************


.. index:: module

Module
======

We are using an HC-05 bluetooth module for communicating with the external
world in real-time.

In both HC-05 and HC-06 modules, the hardware is exactly the same, the only
difference is the firmware. There are notable differences between both
firmwares as the HC-05 is more efficient, more configurable and has a much more
extended AT command set.

The serial baudrate (hardware dependent) can be configured from 4800 to
3686400, allowing a pretty decend communication speed (very convenient as we
will be using it for real-time communication with the robot).

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
   pull-up function (which is not our case).

The PCM pins could be used for echo cancellation if we were using this module
for audio transmission. The SPI and USB pins can be used to change the firmware
of the device. The firmware is not free software (neither the application to
upload new firmware), and are both property of CSR. That is why we are not
using those pins, as we do not really want to change HC-05 firmware, which is
the best firmware for this device freele available. Buying CSR tools would
allow us to make use of other pins (as AIOx), even allowing us to modify the
firmware to make use of the ADCs already available in the bluetooth device, but
this would be interesting only if we did not mind using propietary and
expensive software for applications in which the bluetooth device would work as
a standalone device, reading sensors, controlling signals and communicating
with other devices. As we have already mencioned, this is not our case.

.. note:: With the HC-05 not only you are able to properly configure the module
   as master or slave, set the passkey or list nearby devices or recently
   connected devices, but also, this firmware allows you to configure output
   pins: PIO2-PIO7 and PIO10 (i.e.: to drive some LEDs or to set signals that
   do not need to switch state fast).

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

To enter AT mode we can simply:

#. Reset the device (input low level to pin 11 for at least 5 ms). Or power off
   the device.
#. Input high level to pin 34.
#. Input high level to pin 11 again (or high impedance). Or power on the
   device.

This way the module enters AT-mode with a well-known USART configuration, which
is very convenient:

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


.. index:: configuration

Configuration
=============

For our initial prototype we are using an HC-05 bluetooth module mounted on a
PCB with very few pins available (just enough for serial communication, which
is what we really need) and with a small switch to start in AT-mode, which is
very convenient.

In order to enter the AT-command mode we can siply press the switch while we
power the device. In this case we can see the LED blinking less frequently,
indicating we have successfully entered AT-command mode.

Once we are in AT-command mode, and supposing we are connected to the
bluetooth with a serial interface at ``/dev/ttyUSB0``, we need to set the
appropriate serial configuration:

.. code:: bash

   stty -F /dev/ttyUSB0 38400 cs8 -cstopb -parenb

Then we can open a terminal to display the received data:

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
`Bluetooth terminal`_ and connect to the device. Then, supposing we are still
using a serial interface at ``/dev/ttyUSB0`` with a baud rate of 921600, no
parity, 1 stop bit and 8 bits data:

.. code:: bash

   stty -F /dev/ttyUSB0 921600 cs8 -cstopb -parenb
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
