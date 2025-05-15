import unittest
from datetime import datetime, timezone
from werkzeug.security import generate_password_hash
from sqlalchemy.exc import IntegrityError
from app import create_app
from config import TestingConfig
from app.extensions import db
from app.models.user import User

class UserModelTestCase(unittest.TestCase):
    def setUp(self):
        # Initialize test app with TestingConfig
        self.app = create_app(TestingConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        # Clean up after each test
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_user_creation(self):
        print("=== Test 1: Admin user creation started ===")
        user = User(
            email="admin@outlook.com",
            password_hash=generate_password_hash("13579"),
            role="Admin",
            full_name="Alice Admin",
            education="BSc in Information Systems",
            experience="System administrator and coordinator",
            bio="Manages platform access and permissions.",
            phone="0400 000 006",
            register_time=datetime.now(timezone.utc)
        )

        db.session.add(user)
        db.session.commit()
        print("User inserted into the database. Now verifying...")

        queried = User.query.filter_by(email="admin@outlook.com").first()
        self.assertIsNotNone(queried, "User should exist in the database")
        self.assertEqual(queried.role, "Admin", "User role should be 'Admin'")
        self.assertEqual(queried.full_name, "Alice Admin", "Full name does not match")
        self.assertEqual(queried.phone, "0400 000 006", "Phone number does not match")

        print("=== Test 1 passed: Admin user successfully created and verified ===\n")

    def test_user_duplicate_email(self):
        print("=== Test 2: Duplicate email insertion started ===")
        user1 = User(
            email="duplicate@example.com",
            password_hash=generate_password_hash("123456"),
            role="Guardian",
            full_name="First User",
            register_time=datetime.now(timezone.utc)
        )
        db.session.add(user1)
        db.session.commit()
        print("First user inserted successfully.")

        user2 = User(
            email="duplicate@example.com",  # same email
            password_hash=generate_password_hash("654321"),
            role="Support Worker",
            full_name="Second User",
            register_time=datetime.now(timezone.utc)
        )
        db.session.add(user2)

        try:
            db.session.commit()
            print(" Test 2 failed: Duplicate email inserted without error.")
            self.fail("Duplicate email should raise an IntegrityError")
        except IntegrityError:
            db.session.rollback()
            print(" Test 2 passed: Duplicate email insertion correctly raised IntegrityError.\n")
