from sqlalchemy import Column, Integer
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.sql import text

from flask_philo_sqlalchemy.exceptions import NotFoundError, InvalidQueryError
from flask_philo_sqlalchemy.schema import Base
from flask_philo_sqlalchemy.connection import create_pool


class BaseManager(object):
    """
    Base manager, every model will have this common manager
    that allows us to perform database common operations
    """
    def __init__(self, model):
        self._model = model
        self._pool = None

    @property
    def pool(self):
        if self._pool is None:
            self._pool = create_pool()
        return self._pool

    def filter_by(
        self, order_by='id', limit=500, offset=0,
            connection_name='DEFAULT', **kwargs):

        return self.pool.connections[connection_name].session.query(
            self._model
            ).filter_by(
                **kwargs
            ).order_by(order_by).limit(limit).offset(offset)

    def get_for_update(self, connection_name='DEFAULT', **kwargs):

        """
        http://docs.sqlalchemy.org/en/latest/orm/query.html?highlight=update#sqlalchemy.orm.query.Query.with_for_update  # noqa
        """
        if not kwargs:
            raise InvalidQueryError(
                "Can not execute a query without parameters")

        obj = self.pool.connections[connection_name].session.query(
            self._model).with_for_update(
                nowait=True, of=self._model).filter_by(**kwargs).first()
        if not obj:
            raise NotFoundError('Object not found')
        return obj

    def get(self, connection_name='DEFAULT', **kwargs):

        if not kwargs:
            raise InvalidQueryError(
                "Can not execute a query without parameters")
        obj = self.pool.connections[
            connection_name].session.query(
                self._model).filter_by(**kwargs).first()

        if not obj:
            raise NotFoundError('Object not found')
        return obj

    def count(self, connection_name='DEFAULT'):
        result = self.pool.connections[connection_name].session.execute(
            'SELECT count(id) from {}'.format(self._model.__table__.name)
        )

        r = result.fetchone()
        if len(r) > 0:
            return r[0]
        else:
            return 0

    def raw_sql(self, sql, connection_name='DEFAULT', **kwargs):
        return self.pool.connections[
            connection_name].session.execute(text(sql), kwargs)

    def add_all(self, data, connection_name='DEFAULT'):
        return self.pool.connections[connection_name].session.add_all(data)


class BaseModel(Base):
    """Abstract base model, contains common field and methods for all models
    """
    __abstract__ = True

    id = Column(Integer, primary_key=True)

    def __init__(self, **kwargs):
        super(BaseModel, self).__init__(**kwargs)
        for name, value in kwargs.items():
            if not name.startswith('_'):
                setattr(self, name, value)

    @property
    def dict(self):
        val = {
            k: v for k, v in self.__dict__.items() if (not k.startswith('_'))
        }
        return val

    @declared_attr
    def objects(cls):
        return BaseManager(cls)

    def update(self, connection_name='DEFAULT'):
        self.objects.pool.connections[connection_name].session.flush()

    def add(self, connection_name='DEFAULT'):
        self.objects.pool.connections[connection_name].session.add(self)
        self.objects.pool.connections[connection_name].session.flush()

    def delete(self, connection_name='DEFAULT'):
        self.objects.pool.connections[connection_name].session.delete(self)
        self.objects.pool.connections[connection_name].session.flush()
