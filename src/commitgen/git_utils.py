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
