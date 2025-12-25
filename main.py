from config import Config
from capture import capture_camera

def main():
    config = Config()
    capture_camera(config)

if __name__ == '__main__':
    main()