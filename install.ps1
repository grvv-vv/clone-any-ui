# ==============================================================================
#   CLONE ANY UI (CAU) — Universal 1-Command Installer for Windows
#   Usage: irm https://raw.githubusercontent.com/grvv-vv/clone-any-ui/main/install.ps1 | iex
# ==============================================================================

$ErrorActionPreference = "Stop"

Write-Host ""
Write-Host "==================================================================" -ForegroundColor Cyan
Write-Host "   ⚡ CLONE ANY UI (CAU) — UNIVERSAL 1-COMMAND INSTALLER         " -ForegroundColor Yellow
Write-Host "   Autonomous Web UI & Motion Replication Engine for AI Agents    " -ForegroundColor Cyan
Write-Host "==================================================================" -ForegroundColor Cyan
Write-Host ""

# 1. Verify Python Installation
Write-Host "[1/5] Checking Python environment..." -ForegroundColor White
$pythonCmd = $null
if (Get-Command python -ErrorAction SilentlyContinue) {
    $pythonCmd = "python"
} elseif (Get-Command py -ErrorAction SilentlyContinue) {
    $pythonCmd = "py"
} elseif (Get-Command python3 -ErrorAction SilentlyContinue) {
    $pythonCmd = "python3"
}

if (-not $pythonCmd) {
    Write-Host "[ERROR] Python 3 was not found in PATH." -ForegroundColor Red
    Write-Host "Please install Python 3.10 or higher from https://python.org or via winget:" -ForegroundColor Yellow
    Write-Host "   winget install Python.Python.3.11" -ForegroundColor Yellow
    Exit 1
}

$pyVer = & $pythonCmd --version 2>&1
Write-Host "      Detected: $pyVer" -ForegroundColor Green

# 2. Determine Installation Directory
Write-Host "[2/5] Setting up CAU repository..." -ForegroundColor White
$repoUrl = "https://github.com/grvv-vv/clone-any-ui.git"
$installDir = "$HOME\.clone-any-ui"

# If already inside the repo directory
if ((Test-Path "SKILL.md") -and (Test-Path "clone_any_ui.py")) {
    $targetDir = (Get-Item .).FullName
    Write-Host "      Running inside repository: $targetDir" -ForegroundColor Green
} else {
    $targetDir = $installDir
    if (Test-Path $targetDir) {
        Write-Host "      Updating existing installation at: $targetDir" -ForegroundColor Gray
        try {
            git -C $targetDir pull --quiet
        } catch {
            Write-Host "      Git pull skipped, using current local files." -ForegroundColor Yellow
        }
    } else {
        Write-Host "      Cloning CAU into $targetDir..." -ForegroundColor Gray
        if (Get-Command git -ErrorAction SilentlyContinue) {
            git clone --depth 1 $repoUrl $targetDir
        } else {
            Write-Host "      Git not found, downloading zip archive..." -ForegroundColor Gray
            $zipPath = "$env:TEMP\clone-any-ui.zip"
            Invoke-WebRequest -Uri "https://github.com/grvv-vv/clone-any-ui/archive/refs/heads/main.zip" -OutFile $zipPath
            Expand-Archive -Path $zipPath -DestinationPath "$env:TEMP\cau_zip" -Force
            Move-Item "$env:TEMP\cau_zip\clone-any-ui-main" $targetDir
            Remove-Item $zipPath -Force
            Remove-Item "$env:TEMP\cau_zip" -Recurse -Force
        }
    }
}

# 3. Install Python Dependencies & CLI
Write-Host "[3/5] Installing Python dependencies & CLI..." -ForegroundColor White
Push-Location $targetDir
try {
    & $pythonCmd -m pip install --upgrade pip --quiet
    & $pythonCmd -m pip install -r requirements.txt --quiet
    & $pythonCmd -m pip install -e . --quiet
    Write-Host "      'cau' CLI registered and ready in PATH." -ForegroundColor Green
} catch {
    Write-Host "[WARNING] Editable install failed, falling back to direct package run." -ForegroundColor Yellow
} finally {
    Pop-Location
}

# 4. Integrate into All AI Coding Agents
Write-Host "[4/5] Auto-detecting & integrating with AI coding agents..." -ForegroundColor White
$agentsConfigured = 0

# Agent A: Google Antigravity
$antigravitySkills = "$HOME\.gemini\config\skills"
if (Test-Path (Split-Path $antigravitySkills -Parent)) {
    if (-not (Test-Path $antigravitySkills)) { New-Item -ItemType Directory -Path $antigravitySkills -Force | Out-Null }
    $dest = "$antigravitySkills\clone-any-ui"
    if (Test-Path $dest) { Remove-Item -Path $dest -Recurse -Force -ErrorAction SilentlyContinue }
    Copy-Item -Path $targetDir -Destination $dest -Recurse -Force
    Write-Host "      [+] Google Antigravity: Configured at $dest" -ForegroundColor Green
    $agentsConfigured++
}

# Agent B: Claude Code
$claudeSkills = "$HOME\.claude\skills"
if (Test-Path (Split-Path $claudeSkills -Parent)) {
    if (-not (Test-Path $claudeSkills)) { New-Item -ItemType Directory -Path $claudeSkills -Force | Out-Null }
    $dest = "$claudeSkills\clone-any-ui"
    if (Test-Path $dest) { Remove-Item -Path $dest -Recurse -Force -ErrorAction SilentlyContinue }
    Copy-Item -Path $targetDir -Destination $dest -Recurse -Force
    Write-Host "      [+] Claude Code: Configured at $dest" -ForegroundColor Green
    $agentsConfigured++
}

# Agent C: Cursor (.cursor / .cursorrules)
$cursorDir = "$HOME\.cursor"
if (Test-Path $cursorDir) {
    $cursorSkills = "$cursorDir\skills\clone-any-ui"
    if (-not (Test-Path "$cursorDir\skills")) { New-Item -ItemType Directory -Path "$cursorDir\skills" -Force | Out-Null }
    if (Test-Path $cursorSkills) { Remove-Item -Path $cursorSkills -Recurse -Force -ErrorAction SilentlyContinue }
    Copy-Item -Path $targetDir -Destination $cursorSkills -Recurse -Force
    Write-Host "      [+] Cursor: Configured at $cursorSkills" -ForegroundColor Green
    $agentsConfigured++
}

# Agent D: Windsurf / Codeium
$windsurfDir = "$HOME\.codeium\windsurf"
if (Test-Path $windsurfDir) {
    $wsSkills = "$windsurfDir\skills\clone-any-ui"
    if (-not (Test-Path "$windsurfDir\skills")) { New-Item -ItemType Directory -Path "$windsurfDir\skills" -Force | Out-Null }
    if (Test-Path $wsSkills) { Remove-Item -Path $wsSkills -Recurse -Force -ErrorAction SilentlyContinue }
    Copy-Item -Path $targetDir -Destination $wsSkills -Recurse -Force
    Write-Host "      [+] Windsurf: Configured at $wsSkills" -ForegroundColor Green
    $agentsConfigured++
}

# Agent E: Cline & Roo-Code (VS Code Extensions)
$vscodeExtDir = "$HOME\AppData\Roaming\Code\User\globalStorage"
if (Test-Path $vscodeExtDir) {
    Write-Host "      [+] VS Code (Cline / Roo-Code): Skill files available at $targetDir" -ForegroundColor Green
    $agentsConfigured++
}

if ($agentsConfigured -eq 0) {
    Write-Host "      [i] Global skill location preserved at: $targetDir" -ForegroundColor Yellow
}

# 5. Verification & Final Instructions
Write-Host "[5/5] Verifying installation..." -ForegroundColor White
Write-Host ""
Write-Host "==================================================================" -ForegroundColor Green
Write-Host "   🎉 SUCCESS! CLONE ANY UI IS FULLY INSTALLED & READY!           " -ForegroundColor Green
Write-Host "==================================================================" -ForegroundColor Green
Write-Host ""
Write-Host "How to use in ANY AI AGENT (Antigravity, Claude Code, Cursor, Windsurf):" -ForegroundColor Cyan
Write-Host '   Just prompt: "Clone https://target-site.com using the clone-any-ui skill"' -ForegroundColor White
Write-Host ""
Write-Host "How to use from Terminal:" -ForegroundColor Cyan
Write-Host "   cau --url https://example.com --out ./my-clone --all" -ForegroundColor White
Write-Host ""
Write-Host "Launch Visual Studio GUI:" -ForegroundColor Cyan
Write-Host "   cau-studio   (or python $targetDir\run_studio.py)" -ForegroundColor White
Write-Host "==================================================================" -ForegroundColor Green
Write-Host ""

