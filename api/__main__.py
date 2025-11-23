import sys
from api.run import start_api


if __name__ == "__main__":
    # Grabs log level override option if set
    log_level_override_option = ""
    try:
        idx = sys.argv.index("--log-level")
        log_level_override_option = sys.argv[idx + 1]
    except (IndexError, ValueError):
        pass

    start_api(log_level_override_option)
