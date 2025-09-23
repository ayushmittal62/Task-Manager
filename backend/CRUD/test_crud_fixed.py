from backend.db.database import Sessionlocal
from backend.CRUD import crud_operations as crud

db = Sessionlocal()

# First, check if users already exist
admin = crud.get_user_by_username(db, "admin1")
user = crud.get_user_by_username(db, "user1")

# Create users only if they don't exist
if not admin:
    admin = crud.create_user(db, "admin1", "pass123", role="admin")
    print("Created admin user:", admin.username)
else:
    print("Admin user already exists:", admin.username)

if not user:
    user = crud.create_user(db, "user1", "pass456", role="user")
    print("Created normal user:", user.username)
else:
    print("Normal user already exists:", user.username)

# 2. Create tasks
task1 = crud.create_task(db, "Finish report", "high", user.id)
task2 = crud.create_task(db, "Review PR", "medium", admin.id)
print("Created tasks:", task1.title, task2.title)

# 3. Get tasks
print("Admin can see:", [t.title for t in crud.get_all_tasks(db, admin)])
print("User can see:", [t.title for t in crud.get_all_tasks(db, user)])

# 4. Update task
updated = crud.update_task_admin_only(db, task1.id, user, status="completed")
print("Updated task:", updated.title if updated else "Failed to update")

db.close()