# Technical Task - Cron Expression Parser

---

## **Instructions**

Write a command line application or script that parses a cron string and expands each field to show the times at which it will run. You may use whichever language you feel most
comfortable with. The assignment must have an automated test suite.

Please do not use any existing cron parser libraries for this exercise. While using pre-built libraries is generally a good idea, we want to assess your ability to create your own!

You should only consider the standard cron format with five time fields (minute, hour, day of month, month, and day of week) plus a command, and you do not need to handle the special time strings such as "@yearly". The input will be on a single line.

The cron string will be passed to your application as a single argument.

```
~$ your-program "d"
```

The output should be formatted as a table with the field name taking the first 14 columns and the times as a space-separated list following it.

For example, the following input argument:

```
*/15 0 1,15 * 1-5 /usr/bin/find
```

Should yield the following output:

```
minute        0 15 30 45
hour          0
day of month  1 15
month         1 2 3 4 5 6 7 8 9 10 11 12
day of week   1 2 3 4 5
command       /usr/bin/find
```

---

## **My Implementation**

- Parses standard cron expressions with five time fields and a command.
- Handles wildcards (`*`), ranges (`-`), steps (`/`), and lists (`,`).
- Provides a detailed, table-like output for the parsed fields.
- Includes comprehensive error handling for invalid inputs.
- Automated test suite for happy and sad paths using Python's `unittest`.
- Leverages Python's `argparse` for improved command-line interface (CLI) usability.

---

## **Getting Started**

### **Requirements**

- Python 3.13+
- Unix environment

---

### **Installation**

1. Install Python 3.13+ locally

2. Activate the virtual environment (Optional, but recommended):
   ```bash
   source venv/bin/activate
   ```

---

### **Usage**
From the root directory, navigate to the `src` folder
```bash
cd src 
```

Then run the parser with the desired cron expression as a positional argument:
```bash
python main.py "<cron_expression>"
```

#### **Examples**
- Parse a cron job running every 15 minutes:
  ```bash
  python main.py "*/15 0 * * * /usr/bin/find"
  ```

- Parse a cron job running at midnight on the 1st and 15th of each month:
  ```bash
  python main.py "0 0 1,15 * * /usr/local/bin/backup"
  ```

- See usage help:
  ```bash
  python main.py --help
  ```

	The last command outputs the following:
	
	```plaintext
	usage: main.py [-h] cron_string
	
	A command-line utility to parse and expand cron expressions into a human-readable table.
	
	positional arguments:
	cron_string  The cron expression to be parsed. Example: '*/15 0 1,15 * 1-5 /usr/bin/find'
	
	optional arguments:
	-h, --help    show this help message and exit
	```

---

## **Testing**

### **Run Tests**
The application includes a `unittest` test suite to validate the parser's functionality.

To run the tests:
```bash
python -m unittest discover tests/
```

### **Test Cases**
The test suite covers:
- **Happy Paths**: Valid cron expressions with different combinations of wildcards, steps, ranges, and lists.
- **Sad Paths**: Invalid input formats, incorrect field ranges, and syntax errors.
- **Edge Cases**: Single values, wildcards, and commands.

---

## **Project Structure**

```plaintext
cron-parser/
-- venv/
   (directories and files for our virtual environment)
-- src/
   -- parser.py			# Script that expands and formats cron string
   -- main.py			# Script for parsing cron expressions
-- tests/
   -- test_parser.py	# Test cases for the parser
-- README.md			# Documentation
```

---

## **Assumptions and Limitations**

- The parser only supports the standard cron format (5 fields + command).
- Special strings like `@yearly`, `@monthly`, etc., are not supported.
- The `day of week` field assumes 0 = Sunday, 6 = Saturday.
