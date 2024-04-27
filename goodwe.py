#!/usr/bin/env python3
import socket
import struct
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

def decrypt_data(key, iv, data):
    backend = default_backend()
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=backend)
    decryptor = cipher.decryptor()
    decrypted_data = decryptor.update(data) + decryptor.finalize()
    return decrypted_data

def parse_meter_metrics(data):
    fmt = '<7s I 2s I 8s I 2s I 16s h I h h h I I I I I 21s'
    fields = struct.unpack_from(fmt, data)
    metrics = {
        "PacketType": fields[0],
        "EnergyExportDecawattHoursTotal": fields[1],
        "UnknownBytes1": fields[2],
        "EnergyGenerationDecawattHoursTotal": fields[3],
        "UnknownBytes2": fields[4],
        "SumOfEnergyGenerationAndExportDecawattHoursTotal": fields[5],
        "UnknownBytes3": fields[6],
        "EnergyImportDecawattHoursTotal": fields[7],
        "UnknownBytes4": fields[8],
        "SumOfEnergyImportLessGenerationDecawattHoursTotal": fields[9],
        "UnknownInt5": fields[10],
        "UnknownInt6": fields[11],
        "UnknownInt7": fields[12],
        "UnknownInt8": fields[13],
        "UnknownInt9": fields[14],
        "UnknownInt10": fields[15],
        "UnknownInt11": fields[16],
        "PowerExportWatts": fields[17],
        "PowerGenerationWatts": fields[18],
        "UnknownInt12": fields[19],
        "SumOfPowerGenerationAndExportWatts": fields[20],
        "UnknownBytes5": fields[21]
    }
    return metrics

def handle_connection(connection):
    try:
        while True:
            header = connection.recv(52)  # Attempt to read the header
            if len(header) < 52:
                break  # End of data or incomplete header

            magic, data_size_bytes, unknown, serial_number, iv, timestamp = \
                header[:6], header[6:10], header[10:14], header[14:30], header[30:46], header[46:52]

            if magic.decode() != "POSTGW":
                print("Error: File does not start with the expected magic value.")
                continue

            data_size = int.from_bytes(data_size_bytes, 'big')
            data = connection.recv(data_size - 41)  # Read the data part
            crc = connection.recv(2)  # Read the CRC

            year, month, day, hour, minute, second = timestamp

            print(f"magic   : {magic.decode()}")
            print(f"data_sz : {data_size}")
            print(f"unknown : {unknown.hex()}")
            print(f"s/n     : {serial_number.decode()}")
            print(f"iv      : {iv.hex()}")
            print(f"time    : {2000 + year:04}-{month:02}-{day:02} {hour:02}:{minute:02}:{second:02}")

            key = b'\xFF' * 16
            decrypted_data = decrypt_data(key, iv, data)

            metrics = parse_meter_metrics(decrypted_data)
            print("Decrypted Data Metrics:", metrics)
            print("crc     :", crc.hex())
            print()

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        connection.close()

def listen_on_port(ip, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((ip, port))
    sock.listen(5)
    print(f"Listening on {ip}:{port}")

    try:
        while True:
            connection, addr = sock.accept()
            print(f"Connected by {addr}")
            handle_connection(connection)
    except KeyboardInterrupt:
        print("Server shutting down.")
    finally:
        sock.close()

if __name__ == "__main__":
    listen_on_port('0.0.0.0', 20001)
