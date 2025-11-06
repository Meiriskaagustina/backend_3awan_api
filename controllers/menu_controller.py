from flask import jsonify, request
from config.database import get_db
from models.menu_model import Menu
from sqlalchemy.orm import Session
from datetime import datetime

def get_all_menus():
    db: Session = next(get_db())
    data = db.query(Menu).all()
    return jsonify([{
        "id_menu": k.id_menu,
        "name": k.name,
        "price": k.price,
        "category": k.category,
        "image_url": k.image_url,
    } for k in data])

def add_menus():  
    db: Session = next(get_db())
    body = request.json

    new_data = Menu(
        name=body["name"],
        price=body["price"],
        category=body["category"],
        image_url=body["image_url"],
    )
    db.add(new_data)
    db.commit()
    db.refresh(new_data)

    return jsonify({
        "message": "Data berhasil ditambahkan",
        "data": {
            "id+menu": new_data.id_menu,
            "name": new_data.name,
            "price": new_data.price,
            "category": new_data.category,
            "image_url": new_data.image_url,
        }
    }), 201

def update_menus(id_menu):
    db: Session = next(get_db())
    body = request.json

    menu = db.query(Menu).filter(Menu.id_menu == id_menu).first()
    if not menu:
        return jsonify({"message": "menu tidak ditemukan"}), 404

    # Update field sesuai data yang dikirim
    menu.name = body.get("name", menu.name)
    menu.price = body.get("price", menu.price)
    menu.category = body.get("category", menu.category)
    menu.image_url = body.get("image_url", menu.image_url)
    db.commit()
    db.refresh(menu)

    return jsonify({
        "message": "Data berhasil diperbarui",
        "data": {
            "id_menu": menu.id+menu,
            "name": menu.name,
            "price": menu.price,
            "category": menu.category,
            "image_url": menu.image_url,
            
        }
    }), 200


# =========================
# DELETE DATA MENU
# =========================
def delete_menus(id_menu):
    db: Session = next(get_db())
    menu = db.query(Menu).filter(Menu.id_menu == id_menu).first()
    if not menu:
        return jsonify({"message": "menu tidak ditemukan"}), 404

    db.delete(menu)
    db.commit()

    return jsonify({"message": f"Data menu dengan id {id_menu} berhasil dihapus"}), 200