import unittest

from sqlalchemy import Column, Integer, String, insert, bindparam
from sqlalchemy.orm import Session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.exc import ArgumentError, InvalidRequestError

from common.db.postgres import start_postgres, stop_postgres
from common.db.db import engine, postgres_session_maker
from common.db.crud import clear_table

Base = declarative_base()


class TestPostgresBasic(unittest.TestCase):
    TEST_NAME_OF_ITEM = "BOOK"

    session: Session

    def test_base_model_without_tablename(self):
        with self.assertRaises(InvalidRequestError):
            class D(Base):
                id = Column(Integer, primary_key=True, autoincrement=True, unique=True, nullable=False)
                name = Column(String, unique=True, nullable=False)

    def test_base_model_without_primary_key(self):
        with self.assertRaises(ArgumentError):
            class A(Base):
                __tablename__ = "as"
                id = Column(Integer, primary_key=False, autoincrement=True, unique=True, nullable=False)
                name = Column(String, unique=True, nullable=False)

    def test_query(self):
        result = self.session.query(Item).all()
        self.assertEqual(len(result), 0)

    def test_query_with_simple_class(self):
        class A:
            name: str

        with self.assertRaises(ArgumentError):
            self.session.query(A).all()

    def test_query_with_class_with_columns(self):
        class A:
            id = Column(Integer, primary_key=True, autoincrement=True, unique=True, nullable=False)
            name = Column(String, unique=True, nullable=False)

        with self.assertRaises(ArgumentError):
            self.session.query(A).all()

    def test_insert_one(self):
        stmt = (insert(Item).values(name=self.TEST_NAME_OF_ITEM))
        self.session.execute(stmt)
        self.session.commit()

        result = self.session.query(Item).all()
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].name, self.TEST_NAME_OF_ITEM)

    def test_insert_one_with_param(self):
        stmt = (insert(Item).values(name=bindparam("name")))
        self._execute_insert(stmt)
        self._check_insert()

    def test_insert_one_via_force_param(self):
        stmt = (insert(Item))
        self._execute_insert(stmt)
        self._check_insert()

    def _execute_insert(self, stmt):
        self.session.execute(
            stmt,
            [
                {"name": self.TEST_NAME_OF_ITEM}
            ]
        )
        self.session.commit()

    def _check_insert(self):
        result = self.session.query(Item).all()
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].name, self.TEST_NAME_OF_ITEM)

    def test_override_stmt_values(self):
        stmt = (insert(Item).values(name=self.TEST_NAME_OF_ITEM))
        self.session.execute(
            stmt,
            [
                {"name": "Override"}
            ]
        )

        result = self.session.query(Item).all()
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].name, "Override")

    def test_insert_many_via_loop(self):
        stmt = insert(Item)

        for i in range(100):
            self.session.execute(
                stmt,
                [
                    {"name": f"Create{i}"}
                ]
            )
        self.session.commit()

        result = self.session.query(Item).all()
        self.assertEqual(len(result), 100)
        self.assertEqual(result[-1].name, "Create99")

    def setUp(self):
        super().setUp()
        self.session = postgres_session_maker()

    def tearDown(self):
        super().tearDown()
        clear_table(Item, session=self.session)
        self.session.close()

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        start_postgres()
        Base.metadata.create_all(engine)

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        stop_postgres()


class Item(Base):
    __tablename__ = "items"
    id = Column(Integer, primary_key=True, autoincrement=True, unique=True, nullable=False)
    name = Column(String, unique=True, nullable=False)
