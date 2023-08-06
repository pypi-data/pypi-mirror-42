import numbers

from sqlalchemy import Column, Integer, String, ForeignKey, Enum, Boolean, Table, Float
from sqlalchemy.orm import relationship, backref
import numpy as np

from dblist.base import Base


class Sequence(Base):
    """Class to represent the storage of a list or Numpy array within a
    relational database."""

    __tablename__ = 'dbl_seq'

    id_ = Column('id', Integer, primary_key=True)
    is_array = Column(Boolean, nullable=False)

    parent_id = Column(Integer, ForeignKey('dbl_seq.id'))
    order_id = Column(Integer)

    sub_sequences = relationship('Sequence')
    values_float = relationship('SequenceValueFloat')
    values_int = relationship('SequenceValueInt')

    def __init__(self, sequence, order_id=None):

        self.is_array = isinstance(sequence, np.ndarray)
        self.order_id = order_id

        if not isinstance(sequence, (list, np.ndarray)):
            msg = ('For a sequence to be added to the database, it must be '
                   'a `list` or `numpy.ndarray`.')
            raise ValueError(msg)

        for i_idx, i in enumerate(sequence):

            if isinstance(i, numbers.Integral):
                val = SequenceValueInt(int(i), i_idx)
                self.values_int.append(val)

            elif isinstance(i, numbers.Number):
                val = SequenceValueFloat(float(i), i_idx)
                self.values_float.append(val)

            elif isinstance(i, (list, np.ndarray)):
                val = Sequence(i, i_idx)
                self.sub_sequences.append(val)

            else:
                msg = (f'Sequence element is of type {type(i)}, which is not '
                       f'supported.')
                raise ValueError(msg)

    @property
    def value(self):
        children = self.sub_sequences + self.values_float + self.values_int
        out = [i.value for i in sorted(children, key=lambda x: x.order_id)]
        if self.is_array:
            out = np.array(out)
        return out


class SequenceValueFloat(Base):
    """Class to represent floating point numbers."""

    __tablename__ = 'dbl_val_float'

    sequence_id = Column(Integer, ForeignKey('dbl_seq.id'), primary_key=True)
    order_id = Column(Integer, primary_key=True)
    value = Column(Float)

    def __init__(self, value, order_id):
        if not isinstance(value, float):
            msg = (f'Unexpected data type. Expected a `float`, but got a '
                   f'{type(value)}')
            raise ValueError(msg)
        self.value = value
        self.order_id = order_id


class SequenceValueInt(Base):
    """Class to represent integer numbers."""

    __tablename__ = 'dbl_val_int'

    sequence_id = Column(Integer, ForeignKey('dbl_seq.id'), primary_key=True)
    order_id = Column(Integer, primary_key=True)
    value = Column(Integer)

    def __init__(self, value, order_id):

        if not isinstance(value, int):
            msg = (f'Unexpected data type. Expected an `int`, but got a '
                   f'{type(value)}')
            raise ValueError(msg)
        self.value = value
        self.order_id = order_id
