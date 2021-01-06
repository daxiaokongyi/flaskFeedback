from models import User, Feedback,db
from app import app 

# Create all tables
db.drop_all()
db.create_all()

#Empty table if it is not empty
User.query.delete()

user1 = User.register("Jason", "abc", "1@gmail.com", "Jason", "Jin")
user2 = User.register("James", "123", "2@gmail.com", "James", "Li")
user3 = User.register("Grant", "123", "3@gmail.com", "Grant", "Zhao")
user4 = User.register("Cynthia", "123", "4@gmail.com", "Cynthia", "Zhu")
user5 = User.register("Sally", "123", "5@gmail.com", "Sally", "Kong")

feedback1 = Feedback(title = "first feedback", content = "first content", username = "Jason")

db.session.add_all([user1,user2,user3,user4,user5, feedback1])
db.session.commit()

