# Demo Guide

## Live Demo

https://regex-pattern-replacement-app.vercel.app

The Render backend can require a cold start after inactivity. If the first
request times out, wait briefly and retry once.

## Email Redaction Walkthrough

Use `samples/email_sample.csv`.

1. Open the live application.
2. Select the sample CSV.
3. Choose **Preview data**.
4. Confirm the `ID`, `Name`, and `Email` columns and three rows.
5. Keep `Email` as the target column.
6. Enter `Find email addresses in the Email column`.
7. Choose **Generate regex**.
8. Confirm that the interface displays a regex, explanation, and provider.
9. Set the replacement value to `REDACTED`.
10. Choose **Replace matches**.
11. Confirm three replacements, three affected rows, and unchanged `ID` and
    `Name` values.

## Real LLM Walkthrough

The production backend uses the OpenAI provider.

1. Upload a file containing a phone-number column, or reuse the existing
   preview and select an appropriate text column.
2. Enter `Find Australian mobile phone numbers`.
3. Generate the regex.
4. Confirm `Provider: openai` appears below the regex.
5. Inspect the explanation before applying any replacement.

## Suggested Recording

A concise public demonstration can be recorded in about three minutes:

```text
00:00  Show the live URL and describe the problem.
00:15  Upload the sample CSV and preview the table.
00:40  Select Email and generate a regex from natural language.
01:10  Inspect the generated regex and explanation.
01:30  Replace matches with REDACTED.
01:50  Show replacement statistics and preserved columns.
02:10  Generate an Australian mobile regex with the OpenAI provider.
02:40  Show the public API docs and repository.
```

## Recording Safety

- Use only the committed sample file or synthetic data.
- Hide browser extensions, notifications, personal tabs, and local paths.
- Never show API keys, Render variables, Vercel variables, billing pages, or
  terminal history containing secrets.
- Avoid recording OpenAI usage identifiers or private account information.

## Publication Checklist

- [ ] Video uses only synthetic data.
- [ ] Core upload, generation, and replacement flow is visible.
- [ ] Replacement counts are visible.
- [ ] Real OpenAI provider behavior is visible.
- [ ] Public URLs are readable.
- [ ] Captions or clear narration are included.
- [ ] Published video URL is added to README and this document.

Demo video URL: not published yet.
