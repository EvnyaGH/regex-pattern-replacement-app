from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, SimpleTestCase

from services.regex_generator import EMAIL_REGEX


class FileProcessApiTests(SimpleTestCase):
    def test_processes_all_rows_while_returning_limited_preview(self):
        csv_rows = ["ID,Email"] + [
            f"{row_id},user{row_id}@example.com"
            for row_id in range(1, 61)
        ]
        uploaded_file = SimpleUploadedFile(
            "sixty-emails.csv",
            ("\n".join(csv_rows) + "\n").encode(),
            content_type="text/csv",
        )

        response = Client().post(
            "/api/files/process",
            {
                "file": uploaded_file,
                "target_column": "Email",
                "regex": EMAIL_REGEX,
                "replacement": "REDACTED",
                "preview_limit": "50",
            },
        )

        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual(payload["filename"], "sixty-emails.csv")
        self.assertEqual(payload["row_count"], 60)
        self.assertEqual(payload["preview_limit"], 50)
        self.assertEqual(len(payload["rows"]), 50)
        self.assertEqual(payload["replacement_count"], 60)
        self.assertEqual(payload["affected_row_count"], 60)
        self.assertTrue(all(row["Email"] == "REDACTED" for row in payload["rows"]))

    def test_rejects_missing_target_column_in_uploaded_file(self):
        uploaded_file = SimpleUploadedFile(
            "names.csv",
            b"ID,Name\n1,John Doe\n",
            content_type="text/csv",
        )

        response = Client().post(
            "/api/files/process",
            {
                "file": uploaded_file,
                "target_column": "Email",
                "regex": EMAIL_REGEX,
                "replacement": "REDACTED",
            },
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["error"]["code"], "TARGET_COLUMN_NOT_FOUND")

    def test_rejects_invalid_regex(self):
        uploaded_file = SimpleUploadedFile(
            "emails.csv",
            b"ID,Email\n1,john.doe@example.com\n",
            content_type="text/csv",
        )

        response = Client().post(
            "/api/files/process",
            {
                "file": uploaded_file,
                "target_column": "Email",
                "regex": "[",
                "replacement": "REDACTED",
            },
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["error"]["code"], "INVALID_REGEX")
