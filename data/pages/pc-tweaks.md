---
title: PC Tweaks
url: https://masseffect.fandom.com/wiki/PC_Tweaks
game: Mass Effect
type: lore
characters: []
scraped: '2026-08-28'
---

|  | *This article is about tweaks for the first Mass Effect game. For Mass Effect 2 tweaks, see PC Tweaks (Mass Effect 2\).* *For Mass Effect 3 tweaks, see PC Tweaks (Mass Effect 3\).* |
| --- | --- |

Mass Effect was built from the Unreal Engine (UE) 3 games engine, which allows many modifications by the user to enhance the in\-game graphics and controls.

Mass Effect's in\-game configuration options have very little tweaking possibilities and only support basic graphic and key mapping. This article intends to serve as a guide to players who want to have more control on game performance and personalization, by highlighting options which players can tweak to better suit their needs.

**Disclaimer:** The Mass Effect Wiki does not promote, vouch for, or otherwise endorse the use of any third\-party software not authorized by BioWare or Electronic Arts. Any such software, programs, applications, or files linked or mentioned in this article is done strictly for reference purposes. Anyone choosing to use third\-party software does so at their own risk.

## Preface

### Back up your data

All of the changes that are described in this article should only be tested on the files in the documents folder:

- **On Windows XP/2000:** `%SystemDrive%\Documents and Settings\%Username%\My Documents\BioWare\Mass Effect\Config`
- **On Windows Vista/7/8/10:** `%SystemDrive%\Users\%Username%\Documents\BioWare\Mass Effect\Config`
- **On Steam on Gnu/Linux:** `~/.steam/debian-installation/steamapps/compatdata/17460/pfx/drive_c/users/steamuser/Documents/BioWare/Mass Effect/Config`

(%SystemDrive% will be replaced with the drive letter where your Windows system is installed on following a colon, and %Username% with the current user that you are logged into the system with.)

###

- **Files location**: The Mass Effect game will read the files inside the Config folder. If it fails to do so, or if the files have incorrect data, the game will read the default config files that are located in the folder where you installed your game. By default they are located at 'X:\\Program Files\\Mass Effect\\BioGame\\Config'. Those files will be prefixed with the word *Default* (to avoid editing them by mistake).

- **Backup your files**: To ensure that your gaming experience will not be damaged, make sure to back up every file that you are about to change. A good way to do this is to copy the *Mass Effect* or *Config* folder to a safe place. Alternatively, you can archive the folder to avoid confusion.

- **Game Patches**: BioWare have released two patches that fix various issues. Installation of a patch will overwrite changes made to the configuration files, and update their version (indicated at the bottom of each file).

### Writing style

The configuration files implement the CamelCase writing style for functions and variables names. For example: the 'Caps Lock' key will be written as CapsLock, 'Right mouse button' will be written as RightMouseButton, etc.

Note, however, that this is merely a writing convention. When entering commands in the console, you may use any case, or combination of cases, you prefer. For example: "GiveBonusTalent 14", "givebonustalent 14", "GIVEBONUSTALENT 14", and "Givebonustalent 14" will all yield the same result.

#### Data types

Generally, there are three types of data used in the configuration files:

- Strings \- Any sequence of letters or symbols (generally enclosed with quotation marks). These have no prefixing.
- Floating points \- Any number with decimal point. These will be appended with the letter *f*.
- Boolean \- a Boolean data type is a true/false variable and can only accept *True* or *False*.

## Configuration Files

### Input File (BioInput.ini)

This file is separated into six sections:

| *Engine.PlayerInput* | Basically, how the game will handle the input device that the player is using. Generally, you don't want to change anything in this section. Changes made here could harm your gaming experience. |
| --- | --- |
| *Editor.EditorViewportInput* | The section applies to the editor the developers used. It has no impact on the game. |
| *Engine.Console* | This section defines the Console keys and behavior. More information is in the section about the console. |
| *Engine.UIInputConfiguration* | This section deals with how the mouse or gamepad will operate (sensitivity, movement emulation, etc.) Most likely, you won't need to alter anything in here, but you are free to experiment. |
| *BIOC\_Base.BioPlayerInput* | This section deals with the mapping of keys. |
| *IniVersion* | This section is used for internal identification. |

\[Engine.PlayerInput] (Device Input)

This section deals with the way the controls work:

| MoveForwardSpeed | The in\-game *running* speed. Any changes made here could ruin the game experience by giving the player an advantage. If you want to shorten the time of traveling, see the section referring to changing the game speed. |
| --- | --- |
| MoveStrafeSpeed | The same as *MoveForwardSpeed* but controls sideways movement. |
| LookRightScale | Deals with Shepard's neck, and how much it can be turned for a wider field of vision. This can actually be useful when trying to take screenshots. |
| LookUpScale | The same as *LookRightScale*, but deals with the up/down motion. |
| MouseSensitivity | The sensitivity of the mouse. It's probably better to alter this from the in\-game menu. |
| GamepadAnalogSensitivity | The sensitivity of the gamepad. Again, probably better to alter this from the in\-game menu. |
| DoubleClickTime | The time between clicks that register as a double\-click. As Mass Effect does not treat double\-clicks any differently than single clicks, changing this should not have any effect. |
| bInvertTurn | Invert the axis of the mouse / keypad, if you want to change this, do it from the in\-game menu. |
| bEnableMouseSmoothing | Adds smoothing to the mouse movement. Change this through the in\-game menu. |

\[BIOC\_Base.BioPlayerInput] (Player Input)

This section has many behaviors that can be changed. It is advised to leave any line that does not start with the word 'Binding' alone. The exceptions to this are:

| m\_fDPadCooldownTime | Handles some of the cooldown times of the input devices and should not be altered. |
| --- | --- |
| m\_fStormCooldownTime | The same as *m\_fDPadCooldownTime*. |
| m\_fQuickOrderTime | Unknown function, but should not be touched, regardless. Experiment at your own risk. (Could be a boolean to determine whether time keeps progressing or not while giving quick commands to your team\-mates.) |
| m\_bDisableCinematicAccelerate | Allow or deny the acceleration option for cinematic cut\-scenes. This has no effect in the game. |
| m\_bDisableCinematicSkip | Allow or deny the ability to skip cinematic cut\-scenes (will be discussed later on). |
| m\_fCinematicSkipTriggerDelay | The delay in milliseconds before the actual skip occurs. |
| m\_fSlowMotionSpeed | The game has no slow motion scenes, so this option doesn't effect anything in\-game. |

Changing anything other than the recommended behaviors can cause severe gameplay bugs!

#### Binding overview

The binding of new keys, or changing behavior of existing keys is handled in the following way:
`Bindings=(Name="",InputMode=BIO_INPUT_MODE_NONE,Command="",Control=False,Shift=False,Alt=False)`

- **Name**: Define the key that will execute the behavior.
- **InputMode**: Defines the engine predefined inputs. Should not be changed.
- **Command**: The command you want to assign to the key.
- **Control, Shift, Alt**: Does the key work in combination with one of these keys. Make sure to only set True/False here.
- **Combining Commands:** You can specify multiple commands, provided they don't interfere with each other. (A good example of this is left shift making you sprint or zooming the Mako's cannon). If you include the word "onrelease" before the command, then that particular command will only activate when the user releases this button.

Generally, you only want to alter the *Name* and *Command*, unless you have a specific behavior you want to achieve.

#### Key combinations

When binding a key with Control, Shift, or Alt combination in addition to the same key without that combination, make sure that the declaration with the combination precedes the one without.
For example:

`Bindings=(Name="N", InputMode=BIO_INPUT_MODE_NONE, Command="ToggleHUD",Control=False,Shift=False,Alt=True)`

Toggle the HUD when the "N" and "Alt" key combination are pressed.

`Bindings=(Name="N", InputMode=BIO_INPUT_MODE_NONE, Command="ToggleFlyCam",Control=False,Shift=False,Alt=False)`

Switch to fly cam when only the "N" key is pressed.
Mass Effect comes with a set of commands that can be executed through the console or bound to keys, most are hidden and can only be found through trial and error.

Please note, that changing critical game\-play keys may cause you to not be able to interface with objects, start conversations, etc. There are also some keys that control several action and sub\-actions, removing parts of the binding command can cause that key to stop behaving as expected.

#### Common Tweaks

**Toggle HUD**

`Command=ToggleCommandMenu`

The default method to view the HUD screen is to press and hold the 'Spacebar' key until you want to return to the "action". A different approach is to toggle the HUD so it will stay on by pressing a key, and return to the game when the same button is pressed again. *It is recommended to use a key other than the 'Spacebar' to preserve the default method*.
**Example: switching the spacebar menu into a toggle on/off mode**

open the file BIOInput.ini in a decent text\-editor

search for keyword "spacebar" and replace the correct line with this one:

Bindings\=(Name\="SpaceBar",InputMode\=BIO\_INPUT\_MODE\_NONE,Command\="ToggleCommandMenu \| VehicleThrustersOn \| OnRelease VehicleThrustersOff \| GuiKey BIOGUI\_EVENT\_BUTTON\_X \| OnRelease GuiKey BIOGUI\_EVENT\_BUTTON\_X\_RELEASE",Control\=False,Shift\=False,Alt\=False)

**Skip Cutscenes**

The game has a lot of repetitive cutscenes, i.e. docking on the Citadel, or traveling through the mass relays. Those cutscenes can be skipped, and there is no need to alter the binding keys. To activate the ability to skip cutscenes by pressing the "Draw/Holster Weapon" button (Q is default), just edit the lines:
`m_bDisableCinematicSkip=False
m_fCinematicSkipTriggerDelay=1.000000`

The first line enables you to skip the cutscenes (make sure to only set True/False here). The second line indicates the time that it takes from the button press to the actual skip. **Note:** some locations have the cutscene for a reason (Shepard walk or say something that triggers another event). Skipping that cutscene, therefore, may leave you stuck. Experiment at your own risk.

**Quick\-slot keys**

There are eight lines for the ability keys, they are numbered from 0 to 7, and are easy to alter.
`Command="UseAbility 0"
shift=True`

This example, modifies the *shift* parameter, to allow more control over what keys can be used, what allows the usage of already bound keys to be used with the *shift* key (*A, S, D, or W*, for example). Setting the *Shift* option to *True* instead of *False* will activate that combination, and will make Shepard use the first ability instead of moving to the left.

**Squad Commands**

Sometimes you want to give commands to a certain party member (to move forward, most of the times) and not to both of them.
`Command="SquadCommandMoveTo 1"
Command="SquadCommandMoveTo 2"`

The numerical parameter value is to indicate what squad member will execute the order. Either 1 (first squad member) or 2 (second squad member).

**Quickload**

It is possible to add a quickload option to the game. The problem is that you have to manually set the save name in the configuration file.
`Command="LoadGame John00_QuickSave"`
The *LoadGame* function receive the name of the save as a parameter: *\[profile\_name]00\_QuickSave*. Replace *\[profile\_name]* with the name of your current character. This can be done with any save game file \- look in your documents folder for desired name (`x:\Documents and Settings\[username]\My Documents\BioWare\Mass Effect\Save\`).

Note that should you desire to use an F Key to bind quickload, you will also need to delete its corresponding line, such as

"Bindings(Name\="F9",InputMode\=BIO\_INPUT\_MODE\_NONE,Command\="exec FKEY\_F9\.txt",Control\=False,Shift\=False,Alt\=False)". Otherwise the quickload bind won't do anything.

**Fast game speed for travel and cutscenes**

This hotkey increases game speed tenfold while holding the key.
`Bindings=(Name="MiddleMouseButton",InputMode=BIO_INPUT_MODE_NONE,Command="SloMo 10 | OnRelease SloMo 1",Control=False,Shift=False,Alt=False)`

While holding the middle mouse button, game speed will increase ten times. It's helpful when traveling big distances, such as hub zones or planetary surface. It also works in Mako, and even in cutscenes, allowing you to fast\-forward normally unskippable cutscenes. Speed multiplier may be arbitrary. Using this on a keyboard key sometimes causes glitches (e.g. it may freeze the game when fast\-forwarding Mako landing), but binding on a mouse key doesn't.
### Game Engine (BioEngine.ini)

#### Framerate

*\[Engine.GameEngine]*

`bSmoothFrameRate=True
MinSmoothedFrameRate=22
MaxSmoothedFrameRate=62`
`bSmoothFrameRate` Determines if the engine will enforce the framerate settings (`True`) or if it will let the graphic card manage them. This may cause spikes in FPS and unwanted graphic behavior.

`MinSmoothedFrameRate` and `MaxSmoothedFrameRate` determine the minimum and maximum framerate. Setting the maximum value too high can sometimes degrade quality, rather then enhance it. It is recommended to set those values to the system refresh rate for best performance.
#### Shadows

`bEnableBranchingPCFShadows=True`

This setting controls the presentation of shadows in the game. Setting it to false may increase performance, but at the same time can degrade the presentation of shadows.

`ShadowFilterRadius=2.000000`

Control shadow filtering to determine how sharp or soft the shadows will appear in the game. Higher value will make the shadow softer, and lower value will make them sharper.

`DepthBias=0.012000`
Controls the depth of shadows and how dynamic shadows appear. Higher value reduces the number of shadows shown, up to 1\.0 that removes shadows altogether, and a lower value increase the number of shadows shown. This setting can cause glitches or fix them by changing the value.

**Note:** Patch 1\.02 set this setting to 0\.030 that remove shadowing. Setting this to 0\.012 will return them.

`MinShadowResolution=32
MaxShadowResolution=512`

Determine the minimum and maximum shadow resolution. Higher minimum value will increase the richness of shadows. Lower maximum value will degrade the appearance of shadows. Note, that setting the minimum too high (or maximum too low) may result in glitches and loss of performance.

`ModShadowFadeDistanceExponent=0.200000`

Controls the distance from where shadows will be visible. Higher value will cause shadows to be visible in the near vicinity, while lower value will cause shadows to be shown at greater distance, increasing quality and degrading performance.
#### Sound

*\[ISACTAudio.ISACTAudioDevice]*

`MaxChannels=64`

Depending on your sound card, and glitches you encounter, you can play with the values to enhance performance with sound or fix glitches.
#### Misc. Graphical Settings

*\[SystemSettings]*

`DynamicDecals=True`

Controls the appearance of weapon fire left by players. Setting this setting to `False` enhances performance, but reduces game experience.

`DepthOfField=True`

Controls the Depth of Field that simulate how object inside the "focus area" are sharper than objects outside that field. It most noticeable while using the Sniper Rifle zoom feature that makes targeted objects more crisp and clear, and others blurred. Setting this option to `False` improves performance.

`QualityBloom=True`

Originally meant to control the quality of the Bloom Effect, but does not seem to have any effect in\-game, although setting it to `False` may improve performance.

`Trilinear=True`

Enables or disables the Trilinear Filtering that can improve the quality of textures, but at the same time can cause glitches and loss of quality.

`MaxAnisotropy=4`

If the game is set with Anisotropic as the filtering mode in\-game, this setting can control the level of Anisotropic Filtering used. Specifying numbers between 0 (no anisotropic filtering, better performance, but poorer image quality) to 16 (maximum filtering, degraded performance but crisper and more detailed textures) \- the default is 4\.
*\[TextureLODSettings]*

`TEXTUREGROUP_Character_Diff=(MinLODSize=32,MaxLODSize=512,LODBias=0)
TEXTUREGROUP_Character_Norm=(MinLODSize=32,MaxLODSize=512,LODBias=0)
TEXTUREGROUP_Character_Spec=(MinLODSize=32,MaxLODSize=256,LODBias=0)`
Setting the Min sizes to match the Max will force the game to always use the highest resolution textures on characters. This may decrease performance, but it will ensure a high resolution texture for Garrus's face \- due to a bug, the game will always use the minimum resolution for his face texture.

Raising the Max size is not recommended, this may cause graphical glitches.
*\[D3DDrv.D3DRenderDevice]*

`BIOVertexShaderVersion=vs_2_0`

Setting this to `vs_3_0`, improves game performance with minimal to none drop in graphics. Only recomended to users with GPU newer than the GeForce FX 5900 and the ATI Radeon X850\.
### BioGame.ini

#### Character Behavior

*\[BIOC\_Base.BioActorBehavior]*

`AllowFriendlyCollateral=false`

Enables you to be injured by your squad, and vice\-versa. This makes combat more realistic, but at the same time a problem with the current squad AI. Can also result in the 'death' of non\-targetable NPCs.
*\[BIOC\_Base.BioPlayerController]*

`CoverEnterInterval=0.0`

Determines how much time it takes to the character to enter cover, when walking in\-front of it.

`CoverExitCameraAngle=85`

Determines the camera angle that execute exiting from cover.

`CoverMovementModifier=0.25`

Determines the movement speed when in cover.

`ZoomMovementModifier=0.8`

Determines the movement speed when zooming with a weapon.
#### Inventory

*\[BIOC\_Base.BioInventory]*

`m_nMaxCredits=9999999
m_nMaxGrenades=5
m_fMaxSalvage=999
m_fMaxMedigel=5`

Changes the maximum number of Credits, Grenades, Omni\-gel, and Medi\-gel. Changing any of these values may hamper game\-play experience.
#### Conversation

*\[BIOC\_Base.BioConversation]*

`m_colSubtitleColor=(R=204,G=255,B=255,A=255)`

Changes the color and transparency of the subtitles. The values are in RGB (red, green, and blue) and alpha, which determines the transparency (lower the value to make the subtitles more transparent).

`m_fShowLastLineOffset=5.0`

In conversations, determines how much time passes between the NPC last line and the appearance of the dialogue wheel. Setting this to 0\.0 will cause the wheel to appear immediately, and helps prevent choosing unwanted answers when skipping dialogue.

`m_bRemoveWeapons=True`

Determines if Shepard will holster his/her weapon when initiating a conversation. Setting this option to `False` will cause also cause others present to keep their weapons drawn during the conversation. Can create some strange situations in which Shepard waves an assault rifle at people.

`m_fShowRepliesOffset=2.0`

Changing this to 20\.0 makes the dialogue wheel appear as soon as an NPC's last line of dialog starts.
#### Misc. Behaviors

*\[BIOC\_Base.BioPawnBehavior]*

`m_bAllowPhysicsOnDeadBodies=False`

Dead bodies will react more realistically, and shooting them results in minor movement and blood. Enabling this setting may result in degraded performance.
*\[BIOC\_Base.BioPawn]*

`m_fCorpseCleanupFirstAttemptTime=5.0
m_fCorpseCleanupAttemptRetryTime=2.0`

Determines the time until the game engine will attempt to remove enemy corpses for the first time, and how many retries it will execute. This will increase realism, but degrade performance (especially on intense combats). **Note:** Those settings also appear in *\[BIOC\_Base.BioArtPlaceable]*, and might require the additional change, there.
#### Cooldown

*\[BIOC\_Base.BioActivePower]*

`m_bSkipPowerCooldown=False`

Removes the time limit for ability cooldown. Removing the cooldown also applies to NPCs. For example, geth shock troopers will be able to spawn hex shields without limit, making them very difficult to kill.
#### Merchants

*\[BIOC\_Base.BioWorldInfo]*

`m_buybackArrayMaxSize=20`

Changes the amount of items that you can buy back after selling to Merchants.
#### Saves

*\[BIOC\_Base.BioSaveGame]*

`m_bFilterCharacterSaves=True`

Setting this to `False` will show all the profile's save games from all characters, and will not filter them based on the current active character profile.

`m_nMaxSaveGames=999`

Determines the maximum number of saves allowed. **Note:** This setting might require to change `m_bEnableLimitedSaves` from `False` to `True`.
#### Weapon Light Colours

*\[BIOC\_Base.BioWeapon]*

`m_vActivatedMatParamColor_Active=(R=1,G=2,B=20)`

Controls the RGB hue of weapon lights when the weapon is drawn, in multiples of 10\.

`m_vActivatedMatParamColor_Inactive=(R=20,G=2,B=1)`

Controls the RGB hue of weapon lights when the weapon is holstered, in multiples of 10\.
### BIOGuiResources.ini

*\[BIOC\_Base.BioSFHandler\_CharacterRecord]*

`nMaxRenegade=330
nMaxParagon=330`

Determines the amount of Paragon and Renegade points needed to reach a full bar (squad window), accordingly.
*\[BIOC\_Base.BioSFHandler\_HUD]*

`m_nShieldPointsPerBar=60`

On the shield bars indicator, determines how many shield points per bar.
*\[BIOC\_Base.BioSFHandler\_Shop]*

`DEFAULT_SELL_PRICE_FACTOR=0.15
MINIMUM_SELL_PRICE_FACTOR=0.15
MAXIMUM_SELL_PRICE_FACTOR=0.45

DEFAULT_BUY_PRICE_FACTOR=1.0
MINIMUM_BUY_PRICE_FACTOR=0.70
MAXIMUM_BUY_PRICE_FACTOR=1.0`

Determines the buy and sell prices modifier.
### BioParty.ini

#### Inventory

*\[BIOC\_Base.BioPlayerSquad]*

`m_nMaxInventoryItems=150
m_nMaxInventoryWarningThreshold=135`

Determines how large your inventory can get until you are required to reduce new items into omni\-gel, and when the game will warn you about reaching the limit.
### BioGame.ini

\[BIOC\_Base.BioPawnBehavior]

`m_fVehicleExpScaleFactor=0.4`

Determines the amount of Experience Points awarded for a kill performed in the Mako, relative to the amount you would get on foot. Raising this to 1\.0 will give you the same XP in the Mako as on foot. Raising over 1\.0 also works (useful for speedruns with necessity of max level achievement).
## In\-Game Console

### Enabling The Console

To enable the console, browse to and open the file `...Documents\BioWare\Mass Effect\Config\BioInput.ini` (the full location is mentioned above) in any text editor (Notepad, for example), but not with rich text editor (Microsoft Word, OpenOffice Writer, WritePad, and the likes).

In the file you opened, search for *\[Engine.Console]*, and add the line `ConsoleKey=Tilde` just under it. This will create a console around 3/4 the height of your screen. Adding the line `TypeKey=Tab` underneath `ConsoleKey` (or whatever keys you prefer) will instead create a console that is only one line wide at the bottom of your screen, allowing you full use of the console while allowing you to see in\-game going\-ons.

By default the *\[Engine.Console]* section will contain:
`[Engine.Console]
MaxScrollbackSize=1024
HistoryBot=-1
ConsoleKey=Tilde
TypeKey=Tab`

The code addition is marked as italicised text
**Note:** some keyboard layouts, specifically on non\-US English layouts, the Tilde key will map differently, and the game engine will not recognize the Tilde keyword. In this case, you will need to select a different key, such as Backslash, Tab, CapsLock, or any other to function as the console key.

Be advised that when Mass Effect boots, the BIOInput.ini may be overwritten, and thus will not have the console enabled. To prevent this, set the file to read\-only after making your changes.

### Usage

`GiveItem Self nSophistication Qa_SuperGun nmManufacturer`
Each command requires zero (`0`) or more arguments to be executed. `The GiveItem` code works the following way:

- The GiveItem command \- marked in **bold text**.
- The Self keyword \- indicates the target for the item (Use **`Target`** instead, when giving an item to a squad member).
- The Qa\_SuperGun item \- marked in **bold text** with the indication of the keyword *string* in *italic text*. Indicates the item you want.
- The nmManufacturer code \- indicates the code of the manufacturer of that item.
- The nSophistication number \- represents the 'level' of the item, which is the roman numeral (I, II, V, X, etc.) you see after the item name, but in the console is just a number (1\-10\).

### Commands

| Command | Description | Example |
| --- | --- | --- |
| **AddTargetToParty** | Adds the targeted pawn to your party. |  |
| **ChangeSize** *float* value | Sets Shepard's physical size. 1 is default, 0\.5 is half\-sized, 2\.0 is twice the size, etc. | `ChangeSize 0.01` |
| **God** | Invulnerability. Does not protect against hardcoded instant death scenarios. Mass Effect Legendary Edition only. |  |
| **GiveXP** *int* nValue | Gives/takes experience to player \- cannot lower current level. | `GiveXP 100` |
| **GiveTalentPoints** *int* numPoints | Gives/takes talent points to player. | `GiveTalentPoints -12` |
| **Set BioAttributesPawnParty m\_TalentPoints** *int* numPoints | Sets all active squad members' available talent points to the given value. | `Set BioAttributesPawnParty m_TalentPoints 10` |
| **GiveBonusTalent** *int* bonusIdentifier | Gives bonus talents to player. *See 'Talent Codes' below.* | `GiveBonusTalent 14` |
| **GiveSpectreTalents** | Unlocks Spectre talents. |  |
| **PickSpecialization** | Unlocks bonus classes. |  |
| **GiveSuperArmor** | Gives a light "Survivor X" armor with 8000 shields. |  |
| **GiveItem Self** *string* **QaSuperArmor** nmManufacturer | Gives ultimate armor with 10000\-20000 shields, depending on which manufacturer string is used | `GiveItem Self 10 QaSuperArmor Manf_Spectre03_Armor` |
| **GiveSuperGun** | Gives a geth assault rifle with 25000 points of damage. **Legendary Edition:**  The supergun is never automatically unholstered and must be manually selected from the menu or the previous/next weapon keybinds. |  |
| **GiveItem Self** *string* **Qa\_SuperGun** nmManufacturer | Gives geth\-style Assault Rifle which does 30000 to 40000 damage, depending on which manufacturer string is used. Non\-geth manufacturer codes may or may not be geth\-style. | `GiveItem Self 10 Qa_SuperGun Manf_Geth_Weap` |
| Set **BIOC\_Base.BioPawnBehavior m\_fInsanityEnemyDamageReduction** *\#\#F* | Changes how much damage enemies take on Insanity. A higher number means more damage, while a lower number means less damage. | `set BIOC_Base.BioPawnBehavior m_fInsanityEnemyDamageReduction 500F` |
| **GiveAll** | Gives one of each weapon, weapon mod, bioamp, omnitool, and grenade. Does not give armors. |  |
| **GiveAllBioAmps** *string* nmManufacturer | Gives all bioamps to player. | `GiveAllBioAmps Manf_Serrice_Bioamp` |
| **GiveAllOmniTools** *string* nmManufacturer | Gives all omnitools to player. | `GiveAllOmniTools Manf_Serrice_OmniTool` |
| **GiveAllGrenades** *string* nmManufacturer | Gives all weapons of grenades to player. |  |
| **GiveAllWeapons** *string* nmManufacturer | Gives all weapons of manufacturer to player. | `GiveAllWeapons Manf_Spectre03_Weap` |
| **GiveAllArmor** *string* nmManufacturer | Gives all armors of manufacturer to player. | `GiveAllArmor Manf_Spectre03_Armor` |
| **GiveAllArmorHuman** *string* nmManufacturer | Gives all human armors of manufacturer to player. |  |
| **GiveAllArmorTurian** *string* nmManufacturer | Gives all turian armors of manufacturer to player. |  |
| **GiveAllArmorQuarian** *string* nmManufacturer | Gives all quarian armors of manufacturer to player. |  |
| **GiveAllArmorKrogan** *string* nmManufacturer | Gives all krogan armors of manufacturer to player. |  |
| **GiveAllXMods** | Gives all weapon and armor mods. |  |
| **GiveItem** *string* nmActor *int* nSophistication *string* nmItemLabel *string* nmManufacturer | Gives item to player. The manufacturer string is optional. nSophistication determines the 'level' (I, II, ... X) | Armor: `GiveItem target 10 QuarianL manf_kassa_armor_colossus`Weapon: `GiveItem self 1 assault_rifle manf_hk_weap` |
| **GiveArmor** *string* nmActor *int* nSophistication *string* nmArmorLabel | Gives armor to player. |
| **SetParagon** *int* Points | Sets paragon points to specified value. (340 is max) |  |
| **SetRenegade** *int* Points | Sets renegade points to specified value. (340 is max) |  |
| **AdjustCredits** *int* \#\#\#\#\#\#\# | Increments or decrements the value of the party's credits, to a maximum of 9,999,999\. | `AdjustCredits +250000` |
| **InitCredits** *int* \#\#\#\#\#\#\# | Sets the party's current credits to this amount, with a maximum value of 9,999,999\. |  |
| **InitSalvage** *int* \#\#\# | Sets the amount of the party's total omni\-gel count, to a maximum value of 999\. |  |
| **InitMedigel** *int* \#\# | Sets the amount of the party's CURRENT medi\-gel count; maximum value can only be increased by purchasing medi\-gel count upgrades from stores. |  |
| **InitGrenades** *int* \#\# | Sets the amount of the party's CURRENT grenade count. |  |
| **Set BIOC\_Base.BioInventory m\_nMaxGrenades** *Int \#\#* | Sets the MAX amount of Grenades you can have. |  |
| **KillCurrentTarget** | Kills the currently targeted pawn. |
| **KillAll BioPawn** | Removes the player's henchmen from the party and all nearby pawns from the world. This is reported to cause problems when attempting to play through the full game without a party. |  |
| **SetRunSpeed** *float* speed | Sets your running speed to the specified value | `SetRunSpeed 99` (for slow speed), `SetRunSpeed 9999` (for fast speed) |
| **SuperSpeed** | Toggles on and off super\-fast movement. Using this twice will cancel out changes made by the SetRunSpeed command. |  |
| **UnlockAchievement** *int* nAchievementID | Unlocks an achievement. *See Achievement Codes below.* | `UnlockAchievement 5` |
| **SetGender** *int* \#\# | Changes the PC's gender; 0 is male, 1 is female. Appears to affect body and voice, but not dialog flags, and doesn't seem to kick in until you zone. |  |
| **Ghost** | Disables collision clipping, prevents falling. |  |
| **Fly** | Disables falling. |  |
| **Walk** | Enables collision clipping and falling. |  |
| **Teleport** | Moves player to location at crosshair. |  |
| **Pause** | Pauses the game. Useful for pausing during dialogs. |  |
| **At** *string* newArea | Moves player to new area, places player 'at' the area specified. |  |
| **SpawnVehicle** | Spawns a Mako vehicle at the cursor location. |  |
| **upgradevehicle 6 vehthrusterforcebooster** | Triples the thrust (power) of the Mako underjets. Original game only.Using 5 instead of 6 allows for same boost, but Mako doesn't have to touch ground for the thruster to function again, allowing for repeated thrusts to stay off the ground. Gentle thrusts are needed to avoid falling damage. |  |
| **FOV** *int* \#\# | Changes the Field of View to the specified degrees. | `FOV 45` |
| **Setbind** *string* key *string* command | Binds the specified command to the specified key | `Setbind CapsLock Showhud` |
| **SloMo** *float* multiplier | Changes the game speed by the given multiplier (2\.0 is twice as fast, 0\.5 is half\-speed) |  |
| **StasisAll** | Freezes all NPCs in place permanently. This cannot be reversed without loading a savegame and should not be used aside from things like taking screenshots. |  |
| **ToggleFlyCam** | Toggles free camera mode |  |
| **CamToggleDebug** | Moves the camera slightly up and back of the player. |  |
| **Set BioCameraBehaviorFree m\_fMovementScalar** *float* | Fine\-tune the free camera's directional speed. Does not work in Mass Effect Legendary Edition. | `Set BioCameraBehaviorFree m_fMovementScalar 1.00`  (very slow)  `Set BioCameraBehaviorFree m_fMovementScalar 6000.00` (very fast) |
| **ShowHUD** / **ToggleHUD** | Toggles most parts of the HUD. |  |
| **Show Scaleform** | Toggles all of the  Scaleform  elements off (HUD, menus text, quick power bar). |  |
| **Show Vignette** | Toggles the vignette effect on or off. Mass Effect Legendary Edition only. |  |
| **PlayersOnly** | Toggles the game pause, allowing the player to line up a screenshot. |
| **SaveGame** *string* | Saves the game to filename indicated by *string* (See note 1). |  |
| **LoadGame** *string* | Loads saved game indicated by *string* filename (See note 2). |  |
| **Quit** / **Exit** | Exit game |  |
| **Shot** | Takes a screenshot exactly as it appears on the screen | `Shot` |
| **TiledShot** *int* multiplier *int* overlapPixels | Takes a screenshot at many times the resolution of the screen. Postprocessing effects are rendered at default resolution rather than the target one, however, which may result in visual artifacts around the 'tile' edges. | `TiledShot 3x3` \- takes a screenshot with a grid of 3 by 3\. If the game is running in resolution of 1440x900, this will produce a 4320x2700 screenshot.`TiledShot 2` \- produces a screenshot twice the size of the game resolution.`TiledShot 2 200` \- takes a screenshot twice the size of the game resolution, and overlaps 200 pixels from every grid cell. The overlap may help ensure image continuity although it is not 100% assured. |
| **Stat FPS** | Toggles the display of your framerate |  |
| **Obj Classes** | See Unreal engine console documentation. |  |
| **Obj Dependancies** | See Unreal engine console documentation. |  |
| **Obj Hash** | See Unreal engine console documentation. |  |
| **Obj Linkers** | See Unreal engine console documentation. |  |
| **Get** *string* propertyidentifier *string* value | See Unreal engine console documentation. |  |
| **Set** *string* propertyidentifier *string* value | See Unreal engine console documentation. |  |
| **SetSensitivity** *int* mouseSensitivity | Sets mouse sensitivity from the console. Overrides any settings. |  |
| **Exec** *string* filename | Executes a specified file under the Mass Effect\\Binaries directory |  |
| **ce hench\_picksquad** | Select a new squad from the selection screen |  |

**Notes:**

1. SaveGame `John00_QuickSave`. The first part is the character name followed by the number count of that character name (such as having more than one John). The second part is the save name. `John00_1` will result in "Save 1" in the loading screen user interface. `John00_tester` will result in "Save 0" in the loading screen.
Excluding the Name00 from the string will result in a save file that cannot be accessed via the user interface and can only be loaded with the `LoadGame` command.
2. LoadGame `John00_QuickSave`. Loading a game such as *tester* without having loaded a previous save in the career the save game was created from will result in unrecoverable errors and you will be forced to exit the game via **exit** or **quit**.

### Reference

#### Generic types

- Heavy\_Armor
- Medium\_Armor
- Light\_Armor
- Assault\_Rifle
- Sniper\_Rifle
- Shotgun
- Pistol
- Bioamp
- Omnitool
- Gethgun\_Pulse

Example codes

**BIO AMP:** Giveitem self 10 bioamp manf\_serrice\_bioamp (Mark 10 Serrice bioamp).

**OMNITOOL:** Giveitem self 10 omnitool manf\_serrice\_omnitool (Mark 10 Serrice Omnitool).

**ARMOR:** Giveitem self 10 TurianM manf\_kassa\_armor\_colossus (Mark 10 Medium Turian armor).

**WEAPON:** Giveitem self 10 Assault\_Rifle manf\_Spectre03\_Weap (Mark 10 Spectre Assault rifle).

**ARMOR MODS:** Giveitem self 10 x\_armor\_shieldVI (Mark 10 shields mod for armor).

**GRENADE MODS:** Giveitem self 10 x\_Gammo\_HE (Mark 10 High Energy Explosive).

**WEAPON AMMO MODS:** giveitem self 10 x\_wammo\_Harpoon (Mark 10 Harpoon rounds).

**WEAPON GEAR MODS:** Giveitem self 10 x\_wgear\_frictionlessMAT (Mark 10 frictionless mats)

#### Race\-specific types

- HumanL
- HumanM
- HumanH
- QuarianL
- TurianL
- TurianM
- TurianH
- KroganM
- KroganH

#### Manufacturer Codes

| Item | Code | Manufacturer |
| --- | --- | --- |
| Agent Armor | Manf\_Aldrin\_Armor\_Agent | Aldrin Labs |
| Hydra Armor | Manf\_Aldrin\_Armor\_Hydra |
| Onyx Armor | Manf\_Aldrin\_Armor\_Onyx |
| Bluewire Omnitool | Manf\_Aldrin\_OmniTool |
| Solaris BioAmp | Manf\_Aldrin\_BioAmp |
| Mercenary Armor | Manf\_Ariake\_Armor\_Mercenary | Ariake Technologies |
| Weapon | Manf\_Ariake\_Weap |
| Logic Arrest Omni\-Tool | Manf\_Ariake\_OmniTool |
| Predator L/M/H Armor | Manf\_Armax\_Armor\_Predator | Armax Arsenal |
| Weapon | Manf\_Armax\_Weap |
| GeminiBio\-amp | Manf\_Armax\_BioAmp |
| Nexus Omni\-tool | Manf\_Armali\_OmniTool | Armali Council |
| Prodigy Bio\-amp | Manf\_Armali\_BioAmp |
| Explorer Armor | Manf\_Devlon\_Armor\_Explorer | Devlon Industries |
| Liberator Armor | Manf\_Devlon\_Armor\_Liberator |
| Survivor Armor | Manf\_Devlon\_Armor\_Survivor |
| Thermal Armor | Manf\_Devlon\_Armor\_Thermal |
| Weapon | Manf\_Devlon\_Weap |
| Duelist Armor | Manf\_Elanus\_Armor\_Duelist | Elanus Risk Control |
| Guardian Armor | Manf\_Elanus\_Armor\_Guardian |
| Warlord Armor | Manf\_Elanus\_Armor\_Warlord |
| Weapon | Manf\_Elanus\_Weap |
| Assassin Armor | Manf\_Elkoss\_Armor\_Assassin | Elkoss Combine |
| Gladiator Armor | Manf\_Elkoss\_Armor\_Gladiator |
| Weapon | Manf\_Elkoss\_Weap |
| Cipher Omni\-tool | Manf\_Elkoss\_OmniTool |
| Battlemaster Armor | Manf\_Geth\_Armor\_BattleMaster | Geth Armory |
| Berserker Armor | Manf\_Geth\_Armor\_Berserker |
| Rage Armor | Manf\_Geth\_Armor\_Rage |
| Weapon | Manf\_Geth\_Weap |
| Geth Pulse Rifle | Gethgun\_Pulse\_Player Manf\_Geth\_Weap |
| Geth Shotgun | Gethgun\_Shotgun Manf\_Geth\_Weap |
| Geth Sniper Rifle | Gethgun\_Sniper Manf\_Geth\_Weap |
| Geth Anti\-Tank Gun | Gethgun\_AntiTank Manf\_Geth\_Weap |
| Silverback Armor | Manf\_HK\_Armor\_Hornet | Hahne\-Kedar |
| Mantis Armor | Manf\_HK\_Armor\_Mantis |
| Predator Armor | Manf\_HK\_Armor\_Predator |
| Scorpion Armor | Manf\_HK\_Armor\_Scorpion |
| Ursa Armor | Manf\_HK\_Armor\_Ursa |
| Weapon | Manf\_HK\_Weap |
| Weapon | Manf\_HK\_WeapAppr2 |
| Colossus Armor | Manf\_Kassa\_Armor\_Colossus | Kassa Fabrication |
| Weapon | Manf\_Kassa\_Weap |
| Polaris Omni\-tool | Manf\_Kassa\_OmniTool |
| Polaris Bio\-amp | Manf\_Kassa\_BioAmp |
| Titan Armor | Manf\_Rosen\_Armor\_Titan | Rosenkov Materials |
| Weapon | Manf\_Rosen\_Weap |
| Phantom Armor | Manf\_Serrice\_Armor\_Phantom | Serrice Council |
| Omni\-tool | Manf\_Serrice\_OmniTool |
| Bio\-amp | Manf\_Serrice\_BioAmp |
| Phoenix Armor | Manf\_Sitta\_Armor\_Phoenix | Sirta FoundationNote: 'Sitta' is not a typo |
| Omni\-tool | Manf\_Sitta\_OmniTool |
| Bio\-amp | Manf\_Sitta\_BioAmp |
| Weapon | Manf\_Haliat\_Weap | Haliat Armory |
| Crisis Armor\* | Manf\_Jorman\_Armor\_Crisis | Jormangund Technology |
| Hazard Armor\* | Manf\_Jorman\_Armor\_Hazard |
| Weapon | Manf\_Jorman\_Weap |
| Partisan Armor\* | Manf\_Batarian\_Armor\_Partisan | Batarian State Arms |
| Skirmish Armor\* | Manf\_Batarian\_Armor\_Skirmish |
| Weapon | Manf\_Batarian\_Weap |
| Freedom Armor\* | Manf\_Cerberus\_Armor\_Freedom | Cerberus Skunkworks |
| Hoplite Armor\* | Manf\_Cerberus\_Armor\_Hoplite |
| Weapon | Manf\_Cerberus\_Weap |
| Janissary Armor\* | Manf\_HKShadow\_Armor\_Janissary | Hahne\-Kedar Shadow Works |
| Spectre Armor\* | Manf\_HKShadow\_Armor\_Spectre |
| Weapon | Manf\_HKShadow\_Weap |
| Predator L/M/H Armor VI | Manf\_Spectre01\_Armor | Spectre Master Gear |
| Predator L/M/H Armor VII | Manf\_Spectre02\_Armor |
| Predator L/M/H Armor X | Manf\_Spectre03\_Armor |
| Weapon \- Basic Gear\* | Manf\_Spectre01\_Weap |
| Weapon \- Advanced Gear\* | Manf\_Spectre02\_Weap |
| Weapon \- Master Gear | Manf\_Spectre03\_Weap |
| Omni\-tool \- Basic Gear\* | Manf\_Spectre01\_OmniTool |
| Omni\-tool \- Advanced Gear\* | Manf\_Spectre02\_OmniTool |
| Omni\-tool \- Master Gear\* | Manf\_Spectre03\_OmniTool |
| Bio\-amp \- Basic Gear\* | Manf\_Spectre01\_BioAmp |
| Bio\-amp \- Advanced Gear\* | Manf\_Spectre02\_BioAmp |
| Bio\-amp \- Master Gear\* | Manf\_Spectre03\_BioAmp |

**Note:** Items marked with an asterisk(\*) are not normally obtainable in\-game, and can only be acquired through the console.

#### Armor Mods

Example: GiveItem Self 10 X\_Armor\_MedicalExo

- X\_Armor\_AblCoating (Ablative Coating)
- X\_Armor\_CombatExo (Combat Exoskeleton)
- X\_Armor\_CushGel
- X\_Armor\_EnerWeave (Energized Weave)
- X\_Armor\_EnvSeals (Toxic Seals)
- X\_Armor\_Exoskel (Exoskeleton)
- X\_Armor\_FieldRegen (Shield Regenerator)
- X\_Armor\_FirstAid (First Aid Interface)
- X\_Armor\_HardWeave (Hardened Weave)
- X\_Armor\_HazardSeals (Hazard Seals)
- X\_Armor\_KineticBuff (Kinetic Buffer)
- X\_Armor\_KineticExo (Kinetic Exoskeleton)
- X\_Armor\_MedicalExo (Medical Exoskeleton)
- X\_Armor\_MedicalIntf (Medical Interface)
- X\_Armor\_MotoJoints (Motorized Joints)
- X\_Armor\_Plating (Armor Plating)
- X\_Armor\_PressSeals (Pressurized Seals)
- X\_Armor\_RegenPlating (Energized Plating)
- X\_Armor\_ShieldBatt (Shield Battery)
- X\_Armor\_ShieldMod (Shield Modulator)
- X\_Armor\_ShieldVI (Shield Interface)
- X\_Armor\_ShockAbs (Shock Absorbers)
- X\_Armor\_StimPack (Stimulant Pack)

#### Grenade Ammo Mods

Example: GiveItem Self 10 X\_GAmmo\_Incendiary

- X\_GAmmo\_AntiThorian (Anti\-Thorian Gas I)
- X\_GAmmo\_Cryo (Cryo Explosive)
- X\_GAmmo\_Fusion (Fusion Explosive)
- X\_GAmmo\_HE (High Explosive)
- X\_GAmmo\_Incendiary (Incendiary Explosive)

#### Weapon Ammo Mods

Example: GiveItem Self 10 X\_WAmmo\_SnowBlind

- X\_WAmmo\_AntiPersonnel (Anti\-Personnel Rounds)
- X\_WAmmo\_AP (Armor Piercing Rounds)
- X\_WAmmo\_Chemical (Chemical Rounds)
- X\_WAmmo\_Cryo (Cryo Rounds)
- X\_WAmmo\_Hammerhead (Hammerhead Rounds)
- X\_WAmmo\_Harpoon (Harpoon Rounds)
- X\_WAmmo\_HE (High Explosive Rounds)
- X\_WAmmo\_HyperRail (Does nothing. May have been intended for mod of same name.)
- X\_WAmmo\_Incendiary (Incendiary Rounds)
- X\_WAmmo\_Inferno (Inferno Rounds)
- X\_WAmmo\_Phasic (Phasic Rounds)
- X\_WAmmo\_Polonium (Polonium Rounds)
- X\_WAmmo\_Proton (Proton Rounds)
- X\_WAmmo\_Radioactive (Radioactive Rounds)
- X\_WAmmo\_Shredder (Shredder Rounds)
- X\_WAmmo\_Sledgehammer (Sledgehammer Rounds)
- X\_WAmmo\_SnowBlind (Snowblind Rounds)
- X\_WAmmo\_Striker (Obsolete code)
- X\_WAmmo\_Tungsten (Tungsten Rounds)

#### Weapon Mods

Example: GiveItem Self 10 X\_WGear\_ScramRail

- X\_WGear\_CombatScanner (Combat Scanner)
- X\_WGear\_CombatSensor (Combat Sensor)
- X\_WGear\_CombatVI (Combat Optics)
- X\_WGear\_FrictionlessMat (Frictionless Materials)
- X\_WGear\_HeatSink (Heat Sink)
- X\_WGear\_HighCaliber (High Caliber Barrel)
- X\_WGear\_HyperRail  (Hyper Rail)
- X\_WGear\_ImpSighting (Improved Sighting)
- X\_WGear\_KineticCoil (Kinetic Coil)
- X\_WGear\_KineticStab (Kinetic Stabilizer)
- X\_WGear\_RailExt (Rail Extension)
- X\_WGear\_RecoilDamp (Recoil Damper)
- X\_WGear\_ScramRail (Scram Rail)
- X\_WGear\_TargettingVI

#### Talents

Example: GiveBonusTalent 7

- 0 (Pistols)
- 7 (Assault Rifles)
- 14 (Shotguns)
- 21 (Sniper Rifles)
- 28 (Light Armor)
- 29 (Tactical Armor)
- 35 (Assault Training)
- 49 (Throw)
- 50 (Lift)
- 56 (Warp)
- 57 (Singularity)
- 63 (Barrier)
- 64 (Stasis)
- 84 (Electronics)
- 86 (Damping)
- 91 (Hacking)
- 93 (Decryption)
- 98 (First Aid)
- 99 (Medicine)
- 137 (Shock Trooper: Soldier)
- 138 (Shock Trooper: Vanguard)
- 141 (Commando: Soldier)
- 142 (Commando: Infiltrator)
- 145 (Operative: Engineer)
- 146 (Operative: Infiltrator)
- 149 (Medic: Engineer)
- 150 (Medic: Sentinel)
- 153 (Nemesis: Adept)
- 154 (Nemesis: Vanguard)
- 157 (Bastion: Adept)
- 158 (Bastion: Sentinel)

Difference between same specializations are first 6 points that are same as starting class mentioned in brackets.

When adding the bonus talents string be very careful for the game will only allow you to use around 5\-6 offensive abilities for use in game, no matter how many abilities you add. So keep in mind that firstly you should add the abilities which are most useful*(ex.\- Warp \& Singularity)* fully upgrade them, then go for the other bonus talents. Also one might wanna start adding talents with *spectre* \& *class talents* like \- "commando".

#### Achievements

Example: UnlockAchievement 12

| Achievement | Mass Effect™ (2007\) | Mass Effect™ Legendary Edition |
| --- | --- | --- |
| Medal of Honor Achievement | 1 | 0 |
| Medal of Heroism Achievement | 2 | 1 |
| Distinguished Service Medal Achievement | 3 | 2 |
| Council Legion of Merit Achievement | 4 | 3 |
| Honorarium of Corporate Service Achievement | 5 | 4 |
| Long Service Medal Achievement | 6 | 40 |
| Distinguished Combat Medal Achievement | 7 |  |
| Medal of Valor Achievement | 8 |  |
| Pistol Expert Achievement | 9 |  |
| Shotgun Expert Achievement | 10 |  |
| Assault Rifle Expert Achievement | 11 |  |
| Sniper Expert Achievement | 12 |  |
| Lift Mastery Achievement | 13 | 5 |
| Throw Mastery Achievement | 14 | 6 |
| Warp Mastery Achievement | 15 | 7 |
| Singularity Mastery Achievement | 16 | 8 |
| Barrier Mastery Achievement | 17 | 9 |
| Stasis Mastery Achievement | 18 | 10 |
| Damping Specialist Achievement | 19 | 11 |
| AI Hacking Specialist Achievement | 20 | 12 |
| Overload Specialist Achievement | 21 | 13 |
| Sabotage Specialist Achievement | 22 | 14 |
| First Aid Specialist Achievement | 23 | 15 |
| Neural Shock Specialist Achievement | 24 | 16 |
| Scholar Achievement | 26 | 18 |
| Completionist Achievement | 27 |  |
| Tactician Achievement | 28 |  |
| Medal of Exploration Achievement | 29 |  |
| Rich Achievement | 30 |  |
| Dog of War Achievement | 31 |  |
| Geth Hunter Achievement | 32 |  |
| Soldier Ally Achievement | 33 | 23 |
| Sentinel Ally Achievement | 34 | 24 |
| Krogan Ally Achievement | 35 | 25 |
| Turian Ally Achievement | 36 | 26 |
| Quarian Ally Achievement | 37 | 27 |
| Asari Ally Achievement | 38 | 28 |
| Power Gamer Achievement | 39 |  |
| Extreme Power Gamer Achievement | 40 |  |
| Renegade Achievement | 41 |  |
| Paragon Achievement | 42 |  |
| Paramour Achievement | 43 |  |
| Spectre Inductee Achievement | 44 |  |
| Charismatic Achievement | 45 |  |
| Search and Rescue Achievement | 46 |  |
| Colonial Savior Achievement | 47 |  |
| Undisputed Achievement | 48 |  |
| New Sheriff in Town Achievement | 49 |  |
| Best of the Best Achievement | 50 |  |

Achievement 25 (in the original Mass Effect) is unknown.

#### Area Codes

Structure: Level development code \- Official name \- Console command

##### Main levels

**Group:** 00 Files (Masters)

| ICE00 Master | Noveria | At BIOA\_ICE00 |
| --- | --- | --- |
| JUG00 Master | Virmire | At BIOA\_JUG00 |
| LAV00 Master | Therum | At BIOA\_LAV00 |
| LOS00 Master | Ilos | At BIOA\_LOS00 |
| STA00 Master | Citadel | At BIOA\_STA00 |
| WAR00 Master | Feros | At BIOA\_WAR00 |

**Group:** END (End\-game in Citadel)

| END00 |  | At BIOA\_END00 |
| --- | --- | --- |
| END20\_00 | Citadel | At BIOA\_END00 Start\_END20\_00 |
| END70\_00 | Citadel Plaza | At BIOA\_END00 Start\_END70\_00 |
| END80\_00 | Citadel Tower Space Walk | At BIOA\_END00 Start\_END80\_00 |

**Group:** ICE (Noveria)

| ICE00 |  | At BIOA\_ICE00 |
| --- | --- | --- |
| ICE20\_01 | Alpine City | At BIOA\_ICE00 Start\_ICE20\_01 |
| ICE25\_01 | Aleutsk Valley | At BIOA\_ICE00 Start\_ICE25\_01 |
| ICE50\_01 | Peak 15 Utility Station | At BIOA\_ICE00 Start\_ICE50\_01 |
| ICE60\_01 | Science Station | At BIOA\_ICE00 Start\_ICE60\_01 |
| ICE60\_14 | Binary Helix Hotlabs | At BIOA\_ICE00 Start\_ICE60\_14 |

**Group:** JUG (Virmire)

| JUG20\_00 | Vehicle approach to the Salarian encampment | At BIOA\_JUG00 Start\_JUG00\_01 |
| --- | --- | --- |
| JUG20\_01 | Vehicle landing zone and first barricade | At BIOA\_JUG00 Start\_JUG20\_01 |
| JUG20\_02 | Anti\-Aircraft turret and second barricade | At BIOA\_JUG00 Start\_JUG20\_02 |
| JUG20\_03 | Final approach to the salarian encampment | At BIOA\_JUG00 Start\_JUG20\_03 |
| JUG40\_00 | Pontoon approach to Saren's Facility | At BIOA\_JUG00 Start\_JUG40\_00 |
| JUG40\_01 | Entrance from the Salarian Camp and the first combat | At BIOA\_JUG00 Start\_JUG40\_01 |
| JUG40\_02 | Geth Communications Tower | At BIOA\_JUG00 Start\_JUG40\_02 |
| JUG40\_03 | Jungle approach to the pontoons (mine field) | At BIOA\_JUG00 Start\_JUG40\_03 |
| JUG40\_04 | Pontoons: Entrance and artillery relay (optional objective) | At BIOA\_JUG00 Start\_JUG40\_04 |
| JUG40\_05 | Pontoons: Geth Flyer landing pad (optional objective) | At BIOA\_JUG00 Start\_JUG40\_05 |
| JUG40\_06 | Pontoons: Artillery ammo dump | At BIOA\_JUG00 Start\_JUG40\_06 |
| JUG40\_07 | Pontoons: Geth Flyer landing pad (optional objective) | At BIOA\_JUG00 Start\_JUG40\_07 |
| JUG40\_08 | Entrance to Saren's facility | At BIOA\_JUG00 Start\_JUG40\_08 |
| JUG70\_00 | Saren's indoctrination and Krogan Genophage research facility | At BIOA\_JUG00 Start\_JUG70\_01 |
| JUG70\_01 | Front entrance to the warehouse | At BIOA\_JUG00 Start\_JUG70\_01 |
| JUG70\_02 | Warehouse combat with indoctrinates | At BIOA\_JUG00 Start\_JUG70\_02 |
| JUG70\_03 | Security Office and Detention cells | At BIOA\_JUG00 Start\_JUG70\_03 |
| JUG70\_04 | Krogan Genophage/Indoctrination Labs | At BIOA\_JUG00 Start\_JUG70\_04 |
| JUG70\_05 | Indoctrinated Prisoner Barracks | At BIOA\_JUG00 Start\_JUG70\_05 |
| JUG70\_06 | Sewer combat with indoctrinates | At BIOA\_JUG00 Start\_JUG70\_06 |
| JUG70\_07 | Walkway between Sovereign's Tower and the Breeding Facility | At BIOA\_JUG00 Start\_JUG70\_07 |
| JUG70\_08 | Security Hardpoint before Sovereign's Tower | At BIOA\_JUG00 Start\_JUG70\_08 |
| JUG70\_09 | Facade for the Interior trench | At BIOA\_JUG00 Start\_JUG70\_09 |
| JUG70\_10 | Facade for the ecterior ocean view | At BIOA\_JUG00 Start\_JUG70\_10 |
| JUG70\_11 | Communications tower (Uplink to Sovereign) | At BIOA\_JUG00 Start\_JUG70\_11 |
| JUG80\_00 | Krogan Breeding Facility | At BIOA\_JUG00 Start\_JUG80\_01 |
| JUG80\_01 | Spiral Breakwater path | At BIOA\_JUG00 Start\_JUG80\_01 |
| JUG80\_02 | Entrance Combat on the Breakwater | At BIOA\_JUG00 Start\_JUG80\_02 |
| JUG80\_03 | Facade of the ocean view | At BIOA\_JUG00 Start\_JUG80\_03 |
| JUG80\_04 | Turret one Interior (Sabotage) | At BIOA\_JUG00 Start\_JUG80\_04 |
| JUG80\_05 | Krogan breeding trench entrance | At BIOA\_JUG00 Start\_JUG80\_05 |
| JUG80\_06 | Empty Trench | At BIOA\_JUG00 Start\_JUG80\_06 |
| JUG80\_07 | Central trench hub (Bomb Site/Saren Encounter) | At BIOA\_JUG00 Start\_JUG80\_07 |
| JUG80\_08 | Upper trench fortification | At BIOA\_JUG00 Start\_JUG80\_08 |
| JUG80\_09 | Sealed Krogan Breeding Trench | At BIOA\_JUG00 Start\_JUG80\_09 |
| JUG80\_10 | Breakwater combat corridor | At BIOA\_JUG00 Start\_JUG80\_10 |
| JUG80\_11 | Upper facade structure (Sailes and Details) | At BIOA\_JUG00 Start\_JUG80\_11 |
| JUG80\_12 | Lift to Turret two | At BIOA\_JUG00 Start\_JUG80\_12 |
| JUG80\_13 | Turret two interior (Sabotage) | At BIOA\_JUG00 Start\_JUG80\_13 |
| JUG80\_14 | Lift from Turret two to breakwater | At BIOA\_JUG00 Start\_JUG80\_14 |

**Group:** LAV (Therum)

| LAV00 |  | At BIOA\_LAV00 |
| --- | --- | --- |
| LAV60\_01 | Ring of Fire | At BIOA\_LAV00 Start\_LAV60\_01 |
| LAV70\_01 | Knossos Ruins | At BIOA\_LAV00 Start\_LAV70\_01 |

**Group:** LOS (Ilos Ruins)

| LOS00 |  | At BIOA\_LOS00 |
| --- | --- | --- |
| LOS10\_01 | Landing Zone | At BIOA\_LOS00 Start\_LOS10\_01 |
| LOS30\_02 | Security Station | At BIOA\_LOS00 Start\_LOS30\_02 |
| LOS40\_01 | Archives | At BIOA\_LOS00 Start\_LOS40\_01 |
| LOS50\_01 | Trench Run | At BIOA\_LOS00 Start\_LOS50\_01 |

**Group:** NOR (Normandy)

| NOR00 |  | At BIOA\_NOR00 |
| --- | --- | --- |
| NOR10\_01 | Cockpit | At BIOA\_NOR00 Start\_NOR10\_01 |
| NOR10\_02 | Hallway to Cockpit | At BIOA\_NOR00 START\_NOR10\_02 |
| NOR10\_03 | Galaxy Map | At BIOA\_NOR00 START\_NOR10\_03 |
| NOR10\_04 | Comm Room | At BIOA\_NOR00 START\_NOR10\_04 |
| NOR10\_05 | Stairwell | At BIOA\_NOR00 START\_NOR10\_05 |
| NOR10\_06 | Dining | At BIOA\_NOR00 START\_NOR10\_06 |
| NOR10\_07 | Medical Bay | At BIOA\_NOR00 START\_NOR10\_07 |
| NOR10\_08 | Liara's Room | At BIOA\_NOR00 START\_NOR10\_08 |
| NOR10\_09 | Captain's Quarters | At BIOA\_NOR00 START\_NOR10\_09 |
| NOR10\_10 | Elevator to 2nd Deck | At BIOA\_NOR00 START\_NOR10\_10 |
| NOR10\_11 | Garage | At BIOA\_NOR00 START\_NOR10\_11 |
| NOR10\_12 | Engineering | At BIOA\_NOR00 START\_NOR10\_12 |
| INNERAIRLOCK | Airlock | At BIOA\_NOR00 START\_INNERAIRLOCK |

**Group:** PRO (Eden Prime)

| PRO00 |  | At BIOA\_PRO00 |
| --- | --- | --- |
| PRO10\_01 | Landing Zone | At BIOA\_PRO00 Start\_PRO10\_01 |

**Group:**  STA (Citadel)

| STA00 |  | At BIOA\_STA00 |
| --- | --- | --- |
| STA20\_01 | The Presidium | At BIOA\_STA00 start\_STA20\_01 |
| STA20\_02 | Elevator to Citadel Tower | AT BIOA\_STA00 START\_STA20\_02 |
| STA30\_01 | Marshal's Training Grounds | At BIOA\_STA00 Start\_STA30\_01 |
| STA60\_01 | Wards | At BIOA\_STA00 Start\_STA60\_01 |
| STA70\_01 | Citadel Council Tower | At BIOA\_STA00 Start\_STA70\_01 |

**Group:** WAR (Feros)

| WAR00 |  | At BIOA\_WAR00 |
| --- | --- | --- |
| WAR20\_01 | Human colony | At BIOA\_WAR00 Start\_WAR20\_01 |
| WAR30\_01 | Thorian Lair | At BIOA\_WAR00 Start\_WAR30\_01 |
| WAR40\_01 | War Zone | At BIOA\_WAR00 Start\_WAR40\_01 |
| WAR50\_01 | Imperator Camp | At BIOA\_WAR00 Start\_WAR50\_01 |

**Group:** UNC52 (Asteroid X57\)

| UNC52 | At BIOA\_UNC52 |
| --- | --- |
| Exterior of Main Base | At BIOA\_UNC52 START\_UNC52\_EXT\_MAINBASE |
| Interior of Main Base | At BIOA\_UNC52 START\_UNC52\_INT\_MAINBASE |
| Exterior of Torch 1 | At BIOA\_UNC52 START\_UNC52\_EXT\_TORCH1 |
| Interior of Torch 1 | At BIOA\_UNC52 START\_UNC52\_INT\_TORCH1 |
| Exterior of Torch 2 | At BIOA\_UNC52 START\_UNC52\_EXT\_TORCH2 |
| Interior of Torch 2 | At BIOA\_UNC52 START\_UNC52\_INT\_TORCH2 |
| Exterior of Torch 3 | At BIOA\_UNC52 START\_UNC52\_EXT\_TORCH3 |
| Interior of Torch 3 | At BIOA\_UNC52 START\_UNC52\_INT\_TORCH3 |

**Group:** UNC (Uncharted)

| UNC10 | Klensal | At BIOA\_UNC10 |
| --- | --- | --- |
| UNC11 | Xawin | At BIOA\_UNC11 |
| UNC13 | Mavigon | At BIOA\_UNC13 |
| UNC17 | Antibaar | At BIOA\_UNC17 |
| UNC20 | Trebin | At BIOA\_UNC20 |
| UNC21 | Rayingri | At BIOA\_UNC21 |
| UNC24 | Altahe | At BIOA\_UNC24 |
| UNC25 | Edolus | At BIOA\_UNC25 |
| UNC30 | Chohe | At BIOA\_UNC30 |
| UNC31 | Amaranthine | At BIOA\_UNC31 |
| UNC42 | Nonuel | At BIOA\_UNC42 |
| UNC51 | Luna | At BIOA\_UNC51 |
| UNC53 | Agebinium | At BIOA\_UNC53 |
| UNC54 | Presrop | At BIOA\_UNC54 |
| UNC55 | Solcrum | At BIOA\_UNC55 |
| UNC61 | Tuntau | At BIOA\_UNC61 |
| UNC62 | Nepheron | At BIOA\_UNC62 |
| UNC71 | Metgos | At BIOA\_UNC71 |
| UNC73 | Nepmos | At BIOA\_UNC73 |
| UNC80 | Nodacrux | At BIOA\_UNC80 |
| UNC81 | Chasca | At BIOA\_UNC81 |
| UNC82 | Ontarom | At BIOA\_UNC82 |
| UNC83 | Casbin | At BIOA\_UNC83 |
| UNC84 | Eletania | At BIOA\_UNC84 |
| UNC90 | Sharjila | At BIOA\_UNC90 |
| UNC92 | Binthu | At BIOA\_UNC92 |
| UNC93 | Maji | At BIOA\_UNC93 |

**Group:** FRE (Freighters)

| FRE31 | Freighter of Doom (SP116\) Tarrus IV Freighter | At BIOA\_FRE31 |
| --- | --- | --- |
| FRE32 | Hostage Situation (SP111\) MSV Ontario Freighter | At BIOA\_FRE32 |
| FRE33 | CSI (SP104\) MSV Worthington Freighter | At BIOA\_FRE33 |
| FRE34 | Garrus' Subplot (SP201\) MSV Fedele Freighter | At BIOA\_FRE34 |
| FRE35 | Depot Sigma\-23 (SP107\) Gorgon System Depot Freighter | At BIOA\_FRE35 |

**Group:** PRC2 (Pinnacle Station)

| Pinnacle Station | At BIOA\_PRC2 |
| --- | --- |
| Intai'sei (Shepard's Apartment) | At BIOA\_PRC2AA |

##### Removed levels

Areas of this group were used during game development and are no longer available.

**Group:** DEV (Development)

| TEST\_BuildCheck1 | At TEST\_BuildCheck1 |
| --- | --- |
| TEST\_BuildCheck2 | At TEST\_BuildCheck2 |
| TEST\_MUSEUM\_CHAR | At TEST\_MUSEUM\_CHAR |
| Character \& Placeable Gallery | At zGB\_CharGallery |
| BIOA\_CoverDemo | At BIOA\_CoverDemo |
| BIOA\_zCOM10 | At BIOA\_zCOM10 |
| BIOA\_zCOM20 | At BIOA\_zCOM20 |
| BIOA\_CombatTest100 | At BIOA\_CombatTest100 |
| BIOA\_CombatTest200 | At BIOA\_CombatTest200 |
| BIOA\_zVEH10 | At BIOA\_zVEH10 |
| BIOA\_zCHR10 | At BIOA\_zCHR10 |
| BIOA\_zCHR20 | At BIOA\_zCHR20 |
| Combat Stress Test | At zGB\_CombatStressTest |
| characterprep\_00 | At characterprep\_00 |
| test\_into\_nor00 | At test\_into\_nor00 |
| LAV20\_01 | Throw Down Plaza | At BIOA\_LAV00 Start\_LAV20\_00 |
| LAV40\_01 | Foundry | At BIOA\_LAV00 Start\_LAV40\_01 |
| ICE70\_01 | Binary Helix Hot Labs | At BIOA\_ICE00 Start\_ICE70\_01 |
| STA90\_02 | Oculon | AT BIOA\_STA00 START\_STA90\_02 |
| LOS20\_02 | Power Station | At BIOA\_LOS00 Start\_LOS20\_02 |

**Group:** FRE (Freighters)

| FRE13 | Light content: Freighter Template 04 | At BIOA\_FRE13 |
| --- | --- | --- |
| FRE14 | Light content: Freighter Template 05 | At BIOA\_FRE14 |
| FRE15 | Light content: Freighter Template 06 | At BIOA\_FRE15 |
| FRE16 | Light content: Freighter Template 07 | At BIOA\_FRE16 |
| FRE17 | Light content: Freighter Template 08 | At BIOA\_FRE17 |
| FRE18 | Light content: Freighter Template 09 | At BIOA\_FRE18 |
| FRE19 | Light content: Freighter Template 10 | At BIOA\_FRE19 |

**Group:** MIN (Mine)

| MIN\_00 | Light Content: mining Template 01 | At BIOA\_MIN00 |
| --- | --- | --- |
| MIN\_01 | Light Content: mining Template 02 | At BIOA\_MIN01 |
| MIN\_02 | Light Content: mining Template 03 | At BIOA\_MIN02 |

## Disable Intro Videos

To bypass the intro videos and boot the game directly to the start menu, rename these three files in YOUR GAME DIRECTORY\\BioGame\\CookedPC\\Movies:

- BWLogo.bik
- db\_standard.bik
- ME\_EAsig\_720p\_v2\_raw.bik

## Enable joystick move

This tweak may be useful for those who want to use the mouse while having access to analog movement. Comes in useful for Steam controller users or gamepad users who want to bind gyro to a mouse.

In BIOEngine.ini add

```
[WinDrv.WindowsClient]
AllowJoystickInput=True

```

In BIOinput.ini add

```
[BIOC_Base.BioPlayerInput]
Bindings=(Name="XboxTypeS_LeftX",Command="Axis aStrafe Speed=1.0 DeadZone=0.3")
Bindings=(Name="XboxTypeS_LeftY",Command="Axis aBaseY Speed=1.0 DeadZone=0.3")
Bindings=(Name="XboxTypeS_RightX",Command="Axis aTurn Speed=0.2 DeadZone=0.3")
Bindings=(Name="XboxTypeS_RightY",Command="Axis aLookup Speed=0.2 DeadZone=0.3")

```

## Additional resources

Beyond changes to the configuration files, it is recommended to set your graphics card driver and settings to enhance graphic quality and performance. Below, are some recommendations for further readings:

Tweak Guides:

- Guide to Mass Effect configuration
- The TweakGuide Tweaking Companion
- ATI Catalyst Tweak Guide and Nvidia Forceware Tweak Guide
- The Gamer's Graphics \& Display Settings Guide

Support:

- Community Support
- Technical Support
