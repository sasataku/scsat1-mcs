import argparse
import time
from yamcs.client import YamcsClient

DEFAULT_YAMCS_URL = 'localhost:8090'
DEFAULT_YAMCS_INSTANCE = 'scsat1'

def main(args):

    client = YamcsClient(args.url)
    processor = client.get_processor(args.instance, "realtime")

    command = processor.issue_command(
        "/SCSAT1/ADCS/UPLOAD_OPEN_CMD",
        args={
            "session_id": 0,
            "file_name": "/storage/zephyr.bin",
        }
    )
    print("Issued", command)

    offset = 0

    try:
        with open(args.src, "rb") as file:
            while chunk := file.read(args.chunk):
                command = processor.issue_command(
                    "/SCSAT1/ADCS/UPLOAD_DATA_CMD",
                    args={
                        "session_id": 0,
                        "offset": offset,
                        "size": len(chunk),
                        "data": chunk
                    }
                )
                time.sleep(0.2)
                offset += len(chunk)

            command = processor.issue_command(
                "/SCSAT1/ADCS/UPLOAD_CLOSE_CMD",
                args={
                    "session_id": 0,
                }
            )
            print("Issued", command)
    except FileNotFoundError:
        print(f"File not found: {args.src}")
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="SC-Sat1 Upload file tool")
    parser.add_argument("--src", type=str, required=True,
                        help="Upload file on local host")
    parser.add_argument("--chunk", type=str, default=200,
                        help="Chunk size (byte)")
    parser.add_argument("--url", type=str, default=DEFAULT_YAMCS_URL,
                        help=f"Yamcs URL and Port number (default: {DEFAULT_YAMCS_URL})")
    parser.add_argument("--instance", type=str, default=DEFAULT_YAMCS_INSTANCE,
                        help=f"Yamcs instance name (default: {DEFAULT_YAMCS_INSTANCE})")
    args = parser.parse_args()
    main(args)
