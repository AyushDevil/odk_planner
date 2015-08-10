
import unittest, time, os.path, tempfile, shutil, subprocess, datetime

from config import config, ExcelConfig, lo
from odk_planner import PlannerDriver
from instance import driver, passwords, default_config, upload_config


class TestConfig(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        driver.logout()
        driver.login('admin', passwords['admin'])

    def modify_config(self):
        ''' changes config from demo/ and uploads to server
            :param report_mdays: config.xls cron.report_mdays setting
            :param template: will set template_DM to this template and
                activate sending of this template via cron '''
        ec = default_config()
        upload_config(ec)

    def test_no_errors(self):
        ec = default_config()
        upload_config(ec)
        assert driver.alerts() == []

    def test_no_password(self):
        ec = default_config()
        ec.set_rows('users', 'name', 'secretary', 'password', '')
        upload_config(ec)
        alerts = driver.alerts()
        assert sum(['empty password' in alert for alert in driver.alerts()]) > 0
        ec = ExcelConfig(driver.download_config())
        rows = ec.get_rows('users', 'name', 'secretary')
        assert len(rows) == 1 and rows[0]['password'] != ''

    def test_all_sheets(self):
        ec = default_config()
        del ec.sheets['colors']
        upload_config(ec)
        alerts = driver.alerts()
        error_msg = 'expected to find sheet'
        assert sum([error_msg in alert for alert in driver.alerts()]) > 0

    def test_unknown_plugin(self):
        ec = default_config()
        ec.sheets['xxx'] = [['key', 'value']]
        upload_config(ec)
        alerts = driver.alerts()
        error_msg = 'unknown sheet'
        assert sum([error_msg in alert for alert in driver.alerts()]) > 0

if __name__ == '__main__':
    unittest.main()


