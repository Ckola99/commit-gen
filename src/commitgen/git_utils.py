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
