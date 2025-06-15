from flask import Flask, jsonify, send_from_directory
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from config import Config
from models import db
from auth import auth_bp
from routes import posts_bp, UPLOAD_FOLDER
from sqlalchemy import inspect

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)
    jwt = JWTManager(app)
    CORS(app)

    # Register blueprints
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(posts_bp, url_prefix='/api')

    # Serve uploaded images
    @app.route('/uploads/<path:filename>')
    def uploaded_file(filename):
        return send_from_directory(UPLOAD_FOLDER, filename)

    with app.app_context():
        # Kiểm tra xem tables đã tồn tại chưa
        inspector = inspect(db.engine)
        existing_tables = inspector.get_table_names()
        
        # Chỉ tạo tables nếu chưa có
        if not existing_tables or 'user' not in existing_tables or 'post' not in existing_tables:
            print("Creating database tables...")
            db.create_all()
            print("Database tables created successfully!")
        else:
            print("Database tables already exist, skipping creation.")

        # Tạo admin user nếu chưa có
        from models import User
        import os
        admin = os.getenv("USER_ADMIN")
        password = os.getenv("USER_ADMIN_PASSWORD")
        if not User.query.filter_by(username=admin).first():
            admin_user = User(username=admin)
            admin_user.set_password(password)
            db.session.add(admin_user)
            db.session.commit()
            print(f"Default admin user '{admin}' created with password '{password}'")
        else:
            print("Admin user already exists.")

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)