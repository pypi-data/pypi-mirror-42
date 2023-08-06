# -*- coding: utf-8 -*-
# Copyright (c) 2019, PyRETIS Development Team.
# Distributed under the LGPLv2.1+ License. See LICENSE for more info.
"""Test the initiate restart method."""
import logging
from io import StringIO
import unittest
from unittest.mock import patch
import os
import tempfile
import shutil
from math import isnan, isinf, isclose
from pyretis.inout.common import make_dirs
from pyretis.setup.createsimulation import create_simulation
from pyretis.inout.settings import parse_settings_file

logging.disable(logging.CRITICAL)
HERE = os.path.abspath(os.path.dirname(__file__))
RESTART = os.path.join(HERE, 'restart')


def compare_path_lines(line1, line2, rel_tol=1e-5):
    """Compare two path ensemble lines."""
    if line1.startswith('#') and line2.startswith('#'):
        return True
    stuff1 = line1.split()
    stuff2 = line2.split()
    idx = {
        0: int, 3: str, 4: str, 5: str, 7: str, 8: str, 9: float,
        10: float, 11: int, 12: int, 13: float, 14: int, 15: int
    }
    for i, func in idx.items():
        if func == str:
            check = func(stuff1[i]) == func(stuff2[i])
        else:
            check = isclose(func(stuff1[i]), func(stuff2[i]),
                            rel_tol=rel_tol)
        if not check:
            return False
    return True


def compare_numbers(i, j, rel_tol):
    """Compare two numbers for close-enough-equality."""
    for special in (isnan, isinf):
        if special(i) or special(j):
            return special(i) and special(j)
    return isclose(i, j, rel_tol=rel_tol)


def compare_num_lines(line1, line2, rel_tol=1e-9):
    """Compare number for two lines."""
    if line1.startswith('#') and line2.startswith('#'):
        return True
    num1 = [float(i) for i in line1.split()]
    num2 = [float(i) for i in line2.split()]
    check = [compare_numbers(i, j, rel_tol) for i, j in zip(num1, num2)]
    return all(check)


def compare_data_ensemble_files(file1, file2, line_check=compare_num_lines):
    """Compare the contents of two result files, line-by-line."""
    with open(file1, 'r') as input1:
        with open(file2, 'r') as input2:
            for line1, line2 in zip(input1, input2):
                if not line_check(line1, line2, rel_tol=1e-5):
                    return False
    return True


def setup_for_restart(settings, target_dir, files_to_copy):
    """Copy some simulation files to the given directory."""
    settings['simulation']['exe_path'] = target_dir
    settings['engine']['exe_path'] = target_dir
    settings['ensemble'][0]['simulation']['exe_path'] = target_dir

    for i in files_to_copy:
        file_name = os.path.basename(i)
        target = os.path.join(target_dir, file_name)
        shutil.copyfile(i, target)

    with patch('sys.stdout', new=StringIO()):
        simulation = create_simulation(settings)
    simulation.set_up_output(settings)
    return simulation


class TestInitiateRestart(unittest.TestCase):
    """Run the tests for the initiate restart method."""

    def _run_simulation(self, settings, simulation):
        """Just run a simulation."""
        with patch('sys.stdout', new=StringIO()):
            init = simulation.initiate(settings)
            self.assertTrue(init)
        for _ in simulation.run():
            pass
        simulation.write_restart(now=True)

    def _compare_simulation_results(self, dir1, dir2):
        """Compare output files from two simulations."""
        files = ('pathensemble.txt', 'order.txt', 'energy.txt', 'energy.txt')
        checkers = (compare_path_lines, compare_num_lines, compare_num_lines,
                    compare_num_lines)
        for file_name, check in zip(files, checkers):
            result1 = os.path.join(dir1, file_name)
            result2 = os.path.join(dir2, file_name)
            result = compare_data_ensemble_files(result1, result2,
                                                 line_check=check)
            if not result:
                print(dir1, dir2, file_name)
                print(result1, result2)
            self.assertTrue(result)

    def test_initiate_restart(self):
        """Test the initiate restart method."""
        startdir = os.getcwd()
        settings1 = parse_settings_file(
            os.path.join(RESTART, 'tis-run-full.rst')
        )
        settings2 = parse_settings_file(os.path.join(RESTART, 'tis-run-2.rst'))
        settings3 = parse_settings_file(
            os.path.join(RESTART, 'tis-run-2-4.rst')
        )
        with tempfile.TemporaryDirectory() as tempdir:
            settings1['engine']['exe_path'] =\
                os.path.join(tempdir, 'run-full')
            settings2['engine']['exe_path'] =\
                os.path.join(tempdir, 'run-2')
            settings3['engine']['exe_path'] =\
                os.path.join(tempdir, 'run-2-4')
            settings1['ensemble'][0]['engine']['exe_path'] =\
                os.path.join(tempdir, 'run-full')
            settings2['ensemble'][0]['engine']['exe_path'] =\
                os.path.join(tempdir, 'run-2')
            settings3['ensemble'][0]['engine']['exe_path'] =\
                os.path.join(tempdir, 'run-2-4')
            settings1['ensemble'][0]['simulation']['exe_path'] = \
                os.path.join(tempdir, 'run-full')
            settings2['ensemble'][0]['simulation']['exe_path'] = \
                os.path.join(tempdir, 'run-2')
            settings3['ensemble'][0]['simulation']['exe_path'] = \
                os.path.join(tempdir, 'run-2-4')
            settings3['ensemble'][0]['simulation']['restart'] = \
                os.path.join(tempdir, 'run-2', 'pyretis.restart')

            # First, run a full simulation which we will compare with:
            target_dir1 = os.path.join(tempdir, 'run-full')
            make_dirs(target_dir1)
            files_to_copy = [
                os.path.join(RESTART, 'initial.xyz'),
            ]
            simulation1 = setup_for_restart(settings1, target_dir1,
                                            files_to_copy)
            self._run_simulation(settings1, simulation1)
            del simulation1
            # Next, run a shorter simulation we will restart from.
            target_dir2 = os.path.join(tempdir, 'run-2')
            make_dirs(target_dir2)
            simulation2 = setup_for_restart(settings2, target_dir2,
                                            files_to_copy)
            self._run_simulation(settings2, simulation2)
            del simulation2
            # Restart from simulation 2:
            target_dir3 = os.path.join(tempdir, 'run-2-4')
            make_dirs(target_dir3)
            shutil.copytree(
                os.path.join(target_dir2, '001'),
                os.path.join(target_dir3, '001'),
            )
            simulation3 = setup_for_restart(settings3, target_dir3, [])
            os.chdir(target_dir3)
            self._run_simulation(settings3, simulation3)
            os.chdir(startdir)
            del simulation3
            # So far, so good. Compare outputs from simulation1 and
            # simulation3:
            self._compare_simulation_results(
                os.path.join(tempdir, 'run-full', '001'),
                os.path.join(tempdir, 'run-2-4', '001'),
            )


if __name__ == '__main__':
    unittest.main()
