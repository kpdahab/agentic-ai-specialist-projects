import sys
import importlib.util
from pathlib import Path

# Force tests to always load the repo root app.py
ROOT = Path(__file__).resolve().parents[1]
APP_PATH = ROOT / "app.py"

spec = importlib.util.spec_from_file_location("app", APP_PATH)
app = importlib.util.module_from_spec(spec)
sys.modules["app"] = app
spec.loader.exec_module(app)

# Fixtures for later, e.g. for AWS mocks
# @pytest.fixture
# def fake_secrets_manager(monkeypatch):
#     class FakeSM:
#         def get_secret_value(self, SecretId):
#             return {"SecretString": "fake-key"}
#     monkeypatch.setattr(app, "boto3", type("fake", (), {"client": staticmethod(lambda _: FakeSM())}))
#     return FakeSM()
