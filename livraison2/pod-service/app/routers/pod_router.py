from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db import get_db
from app.schemas.pod_schema import CreatePodRequest, PodOut
from app.services.pod_service import PodService

router = APIRouter(prefix="/pod", tags=["POD"])
service = PodService()


def to_out(pod) -> PodOut:
    return PodOut(
        id=pod.id,
        tracking_number=pod.tracking_number,
        receiver_name=pod.receiver_name,
        receiver_id_number=pod.receiver_id_number,
        signature_base64=pod.signature_base64,
        photo_url=pod.photo_url,
        note=pod.note,
        created_at=pod.created_at.isoformat(),
    )


@router.post("", response_model=PodOut, status_code=201)
def create_pod(payload: CreatePodRequest, db: Session = Depends(get_db)):
    pod = service.create_pod(db, payload)
    return to_out(pod)

@router.get("/pods", response_model=list[PodOut])
def list_pods(db: Session = Depends(get_db)):
    pods = service.list_pods(db)
    return [to_out(p) for p in pods]

@router.get("/{tracking_number}", response_model=PodOut)
def get_pod(tracking_number: str, db: Session = Depends(get_db)):
    pod = service.get_pod(db, tracking_number)
    return to_out(pod)
