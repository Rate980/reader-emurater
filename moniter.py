import serial

SERIAL_PATH = "/dev/pts/1"


def main():
    with serial.Serial(SERIAL_PATH, 115200, timeout=1) as ser:
        while True:
            b = ser.read(1)
            if b:
                print(b.hex().upper(), end=" ", flush=True)
                if b == b"\xc0":
                    print()


if __name__ == "__main__":
    main()
