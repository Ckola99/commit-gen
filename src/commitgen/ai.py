def generate_commit_message(diff_text, context):
    """
    Function that generates a commit message based on the provided diff text and context.
    If no context is provided, it generates a commit message based solely off the diff.
    """
    if not diff_text.strip():
        return "chore: no changes detected"

    prompt = _build_prompt(diff_text, context)

    # TEMP: deterministic fallback
    return _fallback_commit_message(diff_text, context)


def _build_prompt(diff_text: str, context: str) -> str:
    prompt = (
        "You are an expert software engineer.\n"
        "Generate a Conventional Commit message based on the following git diff.\n\n"
        f"GIT DIFF:\n{diff_text}\n\n"
    )

    if context:
        prompt += f"ADDITIONAL CONTEXT:\n{context}\n\n"

    prompt += (
        "Rules:\n"
        "- Use Conventional Commits format\n"
        "- for each change type, use appropriate prefix ([FEAT], [FIX], [DOCS], [STYLE], [REFACTOR], [PERF], [TEST], [CI], [CHORE])\n"
        "- Be concise\n"
        "- If multiple change types are present, include both in the message\n"
        "- example if more than one change type detected '[FEAT]: add user login feature', '[FIX]: resolve crash on startup', '[DOCS]: update README with setup instructions'\n"
        "- Use present tense\n"
        "- Do not include explanations\n"
        "- If no changes detected, respond with '[CHORE]: no changes detected'\n"
        "- adding lines or stylistic changes or whitespace changes is considered a [CHORE]\n"
        "- If presented additional context use it to generate a more specific message\n"
        "- Cap message at 100 characters per change or feat\n"
    )

    return prompt

def _fallback_commit_message(diff_text: str, context: str) -> str:
    if not diff_text.strip():
        return "chore: no changes detected"

    base = "feat: update codebase"

    if context:
        return f"{base}\n\nContext: {context}"

    return base
