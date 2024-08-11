import json


def load_json(path: str) -> dict:
    """
    Load json file

    Parameters
    ----------
    path: str
        Path to the JSON file that should be parsed.
    """
    with open(path, mode="r") as f:
        data = json.load(f)
    return data


def load_css(path) -> str:
    """
    Load css

    Parameters
    ----------
    path: str
        Path to css file
    """
    with open(path, mode="r") as f:
        text = f.read()
    return text
