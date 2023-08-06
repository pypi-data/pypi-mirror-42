# -*- coding: utf-8 -*-
# Copyright (c) 2019, PyRETIS Development Team.
# Distributed under the LGPLv2.1+ License. See LICENSE for more info.
"""Test the methods in pyretis.setup.checker"""
import os
import logging
import unittest
from pyretis.engines.internal import VelocityVerlet
from pyretis.inout.settings import fill_up_tis_and_retis_settings
from pyretis.inout.checker import (check_ensemble,
                                   check_engine,
                                   check_interfaces)
from pyretis.core.system import System
from pyretis.core.particles import ParticlesExt

logging.disable(logging.CRITICAL)
HERE = os.path.abspath(os.path.dirname(__file__))


def make_test_system(conf):
    """Just make a test system with particles."""
    system = System()
    system.particles = ParticlesExt(dim=3)
    system.particles.config = conf
    return system


class TestMethods(unittest.TestCase):
    """Test some of the methods from .checker."""

    def test_check_ensemble(self):
        """Test check_ensemble."""
        settings = {'simulation': {'task': 'retis',
                                   'interfaces': [-1.0, -0.5, 0, 0.5, 1],
                                   'exe_path': HERE,
                                   'zero_ensemble': True,
                                   'flux': True},
                    'orderparameter': {'class': 'Position',
                                       'dim': 'x',
                                       'index': 0,
                                       'periodic': False},
                    'particles': {'type': 'internal'},
                    'system': {'units': 'lj'},
                    'engine': {'obj': VelocityVerlet(0.002)},
                    'tis': {}}
        self.assertFalse(check_ensemble(settings))

        fill_up_tis_and_retis_settings(settings)
        self.assertTrue(check_ensemble(settings))

        settings['simulation']['interfaces'][2] = 4
        self.assertFalse(check_ensemble(settings))

        del settings['ensemble']
        self.assertFalse(check_ensemble(settings))

    def test_check_engine(self):
        """Test check_engine."""
        settings = {'simulation': {'task': 'retis',
                                   'interfaces': [-1.0, -0.5, 0, 0.5, 1],
                                   'exe_path': HERE,
                                   'zero_ensemble': True,
                                   'flux': True},
                    'orderparameter': {'class': 'Position',
                                       'dim': 'x',
                                       'index': 0,
                                       'periodic': False},
                    'particles': {'type': 'external'},
                    'engine': {'type': 'external',
                               'cp2k': 'cp2k',
                               'input_path': 'No thank you',
                               'timestep': 1,
                               'cp2k_format': 'xyz',
                               'subcycles': 1},
                    'tis': {}}
        self.assertTrue(check_engine(settings))

        del settings['engine']['input_path']
        self.assertFalse(check_engine(settings))

        settings['engine']['input_path'] = 'Hahaha'
        del settings['engine']['cp2k_format']
        self.assertFalse(check_engine(settings))

        del settings['engine']['cp2k']
        settings['engine']['gmx'] = 'Buuuuu'
        self.assertFalse(check_engine(settings))

        # todo check for meaningful inputs
        settings['engine']['gmx_format'] = 'Gorilla'
        self.assertTrue(check_engine(settings))

    def test_check_interfaces(self):
        """Test check_interfaces."""
        settings = {'simulation': {'task': 'retis',
                                   'interfaces': [-1.0, -0.5, 0, 0.5, 1],
                                   'zero_ensemble': True,
                                   'flux': True}}

        self.assertTrue(check_interfaces(settings))
        settings['simulation']['zero_ensemble'] = False
        self.assertFalse(check_interfaces(settings))

        settings['simulation']['zero_ensemble'] = True
        settings['simulation']['interfaces'] = [1, 2]
        self.assertFalse(check_interfaces(settings))

        settings['simulation']['interfaces'] = [3, 2, 2.5]
        self.assertFalse(check_interfaces(settings))

        settings['simulation']['interfaces'] = [-1.0, -0.5, 0, 0.5, 1]
        self.assertTrue(check_interfaces(settings))


if __name__ == '__main__':
    unittest.main()
