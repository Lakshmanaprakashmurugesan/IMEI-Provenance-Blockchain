import json, sys
from pathlib import Path
import pytest
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))

@pytest.fixture
def demo_values():
    return json.loads((ROOT/'evidence'/'demo_test_values.json').read_text(encoding='utf-8'))
