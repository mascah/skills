---
type: capability
id: autopilot
status: draft
updated: 2026-09-09
---
## Behavior
The autopilot chooses an orbit range and applies damage per [[tick]]. See [[D-0001-adaptive-autopilot]].

## Acceptance
- [x] Enabling engagement orbits the target.
- [ ] Engage range is shown and changeable.

## Code
- crates/sim/src/autopilot.rs
