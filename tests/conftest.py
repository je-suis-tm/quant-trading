from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path

import matplotlib


matplotlib.use("Agg")


def load_script_module(script_name: str, module_name: str | None = None):
    script_path = Path(__file__).resolve().parents[1] / script_name
    resolved_name = module_name or script_path.stem.replace(" ", "_").replace("-", "_")
    spec = spec_from_file_location(resolved_name, script_path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Could not load module from {script_path}")

    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module
