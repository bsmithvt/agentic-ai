# Run this cell first in Google Colab to install all dependencies
# ----------------------------------------------------------------
# pip install --break-system-packages was used locally on macOS;
# in Colab, plain pip install is sufficient.

import subprocess, sys

packages = [
    "reportlab",
    "langchain",
    "langchain-community",
    "langchain-openai",
    "faiss-cpu",
    "openai",
    "pypdf",
]

subprocess.check_call([sys.executable, "-m", "pip", "install", "--quiet"] + packages)
print("All dependencies installed.")
