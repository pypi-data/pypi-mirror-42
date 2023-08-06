# -*- coding: utf-8 -*-
# Copyright (c) 2019, PyRETIS Development Team.
# Distributed under the LGPLv2.1+ License. See LICENSE for more info.
"""This module defines how we write and read restart files.

Important methods defined here
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

read_restart_file (:py:func:`.read_restart_file`)
    A method for reading restart information from a file.

write_restart_file (:py:func:`.write_restart_file`)
    A method for writing the restart file.

write_ensemble_restart (:py:func:`.write_ensemble_restart`)
    A method for writing restart files for path ensembles.
"""
import logging
import copy
import os
import pickle
logger = logging.getLogger(__name__)  # pylint: disable=invalid-name
logger.addHandler(logging.NullHandler())


__all__ = ['read_restart_file',
           'write_restart_file',
           'write_ensemble_restart']


def write_restart_file(filename, simulation):
    """Write restart info for a simulation.

    Parameters
    ----------
    filename : string
        The file we are going to write to.
    simulation : object like :py:class:`.Simulation`
        A simulation object we will get information from.

    """
    info = simulation.restart_info()

    with open(filename, 'wb') as outfile:
        pickle.dump(info, outfile)


def write_ensemble_restart(ensemble, settings_ens):
    """Write a restart file for a path ensemble.

    Parameters
    ----------
    ensemble : dict.
        It contains:
          *  path_ensemble: object like :py:class:`.PathEnsemble`
                 The path ensemble we are writing restart info for.
          *  system : object like :py:class:`.System`
                 System is used here since we need access to the temperature
                 and to the particle list.
          *  order_function : object like :py:class:`.OrderParameter`
                 The class used for calculating the order parameter(s).
          *  engine : object like :py:class:`.EngineBase`
                 The engine to use for propagating a path.

    settings_ens : dict
        A dictionary with the ensemble settings.

    """
    info = copy.deepcopy(settings_ens)
    if ensemble.get('path_ensemble') is not None:
        info['path_ensemble'] = ensemble['path_ensemble'].restart_info()
    if ensemble.get('system') is not None:
        info['system'] = ensemble['system'].restart_info()
    if ensemble.get('engine') is not None:
        try:
            info['engine'] = ensemble['engine'].restart_info()
        except AttributeError:
            pass
        except ValueError:
            info['engine'] = {}

    if ensemble.get('rgen') is not None:
        info['rgen'] = ensemble['rgen'].get_state()

    filename = os.path.join(
        settings_ens['simulation']['exe_path'],
        ensemble['path_ensemble'].ensemble_name_simple,
        'ensemble.restart')
    with open(filename, 'wb') as outfile:
        pickle.dump(info, outfile)


def read_restart_file(filename):
    """Read restart info for a simulation.

    Parameters
    ----------
    filename : string
        The file we are going to read from.

    """
    with open(filename, 'rb') as infile:
        info = pickle.load(infile)
    return info
