from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from config.database import Base

class Menu(Base):
    __tablename__ = "menus"

    id_menu = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    price = Column(Integer, nullable=False)
    category = Column(String(50))
    image_url = Column(String(255))

    # nama ini harus sama dengan back_populates di Order_item
    order_items = relationship("Order_item", back_populates="menu", lazy="select")
