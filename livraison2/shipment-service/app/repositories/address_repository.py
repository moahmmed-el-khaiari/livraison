from sqlalchemy.orm import Session
from app.models.address import Address

class AddressRepository:
    def create(self, db: Session, address: Address) -> Address:
        db.add(address)
        db.flush()  # obtient l'objet persisté sans commit
        return address
