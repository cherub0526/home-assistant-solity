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

The lock entity works with Home Assistant's built-in HomeKit Bridge
integration. Locks must use HomeKit's "Accessory mode" (a dedicated pairing,
separate from any shared bridge) rather than being bundled into an existing
bridge, since Home Assistant's `homekit` component requires this for `lock`
entities.

### Pair the lock as its own accessory (recommended)

1. Settings → Devices & Services → Add Integration → search for
   **HomeKit Bridge** (add a new entry — do not edit an existing bridge).
2. In the setup wizard, choose mode **Accessory** and select your lock
   entity, e.g. `lock.front_door`.
3. Once created, the new HomeKit entry shows a dedicated QR code / 8-digit
   pairing code.
4. On iPhone/iPad, open the **Home** app → `+` → Add Accessory → scan the QR
   code shown in Home Assistant (or enter the PIN manually).
   - If the accessory isn't found, make sure the iPhone and the Home
     Assistant host are on the same local network and that mDNS/Bonjour
     (UDP 5353) and the HomeKit TCP port aren't blocked by a firewall.
5. Once paired, the lock appears in the Home app and can be locked/unlocked
   or used in automations/scenes.
6. To show battery level on the lock's tile: open the new HomeKit entry →
   Configure → Entities → select the lock → advanced options → **Linked
   battery sensor** → choose `sensor.front_door_battery` → save. Home
   Assistant does not do this automatically, since the battery is a separate
   `sensor` entity rather than an attribute of the lock's own state.

### Adding it to an existing shared bridge instead

You can add the lock entity to an existing HomeKit Bridge via its
Configure → Include entities screen, but Home Assistant will log a warning
recommending a separate accessory-mode pairing instead, since bridged locks
can become unexpectedly unavailable. Prefer the dedicated-accessory approach
above when possible.
