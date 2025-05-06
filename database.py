from peewee import *
from enum import Enum

DB = SqliteDatabase('database.db')


class Messages(Model):
    class MessageStatus(Enum):
        SEND = 'send'
        CHANGE = 'change'
        DELETE = 'delete'

    id_ = IntegerField(primary_key=True)
    from_ = CharField(max_length=255)
    to_ = CharField(max_length=255)
    data = DateTimeField()
    message = TextField()
    type_ = CharField()
    status = CharField(choices=[(role.value, role.name) for role in MessageStatus])

    class Meta:
        database = DB


if __name__ == '__main__':
    DB.create_tables([Messages])