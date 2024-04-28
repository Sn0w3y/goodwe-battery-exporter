def decode_temp_hex(hex_data):
    """Decodes temperature from hexadecimal (in deci-Celsius to Celsius)."""
    hex_value = hex_data[491:494]
    temp_deci_celsius = int(hex_value, 16)
    return temp_deci_celsius / 10


def decode_soc_hex(hex_data):
    """Decodes state of charge from hexadecimal (to integer percentage)."""
    hex_value = hex_data[1238:1242]
    return int(hex_value, 16)


def decode_batt_volt_hex(hex_data):
    """Decodes battery voltage from hexadecimal (to volts)."""
    hex_value = hex_data[514:518]
    voltage = int.from_bytes(bytes.fromhex(hex_value), byteorder='big') / 10
    return voltage


def decode_backup_volt1_hex(hex_data):
    """Decodes backup grid voltage L1 from hexadecimal (to volts)."""
    hex_value = hex_data[786:790]
    voltage = int.from_bytes(bytes.fromhex(hex_value), byteorder='big') / 10
    return voltage


def decode_backup_volt2_hex(hex_data):
    """Decodes backup grid voltage L2 from hexadecimal (to volts)."""
    hex_value = hex_data[790:794]
    voltage = int.from_bytes(bytes.fromhex(hex_value), byteorder='big') / 10
    return voltage


def decode_backup_volt3_hex(hex_data):
    """Decodes backup grid voltage L3 from hexadecimal (to volts)."""
    hex_value = hex_data[794:798]
    voltage = int.from_bytes(bytes.fromhex(hex_value), byteorder='big') / 10
    return voltage


def decode_grid_volt1_hex(hex_data):
    """Decodes grid voltage L1 from hexadecimal (to volts)."""
    hex_value = hex_data[798:802]
    voltage = int.from_bytes(bytes.fromhex(hex_value), byteorder='big') / 10
    return voltage


def decode_grid_volt2_hex(hex_data):
    """Decodes grid voltage L2 from hexadecimal (to volts)."""
    hex_value = hex_data[802:806]
    voltage = int.from_bytes(bytes.fromhex(hex_value), byteorder='big') / 10
    return voltage


def decode_grid_volt3_hex(hex_data):
    """Decodes grid voltage L3 from hexadecimal (to volts)."""
    hex_value = hex_data[806:810]
    voltage = int.from_bytes(bytes.fromhex(hex_value), byteorder='big') / 10
    return voltage


def decode_mpp1_volt_hex(hex_data):
    """Decodes MPPT1 voltage from hexadecimal (to volts)."""
    hex_value = hex_data[234:238]
    voltage = int.from_bytes(bytes.fromhex(hex_value), byteorder='big') / 10
    return voltage


def decode_mpp2_volt_hex(hex_data):
    """Decodes MPPT2 voltage from hexadecimal (to volts)."""
    hex_value = hex_data[250:254]
    voltage = int.from_bytes(bytes.fromhex(hex_value), byteorder='big') / 10
    return voltage
