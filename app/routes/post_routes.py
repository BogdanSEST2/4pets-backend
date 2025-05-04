from flask import Blueprint, jsonify, request



bp = Blueprint('post', __name__) 


@bp.route('/posts', methods=['GET'])
def get_all_posts():
    return jsonify({"message": "Тут будут все посты"}), 200


@bp.route('/posts/<int:post_id>', methods=['GET'])
def get_post_by_id(post_id):
    return jsonify({"message": f"Пост с ID {post_id}"}), 200
