#!/usr/bin/python3
""" cities view """
from flask import make_response, jsonify, abort, request
from models import storage
from models.city import City
from api.v1.views import app_views


@app_views.route("/cities/<city_id>", strict_slashes=False, methods=["GET"])
@app_views.route("/cities", strict_slashes=False, methods=["GET"])
def get_cities(city_id=None):
    """ get all city objects """
    city_objs = storage.all(City)

    if city_id:
        for city_obj in city_objs:
            if city_obj.split(".")[1] == city_id:
                return jsonify(city_objs[city_obj].to_dict())
        abort(404)

    city_list = []

    for city_obj in city_objs:
        city_list.append(city_objs[city_obj].to_dict())

    return jsonify(city_list)


@app_views.route("/cities/<city_id>", strict_slashes=False,
                 methods=["DELETE"])
def delete_cities(city_id):
    """ delete city objects """
    city_objs = storage.all(City)

    for city_obj in city_objs:
        if city_obj.split(".")[1] == city_id:
            city_objs[city_obj].delete()
            storage.save()
            return jsonify({})
    abort(404)


@app_views.route("/cities", strict_slashes=False, methods=["POST"])
def post_cities():
    """ create new city objects """
    if request.mimetype == "application/json":
        json_data = request.get_json()
        if "name" in json_data:
            city = City(**json_data)
            city.save()
            return make_response(jsonify(city.to_dict()), 201)
        else:
            abort(400, "Missing name")
    else:
        abort(400, "Not a JSON")


@app_views.route("/cities/<city_id>", strict_slashes=False, methods=["PUT"])
def put_cities(city_id):
    """ update city objects """
    id = "City.{}".format(city_id)

    if id in storage.all():
        city = storage.all()[id]

        if request.mimetype == "application/json":
            json_data = request.get_json()

            for item in json_data:
                setattr(city, item, json_data[item])

            city.save()
            return make_response(jsonify(city.to_dict()), 200)
        else:
            abort(400, "Not a JSON")
    else:
        abort(404)
