import math
import time
import os
from pathlib import Path

def dbv_to_dbmw(sensitivity_dbv, impedance):
    return sensitivity_dbv - 10 * math.log10(1000 / impedance)

def calculate_max_spl(sensitivity_mw, impedance, v_max_dac):
    max_power_mw = (v_max_dac**2 / impedance) * 1000
    return sensitivity_mw + (10 * math.log10(max_power_mw))

def get_vol_attenuation(system_vol_percent, law=1):
    if system_vol_percent <= 0: return -100
    multiplier = 40 if law == 1 else 60
    return multiplier * math.log10(system_vol_percent / 100)

def get_vol_for_target_spl(target_spl, max_hw_spl, loudness_val, law=1):
    multiplier = 40 if law == 1 else 60
    required_attenuation = target_spl - max_hw_spl - loudness_val
    
    try:
        vol_pct = 100 * (10**(required_attenuation / multiplier))
        return min(vol_pct, 100.0)
    except OverflowError:
        return 0.0

def get_newest_csv(directory):
    files = list(directory.glob("*.csv"))
    if not files:
        return None
    return max(files, key=os.path.getmtime)

def monitor_live_log(sensitivity, unit, impedance, v_max_dac, vol_percent, law_choice):
    log_dir = Path.home() / "Documents" / "Orban Audio Loudness Meter"
    
    if not log_dir.exists():
        print(f"[!] ERROR: Directory not found: {log_dir}")
        return

    file_path = get_newest_csv(log_dir)
    if file_path is None:
        print(f"\n[!] ERROR: No CSV files found in: {log_dir}")
        return

    s_mw = dbv_to_dbmw(sensitivity, impedance) if unit.lower() == "v" else sensitivity
    max_hw_spl = calculate_max_spl(s_mw, impedance, v_max_dac)
    vol_reduction = get_vol_attenuation(vol_percent, law_choice)
    peak_spl = -100.0

    print(f"\n--- SUCCESS: Connected to Newest Log ---")
    print(f"File: {file_path.name}")
    print(f"Hardware Max: {max_hw_spl:.1f} dB | Current Attenuation: {vol_reduction:.1f} dB")
    print("Monitoring BS.1770 Long-Term... Press Ctrl+C to stop.")
    print("-" * 60)

    with open(file_path, "r", errors='ignore') as f:
        f.seek(0, os.SEEK_END)
        try:
            while True:
                line = f.readline()
                if not line or not line.strip():
                    time.sleep(0.1)
                    continue
                
                parts = line.strip().split(',')
                if len(parts) >= 15:
                    try:
                        loudness_val = float(parts[14].strip())
                        current_spl = max_hw_spl + loudness_val + vol_reduction
                        
                        vol_for_75 = get_vol_for_target_spl(75, max_hw_spl, loudness_val, law_choice)
                        
                        if current_spl > peak_spl:
                            peak_spl = current_spl
                        
                        status = "SAFE"
                        if current_spl > 80: status = "!! DANGER !!"

                        print(f"SPL: {current_spl:>5.1f} dB | Vol for 75dB: {vol_for_75:>4.1f}% | PEAK: {peak_spl:>5.1f} dB | {status}    ", end="\r")
                        
                    except ValueError:
                        continue
        except KeyboardInterrupt:
            print(f"\n\nSession Ended. Peak reached: {peak_spl:.1f} dB")

if __name__ == "__main__":
    try:
        sensitivity = float(input("Enter headphone sensitivity in dB/mw (e.g., 101): "))
        impedance = float(input("Enter headphone impedance in ohms (e.g., 60): "))
        v_max_dac = float(input("Enter maximum rms voltage of DAC (e.g., 1.23): "))
        vol_percentage = float(input("Enter volume percentage (0-100): "))
        
        monitor_live_log(
            sensitivity=sensitivity, 
            unit="mw", 
            impedance=impedance, 
            v_max_dac=v_max_dac, 
            vol_percent=vol_percentage,
            law_choice=1 # 1 is square law, 2 is cube law
        )
    except ValueError:
        print("[!] ERROR: Please enter numeric values only.")