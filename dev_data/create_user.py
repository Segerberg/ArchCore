from app import create_app, db
from app.models import User

# Create your application instance
app = create_app()

# Use the application context
with app.app_context():
    # Create a new user instance
    user = User(username='admin', email="admin@example.com")
    user.set_password('admin')

    # Add and commit the user to the database
    db.session.add(user)
    db.session.commit()
