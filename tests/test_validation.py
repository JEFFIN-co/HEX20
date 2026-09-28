import json
from pathlib import Path

def test_validation_artifacts_exist():
    root=Path(__file__).resolve().parents[1]
    data=json.loads((root/"validation/results.json").read_text())
    assert data["summary"]["total"]==1000
    assert data["summary"]["accepted"]==680
    assert data["summary"]["rejected"]==320
