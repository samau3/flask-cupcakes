"""Flask app for Cupcakes"""
from flask import Flask, flash, redirect, render_template, request, jsonify

# separate external and internal imports
from models import db, connect_db, Cupcake


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)


app.config['SECRET_KEY'] = "MY_SECRET"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False


db.create_all()


@app.get("/api/cupcakes")
def list_all_cupcakes():
    """Return JSON {cupcakes: [{id, flavor, size, rating, image}, ...]}"""

    cupcakes = Cupcake.query.all()
    serialized = [cupcake.serialize() for cupcake in cupcakes]

    return jsonify(cupcakes=serialized)


@app.get("/api/cupcakes/<int:cupcake_id>")
def list_single_cupcake(cupcake_id):
    """Return JSON {cupcake: {id, flavor, size, rating, image}}"""

    cupcake = Cupcake.query.get_or_404(cupcake_id)
    serialized = cupcake.serialize()

    return jsonify(cupcake=serialized)


@app.post("/api/cupcakes")
def create_cupcake():
    """ Create cupcake from JSON data and return it

    Respond with JSON like: {cupcake: {id, flavor, size, rating, image}}
    """

    flavor = request.json["flavor"]
    size = request.json["size"]
    rating = request.json["rating"]
    image = request.json["image"]

    new_cupcake = Cupcake(flavor=flavor,
                          size=size,
                          rating=rating,
                          image=image)

    db.session.add(new_cupcake)
    db.session.commit()

    serialized = new_cupcake.serialize()

    return (jsonify(cupcake=serialized), 201)


@app.patch("/api/cupcakes/<int:cupcake_id>")
def modify_cupcake(cupcake_id):
    """Update cupcake

    Respond with JSON {cupcake: {id, flavor, size, rating, image}}
    """

    cupcake = Cupcake.query.get_or_404(cupcake_id)
    resp = request.json

    if (resp.get("flavor")):
        cupcake.flavor = resp["flavor"]
    if (resp.get("size")):
        cupcake.size = resp["size"]
    if (resp.get("rating")):
        cupcake.rating = resp["rating"]
    if (resp.get("image")):
        cupcake.image = resp["image"]

    db.session.commit()

    serialized = cupcake.serialize()

    return (jsonify(cupcake=serialized))


@app.delete("/api/cupcakes/<int:cupcake_id>")
def delete_cupcakes(cupcake_id):
    """Delete cupcakes and respond with {deleted: [cupcake-id]}"""

    cupcake = Cupcake.query.get_or_404(cupcake_id)
    db.session.delete(cupcake)
    db.session.commit()

    return (jsonify(f"deleted: {cupcake_id}"))
