"""Part 9 — In-memory approval store for pending human decisions."""

import time
from dataclasses import dataclass, field
from typing import Any
from uuid import uuid4
from enum import Enum


class ApprovalStatus(str, Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    EXPIRED = "expired"


APPROVAL_TTL_SECONDS = 86400  # 24 hours


@dataclass
class ApprovalRequest:
    approval_id: str
    workflow_type: str       # "prescription" | "billing" | "discharge"
    thread_id: str           # LangGraph thread ID for resumption
    payload: dict[str, Any]  # data surface to the approver
    status: ApprovalStatus = ApprovalStatus.PENDING
    created_at: float = field(default_factory=time.time)
    resolved_at: float | None = None
    resolved_by: str | None = None
    resolution: dict[str, Any] = field(default_factory=dict)


class ApprovalStore:
    """Thread-safe in-memory store for human-approval requests."""

    def __init__(self, ttl_seconds: int = APPROVAL_TTL_SECONDS) -> None:
        self._approvals: dict[str, ApprovalRequest] = {}
        self._ttl = ttl_seconds

    def create(
        self,
        workflow_type: str,
        thread_id: str,
        payload: dict,
    ) -> ApprovalRequest:
        approval_id = str(uuid4())
        req = ApprovalRequest(
            approval_id=approval_id,
            workflow_type=workflow_type,
            thread_id=thread_id,
            payload=payload,
        )
        self._approvals[approval_id] = req
        return req

    def get(self, approval_id: str) -> ApprovalRequest | None:
        req = self._approvals.get(approval_id)
        if req is None:
            return None
        if time.time() - req.created_at > self._ttl:
            req.status = ApprovalStatus.EXPIRED
        return req

    def resolve(
        self,
        approval_id: str,
        approved: bool,
        resolved_by: str,
        resolution: dict | None = None,
    ) -> ApprovalRequest | None:
        req = self.get(approval_id)
        if req is None or req.status != ApprovalStatus.PENDING:
            return None
        req.status = ApprovalStatus.APPROVED if approved else ApprovalStatus.REJECTED
        req.resolved_at = time.time()
        req.resolved_by = resolved_by
        req.resolution = resolution or {}
        return req

    def list_pending(self, workflow_type: str | None = None) -> list[ApprovalRequest]:
        result = [
            r for r in self._approvals.values()
            if r.status == ApprovalStatus.PENDING
        ]
        if workflow_type:
            result = [r for r in result if r.workflow_type == workflow_type]
        return result

    def list_all(self) -> list[ApprovalRequest]:
        return list(self._approvals.values())


_approval_store = ApprovalStore()


def get_approval_store() -> ApprovalStore:
    return _approval_store
