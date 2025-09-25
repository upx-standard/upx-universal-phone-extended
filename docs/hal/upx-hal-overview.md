# UPX HAL Overview (draft)

- Discover modules via I²C/EEPROM or virtual enumeration.
- Read `manifest` → bind kernel drivers (I²C/SPI/PCIe/USB/etc.).
- Expose modules to userspace via `upx-agent` (DBus/Unix socket), with permission gates for Elevated/Hazardous classes.
