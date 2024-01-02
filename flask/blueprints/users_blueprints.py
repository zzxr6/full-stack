from flask import Blueprint, render_template, request, jsonify, flash, url_for, redirect
from models import db, User  # 请根据实际情况导入 User 模型

bp = Blueprint('users', __name__, url_prefix="/")


@bp.route('/users', methods=['GET'])
def get_user_list():
    page = int(request.args.get('page'))
    per_page = 5
    start = (page - 1) * per_page
    users = User.query.offset(start).limit(per_page).all()
    # 获取总用户数
    total_users = User.query.count()
    print(page)
    # 将结果以JSON格式返回
    return jsonify({
        'users': [{'id': user.id, 'username': user.username, 'gender': user.gender} for user in users],
        'total_users': total_users
    })

