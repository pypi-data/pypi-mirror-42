# -*- coding: utf-8 -*-
# Copyright (c) 2019, PyRETIS Development Team.
# Distributed under the LGPLv2.1+ License. See LICENSE for more info.
"""Definition of simulation objects for Monte Carlo simulations.

This module defines some classes and functions for performing
Monte Carlo simulations.

Important classes defined here
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

UmbrellaWindowSimulation (:py:class:`.UmbrellaWindowSimulation`)
    Defines a simulation for performing umbrella window simulations.
    Several umbrella window simulations can be joined to perform a
    umbrella simulation.
"""
import numpy as np
from pyretis.core.montecarlo import max_displace_step
from pyretis.simulation.simulation import Simulation
from pyretis.core.random_gen import create_random_generator

__all__ = ['UmbrellaWindowSimulation']


def mc_task(rgen, system, maxdx):
    """Perform a Monte Carlo displacement move.

    Here, a displacement step will be carried out and
    the trial move will be accepted/rejected and the
    positions and potential energy will be updated as needed.

    Parameters
    ----------
    rgen : object like :py:class`.RandomGenerator`
        This object is used for generating random numbers.
    system : object like :py:class:`.System`
        The system we act on.
    maxdx : float
        Maximum displacement step for the Monte Carlo move.

    """
    accepted_r, _, trial_r, v_trial, status = max_displace_step(rgen, system,
                                                                maxdx)
    if status:
        system.particles.pos = accepted_r
        system.particles.vpot = v_trial
    return accepted_r, v_trial, trial_r, status


class UmbrellaWindowSimulation(Simulation):
    """This class defines an Umbrella simulation.

    The Umbrella simulation is a special case of
    the simulation class with settings to simplify the
    execution of the umbrella simulation.

    Attributes
    ----------
    ensemble : dict
        It contains the simulations info
          *  system : object like :py:class:`.System`
                 The system to act on.
          *  rgen : object like :py:class:`.RandomGenerator`
                 Object to use for random number generation.
          *  umbrella : list, [float, float]
                 The umbrella window to consider.
          *  overlap : float
                 The position we have to cross before the simulation ends.
          *  maxdx : float
                 Defines the maximum movement allowed in the Monte Carlo
    controls: dict of parameters to set up and control the simulations.
        It contains:
           *  steps : int, optional
                  The number of simulation steps to perform.
           *  startcycle : int, optional
                  The cycle we start the simulation on, can be useful if
                  restarting.

    """

    simulation_type = 'umbrella-window'

    def __init__(self, ensemble, settings, controls):
        """Initialise the umbrella simulation simulation.

        Parameters
        ----------
        ensemble : dict
            It contains the simulations info
              *  system : object like :py:class:`.System`
                     The system to act on.
              *  rgen : object like :py:class:`.RandomGenerator`
                     Object to use for random number generation.
              *  umbrella : list, [float, float]
                     The umbrella window to consider.
              *  overlap : float
                     The position we have to cross before the simulation ends.
              *  maxdx : float
                     Defines the maximum movement allowed in the Monte Carlo
                     moves.
        settings : dict
            Contains all the simulation settings.
        controls: dict of parameters to set up and control the simulations.
            It contains:
              *  mincycle : int, optional
                     The *MINIMUM* number of cycles to perform. Note that in
                     base `Simulation` class this is the *MAXIMUM* number of
                     cycles to perform. The meaning is redefined in this class
                     by overriding `self.simulation_finished`.
              *  startcycle : int, optional
                     The current simulation cycle, i.e. where we start.

        """
        super().__init__(settings, controls)
        self.umbrella = ensemble['umbrella']
        self.overlap = ensemble['overlap']
        self.rgen = ensemble.get(
            'rgen',
            create_random_generator(settings['simulation']))

        self.system = ensemble['system']
        self.maxdx = ensemble['maxdx']
        task_monte_carlo = {'func': mc_task,
                            'args': [self.rgen, self.system, self.maxdx],
                            'result': 'displace_step'}
        self.add_task(task_monte_carlo)
        self.first_step = False

    def is_finished(self):
        """Check if the simulation is done.

        In the umbrella simulation, the simulation is finished when we
        cycle is larger than maxcycle and all particles have
        crossed self.overlap.

        Returns
        -------
        out : boolean
            True if the simulation is finished, False otherwise.

        """
        return (self.cycle['step'] > self.cycle['end'] and
                np.all(self.system.particles.pos > self.overlap))

    def __str__(self):
        """Return some info about the simulation as a string."""
        msg = ['Umbrella window simulation']
        msg += ['Umbrella: {}, Overlap: {}.'.format(self.umbrella,
                                                    self.overlap)]
        msg += ['Minimum number of cycles: {}'.format(self.cycle['end'])]
        return '\n'.join(msg)

    def restart_info(self):
        """Return information which can be used to restart the simulation.

        Returns
        -------
        info : dict,
            Contains all the updated simulation settings and counters.

        """
        info = super().restart_info()

        if hasattr(self, 'rgen') and self.rgen is not None:
            info['simulation'].update(self.rgen.get_state())

        info['umbrella'] = self.umbrella
        info['overlap'] = self.overlap
        info['type'] = self.simulation_type
        return info

    def load_restart_info(self, info):
        """Load the restart information."""
        super().load_restart_info(info)

        self.umbrella = info.get('umbrella', self.umbrella)
        self.overlap = info.get('overlap', self.overlap)
        if info['simulation'].get('rgen') is not None and\
                hasattr(self, 'rgen') and self.rgen is not None:
            self.rgen = create_random_generator(info['simulation'])
