import pathlib
import yaml

MANIFEST_DIR = pathlib.Path(__file__).resolve().parents[2] / 'infra' / 'gke'


def test_manifests_load() -> None:
    for path in MANIFEST_DIR.glob('*.yaml'):
        with path.open('r') as f:
            docs = list(yaml.safe_load_all(f))
            assert docs
