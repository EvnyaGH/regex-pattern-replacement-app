import json

from django.test import Client, SimpleTestCase


class BackendRegexFlowTests(SimpleTestCase):
    def test_generate_then_replace_pdf_email_example(self):
        client = Client()
        rows = [
            {"ID": 1, "Name": "John Doe", "Email": "john.doe@example.com"},
            {"ID": 2, "Name": "Jane Smith", "Email": "jane_smith@domain.com"},
            {"ID": 3, "Name": "Alice Brown", "Email": "alice.brown@website.org"},
        ]

        generate_response = client.post(
            "/api/regex/generate",
            data=json.dumps({
                "natural_language": "Find email addresses in the Email column",
                "target_column": "Email",
                "sample_values": [row["Email"] for row in rows],
            }),
            content_type="application/json",
        )
        self.assertEqual(generate_response.status_code, 200)

        replace_response = client.post(
            "/api/regex/replace",
            data=json.dumps({
                "columns": ["ID", "Name", "Email"],
                "rows": rows,
                "target_column": "Email",
                "regex": generate_response.json()["regex"],
                "replacement": "REDACTED",
            }),
            content_type="application/json",
        )

        self.assertEqual(replace_response.status_code, 200)
        payload = replace_response.json()
        self.assertEqual(payload["replacement_count"], 3)
        self.assertEqual(payload["affected_row_count"], 3)
        self.assertEqual([row["Email"] for row in payload["rows"]], ["REDACTED", "REDACTED", "REDACTED"])
