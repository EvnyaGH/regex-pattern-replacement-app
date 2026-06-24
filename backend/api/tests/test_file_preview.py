from io import BytesIO

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, SimpleTestCase, override_settings
from openpyxl import Workbook


class FilePreviewApiTests(SimpleTestCase):
    def test_preview_csv_returns_columns_rows_and_count(self):
        uploaded_file = SimpleUploadedFile(
            "emails.csv",
            b"ID,Name,Email\n1,John Doe,john.doe@example.com\n2,Jane Smith,jane_smith@domain.com\n",
            content_type="text/csv",
        )

        response = Client().post(
            "/api/files/preview",
            {"file": uploaded_file, "preview_limit": "1"},
        )

        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual(payload["filename"], "emails.csv")
        self.assertEqual(payload["columns"], ["ID", "Name", "Email"])
        self.assertEqual(payload["row_count"], 2)
        self.assertEqual(payload["preview_limit"], 1)
        self.assertEqual(len(payload["rows"]), 1)
        self.assertEqual(payload["rows"][0]["Email"], "john.doe@example.com")

    def test_preview_xlsx_returns_columns_rows_and_count(self):
        workbook = Workbook()
        worksheet = workbook.active
        worksheet.append(["ID", "Name", "Email"])
        worksheet.append([1, "John Doe", "john.doe@example.com"])
        worksheet.append([2, "Jane Smith", "jane_smith@domain.com"])
        stream = BytesIO()
        workbook.save(stream)

        uploaded_file = SimpleUploadedFile(
            "emails.xlsx",
            stream.getvalue(),
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )

        response = Client().post(
            "/api/files/preview",
            {"file": uploaded_file, "preview_limit": "2"},
        )

        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual(payload["columns"], ["ID", "Name", "Email"])
        self.assertEqual(payload["row_count"], 2)
        self.assertEqual(len(payload["rows"]), 2)

    def test_preview_rejects_unsupported_file_type(self):
        uploaded_file = SimpleUploadedFile(
            "notes.txt",
            b"not,a,supported,file\n",
            content_type="text/plain",
        )

        response = Client().post("/api/files/preview", {"file": uploaded_file})

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["error"]["code"], "INVALID_FILE_TYPE")

    def test_preview_rejects_empty_file(self):
        uploaded_file = SimpleUploadedFile(
            "empty.csv",
            b"",
            content_type="text/csv",
        )

        response = Client().post("/api/files/preview", {"file": uploaded_file})

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["error"]["code"], "EMPTY_FILE")

    @override_settings(MAX_UPLOAD_BYTES=5)
    def test_preview_rejects_file_over_size_limit(self):
        uploaded_file = SimpleUploadedFile(
            "emails.csv",
            b"ID,Name,Email\n1,John Doe,john.doe@example.com\n",
            content_type="text/csv",
        )

        response = Client().post("/api/files/preview", {"file": uploaded_file})

        self.assertEqual(response.status_code, 413)
        self.assertEqual(response.json()["error"]["code"], "FILE_TOO_LARGE")

    def test_preview_rejects_invalid_preview_limit(self):
        uploaded_file = SimpleUploadedFile(
            "emails.csv",
            b"ID,Name,Email\n1,John Doe,john.doe@example.com\n",
            content_type="text/csv",
        )

        response = Client().post(
            "/api/files/preview",
            {"file": uploaded_file, "preview_limit": "0"},
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["error"]["code"], "INVALID_PREVIEW_LIMIT")

    def test_preview_rejects_corrupt_xlsx(self):
        uploaded_file = SimpleUploadedFile(
            "corrupt.xlsx",
            b"this is not an Excel workbook",
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )

        response = Client().post("/api/files/preview", {"file": uploaded_file})

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["error"]["code"], "FILE_PARSE_ERROR")
