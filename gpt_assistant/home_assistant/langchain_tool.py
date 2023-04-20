from langchain.tools.base import BaseModel
from typing import List
import json

import gpt_assistant.home_assistant.api as api


class HomeAssistantProcessor(BaseModel):

    def command_info(self, commands: str) -> str:
        """Extracts entity_id, device_class, status, and friendly_name from a string of commands in JSON format."""
        commands = json.loads(commands)
        if len(commands) != 4:
            return None

        entity_id, device_class, status, friendly_name = list(
            map(lambda x: x.strip().lower(), commands))
        return entity_id, device_class, status, friendly_name

    def validate_device(self, entity_id: str) -> str:
        """Validates whether a device with the given entity_id exists in the list of devices retrieved from Home Assistant API."""
        devices = api.get_devices()

        # Find the device form the list of devices
        device = None
        for d in devices:
            if d['entity_id'] == entity_id:
                device = d
                break

        return device

    def run(self, commands: str) -> str:
        """Toggles the state of a device with the given entity_id to the specified status."""
        commands = self.command_info(commands)
        entity_id, device_class, status, friendly_name = commands

        # Find the device form the list of devices
        device = self.validate_device(entity_id)

        if device is None:
            return f'Failed to toggle the switch, do not proceed to other action, give final answer now. Response "Sorry, I cannot find the device {friendly_name}"'

        if api.toggle_device_state(entity_id, device_class, status):
            return f"Successfully toggle the {friendly_name} to {status}, give final answer now, do not mention how and entity_id"
        else:
            return f"Failed to toggle the {friendly_name}"

    def read(self, commands: str) -> str:
        """Returns the current state of a device with the given entity_id."""
        commands = json.loads(commands)
        if len(commands) != 3:
            return None

        entity_id, _, friendly_name = list(
            map(lambda x: x.strip().lower(), commands))

        # Find the device form the list of devices
        device = self.validate_device(entity_id)

        if device is None:
            return f'Failed to read the state of the device, do not proceed to other action, give final answer now. Response "Sorry, I cannot find the device {friendly_name}"'

        return f"The current state of {friendly_name} is {device['state']}, give final answer, do not reply with entity_id"

    def read_sensor(self, commands: str) -> str:
        """Returns the current state of a sensor with the given entity_id."""
        commands = json.loads(commands)
        if len(commands) != 3:
            return None

        entity_id, _, friendly_name = list(
            map(lambda x: x.strip().lower(), commands))

        # Find the device form the list of devices
        device = self.validate_device(entity_id)

        if device is None:
            return f'Cannot find the sensor {friendly_name}"'

        return f"The current state of {friendly_name} is {device['state']}, give final answer, do not reply with entity_id"

    def discover(self, *args) -> str:
        """Discovers devices by retrieving the list of devices from Home Assistant API."""
        print(f"\rDiscovering the device")
        try:
            devices = api.get_devices()
        except ConnectionError as e:
            return "Failed to get home devices, process to default action"
        return devices
