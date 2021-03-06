from sqlalchemy import Column, String, Integer, ForeignKey, Unicode
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base
from hashlib import sha1
import os

Base = declarative_base()

class FileHashes(Base):
    __tablename__ = 'file_hashes'

    id = Column(Integer, autoincrement=True, primary_key=True)
    hash_id = Column(Unicode(40))
    files = relationship("CheckedFile", backref="hash")

    def __init__(self, hash_id):
        self.hash_id = hash_id

    def __repr__(self):
        return '<FileHash: {}>'.format(self.hash_id)

class CheckedFile(Base):
    __tablename__ = 'checked_file'

    id = Column(Integer, autoincrement=True, primary_key=True)
    # Access the the file_hashes using 'hash'
    hash_id = Column(Integer, ForeignKey('file_hashes.id'))
    path = Column(Unicode(255))

    def __init__(self, filepath):
        # Double check we're receiving a valid file path
        if os.path.exists(filepath):
            self.path = filepath

    def __repr__(self):
        return '<File: {}>'.format(self.path)

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
        return self.calculate_hash(self.path)
