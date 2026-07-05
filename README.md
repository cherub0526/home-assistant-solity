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

## Apple HomeKit

The lock entity works with Home Assistant's built-in HomeKit Bridge integration:

1. Locks always pair in HomeKit's "Accessory mode", so this lock gets its own
   dedicated pairing code in the Home app, separate from any shared bridge.
2. Home Assistant does not automatically show battery level on the lock tile,
   since it comes from a separate `sensor` entity rather than the lock's own
   state. To show it, open the HomeKit Bridge integration's entity settings
   for the lock and set **Linked battery sensor** to the
   `sensor.<name>_battery` entity created by this integration.
