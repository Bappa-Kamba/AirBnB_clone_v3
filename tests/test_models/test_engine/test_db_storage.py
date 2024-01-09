#!/usr/bin/python3
"""
Contains the TestDBStorageDocs and TestDBStorage classes
"""

from datetime import datetime
import inspect
import models
from models.engine import db_storage
from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
import json
import os
import pep8
import unittest
DBStorage = db_storage.DBStorage
classes = {"Amenity": Amenity, "City": City, "Place": Place,
           "Review": Review, "State": State, "User": User}


class TestDBStorageDocs(unittest.TestCase):
    """Tests to check the documentation and style of DBStorage class"""
    @classmethod
    def setUpClass(cls):
        """Set up for the doc tests"""
        cls.dbs_f = inspect.getmembers(DBStorage, inspect.isfunction)

    def test_pep8_conformance_db_storage(self):
        """Test that models/engine/db_storage.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['models/engine/db_storage.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_pep8_conformance_test_db_storage(self):
        """Test tests/test_models/test_db_storage.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['tests/test_models/test_engine/\
test_db_storage.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_db_storage_module_docstring(self):
        """Test for the db_storage.py module docstring"""
        self.assertIsNot(db_storage.__doc__, None,
                         "db_storage.py needs a docstring")
        self.assertTrue(len(db_storage.__doc__) >= 1,
                        "db_storage.py needs a docstring")

    def test_db_storage_class_docstring(self):
        """Test for the DBStorage class docstring"""
        self.assertIsNot(DBStorage.__doc__, None,
                         "DBStorage class needs a docstring")
        self.assertTrue(len(DBStorage.__doc__) >= 1,
                        "DBStorage class needs a docstring")

    def test_dbs_func_docstrings(self):
        """Test for the presence of docstrings in DBStorage methods"""
        for func in self.dbs_f:
            self.assertIsNot(func[1].__doc__, None,
                             "{:s} method needs a docstring".format(func[0]))
            self.assertTrue(len(func[1].__doc__) >= 1,
                            "{:s} method needs a docstring".format(func[0]))


class TestDBStorage(unittest.TestCase):
    """Test the FileStorage class"""

    def setUp(self):
        """Set up for the tests"""
        # Get the database name from environment variable
        self.HBNB_MYSQL_USER = os.getenv('HBNB_MYSQL_USER')
        self.HBNB_MYSQL_PWD = os.getenv('HBNB_MYSQL_PWD')
        self.HBNB_MYSQL_HOST = os.getenv('HBNB_MYSQL_HOST')
        self.HBNB_MYSQL_DB = os.getenv('HBNB_MYSQL_DB')
        self.HBNB_ENV = os.getenv('HBNB_ENV')

        self.storage = models.storage
        self.storage.reload()  # Connect to the database

        # Insert some test data
        for i in range(10):
            state = State(name=f"State{i}")
            self.storage.new(state)
        self.storage.save()

    def tearDown(self):
        """Clean up after tests"""
        self.storage = models.storage
        for obj in self.storage.all().values():
            self.storage.delete(obj)
        self.storage.save()

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_all_returns_dict(self):
        """Test that all returns a dictionaty"""
        self.assertIs(type(models.storage.all()), dict)

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_all_no_class(self):
        """Test that all returns all rows when no class is passed"""

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_new(self):
        """test that new adds an object to the database"""

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_save(self):
        """Test that save properly saves objects to file.json"""

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_count_all_objects(self):
        """Test counting all objects in storage"""
        # Add some objects to storage
        expected_count = 10  # Example value, replace with the actual expected count
        count = self.storage.count(State)
        self.assertEqual(count, expected_count)

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_count_objects_by_class(self):
        """Test counting objects of a specific class in storage"""
        # Add some objects to storage
        # ...
        SomeClass = State  # Replace with the actual class you want to test
        expected_count = 5  # Example value, replace with the actual expected count
        count = self.storage.count(cls=SomeClass)
        self.assertEqual(count, expected_count)

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_count_invalid_class(self):
        """Test counting objects with an invalid class"""
        InvalidClass = InvalidClass  # Replace with the actual invalid class you want to test
        count = self.storage.count(cls=InvalidClass)
        self.assertEqual(count, 0)
