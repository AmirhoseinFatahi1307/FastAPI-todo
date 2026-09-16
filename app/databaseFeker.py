from core.database import SessionLocal
from sqlalchemy.orm import Session
from tasks.models import Task_models
from users.models import User_Model
from faker import Faker

fake = Faker()


def seed_users(db):
    user = User_Model(username=fake.user_name())
    user.set_password("1234")
    db.add(user)
    db.commit()
    db.refresh(user)
    print(f"user created with username {user.username} and id ={user.id}")
    return user


def seed_tasks(db, user, count=10):
    tasks_list = []
    for _ in range(count):
        tasks_list.append(
            Task_models(
                user_id=user.id,
                title=fake.sentence(nb_words=6),
                description=fake.text(),
                is_completed=fake.boolean(),
            )
        )
    db.add_all(tasks_list)
    db.commit()
    print(f"added 10 tasks for user id {user.id}")


def main():
    db = SessionLocal()
    try:
        user = seed_users(db)
        seed_tasks(db, user)
    finally:
        db.close()


if __name__ == "__main__":
    main()
