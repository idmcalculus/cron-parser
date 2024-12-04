import unittest
from src.parser import CronField, CronParser

class TestCronParser(unittest.TestCase):

	def setUp(self):
		"""Set up reusable instances or data for tests."""
		self.parser_valid = CronParser("*/15 0 1,15 * 1-5 /usr/bin/find")
		self.parser_single_value = CronParser("0 12 10 * * /run-me")
		self.parser_invalid_format = "*/15 0"

	# Test 1: Happy path with all valid fields and a command
	def test_happy_path(self):
		result = self.parser_valid.parse()
		expected = {
			"minute": [0, 15, 30, 45],
			"hour": [0],
			"day_of_month": [1, 15],
			"month": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
			"day_of_week": [1, 2, 3, 4, 5],
			"command": "/usr/bin/find"
		}
		self.assertEqual(result, expected)

	# Test 2: Single value in fields
	def test_single_value_fields(self):
		result = self.parser_single_value.parse()
		expected = {
			"minute": [0],
			"hour": [12],
			"day_of_month": [10],
			"month": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
			"day_of_week": [0, 1, 2, 3, 4, 5, 6],
			"command": "/run-me"
		}
		self.assertEqual(result, expected)

	# Test 3: Invalid format with too few fields
	def test_invalid_format(self):
		with self.assertRaises(ValueError):
			CronParser(self.parser_invalid_format).parse()

	# Test 4: Invalid field range, or invalid values e.g. negative values
	def test_invalid_field_range(self):
		invalid_cron_1 = "*/70 0 1 * * /run-me"
		invalid_cron_2 = "*/-15 0 1 * * /run-me-again"
		
		parser_1 = CronParser(invalid_cron_1)
		parser_2 = CronParser(invalid_cron_2)
		
		with self.assertRaises(ValueError) as context:
			parser_1.parse()
		
		with self.assertRaises(ValueError) as context:
			parser_2.parse()
			
		self.assertIn("Invalid value", str(context.exception))
	
	# Test 5: Valid range parsing
	def test_valid_range_parsing(self):
		cron = "1-5 * * * * /run-range"
		parser = CronParser(cron)
		result = parser.parse()
		self.assertEqual(result["minute"], [1, 2, 3, 4, 5])

	# Test 6: Valid step parsing
	def test_valid_step_parsing(self):
		cron = "*/20 * * * * /step-command"
		parser = CronParser(cron)
		result = parser.parse()
		self.assertEqual(result["minute"], [0, 20, 40])

	# Test 7: Format output test
	def test_format_output(self):
		result = self.parser_valid.format_output()
		expected_output = (
			"minute         0 15 30 45\n"
			"hour           0\n"
			"day of month   1 15\n"
			"month          1 2 3 4 5 6 7 8 9 10 11 12\n"
			"day of week    1 2 3 4 5\n"
			"command        /usr/bin/find"
		)
		self.assertEqual(result, expected_output)

	# Test 8: Handle empty cron string
	def test_empty_cron_string(self):
		with self.assertRaises(ValueError):
			CronParser("").parse()

	# Test 9: Handle wildcard-only cron string
	def test_wildcard_only(self):
		wildcard_cron = "* * * * * /wildcard"
		parser = CronParser(wildcard_cron)
		result = parser.parse()
		self.assertEqual(result["minute"], list(range(0, 60)))
		self.assertEqual(result["hour"], list(range(0, 24)))
		self.assertEqual(result["day_of_month"], list(range(1, 32)))
		self.assertEqual(result["month"], list(range(1, 13)))
		self.assertEqual(result["day_of_week"], list(range(0, 7)))
		self.assertEqual(result["command"], "/wildcard")


if __name__ == "__main__":
	unittest.main()