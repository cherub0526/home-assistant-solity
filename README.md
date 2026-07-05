# Smart Solity

Home Assistant custom integration for Solity smart locks, controlled through
the lock's cloud API. Provides a `lock` entity and a battery `sensor` entity
for the single lock device tied to your account.

## Installation

### HACS (custom repository)

1. HACS → Integrations → ⋮ → Custom repositories.
2. Add this repository URL, category "Integration".
3. Install "Smart Solity", then restart Home Assistant.

### Manual

Copy `custom_components/smart_solity` into your Home Assistant `config/custom_components/` directory and restart.

## Configuration

Settings → Devices & Services → Add Integration → "Smart Solity", then enter
the 6-digit app password shown in the Solity app.
