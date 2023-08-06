# -*- coding: utf-8 -*-
# Copyright (c) 2019, PyRETIS Development Team.
# Distributed under the LGPLv2.1+ License. See LICENSE for more info.
"""Test methods for doing TIS."""
import copy
from io import StringIO
import logging
import unittest
from unittest.mock import patch
import numpy as np
from pyretis.core import System, create_box, Particles
from pyretis.initiation import initiate_path_simulation
from pyretis.setup import create_force_field, create_engine
from pyretis.inout.checker import check_engine
from pyretis.setup.createsimulation import create_tis_simulation
from pyretis.forcefield import ForceField
from pyretis.core.tis import time_reversal, shoot
from pyretis.inout.settings import fill_up_tis_and_retis_settings
from pyretis.setup.createsimulation import create_ensemble
from pyretis.inout.checker import check_ensemble
from pyretis.core.common import big_fat_comparer
from pyretis.core.random_gen import (
    MockRandomGenerator,
    create_random_generator)

from .help import (
    make_internal_path,
    MockPotential,
    MockEngine,
    MockEngine2,
    MockOrder,
    MockOrder2,
    SameOrder,
    NegativeOrder,
)

logging.disable(logging.CRITICAL)

TISMOL_001 = [[262, 'ACC', 'ki', -0.903862, 1.007330, 1, 262],
              [262, 'BWI', 'tr', -0.903862, 1.007330, 262, 1],
              [12, 'BWI', 'sh', 0.957091, 1.002750, 12, 1],
              [262, 'BWI', 'tr', -0.903862, 1.007330, 262, 1],
              [262, 'BWI', 'tr', -0.903862, 1.007330, 262, 1],
              [262, 'BWI', 'tr', -0.903862, 1.007330, 262, 1],
              [77, 'BWI', 'sh', 0.522609, 1.003052, 77, 1],
              [262, 'BWI', 'tr', -0.903862, 1.007330, 262, 1],
              [262, 'BWI', 'tr', -0.903862, 1.007330, 262, 1],
              [262, 'BWI', 'tr', -0.903862, 1.007330, 262, 1],
              [262, 'BWI', 'tr', -0.903862, 1.007330, 262, 1]]


def create_ensemble_and_paths(example=0):
    """Return some test data we can use."""
    # Make some paths for the ensembles.
    interfaces = [(-1., -1., 10.), (-1., 0., 10.),
                  (-1., 1., 10.), (-1., 2., 10.)]
    starts = [(0, -1.1), (0, -1.05), (0, -1.123), (0, -1.01)]
    ends = [(100, -1.2), (100, -1.3), (100, -1.01),
            (100, 10.01)]
    maxs = [(50, -0.2), (50, 0.5), (50, 2.5), (100, 10.01)]

    settings = prepare_test_settings()
    start = starts[example]
    end = ends[example]
    mxx = maxs[example]
    settings['simulation']['interfaces'] = interfaces[example]
    settings['simulation']['zero_ensemble'] = False
    if example == 3:
        settings['tis']['detect'] = interfaces[example][2]
    else:
        settings['tis']['detect'] = interfaces[example][1]
    settings['tis']['ensemble_number'] = example
    with patch('sys.stdout', new=StringIO()):
        ensemble = create_ensemble(settings)
    path = make_internal_path(start, end, mxx, ensemble['interfaces'][1])
    ensemble['path_ensemble'].add_path_data(path, 'ACC')
    return ensemble


def create_simple_system():
    """Create a simple system for testing."""
    box = create_box(periodic=[False])
    system = System(units='reduced', temperature=1.0, box=box)
    particles = Particles(dim=1)
    particles.add_particle(np.zeros((1, 1)), np.zeros((1, 1)),
                           np.zeros((1, 1)))
    system.particles = particles
    system.forcefield = ForceField('empty force field',
                                   potential=[MockPotential()])
    return system


def prepare_test_settings():
    """Prepare a good set of settings"""
    settings = dict()
    # Basic settings for the simulation:
    settings['simulation'] = {'task': 'tis',
                              'steps': 10,
                              'exe_path': '.',
                              'interfaces': [-0.9, -0.9, 1.0],
                              'zero_ensemble': False,
                              'flux': False}
    settings['system'] = {'units': 'lj',
                          'temperature': 0.07}
    # Basic settings for the Langevin integrator:
    settings['engine'] = {'class': 'Langevin',
                          'gamma': 0.3,
                          'high_friction': False,
                          'seed': 1,
                          'exe_path': '.',
                          'rgen': 'rgen',
                          'timestep': 0.002}
    # Fake initial position for particles:
    settings['particles'] = {'type': 'internal',
                             'position': {'generate': 'fcc',
                                          'repeat': [1, 2, 3],
                                          'density': 0.9
                                          }}
    # Potential parameters:
    # The potential is: `V_\text{pot} = a x^4 - b (x - c)^2`.
    settings['potential'] = [{'a': 1.0, 'b': 2.0, 'c': 0.0,
                              'class': 'DoubleWell'}]
    # Settings for the order parameter:
    settings['orderparameter'] = {'class': 'Position',
                                  'dim': 'x', 'index': 0, 'name': 'Position',
                                  'periodic': False}
    # TIS specific settings:
    settings['tis'] = {'freq': 0.5,
                       'maxlength': 20000,
                       'aimless': True,
                       'allowmaxlength': False,
                       'sigma_v': -1,
                       'seed': 1,
                       'rgen': 'mock',
                       'zero_momentum': False,
                       'rescale_energy': False}
    settings['initial-path'] = {'method': 'kick'}

    return settings


def prepare_test_simulation():
    """Prepare a small system we can integrate."""
    settings = prepare_test_settings()

    box = create_box(periodic=[False])
    system = System(temperature=settings['system']['temperature'],
                    units=settings['system']['units'], box=box)
    system.particles = Particles(dim=system.get_dim())
    system.forcefield = create_force_field(settings)
    system.add_particle(np.array([-1.0]), mass=1, name='Ar', ptype=0)
    check_engine(settings)
    engine = create_engine(settings)
    settings['system']['obj'] = system
    settings['engine']['obj'] = engine

    fill_up_tis_and_retis_settings(settings)
    check_ensemble(settings)
    simulation = create_tis_simulation(settings)
    # here we do a hack so that the simulation and Langevin integrator
    # both use the same random generator:
    simulation.ensembles[0]['rgen'] =\
        MockRandomGenerator(settings['tis']['seed'])
    simulation.ensembles[0]['system'] = system
    simulation.ensembles[0]['order_function'] = MockOrder()
    system.particles.vel = np.array([[0.78008019924163818]])
    return simulation, settings


def prepare_test_simulation_rnd():
    """Prepare a small system we can integrate."""
    settings = prepare_test_settings()
    settings['tis']['rgen'] = 'rgen'

    box = create_box(periodic=[False])
    system = System(temperature=settings['system']['temperature'],
                    units=settings['system']['units'], box=box)
    system.particles = Particles(dim=system.get_dim())
    system.forcefield = create_force_field(settings)
    system.add_particle(np.array([-1.0]), mass=1, name='Ar', ptype=0)
    check_engine(settings)
    engine = create_engine(settings)
    settings['system']['obj'] = system
    settings['engine']['obj'] = engine

    fill_up_tis_and_retis_settings(settings)
    check_ensemble(settings)
    simulation = create_tis_simulation(settings)
    rgen = create_random_generator({'seed': 0})
    simulation.ensembles[0]['rgen'] = rgen
    simulation.ensembles[0]['system'] = system
    simulation.ensembles[0]['order_function'] = MockOrder()

    simulation.ensembles[0]['path_ensemble'].start_condition = 'L'
    system.particles.vel = np.array([[0.78008019924163818]])
    return simulation, settings


class TISTest(unittest.TestCase):
    """Run a test for the TIS algorithm.

    This test will compare with results obtained by the old
    FORTRAN TISMOL program.
    """

    def test_tis_001(self):
        """Test a TIS simulation for 001."""
        simulation, in_settings = prepare_test_simulation()
        ensemble = simulation.ensembles[0]
        # Magic tricks to have a backward compatibility
        ensemble['engine'].rgen = ensemble['rgen']
        ensemble['path_ensemble'].rgen = ensemble['engine'].rgen
        ensemble['path_ensemble'].start_condition = 'L'
        for i in range(10):
            if i == 0:
                with patch('sys.stdout', new=StringIO()):
                    for _ in initiate_path_simulation(simulation, in_settings):
                        logging.debug('Running initialisation')
            else:
                simulation.step()

            path = ensemble['path_ensemble'].paths[-1]
            path_data = [path['length'], path['status'], path['generated'][0],
                         path['ordermin'][0], path['ordermax'][0]]
            for j in (0, 1, 2):
                self.assertEqual(path_data[j], TISMOL_001[i][j])
            self.assertAlmostEqual(path_data[3], TISMOL_001[i][3], places=6)
            self.assertAlmostEqual(path_data[4], TISMOL_001[i][4], places=6)

    def test_tis_restart(self):
        """Test various TIS simulation restart."""
        sim1, in_settings1 = prepare_test_simulation_rnd()
        sim2, _ = prepare_test_simulation_rnd()
        sim3, in_settings3 = prepare_test_simulation_rnd()

        for i in range(11):
            if i == 0:
                with patch('sys.stdout', new=StringIO()):
                    for _ in initiate_path_simulation(sim1, in_settings1):
                        logging.debug('Running initialisation')
                    for _ in initiate_path_simulation(sim3, in_settings3):
                        logging.debug('Running initialisation')
            else:
                sim1.step()
                sim3.step()

            lp1 = sim1.ensembles[0]['path_ensemble'].last_path
            lp3 = sim3.ensembles[0]['path_ensemble'].last_path

            pe1 = sim1.ensembles[0]['path_ensemble']
            pe3 = sim3.ensembles[0]['path_ensemble']
            self.assertTrue(lp1 == lp3)
            self.assertTrue(pe1 == pe3)

        sim3.step()

        lp1 = sim1.ensembles[0]['path_ensemble'].last_path
        lp3 = sim3.ensembles[0]['path_ensemble'].last_path

        with patch('sys.stdout', new=StringIO()):
            self.assertFalse(big_fat_comparer(lp1.restart_info(),
                                              lp3.restart_info()))
        sim2.load_restart_info(copy.deepcopy(sim1.restart_info()))

        rst1 = {}
        rst1['order_function'] = sim1.ensembles[0]['order_function']
        rst1['path_ensemble'] = \
            sim1.ensembles[0]['path_ensemble'].restart_info()
        rst1['engine'] = sim1.ensembles[0]['engine'].restart_info()
        rst1['system'] = sim1.ensembles[0]['system'].restart_info()
        rst1['ens-rgen'] = sim1.ensembles[0]['rgen'].get_state()

        with patch('sys.stdout', new=StringIO()):
            sim2.ensembles[0]['engine'].load_restart_info(rst1['engine'])
            sim2.ensembles[0]['system'].load_restart_info(rst1['system'])
            sim2.ensembles[0]['rgen'].set_state(rst1['ens-rgen'])
            sim2.ensembles[0]['order_function'] = rst1['order_function']
            sim2.ensembles[0]['path_ensemble'].load_restart_info(
                rst1['path_ensemble'])

        rst2 = sim2.ensembles[0]['rgen'].get_state()
        self.assertTrue(big_fat_comparer(rst1['ens-rgen'], rst2))

        lp1 = sim1.ensembles[0]['path_ensemble'].last_path
        lp2 = sim2.ensembles[0]['path_ensemble'].last_path
        self.assertEqual(lp1, lp2)
        # TODO: This is a hack: the force field is not loaded via
        # restart for systems. Previously when there were only one
        # system, it was assumed that the force field could just be
        # set up again from the input settings. Structurally, I don't
        # think the force field longer fits as a system attribute. It
        # is perhaps better as an ensemble attribute, given that all
        # phasepoints in an ensemble share the same force field?
        # Anyway, for sim2 to run below, the force field will have to
        # be set:
        for phasepoint in lp2.phasepoints:
            phasepoint.forcefield = sim2.ensembles[0]['system'].forcefield

        pe1 = sim1.ensembles[0]['path_ensemble']
        pe2 = sim2.ensembles[0]['path_ensemble']

        ps1, ps2 = pe1.paths[-1:][0], pe2.paths[-1:][0]
        ps2['cycle'] = ps1['cycle']
        pe2.paths = pe1.paths

        self.assertEqual(ps1, ps2)
        self.assertEqual(pe1, pe2)

        for i in range(5):
            sim2.step()
        lp2 = copy.deepcopy(sim2.ensembles[0]['path_ensemble'].last_path)
        pe2 = copy.deepcopy(sim2.ensembles[0]['path_ensemble'])

        sim3, in_settings3 = prepare_test_simulation_rnd()
        for i in range(16):
            if i == 0:
                with patch('sys.stdout', new=StringIO()):
                    for _ in initiate_path_simulation(sim3, in_settings3):
                        logging.debug('Running initialisation')
            else:
                sim3.step()

        lp3 = sim3.ensembles[0]['path_ensemble'].last_path
        pe3 = sim3.ensembles[0]['path_ensemble']

        self.assertEqual(lp2, lp3)
        self.assertEqual(pe2, pe3)


class TISTestMethod(unittest.TestCase):
    """Test the various TIS methods."""

    def test_time_reversal(self):
        """Test the time reversal move."""
        status = ('ACC', 'ACC', 'ACC', 'BWI')
        accept = (True, True, True, False)
        for i_case, (acc, stat) in enumerate(zip(accept, status)):
            ens = create_ensemble_and_paths(example=i_case)
            path = ens['path_ensemble'].last_path
            accept, new_path, status = time_reversal(
                path, SameOrder(), ens['path_ensemble'].interfaces,
                start_condition='L')
            for i, j in zip(path.phasepoints, reversed(new_path.phasepoints)):
                parti = i.particles
                partj = j.particles
                # Check that positions are the same:
                self.assertTrue(np.allclose(parti.pos, partj.pos))
                # Check that velocities are reversed:
                self.assertTrue(np.allclose(parti.vel, -1.0 * partj.vel))
                # Check that energies are the same:
                self.assertAlmostEqual(parti.ekin, partj.ekin)
                self.assertAlmostEqual(parti.vpot, partj.vpot)
                # Check that order parameters are the same:
                self.assertAlmostEqual(i.order[0], j.order[0])
            self.assertEqual(accept, acc)
            self.assertEqual(status, stat)
            self.assertEqual(new_path.get_move(), 'tr')
            # Check that the ld move is not altered:
            path.set_move('ld')
            accept, new_path, status = time_reversal(
                path, SameOrder(), ens['interfaces'], start_condition='L'
            )
            self.assertEqual(new_path.get_move(), 'ld')
            # Check that order parameters are reversed:
            accept, new_path, status = time_reversal(
                path, NegativeOrder(), ens['interfaces'], start_condition='L'
            )
            for i, j in zip(path.phasepoints,
                            reversed(new_path.phasepoints)):
                self.assertAlmostEqual(i.order[0], -1 * j.order[0])

    def test_shoot1(self):
        """Test the shooting move, vol 1."""
        ensemble = create_ensemble_and_paths(example=0)
        ensemble['order_function'] = MockOrder()
        ensemble['engine'] = MockEngine(timestep=1.0)
        ensemble['system'] = create_simple_system()

        tis_settings = {
            'maxlength': 1000,
            'sigma_v': -1,
            'aimless': True,
            'zero_momentum': False,
            'rescale_energy': False,
            'allowmaxlength': False
        }
        # Generate BTL:
        accept, _, status = shoot(ensemble, tis_settings, start_cond='L')
        self.assertEqual(status, 'BTL')
        self.assertFalse(accept)
        # Generate BTX:
        tis_settings['allowmaxlength'] = True
        accept, _, status = shoot(ensemble, tis_settings, start_cond='L')
        self.assertEqual(status, 'BTX')
        self.assertFalse(accept)
        # Generate BWI:
        tis_settings['allowmaxlength'] = True
        ensemble['engine'].total_eclipse = float('inf')
        ensemble['engine'].delta_v = 1
        accept, _, status = shoot(ensemble, tis_settings, start_cond='L')
        self.assertEqual(status, 'BWI')
        self.assertFalse(accept)
        # Generate ACC:
        tis_settings['allowmaxlength'] = False
        ensemble['engine'].total_eclipse = float('inf')
        ensemble['engine'].delta_v = -0.01
        accept, _, status = shoot(ensemble, tis_settings, start_cond='L')
        self.assertEqual(status, 'ACC')
        self.assertTrue(accept)

    def test_shoot2(self):
        """Test the shooting move, vol 2."""
        ensemble = create_ensemble_and_paths(example=2)
        ensemble['order_function'] = MockOrder()
        ensemble['engine'] = MockEngine(timestep=1.0)
        ensemble['system'] = create_simple_system()
        tis_settings = {
            'maxlength': 1000,
            'sigma_v': -1,
            'aimless': True,
            'zero_momentum': False,
            'rescale_energy': False,
            'allowmaxlength': False,
        }

        # Generate NCR:
        ensemble['engine'].total_eclipse = float('inf')
        ensemble['engine'].delta_v = -0.1
        ensemble['interfaces'] = (-1., 9., 10.)
        accept, _, status = shoot(ensemble, tis_settings, start_cond='L')
        self.assertEqual(status, 'NCR')
        self.assertFalse(accept)

        # Generate FTL:
        ensemble['engine'] = MockEngine2(timestep=1.0,
                                         interfaces=ensemble['interfaces'])
        tis_settings['allowmaxlength'] = False
        ensemble['engine'].delta_v = -0.1
        accept, _, status = shoot(ensemble, tis_settings, start_cond='L')
        self.assertEqual(status, 'FTL')
        self.assertFalse(accept)

        # Generate FTX:
        ensemble['engine'] = MockEngine2(timestep=1.0,
                                         interfaces=ensemble['interfaces'])
        tis_settings['allowmaxlength'] = True
        ensemble['engine'].delta_v = -0.01
        accept, _, status = shoot(ensemble, tis_settings, start_cond='L')
        self.assertEqual(status, 'FTX')
        self.assertFalse(accept)

        # Generate FTX again - Test when move was 'ld':
        ensemble['engine'] = MockEngine2(timestep=1.0,
                                         interfaces=ensemble['interfaces'])
        tis_settings['allowmaxlength'] = False
        ensemble['path_ensemble'].last_path.set_move('ld')
        ensemble['engine'].delta_v = -0.01
        accept, _, status = shoot(ensemble, tis_settings, start_cond='L')
        self.assertEqual(status, 'FTX')
        self.assertFalse(accept)

    def test_shoot_kob(self):
        """Test the shooting move when we get a KOB."""
        ensemble = create_ensemble_and_paths()
        ensemble['engine'] = MockEngine(timestep=1.0)
        ensemble['system'] = create_simple_system()
        ensemble['order_function'] = MockOrder2()
        tis_settings = {
            'maxlength': 1000,
            'sigma_v': -1,
            'aimless': True,
            'zero_momentum': False,
            'rescale_energy': False,
            'allowmaxlength': False
        }

        # Generate BTL
        ensemble['rgen'] = MockRandomGenerator(seed=1)
        accept, _, status = shoot(ensemble, tis_settings, start_cond='L')
        self.assertEqual(status, 'KOB')
        self.assertFalse(accept)

    def test_shoot_aiming(self):
        """Test the non aimless shooting move."""
        ensemble = create_ensemble_and_paths(example=2)
        ensemble['engine'] = MockEngine(timestep=1.0)
        ensemble['system'] = create_simple_system()
        ensemble['order_function'] = MockOrder()
        ensemble['rgen'] = MockRandomGenerator(seed=1)
        ensemble['path_ensemble'].rgen = MockRandomGenerator(seed=160)

        tis_settings = {'maxlength': 1000,
                        'sigma_v': -1,
                        'aimless': False,
                        'zero_momentum': False,
                        'rescale_energy': False,
                        'allowmaxlength': True}

        # Generate ACC
        ensemble['engine'].total_eclipse = float('inf')
        ensemble['engine'].delta_v = -0.01
        accept, _, status = shoot(ensemble, tis_settings, start_cond='L')
        self.assertEqual(status, 'ACC')
        self.assertTrue(accept)
        # Generate MCR:
        accept, _, status = shoot(ensemble, tis_settings, start_cond='L')
        self.assertEqual(status, 'MCR')
        self.assertFalse(accept)


if __name__ == '__main__':
    unittest.main()
