# CyberKeeb2040
A mechnical keyboard and a cyberdeck. Powered by [PicoMK](https://github.com/zli117/PicoMK) for communication between RP2040 and Pi Zero. Watch the demo on YouTube 👇.

[![Watch the demo video](Images/Screenshot%202023-08-19%20CyberKeeb%202040.png)](https://youtu.be/GYs4eybdZCU)

# BOM
| Component | Count |
| ------------- | ------------- |
| Pi Pico  | 1 |
| Pi Zero W or Pi Zero 2 W  | 1 |
| Pi Zero 2x20 Header Pins  | 1 |
| SD Card  | 1 |
| JMD0.96C OLED Display | 1 |
| 4 Position DIP Switch | 1 |
| 0.1" 3 Pin Header + Jumper / 0.1" Pitch SPDT Slide Switch | 1 |
| Hotswap Socket | 66 |
| Keyboard Switch (Hippo Linear) | 66 |
| Keycaps (Redragon Crystal Keycap) | 66 |
| EC11 Rotary Encoder | 1 |
| Encoder Knob (Glorious) | 1 |
| 1N4148 Diode | 84 |
| M2.6 x 10mm Self Tapping Screws | 8 |
| M2.6 x 16mm Self Tapping Screws | 7 |
| 3mm Acrylic Sheet | 2 |
| 1.5mm Acrylic Sheet | 1 |
| 3D Printed Rivet + Spacers | 15 |
| JST-PH 2.0mm 4 Pin Female Connector | 2 |
| Stablizer Set | 1 |
| 330Ω THT Resister | 1 |
| 10kΩ THT Resister | 4 |
| 1206 0.01 µF Capacitor | 2 |
| (Optional) 3.5 inch TFT Display HAT | 1 |
| (Optional) 0.1" 3 Pin 90° Header | 1 |
| (Optional) 0.1" 4 Pin 90° Header | 1 |

# Build Instructions

## PCB
Everything is in [PCB/MainBoard](PCB/MainBoard) dir. Designed with Kicad 7.0. Make sure `Perfect DOS VGA 437 Font` is intalled on Windows. [Gerber](PCB/MainBoard/Gerber) directory is generated with PCBWay's specs. You might need to regenerate according to your fab's specs.

## Case
The case comprises three acrylic plates and various 3D printed rivets:


# PCB Library Licenses

 * Pico symbol, footprint from https://github.com/ncarandini/KiCad-RP-Pico under CC-BY-SA 4.0. 3D model for Pico is obtained from Raspberry Pi Foundation.
 * Pi Zero symbol, footprint and 3D model are from [SnapEDA](https://www.snapeda.com/parts/ADA3708/Adafruit%20Industries%20LLC/view-part/) under [CC BY-SA 4.0](https://support.snapeda.com/en/articles/2957814-what-is-the-license-for-symbols-and-footprints)
 * Key switch footprints and 3D models are from https://github.com/kiswitch/kiswitch
 * PJ320A symbol, footprint are from [Keebio-Parts.pretty](https://github.com/keebio/Keebio-Parts.pretty/blob/master/TRRS-PJ-320A.kicad_mod) under MIT License.
 * Other symbols are from KiCad library which is under CC-BY-SA 4.0 license. 


This work is licensed under a
[Creative Commons Attribution-ShareAlike 4.0 International License][cc-by-sa].

[![CC BY-SA 4.0][cc-by-sa-image]][cc-by-sa]

[cc-by-sa]: http://creativecommons.org/licenses/by-sa/4.0/
[cc-by-sa-image]: https://licensebuttons.net/l/by-sa/4.0/88x31.png
[cc-by-sa-shield]: https://img.shields.io/badge/License-CC%20BY--SA%204.0-lightgrey.svg
