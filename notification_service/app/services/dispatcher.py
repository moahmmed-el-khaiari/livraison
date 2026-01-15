import asyncio
from sqlalchemy.orm import Session

from app.config import settings
from app.db import SessionLocal
from app.repositories.notification_repository import NotificationRepository
from app.utils.time_utils import now_utc

class Dispatcher:
    def __init__(self):
        self.repo = NotificationRepository()
        self._running = False

    async def run(self):
        if not settings.DISPATCHER_ENABLED:
            return

        self._running = True
        while self._running:
            db: Session = SessionLocal()
            try:
                pending = self.repo.list_pending(db, limit=10)
                for n in pending:
                    # ✅ Ici tu brancheras email/sms/push plus tard
                    # Pour le projet: on simule l'envoi
                    print(f"[DISPATCH] send {n.channel} => {n.title} / {n.recipient}")

                    n.status = "SENT"
                    n.sent = True
                    n.sent_at = now_utc()

                db.commit()
            finally:
                db.close()

            await asyncio.sleep(settings.DISPATCHER_INTERVAL_SECONDS)

    def stop(self):
        self._running = False
