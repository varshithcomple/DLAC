# VisionPort — 20 tasks, bundled traffic photo

**Default input:** `data/traffic.jpg` (included). All 15 Python scripts can execute using this one photograph. This does **not** mean every video-based assignment can be performed from one photograph.

## Windows PowerShell quick start

```powershell
cd VisionPort
python -m pip install -r requirements.txt
python 01_capture.py
python 02_image.py
python 05_vehicle_detection.py
python 14_illegal_parking.py
```

YOLO downloads model weights (`yolo11n.pt`) on the first run if not already cached; internet may be required. Every script saves image-mode results under `outputs/<script-name>.jpg`. Close the preview window or press Q. If OpenCV windows fail, run with `--no-display` (except 01_capture.py which does not need it).

For example:
```powershell
python 14_illegal_parking.py --no-display
python 05_vehicle_detection.py --image data/traffic.jpg --no-display
```

**To use actual video:** `python 14_illegal_parking.py --video data/traffic.mp4`; supply your own traffic video, and configure measurement zones/lines in `config/settings.json` before expecting meaningful violations/speeds.

## What one image supports

- Tasks 1–3: environment setup, bundled photo verification and still-image display (Task 2 physical camera capture available with `python 01_capture.py --capture`)
- Tasks 4–5: image preview / saving one image *only*; genuine video playback and video frame extraction require video
- Tasks 6–9: YOLO detects vehicles, classes, confidences and frame count. Crowded small vehicles may be missed
- Tasks 10–11: count-based density; sustained congestion / motion cannot be measured from a photo
- Task 12: detect vehicles only, **no cross-frame tracking IDs** from an image
- Task 13: detect vehicles only, **no speed** from an image
- Task 14: signal UNKNOWN unless a visible light is manually configured using `signal_roi` and `signal_lamps`
- Task 15: **no waiting time** from an image
- Tasks 16–18: **no entry/exit, wrong-turn or wrong-way movement** from an image
- Task 19: detect vehicles but **no illegal parking duration/violation** from an image; video needs a calibrated parking polygon
- Task 20: experimental person/bike spatial association for *possible* triple-riding, requires human verification; do not treat as verified offense

## Scripts

The original 15 numbered Python scripts cover the 20 tasks. By default all scripts use the bundled image. Use `--video` to switch to video (and real motion capabilities). For tasks requiring configured regions, settings remain intentionally unset rather than making up coordinates.

## Original reference documentation

# VisionPort – Intelligent Vehicle Detection and Traffic Monitoring

This starter implementation maps **all 20 tasks** from the supplied *VisionPort Project – Student Tasks and Assignments* sheet to executable Python scripts. It is an educational prototype, **not** an enforcement-grade system. Some advanced tasks require real-world camera calibration, manually selected junction zones, and human validation.

## Setup (Windows PowerShell / VS Code)

Install Python 3.11 or 3.12 (and VS Code if you prefer), open the project folder, then:

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

If `py -3.11` isn't installed, substitute a compatible installed Python version. If PowerShell blocks activation, use `.venv\Scripts\python.exe` instead of `python` without activating. `ultralytics` will automatically download pretrained `yolo11n.pt` weights on first run (internet needed once). This project expects standard COCO IDs: person=0, car=2, motorcycle=3, bus=5, truck=7.

Add your recorded static-camera road scene as **`data/traffic.mp4`**. OpenCV `imshow` needs a desktop graphical environment. You may instead use `--no-display --output outputs/demo.mp4` for most video scripts. No sample video is supplied (you must use your own footage with the appropriate permissions).

## Mapping to all tasks

| Sheet task | Program | Output / notes |
|---|---|---|
| 1 Install Python/OpenCV | `requirements.txt` | Working environment; `python -c "import cv2, ultralytics; print('Ready')"` |
| 2 Capture traffic image | `01_capture.py` | `data/traffic.jpg`; uses computer camera index 0 |
| 3 Read/display image | `02_image.py` | Image window |
| 4 Read/play video | `03_video.py` | Video window |
| 5 Save video frames | `04_extract_frames.py` | `frames/frame_*.jpg`, every ~1 second |
| 6 Detect cars | `05_vehicle_detection.py` | Bounding boxes |
| 7 Detect bikes/buses/trucks | `05_vehicle_detection.py` | COCO classes 3/5/7 |
| 8 Show labels/confidence | `05_vehicle_detection.py` | Overlay |
| 9 Count visible vehicles | `05_vehicle_detection.py` | **Per-frame** count, not total passing count |
| 10 Density | `07_density_congestion.py` | LOW/MEDIUM/HIGH **heuristic**; tune count thresholds and ROI |
| 11 Congestion | `07_density_congestion.py` | Sustained high count + low pixel motion; **possible** congestion |
| 12 Track across frames | `06_vehicle_tracking.py` | ByteTrack object IDs |
| 13 Approximate vehicle speed | `08_speed.py` | Needs **measured** distance between two video lines; crossing direction matters |
| 14 Signal red/yellow/green | `09_signal_status.py` | Manual ROI and separate lamp rectangles; HSV heuristic |
| 15 Waiting times | `10_waiting_time.py` | Approximate stationary time per tracked vehicle |
| 16 Entry/exit count | `11_entry_exit.py` | Unique vehicle IDs that cross each directional line |
| 17 Wrong turns | `12_wrong_turn.py` | Manual zone-to-zone allowed-route rules |
| 18 Wrong way | `13_wrong_way.py` | Lane ROI + direction-vector check |
| 19 Restricted parking | `14_illegal_parking.py` | Restriction polygon + time threshold; **possible** violation |
| 20 Triple riding | `15_triple_riding.py` | **Experimental candidates only**, requires human verification |

All video scripts accept `--video PATH`, `--config PATH`, `--output PATH`, and `--no-display` (except the static image/camera capture scripts). For example:

```powershell
python 05_vehicle_detection.py
python 06_vehicle_tracking.py --output outputs/tracked.mp4
python 07_density_congestion.py --video data/traffic.mp4
python 15_triple_riding.py --output outputs/triple_candidates.mp4
```

The `outputs/` and `frames/` folders are created automatically as needed.

## Configure advanced modules BEFORE running

Edit `config/settings.json` with coordinates matching *your* video. Use `python tools_select_roi.py` to click a polygon's vertices and press `S` to print coordinates for `roi_polygon`, `parking_zone`, `wrongway_zone`, and each element of `zones`. For bounding boxes, manually read frame coordinates using an image viewer or adapt the polygon helper to pick two corners. Coordinate origin is top-left; x grows to the right and y down.

- **Density/congestion (`07_density_congestion.py`):** Optional `roi_polygon` restricts the counted road area. Tune `density_low_max`, `density_medium_max`, `congestion_min_vehicles`, `congestion_max_avg_speed_px_s`, and `congestion_seconds`. Motion is measured in **pixels/sec**; perspective affects reliability. Empty ROI means entire frame.
- **Speed (`08_speed.py`):** Provide `speed_line_a` and `speed_line_b` as pairs of image coordinates: `[[x1,y1],[x2,y2]]`. Provide `speed_distance_m` (e.g. `10.0`) only if you have measured / correctly calibrated the road distance between them. The simple script uses line crossing order; it does not compensate for perspective or vehicle length and cannot guarantee true speed. Crossing direction and disjoint track IDs can distort results.
- **Signal (`09_signal_status.py`):** Provide `signal_roi` `[x1,y1,x2,y2]` around the light and `signal_lamps`: `{"red": [0,0,20,20], "yellow": [0,20,20,40], "green": [0,40,20,60]}`. Lamp rectangles are **relative to the signal ROI**, not global frame coordinates. Adjust HSV thresholds for your footage and ensure non-signal colored objects are excluded.
- **Wait (`10_waiting_time.py`):** Tune `stationary_px_s` and `waiting_stopped_seconds` for camera scale and tracking jitter. Uses timestamps from frame index and FPS, not wall-clock processing time.
- **Entry/exit (`11_entry_exit.py`):** Configure `entry_line` and `exit_line`; set `entry_direction` and `exit_direction` to `1`, `-1` or `0` based on crossing sign. `0` counts either direction. Example: `"entry_line": [[100,200],[700,200]]`.
- **Wrong turn (`12_wrong_turn.py`):** Configure `zones` by name and `route_allowed`, for example `"zones": {"north_entry": [[...]], "south_exit": [[...]], "east_exit": [[...]]}, "route_allowed": {"north_entry": ["south_exit"]}`. Vehicle must first be observed inside an entry zone before an exit zone. Use **distinct** zone names and don't overlap zones. A vehicle that enters a permitted exit zone after an unexpected exit may not be flagged until processed. This is a simplified path heuristic.
- **Wrong way (`13_wrong_way.py`):** Configure `wrongway_zone` polygon and vector such as `wrongway_direction: [0,1]` for downward motion. Alert is based on trajectory displacement against that direction.
- **Parking (`14_illegal_parking.py`):** Configure `parking_zone` polygon and `parking_seconds`. A stopped car in a marked zone is not automatically a legal violation (exceptions and signage matter).
- **Triple-riding (`15_triple_riding.py`):** Prototype associates `person` boxes to a `motorcycle` box with horizontal overlap and nearby lower-body position. At least 3 candidates across multiple frames triggers **CHECK**. It may falsely flag nearby pedestrians or miss occluded riders; it is **not a reliable rider-count classifier**. A stronger project trains an annotated rider-association model or uses pose keypoints and manually checked data.

## Recommended order

1. Complete `01` through `05`, verify that your video loads.
2. Run `05_vehicle_detection.py` and `06_vehicle_tracking.py`.
3. Tune count/density parameters and try waiting-time logic.
4. Mark your signal, lines, and junction zones; test `08` through `14` individually.
5. Save example footage / screenshots for demonstrations; visually inspect alerts and note false positives.

## Important limitations

- YOLO pretrained weights detect common COCO classes; they do **not** automatically infer traffic rules, junction right-of-way, prohibited turns or correct motorcycle rider association.
- A numeric vehicle count is **not** physical traffic density (vehicles per road kilometre). Our level indicator is a configurable proxy.
- Camera perspective, low resolution, occlusion, IDs switching, frame rate, and video quality can produce inaccurate results.
- Model weights, source traffic videos and custom calibrated zone coordinates are **not** bundled.
- For any formal report, label the violation outputs as *experimental / possible*, and quantify performance on manually checked footage before claiming accuracy.
