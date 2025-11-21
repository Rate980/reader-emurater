import sys

import serial


def main():
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} SERIAL_PATH")
        return
    serial_path = sys.argv[1]

    with serial.Serial(serial_path, 115200) as ser:
        while True:
            b = ser.read_until(b"\xc0")[:-1]
            i = 0
            decoded = bytearray()
            while i < len(b):
                byte = b[i]
                if byte == 0xDB:
                    i += 1
                    next_byte = b[i]
                    if next_byte == 0xDC:
                        decoded.append(0xC0)
                    elif next_byte == 0xDD:
                        decoded.append(0xDB)
                else:
                    decoded.append(byte)
                i += 1

            print("=============")
            if len(decoded) % 12 != 0:
                print("Invalid tag length")
                continue
            for j in range(0, len(decoded), 12):
                tag_id = decoded[j : j + 12]
                print(" ".join(f"{b:02X}" for b in tag_id).upper())


if __name__ == "__main__":
    main()
