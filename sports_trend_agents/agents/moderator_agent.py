import re
from pydantic import BaseModel, ValidationError

class TrendOutput(BaseModel):
    title: str
    summary: str
    impact: str

def validate_output(data: dict):
    try:
        clean = TrendOutput(**data)
        if re.search(r"(hate|violence|bias|fake)", clean.summary, re.IGNORECASE):
            return False, "Unsafe content detected"
        return True, clean
    except ValidationError as e:
        return False, str(e)
