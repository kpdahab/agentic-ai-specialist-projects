import sys, os
# Add repo root and src/ to sys.path
repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
src_dir = os.path.join(repo_root, "src")
sys.path.insert(0, repo_root)
sys.path.insert(0, src_dir)