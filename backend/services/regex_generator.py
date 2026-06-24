from __future__ import annotations

from dataclasses import dataclass, field
import re
from typing import Any

from django.conf import settings

from services.openai_llm import OpenAIProviderError, generate_with_openai


EMAIL_REGEX = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,7}\b"


@dataclass
class RegexGenerationError(Exception):
    code: str
    message: str
    status_code: int = 400
    details: dict[str, Any] = field(default_factory=dict)

    def __str__(self) -> str:
        return f"{self.code}: {self.message}"


def generate_regex(
    natural_language: str,
    target_column: str,
    sample_values: list[str] | None = None,
    provider: str | None = None,
) -> dict[str, str]:
    description = natural_language.strip()
    column = target_column.strip()
    samples = sample_values or []
    selected_provider = (provider or settings.LLM_PROVIDER or "mock").strip().lower()

    if not description:
        raise RegexGenerationError(
            code="EMPTY_DESCRIPTION",
            message="Natural language description is required.",
        )

    if len(description) > settings.MAX_NATURAL_LANGUAGE_LENGTH:
        raise RegexGenerationError(
            code="DESCRIPTION_TOO_LONG",
            message="Natural language description exceeds the configured length limit.",
            details={"max_length": settings.MAX_NATURAL_LANGUAGE_LENGTH},
        )

    if not column:
        raise RegexGenerationError(
            code="MISSING_TARGET_COLUMN",
            message="Target column is required.",
        )

    if len(column) > settings.MAX_TARGET_COLUMN_LENGTH:
        raise RegexGenerationError(
            code="TARGET_COLUMN_TOO_LONG",
            message="Target column name exceeds the configured length limit.",
            details={"max_length": settings.MAX_TARGET_COLUMN_LENGTH},
        )

    if len(samples) > settings.MAX_SAMPLE_VALUES:
        raise RegexGenerationError(
            code="TOO_MANY_SAMPLE_VALUES",
            message="Too many sample values were supplied.",
            details={"max_sample_values": settings.MAX_SAMPLE_VALUES},
        )

    if any(len(str(sample)) > settings.MAX_SAMPLE_VALUE_LENGTH for sample in samples):
        raise RegexGenerationError(
            code="SAMPLE_VALUE_TOO_LONG",
            message="A sample value exceeds the configured length limit.",
            details={"max_length": settings.MAX_SAMPLE_VALUE_LENGTH},
        )

    if selected_provider == "mock":
        result = _generate_with_mock(description, column, samples)
    elif selected_provider == "openai":
        try:
            result = generate_with_openai(description, column, samples)
        except OpenAIProviderError as exc:
            raise RegexGenerationError(
                code=exc.code,
                message=exc.message,
                status_code=exc.status_code,
                details=exc.details,
            ) from exc
    else:
        raise RegexGenerationError(
            code="LLM_PROVIDER_NOT_SUPPORTED",
            message="The configured LLM provider is not supported.",
            details={"provider": selected_provider},
        )

    validate_generated_regex(result["regex"])
    return result


def validate_generated_regex(regex: str) -> None:
    if not regex.strip():
        raise RegexGenerationError(
            code="INVALID_GENERATED_REGEX",
            message="Generated regex is empty.",
        )

    if len(regex) > settings.MAX_REGEX_LENGTH:
        raise RegexGenerationError(
            code="INVALID_GENERATED_REGEX",
            message="Generated regex exceeds the configured length limit.",
            details={"max_length": settings.MAX_REGEX_LENGTH},
        )

    try:
        re.compile(regex)
    except re.error as exc:
        raise RegexGenerationError(
            code="INVALID_GENERATED_REGEX",
            message="Generated regex could not be compiled.",
            details={"reason": str(exc)},
        ) from exc


def _generate_with_mock(description: str, target_column: str, sample_values: list[str]) -> dict[str, str]:
    if _looks_like_email_request(description, target_column, sample_values):
        return {
            "regex": EMAIL_REGEX,
            "explanation": "Matches common email addresses using local-part, domain, and TLD groups.",
            "provider": "mock",
        }

    raise RegexGenerationError(
        code="LLM_GENERATION_FAILED",
        message="The Phase 3 mock LLM only supports email address pattern generation.",
        details={"supported_patterns": ["email"]},
    )


def _looks_like_email_request(description: str, target_column: str, sample_values: list[str]) -> bool:
    text = f"{description} {target_column}".lower()
    email_keywords = ("email", "e-mail", "mail address", "邮箱", "邮件", "电子邮件")
    if any(keyword in text for keyword in email_keywords):
        return True

    non_empty_samples = [sample for sample in sample_values if sample]
    if not non_empty_samples:
        return False

    email_like_count = sum(1 for sample in non_empty_samples if "@" in sample and "." in sample)
    return email_like_count / len(non_empty_samples) >= 0.5
