# Privateer Gemini Gold on Vega Strike 0.9.1: port notes

This is the change log for the port. Every item below is a separate commit whose message gives the details; this
page is the overview. The rule for the port is faithfulness: the PGG 1.03 behaviour first, then the 1993
Privateer Playguide.

## Engine changes (Vega Strike, branch `privateer-gold-0.9.1`)

Based on tag `v0.9.1`. They fall into three groups for sending upstream.

### Bug fixes, safe for every game (good upstream pull requests)
| Commit | What it fixes |
|---|---|
| FFmpeg: port video and audio decoding to the FFmpeg 7 API | The FFmpeg code targeted the pre-4.0 API and no longer built or ran; swscale/swresample linking on MSVC. |
| Video: play FFmpeg cutscenes reliably | Black frames (scaler built before the pixel format was known), A/V clock stuck behind or on frame 0, intro frozen on its last frame. |
| Audio: recover streaming sources after a buffer underrun | Streams died for good after any load stall (full/empty ring confusion). |
| Audio: reopen the output device after sleep, hibernate or unplugging | All sound lost until restart after a laptop slept. |
| Python 3: bind Unit.__bool__ | Null units tested true under Python 3. |
| Missions: fix delayed-load race (+ DelayLoadMission, uncounted_mission_name) | Background missions were killed by the game load they were queued behind. The two additions are new API/config with no default effect. |
| Fix crashes: light maps, meshless halos, faction teardown | Crashes on new-game teardown, when engines lit up with old saves, and on quit. |
| Units: default Upgrades at load, ECM init, ammo and hull fixes | Uninitialised ECM drained reactors; ammo doubled on purchase; shop reported failure after fitting a weapon; repairs never restored the hull. Upgrades column only applies where a data set fills it. |
| Factions: load conversations, comm faces, ship modifiers, contraband | The new XML parser silently dropped all of these. |
| System files: keep each planet's alpha blend mode | Invisible nav points became dockable planets. |
| Weapons: quoted JSON floats, proximity fuse, zero-rate cloak (+ gun_speed scaling) | Weapons fell back to default stats; missiles passed through targets; ships stuck "cloaking". Scaling only differs when `gun_speed` is not 1. |
| Combat: hit sounds at the hit point (+ hide_exploding_ships) | Shield hits were silent. The option is off by default. |

### Changes that alter the default behaviour of every game (need discussion or a config switch first)
| Commit | Change |
|---|---|
| AI: use the live simulation atom and 0.5.1 physics priorities | AI timers ran up to 3x slow and every NPC ran at the lowest physics priority. This is a fix, but it visibly changes how NPCs fly. |
| Text: scale the stroke font above 600px, narrow its space | HUD text no longer shrinks at high resolution; stroke-font spaces are narrower. |
| Nav map and cockpit: classic Privateer console behaviour | Click radius 2.5x, start zoom 2.6/2.0 (was 1.8) and drag-panning off by default; the rest is behind `nav_*` switches. |

### Configuration switches added
All in `graphics` unless noted; the default is the stock behaviour unless stated.

| Switch | Default | Purpose |
|---|---|---|
| `hide_exploding_ships` | false | Do not draw a destroyed ship during its explosion. |
| `nav_links_to_uncharted` | false | Sector map shows faded jump links to uncharted systems. |
| `nav_sector_system_info` | false | Sector map info screen lists the selected system's bases. |
| `nav_click_radius_scale` | 2.5 (changed) | Click hotspot size for map items. |
| `nav_galaxy_zoom`, `nav_system_zoom` | 2.6, 2.0 (changed) | Starting zoom of each map. |
| `nav_drag_pan` | false (changed) | Allow dragging the map around. |
| `nav_button_label_<n>`, `nav_button_label_matte` | empty, true | Mod-defined console button labels. |
| `font_reference_height` | 600 (changed) | Height above which the stroke font scales up. |
| `stroke_space_width` | 0.3 (changed) | Stroke-font space width as a fraction of 'W'. |
| `general/uncounted_mission_name` | empty | A menu mission left out of the mission count. |
| `physics/fixed_system_priority_velocity_cutoff` | 50 | Re-enabled 0.5.1 setting. |

## Data and script changes (this repository, branch `vegastrike-0.9.1-port`)
| Commit | What it fixes |
|---|---|
| Ignore Python bytecode, engine binaries and runtime data | Stale committed `.pyc` files; `/bin/` and `/.privgold100/` are local. |
| Python 3: fix the remaining Python 2 constructs | print/exec/imp/string.join/has_key/sort/reduce/integer division and similar. |
| Intro: play the introduction movie in the engine | GUIVideoTexture, skippable intro, `privateer.bat`. |
| Start the dynamic universe after every game load | Empty universe after loading older saves; launches into empty space; menu mission built without a player; Quine save-name editor. |
| New_Game: empty the malformed missionstring section | Loader bailed on every new game. |
| Units: regenerate units.json by column name; full radar cones | ~30 shifted columns (0% shields, broken radar), Upgrades column lost; T/R cycles all ships in range. |
| Ship dealer: sell missiles one at a time | One click sold the whole rack. |
| Meshes: zero the supernova halo material | New games crashed drawing engine halos. |
| Nav console: hide the button overlay meshes | Thin labels drawn over the console's own printed labels. |
| Config: PGG 1.03 game speed, classic nav map, intro, mission limit | `game_speed` .1 as in 1.03, the switches above turned on, three missions. |

## Known issues
- Loading the old "Autosave" save that has no ship file crashes in the NVIDIA GL driver while loading textures.
- Missiles move jerkily.
- Some NPC taunts mix factions' voices.
- Jump-point labels overlap on the system map.
- NPCs being hit play no hit sounds (0.5.1 played them).
- "Error picking comm animation" is logged for five factions without comm animations.
