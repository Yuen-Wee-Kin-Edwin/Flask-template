from src.app import app
from src.extensions import db
from src.entities.user import User

import src.entities
import logging

with app.app_context():
    try:
        db.create_all()
        app.logger.info("Database tables created or already exist")
        print("Tables created successfully")

        # Add dummy data
        if not User.query.first():
            dummy_user = User(name="Edwin")
            db.session.add(dummy_user)
            db.session.commit()
            app.logger.info("Dummy user added sucessfully")
            print("Dummy user added successfully")
        else:
            app.logger.info("Dummy user already exists")

    except Exception as e:
        logging.error(f"Error creating tables: {e}")