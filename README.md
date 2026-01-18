# CommitGen

**AI-powered Conventional Commit message generator CLI**

CommitGen is a command-line tool that generates clean, structured commit messages using AI. It helps you write commits that follow the [Conventional Commits](https://www.conventionalcommits.org/) standard (`FEAT`, `FIX`, `CHORE`, `DOCS`, etc.) directly from your terminal, without needing to think about formatting or context.

---

## Why CommitGen?

We've all written bad commit messages at some point:

```
fix stuff
final fix
pls work
```

Bad commits slow down code reviews, debugging, and collaboration. CommitGen solves this by:

- ✅ Automatically analyzing your staged changes
- ✅ Categorizing them as `FEAT`, `FIX`, `CHORE`, `DOCS`, etc.
- ✅ Generating structured, readable commit messages
- ✅ Summarizing multiple changes in a single commit

---

## Before vs After

### Before (manual / Copilot):

```
fix stuff
final fix
pls work
```

### After CommitGen:

```
[FIX]: guard against None staged diff in CLI
[FIX]: improve get_staged_diff: use pipes, utf-8 encoding, and replace errors
[DOCS]: fix typo in get_staged_diff docstring
```

### Multiple changes example:

```
[FEAT]: add diff parsing utility
[FIX]: handle edge case in CLI for empty staged diff
[DOCS]: update README with usage instructions
```

---

## Features

- 🤖 Generate Conventional Commit messages from staged changes
- 📋 Categorizes changes into `FEAT`, `FIX`, `CHORE`, `DOCS`, and more
- 📦 Supports multiple staged changes and summarizes them automatically
- 💻 Works entirely from the terminal (no IDE required)
- 🔐 Configurable API key storage for OpenAI or other AI models

---

## Installation

```bash
# Clone the repository
git clone https://github.com/<your-username>/commitgen.git
cd commitgen

# Install in editable mode for development
pip install -e .
```

After installation, the `commitgen` command will be available globally.

---

## Usage

```bash
# Generate a commit message from staged changes
commitgen commit

# Generate and push immediately
commitgen commit --push

# Configure your OpenAI API key
commitgen config

# Show version
commitgen version

# See help
commitgen --help
```

---

## Configuration

CommitGen stores your API key in a user-specific config file:

- **Linux/macOS**: `~/.config/commitgen/config.toml`
- **Windows**: `%APPDATA%\commitgen\config.toml`

You can set your API key with:

```bash
commitgen config
```

⚠️ **Never commit your API key to Git.** CommitGen handles this securely.

---

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-feature`)
3. Make changes and write tests
4. Commit your changes with good messages (CommitGen can help!)
5. Push and open a Pull Request

---

## License

MIT License © [Your Name]

---

## Acknowledgments

Built with:
- [OpenAI API](https://openai.com/) for AI-powered message generation
- [Typer](https://typer.tiangolo.com/) for CLI framework
- Conventional Commits standard

---

## Support

If you encounter issues or have suggestions:
- Open an issue on [GitHub Issues](https://github.com/<your-username>/commitgen/issues)
- Contribute improvements via Pull Requests

---

**⭐ If you find CommitGen useful, please star the repository!**
