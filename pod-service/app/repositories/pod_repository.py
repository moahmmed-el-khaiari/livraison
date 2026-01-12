from sqlalchemy.orm import Session
from app.models.proof_of_delivery import ProofOfDelivery


class PodRepository:
    def find_by_tracking(self, db: Session, tracking_number: str) -> ProofOfDelivery | None:
        return db.query(ProofOfDelivery).filter(ProofOfDelivery.tracking_number == tracking_number).first()

    def create(self, db: Session, pod: ProofOfDelivery) -> None:
        db.add(pod)

    def save(self, db: Session) -> None:
        db.commit()

    def refresh(self, db: Session, pod: ProofOfDelivery) -> None:
        db.refresh(pod)
