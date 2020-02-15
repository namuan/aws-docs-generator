import datetime
from pathlib import Path

from playhouse.sqlite_ext import (
    SqliteExtDatabase,
    Model,
    CharField,
    DateTimeField,
    FTSModel,
    TextField,
    IntegrityError
)

APP_DIR = Path.cwd()
DB_DIR = APP_DIR.joinpath("database")
DB_DIR.mkdir(parents=True, exist_ok=True)
DB_PATH = DB_DIR.joinpath("aws-code-docs.db")

db = SqliteExtDatabase(DB_PATH)


class BaseModel(Model):
    class Meta:
        database = db


class CodeDocumentItem(BaseModel):
    doc_sha = CharField(unique=True)
    topic = CharField()
    source_syntax = CharField()
    doc_md = TextField(null=True, default="")
    time_stamp = DateTimeField(default=datetime.datetime.now, index=True)

    def __str__(self):
        return f"{self.topic}"


class FTSCodeDocumentEntry(FTSModel):
    content = TextField()

    class Meta:
        database = db


def save_code_document(code_doc: CodeDocumentItem):
    print(f"Saving {code_doc}")
    try:
        code_doc.save(force_insert=True)
    except IntegrityError as e:
        print(f"Found duplicate file sha: {code_doc.doc_sha}")
        print(e)


print("Loading database from " + DB_PATH.as_posix())
db.connect()
db.create_tables([CodeDocumentItem])
