# Contributing to Mahmut

Thank you for your interest in contributing to `Mahmut`! Contributions are welcome.
This project is open to improvements, bug fixes, and new ideas. If you have any suggestions,
please create an issue or submit a pull request.

## Getting Started

1. Fork the repository.

2. Clone your fork.

```bash
git clone https://github.com/Osman-Kahraman/mahmut.git
cd mahmut
```

3. Create a new branch for your change.

```bash
git checkout -b feature/YOUR-FEATURE-NAME
```

4. Install dependencies.

```bash
pip install -r requirements.txt
```

5. Make your changes and commit them.

```bash
git commit -m "Add: short description of your change"
```

6. Push the branch.

```bash
git push origin feature/your-feature-name
```

7. Open a Pull Request.

## Development Setup

Mahmut is a PyQt5 desktop app and currently supports Windows.

### 1. (Optional) Create and activate a virtual environment

```bash
python -m venv .venv
```

```bash
# Windows
.venv\Scripts\activate
```

```bash
# macOS/Linux
source .venv/bin/activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the app

```bash
python Mahmut.py
```

## Contribution Guidelines

Please follow these rules when contributing:
- Write clear, descriptive commit messages
- Keep pull requests focused on one change
- Follow the existing Python and PyQt5 style in the codebase
- Run the app and verify the affected flow before submitting a PR

Example commit messages:

```sh
Fix: correct word list parsing
Add: progress chart tooltip
Refactor: session state handling
```

## Feature Ideas

Some ideas that could improve the project:
- macOS/Linux support
- Import/export word lists
- Smarter spaced-repetition scheduling
- Search and filter for word sets
- More detailed progress analytics

---

Thank you for helping improve `Mahmut`.
