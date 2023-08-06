# For running unit tests, use
# /usr/bin/python -m unittest test

import unittest
import numpy as np

from Model_1DV import Model


class TestModel_1DV(unittest.TestCase):

    def setUp(self):
        self.model = Model(500, 2)

    def test_initialization(self):
        self.assertEqual(self.model.grid_size, 500, 'incorrect grid size')
        self.assertEqual(self.model.t_end, 2 * 24 * 3600, 'incorrect end time')
        self.assertEqual(self.model.GRAV, 9.81, 'incorrect GRAV')
        self.assertEqual(self.model.FCOR, 1e-4, 'incorrect FCOR')
        self.assertEqual(self.model.KAPPA, 0.4, 'incorrect KAPPA')
        self.assertEqual(self.model.Z0B, 0.0035, 'incorrect Z0B')
        self.assertEqual(self.model.RHO_REF, 1026, 'incorrect RHO_REF')
        self.assertEqual(self.model.CD_AIR, 0.0016, 'incorrect CD_AIR')
        self.assertEqual(self.model.ALP, 0.5, 'incorrect ALP')
        self.assertEqual(self.model.MU_v, 1e-2, 'incorrect MU_v')
        self.assertEqual(self.model.MU_h, 1.0, 'incorrect MU_h')
        self.assertEqual(self.model.l_obc, {
            'north': False,
            'south': False,
            'west': False,
            'east': False
        }, 'incorrect l_obc')

    def test_set_variable(self):
        self.model.set_variable()
        self.assertEqual(self.model.ni, 4, 'incorrect ni')
        self.assertEqual(self.model.nj, 4, 'incorrect nj')
        self.assertEqual(self.model.nk, 101, 'incorrect nk')
        self.assertEqual(self.model.t, 0, 'incorrect t0')
        self.assertEqual(self.model.v3d_u.all(), np.zeros(
            (101, 4, 4)).all(), 'incorrect v3d_u')
        self.assertEqual(self.model.u3d_v.all(), np.zeros(
            (101, 4, 4)).all(), 'incorrect v3d_v')
        self.assertEqual(self.model.Pres.all(), (1013.15 * np.ones(
            (4, 4))).all(), 'incorrect Pres')
        self.assertEqual(self.model.Xstr.all(), (np.zeros(
            (4, 4)) + 1026 * 0.0016 * 100).all(), 'incorrect Xstr')
        self.assertEqual(self.model.Ystr.all(), np.zeros(
            (4, 4)).all(), 'incorrect Ystr')


def test_solve_equations(self):
    self.model.solve_equations(2, 2)


if __name__ == '__main__':
    unittest.main()
