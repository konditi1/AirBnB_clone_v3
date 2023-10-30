#!/usr/bin/python3
""" states view """
from flask import jsonify, abort
from models import storage
from models.state import State
from api.v1.views import app_views


@app_views.route("/states/<state_id>", strict_slashes=False, methods=["GET"])
@app_views.route("/states", strict_slashes=False, methods=["GET"])
def get_states(state_id=None):
    """ get all state objects """
    state_objs = storage.all(State)

    if state_id:
        for state_obj in state_objs:
            if state_obj.split(".")[1] == state_id:
                return jsonify(state_objs[state_obj].to_dict())
        abort(404)
        
    state_list = []

    for state_obj in state_objs:
        state_list.append(state_objs[state_obj].to_dict())

    return jsonify(state_list)
