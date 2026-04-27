# File: src/app/models.py
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = "users"

    # Define the schema columns.
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(
        db.Enum("ADMIN", "USER", name="user_role", create_type=False),
        nullable=False,
        default="USER",
    )
    active = db.Column(db.Boolean, nullable=False, default=True)

    def __repr__(self):
        # Provide a human-readable representation of the object for debugging.
        return f"<User {self.email}>"
