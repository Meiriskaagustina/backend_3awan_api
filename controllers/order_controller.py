from flask import jsonify, request
from config.database import get_db
from models.order_model import Order_item
from models.menu_model import Menu
from sqlalchemy.orm import Session

# =========================
# GET ALL ORDERS
# =========================
def get_all_order():
    db: Session = next(get_db())
    orders = db.query(Order_item).all()
    result = []
    for o in orders:
        result.append({
            "id_order": getattr(o, "id_order", None),
            "id_menu": getattr(o, "id_menu", None),
            "costumer_name": getattr(o, "costumer_name", None),
            "quantity": getattr(o, "quantity", None),
            "subtotal": getattr(o, "subtotal", None),
            "menu": {
                "id_menu": getattr(o.menu, "id_menu", None),
                "name": getattr(o.menu, "name", None),
                "price": getattr(o.menu, "price", None),
                "category": getattr(o.menu, "category", None),
                "image_url": getattr(o.menu, "image_url", None),
            } if getattr(o, "menu", None) else None
        })
    return jsonify(result), 200

# =========================
# ADD ORDER
# =========================
def add_orders():
    db: Session = next(get_db())
    body = request.get_json() or {}

    required = ("id_menu", "costumer_name", "quantity")
    if not all(k in body for k in required):
        return jsonify({"message": "Payload tidak lengkap. Dibutuhkan: id_menu, costumer_name, quantity"}), 400

    menu = db.query(Menu).filter(Menu.id_menu == body["id_menu"]).first()
    if not menu:
        return jsonify({"message": "Menu tidak ditemukan"}), 404

    qty = int(body["quantity"])
    subtotal = (menu.price or 0) * qty

    new_order = Order_item(
        id_menu=body["id_menu"],
        costumer_name=body["costumer_name"],
        quantity=qty,
        subtotal=subtotal
    )
    db.add(new_order)
    db.commit()
    db.refresh(new_order)

    return jsonify({
        "message": "Order berhasil dibuat",
        "data": {
            "id_order": new_order.id_order,
            "id_menu": new_order.id_menu,
            "costumer_name": new_order.costumer_name,
            "quantity": new_order.quantity,
            "subtotal": new_order.subtotal
        }
    }), 201

# =========================
# UPDATE ORDER
# =========================
def update_orders(id_order):
    db: Session = next(get_db())
    body = request.get_json() or {}

    order = db.query(Order_item).filter(Order_item.id_order == id_order).first()
    if not order:
        return jsonify({"message": "Order tidak ditemukan"}), 404

    if "id_menu" in body:
        menu = db.query(Menu).filter(Menu.id_menu == body["id_menu"]).first()
        if not menu:
            return jsonify({"message": "Menu tidak ditemukan"}), 404
        order.id_menu = body["id_menu"]
    else:
        menu = db.query(Menu).filter(Menu.id_menu == order.id_menu).first()

    if "quantity" in body:
        order.quantity = int(body["quantity"])

    # recompute subtotal from menu.price and quantity
    order.subtotal = (menu.price or 0) * (order.quantity or 0)

    if "costumer_name" in body:
        order.costumer_name = body["costumer_name"]

    db.commit()
    db.refresh(order)

    return jsonify({
        "message": "Order berhasil diupdate",
        "data": {
            "id_order": order.id_order,
            "id_menu": order.id_menu,
            "costumer_name": order.costumer_name,
            "quantity": order.quantity,
            "subtotal": order.subtotal
        }
    }), 200

# =========================
# DELETE ORDER
# =========================
def delete_orders(id_order):
    db: Session = next(get_db())
    order = db.query(Order_item).filter(Order_item.id_order == id_order).first()
    if not order:
        return jsonify({"message": "Order tidak ditemukan"}), 404

    db.delete(order)
    db.commit()
    return jsonify({"message": f"Order dengan id {id_order} berhasil dihapus"}), 200
