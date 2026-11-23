"""
VisionPort — Comprehensive Task Runner
Executes all 15 tasks in sequence and reports status and generated outputs.
"""

import sys
import time
import subprocess
from pathlib import Path

TASKS = [
    ("01_capture.py", "Task 2: Capture or verify input image"),
    ("02_image.py", "Task 3: Display traffic image"),
    ("03_video.py", "Task 4: Traffic video playback / image preview"),
    ("04_extract_frames.py", "Task 5: Save/extract video frames"),
    ("05_vehicle_detection.py", "Tasks 6-9: Detection, classes, confidences & vehicle count"),
    ("06_vehicle_tracking.py", "Task 12: ByteTrack multi-object tracking"),
    ("07_density_congestion.py", "Tasks 10-11: Density heuristic and congestion status"),
    ("08_speed.py", "Task 13: Vehicle speed approximation"),
    ("09_signal_status.py", "Task 14: Traffic signal status recognition"),
    ("10_waiting_time.py", "Task 15: Intersection waiting time estimation"),
    ("11_entry_exit.py", "Task 16: Entry and exit directional line counts"),
    ("12_wrong_turn.py", "Task 17: Zone-to-zone wrong turn detection"),
    ("13_wrong_way.py", "Task 18: Wrong-way traffic detection"),
    ("14_illegal_parking.py", "Task 19: Restricted parking zone monitoring"),
    ("15_triple_riding.py", "Task 20: Experimental triple-riding candidate detection"),
]

def main():
    import argparse
    parser = argparse.ArgumentParser(description="Run all VisionPort tasks in sequence.")
    parser.add_argument("--no-display", action="store_true", default=True,
                        help="Run without opening GUI preview windows (default: True)")
    parser.add_argument("--display", dest="no_display", action="store_false",
                        help="Show interactive OpenCV GUI windows for each script (press Q to advance)")
    parser.add_argument("--video", help="Optional override video path for all scripts")
    args = parser.parse_args()

    base_dir = Path(__file__).resolve().parent
    outputs_dir = base_dir / "outputs"
    outputs_dir.mkdir(exist_ok=True)

    print("=" * 72)
    print(" VISIONPORT: Intelligent Vehicle Detection and Traffic Monitoring")
    print("=" * 72)
    print(f"Working Directory : {base_dir}")
    print(f"Display Mode      : {'Headless (--no-display)' if args.no_display else 'Interactive GUI'}")
    if args.video:
        print(f"Video Source      : {args.video}")
    print("=" * 72)

    results = []
    total_start = time.time()

    for script, desc in TASKS:
        script_path = base_dir / script
        if not script_path.exists():
            print(f"[-] {script:<25} File not found!")
            results.append((script, desc, "SKIPPED", "-", 0.0))
            continue

        cmd = [sys.executable, str(script_path)]
        if args.no_display and script != "01_capture.py":
            cmd.append("--no-display")
        if args.video:
            cmd.extend(["--video", args.video])

        print(f"[*] Running {script:<25} ({desc})...", end=" ", flush=True)
        t0 = time.time()
        try:
            res = subprocess.run(cmd, cwd=base_dir, capture_output=True, text=True)
            elapsed = time.time() - t0
            output_file = outputs_dir / f"{Path(script).stem}.jpg"
            has_output = output_file.exists()

            if res.returncode == 0:
                print(f"[OK] ({elapsed:.2f}s)")
                out_name = f"outputs/{output_file.name}" if has_output else "-"
                results.append((script, desc, "SUCCESS", out_name, elapsed))
            else:
                print(f"[FAILED] ({elapsed:.2f}s)")
                err_snippet = (res.stderr or res.stdout).strip().splitlines()[-1] if (res.stderr or res.stdout) else "Error"
                print(f"    Error: {err_snippet}")
                results.append((script, desc, "FAILED", "-", elapsed))
        except Exception as e:
            elapsed = time.time() - t0
            print(f"[ERROR] ({elapsed:.2f}s): {e}")
            results.append((script, desc, "ERROR", "-", elapsed))

    total_time = time.time() - total_start
    print("=" * 72)
    print(f" EXECUTION SUMMARY (Total Time: {total_time:.2f}s)")
    print("=" * 72)
    print(f"{'Script':<25} | {'Status':<8} | {'Time':<7} | {'Output Saved'}")
    print("-" * 72)
    for script, desc, status, out_name, elapsed in results:
        print(f"{script:<25} | {status:<8} | {elapsed:>5.2f}s | {out_name}")
    print("=" * 72)
    print(f"All annotated images and logs are available in: {outputs_dir}")

if __name__ == "__main__":
    main()
