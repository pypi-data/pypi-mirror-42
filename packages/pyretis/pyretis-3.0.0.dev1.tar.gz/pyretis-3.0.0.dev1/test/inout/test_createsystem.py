# -*- coding: utf-8 -*-
# Copyright (c) 2019, PyRETIS Development Team.
# Distributed under the LGPLv2.1+ License. See LICENSE for more info.
"""Test the methods in pyretis.setup.createsystem"""
import os
import logging
import unittest
import numpy as np
from pyretis.core.units import create_conversion_factors
from pyretis.core.box import RectangularBox, TriclinicBox
from pyretis.core.system import System
from pyretis.core.particles import Particles, ParticlesExt
from pyretis.engines.external import ExternalMDEngine
from pyretis.setup.createsystem import (
    list_get,
    guess_particle_mass,
    initial_positions_lattice,
    initial_positions_file,
    create_initial_positions,
    set_up_box,
    create_velocities,
    create_system,
)
logging.disable(logging.CRITICAL)


HERE = os.path.abspath(os.path.dirname(__file__))


def create_test_system():
    """Create a system we can use for testing."""
    settings = {
        'system': {'dimensions': 3, 'units': 'lj', 'type': 'internal'},
        'particles': {
            'position': {
                'generate': 'fcc',
                'repeat': [1, 2, 3],
                'density': 0.9
            }
        }
    }
    create_conversion_factors(settings['system']['units'])
    particles, boxs = initial_positions_lattice(settings)
    box = set_up_box({}, boxs)
    system = System(units='lj', box=box, temperature=1.0)
    system.particles = particles
    return system, settings


class DummyExternal(ExternalMDEngine):
    """A dummy external engine. Only useful for testing!"""

    def __init__(self, input_path, timestep, subcycles):
        """Initialise the dummy engine."""
        super().__init__('External engine for testing!', timestep,
                         subcycles)
        self.input_path = os.path.abspath(input_path)
        self.input_files = {
            'conf': os.path.join(self.input_path, 'dummy_config'),
            'template': os.path.join(self.input_path, 'dummy_template'),
        }

    def step(self, system, name):
        """Initialise the dummy engine."""

    def _read_configuration(self, filename):
        """Initialise the dummy engine."""

    def _reverse_velocities(self, filename, outfile):
        """Initialise the dummy engine."""

    def _extract_frame(self, traj_file, idx, out_file):
        """Initialise the dummy engine."""

    def _propagate_from(self, name, path, ensemble,
                        msg_file, reverse=False):
        """Initialise the dummy engine."""

    def modify_velocities(self, ensemble, vel_settings):
        """Initialise the dummy engine."""


class TestMethods(unittest.TestCase):
    """Test some of the methods from .createsystem"""

    def test_list_get(self):
        """Test the list_get method."""
        lst = [1, 2, 3]
        for idx, i in enumerate(lst):
            item = list_get(lst, idx)
            self.assertEqual(item, i)
        for i in range(3, 10):
            item = list_get(lst, i)
            self.assertEqual(item, lst[-1])

    def test_guess_particle_mass(self):
        """Test the guess_particle_mass method."""
        mass = guess_particle_mass(0, 'He', 'g/mol')
        self.assertAlmostEqual(mass, 4.002602)
        mass = guess_particle_mass(0, 'X', 'g/mol')
        self.assertAlmostEqual(mass, 1.0)

    def test_initial_positions_lattice(self):
        """Test that we can generate positions on a lattice."""
        settings = {'particles': {}, 'system': {'dimensions': 3}}
        settings['particles']['position'] = {
            'generate': 'fcc',
            'repeat': [1, 2, 3],
            'density': 0.9,
        }
        settings['particles']['mass'] = {'X': 1.23}
        settings['particles']['name'] = ['X']
        settings['particles']['ptype'] = [42]
        particles, box = initial_positions_lattice(settings)
        for i in particles.ptype:
            self.assertEqual(i, 42)
        for i in particles.mass:
            self.assertAlmostEqual(i, 1.23)
        for i in particles.name:
            self.assertEqual(i, 'X')
        lenx, leny, lenz = box['high']
        self.assertAlmostEqual(lenx, 1.64414138)
        self.assertAlmostEqual(leny / lenx, 2.0)
        self.assertAlmostEqual(lenz / lenx, 3.0)

    def test_initial_positions_file(self):
        """Test that we can get initial positions from a file."""
        gro = os.path.join(HERE, 'config.gro')
        settings = {
            'particles': {'position': {'input_file': gro}},
            'system': {'dimensions': 3, 'units': 'reduced'}
        }
        create_conversion_factors(settings['system']['units'])
        particles, box, vel = initial_positions_file(settings)
        self.assertTrue(vel)
        self.assertEqual(particles.dim, 3)
        for i in box['cell']:
            self.assertAlmostEqual(i, 20.0)
        for i, j in zip(particles.name, ['Ba', 'Hf', 'O', 'O', 'O']):
            self.assertEqual(i, j)
        # Test override particle names:
        settings['particles']['name'] = ['X', 'Y', 'Z']
        particles, _, _ = initial_positions_file(settings)
        for i, j in zip(particles.name, ['X', 'Y', 'Z', 'Z', 'Z']):
            self.assertEqual(i, j)
        # Test override dimensions:
        settings['system']['dimensions'] = 2
        particles, _, _ = initial_positions_file(settings)
        self.assertEqual(particles.dim, 2)
        # Test missing file info:
        settings['particles']['position'] = {}
        with self.assertRaises(ValueError):
            initial_positions_file(settings)
        # Test unknown format:
        settings['particles']['position'] = {'input_file': 'file.fancy_format'}
        with self.assertRaises(ValueError):
            initial_positions_file(settings)
        # Test .txt format and multiple snapshots:
        settings['particles']['position'] = {
            'input_file': os.path.join(HERE, 'config.txt')
        }
        logging.disable(logging.INFO)
        with self.assertLogs('pyretis.setup.createsystem',
                             level='WARNING'):
            initial_positions_file(settings)
        logging.disable(logging.CRITICAL)
        # Test empty config:
        settings['particles']['position'] = {
            'input_file': os.path.join(HERE, 'config_empty.txt')
        }
        with self.assertRaises(ValueError):
            initial_positions_file(settings)

    def test_create_initial_positions(self):
        """Test that we can create initial positions."""
        # On a lattice:
        settings = {
            'particles': {},
            'system': {'dimensions': 3, 'units': 'reduced'}
        }
        create_conversion_factors(settings['system']['units'])
        settings['particles']['position'] = {
            'generate': 'fcc',
            'repeat': [1, 2, 3],
            'density': 0.9,
        }
        create_initial_positions(settings)
        # From a file:
        settings['particles'] = {
            'position': {'input_file': os.path.join(HERE, 'config.gro')},
        }
        create_initial_positions(settings)
        # And that we fail for other/missing settings:
        settings['particles'] = {
            'position': {'something-else': None},
        }
        with self.assertRaises(ValueError):
            create_initial_positions(settings)

    def test_set_up_box(self):
        """Test that we can set up a box from settings."""
        # From settings:
        settings = {
            'box': {'cell': [1, 2, 3], 'periodic': [True, False, True]}
        }
        box = set_up_box(settings, None)
        self.assertIsInstance(box, RectangularBox)
        for i, j in zip(box.cell, [1., 2., 3.]):
            self.assertAlmostEqual(i, j)
        for i, j in zip(box.periodic, [True, False, True]):
            self.assertEqual(i, j)
        # From dict, with missing settings:
        settings = {}
        boxs = {'cell': [1, 2, 3, 4, 5, 6]}
        box = set_up_box(settings, boxs)
        self.assertIsInstance(box, TriclinicBox)
        mat = np.array([[1., 4., 5.], [0., 2., 6.], [0., 0., 3.]])
        self.assertTrue(np.allclose(box.box_matrix, mat))
        # When we have no settings at all:
        settings = {}
        box = set_up_box(settings, None)
        self.assertIsInstance(box, RectangularBox)
        for i in box.periodic:
            self.assertFalse(i)

    def test_create_velocities(self):
        """Test that we can create velocities."""
        system, settings = create_test_system()
        # If velocities have already be set:
        create_velocities(system, settings, True)
        # If we want to generate them:
        settings['particles']['velocity'] = {
            'generate': 'maxwell',
            'temperature': 4.321,
            'momentum': True,
            'seed': 0
        }
        create_velocities(system, settings, True)
        temp = system.calculate_temperature()
        self.assertAlmostEqual(temp, 4.321)
        # If we want to scale to some energy:
        settings['particles']['velocity'] = {
            'scale': 100.,
        }
        create_velocities(system, settings, True)

    def test_create_system_from_restart(self):
        """Test that we can create from restart settings."""
        system, _ = create_test_system()
        restart = {'restart': {}}
        restart['restart']['system'] = system.restart_info()
        restart['restart']['particles'] = system.particles.restart_info()
        restart['restart']['system']['temperature'] = 1.0
        system2 = create_system(restart)
        self.assertEqual(system.units, system2.units)

    def test_create_system_settings(self):
        """Test creation of system from settings."""
        # Internal engine:
        # On a lattice:
        settings = {
            'particles': {
                'position': {
                    'generate': 'fcc',
                    'repeat': [1, 2, 3],
                    'density': 0.9,
                },
            },
            'system': {
                'dimensions': 3,
                'units': 'reduced',
                'temperature': 1.0
            }
        }
        create_conversion_factors(settings['system']['units'])
        system = create_system(settings)
        self.assertIsInstance(system.particles, Particles)
        settings['engine'] = {'type': 'external',
                              'input_files': {}}
        system = create_system(settings)
        self.assertIsInstance(system.particles, ParticlesExt)
        # Test that missing 'particles' in settings and internal engine gives
        # an KeyError

        settings['simulation'] = 'restart'
        # TODO: Should this give an error when particles is missing?
        # eraseme. Not anymore, particles can also be imported from restart
        # del settings['particles']
        # self.assertRaises(KeyError, lambda: create_system(settings))

        del settings['system']
        with self.assertRaises(KeyError):
            create_system(settings)

    def test_create_system(self):
        """Test that we can use the create_system method."""
        # With restart:
        system, settings = create_test_system()
        restart = {'restart': {}}
        restart['restart']['system'] = system.restart_info()
        restart['restart']['particles'] = system.particles.restart_info()

        system2, settings = create_test_system()
        system2.load_restart_info(restart)
        system4 = create_system(restart)

        self.assertIsInstance(system, System)
        self.assertIsInstance(system2, System)
        self.assertIsInstance(system4, System)

        # todo wish-list to make restarts always possible
        # self.assertTrue(system2 == system4)

        # From settings:
        settings = {
            'particles': {},
            'system': {'dimensions': 3, 'units': 'reduced', 'temperature': 1.0}
        }
        create_conversion_factors(settings['system']['units'])
        settings['particles']['position'] = {
            'generate': 'fcc',
            'repeat': [1, 2, 3],
            'density': 0.9,
        }
        system3 = create_system(settings)
        self.assertIsInstance(system3.particles, Particles)
        self.assertIsInstance(system3, System)


if __name__ == '__main__':
    unittest.main()
