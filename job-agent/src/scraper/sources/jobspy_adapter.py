"""
JobSpy adapter compatibility layer.
Delegates to MultiBoardAdapter under the AuraJobs architecture.
"""
from .multiboard_adapter import MultiBoardAdapter, JobSpyAdapter

__all__ = ["MultiBoardAdapter", "JobSpyAdapter"]
