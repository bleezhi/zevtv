# ZevTV Weather Automation

This directory contains the first version of the automated ZevTV Weather data pipeline.

## How it works

```
Open-Meteo
    ↓
weather.py
    ↓
weather.json
    ↓
future ZevTV graphics/video renderer
    ↓
ErsatzTV channel 03
```

The script fetches current conditions and a 7-day forecast for every location in `locations.json`.

## Run it

From this directory:

```bash
python3 weather.py
```

The generated feed is:

```
output/weather.json
```

No API key is required for the current Open-Meteo integration.

## Automatic refresh

On Linux, run it every 15 minutes with cron:

```cron
*/15 * * * * cd /path/to/zevtv/weather && /usr/bin/python3 weather.py >> /path/to/zevtv/weather/weather.log 2>&1
```

For the ErsatzTV setup, the next layer is a renderer that turns this data into short MP4 weather segments and places them in the media folder watched by ErsatzTV.

## Locations

Edit `locations.json` to add or remove cities. Coordinates are used directly, so the system can support any location with latitude/longitude.

## Data

Weather data is fetched from Open-Meteo. Check its current terms and attribution requirements before public/commercial broadcasting.
