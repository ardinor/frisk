from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql.expression import func
import os

from frisk.settings import DATABASE_URI
from frisk.models import Base, FileHashes, CheckedFile


class Frisk():

    def __init__(self, base_folder=None, single_file=None, single_name=None):
        self.base_folder = base_folder
        self.single_file = single_file
        self.single_name = single_name
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
                self.session.add(new_hash)
                self.session.commit()
                new_entry.hash_id = new_hash.id
            self.session.add(new_entry)
            self.session.commit()

    def check_path(self, folder):
        for dirpath, dirnames, filenames in os.walk(folder):
            for file in filenames:
                self.check_file(os.path.normpath(os.path.join(dirpath, file)))

    def check_name(self, name):
        results = ''
        # When searching, search using lower case so users don't need to put
        # the correct case in when searching.
        existing_entry = self.session.query(CheckedFile). \
            filter(func.lower(CheckedFile.path).like('%{}%'.format(name.lower())))
        if existing_entry.count() > 0:
            if existing_entry.count() > 1:
                for found_entry in existing_entry.all():
                    results += 'File found - {}'.format(os.path.normpath(found_entry.path)) +'\n'
            else:
                results += 'File found - {}'.format(os.path.normpath(existing_entry.one().path))
        else:
            results += "No file with the name '{}' found in the database.".format(name)
        return results.strip()

    def run(self):
        if self.base_folder:
            self.check_path(self.base_folder)
        elif self.single_file:
            self.check_file(self.single_file)
        elif self.single_name:
            result = self.check_name(self.single_name)
            return result

