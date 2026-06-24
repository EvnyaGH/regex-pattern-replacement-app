import json
from types import SimpleNamespace
from unittest.mock import patch

from django.test import Client, SimpleTestCase, override_settings
import httpx
from openai import (
    APIConnectionError,
    APIStatusError,
    APITimeoutError,
    AuthenticationError,
    RateLimitError,
)

from services.openai_llm import OpenAIProviderError, generate_with_openai


class FakeResponses:
    def __init__(self, response=None, error=None):
        self.response = response
        self.error = error
        self.last_request = None

    def create(self, **kwargs):
        self.last_request = kwargs
        if self.error:
            raise self.error
        return self.response


class FakeOpenAIClient:
    def __init__(self, response=None, error=None):
        self.responses = FakeResponses(response=response, error=error)


def completed_response(payload):
    return SimpleNamespace(
        status="completed",
        output_text=json.dumps(payload),
        output=[],
        incomplete_details=None,
    )


@override_settings(
    OPENAI_API_KEY="test-key",
    LLM_MODEL="gpt-5.5",
    LLM_TIMEOUT_SECONDS=20,
    LLM_MAX_RETRIES=1,
    LLM_MAX_OUTPUT_TOKENS=2000,
    LLM_REASONING_EFFORT="low",
)
class OpenAIProviderTests(SimpleTestCase):
    def test_generates_structured_regex_and_disables_storage(self):
        client = FakeOpenAIClient(
            response=completed_response({
                "regex": r"\b04\d{2}\s?\d{3}\s?\d{3}\b",
                "explanation": "Matches Australian mobile numbers.",
            })
        )

        result = generate_with_openai(
            "Find Australian mobile phone numbers",
            "Phone",
            ["0412 345 678"],
            client=client,
        )

        self.assertEqual(result["provider"], "openai")
        self.assertEqual(result["explanation"], "Matches Australian mobile numbers.")
        request = client.responses.last_request
        self.assertEqual(request["model"], "gpt-5.5")
        self.assertFalse(request["store"])
        self.assertEqual(request["reasoning"], {"effort": "low"})
        self.assertEqual(request["max_output_tokens"], 2000)
        self.assertTrue(request["text"]["format"]["strict"])
        self.assertEqual(
            request["text"]["format"]["schema"]["required"],
            ["regex", "explanation"],
        )

    @override_settings(OPENAI_API_KEY="")
    def test_missing_api_key_returns_configuration_error(self):
        with self.assertRaises(OpenAIProviderError) as context:
            generate_with_openai("Find emails", "Email", [])

        self.assertEqual(context.exception.code, "LLM_CONFIGURATION_ERROR")
        self.assertEqual(context.exception.status_code, 503)
        self.assertEqual(
            str(context.exception),
            "LLM_CONFIGURATION_ERROR: OPENAI_API_KEY is required when LLM_PROVIDER=openai.",
        )

    def test_refusal_returns_structured_provider_error(self):
        refusal = SimpleNamespace(
            status="completed",
            output_text="",
            output=[
                SimpleNamespace(
                    type="message",
                    content=[SimpleNamespace(type="refusal", refusal="Request refused.")],
                )
            ],
            incomplete_details=None,
        )

        with self.assertRaises(OpenAIProviderError) as context:
            generate_with_openai("Generate a pattern", "Value", [], client=FakeOpenAIClient(response=refusal))

        self.assertEqual(context.exception.code, "LLM_REFUSED")
        self.assertEqual(context.exception.status_code, 422)

    def test_incomplete_response_returns_structured_provider_error(self):
        incomplete = SimpleNamespace(
            status="incomplete",
            output_text="",
            output=[],
            incomplete_details=SimpleNamespace(reason="max_output_tokens"),
        )

        with self.assertRaises(OpenAIProviderError) as context:
            generate_with_openai("Find emails", "Email", [], client=FakeOpenAIClient(response=incomplete))

        self.assertEqual(context.exception.code, "LLM_INCOMPLETE_RESPONSE")
        self.assertEqual(context.exception.details["reason"], "max_output_tokens")

    def test_invalid_output_text_returns_structured_provider_error(self):
        invalid = SimpleNamespace(
            status="completed",
            output_text="not-json",
            output=[],
            incomplete_details=None,
        )

        with self.assertRaises(OpenAIProviderError) as context:
            generate_with_openai("Find emails", "Email", [], client=FakeOpenAIClient(response=invalid))

        self.assertEqual(context.exception.code, "LLM_INVALID_RESPONSE")

    def test_maps_openai_sdk_errors(self):
        request = httpx.Request("POST", "https://api.openai.com/v1/responses")
        cases = [
            (
                APITimeoutError(request),
                "LLM_TIMEOUT",
                504,
            ),
            (
                APIConnectionError(message="Connection failed", request=request),
                "LLM_CONNECTION_FAILED",
                502,
            ),
            (
                AuthenticationError(
                    "Invalid key",
                    response=httpx.Response(401, request=request),
                    body=None,
                ),
                "LLM_AUTHENTICATION_FAILED",
                503,
            ),
            (
                RateLimitError(
                    "Rate limited",
                    response=httpx.Response(429, request=request),
                    body=None,
                ),
                "LLM_RATE_LIMITED",
                429,
            ),
            (
                APIStatusError(
                    "Provider error",
                    response=httpx.Response(500, request=request),
                    body=None,
                ),
                "LLM_GENERATION_FAILED",
                502,
            ),
        ]

        for error, expected_code, expected_status in cases:
            with self.subTest(expected_code=expected_code):
                with self.assertRaises(OpenAIProviderError) as context:
                    generate_with_openai(
                        "Find emails",
                        "Email",
                        [],
                        client=FakeOpenAIClient(error=error),
                    )
                self.assertEqual(context.exception.code, expected_code)
                self.assertEqual(context.exception.status_code, expected_status)


class OpenAIGenerationApiTests(SimpleTestCase):
    @override_settings(
        LLM_PROVIDER="openai",
        OPENAI_API_KEY="test-key",
        LLM_MODEL="gpt-5.5",
    )
    @patch("services.regex_generator.generate_with_openai")
    def test_api_uses_openai_provider(self, generate_mock):
        generate_mock.return_value = {
            "regex": r"\b04\d{8}\b",
            "explanation": "Matches compact Australian mobile numbers.",
            "provider": "openai",
        }

        response = Client().post(
            "/api/regex/generate",
            data=json.dumps({
                "natural_language": "Find Australian mobile phone numbers",
                "target_column": "Phone",
                "sample_values": ["0412345678"],
            }),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["provider"], "openai")
        generate_mock.assert_called_once()

    @override_settings(
        LLM_PROVIDER="openai",
        OPENAI_API_KEY="",
        LLM_MODEL="gpt-5.5",
    )
    def test_api_reports_missing_openai_key_without_server_error(self):
        response = Client().post(
            "/api/regex/generate",
            data=json.dumps({
                "natural_language": "Find phone numbers",
                "target_column": "Phone",
                "sample_values": ["0412345678"],
            }),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 503)
        self.assertEqual(response.json()["error"]["code"], "LLM_CONFIGURATION_ERROR")

    @override_settings(
        LLM_PROVIDER="openai",
        OPENAI_API_KEY="test-key",
        LLM_MODEL="gpt-5.5",
    )
    @patch("services.regex_generator.generate_with_openai")
    def test_invalid_openai_regex_is_rejected_locally(self, generate_mock):
        generate_mock.return_value = {
            "regex": "[",
            "explanation": "Invalid test regex.",
            "provider": "openai",
        }

        response = Client().post(
            "/api/regex/generate",
            data=json.dumps({
                "natural_language": "Find values",
                "target_column": "Value",
                "sample_values": [],
            }),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["error"]["code"], "INVALID_GENERATED_REGEX")
