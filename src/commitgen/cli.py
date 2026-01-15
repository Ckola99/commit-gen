import typer
import commitgen.git_utils as git_utils

app = typer.Typer(help="CommitGen – AI-powered Conventional Commit generator")


@app.command()
def commit():
    """
    Generate a Conventional Commit message from staged changes.
    """
    typer.echo("Starting commit workflow...")

    # STEP 1: Verify we are inside a Git repository
    typer.echo("Verifying git repository...")
    if not git_utils.verify_repo():
        typer.echo("Error: You are not inside a Git repository.")


    # STEP 2: Check for staged files
    typer.echo("Checking for staged changes...")
    if not git_utils.has_staged_changes():
        typer.echo("Error: No staged changes found. Please stage your changes before committing.")
        return

    # STEP 3: Extract staged diff
    typer.echo("Extracting staged diff...")
    # later → git_utils.get_staged_diff()

    # Everything else comes later
    typer.echo("Workflow scaffold complete.")


@app.command()
def version():
    """
    Show CommitGen version.
    """
    typer.echo("CommitGen version: 0.1.0")
