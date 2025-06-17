from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, Post, User  # Đổi từ .models thành models
import os
import uuid

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

@posts_bp.route('/posts', methods=['POST'])
@jwt_required()
def create_post():
    current_user_id = get_jwt_identity()
    # Check if current_user_id is an admin (you might add a 'is_admin' field to User model)
    # For now, we assume any logged in user can create.
    
    data = request.get_json()
    print("Received data:", data)

    if not data:
            return jsonify({"msg": "No data provided"}), 400
    
    title = data.get('title')
    if not title or not isinstance(title, str):
            return jsonify({"msg": "Title must be a non-empty string"}), 422
    
    content = data.get('content')
    if not content or not isinstance(content, str):
            return jsonify({"msg": "Content must be a non-empty string"}), 422
    image_url = data.get('image_url')
    
    if not title or not content:
        return jsonify({"msg": "Title and content are required"}), 400

    slug = generate_slug(title)
    if Post.query.filter_by(slug=slug).first():
        # Handle duplicate slug: append a unique identifier
        slug = f"{slug}-{str(uuid.uuid4())[:8]}"

    new_post = Post(title=title.strip(), slug=slug, content=content, image_url=image_url, author_id=current_user_id)
    db.session.add(new_post)
    db.session.commit()
    return jsonify({"msg": "Post created", "id": new_post.id, "slug": new_post.slug}), 201


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