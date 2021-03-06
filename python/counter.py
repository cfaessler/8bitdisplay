# -*- coding: utf-8 -*-
from __future__ import print_function, division, absolute_import, unicode_literals
import os
import signal
import RPIO


INPUT_PIN = 3
PIDFILE = '7segment.pid'


def send_signal_to(pid):
    """Closure that returns a GPIO interrupt callback which will send a SIGUSR1
    signal to the 7 segment process with the specified PID on button press."""
    def callback(gpio_id, value):
        os.kill(pid, signal.SIGUSR1)
    return callback


if __name__ == '__main__':

    # Set up GPIO pins
    RPIO.setmode(RPIO.BOARD)
    RPIO.setup(INPUT_PIN, RPIO.IN, pull_up_down=RPIO.PUD_DOWN)

    # Find PID of 7segment process
    with open(PIDFILE, 'r') as f:
        PID = int(f.read())

    callback = send_signal_to(PID)
    RPIO.add_interrupt_callback(INPUT_PIN, callback, edge='rising', debounce_timeout_ms=200)

    try:
        RPIO.wait_for_interrupts()
    except KeyboardInterrupt:
        print('exiting')
    finally:
        print('cleaning up')
        RPIO.cleanup()
