def hex_to_celsius(hex_data):
    """Convert hexadecimal temperature from deci-Celsius to Celsius."""
    hex_value = hex_data[491:494]
    temp_deci_celsius = int(hex_value, 16)
    return temp_deci_celsius / 10


def hex_to_soc(hex_data):
    """Convert hexadecimal state of charge to integer percentage."""
    hex_value = hex_data[1238:1242]
    return int(hex_value, 16)


def hex_to_battery_volt(hex_data):
    """Convert hexadecimal battery voltage to volts."""
    hex_value = hex_data[514:518]
    voltage = int.from_bytes(bytes.fromhex(hex_value), byteorder='big') / 10
    return voltage


def hex_to_backup_volt_l1(hex_data):
    """Convert hexadecimal grid voltage L1 to volts."""
    hex_value = hex_data[786:790]
    voltage = int.from_bytes(bytes.fromhex(hex_value), byteorder='big') / 10
    return voltage


def hex_to_backup_volt_l2(hex_data):
    """Convert hexadecimal grid voltage L2 to volts."""
    hex_value = hex_data[790:794]
    voltage = int.from_bytes(bytes.fromhex(hex_value), byteorder='big') / 10
    return voltage


def hex_to_backup_volt_l3(hex_data):
    """Convert hexadecimal grid voltage L3 to volts."""
    hex_value = hex_data[794:798]
    voltage = int.from_bytes(bytes.fromhex(hex_value), byteorder='big') / 10
    return voltage


def hex_to_grid_volt_l1(hex_data):
    """Convert hexadecimal backup voltage L1 to volts."""
    hex_value = hex_data[798:802]
    voltage = int.from_bytes(bytes.fromhex(hex_value), byteorder='big') / 10
    return voltage


def hex_to_grid_volt_l2(hex_data):
    """Convert hexadecimal backup voltage L2 to volts."""
    hex_value = hex_data[802:806]
    voltage = int.from_bytes(bytes.fromhex(hex_value), byteorder='big') / 10
    return voltage


def hex_to_grid_volt_l3(hex_data):
    """Convert hexadecimal backup voltage L3 to volts."""
    hex_value = hex_data[806:810]
    voltage = int.from_bytes(bytes.fromhex(hex_value), byteorder='big') / 10
    return voltage


def hex_to_MPP1(hex_data):
    """Convert hexadecimal MPPT1 to volts."""
    hex_value = hex_data[234:238]
    voltage = int.from_bytes(bytes.fromhex(hex_value), byteorder='big') / 10
    return voltage


def hex_to_MPP2(hex_data):
    """Convert hexadecimal MPPT2 to volts."""
    hex_value = hex_data[250:254]  # Extract the next two bytes after MPP1
    voltage = int.from_bytes(bytes.fromhex(hex_value), byteorder='big') / 10
    return voltage