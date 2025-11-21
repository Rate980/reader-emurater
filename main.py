import random
import sys
import time

import serial

SLIP_END = 0xC0
SLIP_ESC = 0xDB
SLIP_ESC_END = 0xDC
SLIP_ESC_ESC = 0xDD

tag_prefix = random.randbytes(12 - 1)


tag_list = [False] * 256


def slip_encode(data: bytes) -> bytes:
    encoded = bytearray()
    for byte in data:
        if byte == SLIP_END:
            encoded.append(SLIP_ESC)
            encoded.append(SLIP_ESC_END)
        elif byte == SLIP_ESC:
            encoded.append(SLIP_ESC)
            encoded.append(SLIP_ESC_ESC)
        else:
            encoded.append(byte)
    encoded.append(SLIP_END)
    return bytes(encoded)


def print_available_tags():
    print("------------")
    print("Available tags")
    for i, present in enumerate(tag_list):
        if not present:
            continue
        tag_id = tag_prefix + i.to_bytes(1, "big")
        print(f"{' '.join(f'{b:02X}' for b in tag_id).upper()}")
    print("------------")


def main():
    import threading

    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} SERIAL_PATH")
        return
    serial_path = sys.argv[1]

    threading.Thread(target=sendTask, args=(serial_path,), daemon=True).start()
    print(f"Tag prefix: {' '.join(f'{b:02X}' for b in tag_prefix).upper()}")
    while True:
        print_available_tags()
        line = input("> ")
        commands = line.split()
        if len(commands) <= 0:
            continue
        match commands[0]:
            case "a":
                for x in commands[1:]:
                    if x == "*":
                        for i in range(256):
                            tag_list[i] = True
                        continue
                    tag_id = int(x, 16)
                    tag_list[tag_id] = True
            case "d":
                for x in commands[1:]:
                    if x == "*":
                        for i in range(256):
                            tag_list[i] = False
                        continue
                    tag_id = int(x, 16)
                    tag_list[tag_id] = False
            case _ as u:
                print(f"Unknown command '{u}'")


def sendTask(serial_path: str):
    ser = serial.Serial(serial_path, 9600, timeout=1)
    while True:
        raw = bytearray()
        for i, present in enumerate(tag_list):
            if not present:
                continue
            tag_id = tag_prefix + i.to_bytes(1, "big")
            raw.extend(tag_id)
        packet = slip_encode(raw)
        ser.write(packet)
        ser.flush()
        time.sleep(1)


if __name__ == "__main__":
    main()
