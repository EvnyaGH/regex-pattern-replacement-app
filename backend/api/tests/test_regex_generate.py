import json
import re

from django.test import Client, SimpleTestCase

from services.regex_generator import RegexGenerationError, validate_generated_regex


class RegexGenerateApiTests(SimpleTestCase):
    def test_generate_email_regex_from_english_description(self):
        response = Client().post(
            "/api/regex/generate",
            data=json.dumps({
                "natural_language": "Find email addresses in the Email column",
                "target_column": "Email",
                "sample_values": [
                    "john.doe@example.com",
                    "jane_smith@domain.com",
                    "alice.brown@website.org",
                ],
            }),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual(payload["provider"], "mock")
        self.assertIsNotNone(re.fullmatch(payload["regex"], "john.doe@example.com"))
        re.compile(payload["regex"])

    def test_generate_email_regex_from_chinese_description(self):
        response = Client().post(
            "/api/regex/generate",
            data=json.dumps({
                "natural_language": "查找邮箱地址",
                "target_column": "Email",
                "sample_values": ["john.doe@example.com"],
            }),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["provider"], "mock")

    def test_generate_email_regex_from_sample_values(self):
        response = Client().post(
            "/api/regex/generate",
            data=json.dumps({
                "natural_language": "Find sensitive identifiers",
                "target_column": "Contact",
                "sample_values": ["john.doe@example.com", "jane_smith@domain.com"],
            }),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["provider"], "mock")

    def test_rejects_empty_description(self):
        response = Client().post(
            "/api/regex/generate",
            data=json.dumps({
                "natural_language": "   ",
                "target_column": "Email",
                "sample_values": ["john.doe@example.com"],
            }),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["error"]["code"], "EMPTY_DESCRIPTION")

    def test_rejects_missing_target_column(self):
        response = Client().post(
            "/api/regex/generate",
            data=json.dumps({
                "natural_language": "Find email addresses",
                "target_column": " ",
                "sample_values": ["john.doe@example.com"],
            }),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["error"]["code"], "MISSING_TARGET_COLUMN")

    def test_unsupported_mock_description_returns_generation_error(self):
        response = Client().post(
            "/api/regex/generate",
            data=json.dumps({
                "natural_language": "Find product SKUs",
                "target_column": "SKU",
                "sample_values": ["ABC-123"],
            }),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["error"]["code"], "LLM_GENERATION_FAILED")

    def test_generated_regex_validation_rejects_invalid_regex(self):
        with self.assertRaises(RegexGenerationError) as context:
            validate_generated_regex("[")

        self.assertEqual(context.exception.code, "INVALID_GENERATED_REGEX")
        self.assertIn("Generated regex could not be compiled", str(context.exception))

    def test_unsupported_provider_returns_configuration_error(self):
        with self.settings(LLM_PROVIDER="unsupported"):
            response = Client().post(
                "/api/regex/generate",
                data=json.dumps({
                    "natural_language": "Find email addresses",
                    "target_column": "Email",
                    "sample_values": [],
                }),
                content_type="application/json",
            )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["error"]["code"], "LLM_PROVIDER_NOT_SUPPORTED")
