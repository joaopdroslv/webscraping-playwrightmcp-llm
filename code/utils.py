import os
from typing import Any, Dict, List

import pandas as pd


def write_into_xlsx(output: List[Dict[str, Any]], filename: str) -> None:
    df = pd.DataFrame(output)
    df.to_excel(filename, index=False)


def make_dir(dir_name: str, root_dir: str = "./output") -> str:
    path = os.path.join(root_dir, dir_name)
    os.makedirs(path, exist_ok=True)
    return path
