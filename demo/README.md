# Arctic Night Theme Demo

A self-contained Docker setup that spins up a Home Assistant instance with the Arctic Night theme pre-configured and a showcase dashboard using demo entities.

## Quick Start

```bash
cd demo
docker compose up -d
```

Open [http://localhost:8123](http://localhost:8123) and login with:

- **Username:** `demo`
- **Password:** `demo`

The Arctic Night theme is applied globally, and the demo dashboard is pre-loaded on the home view.

## Graph Data

On first start, 24 hours of realistic temperature and humidity data is automatically seeded into the recorder database. The sensor graphs, gauges, and history cards will populate within a minute of startup. A page refresh may be needed.

## What's Included

- **Home Assistant** with the `demo:` integration, which auto-creates ~100 entities (lights, climate, sensors, locks, covers, media players, etc.)
- **Pre-configured auth** so you can skip onboarding and log in immediately
- **Arctic Night theme** applied globally via pre-seeded storage
- **card-mod** auto-downloaded on first start for full theme styling
- **Showcase dashboard** with:
  - Climate sensors, thermostats, and humidifier
  - Light tiles with brightness sliders
  - Media player controls
  - Vacuum and fan buttons
  - Lock and cover controls, motion sensor
  - Weather forecast, gauges, and history graph
