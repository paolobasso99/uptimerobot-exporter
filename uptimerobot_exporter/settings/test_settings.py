import os
import unittest

from . import Settings


class TestSettings(unittest.TestCase):
    """Test class for Settings"""

    def setUp(self):
        """Set up envirorment variables"""
        os.environ["LOG_LEVEL"] = "CRITICAL"
        os.environ["INTERVAL_SECONDS"] = "200"
        os.environ["PORT"] = "8080"
        os.environ["UPTIMEROBOT_READ_API_KEY"] = "api-keey"

    def test_defaults(self):
        """Test that the defaults work correctly"""

        settings = Settings()
        settings.DEFAULT = {
            "PORT": 1111,
            "INTERVAL_SECONDS": 600,
            "LOG_LEVEL": "CRITICAL"
        }
        settings.reset_default()

        self.assertEqual(settings.get("LOG_LEVEL"),
                         "CRITICAL", "Should be CRITICAL")
        self.assertEqual(settings.get("INTERVAL_SECONDS"),
                         600, "Should be 200")
        self.assertEqual(settings.get("PORT"), 1111, "Should be 8080")
        self.assertEqual(settings.get("UPTIMEROBOT_READ_API_KEY"),
                         "api-keey", "Should be api-keey")

    def test_env(self):
        """Test that envirorment variables are used correctly"""

        settings = Settings()
        self.assertEqual(settings.get("LOG_LEVEL"),
                         "CRITICAL", "Should be CRITICAL")
        self.assertEqual(settings.get("INTERVAL_SECONDS"),
                         200, "Should be 200")
        self.assertEqual(settings.get("PORT"), 8080, "Should be 8080")
        self.assertEqual(settings.get("UPTIMEROBOT_READ_API_KEY"),
                         "api-keey", "Should be api-keey")

    def test_wrong_env(self):
        """Test what happens when env vars are invalid"""
        
        settings = Settings()
        settings.reset_default()

        # Empty LOG_LEVEL
        del os.environ["LOG_LEVEL"]
        settings.load_log_level()
        self.assertEqual(settings.get("LOG_LEVEL"), "INFO",
                         "Should be the default value (INFO)")

        # Wrong LOG_LEVEL
        os.environ["LOG_LEVEL"] = "CRITICAL1"
        settings.load_log_level()
        self.assertEqual(settings.get("LOG_LEVEL"), "INFO",
                         "Should be the default value (INFO)")

        # Wrong INTERVAL_SECONDS
        os.environ["INTERVAL_SECONDS"] = "-2"
        with self.assertRaises(ValueError):
            settings.load_interval_seconds()

        # Wrong PORT
        os.environ["PORT"] = "-2"
        with self.assertRaises(ValueError):
            settings.load_port()

        # Empty UPTIMEROBOT_READ_API_KEY
        del os.environ["UPTIMEROBOT_READ_API_KEY"]
        with self.assertRaises(ValueError):
            settings.load_port()


if __name__ == '__main__':
    unittest.main()
