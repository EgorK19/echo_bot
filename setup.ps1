# setup.ps1 — Bootstrap script for a new machine
# Run from the project root: .\setup.ps1

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

Write-Host "`n=== 1. Creating virtual environment ===" -ForegroundColor Cyan
python -m venv .venv

Write-Host "`n=== 2. Installing dependencies ===" -ForegroundColor Cyan
.\.venv\Scripts\pip install --upgrade pip
if (Test-Path "requirements.txt") {
    .\.venv\Scripts\pip install -r requirements.txt
} elseif (Test-Path "pyproject.toml") {
    .\.venv\Scripts\pip install -e .
} else {
    Write-Host "No requirements.txt or pyproject.toml found — skipping." -ForegroundColor Yellow
}

Write-Host "`n=== 3. Installing VS Code extensions ===" -ForegroundColor Cyan
$extensions = @(
    "ms-python.python",
    "ms-python.vscode-pylance",
    "ms-python.debugpy",
    "ms-python.vscode-python-envs",
    "donjayamanne.python-environment-manager",
    "donjayamanne.python-extension-pack",
    "kevinrose.vsc-python-indent",
    "njpwerner.autodocstring",
    "charliermarsh.ruff",
    "ms-toolsai.jupyter",
    "ms-toolsai.jupyter-keymap",
    "ms-toolsai.jupyter-renderers",
    "ms-toolsai.vscode-jupyter-cell-tags",
    "ms-toolsai.vscode-jupyter-slideshow",
    "ms-toolsai.vscode-jupyter-powertoys",
    "google.colab",
    "akamud.vscode-theme-onedark",
    "pkief.material-icon-theme",
    "aaron-bond.better-comments",
    "github.copilot",
    "github.copilot-chat",
    "visualstudioexptteam.vscodeintellicode",
    "visualstudioexptteam.intellicode-api-usage-examples",
    "github.vscode-pull-request-github",
    "batisteo.vscode-django",
    "wholroyd.jinja",
    "redhat.vscode-yaml",
    "christian-kohler.path-intellisense",
    "mechatroner.rainbow-csv",
    "qwtel.sqlite-viewer",
    "bierner.emojisense"
)

foreach ($ext in $extensions) {
    Write-Host "  Installing $ext..."
    code --install-extension $ext --force
}

Write-Host "`n=== Done! Open the folder in VS Code and select .venv as interpreter. ===" -ForegroundColor Green
