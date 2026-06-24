import json

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, SimpleTestCase, override_settings

from services.regex_generator import EMAIL_REGEX


class ApiErrorContractTests(SimpleTestCase):
    def setUp(self):
        self.client = Client()

    def test_missing_file_uses_structured_validation_error(self):
        response = self.client.post("/api/files/preview", {})

        self.assertEqual(response.status_code, 422)
        payload = response.json()
        self.assertEqual(payload["error"]["code"], "REQUEST_VALIDATION_ERROR")
        self.assertIn("fields", payload["error"]["details"])

    def test_malformed_json_uses_structured_body_error(self):
        response = self.client.post(
            "/api/regex/generate",
            data='{"natural_language":',
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["error"]["code"], "INVALID_REQUEST_BODY")

    def test_missing_json_fields_use_structured_validation_error(self):
        response = self.client.post(
            "/api/regex/generate",
            data=json.dumps({}),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 422)
        self.assertEqual(response.json()["error"]["code"], "REQUEST_VALIDATION_ERROR")

    @override_settings(MAX_NATURAL_LANGUAGE_LENGTH=10)
    def test_rejects_description_over_length_limit(self):
        response = self.client.post(
            "/api/regex/generate",
            data=json.dumps({
                "natural_language": "Find every email address",
                "target_column": "Email",
                "sample_values": [],
            }),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["error"]["code"], "DESCRIPTION_TOO_LONG")

    @override_settings(MAX_SAMPLE_VALUES=1)
    def test_rejects_too_many_sample_values(self):
        response = self.client.post(
            "/api/regex/generate",
            data=json.dumps({
                "natural_language": "Find email addresses",
                "target_column": "Email",
                "sample_values": ["a@example.com", "b@example.com"],
            }),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["error"]["code"], "TOO_MANY_SAMPLE_VALUES")

    @override_settings(MAX_REGEX_LENGTH=5)
    def test_rejects_regex_over_length_limit(self):
        response = self.client.post(
            "/api/regex/replace",
            data=json.dumps({
                "columns": ["Email"],
                "rows": [{"Email": "john.doe@example.com"}],
                "target_column": "Email",
                "regex": EMAIL_REGEX,
                "replacement": "REDACTED",
            }),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["error"]["code"], "REGEX_TOO_LONG")

    @override_settings(MAX_REPLACEMENT_LENGTH=3)
    def test_rejects_replacement_over_length_limit(self):
        response = self.client.post(
            "/api/regex/replace",
            data=json.dumps({
                "columns": ["Email"],
                "rows": [{"Email": "john.doe@example.com"}],
                "target_column": "Email",
                "regex": EMAIL_REGEX,
                "replacement": "REDACTED",
            }),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["error"]["code"], "REPLACEMENT_TOO_LONG")

    @override_settings(MAX_PROCESS_ROWS=1)
    def test_rejects_uploaded_file_over_row_limit(self):
        uploaded_file = SimpleUploadedFile(
            "emails.csv",
            b"ID,Email\n1,a@example.com\n2,b@example.com\n",
            content_type="text/csv",
        )

        response = self.client.post(
            "/api/files/process",
            {
                "file": uploaded_file,
                "target_column": "Email",
                "regex": EMAIL_REGEX,
                "replacement": "REDACTED",
            },
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["error"]["code"], "TOO_MANY_ROWS")
