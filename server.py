from config import *
from conversion_utils import *
from networking import *
from encryption import *
from log_config import *
from vmem import *
from vprotocol import *
from goodwe import ET
from goodwe.protocol import ProtocolResponse
import logging
import asyncio
import inspect

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

                vmem = VMem(decrypted_data)
                #vmem.display_memory()

                inv = ET(None, None)
                inv._protocol = VProtocol(vmem)
                asyncio.run(inv.read_device_info())
                logger.info("Connected to inverter %s, S/N:%s.", inv.model_name, inv.serial_number)
                instance_vars = {k: v for k, v in inspect.getmembers(inv) if not k.startswith('_') and not inspect.ismethod(v)}
                logger.info(instance_vars)

                runtime_data = asyncio.run(inv.read_runtime_data())

                logging.info("---------------------------------------------------------")
                for sensor in inv.sensors():
                    if sensor.id_ in runtime_data:
                        #print(f"{sensor.id_}: \t\t {sensor.name} = {runtime_data[sensor.id_]} {sensor.unit}")
                        value = runtime_data[sensor.id_]
                        if value == 0 or value == "":
                            continue
                        print(f"{sensor.id_:30}: {runtime_data[sensor.id_]} {sensor.unit}")
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
