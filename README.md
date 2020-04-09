# android-pn532-hce

Communicate between PN532 (I used a Raspberry Pi) and android to receive a unique id (uid) of the android device (for auth, whatever). Simple nfc tags like smart card and chip (which will often be shipped with the PN532) will work too.

## Concept

For deeper info check this link by Mohamed Hamdaoui. He communicated between two phones, some of the android code is used from him:
https://medium.com/the-almanac/how-to-build-a-simple-smart-card-emulator-reader-for-android-7975fae4040f

### tl;dr

Default: Card Reader sends APDU (Application Protocol Data Unit Command) -> tag will respond with uid.
Issue: Android device responds with either '01020304' or different id every time you hold it to the reader.
Solution: Android allows Host-based Card Emulation (HCE), so it may behave like a simple nfc tag / smart card. It can take APDU commands and return APDU responses.

Installing the android app will register an APDU service with an AID (in this example 'A0000001020304'). The reader (PN532) sends an APDU command containing this AID, the android device executes our registered service and sends back a local generated id (stored/persistent). No need to run the app after installation, service will do the job in background. Device can be locked, but screen needs to be on (android security policy).

## PN532

This is running on my Pi. The PN532 board needs to be connected via UART (because i2c / spi is not supported by nfcpy lib which will be used). Check some tutorial for this, if you haven't connected it yet.
In this example libnfc is not neccessary.

### Setup

install pip3 if not installed:

```python
sudo apt-get install python3-pip
```

install nfcpy:

```python
pip3 install -U nfcpy
```

### Run

Run the pn532.py file.

```python
python3 pn532.py
```

## Android

Either build this whole project by your own or use the prebuilt apk: [releases](https://github.com/Lexycon/android-pn532-hce/releases)

Copy the apk file to the phone and install it. The UI shows the uid and allows you to generate a new one (whyever :-D)
