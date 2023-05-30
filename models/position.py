from db import db, BaseModel
from sqlalchemy.orm import mapped_column, relationship
from sqlalchemy import Integer, Float, DateTime, String
from sqlalchemy import ForeignKey
from sqlalchemy.sql.functions import now
import requests

from models.mixin_model import MixinModel


class PositionModel(BaseModel, MixinModel):
  __tablename__ = 'car_positions'
  id = mapped_column(Integer, primary_key=True)
  car_id = mapped_column(Integer, ForeignKey('cars.id'))
  latitude = mapped_column(Float)
  longitude = mapped_column(Float)
  date = mapped_column(DateTime)
  address = mapped_column(String(300))

  car = relationship('CarModel', back_populates='position', uselist=False)

  def resolve_address(self, latitude, longitude):
    url = f"https://nominatim.openstreetmap.org/reverse?format=json&lat={latitude}&lon={longitude}&zoom=18&addressdetails=1"
    response = requests.get(url)
    if response.status_code == 200:
      data = response.json()
      self.address = data.get("display_name", "")
    else:
      self.address = ""

  def __init__(self, car_id, latitude, longitude):
    self.car_id = car_id
    self.latitude = latitude
    self.longitude = longitude
    self.date = now()
    self.address = self.resolve_address(latitude=latitude, longitude=longitude)

  def json(self):
    position_json = {
        'latitude': self.latitude,
        'longitude': self.longitude,
        'date': self.date.isoformat() if self.date else None,
    }
    return position_json
