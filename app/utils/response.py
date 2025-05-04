from flask import jsonify



def success_response(data=None, message="Успешно", status=200):
    response = {"status": "success", "message": message}
    if data is not None:
        response["data"] = data
    return jsonify(response), status


def error_response(message="Ошибка", status=400):
    return jsonify({
        "status": "error",
        "message": message
    }), status