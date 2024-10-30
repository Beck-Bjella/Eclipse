# Eclipse

**Eclipse** is a neural network-based aimbot optimized specifically for Fortnite. It provides customizable settings for sensitivity, targeting, and visualization to help you improve in-game aiming precision and responsiveness.

---

## Installation

### Step 1: Install Python
Ensure Python 3.8 or later is installed on your computer. You can download Python from the [official website](https://www.python.org/downloads/release/python-386/).

### Step 2: Setup CUDA
1. Download and install the latest version of [CUDA](https://developer.nvidia.com/cuda-downloads).

### Step 3: Download Eclipse
1. Go to the [Eclipse GitHub repository](https://github.com/Beck-Bjella/Eclipse/).
2. Click on “Code” and then select “Download ZIP.”
3. Extract the downloaded ZIP file to a convenient location on your computer.

### Step 4: Install Dependencies
1. Open the extracted folder, right-click on the background, and select **Open in Terminal** (or **Open PowerShell window here** on Windows).
2. Type the following command to install the necessary packages:
   ```bash
   pip install -r requirements.txt
   ```
   
### Step 5: Run Eclipse
1. Run the following command to start Eclipse:
   ```bash
   python main.py
   ```

## Configuration

To configure Eclipse, edit the `lib/config.json` file directly. This file contains settings for aiming sensitivity, visualization, and screen resolution.

### Configuration Options
- **normal_scale**: Controls the general aiming sensitivity, corresponding to Fortnite’s X/Y sensitivity.
- **targeting_scale**: Controls sensitivity when aiming down sights (right-click to aim), corresponding to Fortnite’s targeting sensitivity.  
  *Note*: Ensure that your in-game targeting and scope sensitivities are the same for best accuracy.
- **visualize**: Set to `true` to enable visualization mode, which opens a separate window to show bounding boxes around detected targets. This mode is useful for calibration.
- **game_resolution**: Set to match your screen resolution for accurate detection. Supported options are `"1920x1080"` and `"1280x720"`.

### Example `config.json` Files
(1920x1080 resolution):
```json
{
    "normal_scale": 0.1,
    "targeting_scale": 0.2,
    "visualize": false,
    "game_resolution": "1920x1080"
}
```

(1280x720 resolution) w/ visualization:
```json
{
    "normal_scale": 0.1,
    "targeting_scale": 0.2,
    "visualize": true,
    "game_resolution": "1280x720"
}
```

## Usage
Once Eclipse is running and correctly configured, all you have to do is hold f2 to enable the aimbot. 
The aimbot will automatically target the nearest enemy player within your crosshair. 
Pressing f3 will stop the programming.

## Contributing
Contributions are welcome! Please feel free to submit a pull request or open an issue if you have any suggestions or improvements.

# License
This project is licensed under the GNU General Public License v3.0. See the license file for more information.