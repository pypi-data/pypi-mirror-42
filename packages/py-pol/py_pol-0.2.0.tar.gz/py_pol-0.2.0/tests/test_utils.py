# !/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Tests for stokes module"""

import sys

import numpy as np

from py_pol import degrees, eps
from py_pol.utils import (comparison, rotation_matrix_Mueller,
                          azimuth_elipt_2_carac_angles,
                          carac_angles_2_azimuth_elipt)


class Test_Utils(object):
    def test_rotation_matrix_Mueller(self):
        solution = np.matrix(
            np.array([[1, 0, 0, 0], [0, 0, 1, 0], [0, -1, 0, 0], [0, 0, 0,
                                                                  1]]))
        proposal = rotation_matrix_Mueller(45 * degrees)
        assert comparison(
            proposal, solution,
            eps), sys._getframe().f_code.co_name + "@ Rotation 45 deg"

    def test_transformation_coordinates(self):
        N = 20
        errors = np.zeros(N)
        for ind in range(N):
            (alpha, delta) = np.random.rand(2)
            alpha = alpha * 90 * degrees
            delta = delta * 360 * degrees
            solution = np.array([alpha, delta])
            (fi, chi) = carac_angles_2_azimuth_elipt(alpha, delta)
            proposal = azimuth_elipt_2_carac_angles(fi, chi)
            proposal = np.array(proposal)
            errors[ind] = comparison(proposal, solution, eps)
        assert all(
            errors), sys._getframe().f_code.co_name + "@ Start in carac angles"

        for ind in range(N):
            (az, el) = np.random.rand(2)
            az = az * 180 * degrees
            el = (1 - 2 * el) * 45 * degrees
            solution = np.array([az, el])
            (alpha, delay) = azimuth_elipt_2_carac_angles(az, el)
            proposal = carac_angles_2_azimuth_elipt(alpha, delay)
            proposal = np.array(proposal)
            errors[ind] = comparison(proposal, solution, eps)
        assert all(errors), sys._getframe().f_code.co_name + "@ Start in az-el"
