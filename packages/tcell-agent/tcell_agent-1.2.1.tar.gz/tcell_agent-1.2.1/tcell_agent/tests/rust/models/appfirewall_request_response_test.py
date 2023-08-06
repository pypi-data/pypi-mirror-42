import unittest

from tcell_agent.appsensor.meta import AppSensorMeta
from tcell_agent.rust.models.appfirewall_request_response import AppfirewallRequestResponse


class AppfirewallRequestTest(unittest.TestCase):

    def create_request_test(self):
        appsensor_meta = AppSensorMeta()
        appsensor_meta.remote_address = "192.168.1.1"
        appsensor_meta.method = "GET"
        appsensor_meta.path = "/some/path"
        appsensor_meta.location = "http://192.168.1.1/some/path?xss_param=<script>"
        appsensor_meta.route_id = "12345"
        appsensor_meta.session_id = "session_id"
        appsensor_meta.user_id = "user_id"
        appsensor_meta.request_content_bytes_len = 1024
        appsensor_meta.response_content_bytes_len = 2048
        appsensor_meta.get_dict = {"user": {"xss_param": "<script>"}}
        appsensor_meta.path_dict = {"xss_param": "<script>"}
        appsensor_meta.post_dict = {("already_flattened", "post_param"): "<script>"}
        appsensor_meta.files_dict = {("already_flattened", "file_param"): "<script>"}
        appsensor_meta.json_dict = {"json_param": "<script>"}
        appsensor_meta.cookie_dict = {"xss_param": "<script>"}
        appsensor_meta.headers_dict = {"xss_param": "<script>"}
        appsensor_meta.user_agent_str = "Mozilla"

        request_response = AppfirewallRequestResponse(appsensor_meta)

        self.assertEqual(
            request_response,
            {
                "method": "GET",
                "status_code": 200,
                "route_id": "12345",
                "path": "/some/path",
                "query_params": [{"name": "xss_param", "value": "<script>"}],
                "post_params": [
                    {"name": "post_param", "value": "<script>"},
                    {"name": "file_param", "value": "<script>"},
                    {"name": "json_param", "value": "<script>"}],
                "headers": [{"name": "xss_param", "value": "<script>"}],
                "cookies": [{"name": "xss_param", "value": "<script>"}],
                "path_params": [{"name": "xss_param", "value": "<script>"}],
                "remote_address": "192.168.1.1",
                "session_id": "session_id",
                "user_id": "user_id",
                "user_agent": "Mozilla",
                "request_bytes_length": 1024,
                "response_bytes_length": 2048,
                "full_uri": "http://192.168.1.1/some/path?xss_param=<script>",
                "database_result_sizes": [],
                "sql_exceptions": [],
            }
        )
