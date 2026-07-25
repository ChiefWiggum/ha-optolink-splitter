# Changelog

## 1.1.0

- Poll list template rebuilt from community-TESTED air-source WO1C configs:
  Vitocal 200-A AWO-E-AC 201.A16 (monobloc, CU401B_A - same controller family
  as the Vitocal 300-A) and Vitocal 200-S AWB-E-AC 201.D16 (Vitosoft-verified
  datapoints). Sources: optolink-splitter wiki "350 Poll Configuration Samples".
- New verified datapoints: defrost (0xB446), fan speed (0xB420), compressor
  phase state machine (0x130B), compressor running (0x0480), DHW temperature
  (0x01CD) and setpoints (0x6000/0x600C), energy counters split heating/DHW
  (0x1640/0x1650/0x1660/0x1670), current COP (0x1690) + SCOP total/heating/DHW
  (0x1680-0x1682), runtimes and compressor starts, pump relays, fault buffers.
- Ready-made HA entities: climate (HK2 thermostat incl. presets), water_heater,
  one-time DHW charge button, e-heater switch, writable heating-curve and
  setpoint numbers, ad-hoc command console (text + resp).
- HK1 and HK2 blocks both included - delete the circuit your system doesn't use.

## 1.0.0

- Initial release.
