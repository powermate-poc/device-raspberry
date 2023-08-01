# PowerMate Device: Raspberry

The PowerMate device code for Raspberry Pi Zero devices.

## configuration

### Certificates 

Put `RootCA.pem`, `certificate.pem.crt`, and `private.pem.key` into the `certs` folder.

### MQTT

Copy the `example.env` as `.env` and enter the required parameters.

```sh
cp example.env .env
```

## get started

Python 3.11 is required.

Install the dependencies with

```sh
pip install -r requirements.txt
```