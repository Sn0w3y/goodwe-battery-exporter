from config import *
from conversion_utils import *
from networking import *
from encryption import *
from log_config import *
import logging

setup_logging()


def handle_connection(connection):
    try:
        with open('decrypted_data.log', 'a') as file:
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

                if FORWARD_ENABLED:
                    response = forward_data(header + data + crc)
                    logging.info(f"Forwarded data, received response: {response.hex()}")
                else:
                    logging.info("Skipped Forwarding to GoodWe")

                decrypted_data = decrypt_data(AES_KEY, iv, data)

                file.write(decrypted_data.hex() + '\n')

                logging.info("---------------------------------------------------------")
                logging.info(f"Date-Time: {day:02}-{month:02}-{2000 + year:04} {hour:02}:{minute:02}:{second:02}")
                logging.info(f"Temperature: {decode_temp_hex(decrypted_data.hex())}°C")
                logging.info(f"State of Charge: {decode_soc_hex(decrypted_data.hex())}%")
                logging.info(f"Voltage of Battery: {decode_batt_volt_hex(decrypted_data.hex())}V")
                logging.info(f"Grid Voltage L1: {decode_grid_volt1_hex(decrypted_data.hex())}V")
                logging.info(f"Grid Voltage L2: {decode_grid_volt2_hex(decrypted_data.hex())}V")
                logging.info(f"Grid Voltage L3: {decode_grid_volt3_hex(decrypted_data.hex())}V")
                logging.info(f"Backup Voltage L1: {decode_backup_volt1_hex(decrypted_data.hex())}V")
                logging.info(f"Backup Voltage L2: {decode_backup_volt2_hex(decrypted_data.hex())}V")
                logging.info(f"Backup Voltage L3: {decode_backup_volt3_hex(decrypted_data.hex())}V")
                logging.info(f"MPPT1 Voltage: {decode_mpp1_volt_hex(decrypted_data.hex())}V")
                logging.info(f"MPPT2 Voltage: {decode_mpp2_volt_hex(decrypted_data.hex())}V")

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