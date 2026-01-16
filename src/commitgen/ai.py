def generate_commit_message(diff_text, context):
    """
    Function that generates a commit message based on the provided diff text and context.
    If no context is provided, it generates a commit message based solely off the diff.
    """
    if not diff_text:
        return "chore: no changes detected"

    msg = "feat: add new changes"
    if context:
        msg += f"\n\nContext: {context}"

    return msg
