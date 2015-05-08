import unittest
import vcr

from pkg_resources import parse_version

import ratd as robust
import ratd.api as core
from ratd.api import atd

class ATDTests(unittest.TestCase):

    # Create & Authenticate for subsequent tests
    @vcr.use_cassette('fixtures/vcr_cassettes/connect.yaml')
    def setUp(self):
        self.myatd = atd('atd.localhost.localdomain')
        error_control, data = self.myatd.connect('admin', 'password!')
        self.assertEqual(1, error_control)

    # Test myatd properties
    def test_connect(self):
        self.assertIsInstance(self.myatd.session, unicode)
        self.assertIsInstance(self.myatd.userId, unicode)
        self.assertGreaterEqual(parse_version(self.myatd.matdver), parse_version(u'3.4.4.1.0'))

    # Get the heartbeat value of the ATD Box
    @vcr.use_cassette('fixtures/vcr_cassettes/heartbeat.yaml')
    def test_heartbeat(self):
        error_control, data = self.myatd.heartbeat()
        self.assertEqual(1, error_control)

    # Get the vmprofilelist
    @vcr.use_cassette('fixtures/vcr_cassettes/vmprofiles.yaml')
    def test_vmprofilelist(self):
        error_control, data = self.myatd.get_vmprofiles()
        self.assertEqual(1, error_control)

    # Upload file to ATD Server
    @vcr.use_cassette('fixtures/vcr_cassettes/upload_file.yaml')
    def test_upload(self):
        error_control, data = self.myatd.upload_file('test/data/putty/putty_upx.exe', 24)  # Make this a windows Profile

        if error_control == 0:
            self.assertFalse(True)
        else:
            # print '\nFile %s uploaded\n'%data['file']
            self.assertIsInstance(data['jobId'], int)
            self.assertIsInstance(data['taskId'], int)
            self.assertIsInstance(data['md5'], unicode)
            self.assertIsInstance(data['size'], int)
            self.assertRegexpMatches(data['mimeType'], 'application')

    # Check status before requesting the report
    @vcr.use_cassette('fixtures/vcr_cassettes/check_status.yaml')
    def test_checkstatus_ok(self):
        error_control, data = self.myatd.check_status(20079)
        self.assertEqual(1, error_control)

    # Check status before requesting the report
    @vcr.use_cassette('fixtures/vcr_cassettes/check_status_notready.yaml')
    def test_checkstatus_waiting(self):
        error_control, data = self.myatd.check_status(20072)
        self.assertIn(error_control, [1,4])

    @vcr.use_cassette('fixtures/vcr_cassettes/get_report.yaml')
    def test_fetchreport(self):
        error_control, data = self.myatd.get_report(8062)
        if error_control == 1:
            self.assertIsInstance(data['Summary']['Verdict']['Severity'], unicode)
            self.assertIsInstance(data['Summary']['Verdict']['Description'], unicode)
        else:
            self.assertFalse(True)

    @vcr.use_cassette('fixtures/vcr_cassettes/disconnect.yaml')
    def test_disconnect(self):
        error_control, data = self.myatd.disconnect()
        # return(1,'Disconnection successful')
        self.assertEqual(1, error_control)

    if __name__ == '__main__':
        unittest.main()
