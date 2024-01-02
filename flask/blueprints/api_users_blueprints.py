from flask import Blueprint, render_template, request, jsonify, flash, url_for, redirect
from models import db, User  # 请根据实际情况导入 User 模型

bp = Blueprint('api_users', __name__, url_prefix="/api")


@bp.route('/users', methods=['POST'])
def add_user():
    data = request.json
    user = User.query.filter(User.username == data['username'], User.gender == data['gender']).first()
    if user:
        return {'message': "用户已存在"}, 404
    try:
        # 创建用户
        new_user = User(username=data['username'], gender=data['gender'])
        db.session.add(new_user)
        db.session.commit()
        return jsonify({'message': '用户创建成功'})
    except Exception as e:
        db.session.rollback()
        print("错误消息: ", str(e))
        return {'message': "用户创建失败"}, 500


@bp.route('/users/<int:user_id>', methods=['PUT'])
def edit_user(user_id):
    data = request.json
    user = User.query.filter(User.username == data['username'], User.gender == data['gender']).first()
    if user:
        return {'message': "用户已存在"}, 404
    try:
        data = request.json
        user = User.query.get(user_id)
        if user:
            # 更新用户信息
            user.username = data.get('username', user.username)
            user.gender = data.get('gender', user.gender)

            # 提交更改到数据库
            db.session.commit()

            return jsonify({'message': '更新用户成功',
                            'user': {'id': user.id, 'username': user.username, 'gender': user.gender}})
        else:
            return jsonify({'message': '用户不存在'}), 404
    except Exception as e:
        return jsonify({'message': str(e)}), 500