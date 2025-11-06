"""Configuration for Kimi K2 refactor."""

import os
from dotenv import load_dotenv

load_dotenv()

# API Configuration
MOONSHOT_API_KEY = os.getenv("MOONSHOT_API_KEY")
# Note: The correct endpoint is api.moonshot.ai (not .cn)
MOONSHOT_BASE_URL = "https://api.moonshot.ai/v1"

# Model Configuration
# Note: Kimi K2 model names - check Moonshot AI documentation for exact identifiers
# Kimi K2 models: "kimi-k2-0905-preview", "kimi-k2", etc.
# See: https://platform.moonshot.ai/docs/guide/kimi-k2-quickstart#powerful-agent-building-capabilities
KIMI_K2_MODEL = os.getenv("KIMI_MODEL", "kimi-k2-0905-preview")  # Default model

# Default settings
DEFAULT_MAX_TOKENS = 4000
DEFAULT_TEMPERATURE = 0.7
DEFAULT_TOP_P = 0.9

# Tool Configuration
USE_TOOLS = os.getenv("KIMI_USE_TOOLS", "true").lower() == "true"
TOOLS_ENABLED = USE_TOOLS  # Can be overridden per agent

# Thinking Mode Configuration
# Supports: "heavy", "medium", "light", or boolean values ("true"/"false")
# When set to "heavy", enables maximum reasoning effort
# When set to boolean, "true" enables default thinking mode, "false" disables it
THINKING_MODE = os.getenv("KIMI_ENABLE_THINKING", "true")
# For backward compatibility, also provide boolean flag
ENABLE_THINKING = THINKING_MODE.lower() not in ("false", "none", "off", "0")

# Fallback to verbose instructions if tools not available
FALLBACK_TO_VERBOSE = True

