"""Module for window openers."""
from .command_send import CommandSend
from .exception import PyVLXException
from .node import Node
from .parameter import CurrentPosition, Position


class OpeningDevice(Node):
    """Meta class for opening device with one main parameter for position."""

    def __init__(self, pyvlx, node_id, name):
        """Initialize opening device."""
        super().__init__(pyvlx=pyvlx, node_id=node_id, name=name)
        self.position = Position()

    async def set_position(self, position):
        """Set window to desired position."""
        command_send = CommandSend(pyvlx=self.pyvlx, node_id=self.node_id, parameter=position)
        await command_send.do_api_call()
        if not command_send.success:
            raise PyVLXException("Unable to send command")
        await self.after_update()

    async def open(self):
        """Open window."""
        await self.set_position(Position(position_percent=0))

    async def close(self):
        """Close window."""
        await self.set_position(Position(position_percent=100))

    async def stop(self):
        """Stop window."""
        await self.set_position(CurrentPosition())


class Window(OpeningDevice):
    """Window object."""

    def __init__(self, pyvlx, node_id, name, rain_sensor=False):
        """Initialize Window class."""
        super().__init__(pyvlx=pyvlx, node_id=node_id, name=name)
        self.rain_sensor = rain_sensor

    def __str__(self):
        """Return object as readable string."""
        return '<{} name="{}" ' \
            'node_id="{}" rain_sensor={}/>' \
            .format(
                type(self).__name__,
                self.name,
                self.node_id, self.rain_sensor)


class Blind(OpeningDevice):
    """Blind objects."""


class RollerShutter(OpeningDevice):
    """RollerShutter object."""
