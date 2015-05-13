import unittest
from pkg_resources import parse_version

import ratd.cliargs
from ratd.cliargs import CliArgs

import sys

# Redirect Standard Error from Argparse failures so they are quiet during testing
sys.stderr = sys.stdout


class CommandLineTestCases(unittest.TestCase):

    def test_with_empty_args(self):
        """
        User passes no args, and no parameters, should fail with TypeError
        """
        with self.assertRaises(TypeError):
             CliArgs()

    def test_with_unknown_args(self):
        """
        User passes no args, should raise with CliArgError
        """
        with self.assertRaises(ratd.cliargs.CliArgError):
             CliArgs('foomonkey')


    def test_with_empty_profile_args(self):
        """
        User passes no args, should fail with SystemExit
        """
        with self.assertRaises(SystemExit):
             CliArgs('profile')

    def test_with_explicit_profile_args(self):
        """
        User passes args, should pass
        """
        test_dict = CliArgs('profile', ['-l', '-n','-u','foo','-v','-v']).__dict__
        self.assertEqual('foo', test_dict['user'])
        self.assertEqual(2, test_dict['verbosity'])

        self.assertEqual(True, test_dict['listprofiles'])

    def test_with_empty_sample_args(self):
        """
        User passes no args, should fail with SystemExit
        """
        with self.assertRaises(SystemExit):
             CliArgs('sample')

    def test_with_explicit_sample_args(self):
        """
        User passes args, should pass
        """
        test_dict = CliArgs('sample', ['-a', '26', '-s', 'somefile', '-n','-u','foo','-v']).__dict__
        self.assertEqual('foo', test_dict['user'])
        self.assertEqual(1, test_dict['verbosity'])
        self.assertEqual('26', test_dict['analyzer_profile'])

    def test_with_empty_watch_args(self):
        """
        User passes no args, should fail with SystemExit
        """
        with self.assertRaises(SystemExit):
             CliArgs('watch')

    def test_with_explicit_watch_args(self):
        """
        User passes args, should pass
        """
        test_dict = CliArgs('watch', ['-a', '26', '-d', 'dir', '-n','-u','foo','-v']).__dict__
        self.assertEqual('foo', test_dict['user'])
        self.assertEqual(1, test_dict['verbosity'])
        self.assertEqual('dir', test_dict['directory'])

    def test_with_empty_search_args(self):
        """
        User passes no args, should fail with SystemExit
        """
        with self.assertRaises(SystemExit):
             CliArgs('search')

    def test_with_explicit_search_args(self):
        """
        User passes args, should pass
        """
        test_dict = CliArgs('search', ['-m', 'c35b154e995a9380664a95ef132df41f', '-n','-u','foo','-v']).__dict__
        self.assertEqual('c35b154e995a9380664a95ef132df41f', test_dict['md5'])

    def test_with_explicit_badmd5_search_args(self):
        """
        User passes md5 not of 32bits length, should fail
        """
        with self.assertRaises(SystemExit):
            CliArgs('search', ['-m', 'c35b1380664a95ef132df41f', '-n','-u','foo','-v']).__dict__
