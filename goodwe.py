#!/usr/bin/env python3
import socket
import logging
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

# Configuration Constants
FORWARD_IP = 'tcp.goodwe-power.com'
FORWARD_PORT = 20001
LISTEN_IP = '0.0.0.0'
LISTEN_PORT = 20001
HEADER_LENGTH = 52
AES_KEY = b'\xFF' * 16

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


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
    hex_value = hex_data[250:254]
    voltage = int.from_bytes(bytes.fromhex(hex_value), byteorder='big') / 10
    return voltage


def hex_to_MPP2(hex_data):
    """Convert hexadecimal MPPT2 to volts."""
    hex_value = hex_data[234:238]  # Extract the next two bytes after MPP1
    voltage = int.from_bytes(bytes.fromhex(hex_value), byteorder='big') / 10
    return voltage


def decrypt_data(key, iv, data):
    """Decrypt data using AES-CBC."""
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    return decryptor.update(data) + decryptor.finalize()


def forward_data(data):
    """Forward data to predefined IP and port, and return the response."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((FORWARD_IP, FORWARD_PORT))
        sock.sendall(data)
        return sock.recv(1024)


def handle_connection(connection):
    """Handle incoming connections and process data."""
    try:
        while True:
            header = connection.recv(HEADER_LENGTH)
            if len(header) < HEADER_LENGTH:
                break

            magic, data_size_bytes, unknown, serial_number, iv, timestamp = \
                header[:6], header[6:10], header[10:14], header[14:30], header[30:46], header[46:52]

            if magic.decode() != "POSTGW":
                logging.error("Invalid magic value.")
                continue

            data_size = int.from_bytes(data_size_bytes, 'big')
            data = connection.recv(data_size - 41)
            crc = connection.recv(2)
            year, month, day, hour, minute, second = [int(x) for x in timestamp]

            response = forward_data(header + data + crc)
            logging.info(f"Forwarded data, received response: {response.hex()}")

            decrypted_data = decrypt_data(AES_KEY, iv, data)

            logging.info(decrypted_data.hex())

            logging.info("---------------------------------------------------------")
            logging.info(f"Date-Time: {day:02}-{month:02}-{2000 + year:04} {hour:02}:{minute:02}:{second:02}")
            logging.info(f"Temperature: {hex_to_celsius(decrypted_data.hex())}°C")
            logging.info(f"State of Charge: {hex_to_soc(decrypted_data.hex())}%")
            logging.info(f"Voltage of Battery: {hex_to_battery_volt(decrypted_data.hex())}V")
            logging.info(f"Grid Voltage L1: {hex_to_grid_volt_l1(decrypted_data.hex())}V")
            logging.info(f"Grid Voltage L2: {hex_to_grid_volt_l2(decrypted_data.hex())}V")
            logging.info(f"Grid Voltage L3: {hex_to_grid_volt_l3(decrypted_data.hex())}V")
            logging.info(f"Backup Voltage L1: {hex_to_backup_volt_l1(decrypted_data.hex())}V")
            logging.info(f"Backup Voltage L2: {hex_to_backup_volt_l2(decrypted_data.hex())}V")
            logging.info(f"Backup Voltage L3: {hex_to_backup_volt_l3(decrypted_data.hex())}V")
            logging.info(f"MPPT1 Voltage: {hex_to_MPP1(decrypted_data.hex())}V")
            logging.info(f"MPPT2 Voltage: {hex_to_MPP2(decrypted_data.hex())}V")

            logging.info("---------------------------------------------------------")

    except Exception as e:
        logging.error(f"An error occurred: {e}")
    finally:
        connection.close()


def listen_on_port():
    """Listen on a specified port and handle connections."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind((LISTEN_IP, LISTEN_PORT))
        sock.listen(5)
        logging.info(f"Listening on {LISTEN_IP}:{LISTEN_PORT}")
        try:
            while True:
                connection, addr = sock.accept()
                logging.info(f"Connected by {addr}")
                handle_connection(connection)
        except KeyboardInterrupt:
            logging.info("Server shutting down.")


if __name__ == "__main__":
    listen_on_port()
