# -*- coding: utf-8 -*-
# Copyright (c) 2019, PyRETIS Development Team.
# Distributed under the LGPLv2.1+ License. See LICENSE for more info.
"""This module checks that the inputs are meaningful.

Important methods defined here
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

"""
import logging

logger = logging.getLogger(__name__)  # pylint: disable=C0103
logger.addHandler(logging.NullHandler())

__all__ = ['check_interfaces', 'check_engine', 'check_ensemble']


def check_ensemble(settings):
    """Check that the ensemble input parameters are complete.

    Parameters
    ----------
    settings : dict
        The settings needed to set up the simulation.

    """
    msg = [' ']
    success = True
    if 'ensemble' in settings:
        savelambda = []
        for ens in settings['ensemble']:
            try:
                savelambda.append(ens['interface'])
                if not ens['interface'] \
                        in settings['simulation']['interfaces']:
                    msg += ['The ensemble interface {} '.format(
                        ens['interface'])]
                    msg += ['is not present in the simulation interface']
                    msg += ['list']
                    success = False
            except ImportError:
                msg += ['An ensemble has been introduced without (!!!)']
                msg += [' its interface']
                success = False

        if not is_sorted(savelambda):
            msg += ['Interface positions in the ensemble simulation ']
            msg += ['interfaces input are NOT properly sorted ']
            msg += ['(ascending order)']
            success = False

    else:
        success = False
        msg += ['No ensemble in settings']

    if not success:
        msgtxt = '\n'.join(msg)
        logger.critical(msgtxt)
    return success


def check_engine(settings):
    """Check the engine settings.

    Checks that the input engine settings are correct, and
    automatically determine the 'internal' or 'external'
    engine setting.

    Parameters
    ----------
    engine : object like :py:class:`.EngineBase`
        The engine which will be used in the simulation.
    settings : dict
        The current input settings.

    """
    msg = [' ']
    success = True
    if settings['engine'].get('type') == 'external':

        if 'input_path' not in settings['engine']:
            msg += ['The section engine requires an input_path entry']
            success = False

        if 'gmx' in settings['engine'] and \
                'gmx_format' not in settings['engine']:
            success = False
            msg += ['File format is not specified for the engine']
        elif 'cp2k' in settings['engine'] and \
                'cp2k_format' not in settings['engine']:
            success = False
            msg += ['File format is not specified for the engine']

    if not success:
        msgtxt = '\n'.join(msg)
        logger.critical(msgtxt)

    return success


def check_interfaces(settings):
    """Check that the interfaces are properly defined.

    Parameters
    ----------
    settings : dict
        The current input settings.

    """
    msg = [' ']
    success = True
    if settings['simulation']['flux'] and \
            not settings['simulation']['zero_ensemble']:
        msg += ['Settings for flux and zero_ensemble make no sense']
        success = False

    if settings['simulation']['task'] in ['retis', 'tis']:
        if len(settings['simulation']['interfaces']) < 3:
            msg += ['Insufficient number of interfaces for {}'
                    .format(settings['simulation']['task'])]
            success = False

        if not is_sorted(settings['simulation']['interfaces']):
            msg += ['Interface positions in the simulation interfaces ']
            msg += ['input are NOT properly sorted (ascending order)']
            success = False

    if not success:
        msgtxt = '\n'.join(msg)
        logger.critical(msgtxt)

    return success


def is_sorted(lll):
    """Check if a list is sorted."""
    return all(aaa <= bbb for aaa, bbb in zip(lll[:-1], lll[1:]))
