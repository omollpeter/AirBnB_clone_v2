import unittest
from unittest.mock import patch
from io import StringIO
from console import HBNBCommand
from models import storage
from pathlib import Path
import json


class TestHBNBConsole(unittest.TestCase):
    def test_create_with_params(self):
        with patch("sys.stdout", new=StringIO()) as f:
            HBNBCommand().onecmd('create State name="Arizona"')

        result = f.getvalue().strip()
        expected = 36
        self.assertEqual(len(result), expected)
