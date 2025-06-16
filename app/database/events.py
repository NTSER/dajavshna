from sqlalchemy import event
from sqlalchemy.orm import Session

from app.database.audit import ConsumerAudit, ProductAudit, SellerAudit, VenueAudit
from app.database.models import Consumer, Product, Seller, Venue

AUDIT_MAP = {
    Product: ProductAudit,
    Venue: VenueAudit,
    Seller: SellerAudit,
    Consumer: ConsumerAudit,
}


def create_audit(obj, audit_model, operation: str):
    obj_dict = obj.model_dump()
    id = obj_dict.pop("id")
    return audit_model(
        **obj_dict,
        operation=operation,
        **{f"{obj.__class__.__name__.lower()}_id": id},
    )


@event.listens_for(Session, "after_flush")
def audit(session: Session, flush_context):
    for operation, collection in [
        ("insert", session.new),
        ("update", session.dirty),
        ("delete", session.deleted),
    ]:
        for obj in collection:
            for model, audit_model in AUDIT_MAP.items():
                if isinstance(obj, model):
                    if operation == "update" and not session.is_modified(
                        obj, include_collections=False
                    ):
                        continue
                    session.add(create_audit(obj, audit_model, operation))
