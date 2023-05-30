from db import db, BaseModel
from sqlalchemy.orm import mapped_column, relationship
from sqlalchemy import Integer, Float, Date
from sqlalchemy import ForeignKey
from sqlalchemy.sql.functions import now

from models.mixin_model import MixinModel


class PositionModel(BaseModel, MixinModel):
  __tablename__ = 'car_positions'
  id = mapped_column(Integer, primary_key=True)
  car_id = mapped_column(Integer, ForeignKey('cars.id'))
  latitude = mapped_column(Float)
  longitude = mapped_column(Float)
  date = mapped_column(Date)

  car = relationship('CarModel', back_populates='position', uselist=False)

  def __init__(self, car_id, latitude, longitude):
    self.car_id = car_id
    self.latitude = latitude
    self.longitude = longitude
    self.date = now()