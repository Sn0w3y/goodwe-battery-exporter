import struct

class VMem:
    def __init__(self, data=None):
        self.memory = {}
        if data:
            self.load_data(data)

    def load_data(self, data):
        """Loads data from binary input into the virtual memory."""
        index = 1  # Start after the number of records byte
        num_records = data[0]
        
        for _ in range(num_records):
            if index + 4 > len(data):
                break
            
            # Read start and end indices
            start_index = struct.unpack('>H', data[index:index+2])[0]
            end_index = struct.unpack('>H', data[index+2:index+4])[0]
            index += 4

            # Each address represents a 16-bit word, increment by 2 for each address
            for addr in range(start_index, end_index + 1):
                # Store the 16-bit word in memory
                self.memory[addr] = struct.unpack('>H', data[index:index+2])[0]
                index += 2

    def to_bytes(self):
        """Converts the virtual memory content to binary format."""
        data = bytearray((max(self.memory.keys()) + 1)*2)

    def read_word(self, address):
        """Reads a 16-bit word from the specified memory address."""
        return self.memory.get(address, None)

    def display_memory(self):
        """Prints the memory content in a hex dump format with collapsing repeating lines and ASCII representation."""
        min_addr = min(self.memory.keys()) & 0xFFF0
        max_addr = max(self.memory.keys())
        last_line = None
        repeat_line = False

        for addr in range(min_addr, max_addr + 1, 16):
            current_line = []
            ascii_repr = ""
            for offset in range(0, 16):
                word = self.read_word(addr + offset)
                if word is not None:
                    current_line.append(f"{word:04X}")
                    # Prepare ASCII representation
                    ascii_repr += chr((word >> 8) & 0xFF) if 32 <= (word >> 8) & 0xFF <= 126 else '.'
                    ascii_repr += chr(word & 0xFF) if 32 <= word & 0xFF <= 126 else '.'
                else:
                    current_line.append("    ")
                    ascii_repr += "  "
                if offset == 7:
                    current_line.append("")

            # Convert list to string for easy comparison
            line_str = ' '.join(current_line)
            if line_str == last_line:
                if not repeat_line:
                    print("*")
                    repeat_line = True
            else:
                print(f"{addr:04X}: {line_str}  |{ascii_repr}|")
                repeat_line = False

            last_line = line_str

