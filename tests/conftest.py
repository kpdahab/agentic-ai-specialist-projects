import sys, os

# Ensure repo root and src/ are on sys.path for imports
repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
src_dir = os.path.join(repo_root, "src")

sys.path.insert(0, repo_root)
sys.path.insert(0, src_dir)
