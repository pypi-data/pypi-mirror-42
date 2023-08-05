from __future__ import absolute_import

from linode_api.errors import UnexpectedResponseError
from linode_api.objects import DerivedBase, Property


class Disk(DerivedBase):
    api_endpoint = '/linode/instances/{linode_id}/disks/{id}'
    derived_url_path = 'disks'
    parent_id_name='linode_id'

    properties = {
        'id': Property(identifier=True),
        'created': Property(is_datetime=True),
        'label': Property(mutable=True, filterable=True),
        'size': Property(filterable=True),
        'status': Property(filterable=True, volatile=True),
        'filesystem': Property(),
        'updated': Property(is_datetime=True),
        'linode_id': Property(identifier=True),
    }


    def duplicate(self):
        result = self._client.post(Disk.api_endpoint, model=self, data={})

        if not 'id' in result:
            raise UnexpectedResponseError('Unexpected response duplicating disk!', json=result)

        d = Disk(self._client, result['id'], self.linode_id, result)
        return d


    def reset_root_password(self, root_password=None):
        rpass = root_password
        if not rpass:
            from linode_api.objects.linode import Instance
            rpass = Instance.generate_root_password()

        params = {
            'password': rpass,
        }

        result = self._client.post(Disk.api_endpoint, model=self, data=params)

        if not 'id' in result:
            raise UnexpectedResponseError('Unexpected response duplicating disk!', json=result)

        self._populate(result)
        if not root_password:
            return True, rpass
        return True
