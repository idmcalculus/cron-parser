from typing import List, Dict, Union

class CronField:
	"""Represents a single field in a cron expression"""
	def __init__(self, min_val: int, max_val: int, name: str):
		# Define the minimum and maximum valid values for a field
		self.min_val = min_val
		self.max_val = max_val
		self.name = name
		
	def validate_value(self, value: str) -> bool:
		"""Checks if a value is within the allowed range"""
		try:
			num = int(value) # Convert the value to an integer
			return self.min_val <= num <= self.max_val
		except ValueError:
			return False
			
class CronParser:
	"""Parses and expands a full cron expression"""
	# Define the valid fields using CronField objects
	FIELDS = {
		"minute": CronField(0, 59, "minute"),
		"hour": CronField(0, 23, "hour"),
		"day_of_month": CronField(1, 31, "day of month"),
		"month": CronField(1, 12, "month"),
		"day_of_week": CronField(0, 6, "day of week")
	}
	
	def __init__(self, input_string: str):
		# print(f"input string {input_string}")
		
		self.cron_string = input_string.strip() # Store the cron string after removing leading/trailing whitespace
		self.parts = self.cron_string.split() # Split the cron string into parts (fields and command)
		
		# print(f"input string parts array {self.parts}")
		
		# Ensure the cron string has at least 6 components (5 fields + command)
		if len(self.parts) < 6:
			raise ValueError("Invalid input string format. Expected 6 space-separated fields.")
			
		self.cron_fields = self.parts[:5] # Slice the first five parts, these are the cron fields
		self.command = " ".join(self.parts[5:]) # everything else is the command
		
		# print(f"cron fields array {self.cron_fields}")
		
	def expand_field(self, field: str, cron_field: CronField) -> List[int]:
		"""Expands a cron field into a list of values"""
		# print(f"field value {field}")
		
		result = []
		
		# Handle the wildcard "*" by returning the full range
		if field == "*":
			return list(range(cron_field.min_val, cron_field.max_val + 1))
		
		# Split the field by "," to handle multiple parts if applicable (e.g., "1,15,30")
		for part in field.split(","):
			if "/" in part: # Handle step values (e.g. "*/15" or '1/5')
				base, step = part.split("/") # Split part into 2, and unpack their values to base and step respectively
				
				if not cron_field.validate_value(step):
					raise ValueError(f"Invalid value: {step}")
				
				step = int(step) # Convert string step to integer
				
				# Step values must be positive
				if step <= 0:
					raise ValueError(f"Step value must be positive: {step}")
				
				# Handle the wildcard '*' or a specific base value
				base_range = (list(range(cron_field.min_val, cron_field.max_val + 1)) if base == "*" else [int(base)])
				
				result.extend(range(base_range[0], cron_field.max_val + 1, step)) # Add the range to the result array
			elif "-" in part: # Handle ranges (e.g. "1-5")
				start, end = map(int, part.split("-")) # Split part into 2, map the resulting strings into integers, and unpack their values to start and end respectively
				# Check that the start and end of the range are within allowed limits
				if not (cron_field.validate_value(str(start)) and cron_field.validate_value(str(end))):
					raise ValueError(f"Invalid range {part} for {cron_field.name}")
				
				result.extend(range(start, end + 1)) # Add the range to the result array
			else: # Handle individual values (e.g. '15')
				# Check that part is a valid value
				if not cron_field.validate_value(part):
					raise ValueError(f"Invalid value {part} for {cron_field.name}")
				
				result.append(int(part)) # Add part to the result array
				
		return sorted(set(result)) # Return the sorted, unique values
		
	def parse(self) -> Dict[str, Union[List[int], str]]:
		"""Parses the cron expression and returns expanded fields"""
		result = {}
		
		# Iterate through the fields and expand each using the corresponding CronField object
		for field_value, (field_name, field_obj) in zip(self.cron_fields, self.FIELDS.items()):
			try:
				result[field_name] = self.expand_field(field_value, field_obj)
			except ValueError as e: # Raise an error if any field is invalid
				raise ValueError(f"Error parsing {field_obj.name}: {str(e)}")
			
		result["command"] = self.command
		return result
		
	def format_output(self) -> str:
		"""Formats the parsed fields into a table-like string"""
		expanded = self.parse() # Parse and expand the fields
		output = []
		
		column_width = 14 # Set a consistent column width for alignment
		
		# Format each field and its values as a table row
		for field_name, field_obj in self.FIELDS.items():
			values = expanded[field_name]
			output.append(f"{field_obj.name:<{column_width}} {' '.join(map(str, values))}")
		
		# Add the command as the last row
		output.append(f"{'command':<{column_width}} {expanded['command']}")
		return "\n".join(output) # Join rows with newline characters