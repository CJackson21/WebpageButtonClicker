# cjackson21@georgefox.edu

from automatedButtonClicker import automator
import argparse

def parse_arguments():
    parser = argparse.ArgumentParser(description="Your script description.")
    parser.add_argument("--user", type=str, help="Enter your username for Buildertrend")
    parser.add_argument("--password", type=str, help="Enter your  password for Buildertrend")
    parser.add_argument("--red", type=int, help="Red component of the RGB color (0-255)")
    parser.add_argument("--green", type=int, help="Green component of the RGB color (0-255)")
    parser.add_argument("--blue", type=int, help="Blue component of the RGB color (0-255)")
    parser.add_argument("--date", type=str, help="Enter the desired start date (format: 11/1/2022)")

    return parser.parse_args()


if __name__ == "__main__":
    args = parse_arguments()
    automator(args.user, args.password, args.red, args.green, args.blue, args.date)
