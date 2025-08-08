# XboxSynth 🎮🎹

**XboxSynth** is a real-time synthesizer controlled with an **Xbox One controller**.  
It combines [Pyo](https://ajaxsoundstudio.com/software/pyo/), [PyGame](https://www.pygame.org/news), and [PyQt6](https://riverbankcomputing.com/software/pyqt/intro) to generate sounds, effects, and recordings while interacting with the gamepad.

For the last Release go to [RELEASE]([https://github.com/zeligmax/XboxSynth/blob/main/LICENSE.md)
---

## 🎯 Features
- Real-time note and effects control using an Xbox controller.
- Built-in effects: **reverb**, **delay**, **chorus**, **phaser**.
- Special trigger sounds:
  - `LT`: deep, long laser (*szoom*).  
  - `RT`: high-pitched, short laser (*piu-piu*).
- Change waveform on the fly.
- Record `.wav` audio output and save `.csv` controller logs.
- Graphical interface for visualizing and adjusting parameters.

---

## 📦 Requirements

- Python 3.11 (recommended)
- Xbox controller connected via USB or Bluetooth
- Python libraries:
  - `pyo`
  - `pygame`
  - `PyQt6`
  - `numpy`

Install dependencies:
#pip install -r requirements.txt

On Windows, make sure you have the official Xbox drivers installed if the controller is not detected.

🚀 How to Run
Clone this repository:
#git clone https://github.com/zeligmax/xboxsynth.git
#cd xboxsynth
#(Optional) Create and activate a virtual environment:

#python -m venv pyo-env
#source pyo-env/bin/activate  # Linux/Mac
#pyo-env\Scripts\activate     # Windows

Install dependencies:
#pip install -r requirements.txt

Start the program:
#python 1_main.py

🎮 Controller Mapping
Control	Action
A/B/X/Y buttons	Play notes (from note_map)
D-Pad	Additional notes (hat_map)
Left joystick	Navigate pentatonic scale
Right joystick (X)	Reverb mix
Right joystick (Y)	Delay feedback
Left trigger (LT)	Szoom (deep, long laser)
Right trigger (RT)	Piu-piu (high-pitched, short laser)
LB button	Toggle Phaser
RB button	Change waveform
Back button	Octave down
Start button	Octave up
Record button (UI)	Start/stop .wav and .csv logging

📁 Project Structure
bash
Copiar
Editar
xboxsynth/
├── 1_main.py            # Main script
├── controlador.py       # Xbox controller logic
├── sonido.py            # Synthesis and effects engine
├── config.py            # Note mapping and wave tables
├── ui/                  # PyQt6 UI
├── logs/                # Audio recordings and control logs
└── requirements.txt

📜 License
This project is released under the MIT License.
See the [LICENSE](https://github.com/zeligmax/XboxSynth/blob/main/LICENSE.md) file for details.

🙌 Credits
Created by Zeligmax.
Inspired by digital audio experimentation and video game controllers.
