from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, Post, User  # Đổi từ .models thành models
import os
import uuid
import logging

posts_bp = Blueprint('posts', __name__)

# Configure upload folder (create this folder in your backend directory)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True) # Ensure the directory exists

# Helper to generate slug
def generate_slug(title):
    import re
    import unicodedata

    title_no_accent = unicodedata.normalize('NFD', title).encode('ascii', 'ignore').decode('utf-8')
    slug = title_no_accent.lower()
    slug = re.sub(r'[^a-z0-9\s-]', '', slug)
    slug = re.sub(r'[\s_-]+', '-', slug)
    slug = re.sub(r'^-+|-+$', '', slug)
    
    return slug

@posts_bp.route('/posts', methods=['GET'])
def get_posts():
    is_featured = request.args.get('is_featured', type=str)
    is_latest = request.args.get('is_latest', type=str)
    limit = request.args.get('limit', type=int)
    query = Post.query

    if is_featured == 'true':
        query = query.filter_by(is_featured=True)

    query = query.order_by(Post.created_at.desc())

    if is_latest == 'true' and limit:
        # Nếu yêu cầu bài viết mới nhất và có giới hạn
        posts = query.filter_by(is_latest=True).limit(limit).all()
    elif is_latest == 'true':
        # Nếu yêu cầu bài viết mới nhất nhưng không có giới hạn (trả về tất cả theo thứ tự mới nhất)
        posts = query.filter_by(is_latest=True)
    elif is_featured == 'true':
        # Nếu chỉ yêu cầu bài viết nổi bật (đã được filter ở trên)
        posts = query.filter_by(is_featured=True)
    else:
        posts = query.all()

    if not posts:
        return jsonify([]), 200 
    
    # posts = Post.query.order_by(Post.created_at.desc()).all()
    output = []
    if not posts:
        return jsonify({"msg": "Bài viết không tìm thấy."}), 404
    output = []
    for post in posts:
       
        output.append({
            'id': post.id,
            'title': post.title,
            'slug': post.slug,
            'image_url': post.image_url,
            'created_at': post.created_at.isoformat(),
            'author': post.author.username,
            'content': post.content, 
            'is_featured': post.is_featured, 
            'is_latest': post.is_latest 
        })
    return jsonify(output), 200

# @posts_bp.route('/posts/<string:slug>', methods=['GET'])
# def get_post(slug):
#     post = Post.query.filter_by(slug=slug).first_or_404()
#     return jsonify({
#         'id': post.id,
#         'title': post.title,
#         'slug': post.slug,
#         'content': post.content,
#         'image_url': post.image_url,
#         'created_at': post.created_at.isoformat(),
#         'updated_at': post.updated_at.isoformat(),
#         'author': post.author.username
#     }), 200
@posts_bp.route('/posts/<string:slug>', methods=['GET'])
def get_post(slug):
    post = Post.query.filter_by(slug=slug).first()
    if not post:
        return jsonify({"msg": "Bài viết không tìm thấy."}), 404
    
    # Đảm bảo bạn trả về đầy đủ các trường cần thiết, bao gồm 'content'
    # và 'author' là một dictionary (object) như frontend mong đợi.
    post_data = {
        'id': post.id,
        'title': post.title,
        'slug': post.slug,
        'content': post.content, # Đảm bảo có trường này
        'image_url': post.image_url,
        'created_at': post.created_at.isoformat(),
        'updated_at': post.updated_at.isoformat() if post.updated_at else None,
        'author': { 
            'id': post.author.id,
            'username': post.author.username
        } if post.author else None,
        'is_featured': post.is_featured, 
        'is_latest': post.is_latest 
    }
    return jsonify(post_data), 200

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

@posts_bp.route('/posts', methods=['POST'])
@jwt_required()
def create_post():
    logger.info("--- Bắt đầu xử lý yêu cầu tạo bài viết mới ---")

    current_user_id = get_jwt_identity()
    logger.info(f"Người dùng hiện tại (ID): {current_user_id}")

    try:
        data = request.get_json()
        logger.info(f"Dữ liệu JSON nhận được: {data}")
    except Exception as e:
        logger.error(f"Lỗi khi parse JSON từ request: {e}")
        return jsonify({"msg": "Invalid JSON format"}), 400

    if not data:
        logger.warning("Không có dữ liệu JSON nào được cung cấp trong yêu cầu.")
        return jsonify({"msg": "No data provided"}), 400

    title = data.get('title')
    logger.info(f"Giá trị của 'title': {title}, kiểu dữ liệu: {type(title)}")
    if not title or not isinstance(title, str):
        logger.error(f"Lỗi xác thực: 'title' phải là một chuỗi không rỗng. Giá trị hiện tại: {title}, kiểu: {type(title)}")
        return jsonify({"msg": "Title must be a non-empty string"}), 422
    logger.info(f"Giá trị 'title' hợp lệ: '{title}'")

    content = data.get('content')
    logger.info(f"Giá trị của 'content': {content}, kiểu dữ liệu: {type(content)}")
    if not content or not isinstance(content, str):
        logger.error(f"Lỗi xác thực: 'content' phải là một chuỗi không rỗng. Giá trị hiện tại: {content}, kiểu: {type(content)}")
        return jsonify({"msg": "Content must be a non-empty string"}), 422
    logger.info(f"Giá trị 'content' hợp lệ: '{content}'")

    image_url = data.get('image_url')
    logger.info(f"Giá trị của 'image_url': {image_url}, kiểu dữ liệu: {type(image_url)}")
    
    slug = generate_slug(title)
    logger.info(f"Slug ban đầu được tạo: {slug}")

    existing_post = Post.query.filter_by(slug=slug).first()
    if existing_post:
        original_slug = slug
        slug = f"{slug}-{str(uuid.uuid4())[:8]}"
        logger.warning(f"Slug '{original_slug}' đã tồn tại. Tạo slug mới: '{slug}'")

    try:
        new_post = Post(title=title.strip(), slug=slug, content=content, image_url=image_url, author_id=current_user_id)
        db.session.add(new_post)
        db.session.commit()
        logger.info(f"Bài viết mới (ID: {new_post.id}, Slug: {new_post.slug}) đã được tạo thành công.")
        return jsonify({"msg": "Post created", "id": new_post.id, "slug": new_post.slug}), 201
    except Exception as e:
        db.session.rollback()
        logger.exception(f"Lỗi khi lưu bài viết vào cơ sở dữ liệu: {e}")
        return jsonify({"msg": f"Failed to create post due to database error: {str(e)}"}), 500
    
@posts_bp.route('/posts/<string:post_slug>', methods=['PUT'])
@jwt_required()
def update_post(post_slug):
    current_user_id = get_jwt_identity()
    post = Post.query.filter_by(slug=post_slug).first_or_404()

    
    if post.author_id != current_user_id: 
        return jsonify({"msg": "Unauthorized to update this post"}), 403

    data = request.get_json()
    post.title = data.get('title', post.title)
    post.content = data.get('content', post.content)
    post.image_url = data.get('image_url', post.image_url)
    post.is_featured = data.get('is_featured', post.is_featured)
    post.is_latest = data.get('is_latest', post.is_latest)

    if 'title' in data: 
        post.slug = generate_slug(post.title)
        

    db.session.commit()
    return jsonify({"msg": "Post updated"}), 200

@posts_bp.route('/posts/<int:post_id>', methods=['DELETE'])
@jwt_required()
def delete_post(post_id):
    current_user_id = get_jwt_identity()
    post = Post.query.get_or_404(post_id)

    # Ensure only the author or a super admin can delete
    if post.author_id != current_user_id: # Add check for is_admin if applicable
        return jsonify({"msg": "Unauthorized to delete this post"}), 403

    db.session.delete(post)
    db.session.commit()
    return jsonify({"msg": "Post deleted"}), 204

@posts_bp.route('/upload-image', methods=['POST'])
@jwt_required()
def upload_image():
    print("Request files:", request.files) 
    if 'file' not in request.files:
        return jsonify({"msg": "No file part"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"msg": "No selected file"}), 400
    if file:
        filename = str(uuid.uuid4()) + os.path.splitext(file.filename)[1] # Unique filename
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)
        # Return the URL relative to the Flask server base URL
        return jsonify({"image_url": f"/uploads/{filename}"}), 201
    return jsonify({"msg": "Upload failed"}), 500