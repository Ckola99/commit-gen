import typer
import commitgen.git_utils as git_utils
from commitgen import ai
from commitgen.config import CONFIG_DIR, CONFIG_FILE

app = typer.Typer(help="CommitGen – AI-powered Conventional Commit generator")


@app.command()
def commit(push: bool = typer.Option(False, "--push", "-p", help="Push the commit after committing")):
    """
    Generate a Conventional Commit message from staged changes.
    """
    # STEP 1: Verify we are inside a Git repository
    if not git_utils.verify_repo():
        typer.echo("Error: You are not inside a Git repository.")
        raise typer.Exit(code=1)


    # STEP 2: Check for staged files
    if not git_utils.has_staged_changes():
        typer.echo("No staged changes. Would you like to stage all changes? [y/N]")
        # This is where the CLI handles user interaction
        if typer.confirm("Stage all?"):
            git_utils.stage_all_changes()
        else:
            typer.echo("Aborting commit process. Stage some changes and try again.")
            raise typer.Exit(code=1)

    # STEP 3: Extract staged diff
    current_context = ""
    while True:
        diff_text = git_utils.get_staged_diff()

        if not diff_text or not diff_text.strip():
            typer.echo("Error: Unable to retrieve staged changes, or no changes detected.")
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
                message = typer.prompt("Type your message manually").strip()
            else:
                message = edited_message.strip()


            if message:
                typer.secho("\n--- Updated Message ---", fg=typer.colors.GREEN)
                typer.echo(message)
                typer.echo("-----------------------\n")

                if typer.confirm("Accept this edited message?"):
                    git_utils.commit_changes(message)
                    typer.echo("Commit successful!")
                    break
            else:
                typer.echo("Commit message cannot be empty. Please try again.")
        elif choice.lower() == 'q':
            typer.echo("Commit aborted.")
            raise typer.Exit() # This stops the whole script immediately


    if push:
        typer.echo("Pushing changes...")
        git_utils.push_changes()
        typer.echo("Push complete.")


@app.command()
def version():
    """
    Show CommitGen version.
    """
    typer.echo("CommitGen version: 0.1.0")


@app.command()
def config():
    """
    Configure commitgen settings (API keys, preferences, etc.)
    """

    api_key = typer.prompt("Enter your OpenAI API Key", hide_input=True)

    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    CONFIG_FILE.write_text(f"OPENAI_API_KEY={api_key}\n")

    typer.echo(f"API key saved successfully.")
