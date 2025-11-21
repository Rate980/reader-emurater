import sys

import serial


def main():
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} SERIAL_PATH")
        return
    serial_path = sys.argv[1]
    with serial.Serial(serial_path, 115200, timeout=1) as ser:
        while True:
            b = ser.read(1)
            if b:
                print(b.hex().upper(), end=" ", flush=True)
                if b == b"\xc0":
                    print()


if __name__ == "__main__":
    main()
