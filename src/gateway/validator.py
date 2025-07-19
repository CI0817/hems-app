import json
from pathlib import Path
from jsonschema import validate, ValidationError

class Validator:
    """
    A class to handle validation of JSON data against schemas.

    It automatically discovers and loads all JSON schemas from a given
    base directory, making it easy to validate incoming data from
    different devices.
    """
    def __init__(self, schema_base_path: str):
        """
        Initializes the Validator and loads all schemas.

        Args:
            schema_base_path: The file path to the root 'schemas' directory.
        """
        self.schemas = self._load_schemas(schema_base_path)
        print(f"Validator initialized. {len(self.schemas)} schemas loaded.")

    def _load_schemas(self, schema_base_path: str) -> dict:
        """
        Scans the schema directory and loads all .json files.

        It creates a dictionary where keys are derived from the file path
        (e.g., 'battery1/telemetry.v1') and values are the loaded
        JSON schema objects.

        Returns:
            A dictionary containing all the loaded schemas.
        """
        schemas = {}
        base_path = Path(schema_base_path)
        
        if not base_path.is_dir():
            print(f"Error: Schema directory not found at '{schema_base_path}'")
            return schemas

        # Find all .json files in the directory and its subdirectories
        for schema_file in base_path.rglob('*.json'):
            try:
                # Create a unique key for the schema based on its path
                # e.g., /path/to/schemas/battery1/telemetry.v1.json -> 'battery1/telemetry.v1'
                key = '/'.join(schema_file.with_suffix('').parts[len(base_path.parts):])
                
                with open(schema_file, 'r') as f:
                    schemas[key] = json.load(f)
                    
            except json.JSONDecodeError:
                print(f"Warning: Could not parse JSON from {schema_file}")
            except Exception as e:
                print(f"Warning: Could not load schema {schema_file}. Error: {e}")

        return schemas