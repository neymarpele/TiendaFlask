from flask import Flask, render_template, session, redirect, url_for, request
from products import products
import os

app = Flask(__name__)

# Clave secreta
app.secret_key = os.environ.get("FLASK_SECRET", "clave_por_defecto")

# Obtener categorías
def get_categories():
    return sorted(set(p["category"] for p in products))


# HOME
@app.route("/")
def index():
    categories = get_categories()
    return render_template("index.html", products=products, categories=categories)


# BUSCAR (la versión correcta y única)
@app.route("/buscar")
def buscar():
    query = request.args.get("q", "").strip().lower()
    categories = get_categories()

    results = [p for p in products if query in p["name"].lower()]

    return render_template(
        "buscar.html",
        query=query,
        results=results,
        categories=categories
    )


# CATEGORÍA
@app.route("/categoria/<category>")
def categoria(category):
    filtered = [p for p in products if p["category"].lower() == category.lower()]
    categories = get_categories()

    return render_template(
        "categoria.html",
        products=filtered,
        category=category,
        categories=categories,
        empty=(len(filtered) == 0)
    )


# AGREGAR AL CARRITO
@app.route("/agregar/<int:producto_id>")
def add_to_cart(producto_id):
    session.setdefault("cart", [])
    session["cart"].append(producto_id)
    session.modified = True
    return redirect(url_for("cart"))


# VER CARRITO
@app.route("/carrito")
def cart():
    cart_ids = session.get("cart", [])
    categories = get_categories()
    items = [p for p in products if p["id"] in cart_ids]
    return render_template("cart.html", items=items, categories=categories)


# VACIAR CARRITO
@app.route("/vaciar")
def empty_cart():
    session["cart"] = []
    return redirect(url_for("cart"))


# DETALLE DE PRODUCTO
@app.route("/producto/<int:producto_id>")
def product_detail(producto_id):
    product = next((p for p in products if p["id"] == producto_id), None)
    categories = get_categories()

    if not product:
        return "Producto no encontrado", 404

    return render_template("product_detail.html", product=product, categories=categories)


if __name__ == "__main__":
    app.run(debug=True)
