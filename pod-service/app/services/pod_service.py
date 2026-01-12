from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.models.proof_of_delivery import ProofOfDelivery
from app.repositories.pod_repository import PodRepository
from app.schemas.pod_schema import CreatePodRequest
from app.services.tracking_client import TrackingClient, TrackingEventCreate
from app.utils.id_utils import new_uuid
from app.utils.time_utils import now_utc


class PodService:
    def __init__(self):
        self.repo = PodRepository()
        self.tracking = TrackingClient()

    def create_pod(self, db: Session, req: CreatePodRequest) -> ProofOfDelivery:
        existing = self.repo.find_by_tracking(db, req.tracking_number)
        if existing:
            raise HTTPException(status_code=409, detail="POD already exists for this tracking number")

        pod = ProofOfDelivery(
            id=new_uuid(),
            tracking_number=req.tracking_number,
            receiver_name=req.receiver_name,
            receiver_id_number=req.receiver_id_number,
            signature_base64=req.signature_base64,
            photo_url=req.photo_url,
            note=req.note,
            created_at=now_utc(),
        )

        self.repo.create(db, pod)
        self.repo.save(db)
        self.repo.refresh(db, pod)

        # Push event to tracking
        self.tracking.add_event(
            TrackingEventCreate(
                tracking_number=req.tracking_number,
                status="DELIVERED_CONFIRMED",
                message=f"POD confirmed by {req.receiver_name}",
            )
        )

        return pod

    def get_pod(self, db: Session, tracking_number: str) -> ProofOfDelivery:
        pod = self.repo.find_by_tracking(db, tracking_number)
        if not pod:
            raise HTTPException(status_code=404, detail="POD not found")
        return pod
