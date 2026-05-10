#!/usr/bin/env python3
"""
Migrate all LangGraph tutorial notebooks from OpenAI to NVIDIA NIM.
Run: python migrate_to_nvidia.py
"""

import json
import os
import re
import glob

NOTEBOOK_DIR = os.path.dirname(os.path.abspath(__file__))

# ── Model mapping ─────────────────────────────────────────────────────────────
MODEL_MAP = {
    "gpt-4-turbo":   "meta/llama-3.3-70b-instruct",
    "gpt-4o":        "meta/llama-3.3-70b-instruct",
    "gpt-4o-mini":   "meta/llama-3.1-8b-instruct",
    "gpt-3.5-turbo": "meta/llama-3.1-8b-instruct",
    "gpt-5-nano":    "meta/llama-3.3-70b-instruct",
    "gpt-4":         "meta/llama-3.3-70b-instruct",
}

# Read API key from environment — never hardcode secrets
try:
    from dotenv import load_dotenv
    load_dotenv(os.path.join(NOTEBOOK_DIR, ".env"))
except ImportError:
    pass
NVIDIA_API_KEY = os.getenv("NVIDIA_API_KEY", "nvapi-your-key-here")

# ── Source-level text replacements (applied to every cell source string) ──────
TEXT_REPLACEMENTS = [
    # Import replacement
    (
        r"from langchain_openai import ChatOpenAI",
        "from langchain_nvidia_ai_endpoints import ChatNVIDIA",
    ),
    # API-key env-var check (raise ValueError)
    (
        r'os\.getenv\("OPENAI_API_KEY"\)',
        'os.getenv("NVIDIA_API_KEY")',
    ),
    (
        r"os\.getenv\('OPENAI_API_KEY'\)",
        "os.getenv('NVIDIA_API_KEY')",
    ),
    # Env-var string literals in prints / checks
    (r'"OPENAI_API_KEY"', '"NVIDIA_API_KEY"'),
    (r"'OPENAI_API_KEY'", "'NVIDIA_API_KEY'"),
    # Installation hints in comments / markdown
    (r"langchain-openai", "langchain-nvidia-ai-endpoints"),
    (r"langchain_openai", "langchain_nvidia_ai_endpoints"),
    # Class name
    (r"\bChatOpenAI\b", "ChatNVIDIA"),
    # OpenAI-specific docs link (markdown cells)
    (
        r"https://platform\.openai\.com/api-keys",
        "https://build.nvidia.com/",
    ),
    (
        r"https://platform\.openai\.com/docs",
        "https://docs.nvidia.com/nim/",
    ),
    (
        r"\[OpenAI API Documentation\]\(https://platform\.openai\.com/docs\)",
        "[NVIDIA NIM Documentation](https://docs.nvidia.com/nim/)",
    ),
    # Error message text
    (
        r"OPENAI_API_KEY not set\. Add it to your \.env file\.",
        "NVIDIA_API_KEY not set. Add it to your .env file.",
    ),
    (
        r"OPENAI_API_KEY not found! Please:",
        "NVIDIA_API_KEY not found! Please:",
    ),
    (
        r"2\. Add: OPENAI_API_KEY=your_key_here",
        "2. Add: NVIDIA_API_KEY=your_key_here",
    ),
    (
        r"3\. Get a key from https://platform\.openai\.com/api-keys",
        "3. Get a key from https://build.nvidia.com/",
    ),
    # pip install comments
    (
        r"# pip install langgraph>=1\.1\.9 langchain-openai>=1\.2\.1",
        "# pip install langgraph>=1.1.9 langchain-nvidia-ai-endpoints",
    ),
    (
        r"# !pip install langgraph langchain-openai langchain-core python-dotenv",
        "# !pip install langgraph langchain-nvidia-ai-endpoints langchain-core python-dotenv",
    ),
    # Middleware reference to OpenAI moderation API comment
    (
        r"# Uses OpenAI moderation API automatically",
        "# Content moderation check",
    ),
    # Markdown prerequisite text
    (
        r"- OpenAI API key \(get one at https://platform\.openai\.com/api-keys\)",
        "- NVIDIA API key (get one at https://build.nvidia.com/)",
    ),
    (
        r"- `\.env` file configured with `OPENAI_API_KEY`",
        "- `.env` file configured with `NVIDIA_API_KEY`",
    ),
    (
        r"`OPENAI_API_KEY`",
        "`NVIDIA_API_KEY`",
    ),
    # Summarization middleware model arg (gpt-4o-mini string literal inside source)
    (
        r'model=\\"gpt-4o-mini\\"',
        'model=\\"meta/llama-3.1-8b-instruct\\"',
    ),
]

# ── Model string replacements for quoted model names ─────────────────────────
def replace_model_names(text: str) -> str:
    """Replace model name strings like \"gpt-4-turbo\" with NVIDIA equivalents."""
    for oai_model, nv_model in MODEL_MAP.items():
        # Handles both escaped-quote variants (in JSON) and plain variants
        text = text.replace(f'\\"{oai_model}\\"', f'\\"{nv_model}\\"')
        text = text.replace(f"\\'{oai_model}\\'", f"\\'{nv_model}\\'")
        text = text.replace(f'"{oai_model}"', f'"{nv_model}"')
        text = text.replace(f"'{oai_model}'", f"'{nv_model}'")
    return text


def migrate_source(source_lines: list) -> list:
    """Apply all text replacements to a cell's source lines."""
    result = []
    for line in source_lines:
        # Apply regex replacements
        for pattern, replacement in TEXT_REPLACEMENTS:
            line = re.sub(pattern, replacement, line)
        # Apply model-name replacements
        line = replace_model_names(line)
        result.append(line)
    return result


def migrate_notebook(path: str) -> int:
    """Migrate a single notebook. Returns number of cells modified."""
    with open(path, "r", encoding="utf-8") as f:
        nb = json.load(f)

    cells_modified = 0
    for cell in nb.get("cells", []):
        original = list(cell.get("source", []))
        cell["source"] = migrate_source(original)
        if cell["source"] != original:
            cells_modified += 1

    with open(path, "w", encoding="utf-8") as f:
        json.dump(nb, f, indent=1, ensure_ascii=False)
        f.write("\n")

    return cells_modified


def create_env_file():
    """Create .env file only if one doesn't already exist (preserves user keys)."""
    env_path = os.path.join(NOTEBOOK_DIR, ".env")
    if os.path.exists(env_path):
        print(f"⚪ {env_path} already exists — skipping (won't overwrite your keys)")
        return
    content = """# NVIDIA NIM API
NVIDIA_API_KEY=nvapi-your-key-here

# LangSmith Observability (required for Notebook 10)
LANGSMITH_API_KEY=ls-your-key-here
LANGCHAIN_TRACING_V2=true
LANGCHAIN_PROJECT=langgraph-tutorials

# LangGraph Platform (required for Notebook 10)
LANGGRAPH_API_URL=https://api.smith.langchain.com

# PostgreSQL (required for Notebooks 08-09 production sections)
# POSTGRES_CONNECTION_STRING=postgresql://user:pass@localhost:5432/langgraph
"""
    with open(env_path, "w") as f:
        f.write(content)
    print(f"✅ Created {env_path} — add your NVIDIA_API_KEY before running notebooks")


def update_env_example():
    """Update .env.example with NVIDIA credentials."""
    env_path = os.path.join(NOTEBOOK_DIR, ".env.example")
    content = """# NVIDIA NIM API
NVIDIA_API_KEY=nvapi-your-key-here

# Optional: Specify which model to use (defaults to meta/llama-3.3-70b-instruct)
# NVIDIA_MODEL=meta/llama-3.3-70b-instruct
# NVIDIA_MODEL=meta/llama-3.1-8b-instruct

# LangSmith Observability (required for Notebook 10)
LANGSMITH_API_KEY=ls-your-key-here
LANGCHAIN_TRACING_V2=true
LANGCHAIN_PROJECT=langgraph-tutorials

# LangGraph Platform (required for Notebook 10)
LANGGRAPH_API_URL=https://api.smith.langchain.com

# PostgreSQL (required for Notebooks 08-09 production sections)
# POSTGRES_CONNECTION_STRING=postgresql://user:pass@localhost:5432/langgraph
"""
    with open(env_path, "w") as f:
        f.write(content)
    print(f"✅ Updated {env_path}")


def update_pyproject():
    """Replace langchain-openai with langchain-nvidia-ai-endpoints in pyproject.toml."""
    path = os.path.join(NOTEBOOK_DIR, "pyproject.toml")
    with open(path, "r") as f:
        content = f.read()

    new_content = content.replace(
        '"langchain-openai>=1.2.1"',
        '"langchain-nvidia-ai-endpoints>=0.3.0"',
    ).replace(
        '"openai>=2.24.0"',
        '"langchain-nvidia-ai-endpoints>=0.3.0"',  # already replaced above, keep idempotent
    )
    # remove duplicate if both replaced to same line
    lines = new_content.splitlines()
    seen = set()
    deduped = []
    for line in lines:
        stripped = line.strip()
        if stripped == '"langchain-nvidia-ai-endpoints>=0.3.0",' and stripped in seen:
            continue
        deduped.append(line)
        seen.add(stripped)
    new_content = "\n".join(deduped) + "\n"

    with open(path, "w") as f:
        f.write(new_content)
    print(f"✅ Updated {path}")


def main():
    print("=" * 60)
    print("  LangGraph Tutorials → NVIDIA NIM Migration")
    print("=" * 60)

    # Create .env files
    create_env_file()
    update_env_example()

    # Update pyproject.toml
    update_pyproject()

    # Migrate all notebooks
    notebooks = sorted(glob.glob(os.path.join(NOTEBOOK_DIR, "*.ipynb")))
    print(f"\n📓 Found {len(notebooks)} notebooks\n")

    total_cells = 0
    for nb_path in notebooks:
        nb_name = os.path.basename(nb_path)
        n = migrate_notebook(nb_path)
        status = f"✅ {n} cell(s) modified" if n > 0 else "⚪ No changes needed"
        print(f"  {nb_name:55s} {status}")
        total_cells += n

    print(f"\n{'=' * 60}")
    print(f"  Migration complete! {total_cells} total cells updated.")
    print(f"  Provider:  NVIDIA NIM (langchain-nvidia-ai-endpoints)")
    print(f"  Model map:")
    for oai, nv in MODEL_MAP.items():
        print(f"    {oai:20s} → {nv}")
    print("=" * 60)
    print("\n📌 Next steps:")
    print("  1. uv pip install langchain-nvidia-ai-endpoints")
    print("  2. jupyter notebook")
    print("  3. Run notebooks – they now use NVIDIA NIM! 🚀")


if __name__ == "__main__":
    main()
