import unittest

from app.models import User
from app import create_application,db
from app.config import TestingConfig

class UserTests(unittest.TestCase):

    def setUp(self):
        testApplication = create_application(TestingConfig)
        self.app_ctx = testApplication.app_context()
        self.app_ctx.push()
        db.create_all()
        return super().setUp()
    
    def addUser(self, username, password):
        user = User(username=username)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        return user

    def test_database_user_model(self):
        self.addUser("alice", "password123")
        self.assertIsNotNone(User.query.filter_by(username="alice").first())

    def test_password_check(self):
        user = self.addUser("bob", "secret")
        self.assertTrue(user.check_password("secret"))
        self.assertFalse(user.check_password("wrongpass"))

    def test_unique_username(self):
        self.addUser("alice", "password123")
        with self.assertRaises(Exception):
            self.addUser("alice", "anotherpassword")

    def test_password_is_hashed(self):
        user = self.addUser("charlie", "mypassword")
        # The hash should not be the plain password
        self.assertNotEqual(user.password_hash, "mypassword")
        # The hash should be a non-empty string
        self.assertIsInstance(user.password_hash, str)
        self.assertTrue(len(user.password_hash) > 0)
        # The hash should verify correctly
        self.assertTrue(user.check_password("mypassword"))
        self.assertFalse(user.check_password("wrongpassword"))

    def test_get_id_returns_string(self):
        user = self.addUser("dave", "pw")
        self.assertIsInstance(user.get_id(), str)

    def test_friendship_relationship(self):
        user1 = self.addUser("eve", "pw1")
        user2 = self.addUser("frank", "pw2")
        from app.models import Friendship
        friendship = Friendship(user_id=user1.id, friend_id=user2.id)
        db.session.add(friendship)
        db.session.commit()
        self.assertEqual(user1.sent_friendships.first().friend_id, user2.id)
        self.assertEqual(user2.received_friendships.first().user_id, user1.id)

    def test_game_result_relationship(self):
        user = self.addUser("grace", "pw")
        from app.models import GameResult
        result = GameResult(user_id=user.id, correct_color="red", selected_color="blue", is_correct=False, euclidean_distance=123.4)
        db.session.add(result)
        db.session.commit()
        self.assertEqual(user.game_results[0].correct_color, "red")

    def test_user_loader(self):
        user = self.addUser("henry", "pw")
        from app.models import load_user
        loaded = load_user(user.id)
        self.assertEqual(loaded.username, "henry")

    def test_user_deletion_cascades_friendships(self):
        #Tests that deleting a user also deletes their friendships
        user1 = self.addUser("alice", "pw1")
        user2 = self.addUser("bob", "pw2")
        from app.models import Friendship
        friendship = Friendship(user_id=user1.id, friend_id=user2.id)
        db.session.add(friendship)
        db.session.commit()
        db.session.delete(user1)
        db.session.commit()
        self.assertIsNone(Friendship.query.filter_by(user_id=user1.id).first())

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_ctx.pop()
        return super().tearDown()