from flask_security import UserMixin, RoleMixin
from flask_sqlalchemy.model import Model
from sqlalchemy import PrimaryKeyConstraint, Column, String, Integer, ForeignKey, Text, Boolean
from sqlalchemy.orm import relationship

from sifa_rehberi import db

roles_users = db.Table(
    "roles_users",
    db.Column("user_id", db.Integer(), db.ForeignKey("user.id", onupdate="CASCADE", ondelete="CASCADE")),
    db.Column("role_id", db.Integer(), db.ForeignKey("role.id", onupdate="CASCADE", ondelete="CASCADE")),
    PrimaryKeyConstraint("user_id", "role_id"), )


class Role(db.Model, RoleMixin):
    id = Column(db.Integer, primary_key=True)
    name = Column(db.String(20), nullable=False, unique=True)
    description = Column(db.String(255))


class User(db.Model, UserMixin):
    id = Column(Integer, primary_key=True)
    email = Column(String(20), nullable=False, unique=True)
    password = Column(String(80), nullable=False)
    active = Column(Boolean(), nullable=False, default=True)
    fs_uniquifier = Column(String(255), unique=True, nullable=False)
    roles = relationship("Role", secondary=roles_users, backref=db.backref("users", lazy="dynamic"))

    @property
    def simple_dict(self):
        return {"id": self.id, "email": self.email,"active":self.active}


class Bitki(db.Model):
    id = Column(Integer, primary_key=True)
    ad = Column(String(255), nullable=False)
    grup = Column(String(50))
    alt_grup = Column(String(50))
    receteler = relationship('Recete', backref='bitki', lazy=True)


class Hastalik(db.Model):
    id = Column(Integer, primary_key=True)
    ad = Column(String(255), nullable=False)
    receteler = relationship('Recete', backref='hastalik', lazy=True)


class Recete(db.Model):
    id = Column(Integer, primary_key=True)
    ad = Column(String(255), nullable=False)
    icerik = Column(Text)
    bitki_id = Column(Integer, ForeignKey('bitki.id'), nullable=False)
    hastalik_id = Column(Integer, ForeignKey('hastalik.id'), nullable=False)
