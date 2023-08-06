# -*- coding: utf-8 -*-
# Copyright (c) 2019, PyRETIS Development Team.
# Distributed under the LGPLv2.1+ License. See LICENSE for more info.
"""This module handles the creation of simulations from settings.

The different simulations are defined as objects which inherit
from the base :py:class:`.Simulation` class defined in
:py:mod:`pyretis.simulation.simulation`. Here, we are treating
each simulation with a special case.

Important methods defined here
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

create_simulation (:py:func:`.create_simulation`)
    Method for creating a simulation object from settings.

create_ensemble (:py:func:`.create_ensemble`)
    Method for creating an ensemble dictionary from settings.

create_ensembles (:py:func:`.create_ensembles`)
    Method for creating a list of ensemble from settings.

create_nve_simulation (:py:func:`.create_mve_simulation`)
    Method for creating a nve simulation object from settings.

create_mdflux_simulation (:py:func:`.create_mdflux_simulation`)
    Method for creating a mdflux simulation object from settings.

create_umbrellaw_simulation (:py:func:`.create_umbrellaw_simulation`)
    Method for creating a umbrellaw simulation object from settings.

create_tis_simulation (:py:func:`.create_tis_simulation`)
    Method for creating a tis simulation object from settings.

create_retis_simulation (:py:func:`.create_retis_simulation`)
    Method for creating a retis simulation object from settings.

prepare_system (:py:func:`.prepare_system`)
    Method for creating a system object from settings.

prepare_engine (:py:func:`.prepare_engine`)
    Method for creating an engine object from settings.

"""
import logging
import os
from pyretis.core.pathensemble import get_path_ensemble_class
from pyretis.setup.createforcefield import create_force_field
from pyretis.inout import print_to_screen
from pyretis.setup.common import create_orderparameter
from pyretis.inout.restart import read_restart_file
from pyretis.core.units import units_from_settings
from pyretis.core.random_gen import create_random_generator
from pyretis.simulation.md_simulation import (
    SimulationNVE,
    SimulationMDFlux,
)
from pyretis.simulation.mc_simulation import UmbrellaWindowSimulation
from pyretis.simulation.path_simulation import (
    SimulationTIS,
    SimulationRETIS
)
from pyretis.setup import (
    create_system,
    create_engine
)
from pyretis.inout.checker import (
    check_engine,
    check_ensemble,
)

logger = logging.getLogger(__name__)  # pylint: disable=invalid-name
logger.addHandler(logging.NullHandler())


__all__ = ['create_simulation', 'create_ensemble', 'create_ensembles',
           'create_nve_simulation', 'create_mdflux_simulation',
           'create_umbrellaw_simulation', 'create_tis_simulation',
           'create_retis_simulation', 'prepare_system', 'prepare_engine']


def create_ensemble(settings):
    """Create the path ensembles from simulation settings.

    Parameters
    ----------
    settings : dict
        This dict contains the settings needed to create the path
        ensemble.

    Returns
    -------
    ensemble : dict, list of
        objects that contain all the information needed in each ensemble.

    """
    i_ens = settings['tis']['ensemble_number']
    exe_dir = settings['simulation'].get('exe_path', os.path.abspath('.'))

    rgen_ens = create_random_generator(settings['tis'])
    rgen_path = create_random_generator(settings['system'])

    engine = prepare_engine(settings)
    system = prepare_system(settings)
    klass = get_path_ensemble_class(settings['particles']['type'])
    interfaces = settings['simulation']['interfaces']
    detect = settings['tis']['detect']
    path_ensemble = \
        klass(i_ens, interfaces, rgen=rgen_path,
              detect=detect, exe_dir=exe_dir)

    if 'restart' in settings:
        engine.load_restart_info(settings['restart']['engine'])
        system.load_restart_info(settings['restart']['system'])
        path_ensemble.load_restart_info(settings['restart']['path_ensemble'])
        rgen_ens.set_state(settings['restart']['rgen'])

    order_function = create_orderparameter(settings)
    if order_function is None:
        msgtxt = 'No order parameter created in ensemble {}!'.format(i_ens)
        logger.critical(msgtxt)
        raise ValueError(msgtxt)

    ensemble = {'system': system,
                'engine': engine,
                'order_function': order_function,
                'interfaces': interfaces,
                'detect': detect,
                'exe_path': exe_dir,
                'path_ensemble': path_ensemble,
                'rgen': rgen_ens}

    return ensemble


def create_ensembles(settings):
    """Create a liast of dictionary from ensembles simulation settings.

    Parameters
    ----------
    settings : dict
        This dict contains the settings needed to create the path
        ensemble.

    Returns
    -------
    ensembles : list of dics,
        List of ensemble.

    """
    ensembles = []
    interfaces = settings['simulation']['interfaces']

    if settings['simulation']['task'] in {'tis', 'retis', 'make-tis-files'}:
        middle, i_t, i_ens = None, 0, 0
        while i_ens != len(settings['ensemble']):
            reactant, product, update = interfaces[0], interfaces[-1], False
            ens_set = settings['ensemble'][i_ens]
            if i_t == 0:
                if settings['simulation']['flux']:
                    reactant, middle, product =\
                        float('-inf'), reactant, reactant
                    update = True
            elif i_t == 1:
                if settings['simulation']['zero_ensemble']:
                    middle = interfaces[i_t - 1]
                    update = True
            else:
                middle = interfaces[i_t - 1]
                update = True

            if update:
                # Each ensemble has only three interfaces
                settings['ensemble'][i_ens]['simulation']['interfaces'] =\
                    [reactant, middle, product]

                if 'tis' not in ens_set:
                    ens_set['tis'] = {}
                if 'ensemble_number' not in ens_set['tis']:
                    ens_set['tis']['ensemble_number'] = i_t
                if 'detect' not in ens_set['tis']:
                    ens_set['tis']['detect'] = interfaces[i_t]
                i_ens += 1
            i_t += 1

        for i in range(i_ens):
            ensembles.append(create_ensemble(settings['ensemble'][i]))

    else:
        ensembles.append(create_ensemble(settings))

    return ensembles


def create_nve_simulation(settings):
    """Set up and create a NVE simulation.

    Parameters
    ----------
    settings : dict
        The settings needed to set up the simulation.

    Returns
    -------
    SimulationNVE : object like :py:class:`.SimulationNVE`
        The object representing the simulation to run.

    """
    ensemble = {'system': prepare_system(settings),
                'engine': prepare_engine(settings),
                'rgen': create_random_generator(settings['simulation'])}

    for key in ('steps',):
        if key not in settings['simulation']:
            msgtxt = 'Simulation setting "{}" is missing!'.format(key)
            logger.critical(msgtxt)
            raise ValueError(msgtxt)

    controls = {'steps': settings['simulation']['steps'],
                'startcycle': settings['simulation'].get('startcycle', 0)}

    return SimulationNVE(ensemble, settings, controls)


def create_mdflux_simulation(settings):
    """Set up and create a MD FLUX simulation.

    Parameters
    ----------
    settings : dict
        The settings needed to set up the simulation.

    Returns
    -------
    SimulationMDFlux : object like :py:class:`.SimulationMDFlux`
        The object representing the simulation to run.

    """
    ensemble = {'system': prepare_system(settings),
                'engine': prepare_engine(settings),
                'order_function': create_orderparameter(settings),
                'rgen': create_random_generator(settings['simulation'])}

    if ensemble['order_function'] is None:
        msgtxt = 'No order parameter created!'
        logger.critical(msgtxt)
        raise ValueError(msgtxt)

    for key in ('steps', 'interfaces'):
        if key not in settings['simulation']:
            msgtxt = 'Simulation setting "{}" is missing!'.format(key)
            logger.critical(msgtxt)
            raise ValueError(msgtxt)
        else:
            ensemble[key] = settings['simulation'][key]

    controls = {'steps': settings['simulation']['steps'],
                'startcycle': settings['simulation'].get('startcycle', 0)}

    return SimulationMDFlux(ensemble, settings, controls)


def create_umbrellaw_simulation(settings):
    """Set up and create a Umbrella Window simulation.

    Parameters
    ----------
    settings : dict
        The settings needed to set up the simulation.

    Returns
    -------
    UmbrellaWindowSimulation : obj like :py:class:`.UmbrellaWindowSimulation`
        The object representing the simulation to run.

    """
    ensemble = {'system': prepare_system(settings),
                'rgen': create_random_generator(settings['simulation'])}

    for key in ('umbrella', 'overlap', 'maxdx', 'mincycle'):
        if key not in settings['simulation']:
            msgtxt = 'Simulation setting "{}" is missing!'.format(key)
            logger.critical(msgtxt)
            raise ValueError(msgtxt)
        else:
            ensemble[key] = settings['simulation'][key]

    controls = {'mincycle': settings['simulation']['mincycle'],
                'startcycle': settings['simulation'].get('startcycle', 0)}

    return UmbrellaWindowSimulation(ensemble, settings, controls)


def create_tis_simulation(settings):
    """Set up and create a single TIS simulation.

    Parameters
    ----------
    settings : dict
        The settings needed to set up the simulation.

    Returns
    -------
    SimulationTIS : object like :py:class:`.SimulationSingleTIS`
        The object representing the simulation to run.

    """
    check_ensemble(settings)
    ensembles = create_ensembles(settings)

    if 'steps' not in settings['simulation']:
        msgtxt = 'Simulation setting "{}" is missing!'.format('steps')
        logger.critical(msgtxt)
        raise ValueError(msgtxt)

    controls = {'rgen': create_random_generator(settings['simulation']),
                'steps': settings['simulation']['steps'],
                'startcycle': settings['simulation'].get('startcycle', 0)}

    return SimulationTIS(ensembles, settings, controls)


def create_retis_simulation(settings):
    """Set up and create a RETIS simulation.

    Parameters
    ----------
    settings : dict
        This dictionary contains the settings for the simulation.

    Returns
    -------
    SimulationRETIS : object like :py:class:`.SimulationRETIS`
        The object representing the simulation to run.

    """
    check_ensemble(settings)
    ensembles = create_ensembles(settings)

    if 'steps' not in settings['simulation']:
        msgtxt = 'Simulation setting "{}" is missing!'.format('steps')
        logger.critical(msgtxt)
        raise ValueError(msgtxt)

    controls = {'rgen': create_random_generator(settings['simulation']),
                'steps': settings['simulation']['steps'],
                'startcycle': settings['simulation'].get('startcycle', 0)}

    return SimulationRETIS(ensembles, settings, controls)


def prepare_system(settings):
    """Create a system from given settings.

    Parameters
    ----------
    settings : dict
        This dictionary contains the settings for the simulation.

    Returns
    -------
    syst : object like :py:class:`.syst`
        This object will correspond to the selected simulation type.

    """
    if 'system' in settings and 'obj' in settings['system']:
        return settings['system']['obj']

    logtxt = 'Creating system from settings.'
    print_to_screen(logtxt, level='info')
    logger.info(logtxt)
    system = create_system(settings)
    logtxt = 'Creating force field.'
    print_to_screen(logtxt, level='info')
    logger.info(logtxt)
    system.forcefield = create_force_field(settings)
    system.extra_setup()
    print_to_screen()
    return system


def prepare_engine(settings):
    """Create an engine from given settings.

    Parameters
    ----------
    settings : dict
        This dictionary contains the settings for the simulation.

    Returns
    -------
    engine : object like :py:class:`.engine`
        This object will correspond to the selected simulation type.

    """
    if 'engine' in settings and 'obj' in settings['engine']:
        return settings['engine']['obj']

    logtxt = 'Initializing unit system.'
    print_to_screen(logtxt, level='message')
    logger.info(logtxt)

    logtxt = units_from_settings(settings)
    print_to_screen(logtxt)
    logger.info(logtxt)

    check_engine(settings)
    engine = create_engine(settings)
    if engine is not None:
        logtxt = 'Created engine "{}" from settings.'.format(engine)
        print_to_screen(logtxt, level='info')
        logger.info(logtxt)
    else:
        logtxt = 'No engine created.'
        print_to_screen(logtxt, level='warning')
        logger.info(logtxt)

    print_to_screen()
    return engine


def create_simulation(settings):
    """Create simulation(s) from given settings.

    This function will set up some common simulation types.
    It is meant as a helper function to automate some very common set-up
    task. It will here check what kind of simulation we are to perform
    and then call the appropriate function for setting that type of
    simulation up.

    Parameters
    ----------
    settings : dict
        This dictionary contains the settings for the simulation.

    Returns
    -------
    simulation : object like :py:class:`.Simulation`
        This object will correspond to the selected simulation type.

    """
    sim_type = settings['simulation']['task'].lower()

    sim_map = {
        'md-nve': create_nve_simulation,
        'md-flux': create_mdflux_simulation,
        'umbrellawindow': create_umbrellaw_simulation,
        'make-tis-files': create_tis_simulation,
        'tis': create_tis_simulation,
        'retis': create_retis_simulation,
    }

    # todo I cleaned the restart part, but it surely can be further improved.
    # a routine where a clear policy of restart (e.g.to  overwrite or not
    # original settings) shall be constructed.
    if 'restart' in settings['simulation']:
        filename = os.path.join(settings['simulation']['exe_path'],
                                settings['simulation']['restart'])
        settings['restart'] = read_restart_file(filename)

        if 'ensemble' in settings:
            for ens, r_ens in zip(settings['ensemble'],
                                  settings['restart']['ensemble']):
                ens['restart'] = read_restart_file(os.path.join(
                    settings['simulation']['exe_path'], r_ens['restart']))
                ens['simulation']['startcycle'] = r_ens['simulation']['steps']

        settings['simulation']['startcycle'] =\
            settings['restart']['simulation']['steps']

    if sim_type not in sim_map:  # TODO put in check_sim_type
        msgtxt = 'Unknown simulation task {}'.format(sim_type)
        logger.error(msgtxt)
        raise ValueError(msgtxt)

    simulation = sim_map[sim_type](settings)
    if isinstance(simulation, list):
        msgtxt = sim_type
    else:
        msgtxt = '{}'.format(simulation)
    logger.info('Created simulation:\n%s', msgtxt)

    return simulation
