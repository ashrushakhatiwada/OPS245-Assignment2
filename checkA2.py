#!/usr/bin/env python3

import unittest
from random import randint
import sys, os
import subprocess as sp
from importlib import import_module
from unittest.mock import mock_open, patch, call

'''
ASSIGNMENT 2 CHECK SCRIPT
Version A: Proc Report
Author: Eric Brauer eric.brauer@senecapolytechnic.ca

Description:

The precise requirements of each student-created function are specified elsewhere.

The script assumes that the student's filename is named 'assignment2.py' and exists in the same directory as this check script.

NOTE: Feel free to _fork_ and modify this script to suit needs. I will try to fix any issues that arise but this script is provided as-is, with no obligation of warranty or support.
'''

class TestModuleRestriction(unittest.TestCase):
    "no modules apart from allowed are being imported"
    
    def setUp(self):
        self.filename = 'assignment2.py'
        self.pypath = sys.executable
        error_output = f'{self.filename} cannot be found (HINT: make sure this script AND your file are in the same directory)'
        file = os.path.join(os.getcwd(), self.filename)
        self.assertTrue(os.path.exists(file), msg=error_output)
        try:
            self.a2 = import_module(self.filename.split('.')[0])
        except ModuleNotFoundError:
            print("Cannot find a function inside your assignment2.py. Do not rename or delete any of the required functions.")
    
    def test_unallowed_module(self):
        "you have imported a prohibited module"
        verboten = ['psutil']
        allowed = ["sys", "subprocess", "argparse", "os"]
        for mod in verboten:
            if mod in sys.modules:
                raise AssertionError(f'You have imported a prohibited module.'
                    f'module {mod} is not allowed. Review the Wiki' 
                    ' instructions again.')


class TestPercent(unittest.TestCase):
    "percent_to_graph is working"
    
    def setUp(self):
        self.filename = 'assignment2.py'
        self.pypath = sys.executable
        error_output = f'{self.filename} cannot be found (HINT: make sure this script AND your file are in the same directory)'
        file = os.path.join(os.getcwd(), self.filename)
        self.assertTrue(os.path.exists(file), msg=error_output)
        try:
            self.a2 = import_module(self.filename.split('.')[0])
        except ModuleNotFoundError:
            print("Cannot find a function inside your assignment2.py. Do not rename or delete any of the required functions.")
    
    def test_percent(self):
        "percent_to_graph returns correct '##    ' format"
        percent_list = [33, 56, 70, 63, 89]
        max_list = [10, 15, 20, 30, 80]
        for i in range(0, (len(percent_list)-1)):
            given = self.a2.percent_to_graph((percent_list[i]/100), max_list[i])  # pcnt is 0.0 - 1.0
            inv_pcnt = 100 - percent_list[i]  # to get spaces rather than symbols
            num_spcs = round((max_list[i] * inv_pcnt) / 100) 
            expected = ' ' * num_spcs
            error_msg = "The output of percent_to_graph() with the argument " + str(percent_list[i]) + " is returning the wrong value"
            self.assertIn(expected, given, error_msg)
            self.assertEqual(max_list[i], len(given), error_msg)


class TestMemFuncs(unittest.TestCase):
    "get_sys_mem and get_avail_mem are working"

    mem1 = f'32{randint(0,9)}93367'
    mem2 = f'191{randint(0,9)}640' 
    mem3 = f'25{randint(0,9)}24192'

    data = (f'MemTotal:       {mem1} kB\n'
            f'MemFree:         {mem2} kB\n'
            f'MemAvailable:   {mem3} kB\n'
            'Buffers:         1908176 kB\n'
            'Cached:         20887140 kB\n'
            'SwapCached:            0 kB\n'
            'Active:          8902796 kB\n'
            'Inactive:       17753404 kB\n'
            'Active(anon):      68408 kB\n'
            'Inactive(anon):  4382760 kB')

    def setUp(self):
        self.filename = 'assignment2.py'
        self.pypath = sys.executable
        error_output = f'{self.filename} cannot be found (HINT: make sure this script AND your file are in the same directory)'
        file = os.path.join(os.getcwd(), self.filename)
        self.assertTrue(os.path.exists(file), msg=error_output)
        try:
            self.a2 = import_module(self.filename.split('.')[0])
        except ModuleNotFoundError:
            print("Cannot find a function inside your assignment2.py. Do not rename or delete any of the required functions.")

    def test_meminfo_total(self):
        error = ('ERROR: not opening meminfo for memory usage. Use open()'
                 ' and the arguments "/proc/meminfo", "r". ')
        m = mock_open(read_data=self.data)
        with patch('builtins.open', m, create=True):
            given = self.a2.get_sys_mem()
            expected = int(self.mem1)
            self.assertEqual(given, expected, error)
            self.assertEqual(m.call_count, 1, error)
            m.assert_has_calls([call('/proc/meminfo', 'r')])

    def test_meminfo_avail(self):
        error = ('ERROR: not opening meminfo for memory usage. Use open()'
                 ' and the arguments "/proc/meminfo", "r". ')
        m = mock_open(read_data=self.data)
        with patch('builtins.open', m, create=True):
            given = self.a2.get_avail_mem()
            expected = int(self.mem3)
            self.assertEqual(given, expected, error)
            self.assertEqual(m.call_count, 1, error)
            m.assert_has_calls([call('/proc/meminfo', 'r')])

'''
I decided I didn't care about making this, BUT:
you can call main block with a2.main(), but also need to
capture stdout correctly. for future reference!
'''
@unittest.skip("Not implemented, please ignore!")
class TestNoArgs(unittest.TestCase):
    "running script without args"
    ...

    pcnt = 0.5
    mem1 = randint(10000,100000)
    mem2 = f'191{randint(0,9)}640' 
    mem3 = mem1 * pcnt

    data = (f'MemTotal:       {mem1} kB\n'
            f'MemFree:         {mem2} kB\n'
            f'MemAvailable:   {mem3} kB\n'
            'Buffers:         1908176 kB\n'
            'Cached:         20887140 kB\n'
            'SwapCached:            0 kB\n'
            'Active:          8902796 kB\n'
            'Inactive:       17753404 kB\n'
            'Active(anon):      68408 kB\n'
            'Inactive(anon):  4382760 kB')

    def setUp(self):
        self.filename = 'assignment2.py'
        self.pypath = sys.executable
        error_output = f'{self.filename} cannot be found (HINT: make sure this script AND your file are in the same directory)'
        file = os.path.join(os.getcwd(), self.filename)
        self.assertTrue(os.path.exists(file), msg=error_output)
        try:
            self.a2 = import_module(self.filename.split('.')[0])
        except ModuleNotFoundError:
            print("Cannot find a function inside your assignment2.py. Do not rename or delete any of the required functions.")

    def test_prog_output_no_args(self):
        "running assignment2.py"
        error_msg = 'Error: make sure running your program with no arguments returns the correct output.'
        m = mock_open(read_data=self.data)
        with patch('builtins.open', m, create=True):
            cmd = [self.pypath, self.filename]
            p = sp.Popen(cmd, stdin=sp.PIPE, stdout=sp.PIPE, stderr=sp.PIPE)
            output, error = p.communicate()
            expected=[f'{self.pcnt:.0%}', 
                      f'{self.mem1}',
                      f'{self.mem3}',
                      r'\S\s{10}\S']
            for e in expected:
                self.assertRegex(output.decode('utf-8'), e, error_msg)


class TestParseArgs(unittest.TestCase):
    "parse_command_args is working"

    def setUp(self):
        self.filename = 'assignment2.py'
        self.pypath = sys.executable
        error_output = f'{self.filename} cannot be found (HINT: make sure this script AND your file are in the same directory)'
        file = os.path.join(os.getcwd(), self.filename)
        self.assertTrue(os.path.exists(file), msg=error_output)
        try:
            self.a2 = import_module(self.filename.split('.')[0])
        except ModuleNotFoundError:
            print("Cannot find a function inside your assignment2.py. Do not rename or delete any of the required functions.")

    def test_argparse_help(self):
        "assignment2.py -h returns the required options"
        p = sp.Popen(['/usr/bin/python3', self.filename, '-h'], stdout=sp.PIPE, stdin=sp.PIPE, stderr=sp.PIPE)
        stdout, err = p.communicate()
        # Fail test if process returns a no zero exit status
        return_code = p.wait()
        error_output = 'Output of `assignment2.py -h` doesn\'t match what\'s expected. Make sure you\'ve added an option!)'
        expected_out = ["[-h]", "[-H]", "[-l LENGTH]", "[program]"]
        for string in expected_out:
            self.assertIn(string, stdout.decode('utf-8'), msg=error_output)


class TestPidList(unittest.TestCase):
    "pids_of_prog is working"

    def setUp(self):
        self.filename = 'assignment2.py'
        self.pypath = sys.executable
        error_output = f'{self.filename} cannot be found (HINT: make sure this script AND your file are in the same directory)'
        file = os.path.join(os.getcwd(), self.filename)
        self.assertTrue(os.path.exists(file), msg=error_output)
        try:
            self.a2 = import_module(self.filename.split('.')[0])
        except ModuleNotFoundError:
            print("Cannot find a function inside your assignment2.py. Do not rename or delete any of the required functions.")

    def test_pids(self):
        error = 'Error: use os.popen to the call the "pidof" command. Use .read() to get the output. Return a list'
        pid_out = '197592 197549 197432 197417 165748 165718 165690 165669 165649 165623 165621 165620 165615'
        expected = pid_out.split()
        with patch.object(os, 'popen') as mock_popen:
            mock_popen().read.return_value = pid_out
            given = self.a2.pids_of_prog('code')
            self.assertEqual(given, expected, error)  
            self.assertEqual(mock_popen().read.call_count, 1, error)


class TestPidMem(unittest.TestCase):
    "get_mem_of_pid is working"

    mem = 9864

    data = ('Name:	zsh\n'
            'Umask:	0002\n'
            'State:	S (sleeping)\n'
            'Tgid:	74168\n'
            'Ngid:	0\n'
            'Pid:	74168\n'
            'PPid:	73327\n'
            'TracerPid:	0\n'
            'Uid:	1000	1000	1000	1000\n'
            'Gid:	1000	1000	1000	1000\n'
            'FDSize:	128\n'
            'Groups:	4 24 27 30 46 122 134 135 138 1000 \n'
            'NStgid:	74168\n'
            'NSpid:	74168\n'
            'NSpgid:	74168\n'
            'NSsid:	74168\n'
            'Kthread:	0\n'
            'VmPeak:	   18960 kB\n'
            'VmSize:	   18912 kB\n'
            'VmLck:	       0 kB\n'
            'VmPin:	       0 kB\n'
            'VmHWM:	    9864 kB\n'
            'VmRSS:	    9864 kB\n'
            'RssAnon:	    4744 kB\n'
            'RssFile:	    5120 kB\n'
            'RssShmem:	       0 kB\n'
            'VmData:	    4380 kB\n'
            'VmStk:	     328 kB\n'
            'VmExe:	     720 kB\n'
            'VmLib:	    2808 kB\n'
            'VmPTE:	      88 kB\n'
            'VmSwap:	       0 kB\n'
            'HugetlbPages:	       0 kB\n'
            'CoreDumping:	0\n'
            'THP_enabled:	1\n'
            'untag_mask:	0xffffffffffffffff\n'
            'Threads:	1\n'
            'SigQ:	1/127766\n'
            'SigPnd:	0000000000000000\n'
            'ShdPnd:	0000000000000000\n'
            'SigBlk:	0000000000000000\n'
            'SigIgn:	0000000000384000\n'
            'SigCgt:	0000000008013003\n'
            'CapInh:	0000000000000000\n'
            'CapPrm:	0000000000000000\n'
            'CapEff:	0000000000000000\n'
            'CapBnd:	000001ffffffffff\n'
            'CapAmb:	0000000000000000\n'
            'NoNewPrivs:	0\n'
            'Seccomp:	0\n'
            'Seccomp_filters:	0\n'
            'Speculation_Store_Bypass:	thread vulnerable\n'
            'SpeculationIndirectBranch:	conditional enabled\n'
            'Cpus_allowed:	00000fff\n'
            'Cpus_allowed_list:	0-11\n'      
            'Mems_allowed:	00000000,00000000,00000000,00000000,00000000,00000000,00000000,00000000,00000000,00000000,00000000,00000000,00000000,00000000,00000000,00000000,00000000,00000000,00000000,00000000,00000000,00000000,00000000,00000000,00000000,00000000,00000000,00000000,00000000,00000000,00000000,00000001\n'
            'Mems_allowed_list:	0\n'         
            'voluntary_ctxt_switches:	209\n' 
            'nonvoluntary_ctxt_switches:	8\n')

    def setUp(self):
        self.filename = 'assignment2.py'
        self.pypath = sys.executable
        error_output = f'{self.filename} cannot be found (HINT: make sure this script AND your file are in the same directory)'
        file = os.path.join(os.getcwd(), self.filename)
        self.assertTrue(os.path.exists(file), msg=error_output)
        try:
            self.a2 = import_module(self.filename.split('.')[0])
        except ModuleNotFoundError:
            print("Cannot find a function inside your assignment2.py. Do not rename or delete any of the required functions.")
    
    def test_rss_total(self):
        error = ('ERROR: not opening smaps for memory usage. Use open()'
                 ' and the arguments "/proc/<pid>/smaps". ')
        m = mock_open(read_data=self.data)
        with patch('builtins.open', m, create=True):
            given = self.a2.rss_mem_of_pid('whatever')
            expected = int(self.mem)
            self.assertEqual(given, expected, error)
            self.assertEqual(m.call_count, 1, error)


if __name__ == "__main__":
    unittest.main(buffer=True)