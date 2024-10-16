from app.models import Node
from app import db
import uuid


fond = Node(title="Fond-1", ref_code=str(uuid.uuid4()),level_of_description="Fonds")
db.session.add(fond)


for a in range(10):
    serie = Node(title=f"Serie-{a}", parent=fond, ref_code=str(uuid.uuid4()), level_of_description="series")
    db.session.add(serie)
    for b in range(5):
        sub_serie = Node(title=f"SubSerie-{b}", parent=serie, ref_code=str(uuid.uuid4()),level_of_description="subseries")
        db.session.add(sub_serie)
        for c in range(3):
            box = Node(title=f"Box-{c}", parent=sub_serie, ref_code=str(uuid.uuid4()),level_of_description="box")
            db.session.add(box)

db.session.commit()
