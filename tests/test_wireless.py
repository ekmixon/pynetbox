import unittest
import six

import pynetbox
from .util import Response

if six.PY3:
    from unittest.mock import patch
else:
    from mock import patch


api = pynetbox.api("http://localhost:8000")

nb_app = api.wireless

HEADERS = {"accept": "application/json;"}


class Generic(object):
    class Tests(unittest.TestCase):
        name = ""
        ret = pynetbox.core.response.Record
        app = "wireless"

        def test_get_all(self):
            with patch("requests.sessions.Session.get", return_value=Response(fixture=f"{self.app}/{self.name}.json")) as mock:
                ret = list(getattr(nb_app, self.name).all())
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
                ret = list(getattr(nb_app, self.name).filter(name="test"))
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
                ret = getattr(nb_app, self.name).get(1)
                self.assertTrue(ret)
                self.assertTrue(isinstance(ret, self.ret))
                mock.assert_called_with(
                    f'http://localhost:8000/api/{self.app}/{self.name.replace("_", "-")}/1/',
                    params={},
                    json=None,
                    headers=HEADERS,
                )


class WirelessLansTestCase(Generic.Tests):
    name = "wireless_lans"

    @patch(
        "requests.sessions.Session.get",
        return_value=Response(fixture="wireless/wireless_lan.json"),
    )
    def test_repr(self, _):
        wireless_lan_obj = nb_app.wireless_lans.get(1)
        self.assertEqual(type(wireless_lan_obj), pynetbox.models.wireless.WirelessLans)
        self.assertEqual(str(wireless_lan_obj), "SSID 1")
