import asyncio
from goodwe.protocol import *
from asyncio.futures import Future

class VProtocol(InverterProtocol):
    def __init__(self, vmem):
        self._vmem = vmem

    async def send_request(self, command: ProtocolCommand) -> Future:
        #print(f"[d] Sending command: {command}")
        nregs = command.value
        data = bytearray(5 + nregs*2)
        for i in range(nregs):
            if word := self._vmem.read_word(command.first_address + i):
                data[5 + i*2]   = (word >> 8) & 0xFF
                data[5 + i*2+1] = word & 0xFF
        response_future = asyncio.get_running_loop().create_future()
        response_future.set_result(data)
        return response_future

    def read_command(self, comm_addr: int, offset: int, count: int) -> ProtocolCommand:
        """Create read protocol command."""
        return ModbusTcpReadCommand(comm_addr, offset, count)
