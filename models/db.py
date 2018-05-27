from peewee import SqliteDatabase, Model

db = SqliteDatabase('worklog.sqlite')

MODELS = []

class BaseModel(Model):
    class Meta:
        database = db

    @staticmethod
    def register(cls):
        MODELS.append(cls)
        return cls

def init_db():
    for model in MODELS:
        model.create_table(True)
