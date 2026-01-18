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
- ✏️ Multiple editing modes: accept, regenerate, inline edit, or extended editor
- 💻 Works entirely from the terminal (no IDE required)
- 🔐 Configurable API key storage for OpenAI
- 🚀 Optional automatic push after commit

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

### Requirements

- Python 3.10+
- Git installed and configured
- OpenAI API key

---

## Quick Start

```bash
# 1. Configure your OpenAI API key (first time only)
commitgen config

# 2. Stage your changes
git add .

# 3. Generate and commit
commitgen commit
```

---

## Usage

### Basic Commands

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

### Interactive Workflow

When you run `commitgen commit`, you'll be presented with a suggested commit message and options:

```
💡 Suggested Commit Message
┌──────────────────────────────────────────────┐
│ [FEAT]: add user authentication endpoint     │
│ [FIX]: resolve null pointer in login handler│
└──────────────────────────────────────────────┘

(a)ccept, (r)egenerate with context, (i)nline edit, (e)xtended inline edit in custom editor, or (q)uit?
```

**Options:**
- `(a)` - Accept the message and commit
- `(r)` - Provide additional context to refine the message
- `(i)` - Edit the message directly in the terminal
- `(e)` - Open your preferred text editor for detailed editing
- `(q)` - Quit without committing

### Handling Unstaged Changes

If you haven't staged changes yet, CommitGen will prompt you:

```
No staged changes detected.
(a) stage all, (s) select files, (q) quit
```

- `(a)` - Stage all modified files (`git add .`)
- `(s)` - Select specific files to stage
- `(q)` - Exit

---

## ✏️ Editing Commit Messages (Editor Instructions)

When using CommitGen, you can edit the generated commit message in multiple ways:

1. **Inline edit** – edit directly in the terminal
2. **Extended editor mode** – open your preferred text editor (recommended for longer messages)

When prompted, choose:

```
(e) extended inline edit in custom editor
```

CommitGen will open your default system editor with instructions at the top of the file.

### ⚠️ Important:

**You must save the file before closing the editor**, otherwise your changes will be discarded.

This behavior is identical to how `git commit` works.

### What you'll see in the editor

At the top of the file, CommitGen inserts instructions like:

```
# CommitGen – Extended Commit Message Editor
#
# Save the file before closing to apply changes.
# VS Code: Ctrl+S (Windows/Linux) or Cmd+S (macOS)
# Vim: :wq
# Nano: Ctrl+O, Enter, then Ctrl+X
#
# Lines starting with '#' will be ignored.
#

[FEAT]: add diff parsing utility
```

- Lines starting with `#` are ignored
- Only the actual commit message is used
- Closing without saving keeps the previous message

---

## Setting Your Preferred Editor

CommitGen uses the same editor resolution order as Git:

1. `$GIT_EDITOR`
2. `$VISUAL`
3. `$EDITOR`

You only need to set one of these.

### ✅ Windows (PowerShell)

**Set VS Code as editor (recommended):**

```powershell
setx GIT_EDITOR "code --wait"
```

Restart your terminal after running this.

**Explanation:**
- `--wait` ensures CommitGen waits until you close the editor
- Without it, the commit will continue immediately

### ✅ Windows (Git Bash)

```bash
export GIT_EDITOR="code --wait"
```

To make it permanent, add it to `~/.bashrc` or `~/.bash_profile`:

```bash
echo 'export GIT_EDITOR="code --wait"' >> ~/.bashrc
```

### ✅ Linux / macOS (Bash or Zsh)

**VS Code:**
```bash
export GIT_EDITOR="code --wait"
```

**Vim (default on many systems):**
```bash
export GIT_EDITOR=vim
```

**Nano (beginner-friendly):**
```bash
export GIT_EDITOR=nano
```

To persist the setting, add it to:
- `~/.bashrc` (Bash)
- `~/.zshrc` (Zsh)

Example:
```bash
echo 'export GIT_EDITOR="code --wait"' >> ~/.zshrc
```

### Editor Shortcuts (Quick Reference)

| Editor | Save & Close |
|--------|--------------|
| VS Code | `Ctrl+S` → close tab |
| Vim | `:wq` + Enter |
| Nano | `Ctrl+O` → Enter → `Ctrl+X` |
| Sublime | `Ctrl+S` → close tab |

### Common Pitfall (and how CommitGen handles it)

If you:
1. Open the editor
2. Close it without saving

CommitGen will safely detect this and show:

```
Editor closed without saving. Keeping previous message.
```

**No crash, no bad commit.**

### Why CommitGen Works This Way

This behavior is intentional and mirrors Git:
- ✅ Prevents accidental commits
- ✅ Gives you full control over the final message
- ✅ Works with any editor
- ✅ Keeps CommitGen editor-agnostic and reliable

---

## Configuration

CommitGen stores your API key in a user-specific config file:

- **Linux/macOS**: `~/.config/commitgen/config.env`
- **Windows**: `%USERPROFILE%\.config\commitgen\config.env`

You can set your API key with:

```bash
commitgen config
```

When prompted, enter your OpenAI API key. The key is stored locally and never transmitted except to OpenAI's API.

⚠️ **Never commit your API key to Git.** CommitGen handles this securely by storing it in your user config directory.

---

## How It Works

### 1. **Analyze Changes**
CommitGen reads your staged git diff using `git diff --staged`

### 2. **AI Processing**
The diff is sent to OpenAI's API with a carefully crafted prompt that:
- Analyzes the changes
- Categorizes them by type (FEAT, FIX, DOCS, etc.)
- Generates concise, present-tense commit messages
- Follows Conventional Commits standards

### 3. **Interactive Review**
You can:
- Accept the message as-is
- Regenerate with additional context
- Edit inline or in your preferred editor
- Abort if needed

### 4. **Commit & Push**
Once approved, CommitGen executes `git commit -m "message"` and optionally pushes to remote.

---

## Conventional Commit Types

CommitGen recognizes and uses these standard prefixes:

| Type | Description | Example |
|------|-------------|---------|
| `FEAT` | New feature | `[FEAT]: add user authentication` |
| `FIX` | Bug fix | `[FIX]: resolve null pointer exception` |
| `DOCS` | Documentation | `[DOCS]: update API documentation` |
| `STYLE` | Code style changes | `[STYLE]: format code with black` |
| `REFACTOR` | Code refactoring | `[REFACTOR]: simplify auth logic` |
| `PERF` | Performance improvement | `[PERF]: optimize database queries` |
| `TEST` | Adding/updating tests | `[TEST]: add unit tests for auth` |
| `CI` | CI/CD changes | `[CI]: update GitHub Actions workflow` |
| `CHORE` | Maintenance tasks | `[CHORE]: update dependencies` |

---

## Examples

### Example 1: Simple Feature

```bash
# Stage changes
git add src/auth.py

# Generate commit
commitgen commit
```

**Output:**
```
[FEAT]: add user authentication endpoint
```

### Example 2: Multiple Changes

```bash
# Stage changes
git add src/api.py tests/test_api.py README.md

# Generate commit
commitgen commit
```

**Output:**
```
[FEAT]: add user registration endpoint
[TEST]: add tests for registration flow
[DOCS]: update README with API examples
```

### Example 3: Bug Fix with Context

```bash
commitgen commit
```

**After generation:**
```
(r) regenerate with context
> "Fixes issue #123 where users couldn't login"
```

**Result:**
```
[FIX]: resolve login failure for users with special characters in username

Fixes #123
```

---

## Troubleshooting

### "You are not inside a Git repository"

**Solution:** Navigate to a Git repository or initialize one:
```bash
git init
```

### "OpenAI API key not found"

**Solution:** Configure your API key:
```bash
commitgen config
```

### "No staged changes detected"

**Solution:** Stage your changes first:
```bash
git add <files>
# or
git add .
```

### Editor opens but changes aren't saved

**Solution:** Make sure you:
1. Save the file (`Ctrl+S` in VS Code, `:wq` in Vim)
2. Close the editor after saving
3. Check that `--wait` flag is set for VS Code users

### CommitGen generates generic messages

**Solution:** Use the regenerate option `(r)` and provide specific context about what the changes accomplish.

---

## Project Structure

```
commitgen/
├── commitgen/
│   ├── __init__.py
│   ├── cli.py           # Main CLI interface with Typer
│   ├── ai.py            # OpenAI API integration
│   ├── git_utils.py     # Git operations
│   └── config.py        # Configuration management
├── pyproject.toml       # Project metadata and dependencies
├── README.md
└── LICENSE
```

---

## Contributing

We welcome contributions! Here's how to get started:

1. **Fork the repository**
2. **Create a feature branch**
   ```bash
   git checkout -b feature/amazing-feature
   ```
3. **Make your changes**
4. **Test thoroughly**
5. **Commit with CommitGen** (dogfooding!)
   ```bash
   commitgen commit
   ```
6. **Push to your fork**
   ```bash
   git push origin feature/amazing-feature
   ```
7. **Open a Pull Request**

### Development Setup

```bash
# Clone your fork
git clone https://github.com/<your-username>/commitgen.git
cd commitgen

# Install in editable mode with dev dependencies
pip install -e .

# Run the CLI
commitgen --help
```

---

## Roadmap

Coming soon:

- [ ] Docker support for containerized usage
- [ ] CI/CD pipeline with GitHub Actions
- [ ] Automated testing suite
- [ ] Support for custom commit message templates
- [ ] Support for other AI providers (Anthropic, Gemini)
- [ ] Commit history analysis and suggestions
- [ ] Integration with Git hooks
- [ ] VS Code extension

---

## License

MIT License © [Christopher Kola]

See [LICENSE](LICENSE) for details.

---

## Acknowledgments

Built with:
- [OpenAI API](https://openai.com/) for AI-powered message generation
- [Typer](https://typer.tiangolo.com/) for the beautiful CLI framework
- [Rich](https://rich.readthedocs.io/) for terminal formatting
- [Conventional Commits](https://www.conventionalcommits.org/) standard

---

## Support

If you encounter issues or have suggestions:
- 🐛 [Open an issue](https://github.com/<your-username>/commitgen/issues)
- 💬 [Start a discussion](https://github.com/<your-username>/commitgen/discussions)
- 🔧 Contribute improvements via Pull Requests

---

## FAQ

### Why use CommitGen instead of GitHub Copilot?

CommitGen is purpose-built for commit messages and:
- Analyzes actual diff content, not just file names
- Follows Conventional Commits strictly
- Handles multiple change types in one commit
- Gives you full editing control before committing

### Does CommitGen work offline?

No, CommitGen requires an internet connection to communicate with OpenAI's API.

### How much does it cost?

CommitGen itself is free and open-source. You only pay for OpenAI API usage, which is typically:
- ~$0.001-0.01 per commit message (very cheap!)
- You can set usage limits in your OpenAI account

### Can I use a different AI provider?

Not yet, but it's on the roadmap! We plan to support Anthropic Claude, Google Gemini, and other providers.

### Is my code sent to OpenAI?

Only the git diff is sent to generate the commit message. Your full codebase is never transmitted.

---

**⭐ If you find CommitGen useful, please star the repository!**

---

**Made with ❤️ by developers who care about commit quality**
