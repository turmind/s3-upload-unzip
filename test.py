import json

from main import lambda_handler
from dotenv import find_dotenv, load_dotenv

def main():
    load_dotenv(find_dotenv('.env'))
    with open('event-demo.txt') as json_file:
        event = json.load(json_file)
    lambda_handler(event, "123")

if __name__ == "__main__":
    main()