from sqlalchemy import Column, Integer, VARCHAR, DateTime, ForeignKey, TEXT
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class project_source(Base):
    __tablename__ = "project_source"  # this is a field that tells package which table to query on
    id = Column(Integer, primary_key=True, autoincrement=True)
    project_name = Column(VARCHAR(255), nullable=False)
    repo_link = Column(VARCHAR(255), nullable=False)
    language = Column(VARCHAR(255), nullable=False)
    category = Column(VARCHAR(255), nullable=False)
    foundation = Column(VARCHAR(255))
    last_update = Column(DateTime())
    last_scan = Column(DateTime())

    def get_dict(self):
        return {
            "id": self.id,
            "project_name": self.project_name,
            "repo_link": self.repo_link,
            "language": self.language,
            "category": self.category,
            "foundation": self.foundation,
            "last_update": self.last_update,
            "last_scan": self.last_scan
        }


class scan_result(Base):
    __tablename__ = "scan_result"  # this is a field that tells package which table to query on
    id = Column(Integer, primary_key=True, autoincrement=True)
    project_id = Column(Integer, ForeignKey("project_source.id"))
    filename = Column(VARCHAR(255))
    report = Column(TEXT)
    create_time = Column(DateTime())
    project_source = relationship("project_source", backref="result_of_project")

    def get_dict(self):
        return {
            "id": self.id,
            "project_id": self.project_id,
            "file_name": self.filename,
            "report": self.report,
            "create_time": self.create_time,
            "project_name": self.project_source.project_name,
            "repo_link": self.project_source.repo_link,
            "language": self.project_source.language,
            "category": self.project_source.category,
            "foundation": self.project_source.foundation,
            "last_update": self.project_source.last_update,
            "last_scan": self.project_source.last_scan
        }


class user(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(VARCHAR(255), nullable=False, unique=True)
    password = Column(VARCHAR(255), nullable=False)

    def get_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "password": self.password,
        }


class key_repo(Base):
    __tablename__ = "key_repo"
    id = Column(Integer, primary_key=True)
    key = Column(VARCHAR(255), nullable=False, unique=True)
