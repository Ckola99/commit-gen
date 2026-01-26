# CommitGen

**AI-powered Conventional Commit message generator for Git**

Stop writing bad commit messages. CommitGen uses AI to analyze your staged changes and generates clean, structured commits that follow the [Conventional Commits](https://www.conventionalcommits.org/) standard.

![PyPI Version](https://img.shields.io/pypi/v/commitgen-tool)
![Python Versions](https://img.shields.io/pypi/pyversions/commitgen-tool)
![License](https://img.shields.io/pypi/l/commitgen-tool)
![Docker Pulls](https://img.shields.io/docker/pulls/chriskola99/commitgen)

## Features

- Generate Conventional Commit messages from staged changes
- Interactive CLI with inline or editor-based editing
- Support for Git workflows of any size
- **Docker support** - run without Python installation
- **Auto-commit mode** - fully automated commits with push

```bash
# Before CommitGen
git commit -m "fix stuff"
git commit -m "final fix"
git commit -m "pls work"

# With CommitGen
[FIX]: resolve null pointer in authentication handler
[FEAT]: add user session management with Redis
[DOCS]: update API documentation with examples
```

---

## Installation

### Option 1: Python Package (Recommended for Local Use)

```bash
pip install commitgen-tool
```

**Requirements:**
- Python 3.10+
- Git installed and configured
- **OpenAI API key with available tokens** (currently required)

> ⚠️ **Important**: This version requires an OpenAI API key and uses paid API calls. Support for free local LLMs is planned for future releases.

### Option 2: Docker (No Python Required)

Perfect for CI/CD pipelines, isolated environments, or if you don't want to install Python dependencies.

#### Pull the Image

```bash
docker pull chriskola99/commitgen:latest
```

#### One-Time Configuration

```bash
docker run --rm -it \
  -v "$(pwd):/workspace" \
  -v "$HOME/.config/commitgen:/home/app/.config/commitgen" \
  chriskola99/commitgen config
```

This command:
- Mounts your current directory as `/workspace`
- Persists your API key in `~/.config/commitgen` (survives container restarts)
- Prompts you to enter your OpenAI API key

#### Run CommitGen with Docker

```bash
# Interactive mode
docker run --rm -it \
  -v "$(pwd):/workspace" \
  -v "$HOME/.config/commitgen:/home/app/.config/commitgen" \
  chriskola99/commitgen commit

# Auto-commit and push
docker run --rm -it \
  -v "$(pwd):/workspace" \
  -v "$HOME/.config/commitgen:/home/app/.config/commitgen" \
  chriskola99/commitgen commit --auto

# Commit and push manually
docker run --rm -it \
  -v "$(pwd):/workspace" \
  -v "$HOME/.config/commitgen:/home/app/.config/commitgen" \
  chriskola99/commitgen commit --push
```

#### Create a Shell Alias (Recommended)

**Linux/macOS:**

```bash
# Add to ~/.bashrc or ~/.zshrc
alias commitgen='docker run --rm -it -v "$(pwd):/workspace" -v "$HOME/.config/commitgen:/home/app/.config/commitgen" chriskola99/commitgen'

# Reload shell
source ~/.bashrc  # or source ~/.zshrc
```

**Windows PowerShell:**

```powershell
# Add to your PowerShell profile
function commitgen {
    docker run --rm -it `
      -v "${PWD}:/workspace" `
      -v "$env:USERPROFILE\.config\commitgen:/home/app/.config/commitgen" `
      chriskola99/commitgen $args
}
```

After setting up the alias, use CommitGen like a native command:

```bash
commitgen config        # Configure API key
commitgen commit        # Interactive commit
commitgen commit --auto # Auto-commit and push
commitgen --help        # Show help
```

---

## Getting an OpenAI API Key

1. Go to [OpenAI Platform](https://platform.openai.com/)
2. Sign up or log in
3. Navigate to API Keys section
4. Create a new API key
5. Add credits to your account (pay-as-you-go)

**Cost**: Approximately $0.001-0.01 per commit message (very affordable!)

You can set usage limits in your OpenAI dashboard to control costs.

---

## Basic Usage

### Generate a Commit

```bash
commitgen commit
```

You'll see a suggested message:

```
💡 Suggested Commit Message
┌──────────────────────────────────────────┐
│ [FEAT]: add user authentication endpoint │
└──────────────────────────────────────────┘

(a)ccept, (r)egenerate with context, (i)nline edit, (e)xtended editor, or (q)uit?
```

### Options When Reviewing

- `a` - Accept and commit immediately
- `r` - Add context to refine the message
- `i` - Edit the message in your terminal
- `e` - Open your preferred text editor
- `q` - Quit without committing

### Auto-Commit Mode (NEW!)

Skip all prompts and commit + push automatically:

```bash
# Stage changes and auto-commit with AI-generated message
commitgen commit --auto

# Short flag
commitgen commit -a
```

**Perfect for:**
- CI/CD pipelines
- Automated workflows
- Quick commits when you trust the AI

### Commit and Push

```bash
# Commit and push in one command
commitgen commit --push

# Or use the short flag
commitgen commit -p
```

### Other Commands

```bash
# Configure API key
commitgen config

# Show version
commitgen version

# Get help
commitgen --help
```

---

## How It Works

1. **Analyzes Your Changes**: Reads `git diff --staged` to see what you've modified
2. **AI Processing**: Sends the diff to OpenAI's GPT-5-nano model with instructions to generate a Conventional Commit
3. **Interactive Review**: Lets you accept, edit, or regenerate the message (unless using `--auto`)
4. **Safe Commit**: Only commits after you approve the message

> **Current Model**: CommitGen uses GPT-5-nano for fast, cost-effective commit generation. Model selection will be configurable in future releases.

### What Gets Sent to OpenAI?

Only your git diff is sent - not your entire codebase. The diff shows:
- Which files changed
- What lines were added/removed
- Function and variable names in the changes

**Privacy Note**: If you're working with sensitive code, review the diff before committing or consider waiting for local LLM support.

---

## Conventional Commit Types

CommitGen automatically categorizes your changes:

| Type | When to Use | Example |
|------|-------------|---------|
| `FEAT` | New features | `[FEAT]: add OAuth2 authentication` |
| `FIX` | Bug fixes | `[FIX]: resolve memory leak in cache` |
| `DOCS` | Documentation | `[DOCS]: add API endpoint examples` |
| `STYLE` | Code formatting | `[STYLE]: apply black formatter` |
| `REFACTOR` | Code restructuring | `[REFACTOR]: extract helper functions` |
| `PERF` | Performance improvements | `[PERF]: optimize database queries` |
| `TEST` | Adding tests | `[TEST]: add unit tests for auth` |
| `CHORE` | Maintenance | `[CHORE]: update dependencies` |
| `CI` | CI/CD changes | `[CI]: add GitHub Actions workflow` |

---

## Configuration

CommitGen stores your API key securely in:

- **Linux/macOS**: `~/.config/commitgen/config.env`
- **Windows**: `%USERPROFILE%\.config\commitgen\config.env`
- **Docker**: Mounted volume at `/home/app/.config/commitgen` (persists between runs)

The key is stored locally and never transmitted except to OpenAI's API.

⚠️ **Never commit this file to Git**

---

## Examples

### Example 1: Simple Feature

```bash
# You made changes to add a login endpoint
git add src/auth.py

commitgen commit
```

**Generated:**
```
[FEAT]: add user login endpoint with JWT tokens
```

---

### Example 2: Multiple Changes

```bash
# You updated API, tests, and docs
git add src/api.py tests/test_api.py README.md

commitgen commit
```

**Generated:**
```
[FEAT]: add user registration endpoint
[TEST]: add integration tests for registration
[DOCS]: update README with API examples
```

---

### Example 3: Bug Fix with Context

```bash
commitgen commit
```

When prompted, choose `(r)` to regenerate with context:

```
Add context: Fixes issue #123 where special characters broke login
```

**Generated:**
```
[FIX]: sanitize special characters in login handler

Fixes #123
```

---

### Example 4: Using Extended Editor

Choose `(e)` to open your editor:

```bash
# CommitGen opens your $GIT_EDITOR with:

# CommitGen – Extended Commit Message Editor
#
# Save the file before closing to apply changes.
# Lines starting with '#' will be ignored.
#

[FEAT]: add user authentication
```

Edit, save (`Ctrl+S`), and close. CommitGen will use your edited message.

---

### Example 5: Auto-Commit in CI/CD

```bash
# In your GitHub Actions, GitLab CI, or Jenkins pipeline
docker run --rm \
  -v "$(pwd):/workspace" \
  -e OPENAI_API_KEY=${{ secrets.OPENAI_API_KEY }} \
  chriskola99/commitgen commit --auto
```

**Benefits:**
- No manual intervention required
- Consistent commit messages across automated workflows
- Perfect for release automation

---

## Setting Your Preferred Editor

CommitGen respects the same editor settings as Git.

### VS Code (Recommended)

**Windows PowerShell:**
```powershell
setx GIT_EDITOR "code --wait"
```

**Linux/macOS:**
```bash
echo 'export GIT_EDITOR="code --wait"' >> ~/.bashrc
# or for zsh:
echo 'export GIT_EDITOR="code --wait"' >> ~/.zshrc
```

### Other Editors

**Vim:**
```bash
export GIT_EDITOR=vim
```

**Nano:**
```bash
export GIT_EDITOR=nano
```

**Sublime Text:**
```bash
export GIT_EDITOR="subl -w"
```

---

## Workflow Integration

### Typical Development Flow

```bash
# 1. Make your changes
vim src/feature.py

# 2. Stage what you want to commit
git add src/feature.py

# 3. Let CommitGen handle the message
commitgen commit

# 4. Push when ready
git push
```

### Quick Commit Flow with Auto Mode

```bash
# 1. Make your changes
vim src/feature.py

# 2. Stage changes
git add src/feature.py

# 3. Auto-commit and push in one command
commitgen commit --auto
```

### Working with Unstaged Changes

If you run `commitgen commit` without staging:

```
No staged changes detected.
(a) stage all, (s) select files, (q) quit?
```

- `a` - Stages everything (`git add .`)
- `s` - Lets you pick specific files
- `q` - Exits so you can stage manually

---

## Docker Usage Details

### Why Use Docker?

**Isolation**: No conflicts with your Python environment or other tools.

**Portability**: Run on any machine with Docker - Linux, macOS, Windows, or CI/CD servers.

**Consistency**: Same environment every time, no dependency issues.

**No Setup**: Skip Python installation and virtual environments.

### Understanding the Docker Command

```bash
docker run --rm -it \
  -v "$(pwd):/workspace" \
  -v "$HOME/.config/commitgen:/home/app/.config/commitgen" \
  chriskola99/commitgen commit
```

**Breaking it down:**
- `--rm`: Automatically remove container after it exits
- `-it`: Interactive terminal (allows you to respond to prompts)
- `-v "$(pwd):/workspace"`: Mount your current Git repository into the container
- `-v "$HOME/.config/commitgen:/home/app/.config/commitgen"`: Persist API key between runs
- `chriskola99/commitgen`: The Docker image
- `commit`: The command to run

### Using Environment Variables (Alternative to Mounted Config)

Instead of mounting the config directory, you can pass your API key directly:

```bash
docker run --rm -it \
  -v "$(pwd):/workspace" \
  -e OPENAI_API_KEY=your_api_key_here \
  chriskola99/commitgen commit --auto
```

**Best for:**
- CI/CD pipelines (use secrets management)
- Temporary environments
- When you can't or don't want to mount volumes

---

## Troubleshooting

### "OpenAI API key not found"

**Solution:**
```bash
commitgen config
# Enter your API key
```

Your key is stored in `~/.config/commitgen/config.env`

**Docker Solution:**
```bash
# Ensure the volume is mounted correctly
docker run --rm -it \
  -v "$HOME/.config/commitgen:/home/app/.config/commitgen" \
  chriskola99/commitgen config

# Or use environment variable
docker run --rm -it \
  -e OPENAI_API_KEY=your_key \
  chriskola99/commitgen commit --auto
```

---

### "You are not inside a Git repository"

**Solution:** Navigate to a Git repository or initialize one:
```bash
git init
```

**Docker Solution:** Ensure you're running the command from your Git repository root:
```bash
cd /path/to/your/git/repo
docker run --rm -it -v "$(pwd):/workspace" ...
```

---

### "No staged changes detected"

**Solution:** Stage your changes first:
```bash
git add <files>
# or
git add .
```

---

### Editor doesn't wait for save

If using VS Code, ensure you have the `--wait` flag:

```bash
# Check your setting
echo $GIT_EDITOR

# Should show: code --wait
# If not, set it:
export GIT_EDITOR="code --wait"
```

---

### Generic/unclear commit messages

**Solution:** Use the regenerate option with context:

1. Choose `(r)` when prompted
2. Provide specific details about what changed
3. CommitGen will regenerate with your context

Example:
```
Add context: Optimized query performance by adding database indexes
```

---

### Docker: Permission Denied on Git Operations

If you encounter permission issues when running Docker:

**Linux/macOS:**
```bash
# Run with your user ID
docker run --rm -it \
  --user $(id -u):$(id -g) \
  -v "$(pwd):/workspace" \
  -v "$HOME/.config/commitgen:/home/app/.config/commitgen" \
  chriskola99/commitgen commit
```

---

## Advanced Usage

### Customizing the Workflow

**Skip the push prompt:**
```bash
# Always push after commit
commitgen commit --push

# Fully automated commit + push
commitgen commit --auto

# Never get asked to push
# (just press 'n' when prompted)
```

**Working with branches:**
```bash
# CommitGen works with any branch
git checkout -b feature/new-feature
# ... make changes ...
commitgen commit
```

**Amending commits:**
```bash
# CommitGen doesn't amend, but you can after:
git commit --amend
```

### CI/CD Integration Examples

**GitHub Actions:**
```yaml
name: Auto Commit
on: [push]
jobs:
  commit:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Auto commit with CommitGen
        env:
          OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
        run: |
          docker run --rm \
            -v "$PWD:/workspace" \
            -e OPENAI_API_KEY \
            chriskola99/commitgen commit --auto
```

**GitLab CI:**
```yaml
commit:
  image: docker:latest
  services:
    - docker:dind
  script:
    - docker run --rm
      -v "$PWD:/workspace"
      -e OPENAI_API_KEY=$OPENAI_API_KEY
      chriskola99/commitgen commit --auto
```

---

## Comparison with Alternatives

### vs Manual Writing

| Manual | CommitGen |
|--------|-----------|
| ❌ Inconsistent format | ✅ Always follows Conventional Commits |
| ❌ Vague messages | ✅ Specific, contextual descriptions |
| ❌ Prone to typos | ✅ Properly formatted |
| ❌ Time-consuming | ✅ Instant generation |

### vs GitHub Copilot

| Copilot | CommitGen |
|---------|-----------|
| Only suggests based on file names | Analyzes actual diff content |
| Generic suggestions | Context-aware with GPT-5-nano |
| No editing workflow | Interactive review and editing |
| No multiple change handling | Handles FEAT + FIX + DOCS in one commit |
| Fixed model | Model selection coming soon |
| No Docker support | Full Docker integration |
| No automation | Auto-commit mode available |

---

## Security & Privacy

### What CommitGen Sends to OpenAI

- ✅ Git diff (added/removed lines)
- ✅ File paths
- ❌ Your full source code
- ❌ Git history
- ❌ Credentials or secrets

### API Key Storage

- Stored locally in `~/.config/commitgen/`
- Never transmitted except to OpenAI
- Never logged or committed
- With Docker: isolated in mounted volume

### Best Practices

1. **Review diffs before committing** - Ensure no secrets are staged
2. **Use `.gitignore`** - Keep sensitive files out of commits
3. **Set OpenAI usage limits** - Control API costs in your OpenAI dashboard
4. **Use environment variables for secrets** - Never hardcode credentials
5. **In CI/CD**: Use secrets management (GitHub Secrets, GitLab Variables, etc.)

---

## Limitations & Future Plans

### Current Limitations

- ⚠️ **Requires OpenAI API key** (paid service)
- ⚠️ **Requires internet connection** to generate messages
- ⚠️ **Fixed AI model** (GPT-5-nano) - no model selection yet
- ⚠️ **No support for commit templates** yet
- ⚠️ **English-only** commit messages (for now)

### Planned Features

- 🔄 **Local LLM support** - Use Ollama, LM Studio, or local models (offline commits!)
- 🎛️ **Model selection** - Choose your preferred OpenAI model (GPT-4, GPT-3.5, etc.)
- 🎨 **Custom templates** - Define your own commit format
- 🌍 **Multi-language** - Commits in your preferred language
- 🔗 **Git hooks integration** - Auto-suggest on `git commit`
- 📊 **Commit history** - Learn from your commit patterns
- 🎯 **Team presets** - Share commit style across teams

---

## Project Roadmap

### Version 0.1.0 ✅
- Basic commit generation with GPT-5-nano
- Interactive workflow (accept/regenerate/edit)
- OpenAI integration
- Configuration management
- Comprehensive test suite
- CI/CD pipeline

### Version 0.1.5 (Current) ✅
- **Docker support with automated builds**
- **Auto-commit mode** (`--auto` flag)
- Enhanced CI/CD integration
- Improved error handling

### Version 0.2.0 (Planned)
- [ ] Local LLM support (Ollama, LM Studio)
- [ ] Configurable AI model selection
- [ ] Custom commit templates
- [ ] Commit message history/learning

### Version 0.3.0 (Future)
- [ ] Multi-language commit messages
- [ ] Git hooks integration
- [ ] VS Code extension
- [ ] Team presets and shared configurations

---

## Contributing

Contributions are welcome! Here's how:

1. **Fork the repository**
2. **Create a feature branch**
   ```bash
   git checkout -b feature/amazing-feature
   ```
3. **Make your changes**
4. **Write or update tests**
5. **Commit using CommitGen!**
   ```bash
   commitgen commit
   ```
6. **Push and open a PR**
   ```bash
   git push origin feature/amazing-feature
   ```

### Development Setup

```bash
# Clone the repo
git clone https://github.com/<your-username>/commitgen.git
cd commitgen

# Install in editable mode
pip install -e .

# Run tests
python -m unittest discover -s tests

# Build Docker image locally
docker build -t commitgen:local .
```

---

## FAQ

### Why does CommitGen need an API key?

Currently, CommitGen uses OpenAI's GPT-5-nano model to understand your code changes. This model is hosted by OpenAI and requires authentication.

**Future versions will support:**
- Free local LLMs (Ollama, LM Studio)
- Model selection (GPT-4, GPT-3.5-turbo, etc.)

---

### How much does it cost?

With GPT-5-nano, approximately **$0.001 to $0.01 per commit** depending on diff size. For most developers:
- 100 commits/month = ~$0.10 - $1.00
- Set usage limits in your OpenAI dashboard to control costs

GPT-5-nano is optimized for speed and cost-effectiveness.

---

### Can I use other AI providers?

Not yet, but it's planned! Future versions will support:
- Anthropic Claude
- Google Gemini
- Local models (Ollama, LM Studio)
- Azure OpenAI

---

### Is my code sent to OpenAI?

Only the **git diff** is sent - showing what changed in your staged files. Your full codebase, git history, and credentials are never transmitted.

---

### What if I don't have internet?

CommitGen requires an internet connection to contact OpenAI's API. Local LLM support (which works offline) is planned for v0.2.0.

---

### Can I customize the commit format?

Not yet, but custom templates are planned for v0.3.0. Currently, CommitGen follows standard Conventional Commits format.

---

### Does CommitGen work with GitLab/Bitbucket?

Yes! CommitGen works with any Git repository, regardless of where it's hosted (GitHub, GitLab, Bitbucket, self-hosted, etc.).

---

### Should I use Docker or pip?

**Use pip if:**
- You're comfortable with Python
- You want the fastest execution
- You work on a single development machine

**Use Docker if:**
- You want complete isolation
- You're setting up CI/CD pipelines
- You work across multiple machines
- You don't want to manage Python dependencies

Both methods work identically and share the same features!

---

## Support

### Found a bug?
Open an issue: [GitHub Issues](https://github.com/ckola99/commitgen/issues)

### Have a question?
Start a discussion: [GitHub Discussions](https://github.com/ckola99/commitgen/discussions)

### Want to contribute?
See our [Contributing](#contributing) section above!

---

## Acknowledgments

Built with:
- [OpenAI API](https://openai.com/) - AI-powered analysis
- [Typer](https://typer.tiangolo.com/) - CLI framework
- [Rich](https://rich.readthedocs.io/) - Terminal formatting
- [Conventional Commits](https://www.conventionalcommits.org/) - Commit standard
- [Docker](https://www.docker.com/) - Containerization

---

## License

MIT License © [Christopher Kola]

See [LICENSE](LICENSE) for full details.

---

## Links

- **PyPI**: [commitgen-tool](https://pypi.org/project/commitgen-tool/)
- **Docker Hub**: [chriskola99/commitgen](https://hub.docker.com/r/chriskola99/commitgen)
- **GitHub**: [github.com/<your-username>/commitgen](https://github.com/ckola99/commitgen)
- **Documentation**: [Coming soon]
- **Changelog**: [CHANGELOG.md](CHANGELOG.md)

---

**⭐ If CommitGen helps you write better commits, please star the repository!**

---

**Made with ❤️ by a developer who cares about commit quality**
