import typer

app = typer.Typer(help="CommitGen – AI-powered Conventional Commit generator")


@app.command()
def commit():
    """
    Generate a Conventional Commit message from staged changes.
    """
    typer.echo("Starting commit workflow...")

    # STEP 1: Verify we are inside a Git repository
    typer.echo("Verifying git repository...")
    # later → git_utils.verify_repo()

    # STEP 2: Check for staged files
    typer.echo("Checking for staged changes...")
    # later → git_utils.has_staged_changes()

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
