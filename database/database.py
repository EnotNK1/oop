from psycopg2 import Error
from sqlalchemy import Integer, String, create_engine, select, func
from sqlalchemy.orm import sessionmaker, joinedload
from database.models import Base, Users, Word
import uuid

engine = create_engine(url="sqlite:///db.db", echo=False)

session_factory = sessionmaker(engine)


class DatabaseService:
    def create_tables(self):
        # Base.metadata.drop_all(engine)
        Base.metadata.create_all(engine)

    def register_user(self, email, password):
        with session_factory() as session:
            try:
                user = Users(email=email,
                             password=password,
                             )
                session.add(user)
                session.commit()
                return 0
            except (Exception, Error) as error:
                # print(error)
                return -1

    def check_user(self, email, password):
        with session_factory() as session:
            try:
                user = session.query(Users).filter_by(email=email).one()
                pas = user.password

                if pas == password:
                    return 0
                else:
                    return -1

            except (Exception, Error) as error:
                # print(error)
                return -1

    def add_phrase(self, user_email, word, translate):
        with session_factory() as session:
            try:
                word = Word(id=uuid.uuid4(),
                            word=word,
                            translate=translate,
                            user_email=user_email)
                session.add(word)
                session.commit()
                return 0
            except (Exception, Error) as error:
                # print(error)
                return -1

    def check_phrase(self, user_email, word, translate):
        with session_factory() as session:
            try:
                phrase = session.query(Word).filter_by(word=word, translate=translate, user_email=user_email).one()
                if phrase:
                    return 1
                return 0
            except (Exception, Error) as error:
                # print(error)
                return -1

    def get_words(self, user_email):
        with session_factory() as session:
            try:
                phrase = session.query(Word).filter_by(user_email=user_email).all()
                list = []
                for obj in phrase:
                    list.append(obj.word)
                    list.append(obj.translate)
                return list
            except (Exception, Error) as error:
                # print(error)
                return -1

    def get_password_user(self, email):
        with session_factory() as session:
            try:
                user = session.get(Users, email)
                return user.password

            except (Exception, Error) as error:
                # print(error)
                return -1

    def set_password_user(self, email, new_pas):
        with session_factory() as session:
            try:
                user = session.get(Users, email)
                user.password = new_pas
                session.commit()
                return 1

            except (Exception, Error) as error:
                # print(error)
                return -1

    def delete_pharse_db(self, email, phrase, translate):
        with session_factory() as session:
            try:
                phrase = session.query(Word).filter_by(user_email=email, word=phrase, translate=translate).first()
                session.delete(phrase)
                session.commit()
                return 1
            except (Exception, Error) as error:
                # print(error)
                return -1




database_service = DatabaseService()

database_service.create_tables()
