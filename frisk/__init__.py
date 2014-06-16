from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

from frisk.settings import DATABASE_URI
from frisk.models import Base, FileHashes, CheckedFile


class Frisk():

    def __init__(self, folder):
        self.folder = folder
        self.engine = self.get_engine()
        self.Session = self.get_session(Base, self.engine)
        self.session = self.Session()

    def get_engine(self):
        return create_engine(DATABASE_URI)

    def get_session(self, base, engine):
        Session = sessionmaker()
        Session.configure(bind=engine)
        base.metadata.create_all(engine)

        return Session

    def check_file(self, filepath):
        existing_entry = self.session.query(CheckedFile).filter(CheckedFile.path==filepath)
        if existing_entry.count() > 0:
            # File already exists in DB, check the hash again?
            pass
        else:
            new_entry = CheckedFile(filepath)
            file_hash = new_entry.get_hash()
            existing_hash = self.session.query(FileHashes).filter(FileHashes.hash_id==file_hash)
            if existing_hash.count() > 0:
                existing_hash = existing_hash.one()
                new_entry.hash_id = existing_hash.id
            else:
                new_hash = FileHashes(file_hash)
                new_entry.hash_id = new_hash.id
                self.session.add(new_hash)
            self.session.add(new_entry)
            self.session.commit()

    def check_path(self, folder):
        for dirpath, dirnames, filenames in os.walk(folder):
            for file in filenames:
                self.check_file(os.path.join(dirpath, file))

    def run(self):
        self.check_path(self.folder)

