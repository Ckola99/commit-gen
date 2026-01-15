import subprocess

def verify_repo():
    """
    Verify that the current directory is inside a Git repository.
    """

    result =  subprocess.run(
        ["git", "rev-parse", "--is-inside-work-tree"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

    return result.returncode == 0

def stage_all_changes():
    """
    Stage all changes in the Git repository.
    """
    subprocess.run(
        ["git", "add", "."]
    )

def has_staged_changes():
    """
    Check if there are any staged changes in the Git repository.
    """
    result = subprocess.run(
        ["git", "diff", "--cached", "--quiet"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

    return result.returncode == 1

def get_staged_diff():
    """
    Returns the text of the staged chages.
    """
    result = subprocess.run(
        ["git", "diff", "--staged"],
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        return ""

    return result.stdout

def push_changes():
    """
    Push committed changes to the remote repository.
    """
    subprocess.run(
        ["git", "push"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

def commit_changes(commit_message: str):
    """
    Commit staged changes with the provided commit message.
    """
    subprocess.run(
        ["git", "commit", "-m", commit_message],
        check=True
    )
