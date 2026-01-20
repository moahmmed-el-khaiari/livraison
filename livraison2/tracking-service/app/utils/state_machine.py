from app.models.enums import TrackingStatus

# Transitions autorisées (machine à états)
ALLOWED_TRANSITIONS: dict[TrackingStatus, set[TrackingStatus]] = {
    TrackingStatus.CREATED: {TrackingStatus.PICKED_UP, TrackingStatus.EXCEPTION},
    TrackingStatus.PICKED_UP: {TrackingStatus.IN_TRANSIT, TrackingStatus.EXCEPTION},
    TrackingStatus.IN_TRANSIT: {TrackingStatus.IN_TRANSIT, TrackingStatus.OUT_FOR_DELIVERY, TrackingStatus.EXCEPTION},
    TrackingStatus.OUT_FOR_DELIVERY: {TrackingStatus.DELIVERED, TrackingStatus.EXCEPTION},
    TrackingStatus.DELIVERED: set(),   # état final
    TrackingStatus.EXCEPTION: {TrackingStatus.IN_TRANSIT, TrackingStatus.OUT_FOR_DELIVERY},  # reprise possible (option)
}

FINAL_STATES = {TrackingStatus.DELIVERED}

def is_transition_allowed(current: TrackingStatus, nxt: TrackingStatus) -> bool:
    return nxt in ALLOWED_TRANSITIONS.get(current, set())
