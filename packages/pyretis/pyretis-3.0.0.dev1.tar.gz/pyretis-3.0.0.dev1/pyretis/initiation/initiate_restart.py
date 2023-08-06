# -*- coding: utf-8 -*-
# Copyright (c) 2019, PyRETIS Development Team.
# Distributed under the LGPLv2.1+ License. See LICENSE for more info.
"""This file contains functions used for initiation of paths.

Important methods defined here
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

initiate_restart (:py:func:`.initiate_restart`)
    A method that will get the initial path from the output from
    a previous simulation.
"""
import logging
import os
from pyretis.core.pathensemble import generate_ensemble_name
from pyretis.core.path import Path
from pyretis.inout import print_to_screen
from pyretis.inout.restart import read_restart_file
logger = logging.getLogger(__name__)  # pylint: disable=invalid-name
logger.addHandler(logging.NullHandler())


__all__ = ['initiate_restart']


def initiate_restart(simulation, settings, cycle):
    """Initialise paths by loading restart data.

    Parameters
    ----------
    simulation : object like :py:class:`.Simulation`
        The simulation we are setting up.
    settings : dictionary
        A dictionary with settings for the initiation.
    cycle : integer
        The simulation cycles we are starting at.

    """
    maxlen = settings['tis']['maxlength']
    for ensemble in simulation.ensembles:
        path_ensemble = ensemble['path_ensemble']
        name = path_ensemble.ensemble_name
        logger.info('Loading restart data for path ensemble %s:', name)
        print_to_screen(
            'Loading restart data for path ensemble {}:'.format(name),
            level='warning'
        )
        ensemble['engine'].exe_dir = path_ensemble.directory['generate']
        path = Path(rgen=path_ensemble.rgen, maxlen=maxlen)
        restart_file = os.path.join(
            generate_ensemble_name(path_ensemble.ensemble_number),
            'ensemble.restart')
        restart_info = read_restart_file(restart_file)

        path_ensemble.load_restart_info(restart_info['path_ensemble'], cycle)
        path.load_restart_info(restart_info['path_ensemble']['last_path'])

        yield True, path, path.status, path_ensemble
