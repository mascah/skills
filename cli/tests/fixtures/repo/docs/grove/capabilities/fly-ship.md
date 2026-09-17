---
type: capability
id: fly-ship
status: settled
updated: 2026-09-10
---
## Behavior
The pilot issues [[intent|intents]] and the server moves the ship each [[tick]].

## Acceptance
- [x] Approach, orbit, stop, and warp intents move the ship.

## Code
- crates/sim/src/autopilot.rs
- client/src/hud.ts
