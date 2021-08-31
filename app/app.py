from flask import Flask, jsonify, request

from utils import load_data_in_memory

app = Flask(__name__)


@app.route("/", methods=["GET"])
def hello_world():
    return "Hello World!"


def get_exact_values(key, value, data):
    result = [row for row in data if row[key] == value]

    return result


def filter_email_domain(value, data):
    result = [row for row in data if row["email"].split("@")[1] == value]

    return result


@app.route("/users", methods=["GET"])
def users():
    file_data = load_data_in_memory()
    limit = int(request.args.get("limit", 10))

    id_ = request.args.get("id")
    if id_:
        file_data = get_exact_values("id", id_, file_data)

    else:
        possible_exact_filters = ["department", "first_name", "gender", "last_name"]

        for possible_filter in possible_exact_filters:
            filter_value = request.args.get(possible_filter)

            if filter_value:
                file_data = get_exact_values(possible_filter, filter_value, file_data)

        email_domain = request.args.get("email_domain")
        if email_domain:
            file_data = filter_email_domain(email_domain, file_data)

    if file_data:
        file_data = file_data[:limit]

    return jsonify(file_data)


if __name__ == '__main__':
    app.run(debug=True)
