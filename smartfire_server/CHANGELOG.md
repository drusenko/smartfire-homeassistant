# Changelog

## 1.0.3

- Fix 500 error when YardStick not connected: return 503 with clear error message
- Add error handling to power endpoint and global exception handler
- Integration now shows server's error message (e.g. "Check that YardStick One is connected")

## 1.0.2

- Log YardStick USB device detection status at startup
- Suppress confusing Flask "Running on 172.30.x.x" messages (container internal IP)
- Add clear startup message explaining how to access the server

## 1.0.1

- Fix addon build: install rfcat from git to avoid PyPI pyproject.toml parsing error
- Upgrade pip before installing packages

## 1.0.0

- Initial release
- REST API for Proflame 2 fireplace control
- YardStick One USB support
