# =============================================================================
# MAC - UNIT TEST PREREQUISITE 
# =============================================================================

1. Install Python 3.12 (if not already installed)
On Ubuntu/Debian:
sudo apt update
sudo apt install -y software-properties-common
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt update
sudo apt install -y python3.12 python3.12-venv python3.12-dev

On macOS (with Homebrew):
brew install python@3.12

2. Verify Python 3.12 installation
python3.12 --version

3. Create a virtual environment using Python 3.12
python3.12 -m venv .venv

4. Activate the environment
source .venv/bin/activate

5. Upgrade pip (optional but recommended)
pip install --upgrade pip

6. Install project dependencies
pip install -r requirements.txt
pip install pytest
- Troubleshoot:
-- which pytest (should show: /venv/bin/pytest). If not: export PATH="$(pwd)/.venv/bin:$PATH"

7. Set PYTHONPATH so tests can find your src modules
export PYTHONPATH=.

8. Run all unit tests with verbose output (unit-marked only)
pytest -v -m "unit"

--- VS Code users: ---
To select the interpreter:
Press Cmd+Shift+P → "Python: Select Interpreter" → Choose ".venv/bin/python"


# =============================================================================
# WINDOWS - UNIT TEST PREREQUISITE 
# =============================================================================

1. Download Python 3.12 from https://www.python.org/downloads/windows/
   and run the installer (make sure to check 'Add Python to PATH').

2. Verify installation:
python --version

If you have multiple versions, use:
py -3.12 --version

3. Create virtual environment using Python 3.12:
py -3.12 -m venv .venv

4. Activate the environment:
.venv\Scripts\activate

5. Upgrade pip (optional but recommended):
python -m pip install --upgrade pip

6. Install project dependencies:
pip install -r requirements.txt
pip install pytest

7. Set PYTHONPATH so tests can find your src modules:
set PYTHONPATH=.

8. Run all unit tests with verbose output (unit-marked only):
pytest -v -m "unit"

--- VS Code users: ---
To select the interpreter:
  Ctrl+Shift+P → "Python: Select Interpreter" → Choose ".venv\\Scripts\\python.exe"

