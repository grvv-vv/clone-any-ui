#!/usr/bin/env bash
# ==============================================================================
#   CLONE ANY UI (CAU) — Universal 1-Command Installer for Linux & macOS
#   Usage: curl -fsSL https://raw.githubusercontent.com/grvv-vv/clone-any-ui/main/install.sh | bash
# ==============================================================================

set -e

# Terminal colors
CYAN='\033[0;36m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e ""
echo -e "${CYAN}==================================================================${NC}"
echo -e "${YELLOW}   ⚡ CLONE ANY UI (CAU) — UNIVERSAL 1-COMMAND INSTALLER         ${NC}"
echo -e "${CYAN}   Autonomous Web UI & Motion Replication Engine for AI Agents    ${NC}"
echo -e "${CYAN}==================================================================${NC}"
echo -e ""

# 1. Verify Python Installation
echo -e "[1/5] Checking Python environment..."
PYTHON_BIN=""
if command -v python3 &> /dev/null; then
    PYTHON_BIN="python3"
elif command -v python &> /dev/null; then
    PYTHON_BIN="python"
fi

if [ -z "$PYTHON_BIN" ]; then
    echo -e "${RED}[ERROR] Python 3 was not found in PATH.${NC}"
    echo -e "${YELLOW}Please install Python 3.10+ via your package manager:${NC}"
    echo -e "   macOS:        brew install python3"
    echo -e "   Ubuntu/Debian: sudo apt update && sudo apt install -y python3 python3-pip python3-venv git"
    echo -e "   Fedora/RHEL:  sudo dnf install -y python3 python3-pip git"
    echo -e "   Arch Linux:   sudo pacman -S python python-pip git"
    exit 1
fi

PY_VER=$($PYTHON_BIN --version 2>&1)
echo -e "      Detected: ${GREEN}${PY_VER}${NC}"

# 2. Determine Installation Directory
echo -e "[2/5] Setting up CAU repository..."
REPO_URL="https://github.com/grvv-vv/clone-any-ui.git"
INSTALL_DIR="$HOME/.clone-any-ui"

if [ -f "SKILL.md" ] && [ -f "clone_any_ui.py" ]; then
    TARGET_DIR="$(pwd)"
    echo -e "      Running inside repository: ${GREEN}${TARGET_DIR}${NC}"
else
    TARGET_DIR="$INSTALL_DIR"
    if [ -d "$TARGET_DIR" ]; then
        echo -e "      Updating existing installation at: ${TARGET_DIR}"
        if command -v git &> /dev/null; then
            git -C "$TARGET_DIR" pull --quiet || true
        fi
    else
        echo -e "      Cloning CAU into ${TARGET_DIR}..."
        if command -v git &> /dev/null; then
            git clone --depth 1 "$REPO_URL" "$TARGET_DIR"
        else
            echo -e "      Git not found, downloading tarball..."
            mkdir -p "$TARGET_DIR"
            curl -fsSL https://github.com/grvv-vv/clone-any-ui/archive/refs/heads/main.tar.gz | tar -xz -C "$TARGET_DIR" --strip-components=1
        fi
    fi
fi

# 3. Install Python Dependencies & CLI
echo -e "[3/5] Installing Python dependencies & CLI..."
cd "$TARGET_DIR"
$PYTHON_BIN -m pip install --upgrade pip --quiet || true
$PYTHON_BIN -m pip install -r requirements.txt --quiet
$PYTHON_BIN -m pip install -e . --quiet || true
echo -e "      ${GREEN}'cau' CLI registered and ready in PATH.${NC}"

# 4. Integrate into All AI Coding Agents
echo -e "[4/5] Auto-detecting & integrating with AI coding agents..."
AGENTS_FOUND=0

# Agent A: Google Antigravity (~/.gemini/config/skills)
ANTIGRAVITY_DIR="$HOME/.gemini/config/skills"
if [ -d "$HOME/.gemini" ]; then
    mkdir -p "$ANTIGRAVITY_DIR"
    rm -rf "$ANTIGRAVITY_DIR/clone-any-ui"
    cp -r "$TARGET_DIR" "$ANTIGRAVITY_DIR/clone-any-ui"
    echo -e "      [+] ${GREEN}Google Antigravity:${NC} Configured at $ANTIGRAVITY_DIR/clone-any-ui"
    AGENTS_FOUND=$((AGENTS_FOUND + 1))
fi

# Agent B: Claude Code (~/.claude/skills)
CLAUDE_DIR="$HOME/.claude/skills"
if [ -d "$HOME/.claude" ]; then
    mkdir -p "$CLAUDE_DIR"
    rm -rf "$CLAUDE_DIR/clone-any-ui"
    cp -r "$TARGET_DIR" "$CLAUDE_DIR/clone-any-ui"
    echo -e "      [+] ${GREEN}Claude Code:${NC} Configured at $CLAUDE_DIR/clone-any-ui"
    AGENTS_FOUND=$((AGENTS_FOUND + 1))
fi

# Agent C: Cursor (~/.cursor/skills)
CURSOR_DIR="$HOME/.cursor"
if [ -d "$CURSOR_DIR" ]; then
    mkdir -p "$CURSOR_DIR/skills"
    rm -rf "$CURSOR_DIR/skills/clone-any-ui"
    cp -r "$TARGET_DIR" "$CURSOR_DIR/skills/clone-any-ui"
    echo -e "      [+] ${GREEN}Cursor:${NC} Configured at $CURSOR_DIR/skills/clone-any-ui"
    AGENTS_FOUND=$((AGENTS_FOUND + 1))
fi

# Agent D: Windsurf (~/.codeium/windsurf/skills)
WINDSURF_DIR="$HOME/.codeium/windsurf"
if [ -d "$WINDSURF_DIR" ]; then
    mkdir -p "$WINDSURF_DIR/skills"
    rm -rf "$WINDSURF_DIR/skills/clone-any-ui"
    cp -r "$TARGET_DIR" "$WINDSURF_DIR/skills/clone-any-ui"
    echo -e "      [+] ${GREEN}Windsurf:${NC} Configured at $WINDSURF_DIR/skills/clone-any-ui"
    AGENTS_FOUND=$((AGENTS_FOUND + 1))
fi

if [ $AGENTS_FOUND -eq 0 ]; then
    echo -e "      [i] ${YELLOW}Global skill location preserved at: $TARGET_DIR${NC}"
fi

# 5. Summary
echo -e "[5/5] Finalizing setup..."
echo -e ""
echo -e "${GREEN}==================================================================${NC}"
echo -e "${GREEN}   🎉 SUCCESS! CLONE ANY UI IS FULLY INSTALLED & READY!           ${NC}"
echo -e "${GREEN}==================================================================${NC}"
echo -e ""
echo -e "${CYAN}How to use in ANY AI AGENT (Antigravity, Claude Code, Cursor, Windsurf):${NC}"
echo -e '   Just prompt: "Clone https://target-site.com using the clone-any-ui skill"'
echo -e ""
echo -e "${CYAN}How to use from Terminal:${NC}"
echo -e "   cau --url https://example.com --out ./my-clone --all"
echo -e ""
echo -e "${CYAN}Launch Visual Studio GUI:${NC}"
echo -e "   cau-studio   (or python3 $TARGET_DIR/run_studio.py)"
echo -e "${GREEN}==================================================================${NC}"
echo -e ""
