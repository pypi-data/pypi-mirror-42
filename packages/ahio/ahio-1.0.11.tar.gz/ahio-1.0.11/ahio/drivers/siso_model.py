# -*- coding: utf-8; -*-
#
# Copyright (c) 2016 Álan Crístoffer
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

from enum import Enum

import ahio.abstract_driver
import numpy as np


class ahioDriverInfo(ahio.abstract_driver.AbstractahioDriverInfo):
    NAME = 'SISO Model'
    AVAILABLE = True


class Driver(ahio.abstract_driver.AbstractDriver):
    Pins = Enum('Pins', 'U, Y')
    x = None
    u = None
    model = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass

    def setup(self, model='([[0.5]], [[1]], [[1]], [[0]])'):
        self.model = [np.array(x) for x in eval(model)]
        A, B, C, D = self.model
        self.u = 0
        self.x = np.zeros((A.shape[0], 1))

    def __create_pin_info(self, pid, pwm=False):
        obj = {
            'id': pid,
            'name': 'U' if pid.value == 1 else 'Y',
            'analog': {
                'input': pid.value == 2,
                'output': pid.value == 1,
                'read_range': (0, 100),
                'write_range': (0, 100)
            },
            'digital': {
                'input': False,
                'output': False,
                'pwm': False
            }
        }
        return obj

    def available_pins(self):
        pins = [p for p in Driver.Pins]
        return [self.__create_pin_info(pin, True) for pin in pins]

    def _set_pin_direction(self, pin, direction):
        pass

    def _pin_direction(self, pin):
        return ahio.Direction.Input if pin == 2 else ahio.Direction.Output

    def _set_pin_type(self, pin, ptype):
        pass

    def _pin_type(self, pin):
        return ahio.PortType.Digital

    def _write(self, pin, value, pwm):
        self.u = value

    def _read(self, pin):
        A, B, C, D = self.model
        if A.shape[0] == 1:
            self.x = A * self.x + B * self.u
            y = C * self.x
        else:
            self.x = A @ self.x + B * self.u
            y = C @ self.x
        return np.asscalar(y)

    def analog_references(self):
        return []

    def _set_analog_reference(self, reference, pin):
        pass

    def _analog_reference(self, pin):
        return []

    def _set_pwm_frequency(self, frequency, pin):
        pass
