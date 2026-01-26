# Changelog

## 0.1.6
### Added
- Docker support for running CommitGen without a local Python environment.
- --auto (-a) flag for automatically generating commit messages, committing, and pushing without user prompts.

## 0.1.5
### Fixed
- Fixed failure of the `r` (regenerate/refine) option caused by an invalid `diff_text` parameter being passed to `ai.refine_commit_message`.

### Changed
- Improved CLI prompt wording for better clarity.
- Enhanced CLI visual output using Rich for a more polished and readable user experience.

---

## 0.1.1
### Fixed
- Fixed failure of the `r` (refine) option caused by an invalid `diff_text` parameter being passed to `ai.refine_commit_message`.

### Changed
- Improved CLI prompt wording for better clarity and usability.

## 0.1.0
### Added
- Initial release.
- AI-powered commit message generation.
- Interactive CLI workflow.
