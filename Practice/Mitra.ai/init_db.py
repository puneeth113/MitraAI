from database import create_tables, add_user

create_tables()

# create default admin
add_user("admin", "admin123", "admin")

print("Database initialized successfully")