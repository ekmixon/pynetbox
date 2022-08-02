import unittest
import six

from .util import Response
import pynetbox

if six.PY3:
    from unittest.mock import patch
else:
    from mock import patch


api = pynetbox.api(
    "http://localhost:8000",
)

nb = api.virtualization

HEADERS = {"accept": "application/json;"}


class Generic(object):
    class Tests(unittest.TestCase):
        name = ""
        ret = pynetbox.core.response.Record
        app = "virtualization"

        def test_get_all(self):
            with patch("requests.sessions.Session.get", return_value=Response(fixture=f"{self.app}/{self.name}.json")) as mock:
                ret = list(getattr(nb, self.name).all())
                self.assertTrue(ret)
                self.assertTrue(isinstance(ret[0], self.ret))
                mock.assert_called_with(
                    f'http://localhost:8000/api/{self.app}/{self.name.replace("_", "-")}/',
                    params={"limit": 0},
                    json=None,
                    headers=HEADERS,
                )

        def test_filter(self):
            with patch("requests.sessions.Session.get", return_value=Response(fixture=f"{self.app}/{self.name}.json")) as mock:
                ret = list(getattr(nb, self.name).filter(name="test"))
                self.assertTrue(ret)
                self.assertTrue(isinstance(ret[0], self.ret))
                mock.assert_called_with(
                    f'http://localhost:8000/api/{self.app}/{self.name.replace("_", "-")}/',
                    params={"name": "test", "limit": 0},
                    json=None,
                    headers=HEADERS,
                )

        def test_get(self):
            with patch("requests.sessions.Session.get", return_value=Response(fixture=f"{self.app}/{self.name[:-1]}.json")) as mock:
                ret = getattr(nb, self.name).get(1)
                self.assertTrue(ret)
                self.assertTrue(isinstance(ret, self.ret))
                mock.assert_called_with(
                    f'http://localhost:8000/api/{self.app}/{self.name.replace("_", "-")}/1/',
                    params={},
                    json=None,
                    headers=HEADERS,
                )


class ClusterTypesTestCase(Generic.Tests):
    name = "cluster_types"


class ClusterGroupsTestCase(Generic.Tests):
    name = "cluster_groups"


class ClustersTestCase(Generic.Tests):
    name = "clusters"


class VirtualMachinesTestCase(Generic.Tests):
    name = "virtual_machines"


class InterfacesTestCase(Generic.Tests):
    name = "interfaces"
