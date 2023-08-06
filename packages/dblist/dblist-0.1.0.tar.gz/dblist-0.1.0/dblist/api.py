from dblist import Session
from dblist.models import Sequence


def add_sequence(sequence):
    """Add a new sequence to the database."""

    seq = Sequence(sequence)
    session = Session()
    try:
        session.add(seq)
        session.commit()
        seq_id = seq.id_
    except:
        session.rollback()
        raise
    finally:
        session.close()

    return seq_id


def get_sequence(sequence_id):
    """Get a sequence by ID from the database."""
    session = Session()
    seq = session.query(Sequence).get(sequence_id)
    if not seq:
        msg = f'Could not find a sequence with ID {sequence_id}.'
        raise ValueError(msg)

    return seq.value
