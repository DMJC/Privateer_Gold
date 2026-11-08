# Privateer Gold
Privateer Gemini Gold - Updated for Modern releases of the Vegastrike engine.
It is not intended to build/release engine binaries at this time, this repository exists so that the community can benefit from access to the Privateer Gemini Gold content updated to run on modern systems.

# Status
The game is playable end to end on Vega Strike 0.9.1 with Python 3: new game and saved games, trading, the
mission computer and fixers (up to three missions), combat, the nav computer, ship dealer and repairs, comms and
the intro movie. It still needs a patched engine (below) until those fixes are accepted upstream.

What changed and why: [docs/PORT_NOTES.md](docs/PORT_NOTES.md) (each change is also its own commit with the reason).

# Engine
Use Vega Strike 0.9.1 with the Privateer Gold fixes, branch `privateer-gold-0.9.1` of
https://github.com/JesseWBDL/Vega-Strike-Engine-Source (based on the `v0.9.1` tag). The engine must be built
with FFmpeg for the intro movie; `engine/vcpkg.json` on that branch pulls it in. With an engine built without
FFmpeg, set `intro_movie` to `false` in `vegastrike.config`.

# Installation
- Clone this repository: `git clone https://github.com/DMJC/Privateer_Gold`
- Build the engine above (see its README, "Compiling Vega Strike") and copy the binaries, with their runtime
  libraries, into `Privateer_Gold/bin`.
- Run the game from the Privateer_Gold folder: `./privateer.sh` (Linux/macOS), `privateer.bat` (Windows), or
  `./bin/vegastrike-engine -d.`
