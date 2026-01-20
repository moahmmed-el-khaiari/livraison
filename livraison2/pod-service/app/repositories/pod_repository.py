from sqlalchemy.orm import Session
from app.models.proof_of_delivery import ProofOfDelivery
from sqlalchemy.orm import Session


class PodRepository:
    def find_by_tracking(self, db: Session, tracking_number: str) -> ProofOfDelivery | None:
        return db.query(ProofOfDelivery).filter(ProofOfDelivery.tracking_number == tracking_number).first()

    def create(self, db: Session, pod: ProofOfDelivery) -> None:
        db.add(pod)

    def save(self, db: Session) -> None:
        db.commit()

    def refresh(self, db: Session, pod: ProofOfDelivery) -> None:
        db.refresh(pod)

    def find_all(self, db: Session):
     return db.query(ProofOfDelivery).all()
