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
    
    def validate_message(self, topic: str, data: dict) -> bool:
        """
        Validates a data payload based on its MQTT topic.

        It extracts the device, message type, and version from the topic to 
        find the correct schema.

        Args:
            topic: The MQTT topic, e.g., 'home1/battery1/telemetry/v1'.
            data: The JSON data payload (as a Python dictionary).

        Returns:
            True if the data is valid, False otherwise.
        """
        try:
            # Extract the parts from the topic string to build the schema key
            # e.g., 'home1/battery1/telemetry/v1' -> ['home1', 'battery1', 'telemetry', 'v1']
            parts = topic.strip('/').split('/')
            
            # The topic must have 4 parts: home/device/type/version
            if len(parts) < 4:
                print(f"Invalid topic format: {topic}. Expected '<home>/<device>/<type>/<version>'.")
                return False

            device = parts[1]       # e.g., 'battery1'
            message_type = parts[2] # e.g., 'telemetry'
            version = parts[3]      # e.g., 'v1'
            
            # Construct the schema key from the topic parts
            # e.g., 'battery1/telemetry.v1'
            schema_key = f"{device}/{message_type}.{version}"

            # Find the correct schema in our loaded schemas
            schema = self.schemas.get(schema_key)

            if not schema:
                print(f"Validation failed: No schema found for key '{schema_key}' from topic '{topic}'")
                return False

            # The 'validate' function will raise a ValidationError if the data is invalid
            validate(instance=data, schema=schema)
            print(f"Data for topic '{topic}' is valid.")
            return True

        except ValidationError as e:
            # The data did not match the schema
            print(f"Validation failed for topic '{topic}'")
            print(f"   Error: {e.message} in '{'.'.join(str(p) for p in e.path)}'")
            return False
        except Exception as e:
            # Handle other potential errors, like a malformed topic
            print(f"An unexpected error occurred during validation for topic '{topic}': {e}")
            return False