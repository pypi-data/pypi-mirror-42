# -*- coding: utf-8 -*-
# Copyright (c) 2019, PyRETIS Development Team.
# Distributed under the LGPLv2.1+ License. See LICENSE for more info.
"""Definitions of simulation objects for path sampling simulations.

This module defines simulations for performing path sampling
simulations.

Important classes defined here
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

PathSimulation (:py:class:`.PathSimulation`)
    The base class for path simulations.

SimulationTIS (:py:class:`.SimulationSingleTIS`)
    Definition of a TIS simulation for a single path ensemble.

SimulationRETIS (:py:class:`.SimulationRETIS`)
    Definition of a RETIS simulation.

"""
import logging
import os
import numpy as np
from pyretis.simulation.simulation import Simulation
from pyretis.core.tis import make_tis_step_ensemble
from pyretis.core.retis import make_retis_step
from pyretis.initiation import initiate_path_simulation
from pyretis.core.random_gen import create_random_generator
from pyretis.inout.simulationio import task_from_settings
from pyretis.inout.screen import print_to_screen
from pyretis.inout.common import make_dirs
from pyretis.core.tis import make_tis
from pyretis.inout.restart import write_ensemble_restart
logger = logging.getLogger(__name__)  # pylint: disable=invalid-name
logger.addHandler(logging.NullHandler())


__all__ = ['PathSimulation', 'SimulationTIS', 'SimulationRETIS']


class PathSimulation(Simulation):
    """A base class for TIS/RETIS simulations.

    Attributes
    ----------
    ensembles : list of dictionaries of objects, that contains:
          *  path_ensemble: objects like :py:class:`.PathEnsemble`
                 This is used for storing results for the different path
                 ensembles.
          *  engine : object like :py:class:`.EngineBase`
                 This is the integrator that is used to propagate the system
                 in time.
          *  rgen : object like :py:class:`.RandomGenerator`
                 This is a random generator used for the generation of paths.
          *  system : object like :py:class:`.System`
                 This is the system the simulation will act on.
    settings : dict
        A dictionary with TIS and RETIS settings. We expect that
        we can find ``settings['tis']`` and possibly
        ``settings['retis']``. For ``settings['tis']`` we further
        expect to find the keys:

        * `aimless`: Determines if we should do aimless shooting
          (True) or not (False).
        * `sigma_v`: Scale used for non-aimless shooting.
        * `seed`: A integer seed for the random generator used for
          the path ensemble we are simulating here.

        Note that the
        :py:func:`pyretis.core.tis.make_tis_step_ensemble` method
        will make use of additional keys from ``settings['tis']``.
        Please see this method for further details. For the
        ``settings['retis']`` we expect to find the following keys:

        * `swapfreq`: The frequency for swapping moves.
        * `relative_shoots`: If we should do relative shooting for
          the path ensembles.
        * `nullmoves`: Should we perform null moves.
        * `swapsimul`: Should we just swap a single pair or several
          pairs.
    required_settings : tuple of strings
        This is just a list of the settings that the simulation
        requires. Here it is used as a check to see that we have
        all we need to set up the simulation.

    """

    required_settings = ('tis', 'retis')
    name = 'Generic path simulation'
    simulation_type = 'generic-path'
    simulation_output = [
        {
            'type': 'pathensemble',
            'name': 'path_ensemble',
            'result': ('pathensemble-{}',),
        },
        {
            'type': 'path-order',
            'name': 'path_ensemble-order',
            'result': ('path-{}', 'status-{}'),
        },
        {
            'type': 'path-traj-{}',
            'name': 'path_ensemble-traj',
            'result': ('path-{}', 'status-{}', 'pathensemble-{}'),
        },
        {
            'type': 'path-energy',
            'name': 'path_ensemble-energy',
            'result': ('path-{}', 'status-{}'),
        },
    ]

    def __init__(self, ensembles, settings, controls):
        """Initialise the path simulation object."""
        super().__init__(settings, controls)
        self.ensembles = ensembles
        self.settings = settings
        self.rgen = controls.get('rgen', create_random_generator())

        for key in self.required_settings:
            if key not in self.settings:
                logtxt = 'Missing required setting "{}" for simulation "{}"'
                logtxt = logtxt.format(key, self.name)
                logger.error(logtxt)
                raise ValueError(logtxt)
            else:
                self.settings[key] = settings[key]

        # Additional setup for shooting:
        for i, ensemble in enumerate(ensembles):
            ensemble['system'].potential_and_force()

            if self.settings['ensemble'][i]['tis']['sigma_v'] < 0.0:
                self.settings['ensemble'][i]['tis']['aimless'] = True
                logger.debug('%s: aimless is True', self.name)
            else:
                logger.debug('Path simulation: Creating sigma_v.')
                sigv = (self.settings['ensemble'][i]['tis']['sigma_v'] *
                        np.sqrt(ensemble['system'].particles.imass))
                logger.debug('Path simulation: sigma_v created and set.')
                self.settings['ensemble'][i]['tis']['sigma_v'] = sigv
                self.settings['ensemble'][i]['tis']['aimless'] = False
                logger.debug('Path simulation: aimless is False')

    def restart_info(self):
        """Return restart info.

        The restart info for the path simulation includes the state of
        the random number generator(s).

        Returns
        -------
        info : dict,
            Contains all the updated simulation settings and counters.

        """
        info = super().restart_info()
        if hasattr(self, 'rgen') and self.rgen is not None:
            info['simulation']['rgen'] = self.rgen.get_state()

        # Here we store only the necessary info to initialize the
        # ensemble objects constructed in `pyretis.setup.createsimulation`
        if hasattr(self, 'ensembles'):
            info['ensemble'] = []
            for ens in self.ensembles:
                info['ensemble'].append(
                    {'restart': os.path.join(
                        ens['path_ensemble'].ensemble_name_simple,
                        'ensemble.restart'),
                     'particles': self.settings.get('particles'),
                     'engine': self.settings.get('engine'),
                     'system': self.settings.get('system'),
                     'simulation': self.settings.get('simulation')})

        return info

    def load_restart_info(self, info):
        """Load the restart information."""
        super().load_restart_info(info)

        if info['simulation'].get('rgen') is not None:
            self.rgen = create_random_generator(info['simulation']['rgen'])

    def create_output_tasks(self, settings, progress=False):
        """Create output tasks for the simulation.

        This method will generate output tasks based on the tasks
        listed in :py:attr:`.simulation_output`.

        Parameters
        ----------
        settings : dict
            These are the simulation settings.
        progress : boolean
            For some simulations, the user may select to display a
            progress bar, we then need to disable the screen output.

        """
        logging.debug('Clearing output tasks & adding pre-defined ones')
        self.output_tasks = []
        for ensemble in self.ensembles:
            path_ensemble = ensemble['path_ensemble']
            directory = path_ensemble.directory['path_ensemble']
            idx = path_ensemble.ensemble_number
            logger.info('Creating output directories for path_ensemble %s',
                        path_ensemble.ensemble_name)
            for dir_name in path_ensemble.directories():
                msg_dir = make_dirs(dir_name)
                logger.info('%s', msg_dir)
            for task_dict in self.simulation_output:
                task_dict_ens = task_dict.copy()
                if 'result' in task_dict_ens:
                    task_dict_ens['result'] = \
                        [key.format(idx) for key in task_dict_ens['result']]
                task = task_from_settings(task_dict_ens, settings, directory,
                                          ensemble['engine'], progress)
                if task is not None:
                    logger.debug('Created output task:\n%s', task)
                    self.output_tasks.append(task)

    def write_restart(self, now=False):
        """Create a restart file.

        Parameters
        ----------
        now : boolean, optional
            If True, the output file will be written irrespective of the
            step number.

        """
        super().write_restart(now=now)
        if now or (self.restart_freq is not None and
                   self.cycle['stepno'] % self.restart_freq == 0):
            for idx, ensemble in enumerate(self.ensembles):
                write_ensemble_restart(ensemble,
                                       self.settings['ensemble'][idx])

    def initiate(self, settings):
        """Initialise the path simulation.

        Parameters
        ----------
        settings : dictionary
            The simulation settings.

        """
        init = initiate_path_simulation(self, settings)
        print_to_screen('')
        for i_ens, (accept, path, status, path_ensemble) in enumerate(init):
            print_to_screen(
                'Found initial path for {}:'.format(
                    path_ensemble.ensemble_name),
                level='success' if accept else 'warning',
            )
            for line in str(path).split('\n'):
                print_to_screen('- {}'.format(line))
            logger.info('Found initial path for %s',
                        path_ensemble.ensemble_name)
            logger.info('%s', path)
            print_to_screen('')
            idx = path_ensemble.ensemble_number
            path_ensemble_result = {
                'pathensemble-{}'.format(idx): path_ensemble,
                'path-{}'.format(idx): path,
                'status-{}'.format(idx): status,
                'cycle': self.cycle,
                'system': self.system,
            }
            # If we are doing a restart, we do not print out at the
            # "restart" step as we assume that this is already
            # outputted in the "previous" simulation (the one
            # we restart from):
            if settings['initial-path']['method'] != 'restart':
                for task in self.output_tasks:
                    task.output(path_ensemble_result)
                write_ensemble_restart({'path_ensemble': path_ensemble},
                                       settings['ensemble'][i_ens])
            if self.soft_exit():
                return False
        return True


class SimulationTIS(PathSimulation):
    """A TIS simulation.

    This class is used to define a TIS simulation where the goal is
    to calculate crossing probabilities for a single path ensemble.

    """

    required_settings = ('tis',)
    name = 'TIS simulation'
    simulation_type = 'tis'
    simulation_output = PathSimulation.simulation_output + [
        {
            'type': 'pathensemble-screen',
            'name': 'path_ensemble-screen',
            'result': ('pathensemble-{}',),
        },
    ]

    def __init__(self, ensembles, settings, controls):
        """Initialise the TIS simulation object.

        Parameters
        ----------
        ensembles : list.
             It contains:
               *  path_ensemble: object like :py:class:`.PathEnsemble`
                      This is used for storing results for the simulation. It
                      is also used for defining the interfaces for this
                      simulation.
               *  system : object like :py:class:`.System`
                      This is the system we are investigating.
               *  order_function : object like :py:class:`.OrderParameter`
                      The object used for calculating the order parameter.
               *  engine : object like :py:class:`.EngineBase`
                      This is the integrator that is used to propagate the
                      system in time.
               *  rgen : object like :py:class:`.RandomGenerator`
                      This is the random generator to use in the ensemble.
        settings : dict
            This dictionary contains the settings for the simulation.
        controls: dict of parameters to set up and control the simulations.
            It contains:
              *  steps : int, optional
                     The number of simulation steps to perform.
              *  startcycle : int, optional
                     The cycle we start the simulation on, can be useful if
                     restarting.
              *  rgen : object like :py:class:`.RandomGenerator`
                     This object is the random generator to use in the
                     simulation.

        """
        super().__init__(ensembles, settings, controls)

    def step(self):
        """Perform a TIS simulation step.

        Returns
        -------
        out : dict
            This list contains the results of the TIS step.

        """
        results = {}
        self.cycle['step'] += 1
        self.cycle['stepno'] += 1
        tis_step = make_tis(
            self.ensembles,
            self.rgen,
            self.settings,
            self.cycle['step'])

        for i_res, res in enumerate(tis_step):
            idx = res['ensemble_number']
            results['move-{}'.format(idx)] = res['tis-move']
            results['status-{}'.format(idx)] = res['status']
            results['path-{}'.format(idx)] = res['trial']
            results['accept-{}'.format(idx)] = res['accept']
            results['all-{}'.format(idx)] = res
            results['pathensemble-{}'.format(idx)] = \
                self.ensembles[i_res]['path_ensemble']

        results['cycle'] = self.cycle

        return results

    def __str__(self):
        """Just a small function to return some info about the simulation."""
        msg = ['TIS simulation']
        msg += ['Ensembles:']
        for ensemble in self.ensembles:
            path_ensemble = ensemble['path_ensemble']
            msg += ['Path ensemble: {}'.format(path_ensemble.ensemble_number)]
            msg += ['{}: Interfaces: {}'.format(path_ensemble.ensemble_name,
                                                path_ensemble.interfaces)]
            msg += ['Engine: {}'.format(ensemble['engine'])]

        nstep = self.cycle['end'] - self.cycle['start']
        msg += ['Number of steps to do: {}'.format(nstep)]
        return '\n'.join(msg)


class SimulationRETIS(PathSimulation):
    """A RETIS simulation.

    This class is used to define a RETIS simulation where the goal is
    to calculate crossing probabilities for several path ensembles.

    The attributes are documented in the parent class, please see:
    :py:class:`.PathSimulation`.
    """

    required_settings = ('retis',)
    name = 'RETIS simulation'
    simulation_type = 'retis'
    simulation_output = PathSimulation.simulation_output + [
        {
            'type': 'pathensemble-retis-screen',
            'name': 'path_ensemble-retis-screen',
            'result': ('pathensemble-{}',),
        },
    ]

    def __init__(self, ensembles, settings, controls):
        """Initialise the RETIS simulation object.

        Parameters
        ----------
        ensembles : list.
             It contains:
               *  path_ensemble: object like :py:class:`.PathEnsemble`
                      This is used for storing results for the simulation. It
                      is also used for defining the interfaces for this
                      simulation.
               *  system : object like :py:class:`.System`
                      This is the system we are investigating.
               *  order_function : object like :py:class:`.OrderParameter`
                      The object used for calculating the order parameter.
               *  engine : object like :py:class:`.EngineBase`
                      This is the integrator that is used to propagate the
                      system in time.
               *  rgen : object like :py:class:`.RandomGenerator`
                      This is the random generator to use in the ensemble.
        settings : dict
            This dictionary contains the settings for the simulation.
        controls: dict of parameters to set up and control the simulations.
            It contains:
              *  steps : int, optional
                     The number of simulation steps to perform.
              *  startcycle : int, optional
                     The cycle we start the simulation on, can be useful if
                     restarting.
              *  rgen : object like :py:class:`.RandomGenerator`
                     This object is the random generator to use in the
                     simulation.

        """
        super().__init__(ensembles, settings, controls)

    def step(self):
        """Perform a RETIS simulation step.

        Returns
        -------
        out : dict
            This list contains the results of the defined tasks.

        """
        results = {}
        self.cycle['step'] += 1
        self.cycle['stepno'] += 1
        msgtxt = 'RETIS step. Cycle {}'.format(self.cycle['stepno'])
        logger.info(msgtxt)
        retis_step = make_retis_step(
            self.ensembles,
            self.rgen,
            self.settings,
            self.cycle['step'],
        )
        for res in retis_step:
            idx = res['ensemble_number']
            results['move-{}'.format(idx)] = res['retis-move']
            results['status-{}'.format(idx)] = res['status']
            results['path-{}'.format(idx)] = res['trial']
            results['accept-{}'.format(idx)] = res['accept']
            results['all-{}'.format(idx)] = res
            results['pathensemble-{}'.format(idx)] = \
                self.ensembles[idx]['path_ensemble']

        results['system'] = self.system  # TODO: IS THIS REALLY NEEDED HERE?
        results['cycle'] = self.cycle
        return results

    def __str__(self):
        """Just a small function to return some info about the simulation."""
        msg = ['RETIS simulation']
        msg += ['Ensembles:']
        for ensemble in self.ensembles:
            path_ensemble = ensemble['path_ensemble']
            msgtxt = '{}: Interfaces: {}'.format(path_ensemble.ensemble_name,
                                                 path_ensemble.interfaces)
            msg += [msgtxt]
        nstep = self.cycle['end'] - self.cycle['start']
        msg += ['Number of steps to do: {}'.format(nstep)]
        return '\n'.join(msg)
