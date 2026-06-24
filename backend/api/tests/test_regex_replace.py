import json

from django.test import Client, SimpleTestCase

from services.regex_generator import EMAIL_REGEX


class RegexReplaceApiTests(SimpleTestCase):
    def test_replace_pdf_email_example(self):
        response = Client().post(
            "/api/regex/replace",
            data=json.dumps({
                "columns": ["ID", "Name", "Email"],
                "rows": [
                    {"ID": 1, "Name": "John Doe", "Email": "john.doe@example.com"},
                    {"ID": 2, "Name": "Jane Smith", "Email": "jane_smith@domain.com"},
                    {"ID": 3, "Name": "Alice Brown", "Email": "alice.brown@website.org"},
                ],
                "target_column": "Email",
                "regex": EMAIL_REGEX,
                "replacement": "REDACTED",
            }),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual(payload["replacement_count"], 3)
        self.assertEqual(payload["affected_row_count"], 3)
        self.assertEqual([row["Email"] for row in payload["rows"]], ["REDACTED", "REDACTED", "REDACTED"])
        self.assertEqual(payload["rows"][0]["Name"], "John Doe")

    def test_replace_counts_multiple_matches_in_one_row(self):
        response = Client().post(
            "/api/regex/replace",
            data=json.dumps({
                "columns": ["ID", "Notes"],
                "rows": [
                    {"ID": 1, "Notes": "a@example.com and b@example.com"},
                    {"ID": 2, "Notes": "no email here"},
                ],
                "target_column": "Notes",
                "regex": EMAIL_REGEX,
                "replacement": "REDACTED",
            }),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual(payload["replacement_count"], 2)
        self.assertEqual(payload["affected_row_count"], 1)
        self.assertEqual(payload["rows"][0]["Notes"], "REDACTED and REDACTED")
        self.assertEqual(payload["rows"][1]["Notes"], "no email here")

    def test_no_matches_returns_success_with_zero_counts(self):
        response = Client().post(
            "/api/regex/replace",
            data=json.dumps({
                "columns": ["ID", "Email"],
                "rows": [{"ID": 1, "Email": "not an address"}],
                "target_column": "Email",
                "regex": EMAIL_REGEX,
                "replacement": "REDACTED",
            }),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual(payload["replacement_count"], 0)
        self.assertEqual(payload["affected_row_count"], 0)
        self.assertEqual(payload["rows"][0]["Email"], "not an address")

    def test_rejects_missing_target_column(self):
        response = Client().post(
            "/api/regex/replace",
            data=json.dumps({
                "columns": ["ID", "Email"],
                "rows": [{"ID": 1, "Email": "john.doe@example.com"}],
                "target_column": " ",
                "regex": EMAIL_REGEX,
                "replacement": "REDACTED",
            }),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["error"]["code"], "MISSING_TARGET_COLUMN")

    def test_rejects_target_column_not_found(self):
        response = Client().post(
            "/api/regex/replace",
            data=json.dumps({
                "columns": ["ID", "Name"],
                "rows": [{"ID": 1, "Name": "John Doe"}],
                "target_column": "Email",
                "regex": EMAIL_REGEX,
                "replacement": "REDACTED",
            }),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["error"]["code"], "TARGET_COLUMN_NOT_FOUND")

    def test_rejects_invalid_regex(self):
        response = Client().post(
            "/api/regex/replace",
            data=json.dumps({
                "columns": ["ID", "Email"],
                "rows": [{"ID": 1, "Email": "john.doe@example.com"}],
                "target_column": "Email",
                "regex": "[",
                "replacement": "REDACTED",
            }),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["error"]["code"], "INVALID_REGEX")

    def test_rejects_empty_regex(self):
        response = Client().post(
            "/api/regex/replace",
            data=json.dumps({
                "columns": ["ID", "Email"],
                "rows": [{"ID": 1, "Email": "john.doe@example.com"}],
                "target_column": "Email",
                "regex": " ",
                "replacement": "REDACTED",
            }),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["error"]["code"], "INVALID_REGEX")

    def test_rejects_no_rows(self):
        response = Client().post(
            "/api/regex/replace",
            data=json.dumps({
                "columns": ["ID", "Email"],
                "rows": [],
                "target_column": "Email",
                "regex": EMAIL_REGEX,
                "replacement": "REDACTED",
            }),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["error"]["code"], "NO_ROWS")

    def test_empty_replacement_deletes_matches(self):
        response = Client().post(
            "/api/regex/replace",
            data=json.dumps({
                "columns": ["ID", "Email"],
                "rows": [{"ID": 1, "Email": "john.doe@example.com"}],
                "target_column": "Email",
                "regex": EMAIL_REGEX,
                "replacement": "",
            }),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["rows"][0]["Email"], "")
