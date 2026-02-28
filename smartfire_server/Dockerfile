# https://developers.home-assistant.io/docs/add-ons/configuration#add-on-dockerfile
ARG BUILD_FROM
FROM $BUILD_FROM

# Install system dependencies for rfcat (USB/RF)
RUN apk add --no-cache \
    python3 \
    py3-pip \
    libusb \
    libusb-dev \
    gcc \
    musl-dev \
    linux-headers

# Install Python dependencies
RUN pip3 install --no-cache-dir \
    rfcat \
    bitstring \
    flask

# Copy application
COPY smartfire_controller/ /app/
WORKDIR /app

# Run the server
CMD ["python3", "server.py"]
