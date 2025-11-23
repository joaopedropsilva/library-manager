import sys

import uvicorn

from api.run import setup_api


if __name__ == "__main__":
    # Grabs log level override option if set
    log_level_override = ""
    try:
        idx = sys.argv.index("--log-level")
        log_level_override = sys.argv[idx + 1]
    except (IndexError, ValueError):
        pass

    app = setup_api(log_level_override=log_level_override)

    uvicorn.run(app, host="0.0.0.0", port=8000)
