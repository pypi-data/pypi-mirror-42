# Python RC522 library
pyrc522 provides a simple interface for controlling an SPI RFID module "RC522"
using Raspberry Pi.

Based on [MFRC522-python](https://github.com/mxgxw/MFRC522-python/) and
[pi-rc522](https://github.com/ondryaso/pi-rc522/).

Install using pip:
```
pip install pyrc522
```

Or get source code from Github:

```
git clone https://github.com/fladi/pyrc522.git
cd pyrc522
python setup.py install
```

You'll also need to install the [**periphery**](https://pypi.python.org/pypi/periphery) library.

[MIFARE datasheet](https://www.nxp.com/docs/en/data-sheet/MF1S50YYX_V1.pdf) can be useful.

## Sectors? Blocks?
Classic 1K MIFARE tag has **16 sectors**, each contains **4 blocks**. Each block
has 16 bytes. All this stuff is indexed - you must count from zero. The library
uses "**block addresses**", which are positions of blocks - so block address 5
is second block of second sector, thus it's block 1 of sector 1 (indexes). Block
addresses 0, 1, 2, 3 are from the first sector - sector 0. Block addresses 4, 5,
6, 7 are from the second sector - sector 1, and so on. You should **not write**
to first block - S0B0, because it contains manufacturer data. Each sector has
it's **sector trailer**, which is located at it's last block - block 3. This
block contains keys and access bits for corresponding sector. For more info,
look at page 10 of the datasheet. You can use
[this](http://www.proxmark.org/forum/viewtopic.php?id=1408) useful utility to
calculate access bits.

## Connecting
Connecting RC522 module to SPI is pretty easy. You can use [this neat
website](http://pi.gadgetoid.com/pinout) for reference.

| Board pin name | Board pin | Physical RPi pin | RPi pin name |
|----------------|-----------|------------------|--------------|
| SDA            | 1         | 24               | GPIO8, CE0   |
| SCK            | 2         | 23               | GPIO11, SCKL |
| MOSI           | 3         | 19               | GPIO10, MOSI |
| MISO           | 4         | 21               | GPIO9, MISO  |
| IRQ            | 5         | 18               | GPIO24       |
| GND            | 6         | 6, 9, 20, 25     | Ground       |
| RST            | 7         | 22               | GPIO25       |
| 3.3V           | 8         | 1,17             | 3V3          |

You can also connect the SDA pin to CE1 (GPIO7, pin #26) and call the RFID
constructor with *bus=0, device=1* and you can connect RST pin to any other free
GPIO pin and call the constructor with *pin_rst=__BOARD numbering pin__*.
Furthermore, the IRQ pin is configurable by passing *pin_irq=__BOARD numbering pin__*.

__NOTE:__ For RPi A+/B+/2/3 with 40 pin connector, SPI1/2 is available on top of
SPI0. Kernel 4.4.x or higher and *dtoverlay* configuration is required. For
SPI1/2, *pin_ce=__BOARD numbering pin__* is required.

You may change BOARD pinout to BCM py passing *pin_mode=RPi.GPIO.BCM*. Please
note, that you then have to define all pins (irq+rst, ce if neccessary).
Otherwise they would default to perhaps wrong pins (rst to pin 15/GPIO22, irq to
pin 12/GPIO18).

## Usage
The library provides a single class - **RFID**. You basically want to
start with *while True* loop and "poll" the tag state. That's done using
*request* method. Most of the methods return error state, which is simple
boolean - True is error, False is not error. The *request* method returns True
if tag is **not** present. If request is successful, you should call *anticoll*
method. It runs anti-collision algorithms and returns used tag UID, which you'll
use for *select_tag* method. Now you can do whatever you want. Important methods
are documented.

```python
from pyrc522 import RFID
rdr = RFID()

while True:
  rdr.wait_for_tag()
  (error, tag_type) = rdr.request()
  if not error:
    print("Tag detected")
    (error, uid) = rdr.anticoll()
    if not error:
      print("UID: " + str(uid))
      # Select Tag is required before Auth
      if not rdr.select_tag(uid):
        # Auth for block 10 (block 2 of sector 2) using default shipping key A
        if not rdr.card_auth(rdr.auth_a, 10, [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF], uid):
          # This will print something like (False, [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
          print("Reading block 10: " + str(rdr.read(10)))
          # Always stop crypto1 when done working
          rdr.stop_crypto()

# Calls GPIO cleanup
rdr.cleanup()
```
