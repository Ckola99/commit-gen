def generate_commit_message(diff_text: str, context: str = "") -> str:
    """
    Pure function: Takes text, returns text.
    """
    if not diff_text:
        return "chore: no changes detected"

    msg = "feat: add new changes"
    if context:
        msg += f"\n\nContext: {context}"

    return msg
