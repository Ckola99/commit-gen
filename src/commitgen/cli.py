import typer
import commitgen.git_utils as git_utils
from commitgen import ai

app = typer.Typer(help="CommitGen – AI-powered Conventional Commit generator")


@app.command()
def commit(push: bool = typer.Option(False, "--push", "-p", help="Push the commit after committing")):
    """
    Generate a Conventional Commit message from staged changes.
    """
    typer.echo("Starting commit workflow...")

    # STEP 1: Verify we are inside a Git repository
    typer.echo("Verifying git repository...")
    if not git_utils.verify_repo():
        typer.echo("Error: You are not inside a Git repository.")
        raise typer.Exit(code=1)


    # STEP 2: Check for staged files
    typer.echo("Checking for staged changes...")
    if not git_utils.has_staged_changes():
        typer.echo("No staged changes. Would you like to stage all changes? [y/N]")
        # This is where the CLI handles user interaction
        if typer.confirm("Stage all?"):
            git_utils.stage_all_changes()
        else:
            typer.echo("Aborting commit process. Stage some changes and try again.")
            raise typer.Exit(code=1)

    # STEP 3: Extract staged diff
    typer.echo("Extracting staged diff...")
    current_context = ""
    while True:
        diff_text = git_utils.get_staged_diff()
        if not diff_text.strip():
            typer.echo("Error: Unable to retrieve staged changes.")
            raise typer.Exit(code=1)

        message = ai.generate_commit_message(diff_text, current_context)

        typer.secho("\n--- Suggested Commit Message ---", fg=typer.colors.CYAN)
        typer.echo(message)
        typer.echo("---------------------------------\n")

        choice = typer.prompt("(a)ccept, (r)egenerate with context, (e)dit, or (q)uit?")

        if choice.lower() == 'a':
            git_utils.commit_changes(message)
            typer.echo("Commit successful!")
            break
        elif choice.lower() == 'r':
            current_context = typer.prompt("Enter additional context")
            continue # Re-runs the loop with new context
        elif choice.lower() == 'e':
            edited_message = typer.edit(message)

            if edited_message is None:
                typer.echo("Could not open editor. Falling back to inline edit.")
                message = typer.prompt("Type your message manually")

            if edited_message is not None:
                message = edited_message.strip()
                typer.secho("\n--- Updated Message ---", fg=typer.colors.GREEN)
                typer.echo(message)

                if typer.confirm("Accept this edited message?"):
                    git_utils.commit_changes(message)
                    typer.echo("Commit successful!")
                    break
            else:
                typer.echo("No changes made to the message.")
        else:
            typer.echo("Commit cancelled.")
            break


    if push:
        typer.echo("Pushing changes...")
        git_utils.push_changes()
        typer.echo("Push complete.")

    typer.echo("Done.")

@app.command()
def version():
    """
    Show CommitGen version.
    """
    typer.echo("CommitGen version: 0.1.0")
