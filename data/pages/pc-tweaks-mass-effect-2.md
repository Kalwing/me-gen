---
title: PC Tweaks (Mass Effect 2)
url: https://masseffect.fandom.com/wiki/PC_Tweaks_(Mass_Effect_2)
game: Mass Effect 2
type: lore
characters: []
scraped: '2026-08-28'
---

Mass Effect 2 is based on Unreal Engine 3 and many settings can be modified in a way similar to Mass Effect, allowing the user to mod, tweak or cheat. Unlike the first Mass Effect, Mass Effect 2's in\-game console is locked in a more serious way, but a multitude of effects and in\-game commands can be activated through editing configuration files.

**Disclaimer:** The Mass Effect Wiki does not promote, vouch for, or otherwise endorse the use of any third\-party software not authorized by BioWare or Electronic Arts. Any such software, programs, applications, or files linked or mentioned in this article is done strictly for reference purposes. Anyone choosing to use third\-party software does so at their own risk.

*See also: PC Tweaks, PC Tweaks (Mass Effect 3\)*
## Preface

### Backup Your Career

Using the modifications described in this article may alter your career permanently. It is recommended to backup your career for the option to revert back later on. The career files are located at:

**Windows XP:**

*X:\\Documents and Settings\\%Username%\\My Documents\\BioWare\\Mass Effect 2\\Save*

**Windows Vista/7:**

*X:\\Users\\%Username%\\Documents\\BioWare\\Mass Effect 2\\Save*

Where X is the drive letter where your Windows system is installed on (usually C:), and %Username% \- username that you are logging into the system with.

The career folders are named in the format *John\_31\_Soldier\_060310* (first name, psych profile/history, class, date of creation). The ME1 folder contains the Mass Effect save files transferred over by ME2 Configuration Utility.

There is also a profile file called *Player1\.prf* under the same folder in *%Username%\\Documents\\BioWare\\Mass Effect 2\\BIOGame\\Profile* that you may want to backup. This file stores your achievements and bonus power unlocks.

### Disabling DLC Integrity Check

Some tweaks described in this article require editing (or patching) of DLC files. This may cause the game to detect that the DLC is "not authorized". If you experience such error, you may need to do some DLL patching.

**Legendary Edition:**  DLC integrity is no longer checked in the Legendary Edition.

## Enabling console

Mass Effect 2 console for the original game can be enabled by using three different methods:

- DLL patching tool mentioned above simultaneously enables in\-engine console (default keys: TAB, Tilde). So if you already have that installed, you don't need to do anything else. This is the easiest way.

- Automatically patch main game configuration file (SFXGame.pcc) to remove the lock of game\-based console (console use settings from Coalesced.ini). The program for patching can be found here.

- (As of the Newest Patch this no longer works) Manually patch MassEffect2\.exe to enable engine\-locked console (console use default settings). This method requires HEX editor and recommended for advanced users only. Basic instructions are here however are missing a fair amount of detail. Step by step guide is as follows:
	- Download HxD, which is a hex editor program.
	- Open MassEffect2\.exe in HxD, which can be found in \<Game Directory\>/Binaries.
	- Scroll down to offset row E21730\. Use page up and page down to scroll faster.
	- Under columns 04 to 06, the values should read 70 B4 56\. Typing over the current values, replace them with C0 0C 54\.
	- Hit save, and close HxD.

**Legendary Edition:**  For Legendary Edition, the only current way to enable the console is to install the binkw64 proxy. Compiled dll can be installed directly via ME3Tweaks Mod Manager (Tools \-\> Bink bypasses submenu). Alternatively, it can be compiled manually from the source published GitHub.

Note: press "\~", tilde key to open 3/4 console in game. "tab" for single bar console.

## Commands

*See also: PC Tweaks\#Commands*

| Command | Description | Example |
| --- | --- | --- |
| **ce hench\_empty** | Remove squadmates from party | `ce hench_empty` |
| **ce hench\_picksquad** | Bring up the squad selection screen. After using this command, dialog and music may be disabled until you close and reopen the game. | `ce hench_picksquad` |
| **GiveTalentPoints** *int* value | Give (remove) talent points | `GiveTalentPoints -5` |
| **GiveXP** *int* value | Give experience | `GiveXP 1000` |
| **GivePower** *target* power | Temporarily give a power to the target *(power list)* Does not persist through loading screens. | `GivePower self SFXPower_Shockwave` |
| **RemovePower** *target* power | Remove a power from the target | `RemovePower self SFXPower_Shockwave` |
| **SetRank** *target* power *int* rank | Set the rank of the target's power | `SetRank self SFXPower_Shockwave 3` |
| **GiveItem** target object | Give a specific object to the target *(weapon list)* | `GiveItem Self HeavyPistol` |
| **GiveSuperGun** | Give 99999 ammo clip and increases damage tremendously | `GiveSuperGun` |
| **SetParagon** *int* value | Set paragon points | `SetParagon 3000` |
| **SetRenegade** *int* value | Set renegade points | `SetRenegade 3000` |
| **EnablePowerCooldown** *bool* value | Set power cooldown (not working with class\-specific skills) | `EnablePowerCooldown 1` |
| **God** | Toggle godmode. Does not protect against hardcoded death scenarios and wears off when switching to flycam. | `God` |
| **KillTarget** | Kill the target under the reticle | `KillTarget` |
| **KillEnemies** | Kill all enemies | `KillEnemies` |
| **KillParty** | Kill henchmen | `KillParty` |
| **StasisParty** | Freeze henchmen | `StasisParty` |
| **KillSelf** / **Suicide** | Kill the player | `KillSelf` |
| **InitAmmo** *int* value | Set ammo | `InitAmmo 999` |
| **InitMedigel** *int* value | Set Medi\-gel | `InitMedigel 5` |
| **InitProbes**  *int* value | Set probes | `InitProbes 50` |
| **InitFuel**  *int* value | Set fuel amount | `InitFuel 500` |
| **InitCredits** *int* value | Set credits amount | `InitCredits 10000` |
| **InitPalladium** *int* value | Set Palladium amount | `InitPalladium 1000` |
| **InitIridium** *int* value | Set Iridium amount | `InitIridium 1000` |
| **InitEezo** *int* value | Set Element Zero amount | `InitEezo 1000` |
| **InitPlatinum** *int* value | Set Platinum amount | `InitPlatinum 1000` |
| **ToggleFlyCam** | Toggle free camera mode | `ToggleFlyCam` |
| **Shot** | Take screenshot | `Shot` |
| **TiledShot** *int* multiplier *int* overlapPixels | Take screenshot at many times the screen resolution. Postprocessing effects are rendered at default resolution rather than the target one, however, which may result in visual artifacts around the 'tile' edges. | `TiledShot 3x3` \- with a grid of 3x3 (input 1440x900, result 4320x2700\)`TiledShot 2` \- twice the size of dimensions`TiledShot 2 200` \- twice the dimension, overlaps 200 pixels from a grid cell |
| **PlayersOnly** / **TogglePlayersOnly** | Freeze the game | `PlayersOnly` |
| **ShowHUD** / **ToggleHUD** | Toggle most parts of the HUD. Retains the quickslot bar. | `ToggleHUD` |
| **Show** *keyword* | Multipurpose client command for controlling display elements on the screen. **Show Lensflares**: Toggles lens flare rendering and highlighting on Bypass objects. **Show Particles**: Toggle particle rendering on/off. Removes prop GUIs. **Show Postprocess**: Enable/disable postprocessing effects. Off results in washed\-out colors and therefore not recommended for screencapping. **Show Scaleform**: Toggle Scaleform elements (text, quick slots, player HUD). Covers more elements than ShowHUD. **Show Vignette**: Toggles the vignette effect on or off. Mass Effect Legendary Edition only. | `Show Lensflares` `Show Particles` `Show Postprocess` `Show Scaleform` `Show Vignette` |
| **SloMo** *float* multiplier | Change the game speed | `SloMo 2` |
| **FOV** *int* fovDegrees | Modify field of view. Overrides every game\-initiated FOV change (sprint, cutscenes) until the load screen. | `FOV 80` |
| **UnlockAchievement** *int* ID | Unlock an achievement *(achievement list)* | `UnlockAchievement 3` |
| **At** / **Open** *string* value | Teleport to the level *(level list)* | `At BioP_ProCer` |
| **Stat FPS** | Toggle the framerate display | `Stat FPS` |
| **SetIntByName** *string* nmVar *int* value | Set integer variable (use to unlock upgrades) *(upgrade list)* | `SetIntByName Tec_AutoPistol 5` |
| **SetBoolByName** *string* nmVar *bool* value | Set boolean variable | `SetBoolByName Bloom 1` |
| **SetBoolByID** *int* nmVar *bool* value | Set story boolean variable | `SetBoolByID 27975 1` |
| **Exec** *filename* | Execute a file under the Binaries folder (type commands inside, and the game will run them) | `Exec powers.txt` |
| **Profile combat** *target* | Show combat data for the target | `Profile combat self` |
| **Profile power** *target* | Show powers data for the target | `Profile power target` |
| **Profile anim** *target* | Show animation data for the target | `Profile anim SFXPawn_Garrus_01_0` |
| **Profile camera** *target* | Show camera data for the target | `Profile camera self` |
| **Profile tech** | Show upgrades data | `Profile tech` |
| **Profile vehicle** | Show vehicle data | `Profile vehicle` |
| **Profile none** | Clear the screen from profile data | `Profile none` |
| **set** *functionname* *variablename* *value* | A versatile command that allows on\-the\-fly changing of hardcoded game values like in `coalesced.ini`. Persists until game exit. | `set SFXGame.BioPlayerSelection SelectionFarRange 1` \- change distance to show blue bounding box on highlighted items. Default is 3000\. `set SFXGame.BioPlayerSelection SelectionCloseRange 1` \- change distance to show orange bounding box on highlighted items. Default is 1500\. `Set BioCameraBehaviorFree m_fMovementScalar float` \- fine\-tune the camera's directional speed. Does not work for the Legendary Edition of the first game but works fine in all other versions. |

### Achievements

Full unlock: `Command=("UnlockAchievement 0 | UnlockAchievement 1 | UnlockAchievement 2 | UnlockAchievement 3 | UnlockAchievement 4 | UnlockAchievement 5 | UnlockAchievement 6 | UnlockAchievement 7 | UnlockAchievement 8 | UnlockAchievement 9 | UnlockAchievement 10 | UnlockAchievement 11 | UnlockAchievement 12 | UnlockAchievement 13 | UnlockAchievement 14 | UnlockAchievement 15 | UnlockAchievement 16 | UnlockAchievement 17 | UnlockAchievement 18 | UnlockAchievement 19 | UnlockAchievement 20 | UnlockAchievement 21 | UnlockAchievement 22 | UnlockAchievement 23 | UnlockAchievement 24 | UnlockAchievement 25 | UnlockAchievement 26 | UnlockAchievement 27 | UnlockAchievement 28 | UnlockAchievement 29 | UnlockAchievement 30 | UnlockAchievement 31 | UnlockAchievement 32 | UnlockAchievement 33 | UnlockAchievement 34 | UnlockAchievement 35 | UnlockAchievement 36 | UnlockAchievement 37 | UnlockAchievement 38 | UnlockAchievement 39 | UnlockAchievement 40 | UnlockAchievement 41 | UnlockAchievement 42 | UnlockAchievement 43 | UnlockAchievement 44 | UnlockAchievement 45 | UnlockAchievement 46 | UnlockAchievement 47 | UnlockAchievement 48 | UnlockAchievement 49 | UnlockAchievement 50 | UnlockAchievement 51 | UnlockAchievement 52 | UnlockAchievement 53 | UnlockAchievement 54 | UnlockAchievement 55 | UnlockAchievement 56 | UnlockAchievement 57 | UnlockAchievement 58 | UnlockAchievement 59 | UnlockAchievement 60 | UnlockAchievement 61")`

| \# | Achievement | Note |
| --- | --- | --- |
| 0 | Highly Trained |  |
| 1 | Missing In Action | Normandy is destroyed (intro) |
| 2 | Very Elusive | Shepard joins Cerberus |
| 3 | The Convict | Recruit Jack |
| 4 | The Krogan | Recruit Grunt |
| 5 | The Archangel | Recruit Garrus |
| 6 | The Professor | Recruit Mordin |
| 7 | The Quarian | Recruit Tali |
| 8 | The Justicar | Recruit Samara |
| 9 | The Assassin | Recruit Thane |
| 10 | Colony Defense |  |
| 11 | The Prodigal | Miranda's loyalty mission |
| 12 | Ghost of the Father | Jacob's loyalty mission |
| 13 | Catharsis | Jack's loyalty mission |
| 14 | Battlemaster | Grunt's loyalty mission |
| 15 | Fade Away | Garrus' loyalty mission |
| 16 | The Cure | Mordin's loyalty mission |
| 17 | Treason | Tali's loyalty mission |
| 18 | Doppelganger | Samara's loyalty mission |
| 19 | Cat's in the Cradle | Thane's loyalty mission |
| 20 | Friend or Foe | Recover Legion |
| 21 | A House Divided | Legion's loyalty mission |
| 22 | Ghost Ship |  |
| 23 | Suicide Mission | Use Omega\-4 Relay |
| 24 | Mission Accomplished | Finish the game |
| 25 | Against All Odds | Survive suicide mission |
| 26 | Insanity |  |
| 27 | No One Left Behind | No\-one dies in suicide mission |
| 28 | Long Service Medal | Finish game twice or use character from ME1 |
| 29 | Paramour |  |
| 30 | Head Hunter | Kill the thresher maw |
| 31 | Brawler |  |
| 32 | Big Game Hunter |  |
| 33 | Tactician |  |
| 34 | Master at Arms |  |
| 35 | Merciless |  |
| 36 | Overload Specialist |  |
| 37 | Warp Specialist |  |
| 38 | Incineration Specialist |  |
| 39 | Operative |  |
| 40 | Agent |  |
| 41 | Prospector |  |
| 42 | Explorer |  |
| 43 | Power Gamer |  |
| 44 | Scholar |  |
| 45 | Technician |  |
| 46 | Weapon Specialist |  |
| 47 | Scientist |  |
| 48 | Fashionista |  |
| 49 | Power Full |  |
| 50 | Revenge! | Zaeed's loyalty mission |
| 51 | Broke, Blind, and Bedlam | Kasumi's loyalty mission |
| 52 | Data Hound | Overlord DLC |
| 53 | Digital Exorcist | Overlord DLC |
| 54 | Detail Orientated | Lair of the Shadow Broker DLC |
| 55 | Most Dangerous Game | Lair of the Shadow Broker DLC |
| 56 | Heart of Darkness | Lair of the Shadow Broker DLC |
| 57 | The Hard Way | Lair of the Shadow Broker DLC |
| 58 | Catching Up | Lair of the Shadow Broker DLC |
| 59 | The Ultimate Sacrifice | Arrival DLC |
| 60 | Last Stand | Arrival DLC |
| 61 | Covert Action | Arrival DLC |

### Upgrades

Full unlock (with Squad Upgrades): `Command=("SetIntByName Tec_AutoPistol 5 | SetIntByName Tec_AutoPistolR1 1 | SetIntByName Tec_AutoPistolR2 1 | SetIntByName Tec_AssaultRifle 5 | SetIntByName Tec_AssaultRifleR1 1 | SetIntByName Tec_AssaultRifleR2 1 | SetIntByName Tec_BioticUpgrade 5 | SetIntByName Tec_BioticR1 1 | SetIntByName Tec_BioticR2 1 | SetIntByName Tec_HeavyAmmo 5 | SetIntByName Tec_HeavyPistol 5 | SetIntByName Tec_HeavyPistolR1 1 | SetIntByName Tec_HeavyPistolR2 1 | SetIntByName Tec_LegionUpgrade 2 | SetIntByName Tec_MediGel 6 | SetIntByName Tec_MediGelR1 1 | SetIntByName Tec_MediGelR2 1 | SetIntByName Tec_MiniGameDecrypt 1 | SetIntByName Tec_MiniGameHack 1 | SetIntByName Tec_ShepardHealth 5 | SetIntByName Tec_ShepardR1 1 | SetIntByName Tec_ShepardR2 1 | SetIntByName Tec_Shield 5 | SetIntByName Tec_ShieldR1 1 | SetIntByName Tec_ShieldR2 1 | SetIntByName Tec_Shotgun 5 | SetIntByName Tec_ShotgunR1 1 | SetIntByName Tec_ShotgunR2 1 | SetIntByName Tec_SniperRifle 5 | SetIntByName Tec_SniperRifleR1 1 | SetIntByName Tec_SniperRifleR2 1 | SetIntByName Tec_TechUpgrade 5 | SetIntByName Tec_TechR1 1 | SetIntByName Tec_TechR2 1 | SetIntByName Tec_BovineFortitude 1 | SetIntByName Tec_QuarianShields 1 | SetIntByName Tec_GruntShotgun 2 | SetIntByName Tec_GruntUpgrade 2 | SetIntByName Tec_JackUpgrade 1 | SetIntByName Tec_LegionSniper 2 | SetIntByName Tec_LegionUpgrade 2 | SetIntByName Tec_MordinUpgrade 1")`

**Note:**  After using the code, any collected upgrade will be added as an extra upgrade ('10' is upper limit).

#### Weapon Upgrades

| Name | Description | Plot ID and Level |
| --- | --- | --- |
| **Tec\_AutoPistol** | Submachine Gun Damage (Microfield Pulsar) | `Tec_AutoPistol 5` |
| **Tec\_AutoPistolR1** | SMG Shield Piercing (Phasic Jacketing) | `Tec_AutoPistolR1 1` |
| **Tec\_AutoPistolR2** | SMG Extra Rounds (Heat Sink Capacity) | `Tec_AutoPistolR2 1` |
| **Tec\_AssaultRifle** | Assault Rifle Damage (Kinetic Pulsar) | `Tec_AssaultRifle 5` |
| **Tec\_AssaultRifleR1** | Assault Rifle Penetration (Tungsten Jacket) | `Tec_AssaultRifleR1 1` |
| **Tec\_AssaultRifleR2** | Assault Rifle Accuracy (Targeting VI) | `Tec_AssaultRifleR2 1` |
| **Tec\_BioticUpgrade** | Biotic Damage (Hyper\-Amp) | `Tec_BioticUpgrade 5` |
| **Tec\_BioticR1** | Biotic Duration (Neural Mask) | `Tec_BioticR1 1` |
| **Tec\_BioticR2** | Biotic Cooldown (Smart Amplifier) | `Tec_BioticR2 1` |
| **Tec\_HeavyAmmo** | Heavy Weapon Ammo Upgrade (Microfusion Array) | `Tec_HeavyAmmo 5` |
| **Tec\_HeavyPistol** | Heavy Pistol Damage (Titan Pulsar) | `Tec_HeavyPistol 5` |
| **Tec\_HeavyPistolR1** | AP Heavy Pistol (Sabot Jacketing) | `Tec_HeavyPistolR1 1` |
| **Tec\_HeavyPistolR2** | Heavy Pistol Critical (Smart Rounds) | `Tec_HeavyPistolR2 1` |
| **Tec\_MediGel** | Medi\-Gel Capacity (Microscanner) | `Tec_MediGel 5` |
| **Tec\_MediGelR1** | Trauma Module (Medical VI) | `Tec_MediGelR1 1` |
| **Tec\_MediGelR2** | Emergency Shielding (Shield Harmonics) | `Tec_MediGelR2 1` |
| **Tec\_ShepardHealth** | Heavy Skin Weave (Lattice Shunting) | `Tec_ShepardHealth 5` |
| **Tec\_ShepardR1** | Heavy Bone Weave (Skeletal Lattice) | `Tec_ShepardR1 1` |
| **Tec\_ShepardR2** | Heavy Muscle Weave (Microfiber Weave) | `Tec_ShepardR2 1` |
| **Tec\_Shield** | Damage Protection (Ablative VI) | `Tec_Shield 5` |
| **Tec\_ShieldR1** | Redundant Field Generator (Burst Regeneration) | `Tec_ShieldR1 1` |
| **Tec\_ShieldR2** | Hard Shields (Nanocrystal Shield) | `Tec_ShieldR2 1` |
| **Tec\_Shotgun** | Shotgun Damage (Synchronized Pulsar) | `Tec_Shotgun 5` |
| **Tec\_ShotgunR1** | Shotgun Shield Piercing (Microphasic Pulse) | `Tec_ShotgunR1 1` |
| **Tec\_ShotgunR2** | Shotgun Extra Rounds (Thermal Sink) | `Tec_ShotgunR2 1` |
| **Tec\_SniperRifle** | SniperRifleDamage (Scrum Pulsar) | `Tec_SniperRifle 5` |
| **Tec\_SniperRifleR1** | AP Sniper Rifle (Tungsten Sabot Jacket) | `Tec_SniperRifleR1 1` |
| **Tec\_SniperRifleR2** | Sniper Headshot Damage (Combat Scanner) | `Tec_SniperRifleR2 1` |
| **Tec\_TechUpgrade** | Tech Damage (Multicore Umplifier) | `Tec_TechUpgrade 5` |
| **Tec\_TechR1** | Tech Duration (Custom Heuristics) | `Tec_TechR1 1` |
| **Tec\_TechR2** | Tech Cooldowns (Hydra Module) | `Tec_TechR2 1` |
| **Tec\_BovineFortitude** | Calcified Endoskeleton (Bovine Fortitude)]] | `Tec_BovineFortitude 1` |
| **Tec\_QuarianShields** | Quarian Shield Capacitor (Cyclonic Array)]] | `Tec_QuarianShields 1` |
| **Tec\_HackModule** | Hack Module for hacking mini game | `Tec_MiniGameHack 1` |
| **Tec\_BypassModule** | Bypass Module for the bypass mini game | `Tec_MiniGameDecrypt 1` |

These upgrades can't be normally obtained.

#### Squad Member Upgrades

| **Tec\_GruntShotgun** | Krogan Shotgun (Custom Claymore) \[Grunt] | `Tec_GruntShotgun 2` |
| --- | --- | --- |
| **Tec\_GruntUpgrade** | Krogan Vitality (Microfiber Weave) \[Grunt] | `Tec_GruntUpgrade 2` |
| **Tec\_JackUpgrade** | Subject Zero Biotic Boost (Multicore Implants) \[Jack] | `Tec_JackUpgrade 1` |
| **Tec\_LegionSniper** | Geth Sniper Rifle (Custom Widow Rifle) \[Legion] | `Tec_LegionSniper 2` |
| **Tec\_LegionUpgrade** | Geth Shield Strength 2/2 (Cyclonic Particles) \[Legion] | `Tec_LegionUpgrade 2` |
| **Tec\_MordinUpgrade** | Mordin Omni\-Tool \[Mordin] | `Tec_MordinUpgrade 1` |

#### Ship Upgrades

**Warning:**  It is highly recommended to **not** use the codes below, because those may be unlocked but during the Suicide Mission they won't have any effect and squad members **will** die. Also the facial scars can't be healed.

| **Tec\_FaceLift** | Medical\-Bay Upgrade (Dermal Regeneration) | `Tec_FaceLift 1` |
| --- | --- | --- |
| **Tec\_ShipArmor** | Heavy Ship Armor (Silaris Armor Tech) | `Tec_ShipArmor 1` |
| **Tec\_ShipGun** | Thanix Cannon (Particle Cannon) | `Tec_ShipGun 1` |
| **Tec\_ShipScanner** | Advanced Mineral Scanner (Argus Scanner Array) | `Tec_ShipScanner 1` |
| **Tec\_ShipShield** | Multicore Shielding (Cyclone Shield Tech) | `Tec_ShipShield 1` |
| **Tec\_ShipProbes** | Modular Probe Bay (Probe Booster) | `Tec_ShipProbes 1` |

## Configuration file

Coalesced.ini is the main configuration files, designed for easy adjusting the game parameters stored in .pcc files. The file can be found here:

**Default location:**

*C:\\Program Files\\Mass Effect 2\\BioGame\\Config\\PC\\Cooked\\Coalesced.ini*

1. **Make a backup before you even move your cursor over it.**
2. **You cannot edit it with Notepad, or the game will crash on load.**
3. **Make sure the modified file is exactly the same size as the original, or the game may crash on load.** This may depend on your version of the game. You can do this by adding extra spaces to the end of a line, or deleting unnecessary lines from the international keybindings.

If you want to edit the file manually, you will need a text editor that can handle UNIX\-format files (e.g., Notepad\+\+) and a way of "rebuilding" Coalesced.ini after your edits.

Another approach is using a specific utility such as the Mass Effect 2 Coalesced Editor for making changes. The utility takes care of the file's format and CRC, and you can add/remove settings without having to care about the file's length.

### BIOGame

\[SFXGame.SFXGame]

| Variable | Description |
| --- | --- |
| **StormRegen** | regeneration speed of combat storm stamina |
| **StormRegenNonCombat** | regeneration speed of non\-combat storm stamina |
| **StormStamina** | determines how long Shepard can storm during combat |
| **StormStaminaNonCombat** | determines how long Shepard can storm outside of combat |

### BIOInput

This section is where binds can be added to the game (or removed. Be careful when doing this.)
There are several subsections which describe key bindings during various "modes" in the game.

#### Subsections

| Section | Description |
| --- | --- |
| **\[SFXGame.SFXGameModeBase]** | All SFXGameModes inherit from this class. Bindings placed here would be usable in all modes, including engine\-driven cinematics (making this the ideal place for screenshot and fast\-forward bindings). |
| **\[SFXGame.SFXGameModeDefault]** | This is the "Default" game mode, where you control Shepard and can move them around. |
| **\[SFXGame.SFXGameModeCommand]** | This mode is activated when in "command mode," where the game is paused, allowing you to give orders to your squad |
| **\[SFXGame.SFXGameModeConversation]** | This is the game mode used when in conversations. |
| **\[SFXGame.SFXGameModeCinematic]** | This mode is used when in\-game, non\-interactive cinematics are displayed. (While the shuttle lands on a planet, for instance.) |
| **\[SFXGame.SFXGameModeGalaxy]** | This mode is used while the Galaxy Map is open |
| **\[SFXGame.SFXGameModeGUI]** | This mode is used for hacking and decryption mini\-games, as well as menus. |
| **\[SFXGame.SFXGameModeMovie]** | This mode is used when pre\-rendered movies are being played |
| **\[SFXGame.SFXGameModeOrbital]** | This mode is used when scanning planets. Aside from bindings, several values which govern the speed of the scanning reticle are found here. |
| **\[SFXGame.SFXGameModeVehicle]** | This game mode is used when the player is in the Hammerhead. |

#### Bindings format

To add a new bind to any of the above sections, use the format

`Bindings=( Name= "Key name", Command="Command", Ctrl="True", Shift="True", Alt="True")`

Ctrl, Shift, Alt commands are optional, if they are not specified default value is "False". The most common use for this is to bind a command to the press of single or combination of keys.

Example: adding this to the \[SFXGame.SFXGameModeDefault] section will allow the player to take screenshots while on foot by pressing F8:
`Bindings=( Name= "F8", Command="Shot" )`

### BIOWeapon

#### Weapon Properties

*See also: \#Weapon List*
In the subsections dealing with weapon properties, there is a "base template" section in \[SFXGame.SFXWeapon] that defines general weapon properties, which are then overridden by specific weapon settings in the other categories if necessary.

At least the following settings can be used (added if not existing by default):

| Variable | Description |
| --- | --- |
| **AccFireInterpSpeed** | Determines how quick accuracy parameters approximate their maximal values |
| **AccFirePenalty** | Determines cone of fire increase per shot from the hip |
| **AdhesionRot** |  |
| **AI\_AccCone\_Max** | Maximal accuracy cone for AI |
| **AI\_AccCone\_Min** | Minimal accuracy cone for AI |
| **AI\_AimDelay** | Time while AI is aiming |
| **AI\_BurstFireCount** | Amount of bursts enemies and henchmen make before returning to cover. First \- minimal number, second is the maximum. |
| **AI\_BurstFireDelay** | Time enemies and henchmen wait between firing bursts from cover |
| **AI\_BurstFireMovingDelay** | Time enemies and henchmen wait between firing bursts when out of cover |
| **AI\_HenchBurstFireMultiplier** |  |
| **AimCorrectionAmount** |  |
| **AmmoPerShot** | Amount of ammo spent per shot |
| **AmmoPrettyName** |  |
| **bAdhesionDuringCam** |  |
| **bAdhesionEnabled** |  |
| **bCanDropAmmo** | Whether weapon drops ammo or not |
| **bCanDropWeapon** |  |
| **bFrictionDistanceScalingEnabled** |  |
| **bFrictionEnabled** |  |
| **bInfiniteAmmo** | Infinite ammo on/off (must reload, but spare ammo is not decreased) |
| **bIsAutomatic** | The weapon doesn't require to rearrange the trigger to keep firing (considers RateOfFire parameter) |
| **bUpgradesBasicWeapon** | Use parameters from the basic weapon type template |
| **BurstRefireTime** | Delay before next burst (makes RateOfFire parameter irrelevant) |
| **BurstRounds** | Number of rounds per burst (set to 0 for full auto) |
| **bUseSniperCam** | Use sniper scope for a weapon |
| **bZoomSnapEnabled** |  |
| **CamInputAdhesionDamping** |  |
| **CoverLeanPositions** |  |
| **CrosshairRange** | Crosshair size (Min,Max) |
| **Damage** | Base damage |
| **DamageAI** | Damage multiplier for enemies |
| **DamageHench** | Damage multiplier for squad members |
| **fAmmoMultiplier** | Multiplier for dropped ammo (?) |
| **GeneralDescription** | ID number for text to show in game to describe the weapon |
| **GUIClassDescription** |  |
| **GUIClassName** |  |
| **GUIImage** | Image of the weapon, that will be shown upon acquisition, when choosing weapon in weapons locker and codex |
| **IconRef** | Image ID to be shown on HUD during a fight |
| **InitialMagazines** | The amount of ammo (x MagSize) given when starting a mission |
| **LowAmmoSoundThreshold** | Threshold for low ammo warning |
| **MagSize** | Size of magazine |
| **MaxAimError** | Maximum bullet drift |
| **MaxSpareAmmo** | Maximum amount of spare ammo |
| **MaxZoomAimError** | Maximum bullet drift when zooming |
| **MinAimError** | Minimum bullet drift |
| **MinZoomAimError** | Minimum bullet drift when zooming |
| **NoAmmoFireSoundDelay** | Delay before pulling the trigger and playing "click" sound for weapon without ammo |
| **PrettyName** | In\-game name for the weapon, requires string ID from .tlk |
| **RateOfFire** | Rate of fire |
| **RateOfFireAI** | Rate of fire for enemies and henchmen |
| **Recoil** | Recoil |
| **RecoilCap** | Recoil cap |
| **RecoilFadeSpeed** | Rate of recoil fade |
| **RecoilInterpSpeed** | Shakiness of the screen when firing |
| **RecoilYawBias** | Diagonal deviation |
| **RecoilYawFrequency** |  |
| **RecoilYawScale** |  |
| **RecoilZoomFadeSpeed** | Rate of recoil fade in zoom mode |
| **ReloadFailureDuration** | Time which is required for weapon to be reloaded |
| **ShortDescription** | Text line ID number for description in the command menu |
| **ShowTracerDistance** |  |
| **SteamSoundThreshold** | Amount of ammo to be left in clip before playing "running low" sound along with normal shooting sound |
| **TracerSpawnOffset** | Frequency of tracers (visible bullets) |
| **ZoomAccFireInterpSpeed** | Determines how fast weapon parameters approximate their maximal values in zoom mode |
| **ZoomAccFirePenalty** | Determines cone of fire increase per shot in zoom mode |
| **ZoomCrosshairRange** | Crosshair size when zooming (Min,Max) |
| **ZoomFOV** | Sniper Scope Magnification (Bigger Number\=Smaller Zoom) |
| **ZoomRecoil** | Recoil when zooming |

#### Shield Properties

All non\-template shield sections inherit parameters from the base section.

| Section | Description |
| --- | --- |
| **\[SFXGame.SFXShield\_Base]** | Base shield template |
| **\[SFXGame.SFXShield\_Armour]** | AI armor |
| **\[SFXGame.SFXShield\_Armour\_Player]** | Player's armor |
| **\[SFXGame.SFXShield\_Biotic]** | AI barrier |
| **\[SFXGame.SFXShield\_Biotic\_Player]** | Player's biotic barrier |
| **\[SFXGame.SFXShield\_Energy]** | AI kinetic barrier |
| **\[SFXGame.SFXShield\_Energy\_Player]** | Player's kinetic barrier |
| **\[SFXGame.SFXShield\_GethEnergy]** | AI geth energy shield |
| **\[SFXGame.SFXShield\_GethEnergy\_Player]** | Player's geth energy shields |
| **\[SFXGame.SFXShield\_Player]** | Player's shield template |

| Variable | Description |
| --- | --- |
| **bAbsorbDamageOnBreak** | Shield absorbs full damage on breaking |
| **bFastCoverRegen** | Shield recharges fast when in cover |
| **bRechargeable** | Shield is rechargeable |
| **DamageGateInterval** | Amount of damage shields can take before collapsing |
| **MaxShields** |  |
| **PartialBreakPct** |  |
| **ShieldDisplayName** | The ID of the line in a .tlk file |
| **ShieldPointsPerBar** |  |
| **ShieldRechargeTime** | Time it takes for shields to recharge |
| **ShieldRegenDelay** | Delay before shields recharge |

## Tweaks

### Ability to take only certain weapon types

Now you'll be able to pick only certain weapon types like in Mass Effect 3\.

\[SFXGame.SFXPlayerSquadLoadoutData]

`AssaultRifles=(ClassName="SFXGame.SFXWeapon_AssaultRifle_Base")

Shotguns=(ClassName="SFXGame.SFXWeapon_Shotgun_Base")

SniperRifles=(ClassName="SFXGame.SFXWeapon_SniperRifle_Base")

AutoPistols=(ClassName="SFXGame.SFXWeapon_AutoPistol_Base")

HeavyPistols=(ClassName="SFXGame.SFXWeapon_HeavyPistol_Base")

HeavyWeapons=(ClassName="SFXGame.SFXHeavyWeapon")`

\[SFXGame.SFXWeapon]

`IconRef=0

GUIImage=GUI_Codex_Images.AssaultRifles_512

PrettyName=339532

GeneralDescription=0

ShortDescription=0`

### Change Player Shield Recharge time

You can modify shield recharge time to increase/decrease combat pace to suit your play style:

\[SFXGame.SFXShield\_Base]

`ShieldRechargeTime=(X=2.0f,Y=2.0f)`

The time shield needed to fully regenerate (in seconds).

`ShieldRegenDelay=(X=5.0f,Y=5.0f)`

The time before shield start regenerating (in seconds).

Change the values to 0\.0 will cause shield unable to regenerate.

This also affects your squad members shield.

### Carrying upgrades to New Game\+

\[SFXGame.SFXGame]

`NGPlusPlotVariables=Tec_AssaultRifle`

You can grab upgrades plot variables above.

### Editing Shepard Template Face Codes

You can add or remove custom Shepard pregenerated codes in the game:

\[SFXGame.BioSFHandler\_NewCharacter]

`MalePregeneratedHeadCodes=`*{Facecode}*

`FemalePregeneratedHeadCodes=`*{Facecode}*

**Note:** If you have Kasumi DLC installed removing standard face codes will not work, because of rewriting section by DLC .ini file. In this case you have to modify DLC .ini directly.

### Changing Power Cooldown Time

Go to appropriate for your difficulty section:

\[SFXGame.SFXDifficulty\_Level2]

`EnemyPowerCooldownMultiplier=1.0`

`SquadPowerCooldownMultiplier=1.0`

Set the values to 0\.0 to completely remove cooldown.

Note1: Level1\=Casual, Level2\=Normal, Level3\=Hard, Level4\=Veteran, Level5\=Insanity. Level6 is not used.

Note2: Cooldown for some powers, such as Adrenaline Rush, is not affected by this parameter.

### Unlocking Weapons

There are three ways of unlocking weapons:

1\. By setting weapon boolean parameters to true

\[SFXGame.SFXGameModeDefault]

`Bindings=( Name="NumPadOne", Command="SetIntByName Wpn_GethPulseRifle 1" )`
To unlock all normal weapons, add: `Bindings=( Name="NumPadOne", Command="SetIntByName Wpn_AssaultRifle2 1 | SetIntByName Wpn_AutoPistol2 1 | SetIntByName Wpn_Locust 1 | SetIntByName Wpn_GethPulseRifle 1 | SetIntByName Wpn_HeavyPistol2 1 | SetIntByName Wpn_Shotgun2 1 | SetIntByName Wpn_SniperRifle2 1" )`
To unlock all heavy weapons, add: `Bindings=( Name="NumPadTwo", Command="SetIntByName Wpn_CryoBlaster 1 | SetIntByName Wpn_GrenadeLauncher 1 | SetIntByName Wpn_NukeLauncher 1 | SetIntByName Wpn_ParticleBeam 1 | SetIntByName Wpn_Flamethrower 1 | SetIntByName Wpn_MissileLauncher 1" )`
To unlock all Collector Ship weapons, add: `Bindings=( Name="NumPadThree", Command="SetIntByName Wpn_SuperAssaultRifle 1 | SetIntByName Wpn_SuperShotgun 1 | SetIntByName Wpn_SuperSniperRifle 1" )`
Unlocked weapons will stay unlocked for subsequent play\-throughs for the current career, and it is possible to get all Collector Ship weapons (although you must still have the proper class to actually equip them).
2\. By removing or changing weapon dependency conditions

\[SFXGame.SFXPlayerSquadLoadoutData]

`AssaultRifles=(ClassName="SFXGameContent_Inventory.SFXWeapon_Needler",UnlockPlotID=Wpn_AssaultRifle2)`
`AssaultRifles=(ClassName="SFXGameContent_Inventory.SFXWeapon_MachineGun",bNotRegularWeaponGUI=true)`
Remove `bNotRegularWeaponGUI` and `UnlockPlotID` parameters.
If you want to make a special weapon available to your squadmates only when you've unlocked the weapon change the line to:
`AssaultRifles=(ClassName="SFXGameContent_Inventory.SFXWeapon_MachineGun",UnlockPlotID=Wpn_SuperAssaultRifle)`
You can use the method to unlock all special weapons for your companions. The M\-300 Claymore's (SFXWeapon\_FlakGun) code is `Wpn_SuperShotgun` and the M\-98 Widow's (SFXWeapon\_MassCannon) is `Wpn_SuperSniperRifle`.
3\. By typing in the command "SetIntByName Wpn\_\[WEAPON NAME] 1" into the console, with \[WEAPON NAME] being whatever the game names the guns. (M\-3 Predator is HeavyPistol, etc.)
To unlock the Revenant Machine Gun, type into the console: `SetIntByName Wpn_SuperAssaultRifle 1`
To unlock the M\-98 Widow, type into the console: `SetIntByName Wpn_SuperSniperRifle 1`

### Unlocking Bonus Powers

\[SFXGame.BioSFHandler\_NewCharacter]

`BonusTalents=(PowerClassName="SFXGameContent_Powers.SFXPower_Barrier_Player,AchievementID=*)`

Change the AchievementID parameter to `AchievementID=1`

### Unlocking Squad Appearances

\[SFXGame.BioSFHandler\_PartySelection]

`1stAppearances=(Tag=hench_miranda,PlotFlag=*)`

Change the PlotFlag parameter to `PlotFlag=-1`

**Note:** If using the ME2 Coalesced Editor SFXGame.BioSFHandler\_PartySelection is located under the BIOUI tab

### Enable joystick move (useful for those who want to use mouse while having access to analog movement)

Locate \[WinDrv.WindowsClient]

Change

```
allowjoystickinput=0
```
 to

```
allowjoystickinput=1
```

locate \[SFXGame.SFXGameModeBase]

Paste in

```
Bindings=(Name="XboxTypeS_LeftX",Command="Axis aStrafe Speed=1.0 DeadZone=0.3")

Bindings=(Name="XboxTypeS_LeftY",Command="Axis aBaseY Speed=1.0 DeadZone=0.3")

Bindings=(Name="XboxTypeS_RightX",Command="Axis aTurn Speed=0.2 DeadZone=0.3")

Bindings=(Name="XboxTypeS_RightY",Command="Axis aLookup Speed=0.2 DeadZone=0.3")
```

Comes in useful for steam controller users or gamepad users who want to bind gyro to a mouse.

### Changing Squad Weapon Loadouts

You are able to define which weapon classes are available to which player classes and companions.

\[SFXGame.SFXPlayerSquadLoadoutData], located under the BIOGame section

`HenchLoadoutInfo=(ClassName=SFXPawn_$SQUADMATE,WeaponClasses=(LoadoutWeapons_HeavyPistols,LoadoutWeapons_Shotguns))`

Replace the `LoadoutWeapons_*` list to a comma\-separated combination of the following:

```
LoadoutWeapons_AssaultRifles
LoadoutWeapons_Shotguns
LoadoutWeapons_SniperRifles
LoadoutWeapons_HeavyPistols
LoadoutWeapons_AutoPistols
LoadoutWeapons_HeavyWeapons
```

### Unlimited Ammo

There are four ways to enable unlimited ammo:

1. Open the properties of a weapon (e.g., `[SFXGameContent_Inventory.SFXWeapon_Needler]` section for the M\-15 Vindicator; see the table below for a full list) and change `bInfiniteAmmo=false` into `bInfiniteAmmo=true`. The weapon will now spend ammo from the magazine and has to be reloaded, but spare ammo will never decrease. Other weapons are unaffected, so you have to repeat this for all weapons.
**Note:** For DLC weapons, you have to edit the `BIOWeapon.ini` file for the respective DLC. The file will be located in the `$ME2_INSTALL_FOLDER\BioGame\DLC\$DLC_Codename\CookedPC` folder. Be aware that some DLCs contain more than one weapon; in that case, the `bInfiniteAmmo=true` line needs to be added to all relevant sections (replacing existing `bInfiniteAmmo` if any).
2. In the `[SFXGame.SFXWeapon]` section change `AmmoPerShot=1` into `AmmoPerShot=0`. None of your weapons will spend any ammo when firing and don't need to be reloaded. For M\-920 Cain do the same in `[SFXGameContent_Inventory.SFXHeavyWeapon_NukeLauncher]`.
3. Changing the "reload" binding to `( Name="PC_Reload", Command="SwapWeaponIfEmpty | TryReload | initammo 999" )` in the \[SFXGame.SFXGameModeBase] section.. This will refill spare ammunition every time the reload button is pressed. This affects only non\-heavy weapons.
4. Changing the "shoot" combat binding to read `( Name="Shared_Shoot", Command="initammo 999 | SwapWeaponIfEmpty | FireWeapon | OnRelease StopFiringWeapon" )` will reset the player's spare ammunition every time the fire trigger is pressed. This affects all weapons.

**Note:** If you use the second or fourth method, you won't able to reload your weapon. That will result in inability to make progress in the Lazarus Project medbay (the door won't unlock until you reload). The `bInfiniteAmmo` tweak (the first method) will force you to empty your clip in order to leave. Once your clip is empty, Shepard will reload the pistol and the door will be opened.

### Hybrid Heat/Ammo System

It is possible to change the ammo system into a "hybrid heat/ammo system", in which the weapon will regenerate its ammo when not fired for awhile. (You can consider the "ammo" as "how many shots can be made before weapon overheats".) When the ammo reaches zero, the weapon will automatically reload and consume the spare ammos. (You can consider the reload as "emergency heat sink / thermal clip ejection".)
To activate this "hybrid" ammo system:

1. In `[SFXGame.SFXGameConfig]` set `WeaponsUseHeat` to `true`
2. Configure the weapons for "Unlimited Ammo" using **Method 1** in the previous section. The weapons will *NOT* actually have unlimited ammo; this is needed to turn on the "hybrid" system.
3. Optionally, you can tune `HeatDissipationRate` to make the weapons 'cool down' slower or faster; the value for this setting is a *float*, so you can use fractional numbers.

**Note:** When you activate this "hybrid" system, you will no longer be able to manually reload any weapon. Please see the note of the previous section for the impact of this change.

### Toggle Command Menu

**Note:** Modifying this line of code inside Coalesced.ini may crash the game's API or prevent it from loading if you are not careful. See note above about config file size.

The default method to view the HUD screen is to press and hold a key until you want to return to the "action". A different approach is to toggle the HUD so it will stay on by pressing a key, and return to the game when the same button is pressed again.
To enable Command Menu toggle find the line in \[SFXGame.SFXGameModeBase] section.

`Bindings=( Name="PC_ExitCommandMenu", Command="OnRelease ExitCommandMenu" )`
Change it to `Bindings=( Name="PC_ExitCommandMenu", Command="ExitCommandMenu" )`

### More Fuel and Probes for Normandy

Locate \[SFXGame.SFXInventoryManager] section in BIOWeapon module and set appropriate values for these variables: `MaxProbes` and `MaxFuel`.

Do this before starting a new game and these values will be actual for free: just forget about refueling for whole game. Changing in the middle of the game also works, but with necessity of filling new capacity and spending (a lot of) money.

### Collect More Resources From Planets

Locate \[SFXGame.BioPlanet]. It should contain four variables, `EezoMineralsBase`, `PlacedMineralsPool`, `RandomMineralsBase`, and `ScanBarMaxMineralSize`. Multiply the values of all of them by the same value, such as 20, to then get that many times more resources from every probe launched onto a planet.

### Bind Storm To A Different Key Than Use/Cover

**Note:** Using this tweak may crash the game's API or prevent it from loading if you are not careful. See note above about config file size.

Locate \[SFXGame.SFXGameModeBase] section in BIOInput module, and find the line reading:

`Bindings=( Name="Shared_Action", Command="Exclusive Used | TryClimbOrMantleCover | Exclusive TryAcquireCover | OnRelease StormOff | OnHold 0.2 StormOn | OnTap 0.3 TryExitCover 1" )`

Change it to:

`Bindings=( Name="Shared_Action", Command="Exclusive Used | TryClimbOrMantleCover | Exclusive TryAcquireCover | OnTap 0.3 TryExitCover 1" )`

This will remove storming from the use/cover key. Now, locate the \[SFXGame.SFXGameModeDefault] section, immediately below. Add a new line to the bottom of this section:

`Bindings=( Name="LeftAlt", Command="OnRelease StormOff | OnHold 0.2 StormOn" )`

Replace `LeftAlt` with whichever key you prefer to use.

### Skipping Dialogue without Choosing an Unwanted Answer

On the second and subsequent playthroughs, you may want to skip already\-seen dialogue by pressing Spacebar. But there is an unfortunate side effect of accidentally choosing a dialogue option when the dialog wheel appears. This tweak modifies the behavior of Spacebar to *only* skip dialogue. There are two methods:

**Method 1**

Locate `[SFXGame.SFXGameModeConversation]` in `BIOInput` and change the following line:
`Bindings=( Name="SpaceBar",Command="PC_ConvSkip")`
into (all in one line):
`Bindings=( Name="SpaceBar",Command="set BioConversation m_bSkipRequested true | OnRelease set BioConversation m_bSkipRequested false")`
**Method 2**

Find `[SFXGame.SFXGameModeBase]` in `BIOInput` and change the following line:
`Bindings=( Name="PC_ConvSkip", Command="SkipConversation" )`
into (all in one line):
`Bindings=( Name="PC_ConvSkip", Command="set BioConversation m_bSkipRequested true | OnRelease set BioConversation m_bSkipRequested false")`

### Fix Field of View (FOV)

Some players feel that the game's default FOV in combat mode is too small; one needs to keep looking around left and right just to gain some situational awareness. Unfortunately, the default FOV is *not* permanently fixable. However, a workaround to fix the FOV during combat scenes can be done by creating a Binding for the command `set SFXGame.SFXCameraMode FOV $N`, where `$N` is the desired value for the FOV: 75 is the game's default value, and it is suggested that values in the range of `90..120` (inclusive) works best.

For example, to bind the command to the "." (Period) key, find the `[SFXGame.SFXGameModeDefault]` section, and add the following:

`Bindings=( Name="Period", Command="set SFXGame.SFXCameraMode FOV $N" )`
Now, during combat/traveling mode, a press of the "." key will set the FOV to the value you desire (remember to replace `$N` with a numerical value). The new FOV value will remain effective until you exit the game.

### Temporarily Activate "NoClip" Mode

Mass Effect 2 is buggy, and one of the bugs is the possibility of Shepard somehow managing to climb to places they shouldn't be able to... and got trapped there. The only way to exit this situation is to either load a prior save, or to temporarily activate "No Clip" mode which will allow Shepard to leave the bounding box.

To enable temporary activation of "NoClip", you can add the following binding to the `[SFXGame.SFXGameModeDefault]` section:

`Bindings=( Name="Backslash", Command="Ghost | OnRelease Walk")`
Pressing (and holding) the \\ (backslash) key will activate the "NoClip" mode, enabling you to leave the 'trap' and enter an actual path/area where Shepard should be.

(As usual, you can customize the "Backslash" key to any key you prefer.)

### Disable EA and BioWare Intros

It's possible to disable the normally unskippable BioWare and EA intro videos for Mass Effect 2\.

First, navigate to the Mass Effect 2 folder, then find the movies folder:

*Mass Effect 2\\BioGame\\Movies*

Then rename or delete:

*BWLogo.bik*

*ME\_EAsig\_720p\_v2\_raw.bik*

## Reference Table

This section contains a list of possible parameters for commands.

### Level List

| **BioP\_Nor** | Normandy SR\-2 |
| --- | --- |
| **BioP\_CitHub** | Citadel \- Zakera Ward |
| **BioP\_KroHub** | Tuchanka \- Urdnot Camp |
| **BioP\_OmgHub** | Omega \- Merchant District |
| **BioP\_TwrHub** | Illium \- Nos Astra |
| **BioP\_ProNor** | Normandy SR\-1 |
| **BioP\_ProCer** | Lazarus Research Station |
| **BioP\_ProFre** | Freedom's Progress |
| **BioP\_HorCr1** | Horizon |
| **BioP\_ShpCr2** | Collector Vessel |
| **BioP\_RprGtA** | Derelict Reaper |
| **BioP\_EndGm1** | Tartarus Debris Field |
| **BioP\_EndGm2** | Collector Station |
| **BioP\_EndGm3** | Suicide Mission Epilogue |
| **BioP\_BchLmL** | Aeia \- Hugo Gernsback Crash Site |
| **BioP\_BlbGtl** | Heretic Station |
| **BioP\_JnkKgA** | Korlus \- Blue Suns Facility |
| **BioP\_OmgGrA** | Omega \- Archangel's Base |
| **BioP\_OmgPrA** | Omega \- Slums District |
| **BioP\_SunTlA** | Haestrom \- Quarian Landing Zone |
| **BioP\_TwrAsA** | Illium \- Dantius Towers |
| **BioP\_TwrMwA** | Illium \- Commercial Spaceport |
| **BioP\_CitAsL** | Citadel \- 800 Blocks |
| **BioP\_CitGrL** | Citadel \- Factory Distric |
| **BioP\_JunCvL** | Pragia \- Teltin Facility |
| **BioP\_KroKgL** | Tuchanka \- Urdnot Ruins |
| **BioP\_KroPrL** | Tuchanka \- Weyrloc Facility |
| **BioP\_PrsCvA** | Prison Ship Purgatory |
| **BioP\_PtyMtL** | Bekenstein \- Hock's Party |
| **BioP\_QuaTlL** | Migrant Fleet |
| **BioP\_TwrVxL** | Illium \- Transport Station |
| **BioP\_ZyaVtL** | Zorya \- Eldfell\-Ashland Refinery |
| **BioP\_Unc1Explore** | Aite |
| **BioP\_Unc1Base1** | Aite \- Hermes Station |
| **BioP\_Unc1Base2** | Aite \- Vulcan Station |
| **BioP\_Unc1Base3** | Aite \- Prometheus Station |
| **BioP\_Unc1Base4** | Aite \- Atlas Station |
| **BioP\_Exp1Lvl1** | Illium \- Market District |
| **BioP\_Exp1Lvl2** | Illium \- Hotel Azure |
| **BioP\_Exp1Lvl3** | Hagalaz \- Ship Exterior |
| **BioP\_Exp1Lvl4** | Hagalaz \- Ship Base |
| **BioP\_Exp1Lvl5** | Hagalaz \- Broker Base |
| **BioP\_ArvLvl1** | Aratoht |
| **BioP\_ArvLvl4** | Project Base \- Station Port |
| **BioP\_ArvLvl3** | Project Base \- Med Bay |
| **BioP\_ArvLvl2** | Project Base \- Generator Room |
| **BioP\_ArvLvl5** | Project Base \- Station Exterior |
| **BioP\_N7BldInv1** | Tarith \- Blood Pack Comm Relay |
| **BioP\_N7BldInv2** | Zada Ban \- Blood Pack Base |
| **BioP\_N7Crsh** | Zanethu \- MSV Estevanico Site |
| **BioP\_N7DriveBy** | Corang |
| **BioP\_N7Geth1** | Lattesh |
| **BioP\_N7Geth2** | Canalus |
| **BioP\_N7Ruins** | Kopis \- Dig Site |
| **BioP\_N7ShipWreck** | Zeona \- Firewalker |
| **BioP\_N7Spdr1** | Joab \- Dig Site |
| **BioP\_N7Spdr2** | MSV Strontium Mule |
| **BioP\_N7Spdr3** | Sanctum \- Blue Suns Base |
| **BioP\_N7VIQ1** | Neith \- MSV Corsica Site |
| **BioP\_N7VIQ2** | Jarrahe Station |
| **BioP\_N7VIQ3** | Capek \- Hahne\-Kedar Facility |
| **BioP\_N7Mine** | Helyme \- Eldfell\-Ashland Facility |
| **BioP\_N7mmnt1** | Daratar \- Eclipse Cache |
| **BioP\_N7mmnt2** | Gei Hinnom \- Quarian Crash Site |
| **BioP\_N7mmnt3** | Taitus \- Mining the Canyon |
| **BioP\_N7mmnt4** | MSV Broken Arrow |
| **BioP\_N7mmnt5** | Lorek \- Eclipse Base |
| **BioP\_N7mmnt6** | Sinmara \- Magnetic Shield Generator |
| **BioP\_N7mmnt7** | Franklin \- Javelin Mk.II Silo |
| **BioP\_N7mmnt8** | Karumto |
| **BioP\_N7mmnt10** | Aequitas \- Mining Facility |
| **BioP\_N7NorCrash** | Alchera \- Normandy SR\-1 Site |

### Weapon List

| **SFXGame.SFXWeapon** | Base template |
| --- | --- |
| **SFXGameContent\_Inventory.SFXWeapon\_HeavyPistol** | M\-3 Predator |
| **SFXGameContent\_Inventory.SFXWeapon\_HandCannon** | M\-6 Carnifex |
| **SFXGameContent\_Inventory.SFXWeapon\_AutoPistol** | M\-4 Shuriken |
| **SFXGameContent\_Inventory.SFXWeapon\_SMG** | M\-9 Tempest |
| **SFXGameContent\_Inventory.SFXWeapon\_AssaultRifle** | M\-8 Avenger |
| **SFXGameContent\_Inventory.SFXWeapon\_Needler** | M\-15 Vindicator |
| **SFXGameContent\_Inventory.SFXWeapon\_Machinegun** | M\-76 Revenant |
| **SFXGameContent\_Inventory.SFXWeapon\_GethPulseRifle** | Geth Pulse Rifle |
| **SFXGameContent\_Inventory.SFXWeapon\_Shotgun** | M\-23 Katana |
| **SFXGameContent\_Inventory.SFXWeapon\_HeavyShotgun** | M\-27 Scimitar |
| **SFXGameContent\_Inventory.SFXWeapon\_FlakGun** | M\-300 Claymore |
| **SFXGameContent\_Inventory.SFXWeapon\_SniperRifle** | M\-92 Mantis |
| **SFXGameContent\_Inventory.SFXWeapon\_AntiMatRifle** | M\-97 Viper |
| **SFXGameContent\_Inventory.SFXWeapon\_MassCannon** | M\-98 Widow |
| **SFXGameContent\_Inventory.SFXHeavyWeapon\_GrenadeLauncher** | M\-100 Grenade Launcher |
| **SFXGameContent\_Inventory.SFXHeavyWeapon\_MissileLauncher** | ML\-77 Missile Launcher |
| **SFXGameContent\_Inventory.SFXHeavyWeapon\_FreezeGun** | M\-622 Avalanche |
| **SFXGameContent\_Inventory.SFXHeavyWeapon\_NukeLauncher** | M\-920 Cain |
| **SFXGameContent\_Inventory.SFXHeavyWeapon\_ParticleBeam** | Collector Particle Beam |
| **SFXGameContentDLC\_Pistol.SFXWeapon\_LaserPistol** † | M\-5 Phalanx |
| **SFXGameContentDLC\_HEN\_MT.SFXWeapon\_TacticalMachinePistol** † | M\-12 Locust |
| **SFXGameContentDLC\_PRE\_Collectors.SFXWeapon\_CollectorAssaultRifle** † | Collector Assault Rifle |
| **SFXGameContentDLC\_Desert.SFXWeapon\_DesertAssaultRifle** † | M\-96 Mattock |
| **SFXGameContentDLC\_PRE\_Cerberus.SFXWeapon\_CerberusShotgun**† | M\-22 Eviscerator |
| **SFXGameContentDLC\_MCR\_02\.SFXWeapon\_GethShotgun**† | Geth Plasma Shotgun |
| **SFXGameContentDLC\_PRE\_Incisor.SFXWeapon\_IncisorSniperRifle** † | M\-29 Incisor (Deluxe Edition) |
| **SFXGameContentDLC\_CER\_02\.SFXWeapon\_IncisorSniperRifle\_CER\_02** † | M\-29 Incisor (Aegis Pack) |
| **SFXGameContentDLC\_HEN\_VT.SFXHeavyWeapon\_FlameThrower\_Player** † | M\-451 Firestorm |
| **SFXGameContentDLC\_CER\_Arc.SFXHeavyWeapon\_ArcProjector** † | Arc Projector |
| **SFXGameContentDLC\_PRE\_Gamestop.SFXHeavyWeapon\_Blackstorm** † | M\-490 Blackstorm |

† These sections are located in the DLC's respective `BIOWeapon.ini` file instead of inside `Coalesced.ini`
### Power List

Note: Not all powers work on all characters.

### Companion Usable Powers

These powers can be assigned to your companions and work correctly.

| Power Name | Description | Example |
| --- | --- | --- |
| SFXPower\_AIHacking | GIve AI Hacking to companion | GivePower Garrus SFXPower\_AIHacking |
| SFXPower\_ArmorPiercingAmmo | GIve Armor Piercing Ammo to companion | GivePower Miranda SFXPower\_ArmorPiercingAmmo |
| SFXPower\_WarpAmmo\_Player | GIve Warp Ammo power to companion | GivePower Miranda SFXPower\_WarpAmmo\_Player |
| SFXPower\_Cloak | GIve Infiltrator cloaking power to companion | GivePower Miranda SFXPower\_Cloak |
| SFXPower\_CombatDrone | GIve Combat Drone power to companion | GivePower Garrus SFXPower\_CombatDrone |
| SFXPower\_ConcussiveShot | GIve Concussive Shot power to companion | GivePower Miranda SFXPower\_ConcussiveShot |
| SFXPower\_Crush | GIve Miranda's Slam power to a companion | GivePower Garrus SFXPower\_Crush |
| SFXPower\_CryoAmmo | GIve Cryo Ammo to a companion | GivePower Garrus SFXPower\_CryoAmmo |
| SFXPower\_Singularity | GIve Singularity to a companion | GivePower Garrus SFXPower\_Singularity |

### ALL Powers

SFXPower\_AbominationExplosion

SFXPower\_AIHacking

SFXPower\_AIHacking\_Engineer

SFXPower\_AIHacking\_Heavy

SFXPower\_AIHacking\_Infiltrator

SFXPower\_AIHacking\_Legion

SFXPower\_AIHacking\_Radius

SFXPower\_AIHacking\_Tali

SFXPower\_AnimatedReactionPower

SFXPower\_ArmorPiercingAmmo

SFXPower\_ArmorPiercingAmmo\_Garrus

SFXPower\_ArmorPiercingAmmo\_Heavy

SFXPower\_ArmorPiercingAmmo\_Infiltrator

SFXPower\_ArmorPiercingAmmo\_Soldier

SFXPower\_ArmorPiercingAmmo\_Squad

SFXPower\_ArmorPiercingAmmo\_Thane

SFXPower\_WarpAmmo\_Player

SFXPower\_AdrenalineRush

SFXPower\_AdrenalineRush\_Evolved1

SFXPower\_AdrenalineRush\_Evolved2

SFXPower\_Barrier

SFXPower\_Barrier\_Adept

SFXPower\_Barrier\_Damage

SFXPower\_Barrier\_Heavy

SFXPower\_Barrier\_Mordin

SFXPower\_Barrier\_NPC

SFXPower\_Barrier\_Samara

SFXPower\_Barrier\_Sentinel

SFXPower\_BioticCharge

SFXPower\_BioticCharge\_Radius

SFXPower\_BioticCharge\_Slam

SFXPower\_Carnage

SFXPower\_Carnage\_Heavy

SFXPower\_Carnage\_NPC

SFXPower\_Carnage\_Radius

SFXPower\_Carnage\_Soldier

SFXPower\_Carnage\_Vanguard

SFXPower\_Cloak

SFXPower\_Cloak\_Damage

SFXPower\_Cloak\_Enhanced

SFXPower\_Cloak\_Infiltrator

SFXPower\_Cloak\_NPC

SFXPower\_ColossusPulse

SFXPower\_CombatDrone

SFXPower\_CombatDroneAttack

SFXPower\_CombatDroneDeath

SFXPower\_CombatDrone\_Engineer

SFXPower\_CombatDrone\_NPC

SFXPower\_CombatDrone\_Rocket

SFXPower\_CombatDrone\_Tali

SFXPower\_CombatDrone\_Tech

SFXPower\_ConcussiveShot

SFXPower\_ConcussiveShot\_Garrus

SFXPower\_ConcussiveShot\_Heavy

SFXPower\_ConcussiveShot\_Infiltrator

SFXPower\_ConcussiveShot\_Radius

SFXPower\_ConcussiveShot\_Soldier

SFXPower\_ConcussiveShot\_Zaeed

SFXPower\_Crush

SFXPower\_CryoAmmo

SFXPower\_CryoAmmo\_Evolved1

SFXPower\_CryoAmmo\_Evolved2

SFXPower\_CryoFreeze

SFXPower\_CryoFreeze\_Mordin

SFXPower\_CryoFreezeInstant\_Evolved1

SFXPower\_CryoFreezeInstant\_Evolved2

SFXPower\_DisruptorAmmo

SFXPower\_DisruptorAmmo\_Grunt

SFXPower\_DisruptorAmmo\_Heavy

SFXPower\_DisruptorAmmo\_Infiltrator

SFXPower\_DisruptorAmmo\_Legion

SFXPower\_DisruptorAmmo\_NPC

SFXPower\_DisruptorAmmo\_Soldier

SFXPower\_DisruptorAmmo\_Squad

SFXPower\_DisruptorAmmo\_Vanguard

SFXPower\_FirstAid

SFXPower\_Fortification

SFXPower\_Fortification\_Grunt

SFXPower\_Fortification\_Heavy

SFXPower\_Fortification\_NPC

SFXPower\_Fortification\_Soldier

SFXPower\_Fortification\_Squad

SFXPower\_GethJuggernautDeath

SFXPower\_GethPrimeDeath

SFXPower\_GethPrimePulse

SFXPower\_GethTrooperDeath

SFXPower\_GethTrooperDeath\_Red

SFXPower\_GunShipRocketSlow\_Left

SFXPower\_GunshipRocketSlow\_Right

SFXPower\_GunshipRocket\_Left

SFXPower\_GunshipRocket\_Right

SFXPower\_HeavyMechExplosion

SFXPower\_HeavyMechRocket

SFXPower\_HeavyPunch

SFXPower\_HuskMelee\_Left

SFXPower\_HuskMelee\_Right

SFXPower\_HuskTesla

SFXPower\_IncendiaryAmmo

SFXPower\_IncendiaryAmmo\_Grunt

SFXPower\_IncendiaryAmmo\_Infiltrator

SFXPower\_IncendiaryAmmo\_Jacob

SFXPower\_IncendiaryAmmo\_NPC

SFXPower\_IncendiaryAmmo\_Radius

SFXPower\_IncendiaryAmmo\_Soldier

SFXPower\_IncendiaryAmmo\_Squad

SFXPower\_IncendiaryAmmo\_Vanguard

SFXPower\_Incinerate

SFXPower\_Incinerate\_Engineer

SFXPower\_Incinerate\_Garrus

SFXPower\_Incinerate\_Heavy

SFXPower\_Incinerate\_Mordin

SFXPower\_Incinerate\_Infiltrator

SFXPower\_Incinerate\_NPC

SFXPower\_Incinerate\_Radius

SFXPower\_KasumiCloakTeleport

SFXPower\_KasumiCloakTeleport\_Evolved1

SFXPower\_KasumiCloakTeleport\_Evolved2

SFXPower\_KasumiUnique

SFXPower\_KasumiUnique\_Evolved1

SFXPower\_KasumiUnique\_Evolved2

SFXPower\_KasumiUnique\_Player

SFXPower\_KroganCharge

SFXPower\_KroganMelee

SFXPower\_KroganRegen

SFXPower\_Lift

SFXPower\_Lift\_Adept

SFXPower\_Lift\_Heavy

SFXPower\_Lift\_Jack

SFXPower\_Lift\_NPC

SFXPower\_Lift\_Samara

SFXPower\_Lift\_TwrMwA

SFXPower\_LightMechShock

SFXPower\_LoyaltyRequirement

SFXPower\_MechDeathExplosion

SFXPower\_MechDogTaser

SFXPower\_NeuralShock

SFXPower\_NeuralShock\_Radius

SFXPower\_NeuralShock\_Heavy

SFXPower\_NeuralShock\_Mordin

SFXPower\_Overload

SFXPower\_Overload\_Garrus

SFXPower\_Overload\_Heavy

SFXPower\_Overload\_Kasumi

SFXPower\_Overload\_Radius

SFXPower\_Overload\_Engineer

SFXPower\_Overload\_Miranda

SFXPower\_Overload\_Sentinel

SFXPower\_Overload\_Tali

SFXPower\_PhaseShift

SFXPower\_PlayerMelee

SFXPower\_PlayerMeleePistol

SFXPower\_PraetorianDeathChoir

SFXPower\_Pull

SFXPower\_PullProjectile

SFXPower\_PullProjectile\_Heavy

SFXPower\_PullProjectile\_Radius

SFXPower\_Pull\_Adept

SFXPower\_Pull\_Heavy

SFXPower\_Pull\_Hench

SFXPower\_Pull\_Jack

SFXPower\_Pull\_Jacob

SFXPower\_Pull\_Radius

SFXPower\_Pull\_Samara

SFXPower\_Pull\_Vanguard

SFXPower\_RobotDeathExplosion

SFXPower\_RocketDroneAttack

SFXPower\_Sabotage

SFXPower\_ScionTesla

SFXPower\_ShieldBoost

SFXPower\_ShieldBoost\_Advanced

SFXPower\_ShieldBoost\_Engineer

SFXPower\_ShieldBoost\_Hardened

SFXPower\_ShieldBoost\_NPC

SFXPower\_ShieldJack

SFXPower\_Singularity

SFXPower\_Singularity\_Adept

SFXPower\_Singularity\_Heavy

SFXPower\_Singularity\_Radius

SFXPower\_Singularity\_Liara

SFXPower\_SpiderBloodSpray

SFXPower\_StasisNew

SFXPower\_StasisNew\_Evolved1

SFXPower\_StasisNew\_Evolved2

SFXPower\_StasisNew\_Liara

SFXPower\_ThresherMawSpit

SFXPower\_Throw

SFXPower\_ThrowProjectile

SFXPower\_ThrowProjectile\_Heavy

SFXPower\_ThrowProjectile\_Radius

SFXPower\_Throw\_Adept

SFXPower\_Throw\_Heavy

SFXPower\_Throw\_Jack

SFXPower\_Throw\_Miranda

SFXPower\_Throw\_Morinth

SFXPower\_Throw\_NPC

SFXPower\_Throw\_Radius

SFXPower\_Throw\_Sentinel

SFXPower\_Throw\_Thane

SFXPower\_Varren

SFXPower\_VorchaRegen

SFXPower\_Warp

SFXPower\_WarpProjectile

SFXPower\_WarpProjectile\_Heavy

SFXPower\_WarpProjectile\_Radius

SFXPower\_Warp\_Adept

SFXPower\_Warp\_Heavy

SFXPower\_Warp\_Jacob

SFXPower\_Warp\_Liara

SFXPower\_Warp\_Miranda

SFXPower\_Warp\_Morinth

SFXPower\_Warp\_NPC

SFXPower\_Warp\_Radius

SFXPower\_ZaeedUnique

SFXPower\_ZaeedUnique\_Evolved1

SFXPower\_ZaeedUnique\_Evolved2

SFXPower\_ZaeedUnique\_Player

SFXPower\_AdeptPassive

SFXPower\_AdeptPassive\_Evolved1

SFXPower\_AdeptPassive\_Evolved2

SFXPower\_EngineerPassive

SFXPower\_EngineerPassive\_Evolved1

SFXPower\_EngineerPassive\_Evolved2

SFXPower\_InfiltratorPassive

SFXPower\_InfiltratorPassive\_Evolved1

SFXPower\_InfiltratorPassive\_Evolved2

SFXPower\_SentinelPassive

SFXPower\_SentinelPassive\_Evolved1

SFXPower\_SentinelPassive\_Evolved2

SFXPower\_SoldierPassive

SFXPower\_SoldierPassive\_Evolved1

SFXPower\_SoldierPassive\_Evolved2

SFXPower\_VanguardPassive

SFXPower\_VanguardPassive\_Evolved1

SFXPower\_VanguardPassive\_Evolved2

SFXPower\_GarrusPassive

SFXPower\_GarrusPassive\_Evolved1

SFXPower\_GarrusPassive\_Evolved2

SFXPower\_GruntPassive

SFXPower\_GruntPassive\_Evolved1

SFXPower\_GruntPassive\_Evolved2

SFXPower\_JacobPassive

SFXPower\_JacobPassive\_Evolved1

SFXPower\_JacobPassive\_Evolved2

SFXPower\_JackPassive

SFXPower\_JackPassive\_Evolved1

SFXPower\_JackPassive\_Evolved2

SFXPower\_KasumiPassive

SFXPower\_KasumiPassive\_Evolved1

SFXPower\_KasumiPassive\_Evolved2

SFXPower\_LiaraPassive

SFXPower\_LiaraPassive\_Evolved1

SFXPower\_LiaraPassive\_Evolved2

SFXPower\_LegionPassive

SFXPower\_LegionPassive\_Evolved1

SFXPower\_LegionPassive\_Evolved2

SFXPower\_MirandaPassive

SFXPower\_MirandaPassive\_Evolved1

SFXPower\_MirandaPassive\_Evolved2

SFXPower\_MordinPassive

SFXPower\_MordinPassive\_Evolved1

SFXPower\_MordinPassive\_Evolved2

SFXPower\_SamaraPassive

SFXPower\_SamaraPassive\_Evolved1

SFXPower\_SamaraPassive\_Evolved2

SFXPower\_TaliPassive

SFXPower\_TaliPassive\_Evolved1

SFXPower\_TaliPassive\_Evolved2

SFXPower\_ThanePassive

SFXPower\_ThanePassive\_Evolved1

SFXPower\_ThanePassive\_Evolved2

SFXPower\_ZaeedPassive

SFXPower\_ZaeedPassive\_Evolved1

SFXPower\_ZaeedPassive\_Evolved2

SFXPower\_ConcussiveRounds

SFXPower\_ConcussiveRounds\_Evolved1

SFXPower\_ConcussiveRounds\_Evolved2

SFXPower\_ConcussiveRounds\_Infiltrator

SFXPower\_ConcussiveRounds\_Soldier

SFXPower\_ConcussiveRounds\_Thane

SFXPower\_ConcussiveRounds\_Vanguard

SFXPower\_Fissure

SFXPower\_Fissure\_Engineer

SFXPower\_Fissure\_Garrus

SFXPower\_Fissure\_Heavy

SFXPower\_Fissure\_Infiltrator

SFXPower\_Fissure\_Mordin

SFXPower\_Fissure\_NPC

SFXPower\_Fissure\_Radius

SFXPower\_Flashbang

SFXPower\_Flashbang\_Damage

SFXPower\_Flashbang\_Radius

SFXPower\_Flashbang\_Garrus

SFXPower\_Flashbang\_Legion

SFXPower\_Flashbang\_Soldier

SFXPower\_Flashbang\_Vanguard

SFXPower\_Negotiate

SFXPower\_NeuralShock\_Miranda

SFXPower\_NeuralShock\_Infiltrator

SFXPower\_NeuralShock\_Engineer

SFXPower\_NeuralShock\_Sentinel

SFXPower\_Stasis

SFXPower\_Stasis\_Adept

SFXPower\_Stasis\_Damage

SFXPower\_Stasis\_Heavy

SFXPower\_Stasis\_Morinth

SFXPower\_Stasis\_Sentinel

SFXPower\_Stasis\_Thane

## Tools and Useful Links

- ME2 Ini File Fixer: https://www.nexusmods.com/masseffect2/mods/116?tab\=files
- Mass Effect 2 Coalesced Compiler
- Mass Effect 2 Coalesced Editor
- Mass Effect 2 Coalesced.ini Mod Manager
- Gibbed's Save Editor Extended \| Gibbed's Save Editor (Original)
- Texmod
- List of level codes

##
