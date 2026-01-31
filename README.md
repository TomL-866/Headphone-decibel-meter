# Headphone-Decibelmeter

A Python-based utility that monitors and displays the decibel output of your headphones in real-time by interfacing with the Orban Loudness Meter.

I mainly made this so that I can tell when I'm approaching unsafe listening levels. 

---

### Prerequisites
Before you begin, ensure you have the following installed:

* **Operating System:** Windows (Tested on Windows 11)
* **Python:** [Download Python 3.x](https://www.python.org/downloads/windows/)
* **Orban Loudness Meter:** [Download via Orban.com](https://www.orban.com/meter)

---

### Setup (Orban Loudness)
To allow the Python script to read your audio data, you must configure the Orban Loudness Meter to log its output:

1.  **Select Device:** Open Orban Loudness Meter, go to **Settings**, and select your audio device from the **Audio** dropdown.
2.  **Activate Metering:** Navigate to the **Meters** tab and click the ON button at the bottom.
3.  **Enable Logging:** Select **Write to log file** at the bottom right.

---

### How to Run
Once Orban Loudness Meter is running and logging data:

1.  **Open Terminal in folder containing main.py**
2.  **Launch Script:**
    ```powershell
    python main.py
    ```
3.  **Input Specifications:** Enter the required values for your specific headphones and DAC. 
    > *Note: These specs are usually available online.*

---

### Contributing
Spot any issues or want to improve this? 
* Please submit a **Pull Request**!
