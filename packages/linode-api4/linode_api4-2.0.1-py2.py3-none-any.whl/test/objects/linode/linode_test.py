from datetime import datetime

from test.base import ClientBaseCase
from linode_api.objects.base import MappedObject

from linode_api.objects import Config, Image, Instance


class LinodeTest(ClientBaseCase):
    """
    Tests methods of the Linode class
    """
    def test_get_linode(self):
        """
        Tests that a client is loaded correctly by ID
        """
        linode = Instance(self.client, 123)
        self.assertEqual(linode._populated, False)

        self.assertEqual(linode.label, "linode123")
        self.assertEqual(linode.group, "test")

        self.assertTrue(isinstance(linode.image, Image))
        self.assertEqual(linode.image.label, "Ubuntu 17.04")

    def test_rebuild(self):
        """
        Tests that you can rebuild with an image
        """
        linode = Instance(self.client, 123)

        with self.mock_post('/linode/instances/123') as m:
            pw = linode.rebuild('linode/debian9')

            self.assertIsNotNone(pw)
            self.assertTrue(isinstance(pw, str))

            self.assertEqual(m.call_url, '/linode/instances/123/rebuild')

            self.assertEqual(m.call_data, {
                "image": "linode/debian9",
                "root_pass": pw,
            })

    def test_available_backups(self):
        """
        Tests that a Linode can retrieve its own backups
        """
        linode = Instance(self.client, 123)

        backups = linode.available_backups

        # assert we got the correct number of automatic backups
        self.assertEqual(len(backups.automatic), 3)

        # examine one automatic backup
        b = backups.automatic[0]
        self.assertEqual(b.id, 12345)
        self.assertEqual(b._populated, True)
        self.assertEqual(b.status, 'successful')
        self.assertEqual(b.type, 'auto')
        self.assertEqual(b.created, datetime(year=2018, month=1, day=9, hour=0,
                                             minute=1, second=1))
        self.assertEqual(b.updated, datetime(year=2018, month=1, day=9, hour=0,
                                             minute=1, second=1))
        self.assertEqual(b.finished, datetime(year=2018, month=1, day=9, hour=0,
                                             minute=1, second=1))
        self.assertEqual(b.region.id, 'us-east-1a')
        self.assertEqual(b.label, None)
        self.assertEqual(b.message, None)

        self.assertEqual(len(b.disks), 2)
        self.assertEqual(b.disks[0].size, 1024)
        self.assertEqual(b.disks[0].label, 'Debian 8.1 Disk')
        self.assertEqual(b.disks[0].filesystem, 'ext4')
        self.assertEqual(b.disks[1].size, 0)
        self.assertEqual(b.disks[1].label, '256MB Swap Image')
        self.assertEqual(b.disks[1].filesystem, 'swap')

        self.assertEqual(len(b.configs), 1)
        self.assertEqual(b.configs[0], 'My Debian 8.1 Profile')

        # assert that snapshots came back as expected
        self.assertEqual(backups.snapshot.current, None)
        self.assertEqual(backups.snapshot.in_progress, None)

    def test_update_linode(self):
        """
        Tests that a Linode can be updated
        """
        with self.mock_put('linode/instances/123') as m:
            linode = Instance(self.client, 123)

            linode.label = "NewLinodeLabel"
            linode.group = "new_group"
            linode.save()

            self.assertEqual(m.call_url, '/linode/instances/123')
            self.assertEqual(m.call_data, {
                "label": "NewLinodeLabel",
                "group": "new_group"
            })

    def test_delete_linode(self):
        """
        Tests that deleting a Linode creates the correct api request
        """
        with self.mock_delete() as m:
            linode = Instance(self.client, 123)
            linode.delete()

            self.assertEqual(m.call_url, '/linode/instances/123')

    def test_reboot(self):
        """
        Tests that you can submit a correct reboot api request
        """
        linode = Instance(self.client, 123)
        result = {}

        with self.mock_post(result) as m:
            linode.reboot()
            self.assertEqual(m.call_url, '/linode/instances/123/reboot')

    def test_shutdown(self):
        """
        Tests that you can submit a correct shutdown api request
        """
        linode = Instance(self.client, 123)
        result = {}

        with self.mock_post(result) as m:
            linode.shutdown()
            self.assertEqual(m.call_url, '/linode/instances/123/shutdown')

    def test_boot(self):
        """
        Tests that you can submit a correct boot api request
        """
        linode = Instance(self.client, 123)
        result = {}

        with self.mock_post(result) as m:
            linode.boot()
            self.assertEqual(m.call_url, '/linode/instances/123/boot')

    def test_boot_with_config(self):
        """
        Tests that you can submit a correct boot with a config api request
        """
        linode = Instance(self.client, 123)
        config = linode.configs[0]
        result = {}

        with self.mock_post(result) as m:
            linode.boot(config=config)
            self.assertEqual(m.call_url, '/linode/instances/123/boot')

    def test_mutate(self):
        """
        Tests that you can submit a correct mutate api request
        """
        linode = Instance(self.client, 123)
        result = {}

        with self.mock_post(result) as m:
            linode.mutate()
            self.assertEqual(m.call_url, '/linode/instances/123/mutate')

