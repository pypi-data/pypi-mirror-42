# -*- coding: utf-8 -*-
# Copyright (c) 2019, PyRETIS Development Team.
# Distributed under the LGPLv2.1+ License. See LICENSE for more info.
"""Test the methods in pyretis.setup.createsimulation"""
import os
import logging
import unittest
import numpy as np
from pyretis.engines.internal import VelocityVerlet
from pyretis.core.units import create_conversion_factors
from pyretis.core.system import System
from pyretis.core.particles import Particles
from pyretis.core.pathensemble import (
    PathEnsemble,
    PathEnsembleExt,
)
from pyretis.setup.createsimulation import (
    create_ensemble,
    create_ensembles,
    create_nve_simulation,
    create_mdflux_simulation,
    create_umbrellaw_simulation,
    create_tis_simulation,
    create_retis_simulation,
    create_simulation,
)
from pyretis.tools.lattice import generate_lattice
from pyretis.forcefield.forcefield import ForceField
from pyretis.forcefield.potentials import PairLennardJonesCutnp
from pyretis.core.box import create_box
from pyretis.inout.settings import SECTIONS

from pyretis.simulation.md_simulation import (
    SimulationNVE,
    SimulationMDFlux,
)
from pyretis.simulation.mc_simulation import UmbrellaWindowSimulation
from pyretis.simulation.path_simulation import (
    SimulationTIS,
    SimulationRETIS
)
from pyretis.inout.settings import fill_up_tis_and_retis_settings
from pyretis.inout.checker import check_ensemble
from pyretis.core.random_gen import create_random_generator

logging.disable(logging.CRITICAL)


HERE = os.path.abspath(os.path.dirname(__file__))

ORDER_ERROR_MSG = 'No order parameter created!'
ORDER_ERROR_MSG_ENS_0 = 'No order parameter created in ensemble 0!'
ORDER_ERROR_MSG_ENS_2 = 'No order parameter created in ensemble 2!'

MISSING_STEPS_ERROR_MSG = 'Simulation setting "steps" is missing!'
MISSING_INTERFACES_ERROR_MSG = 'Simulation setting "interfaces" is missing!'


def create_test_system():
    """Create a system we can use for testing."""
    create_conversion_factors('lj')
    xyz, size = generate_lattice('fcc', [2, 2, 2], density=0.9)
    size = np.array(size)
    box = create_box(low=size[:, 0], high=size[:, 1])
    system = System(units='lj', box=box, temperature=2.0)
    system.particles = Particles(dim=3)
    for pos in xyz:
        system.add_particle(pos, vel=np.zeros_like(pos),
                            force=np.zeros_like(pos),
                            mass=1.0, name='Ar', ptype=0)
    gen_settings = {'distribution': 'maxwell', 'momentum': True, 'seed': 0}
    system.generate_velocities(**gen_settings)
    potentials = [
        PairLennardJonesCutnp(dim=3, shift=True, mixing='geometric'),
    ]
    parameters = [
        {0: {'sigma': 1, 'epsilon': 1, 'rcut': 2.5}},
    ]
    system.forcefield = ForceField(
        'Lennard Jones force field',
        potential=potentials,
        params=parameters,
    )
    return system


class TestMethods(unittest.TestCase):
    """Test some of the methods from .createsimulation."""

    def test_create_path_ensemble(self):
        """Test create_path_ensemble."""
        path_ensemble = PathEnsemble(2, [-1., 0, 1])
        self.assertEqual(path_ensemble.ensemble_number, 2)
        self.assertIsInstance(path_ensemble, PathEnsemble)
        path_ensemble = PathEnsembleExt(2, [-1., 0, 1])
        self.assertIsInstance(path_ensemble, PathEnsembleExt)
        self.assertEqual(path_ensemble.ensemble_number, 2)
        # Test with some "missing" settings:
        path_ensemble = PathEnsemble(2, [-1., 0, 1])
        with self.assertRaises(KeyError):
            settings = {'simulation': {'interfaces': [-1., 0.]}}
            create_ensemble(settings)

    def test_create_ensemble(self):
        """Test create_ensemble."""
        settings = {'simulation': {'task': 'retis',
                                   'interfaces': [-1., 0, 1],
                                   'exe_path': HERE,
                                   'zero_ensemble': True,
                                   'flux': True},
                    'orderparameter': {'class': 'Position',
                                       'dim': 'x',
                                       'index': 0,
                                       'periodic': False},
                    'particles': {'type': 'internal'},
                    'system': {'units': 'lj',
                               'obj': create_test_system()},
                    'engine': {'obj': VelocityVerlet(0.002)},
                    'tis': {}}

        fill_up_tis_and_retis_settings(settings)
        check_ensemble(settings)
        ensembles = create_ensembles(settings)
        for i_ens, ensemble in enumerate(ensembles):
            path_ensemble = ensemble['path_ensemble']
            self.assertEqual(path_ensemble.ensemble_number, i_ens)
            self.assertIsInstance(path_ensemble, PathEnsemble)

        for i_ens in range(len(ensembles)):
            settings['ensemble'][i_ens]['particles']['type'] = 'external'

        ensembles = create_ensembles(settings)
        for i_ens, ensemble in enumerate(ensembles):
            path_ensemble = ensemble['path_ensemble']
            self.assertIsInstance(path_ensemble, PathEnsembleExt)
            self.assertEqual(path_ensemble.ensemble_number, i_ens)

    def test_create_ensembles(self):
        """Test create_ensembles."""
        settings = {'simulation': {'task': 'tis',
                                   'interfaces': [-1., 0., 1.0, 2.0],
                                   'exe_path': HERE,
                                   'zero_ensemble': False,
                                   'flux': False},
                    'tis': {},
                    'orderparameter': {'class': 'Position',
                                       'dim': 'x',
                                       'index': 0,
                                       'periodic': False},
                    'particles': {'type': 'internal'},
                    'system': {'units': 'lj',
                               'obj': create_test_system()},
                    'engine': {'obj': VelocityVerlet(0.002)}}
        fill_up_tis_and_retis_settings(settings)
        check_ensemble(settings)
        ensembles = create_ensembles(settings)
        for ens in ensembles:
            self.assertIsInstance(ens['path_ensemble'], PathEnsemble)

    def test_fail_simulation(self):
        """Test fail simulation."""
        settings = {'simulation': {'task': 'fake'}}
        with self.assertRaises(ValueError) as err:
            create_simulation(settings)

    def test_create_nve_simulation(self):
        """Test create_nve_simulation."""
        settings = {'simulation': {'task': 'md-nve', 'steps': 10},
                    'system': {'obj': create_test_system()},
                    'engine': {'obj': VelocityVerlet(0.002)}}
        sim = create_nve_simulation(settings)
        self.assertIsInstance(sim, SimulationNVE)
        self.assertEqual(sim.simulation_type,
                         SimulationNVE.simulation_type)
        del settings['simulation']['steps']
        with self.assertRaises(ValueError):
            create_nve_simulation(settings)

    def test_create_mdflux_simulation(self):
        """Test create_mdflux_simulation."""
        settings = {'simulation': {'task': 'mdflux'},
                    'system': {'obj': create_test_system()},
                    'engine': {'obj': VelocityVerlet(0.002)}}

        with self.assertRaises(ValueError) as err:
            create_mdflux_simulation(settings)
        self.assertEqual(ORDER_ERROR_MSG, str(err.exception))
        settings['orderparameter'] = {'class': 'Position',
                                      'dim': 'x', 'index': 0,
                                      'periodic': False}
        # Test that we fail because required setting "steps" are missing:
        with self.assertRaises(ValueError) as err:
            create_mdflux_simulation(settings)
        self.assertEqual(MISSING_STEPS_ERROR_MSG, str(err.exception))
        settings['simulation']['steps'] = 10
        # Test that we fail because required setting "interfaces" are
        # missing:
        with self.assertRaises(ValueError) as err:
            create_mdflux_simulation(settings)
        self.assertEqual(MISSING_INTERFACES_ERROR_MSG, str(err.exception))
        settings['simulation']['interfaces'] = [0, 1]
        sim = create_mdflux_simulation(settings)
        self.assertIsInstance(sim, SimulationMDFlux)

    def test_create_umbrellawsimulation(self):
        """Test create_umbreallaw_simulation."""
        settings = {'simulation': {'task': 'umbrellawindow', 'seed': 3},
                    'system': {'obj': create_test_system}}

        with self.assertRaises(ValueError):
            create_umbrellaw_simulation(settings)
        settings['simulation']['umbrella'] = [-1.0, 0.0]
        with self.assertRaises(ValueError):
            create_umbrellaw_simulation(settings)
        settings['simulation']['overlap'] = -0.5
        with self.assertRaises(ValueError):
            create_umbrellaw_simulation(settings)
        settings['simulation']['maxdx'] = 1.0
        with self.assertRaises(ValueError):
            create_umbrellaw_simulation(settings)
        settings['simulation']['mincycle'] = 10
        sim = create_umbrellaw_simulation(settings)
        self.assertIsInstance(sim, UmbrellaWindowSimulation)

    def test_create_tis_simulation(self):
        """Test create_tis_simulation."""
        settings = {'simulation': {'task': 'tis',
                                   'interfaces': [-1., 0., 1.],
                                   'exe_path': HERE,
                                   'zero_ensemble': False,
                                   'flux': False},
                    'tis': SECTIONS['tis'],
                    'particles': {'type': 'internal'},
                    'system': {'obj': create_test_system()},
                    'engine': {'obj': VelocityVerlet(0.002)}}
        fill_up_tis_and_retis_settings(settings)

        # Test that the set up fails, when we did not define an
        # order parameter and the engine wants it:
        with self.assertRaises(ValueError) as err:
            create_tis_simulation(settings)
        self.assertEqual(ORDER_ERROR_MSG_ENS_2, str(err.exception))
        # Continue testing with an order parameter defined:
        settings['orderparameter'] = {'class': 'Position',
                                      'dim': 'x', 'index': 0,
                                      'periodic': False}
        # Test that we fail when we are missing some settings:
        with self.assertRaises(ValueError) as err:
            create_tis_simulation(settings)
        # it should raise also missing steps
        self.assertEqual(ORDER_ERROR_MSG_ENS_2, str(err.exception))
        settings['simulation']['steps'] = 10
        fill_up_tis_and_retis_settings(settings)
        sim = create_tis_simulation(settings)
        self.assertIsInstance(sim, SimulationTIS)

    def test_create_tis_multiple_simulations(self):
        """Test create_tis_simulations."""
        settings = {'simulation': {'task': 'tis',
                                   'interfaces': [-1., 0., 1., 2],
                                   'steps': 10,
                                   'exe_path': HERE,
                                   'zero_ensemble': False,
                                   'flux': False},
                    'tis': SECTIONS['tis'],
                    'orderparameter': {'class': 'Position',
                                       'dim': 'x',
                                       'index': 0,
                                       'periodic': False},
                    'output': SECTIONS['output'],
                    'particles': {'type': 'internal'},
                    'system': {'units': 'lj',
                               'obj': create_test_system()},
                    'engine': {'obj': VelocityVerlet(0.002)}}
        fill_up_tis_and_retis_settings(settings)
        simulations = create_tis_simulation(settings)
        self.assertIsInstance(simulations, SimulationTIS)

    def test_create_retis_simulation(self):
        """Test create_retis_simulation."""
        settings = {'simulation': {'task': 'retis',
                                   'interfaces': [-1., 0., 1.],
                                   'exe_path': '.',
                                   'zero_ensemble': True,
                                   'flux': True},
                    'tis': SECTIONS['tis'],
                    'retis': SECTIONS['retis'],
                    'engine': {'obj': VelocityVerlet(0.002)},
                    'particles': {'type': 'internal'},
                    'system': {'type': 'internal',
                               'units': 'lj',
                               'obj': create_test_system()}}

        del settings['tis']['ensemble_number']
        fill_up_tis_and_retis_settings(settings)
        with self.assertRaises(ValueError):
            create_retis_simulation(settings)

        # Test that we fail without an order parameter defined:
        with self.assertRaises(ValueError) as err:
            create_retis_simulation(settings)
        self.assertEqual(ORDER_ERROR_MSG_ENS_0, str(err.exception))
        settings['orderparameter'] = {'class': 'Position',
                                      'dim': 'x', 'index': 0,
                                      'periodic': False}

        fill_up_tis_and_retis_settings(settings)
        # Test that we fail when we are missing some settings:
        with self.assertRaises(ValueError) as err:
            create_retis_simulation(settings)
        self.assertEqual(MISSING_STEPS_ERROR_MSG, str(err.exception))
        settings['simulation']['steps'] = 10
        sim = create_retis_simulation(settings)
        self.assertIsInstance(sim, SimulationRETIS)

    def test_create_simulation(self):
        """Test create_simulation."""
        settings = {'simulation': {'task': 'does-not-exist'}}
        with self.assertRaises(ValueError):
            create_simulation(settings)

    def test_create_simulationnve(self):
        """Test create_simulation for NVE"""
        settings = {'simulation': {'steps': 10, 'task': 'md-nve'},
                    'system': {'obj': create_test_system()},
                    'engine': {'obj': VelocityVerlet(0.002)}}
        sim = create_simulation(settings)
        self.assertIsInstance(sim, SimulationNVE)

    def test_create_simulationmdflux(self):
        """Test create_simulation for MD-Flux"""
        settings = {'simulation': {'steps': 10,
                                   'task': 'md-flux',
                                   'interfaces': [-1.0]},
                    'system': {'obj': create_test_system()},
                    'engine': {'obj': VelocityVerlet(0.002)},
                    'orderparameter': {'class': 'Position',
                                       'dim': 'x',
                                       'index': 0,
                                       'periodic': False}}
        sim = create_mdflux_simulation(settings)
        self.assertIsInstance(sim, SimulationMDFlux)

    def test_create_simulationumb(self):
        """Test create_simulation for UmbrellaWindow"""
        settings = {'simulation': {'task': 'umbrellawindow',
                                   'umbrella': [-1.0, 0.0],
                                   'overlap': -0.5,
                                   'maxdx': 1.0,
                                   'mincycle': 10},
                    'system': {'obj': create_test_system()},
                    'orderparameter': {'class': 'Position',
                                       'dim': 'x',
                                       'index': 0,
                                       'periodic': False}}
        sim = create_umbrellaw_simulation(settings)
        self.assertIsInstance(sim, UmbrellaWindowSimulation)

    def test_create_simulationtis1(self):
        """Test create_simulation for SimulationTIS single."""
        # TIS:
        settings = {'simulation': {'task': 'tis',
                                   'interfaces': [-1., 0., 1.],
                                   'steps': 10,
                                   'exe_path': HERE,
                                   'zero_ensemble': False,
                                   'flux': False},
                    'tis': SECTIONS['tis'],
                    'particles': {'type': 'internal'},
                    'system': {'obj': create_test_system(),
                               'units': 'lj'},
                    'engine': {'obj': VelocityVerlet(0.002)},
                    'orderparameter': {'class': 'Position',
                                       'dim': 'x',
                                       'index': 0,
                                       'periodic': False},
                    'output': SECTIONS['output']}
        fill_up_tis_and_retis_settings(settings)
        sim = create_tis_simulation(settings)
        self.assertIsInstance(sim, SimulationTIS)

    def test_create_simulationtis2(self):
        """Test create_simulation for SimulationTIS multiple."""
        # TIS-multiple:
        settings = {'simulation': {'task': 'tis',
                                   'interfaces': [-1., 0., 1., 2.0],
                                   'steps': 10,
                                   'exe_path': HERE,
                                   'zero_ensemble': False,
                                   'flux': False},
                    'tis': SECTIONS['tis'],
                    'orderparameter': {'class': 'Position',
                                       'dim': 'x',
                                       'index': 0,
                                       'periodic': False},
                    'particles': {'type': 'internal'},
                    'system': {'obj': create_test_system(),
                               'units': 'lj'},
                    'engine': {'obj': VelocityVerlet(0.002)},
                    'output': SECTIONS['output']}
        fill_up_tis_and_retis_settings(settings)
        simulations = create_tis_simulation(settings)
        self.assertIsInstance(simulations, SimulationTIS)

    def test_create_simulationretis(self):
        """Test create_simulation for SimulationRETIS."""
        settings = {'system': {'obj': create_test_system(),
                               'units': 'lj'},
                    'particles': {'type': 'internal'},
                    'engine': {'obj': VelocityVerlet(0.002)},
                    'simulation': {'steps': 10,
                                   'task': 'retis',
                                   'interfaces': [-1., 0., 1.],
                                   'exe_path': HERE,
                                   'zero_ensemble': True,
                                   'flux': True},
                    'tis': SECTIONS['tis'],
                    'retis': SECTIONS['retis'],
                    'orderparameter': {'class': 'Position',
                                       'dim': 'x',
                                       'index': 0,
                                       'periodic': False}}

        fill_up_tis_and_retis_settings(settings)
        sim = create_retis_simulation(settings)
        self.assertIsInstance(sim, SimulationRETIS)


if __name__ == '__main__':
    unittest.main()
