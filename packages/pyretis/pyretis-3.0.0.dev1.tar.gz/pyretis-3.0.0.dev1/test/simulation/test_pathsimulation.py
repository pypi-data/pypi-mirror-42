# -*- coding: utf-8 -*-
# Copyright (c) 2019, PyRETIS Development Team.
# Distributed under the LGPLv2.1+ License. See LICENSE for more info.
"""Test the path simulation classes."""
from io import StringIO
import unittest
from unittest.mock import patch
import logging
import tempfile
import os
import copy
from pyretis.simulation.path_simulation import (
    PathSimulation,
    SimulationRETIS,
)
from pyretis.inout.settings import _add_default_settings
from pyretis.inout.settings import fill_up_tis_and_retis_settings
from pyretis.setup.createsimulation import create_ensembles
from .test_helpers import TEST_SETTINGS

logging.disable(logging.CRITICAL)

HERE = os.path.abspath(os.path.dirname(__file__))

SETTINGS1 = {
    'simulation': {
        'task': 'tis',
        'steps': 10,
        'interfaces': [-0.9, -0.9, 1.0],
        'seed': 1,
        'rgen': 'rgen',
    },
    'system': {'units': 'lj', 'temperature': 0.1, 'dimensions': 1},
    'engine': {
        'class': 'Langevin',
        'gamma': 0.3,
        'high_friction': False,
        'seed': 321,
        'timestep': 0.002
    },
    'potential': [{'a': 1.0, 'b': 2.0, 'c': 0.0, 'class': 'DoubleWell'}],
    'orderparameter': {
        'class': 'Position',
        'dim': 'x',
        'index': 0,
        'name': 'Position',
        'periodic': False
    },
    'initial-path': {'method': 'kick'},
    'particles': {'position': {'input_file': 'initial.xyz'}},
    'retis': {
        'swapfreq': 0.5,
        'nullmoves': True,
        'swapsimul': True,
    },
    'tis': {
        'freq': 0.5,
        'maxlength': 2000,
        'aimless': True,
        'allowmaxlength': False,
        'sigma_v': -1,
        'seed': 1,
        'rgen': 'rgen',
        'zero_momentum': False,
        'rescale_energy': False,
    },
}


def create_variables(exe_path=None):
    """Create system, engine, order parameter etc."""
    settings = {key: copy.deepcopy(val) for key, val in TEST_SETTINGS.items()}
    settings['engine'] = {'class': 'Langevin', 'gamma': 0.3,
                          'high_friction': False,
                          'timestep': 0.002}
    settings['orderparameter'] = {'class': 'Position',
                                  'index': 0}

    if exe_path is not None:
        settings['simulation'] = {'exe_path': exe_path}
    _add_default_settings(settings)
    settings['particles']['type'] = 'internal'
    settings['simulation']['interfaces'] = [-1.0, 0.0, 1.0, 2.0]
    settings['simulation']['task'] = 'tis'
    settings['simulation']['zero_ensemble'] = True
    settings['simulation']['flux'] = True
    settings['retis'] = {'rgen': 'rgen'}
    with patch('sys.stdout', new=StringIO()):
        fill_up_tis_and_retis_settings(settings)
        ensembles = create_ensembles(settings)
    return settings, ensembles


def create_variables1(exe_path=None):
    """Create system, engine, order parameter etc."""
    settings = {key: copy.deepcopy(val) for key, val in SETTINGS1.items()}
    _add_default_settings(settings)
    settings['particles']['position']['input_file'] =\
        os.path.join(HERE, 'initial.xyz')
    settings['particles']['type'] = 'internal'
    settings['simulation']['task'] = 'retis'
    settings['simulation']['zero_ensemble'] = True
    settings['simulation']['flux'] = True
    settings['simulation']['exe_path'] = exe_path

    with patch('sys.stdout', new=StringIO()):
        fill_up_tis_and_retis_settings(settings)
        ensembles = create_ensembles(settings)
    return settings, ensembles


class TestPathSimulation(unittest.TestCase):
    """Run the tests for the PathSimulation class."""

    def test_init(self):
        """Test that we can create the simulation object."""
        settings, ensembles = create_variables()
        simulation = PathSimulation(ensembles, settings, {})
        self.assertTrue(hasattr(simulation, 'rgen'))
        simulation = PathSimulation(ensembles, settings, {})
        self.assertEqual(len(simulation.ensembles), len(ensembles))
        for i, j in zip(simulation.ensembles, ensembles):
            self.assertIs(i, j)
        self.assertTrue(simulation.settings['tis']['aimless'])
        settings['engine']['sigma_v'] = 0.1
        simulation = PathSimulation(ensembles, settings, {})
        self.assertTrue(simulation.settings['tis']['aimless'])
        del settings['tis']
        with self.assertRaises(ValueError):
            simulation = PathSimulation(ensembles, settings, {})

    def test_restart_info(self):
        """Test generation of restart info."""
        settings, ensembles = create_variables()
        simulation = PathSimulation(ensembles, settings, {})
        info = simulation.restart_info()
        for key in ('cycle', 'rgen'):
            self.assertIn(key, info['simulation'])
        self.assertEqual(info['simulation']['rgen']['state'][2], 624)
        self.assertIn('engine', info)

    def test_write_restart_file(self):
        """Test that we can create the restart files."""
        with tempfile.TemporaryDirectory() as tempdir:
            settings, ensembles = create_variables(exe_path=tempdir)
            simulation = PathSimulation(ensembles, settings, {})
            simulation.set_up_output(settings)
            simulation.write_restart(now=True)
            dirs = [i.name for i in os.scandir(tempdir) if i.is_dir()]
            self.assertEqual(len(dirs), 4)
            for i in ensembles:
                self.assertIn(i['path_ensemble'].ensemble_name_simple, dirs)
                for j in os.scandir(
                        i['path_ensemble'].directory['path_ensemble']):
                    if j.is_file():
                        self.assertEqual('ensemble.restart', j.name)
            files = [i.name for i in os.scandir(tempdir) if i.is_file()]
            self.assertEqual(len(files), 1)
            self.assertIn('pyretis.restart', files)

    def test_initiation(self):
        """Test the initiation method."""
        with tempfile.TemporaryDirectory() as tempdir:
            # Generate a input file in the temp directory
            scrivi = open(os.path.join(tempdir, 'initial.xyz'), 'w')
            scrivi.write('1\n \n Ar  -1.0  -0.0  -0.0 ')
            scrivi.close()

            settings, ensembles = create_variables1(exe_path=tempdir)
            simulation = PathSimulation(ensembles, settings, {})
            simulation.set_up_output(settings)
            with patch('sys.stdout', new=StringIO()):
                self.assertTrue(simulation.initiate(settings))
            # Check the soft exit option:
            open(os.path.join(tempdir, 'EXIT'), 'w').close()
            with patch('sys.stdout', new=StringIO()):
                self.assertFalse(simulation.initiate(settings))


class TestSimulationRETIS(unittest.TestCase):
    """Run the tests for the SimulationRETIS class."""

    def test_step(self):
        """Test the initiation method."""
        moves = {'move-0': 'tis', 'move-1': 'tis', 'move-2': 'tis'}

        with tempfile.TemporaryDirectory() as tempdir:
            settings, ensembles = create_variables1(exe_path=tempdir)
            simulation = SimulationRETIS(ensembles, settings, {})
            simulation.set_up_output(settings)
            with patch('sys.stdout', new=StringIO()):
                self.assertTrue(simulation.initiate(settings))
                result = simulation.step()
                for key, move in moves.items():
                    self.assertIn(key, result)
                    self.assertEqual(move, result[key])


if __name__ == '__main__':
    unittest.main()
