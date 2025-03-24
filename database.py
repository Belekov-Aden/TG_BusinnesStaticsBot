from peewee import *

DB = SqliteDatabase('database.db')


class Messages(Model):
    id_ = IntegerField(primary_key=True)
    from_ = CharField(max_length=255)
    to_ = CharField(max_length=255)
    data = DateTimeField()
    message = TextField()

    class Meta:
        database = DB


if __name__ == '__main__':
    DB.create_tables([Messages])