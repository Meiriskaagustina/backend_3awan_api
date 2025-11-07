from flask import Blueprint
from controllers.menu_controller import get_all_menus, add_menus, update_menus, delete_menus
from controllers.order_controller import get_all_order, add_orders, update_orders, delete_orders

web = Blueprint("web", __name__)

# Endpoint API
web.route("/", methods=["GET"])(get_all_menus)
web.route("/api/menus", methods=["POST"])(add_menus)
web.route("/api/menus/<int:id_menu>", methods=["PUT"])(update_menus)
web.route("/api/menus/<int:id_menu>", methods=["DELETE"])(delete_menus)

web.route("/api/orders", methods=["GET"])(get_all_order)
web.route("/api/orders", methods=["POST"])(add_orders)
web.route("/api/orders/<int:id_order>", methods=["PUT"])(update_orders)
web.route("/api/orders/<int:id_order>", methods=["DELETE"])(delete_orders)