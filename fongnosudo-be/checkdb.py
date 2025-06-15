from app import create_app
from models import db, Post, User
from sqlalchemy import inspect, text
import os

def get_table_columns(engine, table_name):
    """Lấy danh sách columns của table"""
    inspector = inspect(engine)
    if table_name in inspector.get_table_names():
        columns = inspector.get_columns(table_name)
        return {col['name']: col for col in columns}
    return {}

def get_model_columns(model):
    """Lấy danh sách columns từ SQLAlchemy model"""
    columns = {}
    for column_name in model.__table__.columns.keys():
        column = model.__table__.columns[column_name]
        columns[column_name] = {
            'name': column_name,
            'type': str(column.type),
            'nullable': column.nullable,
            'primary_key': column.primary_key,
            'unique': getattr(column, 'unique', False)
        }
    return columns

def compare_columns(existing_cols, model_cols):
    """So sánh columns giữa database và model"""
    missing_columns = []
    
    for col_name, col_info in model_cols.items():
        if col_name not in existing_cols:
            missing_columns.append((col_name, col_info))
        else:
            # Có thể thêm logic để so sánh type, constraints, etc.
            pass
    
    return missing_columns

def add_missing_columns(engine, table_name, missing_columns):
    """Thêm columns thiếu vào table"""
    with engine.connect() as conn:
        for col_name, col_info in missing_columns:
            # Tạo SQL để thêm column
            column_type = col_info['type']
            nullable = "NULL" if col_info['nullable'] else "NOT NULL"
            
            # Xử lý một số type đặc biệt
            if 'VARCHAR' in column_type.upper():
                sql_type = column_type
            elif 'INTEGER' in column_type.upper():
                sql_type = 'INTEGER'
            elif 'BOOLEAN' in column_type.upper():
                sql_type = 'BOOLEAN'
            elif 'DATETIME' in column_type.upper():
                sql_type = 'TIMESTAMP'
            elif 'TEXT' in column_type.upper():
                sql_type = 'TEXT'
            else:
                sql_type = column_type
            
            # Tạo default value cho NOT NULL columns
            default_value = ""
            if not col_info['nullable']:
                if 'INTEGER' in sql_type.upper():
                    default_value = " DEFAULT 0"
                elif 'BOOLEAN' in sql_type.upper():
                    default_value = " DEFAULT FALSE"
                elif 'VARCHAR' in sql_type.upper() or 'TEXT' in sql_type.upper():
                    default_value = " DEFAULT ''"
                elif 'TIMESTAMP' in sql_type.upper():
                    default_value = " DEFAULT CURRENT_TIMESTAMP"
            
            alter_sql = f"ALTER TABLE {table_name} ADD COLUMN {col_name} {sql_type}{default_value} {nullable}"
            
            try:
                print(f"Adding column: {alter_sql}")
                conn.execute(text(alter_sql))
                conn.commit()
                print(f"✅ Successfully added column '{col_name}' to table '{table_name}'")
            except Exception as e:
                print(f"❌ Error adding column '{col_name}': {str(e)}")
                conn.rollback()

def migrate_database():
    app = create_app()
    
    with app.app_context():
        print("🔍 Checking database schema...")
        
        # Kiểm tra xem database connection có hoạt động không
        try:
            inspector = inspect(db.engine)
            existing_tables = inspector.get_table_names()
            print(f"📊 Found existing tables: {existing_tables}")
        except Exception as e:
            print(f"❌ Database connection error: {e}")
            return
        
        # Dictionary chứa các models cần kiểm tra
        models_to_check = {
            'user': User,
            'post': Post
        }
        
        tables_created = []
        columns_added = []
        
        for table_name, model in models_to_check.items():
            print(f"\n🔍 Checking table '{table_name}'...")
            
            # Kiểm tra xem table có tồn tại không
            if table_name not in existing_tables:
                print(f"❌ Table '{table_name}' does not exist. Creating...")
                try:
                    # Tạo table
                    model.__table__.create(db.engine)
                    tables_created.append(table_name)
                    print(f"✅ Successfully created table '{table_name}'")
                except Exception as e:
                    print(f"❌ Error creating table '{table_name}': {str(e)}")
                    continue
            else:
                print(f"✅ Table '{table_name}' exists")
                
                # Kiểm tra columns
                existing_cols = get_table_columns(db.engine, table_name)
                model_cols = get_model_columns(model)
                missing_columns = compare_columns(existing_cols, model_cols)
                
                if missing_columns:
                    print(f"❌ Missing columns in '{table_name}': {[col[0] for col in missing_columns]}")
                    add_missing_columns(db.engine, table_name, missing_columns)
                    columns_added.extend([f"{table_name}.{col[0]}" for col in missing_columns])
                else:
                    print(f"✅ All columns exist in table '{table_name}'")
        
        # Tạo admin user nếu chưa có
        print(f"\n👤 Checking admin user...")
        admin_user = User.query.filter_by(username='admin').first()
        if not admin_user:
            try:
                admin_user = User(username='admin')
                admin_user.set_password('admin123')
                db.session.add(admin_user)
                db.session.commit()
                print("✅ Created admin user (username: admin, password: admin123)")
            except Exception as e:
                print(f"❌ Error creating admin user: {str(e)}")
                db.session.rollback()
        else:
            print("✅ Admin user already exists")
        
        # Tóm tắt kết quả
        print(f"\n📋 Migration Summary:")
        print(f"   • Tables created: {len(tables_created)} - {tables_created}")
        print(f"   • Columns added: {len(columns_added)} - {columns_added}")
        print(f"✅ Database migration completed!")

if __name__ == '__main__':
    migrate_database()