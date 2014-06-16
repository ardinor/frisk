from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base
from hashlib import sha1

Base = declarative_base()

class FileHashes(Base):
    __tablename__ = 'file_hashes'

    hash_id = Column(Unicode(40), primary_key=True)

class FilePath(Base):
    __tablename__ = 'file_path'

    path_id = Column(Integer, autoincrement=True, primary_key=True)
    hash_id = Column(Unicode(40), ForeignKey('file_hashes.hash_id'))
    path = Column(Unicode(255))

    def __init__(self, filepath):
        self.path = filepath

    def calculate_hash(self, filepath):
        # From Ben's comments on StackOverflow (http://stackoverflow.com/a/19711609/2809087)
        sha = sha1()
        try:
            with open(filepath, 'rb') as f:
                while True:
                    block = f.read(2**10)
                    if not block:
                        break
                    sha.update(block)
            return sha.hexdigest()
        except IOError:
            # unable to read file
            return False

    def get_hash(self):
        return self.calculate_hash(filepath)
