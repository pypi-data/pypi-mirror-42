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

    remote_location: str = ""

    def summary(self) -> str:
        """Return a summary string of the data."""
        return f"""{'#' * 80}
# LOLA RUN SUMMARY    {self.run_id}
  - run_id:           {self.run_id}
  - project:          {self.project}
  - path:             {self.path}
  - status:           {self.status}
  - remote_location:  {self.remote_location}
  - start_time:       {self.start_time}
  - end_time:         {self.end_time}

  - metrics:          {len(self.metrics)} datapoint(s)
  - params:           {len(self.params)} datapoint(s)
  - artifacts:        {len(self.artifacts)} datapoint(s)
{'#' * 80}
"""
