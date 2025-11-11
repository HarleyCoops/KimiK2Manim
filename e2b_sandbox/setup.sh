#!/bin/bash
# E2B Sandbox Setup Script for KimiK2Manim

set -e  # Exit on error

echo "=================================================="
echo "KimiK2Manim E2B Sandbox Setup"
echo "=================================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if running in E2B environment
if [ -d "/home/user" ]; then
    BASE_DIR="/home/user/kimik2"
else
    BASE_DIR="$(pwd)"
fi

echo -e "${GREEN}Using base directory: ${BASE_DIR}${NC}"

# Create necessary directories
echo -e "\n${YELLOW}Creating directories...${NC}"
mkdir -p "${BASE_DIR}/output"
mkdir -p "${BASE_DIR}/media/videos"
mkdir -p "${BASE_DIR}/media/images"
mkdir -p "${BASE_DIR}/logs"
mkdir -p "${BASE_DIR}/e2b_sandbox"

echo -e "${GREEN}✓ Directories created${NC}"

# Check Python version
echo -e "\n${YELLOW}Checking Python version...${NC}"
PYTHON_VERSION=$(python3 --version 2>&1 | grep -oP '\d+\.\d+')
REQUIRED_VERSION="3.13"

if awk "BEGIN {exit !($PYTHON_VERSION >= $REQUIRED_VERSION)}"; then
    echo -e "${GREEN}✓ Python $PYTHON_VERSION (>= $REQUIRED_VERSION required)${NC}"
else
    echo -e "${RED}✗ Python $PYTHON_VERSION found, but $REQUIRED_VERSION or higher is required${NC}"
    exit 1
fi

# Check if .env file exists
echo -e "\n${YELLOW}Checking environment configuration...${NC}"
if [ -f "${BASE_DIR}/.env" ]; then
    echo -e "${GREEN}✓ .env file found${NC}"
else
    echo -e "${YELLOW}! .env file not found${NC}"
    if [ -f "${BASE_DIR}/e2b_sandbox/.env.template" ]; then
        echo "  Copying .env.template to .env..."
        cp "${BASE_DIR}/e2b_sandbox/.env.template" "${BASE_DIR}/.env"
        echo -e "${GREEN}✓ Created .env from template${NC}"
        echo -e "${RED}! IMPORTANT: Edit .env and add your MOONSHOT_API_KEY${NC}"
    else
        echo -e "${RED}✗ No .env.template found${NC}"
    fi
fi

# Install Python dependencies
echo -e "\n${YELLOW}Installing Python dependencies...${NC}"

if command -v uv &> /dev/null; then
    echo "Using uv package manager..."
    uv pip install -e "${BASE_DIR}"
else
    echo "Using pip..."
    pip install -r "${BASE_DIR}/requirements.txt"
fi

# Install Manim
echo -e "\n${YELLOW}Installing Manim...${NC}"
pip install manim

echo -e "${GREEN}✓ Python dependencies installed${NC}"

# Install additional tools
echo -e "\n${YELLOW}Installing additional tools...${NC}"
pip install jupyter ipywidgets matplotlib numpy pandas rich typer httpx

echo -e "${GREEN}✓ Additional tools installed${NC}"

# Check ffmpeg
echo -e "\n${YELLOW}Checking ffmpeg...${NC}"
if command -v ffmpeg &> /dev/null; then
    FFMPEG_VERSION=$(ffmpeg -version 2>&1 | head -n1)
    echo -e "${GREEN}✓ ffmpeg found: ${FFMPEG_VERSION}${NC}"
else
    echo -e "${YELLOW}! ffmpeg not found${NC}"
    echo "  Install with: apt-get install ffmpeg (Ubuntu/Debian)"
fi

# Check LaTeX
echo -e "\n${YELLOW}Checking LaTeX...${NC}"
if command -v latex &> /dev/null; then
    LATEX_VERSION=$(latex --version 2>&1 | head -n1)
    echo -e "${GREEN}✓ LaTeX found: ${LATEX_VERSION}${NC}"
else
    echo -e "${YELLOW}! LaTeX not found${NC}"
    echo "  Install with: apt-get install texlive-full (Ubuntu/Debian)"
    echo "  Note: Manim can work without LaTeX but with limited text rendering"
fi

# Verify installation
echo -e "\n${YELLOW}Verifying installation...${NC}"

# Test imports
python3 -c "
import sys
sys.path.insert(0, '${BASE_DIR}')

try:
    from agents.prerequisite_explorer_kimi import KimiPrerequisiteExplorer
    from agents.enrichment_chain import KimiEnrichmentPipeline
    from e2b_sandbox.sandbox_config import SandboxConfig
    from e2b_sandbox.interactive_explorer import InteractiveExplorer
    print('✓ All modules imported successfully')
except ImportError as e:
    print(f'✗ Import error: {e}')
    sys.exit(1)
"

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Installation verified${NC}"
else
    echo -e "${RED}✗ Installation verification failed${NC}"
    exit 1
fi

# Display summary
echo -e "\n=================================================="
echo -e "${GREEN}Setup Complete!${NC}"
echo "=================================================="
echo ""
echo "Next steps:"
echo "  1. Edit .env file and add your MOONSHOT_API_KEY"
echo "  2. Run an exploration:"
echo "     python e2b_sandbox/interactive_explorer.py"
echo "  3. Run visual reasoning tests:"
echo "     python e2b_sandbox/visual_reasoning_tests.py"
echo "  4. Use sandbox tools:"
echo "     python e2b_sandbox/tools.py menu"
echo ""
echo "Directory structure:"
echo "  Output: ${BASE_DIR}/output"
echo "  Media:  ${BASE_DIR}/media"
echo "  Logs:   ${BASE_DIR}/logs"
echo ""
echo "=================================================="

# Make this script executable
chmod +x "$0"
