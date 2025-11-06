from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship
from config.database import Base

class Order_item(Base):
    __tablename__ = "orders"

    id_order = Column(Integer, primary_key=True, index=True)
    id_menu = Column(Integer, ForeignKey("menus.id_menu"))
    costumer_name = Column(String(100), nullable=False)
    quantity = Column(Integer, default=1)
    subtotal = Column(Integer, nullable=False)

    # back_populates harus menunjuk nama relationship di model Menu (mis: order_items)
    menu = relationship("Menu", foreign_keys=[id_menu], back_populates="order_items")
