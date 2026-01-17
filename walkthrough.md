# Blue Iris AI Proxy - Verification & Walkthrough

## 1. Installation
Ensure prerequisites are met (Python 3.10+).

```powershell
./scripts/install_service.ps1
```

## 2. Configuration
Check `.env` file matches your setup:
```ini
BLUE_ONYX_URL=http://192.168.1.159:32168
SPECIESNET_REGION=AUS
TRIGGER_LABELS=animal,bird
PORT=8000
```

## 3. Verification
Run the simulation script to test the service without Blue Iris:
```powershell
python scripts/simulate_blue_iris.py
```
Check `service.log` for activity.

## 4. Verification Results (Debugging Session)

### Service Startup
- **Status**: Passed
- **Details**: Service starts successfully as a Windows Service ("BlueIrisAiProxy"). Log files (`service.log`) show correct initialization of `SpeciesNetWrapper` and `BlueOnyxClient`.
- **Fixes Applied**: Removed incorrect `geographic_info` argument from `SpeciesNet` initialization.

### End-to-End Prediction
- **Status**: Passed
- **Details**: Verified using `scripts/simulate_blue_iris.py`.
    - Proxy correctly receives image from simulated Blue Iris request.
    - Proxy correctly delegates to Blue Onyx (simulated response).
    - Proxy triggers SpeciesNet when Blue Onyx returns no predictions.
    - SpeciesNet correctly processes the image and returns predictions.

### Geofencing Logic
- **Status**: Verified (Model Data Limitation)
- **Observation**: User reported "non-AUS animal" (Wild Turkey) being returned despite `SPECIESNET_REGION=AUS`.
- **Root Cause**: The underlying SpeciesNet v4 model's geofence map **explicitly allows** Wild Turkey (*Meleagris gallopavo*) in Australia. This was confirmed by inspecting the model's internal `geofence_release.20251208.json` file.
- **Conclusion**: The service is correctly applying the configuration, but the model's geofence data is permissive for this species.

## 5. Troubleshooting
Check logs:
```powershell
Get-Content service.log -Wait
```
