from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class RunData:
    project: str  # the name of the project
    run_id: str  # the uuid for the run
    status: str  # running, done, error
    path: str  # the path for the artifacts
    run_file: str  # the path to the json representation of the run
    user: str  # the user who runs the experiment

    start_time: str  # datetime str
    end_time: Optional[str] = None  # datetime str

    metrics: List[Dict] = field(default_factory=list)
    params: Dict[str, Any] = field(default_factory=dict)
    tags: List[str] = field(default_factory=list)
    artifacts: Dict[str, Dict] = field(default_factory=dict)

    git: Optional[Dict[str, Any]] = None
    call_info: Optional[Dict[str, Any]] = None
