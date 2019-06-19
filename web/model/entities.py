from sqlalchemy import Column, Integer, String, Sequence, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from database import connector
from datetime import datetime

class Users(connector.Manager.Base):
    __tablename__ = 'Users'
    id = Column(Integer, Sequence('users_id_seq'), primary_key=True)
    firstName = Column(String(50))
    lastName = Column(String(50))
    password = Column(String(80))
    isAdmin = Column(Boolean(), default=False)
    email = Column(String(50), unique=True)

class Championship(connector.Manager.Base):
    __tablename__ = 'Championships'
    id = Column(Integer, Sequence('championships_id_seq'), primary_key=True)
    title = Column(String(50))
    category = Column(String(10))
    maxCompetitors = Column(String(50))
    description = Column(String(1000))
    price = Column(Integer)
    startDate = Column(String(15))
    endDate = Column(String(15))
    location = Column(String(50))

class InscriptionSailing(connector.Manager.Base):
    __tablename__ = 'InscriptionsSailing'
    id = Column(Integer, Sequence('inscriptionsSailing_id_seq'), primary_key=True)
    sailingNumber = Column(String(50))
    category = Column(String(50))
    user_id = Column(Integer, ForeignKey('Users.id'))
    user = relationship(Users, foreign_keys=[user_id])
    championship_id = Column(Integer, ForeignKey('Championships.id'))
    championship = relationship(Championship, foreign_keys=[championship_id])


class InscriptionSoccer(connector.Manager.Base):
    __tablename__ = 'InscriptionsSoccer'
    id = Column(Integer, Sequence('inscriptionsSoccer_id_seq'), primary_key=True)
    soccerTeam = Column(String(50))
    category = Column(String(50))
    user_id = Column(Integer, ForeignKey('Users.id'))
    user = relationship(Users, foreign_keys=[user_id])
    championship_id = Column(Integer, ForeignKey('Championships.id'))
    championship = relationship(Championship, foreign_keys=[championship_id])

class Notification(connector.Manager.Base):
    __tablename__ = 'Notifications'
    id = Column(Integer, Sequence('notifications_id_seq'), primary_key=True)
    date = Column(default=datetime.now())
    text = Column(String(200))
    type = Column(String(30))

class Payment(connector.Manager.Base):
    __tablename__ = 'Payments'
    id = Column(Integer, Sequence('payments_id_seq'), primary_key=True)
    paymentToken = Column(String(80))
    user_id = Column(Integer, ForeignKey('Users.id'))
    user = relationship(Users, foreign_keys=[user_id])
    championship_id = Column(Integer, ForeignKey('Championships.id'))
    championship = relationship(Championship, foreign_keys=[championship_id])




"""
class EmergencyContact(connector.Manager.Base):
    __tablename__ = 'emergencyContact'
    id = Column(Integer, Sequence('message_id_seq'), primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship(User, foreign_keys=[user_id])
"""
