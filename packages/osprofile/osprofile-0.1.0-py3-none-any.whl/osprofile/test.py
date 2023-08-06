import unittest
import os
import json
from osprofile import OSProfile


class TestOSProfile(unittest.TestCase):

    def setUp(self):

        self.options = dict(test='test')
        self.osp = OSProfile(appname='test_app',
                             profile='test_app.json', options=self.options)

    def tearDown(self):
        pass

    def test_init(self):

        if os.path.exists(os.path.join(self.osp.path, self.osp.profile)):
            with open(os.path.join(self.osp.path, self.osp.profile)) as f:
                self.assertEqual(self.options, json.loads(f.read()))
        else:
            self.fail('Init Failed.')

    def test_read_profile(self):
        self.assertDictEqual(self.osp.read_profile(), self.options)

    def test_update_profile(self):
        options = dict(test='123456')
        self.osp.update_profile(options)
        self.assertDictEqual(self.osp.read_profile(), options)


if __name__ == '__main__':
    unittest.main()
