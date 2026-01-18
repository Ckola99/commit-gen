import typer
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
import commitgen.git_utils as git_utils
from commitgen import ai
from commitgen.config import CONFIG_DIR, CONFIG_FILE

app = typer.Typer(help="CommitGen – AI-powered Conventional Commit generator")
console = Console()


def display_change_summary(changes: list[tuple[str, str]]):
    """
    Display a table summarizing multiple changes (FEAT/FIX/DOCS/CHORE/TEST/etc.).
    Each row is a tuple: (change_type, description)
    """
    if not changes:
        return

    table = Table(title="📝 Summary of Changes", show_lines=True)
    table.add_column("Type", style="bold cyan")
    table.add_column("Description", style="white")

    for change_type, description in changes:
        table.add_row(change_type, description)

    console.print(table)


@app.command()
def commit(push: bool = typer.Option(False, "--push", "-p", help="Push the commit after committing")):
    """
    Generate a Conventional Commit message from staged changes.
    """

    current_context = ""
    message = None           # cached AI output
    diff_text = None

    if not git_utils.verify_repo():
        console.print(Panel("[bold red]You are not inside a Git repository[/bold red]", title="Error", border_style="red"))
        raise typer.Exit(code=1)


    if not git_utils.has_staged_changes():
        console.print(Panel("[yellow]No staged changes detected.[/yellow]", title="Info", border_style="yellow"))

        choice = typer.prompt(
            "(a) stage all, (s) select files, (q) quit"
        ).lower()

        if choice == 'a':
            git_utils.stage_all_changes()
        elif choice == 's':
            files = git_utils.get_modified_files()

            if not files:
                console.print("[red]No files to stage[/red]")
                raise typer.Exit(code=1)

            for i, f in enumerate(files, 1):
                console.print(f"[{i}] {f}")

            selection = typer.prompt(
                "Select files (comma-separated numbers)"
            )

            try:
                indexes = [int(i.strip()) for i in selection.split(",")]
                for i in indexes:
                    git_utils.stage_file(files[i - 1])

                console.print(
                    Panel(
                        "[green]Selected files staged successfully[/green]",
                        title="Success",
                        border_style="green",
                    )
                )
            except ValueError:
                console.print("[red]Invalid selection[/red]")
                raise typer.Exit(code=1)

        else:
            raise typer.Exit(code=1)

    while True:
        if diff_text is None:
            diff_text = git_utils.get_staged_diff()

            if not diff_text.strip():
                console.print(
                    Panel(
                        "[bold red]Unable to retrieve staged changes[/bold red]",
                        title="Error",
                        border_style="red",
                    )
                )
                raise typer.Exit(code=1)

        if message is None:
            message = ai.generate_commit_message(diff_text, current_context)

        # Optional: extract multiple change types from AI message
        # Simple heuristic: lines starting with '[TYPE]'
        changes = []
        for line in message.splitlines():
            if line.startswith('[') and ']' in line:
                type_part = line[1:line.index(']')]
                desc_part = line[line.index(']') + 2:]  # skip "] "
                changes.append((type_part, desc_part))

        # --- Suggested Commit Message ---
        console.print(Panel(message, title="💡 Suggested Commit Message", border_style="cyan"))

        # --- Show table if multiple changes ---
        if len(changes) > 1:
            display_change_summary(changes)

        choice = typer.prompt("(a)ccept, (r)egenerate with context, (i)nline edit, (e)xtended inline edit in custom editor, or (q)uit?")

        if choice.lower() == 'a':
            git_utils.commit_changes(message)
            console.print(Panel("[green]✅ Commit successful![/green]", title="Success", border_style="green"))
            break

        elif choice.lower() == 'r':
            extra_context = typer.prompt("Add context to refine this message").strip()

            if not extra_context:
                continue

            message = ai.refine_commit_message(diff_text, message, extra_context)

        elif choice.lower() == 'i':
            edited = typer.prompt(
                "Edited commit message",
                default=message,
                show_default=True
            ).strip()

            if not edited:
                console.print(
                    Panel(
                        "[red]Commit message cannot be empty.[/red]",
                        title="Error",
                        border_style="red",
                    )
                )
                continue
            message = edited

        elif choice.lower() == 'e':
            edited_message = typer.prompt(
                "Edit commit message",
                default=message,
                show_default=True,
            )

            message = edited_message.strip()

            if message:
                console.print(Panel(message, title="✏️ Edited Message", border_style="green"))
                if typer.confirm("Accept this edited message?"):
                    git_utils.commit_changes(message)
                    console.print(Panel("[green]✅ Commit successful![/green]", title="Success", border_style="green"))
                    break
            else:
                console.print(Panel("[red]Commit message cannot be empty. Please try again[/red]", title="Error", border_style="red"))

        elif choice.lower() == 'q':
            console.print(Panel("[yellow]Commit aborted by user[/yellow]", title="Aborted", border_style="yellow"))
            raise typer.Exit(code=1)

    if push:
        console.print(Panel("[cyan]Pushing changes...[/cyan]", title="Info", border_style="cyan"))
        git_utils.push_changes()
        console.print(Panel("[green]✅ Push complete![/green]", title="Success", border_style="green"))


@app.command()
def version():
    """Show CommitGen version."""
    console.print(Panel("CommitGen version: 0.1.0", title="Version", border_style="cyan"))


@app.command()
def config():
    """Configure commitgen settings (API keys, preferences, etc.)"""
    api_key = typer.prompt("Enter your OpenAI API Key", hide_input=True)

    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    CONFIG_FILE.write_text(f"OPENAI_API_KEY={api_key}\n")

    console.print(Panel("[green]API key saved successfully![/green]", title="Success", border_style="green"))
