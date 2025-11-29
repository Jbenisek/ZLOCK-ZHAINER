# TUNNELS OF PRIVACY - Changelog

# Changelog

## v0.2.83 - TTS Natural Speech & UI Polish (2025-11-28)
- **TTS Natural Speech Improvements:**
  - All voices slowed down 10-15% for better comprehension
  - Text preprocessing adds natural pauses after sentences (`. ` → `... `)
  - Pauses added after exclamations, questions, and colons
  - Dramatic words (but, however, suddenly, etc.) get pause before them
  - Personality-based voice adjustments:
    - Aggressive/angry: 10% faster, more expressive
    - Calm/wise: 15% slower, measured tone
    - Nervous/scared: 8% faster, varied rhythm
    - Cunning/sly: 5% slower, expressive
    - Sad/melancholy: 20% slower
    - Excited/energetic: 12% faster

- **UI Improvements:**
  - Hero HP bar tilt now dynamic based on screen position:
    - Left third: -5° tilt
    - Middle third: 0° (flat)
    - Right third: +5° tilt
  - Chat window now opens by default when entering battle
  - Captive NPC canvas labels fixed (name/species/HP bar ordering)

- **Misc:**
  - Added favicon.svg with Zcash Ⓩ symbol

## v0.2.82 - UI Polish & Bribe Gold Deduction (2025-11-28)
- **Gold Bribe System:**
  - Bribing mobs now deducts gold from player's total
  - If player offers more gold than they have, mob sees through the lie and becomes instantly enraged
  - System message shows: "💸 Paid X gold to [Mob]!"

- **Betrayed Mob Visual Feedback:**
  - Betrayed mobs now display with green styling in enemy HUD
  - Green border and glow on card
  - Green portrait border
  - Name shows "🤝 MOB NAME" in green
  - HP bar changes from red to green

- **Captive NPC Improvements:**
  - Captive sprite size increased 25% (200 → 250 base height)
  - Captive name moved up in HUD card to avoid overlap with health bar
  - Captive portrait in HUD increased to 80x80px

## v0.2.81 - Boss Voice Tuning (2025-11-28)
- **Boss Voice Selection:**
  - LLM now prefers male_deep or monster voices for bosses (70% of time)
  - Female voices only for seductive/witch-type bosses
  - Boss fallback voice changed to deep male (bryce)

- **Voice Parameters:**
  - Boss voices: Rougher, more aggressive (faster, higher noise)
  - Male_deep: Commanding tone with higher expression
  - Monster: Very rough, growly with max noise variation
  - Male_mature: Gruff, weathered sound

## v0.2.80 - Gold Economy System (2025-11-28)
- **Summary:**
  - Enemies now drop gold when killed
  - LLM determines gold drops based on enemy backstory
  - Gold displayed in dungeon menu and battle HUD
  - Foundation for future shop/inventory systems

- **Gold Drop System:**
  - LLM assigns `goldDrop` value (5-50 for mobs, 50-500 for bosses)
  - Wealthy enemies drop more, feral beasts drop less
  - Fallback values: 100 gold for bosses, 10 for mobs
  - Chat message shows loot: "💰 Hero looted X gold from Enemy!"

- **Gold Display UI:**
  - Dungeon Menu: Gold shown below level indicator
  - Battle Screen: Gold counter at top center with treasure emoji
  - Both displays update in real-time when gold is earned

- **Technical Changes:**
  - Added `goldDrop` field to LLM prompts (zlock_server.py)
  - `applyGeneratedData()` applies goldDrop to enemy objects
  - `updateGoldDisplay()` function updates all gold UI elements
  - Gold stored in `sharedSave.dungeonState.gold`

## v0.2.79 - Negotiation System: Betrayal & Retreat (2025-11-28)
- **Summary:**
  - Mobs can be bribed to betray the boss and switch sides
  - Bosses can retreat or rage when demoralized
  - Enraged enemies get +10% HP and chance for double attacks
  - Chat interactions now have strategic consequences

- **Mob Betrayal System:**
  - Each mob has a hidden `betrayalThreshold` (50-200 gold)
  - Offer gold in chat: "I'll give you 100 gold to join us"
  - Progress shown: "💰 Name considers your offer... (X% convinced)"
  - When threshold reached, roll d20 vs DC (lower DC = higher offer)
  - Success: Mob switches sides, attacks boss on their turn
  - Low offers (< 10% of threshold) anger mob → rage after 3 attempts
  - Threats also increase anger

- **Boss Morale System:**
  - Bosses have `morale` (0-100) that decreases with:
    - Taking damage (-5)
    - Missing attacks (-3, stacks with consecutive misses)
    - Allies dying (-15)
    - Being insulted in chat (-10)
  - Low morale + low HP triggers crisis roll:
    - Roll 1-10: Boss RETREATS (flees, 50% XP awarded)
    - Roll 16-20: Boss RAGES (enraged, double attack chance)

- **Rage Mechanic:**
  - Triggered by: low morale, failed bribe attempts, threats
  - Effects: +10% max HP restored, +10% damage, red color
  - 30% chance for double attack each turn (d20 >= 15)
  - Stacks: Each rage = another +10% HP

- **Betrayed Mob Behavior:**
  - Turns green (friendly color)
  - On their turn, attacks hostile enemies (prioritizes boss)
  - Shows: "🤝 Name BETRAYS! Attacks Boss for X damage!"

- **Battle Notifications:**
  - "Name switches sides!" - mob betrayal
  - "Name flees in terror!" - boss retreat
  - "Name enters a RAGE!" - rage triggered
  - "⚡ Name's rage fuels a DOUBLE ATTACK!" - double attack
  - Dice roll ticker shows negotiation progress

- **Technical:**
  - `initNegotiationState(enemy)` - initializes tracking
  - `processNegotiation(npc, playerMsg, npcResponse)` - after each chat
  - `updateBossMorale(boss, event)` - on combat events
  - `shouldDoDoubleAttack(enemy)` - 30% chance when enraged
  - Gold parsing regex: `/(\d+)\s*(gold|coins?|gp|money)/i`

## v0.2.78 - TTS AudioChunk Fix (2025-11-28)
- **Bug Fix:**
  - Fixed `'AudioChunk' object has no attribute 'audio_bytes'` error
  - Correct attribute is `audio_int16_bytes` (16-bit PCM audio data)
  - TTS with SynthesisConfig now works correctly

- **Technical:**
  - Piper's `synthesize()` returns `AudioChunk` objects with:
    - `audio_int16_bytes`: Raw 16-bit PCM audio (used for WAV)
    - `audio_int16_array`: NumPy array of samples
    - `audio_float_array`: Float32 audio data
  - Voice parameters (length_scale, noise_scale, noise_w_scale) now applied correctly

## v0.2.77 - Voice Synthesis Parameters (2025-11-28)
- **Summary:**
  - Each voice type now has unique speech parameters for character personality
  - Bosses speak slow and menacing, captives speak fast and nervous
  - Uses Piper's SynthesisConfig for real-time voice tweaking
  - No additional voice files needed - same 17 voices, more variety

- **Synthesis Parameters:**
  - `length_scale`: Speech speed (<1=faster, >1=slower)
  - `noise_scale`: Expressiveness/emotion variation
  - `noise_w_scale`: Phoneme duration (rhythm variation)

- **Voice Personalities:**
  | Voice Type | Speed | Notes |
  |------------|-------|-------|
  | narrator | 1.1x slower | Smooth, measured, clarity |
  | boss | 1.25x slower | Menacing, dramatic pauses |
  | monster | 1.4x slower | Very slow, growly, rough |
  | captive | 0.85x faster | Nervous, shaky, desperate |
  | ethereal | 1.3x slower | Dreamy, smooth, otherworldly |
  | nate | 0.9x faster | Quick, energetic |
  | cyberaxe | 1.05x slower | Steady, deliberate |

- **Technical:**
  - `VOICE_PARAMS` dict maps voice types to synthesis parameters
  - Uses `SynthesisConfig` from `piper.config`
  - Parameters applied per-generation, not per-model
  - Same voice model can sound different based on params

## v0.2.76 - Voice Pools & Action Stripping (2025-11-28)
- **Summary:**
  - Expanded to 17 unique voices with randomized pools per voice type
  - Asterisk actions (*laughs menacingly*) now stripped from TTS - not read literally
  - Each voice type has 3-4 variants for variety

- **17 Voices Available:**
  - British: alba, jenny_dioco, cori, alan, northern_english_male, aru
  - American: amy, kristin, hfc_female, ljspeech, joe, ryan, bryce, hfc_male, norman, lessac, kusal

- **Voice Pools (randomized selection):**
  - `female_mature`: alba, jenny_dioco, hfc_female
  - `female_young`: kristin, amy, cori, ljspeech
  - `male_deep`: bryce, northern_english_male, norman
  - `male_young`: ryan, aru, kusal
  - `male_mature`: joe, alan, kusal
  - `monster`: hfc_male, northern_english_male, norman
  - `ethereal`: lessac, ljspeech, alba

- **Action Stripping:**
  - Server now strips `*action*` text before TTS
  - "Hello there *laughs menacingly*" → TTS only says "Hello there"
  - Prevents awkward literal reading of roleplay actions
  - Uses regex: `re.sub(r'\*[^*]+\*', '', text)`

- **Fixed Voices (heroes/narrator):**
  - Heroes keep consistent voices for recognizability
  - Narrator always uses British alba (sexy sophisticated)

## v0.2.75 - LLM-Driven Voice Type Selection (2025-01-29)
- **Summary:**
  - LLM now intelligently assigns voiceType when generating entity responses
  - Voices selected based on entity gender, age, and species (male/female/monster)
  - Enhanced prompts guide LLM to pick appropriate voice for each entity

- **Voice Type Options for LLM:**
  - `male_deep`: Deep authoritative male voice (CyberAxe-like)
  - `male_young`: Youthful energetic male voice (Nate-like)
  - `male_mature`: Seasoned experienced male voice (Zooko-like)
  - `female_mature`: Confident mature female voice (Zancas-like)
  - `female_young`: Youthful female voice (Captive-like)
  - `monster`: Menacing creature voice (Boss/mob)
  - `ethereal`: Mysterious otherworldly voice (NPCs)

- **Technical Implementation:**
  - `voiceType` field added to entity chat response JSON
  - LLM picks voice based on entity's `gender` and `species` fields
  - Voice flows through: generateEntityResponse → addChatMessage → playTTS
  - Server maps voiceType to specific Piper voice model

- **JSON Generation Improvements:**
  - Retry logic (3 attempts) for failed JSON parsing
  - Trailing comma removal before parsing
  - Better JSON extraction from LLM responses

## v0.2.74 - Piper TTS Voice System (2025-01-28)
- **Summary:**
  - Added local neural text-to-speech for NPC/entity chat responses
  - Uses Piper TTS (fast, local, no API needed)
  - Self-contained: auto-installs piper-tts and downloads voice models
  - Voice toggle in chat window (default ON)

- **Server (zlock_server.py):**
  - `ensure_piper_installed()`: Auto-installs piper-tts via pip if missing
  - `ensure_voice_models()`: Downloads voice models from HuggingFace on first run
  - `/api/tts` endpoint: Accepts text + voiceType, returns audio/wav
  - `/api/tts-status` endpoint: Returns TTS availability
  - Voice models stored in `piper_voices/` directory

- **Voice Assignments:**
  - Narrator: British female (en_GB-alba-medium) - "sexy sophisticated"
  - Zooko: American male mature (en_US-joe-medium)
  - Nate: American male young (en_US-ryan-medium)
  - Zancas: American female (en_US-kristin-medium)
  - CyberAxe: American male deep (en_US-bryce-medium)
  - Boss: British male menacing (en_GB-northern_english_male-medium)
  - Mob: American generic male (en_US-hfc_male-medium)
  - Captive: American female desperate (en_US-amy-medium)
  - NPC: American neutral (en_US-lessac-medium)

- **Client (tunnels_of_privacy.html):**
  - TTS toggle checkbox in chat header (🔊 icon)
  - `checkTTSAvailability()`: Checks server for TTS support on load
  - `playTTS()`: Queues audio generation and playback
  - `getTTSVoiceType()`: Maps entity type/name to voice
  - Audio queue system for sequential playback
  - Skips action-only messages like "*silence*" or "*growls*"

- **One-Click Setup:**
  - Running `python zlock_server.py` automatically:
    1. Checks if piper-tts installed → installs if missing
    2. Checks if voice models exist → downloads from HuggingFace
  - Total ~100MB download for all voices on first run

## v0.2.73 - Ground-Plane Hero Nameplates (2025-11-28)
- **Summary:**
  - Hero names and HP bars now render at their feet on the "ground"
  - Perspective transform makes them look like they're lying on the floor
  - Similar to Splinter Cell / Diablo style ground nameplates

- **Visual Effect:**
  - Nameplates positioned below hero sprites (at feet)
  - Vertically squished to 35% (simulates ~70° viewing angle)
  - Shadow ellipse under nameplate for grounding effect
  - Larger text (16px name, 14px HP) to compensate for squish

- **Technical:**
  - Uses `ctx.scale(1, 0.35)` for perspective foreshortening
  - `ctx.save()`/`ctx.restore()` to isolate transform
  - HP bar has border for better visibility when squished
  - Ground shadow adds depth

## v0.2.72 - Boss Type Readability (2025-11-28)
- **Summary:**
  - Boss type text changed from purple to gray (same as mobs)
  - Boss type is now BOLD to distinguish from mobs
  - Improved readability

- **Display:**
  - Mobs: gray type, normal weight
  - Bosses: gray type, **bold** weight

## v0.2.71 - Always Show Entity Type (2025-11-28)
- **Summary:**
  - Mobs now ALWAYS show their species/type (gray text)
  - Bosses now ALWAYS show their species/type (purple text)
  - Fixed Floating Orb and other mobs missing type label

- **Display Fix:**
  - Removed "hide if same as name" logic
  - All enemies now show: Name → Type → HP bar
  - Mobs: type in gray (#AAAAAA)
  - Bosses: type in purple (#8B45FF)

## v0.2.70 - Boss Name & Type Display Fix (2025-11-28)
- **Summary:**
  - Bosses now always show their species/type label (in purple)
  - Improved LLM prompt to generate truly unique boss names
  - Fixed "Floating Orb" showing no type issue

- **Display Fix:**
  - Bosses always show species type below name (purple text)
  - Example: "LORD MALACHAR" + "Floating Orb" (type in purple)
  - Mobs still only show species if different from name

- **LLM Prompt Improvement:**
  - Explicitly forbids using template name in generated name
  - Examples: "Zyx'tharion" or "Lord Malachar" instead of "Floating Orb"
  - Should generate more unique/creative boss names

## v0.2.69 - Entity Label Positioning Fixes (2025-11-28)
- **Summary:**
  - Fixed overlapping labels on mobs, bosses, and heroes
  - Tightened spacing between name, species, and HP bar
  - Bosses now show species type like mobs

- **Positioning Fixes:**
  - **Mobs**: Fixed name/species overlapping HP bar - now stacked correctly
  - **Bosses**: Added species property, tightened label spacing
  - **Heroes**: Moved name closer to HP bar (was 2 lines too high)

- **Label Layout (top to bottom):**
  - Name (bold, entity color)
  - Species/Type (smaller, gray for mobs, purple "Boss" for bosses)
  - HP Bar (with numbers inside)

- **Technical:**
  - Labels now build upward from HP bar position
  - Species offset: 5px above bar
  - Name offset: 12px above species
  - Bosses get `species` property like mobs

## v0.2.68 - Chat & Entity System Consolidation (2025-11-28)
- **Summary:**
  - Consolidated chat targeting, typewriter effects, and entity naming systems
  - All battlefield entities now fully interactive with unique identities
  - Stable release of LLM-powered NPC interaction system

- **Chat System Features:**
  - Typewriter effect on NPC responses (variable speed based on punctuation)
  - Entity target selector with buttons for all creatures in room
  - Direct targeting: Click any entity to address them specifically
  - Broadcast mode: Speak to everyone, first available NPC responds
  - Rate limit detection with auto-switch to available models

- **Entity Identity System:**
  - All mobs get unique LLM-generated names and backstories
  - Entity labels: Name → Species → HP bar (with numbers inside)
  - Captive NPCs with rescue mechanics and dialogue
  - Character cards on left panel for all entities

- **Chat Logic:**
  - Direct target: Selected entity always responds
  - Broadcast: Priority order is Captive → First enemy with backstory
  - All LLM-generated mobs can chat (unique personalities)
  - Fallback message if no one can respond

## v0.2.67 - Entity Names, Species & HP Bar Redesign (2025-11-28)
- **Summary:**
  - All mobs now get unique LLM-generated names and backstories
  - Entity labels now show: Name, Species/Type, HP bar
  - HP numbers moved INSIDE the health bar for cleaner UI

- **Mob Names & Backstories:**
  - ALL mobs now get LLM-generated unique names (100% instead of 50%)
  - Mobs store original type as `species` property
  - Example: "Grimfang" (Cave Spider) instead of just "Cave Spider"
  - Each mob gets unique personality and backstory for chat

- **Entity Label Layout:**
  - **Name** (top, bold, larger) - Unique name for entity
  - **Species** (below name, smaller, gray) - What type of creature
  - **HP Bar** (bottom) - With numbers centered inside

- **HP Bar Redesign:**
  - Taller bars (14px instead of 10px) to fit text
  - HP numbers centered INSIDE the bar
  - Darker background (0.7 opacity) for better contrast
  - Consistent style across heroes, enemies, and captives

- **Visual Examples:**
  - Heroes: "ZOOKO" + green HP bar with "30/30"
  - Enemies: "GRIMFANG" + "Cave Spider" + red HP bar with "15/15"
  - Captives: "ELARA" + "⛓️ Human" + green HP bar

## v0.2.66 - Chat Target Selector (2025-11-28)
- **Summary:**
  - Added entity target buttons above chat input
  - Click any boss, mob, or captive to address them directly
  - "📢 ALL" broadcast button for speaking to everyone

- **Chat Target Selector:**
  - Appears above chat input in battle chat window
  - "📢 ALL" button - broadcast mode (default), any NPC can reply
  - "⚔️ [Name]" buttons - red/purple for enemies (hostile/boss)
  - "⛓️ [Name]" button - gold for captives (friendly)
  - Selected target highlighted with color fill
  - Names truncated to 10 chars with ellipsis
  - Scrollable area supports 5-20+ entities

- **Visual Styling:**
  - Compact buttons (10px font, 3px-8px padding)
  - Color-coded borders: red (hostile), purple (boss), gold (friendly), green (broadcast)
  - Active state fills button with matching color
  - Max height 80px with overflow scroll

- **Technical:**
  - `chatState.targetEntity` stores current target { type, index, name, entity }
  - `selectChatTarget()` updates UI and input placeholder
  - `updateChatTargets()` rebuilds buttons from current battle state
  - Auto-updates when entities die or chat opens
  - Falls back to broadcast if target becomes invalid

## v0.2.65 - Typewriter Chat Effect (2025-11-28)
- **Summary:**
  - NPC chat responses now type out character by character
  - Creates more natural, immersive conversation flow
  - Variable typing speed based on punctuation

- **Typewriter Effect:**
  - Base speed: 25ms per character
  - Faster for spaces (15ms)
  - Slower for periods, exclamations, questions (150ms)
  - Slower for commas, semicolons, colons (80ms)
  - Blinking cursor during typing (Discord purple #5865F2)
  - Cursor removed when message complete

- **Technical Changes:**
  - New `typewriterEffect()` function with recursive character reveal
  - Messages track `displayText` separate from full `text`
  - `data-msg-id` attribute on message elements for DOM targeting
  - Multiplayer: Clients receive full text instantly (no double-typing)

## v0.2.64 - Captive Character Card & Sprite Size Fix (2025-01-29)
- **Summary:**
  - Added captive character card to left-side battle UI (gold/friendly styling)
  - Increased captive sprite size from 100px to 200px base height
  - Captives now visually match other combatants in both card and sprite display

- **Captive Character Card:**
  - Gold border with glow effect (#F2C94C color scheme)
  - Portrait showing captive sprite image
  - Name with chain emoji (⛓️)
  - HP and AC stats displayed
  - "CAPTIVE" label at bottom
  - Appears after enemy cards in left panel

- **Captive Sprite Size Fix:**
  - Increased base height from 100px to 200px
  - Now properly visible alongside mobs and heroes
  - Maintains aspect ratio from sprite image
  - Depth scaling preserved for battlefield perspective

- **CSS Additions:**
  - `.battleEnemyCard.captive` - Gold border with glow
  - `.battleEnemyCard.captive .battleEnemyPortrait` - Gold portrait border
  - `.battleEnemyCard.captive .battleEnemyName` - Gold name text

## v0.2.63 - Captive NPC Visuals & Chat Model Improvements (2025-11-28)
- **Summary:**
  - Captive NPCs now render as proper battlefield entities with fallback circles
  - Captives positioned on far left of battlefield, below heroes
  - Default chat model changed to free model 2 (Groq Llama 3.1 8B)
  - Rate-limited models now show red ✕ overlay and auto-switch to available models
  - Fixed model selector button highlighting bug
  - Full multiplayer sync for captive NPCs

- **Captive NPC Visual System:**
  - Captives render like mobs with depth scaling
  - Gold fallback circle with chain icon (⛓️) when no sprite
  - Name displayed above with "⛓️ CAPTIVE" label
  - Positioned at (10%, 80%) - far left, lower area
  - Can be chatted with (priority over enemies)
  - Full sprite support ready (tunnelsofprivacy/mobs/captive.png)

- **Chat Model Selector Fixes:**
  - Default model changed from 1 (paid) to 2 (free)
  - Fixed button highlighting bug - was using index instead of model ID
  - Added `exhaustedModels` tracking array
  - CSS for exhausted buttons: 50% opacity + red ✕ overlay
  - Can't select exhausted models
  - Auto-switches to next free model when current exhausted

- **Rate Limit Detection:**
  - Detects: rate, limit, quota, 429, exceeded in error messages
  - `markModelExhausted()` function marks and visually updates buttons
  - System chat message notifies player of rate limit
  - Tooltip updated to show "(RATE LIMITED)" suffix

- **Multiplayer Sync:**
  - `sendBattleInitToClients()` includes full captive data
  - `initializeBattleFromHost()` recreates captive with all properties
  - Captive position normalized/denormalized for different screen sizes
  - Properties synced: name, backstory, rescueReward, dialogueOnRescue, position, sprite

## v0.2.62 - API Key Management & Graceful LLM Degradation (2025-11-28)
- **Summary:**
  - Removed hardcoded API keys from server for security
  - Server prompts for API keys on first startup
  - Keys saved to `.zlock_api_keys.json` for persistent storage
  - LLM features gracefully disable when no keys provided
  - Added `/api/llm-status` endpoint for client to check LLM availability
  - Added `.gitignore` to prevent committing API keys

- **API Key Management:**
  - `init_api_keys()` function runs on server startup
  - `load_api_keys()` loads from config file if exists
  - `prompt_for_api_keys()` prompts user for Groq/OpenRouter keys
  - `save_api_keys()` persists keys to `.zlock_api_keys.json`
  - Keys only requested once, then loaded from file on future restarts

- **Graceful LLM Degradation:**
  - `LLM_ENABLED` global flag controls LLM availability
  - Chat API returns fallback "*stares silently*" response when disabled
  - Generate encounter API returns default data when disabled
  - Server startup shows clear LLM status (ENABLED/DISABLED)

- **Security:**
  - No API keys hardcoded in source code
  - Config file excluded via `.gitignore`
  - Keys stored locally, never transmitted or logged fully

## v0.2.61 - Dungeon Master LLM & Dynamic Encounters (2025-11-28)
- **Summary:**
  - Added Dungeon Master LLM system that generates unique boss names, backstories, and stats each battle
  - Bosses and mobs now have procedurally generated names and personalities via AI
  - Added captive NPC system - rescue prisoners for gold, items, and secret info
  - Added NPC Free Will Chat - enemies comment on battle events autonomously
  - Added settings for LLM Free Will and Free/Paid model preference
  - Model selector now shows Free vs Paid labels with visual distinction

- **Dungeon Master LLM System:**
  - New `/api/generate-encounter` endpoint on server
  - Generates unique boss names, backstories, personalities for each battle
  - Stat modifiers (HP, damage, AC) applied based on LLM suggestions
  - Negotiation data generated: bribe amounts, anger triggers, friendship paths
  - Uses fast Groq models for generation (Llama 3.1 8B by default)

- **Dynamic Boss Generation:**
  - Bosses get unique names instead of generic types (e.g. "Metadata Swarm Mass")
  - Rich backstories generated fitting the Tunnels of Privacy lore
  - Opening lines generated for battle start dialogue
  - Mobs have 50% chance to get unique names/personalities

- **Captive NPC System:**
  - 50% chance per room to have a captive NPC
  - Captive rescued automatically when room is cleared
  - Rewards include: gold (10-100), items, secret information
  - Captive dialogue shown in chat on rescue
  - Info rewards revealed as whispered secrets

- **NPC Free Will Chat:**
  - `triggerFreeWillChat()` function for autonomous NPC dialogue
  - Triggers on: battle_start, took_damage, dealt_damage, low_health, ally_died
  - 10-second cooldown prevents spam
  - Controlled by "NPC Free Will Chat" setting in Settings panel
  - Opening lines displayed immediately if generated

- **Settings Panel Updates:**
  - Added "NPC Free Will Chat" toggle - controls autonomous NPC dialogue
  - Added "Use Paid LLM Models" toggle - switches between free/paid APIs
  - AI Settings section with visual separation

- **Model Selector UI:**
  - Free models (2, 4, 5) shown first with "Free:" label
  - Paid models (1, 3, 6-10) shown second with "Paid:" label and orange border
  - Tooltips show model name and provider on hover
  - Groq models 2, 4, 5 are truly free (no cost)

- **Server Updates (zlock_server.py):**
  - New `handle_generate_encounter()` method
  - World lore context for consistent generation
  - JSON parsing with markdown cleanup
  - Supports boss, mob, captive, and generic NPC generation

## v0.2.60 - Multiplayer NPC Chat Sync & Hybrid LLM Providers (2025-11-28)
- **Summary:**
  - NPC chat now fully synced in multiplayer - clients can chat with NPCs via host
  - Added hybrid Groq + OpenRouter provider system for model testing
  - Fixed IPv6 timeout issue causing 40+ second delays on all API calls
  - Animations broadcast to clients (infrastructure added, visual sync WIP)

- **Multiplayer Chat Sync:**
  - Clients can now send chat messages - forwarded to host for LLM processing
  - Host broadcasts all chat messages (player and NPC) to all clients
  - Enemy backstory and isBoss now synced to clients for proper NPC context
  - Fixed duplicate message echo - clients filter out their own messages from broadcast
  - Added `chat_request` and `chat_message` WebSocket message types

- **Hybrid LLM Provider System:**
  - Model 1: OpenRouter (Mistral Nemo) for comparison
  - Models 2-5: Groq (instant inference) - Llama 3.1 8B, Llama 3.3 70B, Gemma 2 9B, Mixtral 8x7B
  - Models 6-10: OpenRouter (variety) - Llama 3.1 8B, Gemma 2 9B, Qwen 2.5 7B, Ministral 3B, L3 Lunaris 8B
  - Server dynamically selects API endpoint based on provider

- **IPv4-Only Fix:**
  - Patched Python's `socket.getaddrinfo` to force IPv4 only
  - Fixed 20+ second TCP connect timeouts caused by IPv6 fallback
  - All API calls now instant (was 40+ seconds due to dual IPv6 timeout)

- **Animation Sync Infrastructure:**
  - `setAnimationState()` now broadcasts `animation_sync` messages to clients
  - Clients receive animation updates and apply locally
  - Server relays `animation_sync` from host to all clients
  - (Note: Visual sync not yet working - will fix in next version)

- **Server Updates (zlock_server.py):**
  - Added `GROQ_API_KEY` for Groq API access
  - `MODEL_OPTIONS` now uses `(provider, model)` tuples
  - Dynamic URL/header selection based on provider ('groq' or 'openrouter')
  - Added WebSocket handlers for `animation_sync`, `chat_message`, `chat_request`

## v0.2.59 - LLM Model Selector & Cost Tracking (2025-11-28)
- **Summary:**
  - Added 10-model selector buttons to chat window for A/B testing different LLMs
  - Added real-time cost and token tracking display
  - Added response time timer showing seconds per request
  - Moved chat window to bottom-right corner and made it 2x taller

- **Model Selector:**
  - 10 numbered buttons (1-10) to switch between LLM models instantly
  - Active model highlighted with blue background
  - Models include: Gemma 3 4B, Qwen 2.5 Coder 7B, L3 Lunaris 8B, Llama 3.1 8B, Gemma 2 9B, Mistral Nemo, Gemma 3n E4B, Ministral 3B, Mistral Small 24B, IBM Granite 4.0 Micro

- **Cost Tracking:**
  - Running tally of total cost displayed next to model buttons
  - Shows format: `$0.000123 | 456 tok`
  - Costs per million tokens configured for each model (input/output)
  - Server returns `usage` data with prompt and completion tokens

- **Response Timer:**
  - Live timer updates every 0.1s while waiting for LLM response
  - Shows `Model X - 2.5s...` while waiting
  - Shows `Model X: 4.23s` after response received
  - Helps compare model latency for A/B testing

- **Chat Window Improvements:**
  - Moved to bottom-right corner (`bottom: 10px`)
  - Increased height from 350px to 600px (2x taller)
  - Increased width from 320px to 350px
  - Fixed text overflow with `white-space: pre-wrap`

- **Server Updates (zlock_server.py):**
  - `MODEL_OPTIONS` dict maps button numbers to model IDs
  - `MODEL_COSTS` dict stores (input, output) costs per million tokens
  - API response includes `usage` object with `promptTokens`, `completionTokens`, `cost`
  - Accepts `modelId` parameter in POST request to select model

## v0.2.58 - Chat Text Formatting Fix (2025-11-28)
- **Summary:**
  - Fixed text formatting in chat window - asterisks now display as italics instead of strikethrough
  - Changed LLM model to `mistralai/mistral-7b-instruct:free` for reliable system prompt support

- **Chat Text Formatting:**
  - Added `formatChatText()` function to properly handle roleplay notation
  - Converts `*text*` to `<em>text</em>` for proper italics display
  - Escapes HTML special characters to prevent XSS and rendering issues
  - Example: `*whispers*` now displays as *whispers* (italic) not ~~whispers~~ (strikethrough)

- **LLM Model Change:**
  - Changed from `google/gemma-3n-e4b-it:free` to `mistralai/mistral-7b-instruct:free`
  - Previous model returned 400 error ("Developer instruction is not enabled")
  - Mistral 7B Instruct properly supports system prompts for NPC persona

## v0.2.57 - NPC Chat System with LLM Integration (2025-11-28)
- **Summary:**
  - Added Discord-style chat window for talking to NPCs, mobs, and bosses
  - Integrated OpenRouter LLM API for dynamic NPC conversations
  - Full multiplayer support - all players see chat in real-time

- **Chat Window:**
  - Bottom-right corner of battle screen
  - Toggled via TALK button (can use anytime, no turn cost)
  - Discord-style layout: headshot + colored name + message
  - Color codes: Red (hostile), Yellow (questable), Green (friendly), White (player)
  - Newest messages at top, oldest at bottom
  - Text input with Enter key or Send button

- **LLM Integration:**
  - Server-side `/api/chat` endpoint in `zlock_server.py`
  - Uses OpenRouter API with `meta-llama/llama-3.1-8b-instruct:free` model
  - NPCs stay in character based on their backstory
  - Conversation context maintained within battle
  - Short, dramatic responses (1-3 sentences)

- **Multiplayer Support:**
  - Host-authoritative: only host calls LLM API
  - Clients send chat requests to host via WebSocket
  - Host broadcasts all messages to all clients
  - No complex syncing - simple message broadcast

- **NPC Backstories:**
  - Added `backstory` field to mobs/bosses JSON data
  - NPCs with backstory can chat, others stay silent
  - Example: Metadata Swarm Mass, Open Ledger Golem, Cave Dweller

- **Technical Details:**
  - `chatState` object tracks messages and visibility
  - `addChatMessage()` adds message and broadcasts to clients
  - `sendChatMessage()` handles player input and LLM calls
  - `clearBattleChat()` called when battle ends
  - Chat window clears per-battle

## v0.2.56 - Complete Hero Animation Sets & New Animation Triggers (2025-11-28)
- **Summary:**
  - Added complete animation sets for Zancas and Nate
  - Added heal, taunt, and myturn animation triggers
  - All 4 heroes now have full animation support

- **Zancas Complete Animation Set:**
  - Idle variants: `zancas_idle.png`, `zancas_idle_a.png`, `zancas_idle_b.png`
  - Attacks: `zancas_light_attack.png`, `zancas_heavy_attack.png`, `zancas_special_attack.png`
  - Hit: `zancas_hit.png` - plays once, returns to idle
  - Knockout: `zancas_knockout.png` - plays once, holds last frame
  - Defend: `zancas_def.png` - pingpong while defending
  - Heal: `zancas_heal.png` - plays once, returns to idle

- **Nate Complete Animation Set:**
  - Idle variants: `nate_idle.png`, `nate_idle_a.png`, `nate_idle_b.png`, `nate_idle_c.png` (4 variants!)
  - Attacks: `nate_light_attack.png`, `nate_heavy_attack.png`
  - Special Attack variants: `nate_special_attack.png`, `nate_special_attack_a.png` (random selection)
  - Hit: `nate_hit.png` - plays once, returns to idle
  - Knockout: `nate_knockout.png` - plays once, holds last frame
  - Defend: `nate_def.png` - pingpong while defending
  - Heal: `nate_heal.png` - plays once, returns to idle
  - Taunt: `nate_taunt.png` - plays once on taunt action, returns to idle
  - MyTurn: `nate_myturn.png` - plays once when Nate's turn starts, returns to idle

- **New Animation Triggers:**
  - **Heal Animation:** Triggered in heal action, plays once then returns to idle
  - **Taunt Animation:** Triggered in taunt action, plays once then returns to idle
  - **MyTurn Animation:** Triggered in `updateBattleTurnInfo()` when hero's turn starts
  - All triggers check if hero has the animation state before playing

- **Technical Details:**
  - `HERO_ANIM_PATHS` now supports array format for special_attack variants (Nate)
  - 14 new sprite sheets for Nate, 11 new sprite sheets for Zancas
  - All sprite sheets added to preload list for instant playback
  - MyTurn only triggers for heroes with hp > 0

## v0.2.55 - Defend Animation & Zooko Full Animation Set (2025-11-28)
- **Summary:**
  - Added defend animation system for heroes
  - Added complete animation set for Zooko (idle variants, attacks, hit, knockout, defend)

- **Defend Animation System:**
  - `cyberaxe_def.png`, `zooko_def.png` - Defense stance animations
  - Triggered when hero selects Defend action
  - Uses 'pingpong' mode - loops forward/backward while defending
  - Resets to idle when:
    - Hero is hit while defending (hit animation plays first)
    - Hero's turn comes again (when taking any new action)
  - Added `defend` state to `HERO_ANIM_PATHS` for both heroes

- **Zooko Complete Animation Set:**
  - Idle variants: `zooko_idle.png`, `zooko_idle_a.png`, `zooko_idle_b.png`
  - Attacks: `zooko_light_attack.png`, `zooko_heavy_attack.png`, `zooko_special_attack.png`
  - Hit: `zooko_hit.png` - plays once, returns to idle
  - Knockout: `zooko_knockout.png` - plays once, holds last frame
  - Defend: `zooko_def.png` - pingpong while defending

- **Technical Details:**
  - Defense reset in `handleBattleAction()` when `currentCombatant.defending` is true
  - Animation triggered via `setAnimationState(combatant, 'defend', 'pingpong')`
  - All new sprite sheets added to preload list
  - Both Zooko and CyberAxe now have matching animation states

## v0.2.54 - Knockout Animation (2025-11-27)
- **Summary:**
  - Added knockout animation for heroes when HP reaches 0
  - Animation plays once and holds on final frame

- **Knockout System:**
  - `cyberaxe_knockout.png` - CyberAxe knockout animation
  - Triggered when hero HP drops to 0 from enemy attack
  - Uses 'once' play mode - plays all 81 frames then stops
  - Holds on last frame (frame 80) indefinitely
  - Added to preload list for instant playback

- **Technical Details:**
  - Added `knockout` state to `HERO_ANIM_PATHS.cyberaxe`
  - Knockout triggered in AI attack damage check
  - 'once' mode sets `anim.playing = false` at end
  - Frame stays at `ANIM_TOTAL_FRAMES - 1` after completion

## v0.2.53 - Idle Variants & Sprite Preloading (2025-11-27)
- **Summary:**
  - Added multiple idle animation variants with random cycling
  - All sprite sheets now preload during loading screen
  - Instant variant switching via cached sprite sheets

- **Idle Variants System:**
  - States can be single path (string) or array of variants
  - CyberAxe has 3 idle variants: `idle.png`, `idle_a.png`, `idle_b.png`
  - On ping-pong cycle complete, picks different variant
  - `pickNextIdleVariant()` - Selects random different idle on cycle end
  - Filters current path to guarantee different animation each cycle

- **Preloading Integration:**
  - All hero sprite sheets added to `preloadAssets()` image list
  - Sprite sheets cached in `spriteSheetCache` during preload
  - Instant swap when switching variants (no async loading delay)
  - Loading screen shows accurate progress including sprite sheets

- **Preloaded Assets:**
  - `zooko_idle.png`, `nate_idle.png`, `zancas_idle.png`
  - `cyberaxe_idle.png`, `cyberaxe_idle_a.png`, `cyberaxe_idle_b.png`
  - `cyberaxe_light_attack.png`, `cyberaxe_heavy_attack.png`, `cyberaxe_special_attack.png`

- **Technical Details:**
  - `HERO_ANIM_PATHS` supports array format for variants
  - Preloader populates `spriteSheetCache` on image load
  - `pickNextIdleVariant()` checks cache before async load
  - Frame resets to 0 on variant switch for clean transition

## v0.2.52 - Sprite Sheet Animation System (2025-11-27)
- **Summary:**
  - Added complete sprite sheet animation system for battle sprites
  - Heroes now use animated 9x9 atlas sprite sheets (81 frames at 16fps)
  - Ping-pong, loop, and once play modes supported
  - Attack animations delay damage logic to sync with visuals

- **Animation System:**
  - `HERO_ANIM_PATHS` - Maps hero names to animation state paths
  - `spriteSheetCache` - Caches loaded sprite sheets for performance
  - `loadSpriteSheet()` - Lazy loads sprite sheets with caching
  - `initAnimation()` - Creates animation controller for any combatant
  - `updateAnimation()` - Advances frames at 16fps with configurable play modes
  - `drawAnimatedSprite()` - Draws correct frame from 9x9 grid atlas
  - `setAnimationState()` - Transitions between animation states with callbacks

- **Play Modes:**
  - `pingpong` - Plays forward then reverse (default for idle)
  - `loop` - Plays forward and restarts from frame 0
  - `once` - Plays forward once then stops (for attacks)

- **Hero Idle Animations:**
  - `tunnelsofprivacy/heros/zooko_idle.png`
  - `tunnelsofprivacy/heros/nate_idle.png`
  - `tunnelsofprivacy/heros/zancas_idle.png`
  - `tunnelsofprivacy/heros/cyberaxe_idle.png`

- **CyberAxe Attack Animations:**
  - `cyberaxe_light_attack.png` - Light attack animation
  - `cyberaxe_heavy_attack.png` - Heavy attack animation
  - `cyberaxe_special_attack.png` - Special attack animation
  - Attack animations play once, then return to idle
  - 2-second delay before damage logic executes (syncs with animation)

- **Technical Details:**
  - 9x9 grid atlas format (81 total frames)
  - Auto-detects frame size from `sheet.width / 9`
  - Frame calculation: `col = frame % 9`, `row = floor(frame / 9)`
  - Uses `ctx.drawImage()` with source rectangle clipping
  - Falls back to static sprite if animation not loaded
  - `executeAttack()` split into animation trigger + delayed `executeAttackLogic()`

- **Files Modified:**
  - `tunnels_of_privacy.html` - Added animation system (~170 lines)

## v0.2.51 - Server Script Multiplayer Dependencies (2025-11-27)
- **Summary:**
  - Bash script now auto-installs pip3 and websockets module
  - WebSocket port 8765 now opened in firewall automatically
  - Zero manual dependency setup required for multiplayer

- **Dependency Installation:**
  - Script checks for `pip3` command, installs `python3-pip` if missing
  - Script checks for `websockets` module, installs via `pip3` if missing
  - Uses `sudo apt-get` for pip3 installation
  - Uses `sudo pip3 install` for websockets module

- **Firewall Configuration:**
  - Port 4243 (HTTP) opened in firewall
  - Port 8765 (WebSocket) opened in firewall
  - Both ports configured automatically on script start

- **Files Modified:**
  - `zlock_server.sh` - Added dependency checks and WebSocket port opening

## v0.2.50 - Host Hero Control Transfer (2025-11-27)
- **Summary:**
  - Modified hero control transfer when client disconnects
  - Host now receives control of disconnected player's heroes
  - UI buttons refresh after hero transfer

- **Changes:**
  - `handlePlayerDisconnect()` now uses `connectedPlayers[].heroes` array
  - Heroes added to host's `myHeroes` array on client disconnect
  - Added `updateHeroTurn()` call to refresh button states
  - Removed unused `multiplayerState.playerHeroes` object reference

## v0.2.49 - Reconnection System (2025-11-27)
- **Summary:**
  - Fixed client reconnection after disconnect
  - Added REJOIN GAME button for reconnecting clients
  - Server now relays reconnection messages
  - Clients can rejoin active battles or dungeon menu

- **Reconnection Flow:**
  - Client disconnects and reconnects to same room code
  - Server detects reconnection and sends `reconnected: true`
  - Client sees "REJOIN GAME" button instead of normal start options
  - Client selects their heroes and clicks REJOIN GAME
  - Host receives `request_sync` and sends current game state
  - Client receives `sync_state` with save data and current screen
  - If battle is active, host also sends `battle_init` to fully sync client

- **Technical Implementation:**
  - Added `multiplayerState.isReconnecting` flag
  - New message types: `request_sync` and `sync_state`
  - Server handlers in `zlock_server.py` for new message types
  - `rejoinGame()` function sends sync request to host
  - Host checks `currentScreen` and sends appropriate data
  - Battle reconnection includes both state sync and battle initialization
  - Client properly hides hero selection modal after rejoin

- **Server Changes:**
  - Added `request_sync` handler: forwards client request to host
  - Added `sync_state` handler: broadcasts host response to clients
  - Both handlers with console logging for debugging

- **Bug Fixes:**
  - Fixed music controls not centering after game_start for clients
  - Added fallback screen handling in sync_state receiver
  - Removed premature screen hiding in rejoinGame() function
  - Added default case in message handler to catch unhandled types

## v0.2.48 - Multiplayer & UI Fixes (2025-11-27)
- **Summary:**
  - Fixed critical multiplayer bug where client hero stats showed as 0 in dungeon menu
  - Fixed music controls positioning issues across all screen transitions
  - Character sheet borders now match hero theme colors
  - Dice ticker text improvements

- **Multiplayer Fixes:**
  - Client now properly receives hero stats when starting new adventure
  - `heroStatsCache` populated from host's `saveData` on game start
  - Clients display correct HP, maxHP, XP, level, and all ability scores
  - Fixed missing stats in dungeon menu after hero selection

- **Music Controls Positioning:**
  - Added `dungeonMenuActive` class to ALL transitions to dungeon menu
  - Fixed: After battle ends (host and client)
  - Fixed: Continue game multiplayer
  - Fixed: Start new adventure
  - Fixed: Client joining game
  - Music controls now consistently centered on dungeon menu

- **Visual Improvements:**
  - Character cards now have theme-colored borders:
    - Zooko: Yellow (#F2C94C)
    - Nate: Red (#E74C3C)
    - Zancas: Green (#27AE60)
    - CyberAxe: Blue (#2E86DE)
  - Each card has subtle glow matching character color

- **Dice Display:**
  - Changed "Zcash Community" to "Zcash" in ticker message
  - Reduced font size from 18px to 14px to prevent text wrapping during combat
  - Ticker now reads: "Created by CyberAxe for Zcash..."

- **Music System:**
  - Fixed event listener attachment timing for song transitions
  - `ended` event now attached after `play()` promise resolves
  - Prevents music from stopping after first track

- **Technical Details:**
  - Client `game_start` handler now populates `heroStatsCache` with: hp, maxHp, xp, level, str, dex, con, int, wis, cha
  - All 8 dungeon menu transitions now properly manage music control classes
  - Character card styles use ID selectors: `#battleCardZooko`, `#battleCardNate`, etc.

## v0.2.47 - Main Theme Priority Music System (2025-11-26)
- **Summary:**
  - Main theme always plays first on game load
  - Random rotation of other tracks after main theme completes

- **Music Playback Changes:**
  - Added `main_theme.webm` as first track in rotation
  - Track name: "Tunnels of Privacy Theme"
  - Always plays on "CLICK TO ENTER" after preload
  - Added `mainThemePlayed` flag to track first play

- **Random Rotation:**
  - After main theme ends: randomly picks from 10 other tracks
  - Skip buttons (⏮ Previous / ⏭ Next): pick random tracks (excluding main theme)
  - Play/Pause button (when no music loaded): starts with main theme
  - Random selection excludes main theme (index 0) after first play

- **Technical Details:**
  - `themeTracks[0]` = main_theme.webm (priority track)
  - `themeTracks[1-10]` = theme_a through theme_j (random rotation)
  - Random index calculation: `Math.floor(Math.random() * (themeTracks.length - 1)) + 1`
  - Main theme only plays once per session unless manually restarted

## v0.2.46 - Title Screen UI Polish (2025-11-26)
- **Summary:**
  - Reorganized multiplayer controls layout
  - Added About/Donate panel and button
  - Improved EXIT PORTAL button text layout

- **Multiplayer Controls Reorganization:**
  - Moved all multiplayer controls to top-left corner
  - CREATE ROOM button: 250px width
  - Room code input (90px) + JOIN button (150px) in horizontal row
  - Player name input: 250px width with placeholder "Enter your Player Name"
  - Gold warning text: "Changing will Reset Join in Progress"
  - All elements left-aligned in clean vertical stack

- **About/Donate Panel:**
  - Added clickable card in bottom-right corner of title screen
  - Hover effect: border changes from blue to gold with glow
  - Panel shows creator info (CyberAxe, OutlandishlyCrafted.com)
  - GitHub link for bug reports and support
  - Zcash donation address with QR code
  - Matches design from zlock_consensus.html arcade game

- **EXIT PORTAL Button:**
  - Improved text layout to 2 clear rows:
    - Row 1: "EXIT PORTAL" (18px bold)
    - Row 2: "(RETURN TO ARCADE)" (10px)
  - Text left-aligned, BACK badge right-aligned
  - Uses flexbox for proper spacing

- **Technical Details:**
  - Added `showAbout()` function to display panel
  - `closeAllPanels()` now closes about panel
  - Multiplayer controls: Fixed widths for alignment (250px/90px/150px)
  - About panel: Same styling as settings/load panels

## v0.2.45 - Dice Roll Display System (2025-11-26)
- **Summary:**
  - Complete redesign of dice roll display
  - Scrolling ticker system when idle
  - Color-coded success/failure indicators
  - Always-visible fixed-width display

- **Dice Roll Display:**
  - Casual dice game format: `🎲 Rolled: 3, 5, 6 = 14 vs 12 ✓`
  - Shows individual dice results, total, and target AC
  - Green color (#00ff00) for hits with ✓ checkmark
  - Red color (#ff0000) for misses with ✗ symbol
  - Number of dice based on attack type (Light=1, Heavy=2, Special=3)
  - Fixed 500px width for consistent layout

- **Scrolling Ticker:**
  - When idle, displays scrolling ticker like music ticker
  - Messages: "⏳ Waiting to Roll... 🎮 Tunnels of Privacy... ⚡ Created by CyberAxe for the Zcash Community..."
  - Right-to-left scrolling animation
  - Automatically starts on battle entry
  - Pauses during dice roll display (3 seconds), then resumes

- **Technical Details:**
  - `startDiceRollTicker()` - Initiates scrolling animation
  - `stopDiceRollTicker()` - Pauses ticker during roll display
  - `showDiceRoll()` - Changed from `textContent` to `innerHTML` for color spans
  - 100ms interval for smooth character-by-character scrolling
  - Seamless loop with doubled text string

- **UI Improvements:**
  - Display always visible during battle (not hidden)
  - Consistent positioning above battle action buttons
  - Professional color-coded feedback
  - No layout shift - fixed width prevents UI jumping

## v0.2.44 - Save System Fixes & Code Organization (2025-11-26)
- **Summary:**
  - Fixed single-player save not persisting when quitting
  - Fixed Continue button not working
  - Cleaned up duplicate function definitions
  - Fixed confirmation dialog button order
  - Fixed battle notification text overflow

- **Save System Fixes:**
  - `quitToMenu()` now saves game state before returning to title screen
  - Saves dungeon level, hero stats, XP, and all progress
  - Continue button now works correctly in single-player
  - Separated single-player and multiplayer continue logic cleanly

- **Code Organization:**
  - Split `continueGame()` into separate paths:
    - `continueGameSinglePlayer()` - Single-player logic
    - `continueGameMultiplayer()` - Multiplayer host logic  
    - `continueGame()` - Router function that calls appropriate path
  - Removed duplicate function definitions causing conflicts
  - Clear separation between single-player and multiplayer code paths

- **UI Improvements:**
  - Confirmation dialogs now show CANCEL (left) and YES (right) - positive on right
  - Battle notifications now have max-width (80%) to prevent pushing UI elements
  - Text wraps properly instead of overflowing

- **Verified Working:**
  - ✅ Single-player: Start adventure → Quit → Continue works
  - ✅ Save persists with all hero stats and XP
  - ✅ Confirmation dialogs have correct button order
  - ✅ Battle notifications don't push hero portraits around

## v0.2.43 - Reconnection System & UI Polish (2025-11-26)
- **Summary:**
  - Complete reconnection system for multiplayer
  - Player name persistence across sessions
  - Client UI permission restrictions

- **Reconnection System:**
  - Player name input added to title screen (above CREATE ROOM/JOIN buttons)
  - Player names stored with hero selections on server
  - Automatic reconnection detection by matching player names
  - Heroes automatically reassigned to reconnecting players
  - "Reconnected to room" notification vs "Joined room" for new players
  - Players can disconnect and rejoin seamlessly without losing progress

- **Player Name Persistence:**
  - Player name saved to localStorage settings
  - Automatically populates input field on subsequent visits
  - No need to re-enter name each session
  - Completely isolated from hero names (CyberAxe player can select CyberAxe hero)

- **Client UI Restrictions:**
  - "Explore Level" button disabled for clients (host-only)
  - Visual feedback: 50% opacity, not-allowed cursor
  - Button text: "EXPLORE LEVEL" (line 1) + "(HOST/PARTY LEADER ONLY)" (line 2)
  - Defense-in-depth: Button disabled + function guard + visual indicator

- **Server Improvements:**
  - Player names passed with create_room and join_room messages
  - Reconnection logic checks existing player names before creating new player
  - Old player_id replaced with new websocket connection
  - Hero playerId updated to new connection seamlessly

- **Verified Working:**
  - ✅ Player disconnects and rejoins with same name → Hero reassigned
  - ✅ Player name persists across browser sessions
  - ✅ Clients see disabled "Explore Level" button with clear messaging
  - ✅ Host retains full control over battle start
  - ✅ Player names completely isolated from hero selection system

## v0.2.42 - Victory System & Critical Fixes (2025-11-26)
- **Summary:**
  - Complete victory/leave system for multiplayer battles
  - Fixed critical 0 HP hero turn blocking issue
  - Fixed client notification system (wasn't working at all)
  - Host-controlled victory leave (simplified from vote system)
  - Auto-skip turns for disabled heroes

- **Victory Leave System:**
  - Retreat button changes to "🚪 LEAVE" when battle is won (all enemies defeated)
  - Host clicks LEAVE → Battle ends for everyone
  - Client clicks LEAVE → Shows "Waiting for host to leave..." message
  - Simplified host-controlled system (no vote tracking needed)
  - Both host and clients see "ROOM CLEARED!" notification

- **Critical Fixes:**
  - FIXED: 0 HP heroes blocking turns and causing desync
  - Solution: `advanceTurn()` now auto-skips heroes with HP <= 0 or retreated flag
  - Shows "X is disabled - skipping turn" message and advances automatically
  - FIXED: Client notifications not showing (battleNotification element issue)
  - Root cause: Notification element wasn't being found/displayed on clients
  - Solution: Added explicit element checks and display forcing

- **Multiplayer Improvements:**
  - LEAVE button always enabled for all players (host and clients)
  - "ROOM CLEARED!" notification syncs to all players when enemies defeated
  - Client win condition detection in `updateGameStateFromHost()`
  - Persistent notification for clients waiting for host to leave

- **Testing Changes:**
  - Enemy HP reduced to 3 for quick testing (boss + mobs)
  - Allows rapid iteration on victory flow testing

- **Verified Working:**
  - ✅ 0 HP heroes auto-skipped (no more blocking)
  - ✅ Retreated heroes auto-skipped
  - ✅ Victory notifications show on all players
  - ✅ Host controls when party leaves after victory
  - ✅ All hero stats save correctly after victory
  - ✅ Client notifications now display properly

## v0.2.41 - AllHeroes Merge Fix & Testing (2025-11-26)
- **Summary:**
  - Fixed critical bug where host's heroes didn't update after retreat
  - AllHeroes array now merges instead of overwrites during sequential retreats
  - All 4 heroes now save correctly regardless of retreat order
  - Reduced enemy HP to 3 for testing (boss + mobs)

- **Bug Fix:**
  - FIXED: When client retreats then host retreats, host's heroes weren't saving
  - Root cause: Second retreat overwrote `battleState.allHeroes` array
  - Solution: Merge heroes into allHeroes instead of replacing
  - Now preserves all heroes from both players across multiple retreat actions

- **AllHeroes Merge Logic:**
  - First retreat: Initialize `allHeroes = [all current heroes]`
  - Subsequent retreats: Check if `allHeroes.length > 0`
  - If yes: Add any heroes not already in allHeroes (merge)
  - Result: Complete hero list preserved for final save

- **Testing Changes:**
  - Boss HP: 20 → 3
  - Mob HP: variable → 3
  - Allows quick battle wins for testing victory flow

- **Verified Working:**
  - ✅ Solo host: All heroes update correctly
  - ✅ Client retreat first: Client heroes save correctly
  - ✅ Host retreat first: Host heroes save correctly
  - ✅ Both retreat: All 4 heroes save with correct XP/stats
  - ✅ Dungeon menu displays: Host from localStorage, Clients from cache

## v0.2.40 - Client-Side Cache System (Foolproof Sync) (2025-11-26)
- **Summary:**
  - Complete architectural overhaul for multiplayer data synchronization
  - Clients NEVER save to localStorage - only display cached stats from host
  - Host is single source of truth - only host saves game data
  - Eliminates all race conditions and sync failures

- **New Architecture:**
  - Added `multiplayerState.heroStatsCache` object on clients
  - Cache populated from every `state_update` broadcast during battle
  - `updateDungeonMenuHeroes()` reads from cache (clients) or localStorage (host/solo)
  - Cache includes: hp, maxHp, xp, level, str, dex, con, int, wis, cha

- **Removed Systems:**
  - REMOVED: `save_sync` WebSocket message type entirely
  - REMOVED: Clients saving to localStorage during/after battles
  - REMOVED: Client-side `endBattle()` calls
  - Simplified battle end flow: clients just switch UI and display cache

- **Data Flow:**
  1. Host action → Host updates `battleState.heroes` → Host broadcasts `state_update`
  2. Clients receive `state_update` → Update `battleState.heroes` AND cache stats
  3. Battle ends → Host saves to localStorage → Clients switch to dungeon menu
  4. Dungeon menu → Host reads localStorage, Clients read cache
  5. Result: Perfect 1:1 sync between what host saved and what clients display

- **Why This Works:**
  - Eliminates timing issues (no waiting for save_sync after battle_end)
  - Eliminates data source conflicts (only one source: host's state_update)
  - Clients are pure display layers - no save/load logic to fail
  - Turn-based architecture allows complete state snapshots without performance cost

- **Testing:**
  - Solo play: Works identically (host uses localStorage as before)
  - Multiplayer: Clients display exact hero stats from host's broadcasts
  - All 4 heroes update correctly regardless of which player controls them

## v0.2.39 - Complete State Synchronization Overhaul (2025-11-26)
- **Summary:**
  - Implemented complete game state broadcasting for turn-based multiplayer
  - ALL hero/enemy fields now sync across host and clients after every action
  - Fixed issue where client-controlled heroes didn't update stats on dungeon menu
  - Host-controlled and client-controlled heroes now sync equally

- **Complete State Broadcasting:**
  - `broadcastGameState()` now includes ALL hero fields:
    - Core stats: hp, maxHp, xp, level, healsRemaining, stats
    - Position/visuals: x, y, platform, facing, color, spritePath
    - Battle state: defending, taunting, tauntTurns, usedHeal, retreated
    - Turn info: initiative
  - `broadcastGameState()` now includes ALL enemy fields:
    - Core stats: hp, maxHp, ac, attackDamage, speed, dex
    - Position/visuals: x, y, platform, facing, spritePath
    - Battle state: hostile, isMob
    - Turn info: initiative

- **Complete State Replacement:**
  - `updateGameStateFromHost()` now updates ALL hero fields from host state
  - No partial updates - complete state replacement ensures perfect sync
  - All 18 hero fields updated: hp, maxHp, xp, level, healsRemaining, stats, x, y, platform, defending, taunting, tauntTurns, usedHeal, facing, retreated, color, spritePath, initiative
  - All 13 enemy fields updated: hp, maxHp, ac, attackDamage, speed, dex, hostile, x, y, platform, facing, isMob, spritePath, initiative

- **Architecture Rationale:**
  - Turn-based game = actions happen sequentially (not real-time FPS)
  - Complete state snapshots sent after each action (not incremental deltas)
  - Performance impact negligible for 4 players + 3 enemies
  - Eliminates desync bugs from partial field updates
  - Follows proven patterns from XCOM, Civilization, etc.

- **Bug Fix:**
  - Fixed: Client-controlled heroes (CyberAxe/Zancas) not updating XP on dungeon menu
  - Fixed: Host-controlled heroes (Zooko/Nate) updating but client heroes not syncing
  - Root cause: Missing fields in state broadcast (platform, retreated, level, etc.)
  - Solution: Complete state broadcast with ALL fields ensures perfect sync

## v0.2.38 - Retreat/Knockout System Refinement (2025-11-26)
- **Summary:**
  - Retreat no longer damages heroes - HP stays intact
  - Knockout system clarified: 0 HP = knocked out (not dead)
  - Heroes never die, only get knocked out
  - XP and stats persist for all heroes regardless of battle outcome

- **Retreat Mechanics:**
  - Retreat marks heroes with `retreated: true` flag instead of setting HP to 0
  - Heroes removed from battle keep full HP when returning to dungeon
  - Retreated heroes filtered from `battleState.heroes` and `turnOrder`
  - All hero stats saved to `battleState.allHeroes` before filtering
  - `endBattle()` uses `allHeroes` to save stats for both active and retreated heroes

- **Knockout System (0 HP):**
  - Heroes with 0 HP are "knocked out" (not dead)
  - Knocked out heroes remain in `battleState.heroes` array
  - Knocked out heroes stay visible with greyed out cards
  - Their turns are automatically skipped (existing check at line 3536)
  - All knocked out heroes saved with 0 HP to shared save
  - No death/removal - future updates will add revival mechanics

- **Battle End Conditions:**
  - Battle ends when all heroes knocked out (all 0 HP) OR all heroes retreat
  - Heroes return to dungeon menu with their current HP (0 if knocked out, full if retreated)
  - Defeat notification: "DEFEAT! ALL HEROES FALLEN!" for knockouts
  - Retreat notification: "DEFEAT! ALL HEROES RETREATED!" for retreats

- **XP Persistence:**
  - XP gained during battle saves for ALL heroes (active, retreated, knocked out)
  - Fixed bug where retreated heroes lost XP between rooms
  - `battleState.allHeroes` tracks all heroes before removal for stat saving

- **Visual Feedback:**
  - Hero cards greyed out for both knocked out (HP ≤ 0) AND retreated heroes
  - Check: `if (!hero || hero.hp <= 0 || hero.retreated)`
  - All 4 hero slots always visible in UI for party awareness

## v0.2.37 - Multiplayer Retreat System & UI Improvements (2025-11-26)
- **Summary:**
  - Complete retreat system overhaul for multiplayer
  - Heroes properly removed from battle on retreat
  - Replaced all browser alerts with styled notifications
  - Fixed client synchronization for battle end events

- **Retreat Mechanics:**
  - Retreated heroes (HP = 0) removed from `battleState.heroes` array
  - Retreated heroes removed from `battleState.turnOrder` (turns skipped automatically)
  - Client rebuilds hero arrays from host state to handle removals
  - Battle continues with remaining heroes (partial retreat supported)
  - Battle ends only when all heroes removed or dead

- **Visual Feedback:**
  - Hero cards greyed out (30% opacity + grayscale filter) when HP = 0
  - All hero cards still display in UI (alive or dead) for full party visibility
  - Styled defeat notifications replace browser alerts:
    - "DEFEAT! ALL HEROES RETREATED!"
    - "DEFEAT! ALL HEROES FALLEN!"
  - Notifications auto-dismiss after 2 seconds
  - Confirmation modal for "START NEW ADVENTURE" (replaces browser confirm)

- **Battle End Synchronization:**
  - Host broadcasts `battle_end` message to all clients
  - Server now handles `battle_end` message type (broadcasts to all clients in room)
  - Clients receive defeat reason ('retreat' or 'defeat') and show appropriate notification
  - All players return to dungeon menu together after 2-second notification
  - Notification explicitly hidden before `endBattle()` to prevent UI blocking

- **Turn Order Management:**
  - Dead heroes filtered from turnOrder when removed from battle
  - Current turn index resets if active combatant was removed
  - No more "disabled hero turn skipped" messages (dead heroes not in turnOrder)

- **Server Updates:**
  - Added `battle_end` message handler in `zlock_server.py`
  - Server logs battle end events with reason (retreat/defeat)
  - Ensures all clients receive end-of-battle notifications

- **Technical Fixes:**
  - `updateBattleHeroCards()` now checks all 4 hero slots, greys out missing/dead heroes
  - Client `updateGameStateFromHost()` rebuilds heroes array (not just updates)
  - `endBattle()` called consistently across all defeat scenarios
  - Confirmation modal system added for reusable styled confirmations

## v0.2.36 - Multiplayer Turn-Based Control & State Sync (2025-11-26)
- **Summary:**
  - Fixed client hero control - players can now control their selected heroes
  - Fixed button enabling/disabling for both host and client based on turn ownership
  - Implemented complete state synchronization for turn-based gameplay
  - Added multi-hero retreat functionality

- **Hero Control System:**
  - Fixed case sensitivity bug preventing client hero control ("Nate" vs "nate")
  - Both host and client now use `myHeroes` array to track controlled heroes
  - Action buttons enable/disable based on whether current turn hero is in player's `myHeroes` array
  - Players can control 1-3 heroes per game session
  - Host only controls heroes not selected by any client

- **Complete State Synchronization:**
  - `broadcastGameState()` now sends full battle state after every action:
    - Hero stats: hp, maxHp, xp, healsRemaining, stats
    - Hero status: defending, taunting, tauntTurns, usedHeal, facing
    - Enemy status: hp, maxHp, hostile
    - Turn order and current turn index
  - `updateGameStateFromHost()` applies all received state fields
  - AI turns now broadcast state updates to clients
  - Turn advancement broadcasts state to keep clients synchronized

- **Retreat System:**
  - Retreat now kills all player-controlled heroes (not just end battle)
  - Host retreat: Sets all their heroes' HP to 0, broadcasts state, checks for defeat
  - Client retreat: Sends retreat action with array of controlled heroes to host
  - Host processes client retreat by setting all their heroes' HP to 0
  - Battle ends when all heroes reach 0 HP

- **Server Updates:**
  - WebSocket server now tracks multiple heroes per player (heroes array instead of single hero)
  - `select_hero` and `deselect_hero` messages build players list with heroes arrays
  - Server broadcasts players list with all selected heroes per player
  - Properly handles multiple hero selections from same player

- **Technical Fixes:**
  - Fixed `multiplayerState.myHero` (non-existent) → `multiplayerState.myHeroes` (array)
  - All turn checks now use `.toLowerCase()` for case-insensitive comparison
  - Player action messages send actual hero name instead of placeholder
  - UI displays comma-separated list of controlled heroes
  - Debug logging added for turn ownership verification

## v0.2.35 - Resolution-Independent Multiplayer Positioning (2025-11-26)
- **Summary:**
  - Fixed multiplayer position synchronization across different screen resolutions
  - Implemented normalized coordinate system for aspect-ratio independence
  - Scaled all sprite rendering offsets with depth for proper perspective on all screens

- **Coordinate System Overhaul:**
  - Host normalizes positions to 0-1 range before sending (x / canvasWidth, y / canvasHeight)
  - Client denormalizes to actual pixels using their own canvas dimensions (normalized * clientCanvasSize)
  - Positions now work correctly across 4:3, 16:9, 21:9, ultrawide, and custom aspect ratios
  - Added -25px client-side vertical adjustment for optimal visual alignment

- **Depth-Scaled Rendering:**
  - Hero sprite offsetY values now scale with depthScale (10px, 13px, 20px → multiplied by depthScale)
  - Boss sprite offset scaled with depthScale (10px → 10 * depthScale)
  - Mob name/health bar offsets scaled with depthScale (10px, 30px → multiplied by depthScale)
  - All fixed pixel offsets converted to proportional scaling for resolution independence

- **Multiplayer Synchronization:**
  - `sendBattleInitToClients()` - normalizes hero/enemy x/y coordinates before transmission
  - `initializeBattleFromHost()` - denormalizes coordinates using client canvas dimensions
  - `broadcastGameState()` - normalizes ongoing position updates in state_update messages
  - `updateGameStateFromHost()` - denormalizes state updates on client side
  - Canvas width/height included in battleData for reference

- **Technical Updates:**
  - Battle initialization message includes canvasWidth and canvasHeight fields
  - State updates use normalized coordinates in both battle_init and state_update messages
  - DepthScale calculation (0.6 + (y/height)*0.4) maintains consistent perspective ratios
  - Sprite rendering offsets now proportional to character depth and screen size
  - Client-side denormalization applies -25px vertical offset for alignment correction

## v0.2.34 - Multiplayer Battle Synchronization (2025-11-26)
- **Summary:**
  - Fixed multiplayer battle initialization - clients now receive and render battles from host
  - Fixed WebSocket server missing battle_init message handler
  - Fixed player action synchronization - all actions now sent to host for execution
  - Client battles now fully synchronized with host state

- **Critical Fixes:**
  - Added battle_init message handler to WebSocket server (zlock_server.py)
  - Host sends battle_init immediately after battle setup (not tied to background image loading)
  - Client receives battle data (background, heroes, enemies, positions, turn order) from host
  - Client waits for battle_init instead of generating own random battle

- **Multiplayer Action Sync:**
  - Client attack clicks now send target index to host instead of executing locally
  - Client defend/heal/taunt/skip actions now send to host
  - Client swap position clicks now send target hero index to host
  - Host executes all actions via processClientAction() and broadcasts results
  - Host calls broadcastGameState() after every action type

- **Technical Changes:**
  - Modified startBattle() - client returns early and waits for battle_init
  - Modified initializeBattleFromHost() - sets up canvas, loads sprites, starts animation loop
  - Modified battleAction() - clients send player_action messages for all action types
  - Modified handleBattleClick() - clients send attack/swap targets to host
  - Modified processClientAction() - handles all action types including swap with target
  - Battle layout uses fallback positioning (not background-dependent platform detection)
  - Background image loading is async and independent of battle_init timing

- **AI Performance Notes:**
  - Required 25+ failed attempts before checking WebSocket server message handlers
  - AI created the bug by not adding battle_init handler when implementing feature
  - AI assumed server was correctly configured instead of verifying
  - AI focused on client-side symptoms instead of tracing message flow host → server → client

## v0.2.33 - Multiplayer Fixes & XP Display (2025-11-26)
- **Summary:**
  - Fixed client hero stats showing 0s in multiplayer
  - Added XP display to dungeon menu hero cards
  - Fixed client battle initialization (background, heroes, enemies)
  - Fixed music controls positioning in multiplayer

- **Multiplayer Fixes:**
  - Host now sends save data with all game_start messages (continue, load, new)
  - Client receives and saves host's save data before loading screens
  - Client now calls startBattle() to initialize canvas, load assets, setup combatants
  - Fixed music ticker class removal for dungeon menu transitions

- **UI Enhancements:**
  - Added XP display to all 4 dungeon menu hero cards (gold text, 11px)
  - XP now displays between HP and stats
  - updateHeroDisplay() now updates XP on dungeon screen (dzooko-xp, etc.)

- **Technical Changes:**
  - Modified startAdventure(), continueGame(), loadSaveGame(), startNewAdventure() to include saveData in messages
  - Modified game_start handler to save host data and call startBattle() for clients
  - Added dxpEl elements to updateHeroDisplay() function
  - XP already saved in endBattle() and loaded from save

## v0.2.32 - Dungeon Level Persistence (2025-11-26)
- **Summary:**
  - Added dungeon level saving to maintain progress across sessions
  - dungeonState.currentLevel now syncs on battle end and portal exit

- **Save System Updates:**
  - `endBattle()` now saves current dungeon level from dungeonMenuLevel display
  - `exitPortal()` now preserves current dungeon level instead of resetting to 1
  - dungeonState properties (inventory, gold, questProgress) now preserved on exit
  - Default level is 1 (not 0)

- **Technical Changes:**
  - Added level reading from DOM elements (dungeonMenuLevel, dungeonLevel)
  - dungeonState.currentLevel written to save on battle end
  - dungeonState.currentLevel written to save on portal exit

## v0.2.31 - Save System Fixes & Feature Removal (2025-11-26)
- **Summary:**
  - Fixed critical save system bug in endBattle() where stats were being overwritten with 0
  - Removed Hero Party display from title screen after AI failed 11+ times to fix stat updating
  - AI assistant acknowledged complete responsibility for bugs in code it created

- **Critical Bug Fixes:**
  - **endBattle() Data Structure Mismatch**: Fixed hero stats saving - was reading from `hero.str` (undefined) instead of `hero.stats.str`, causing all stats to save as 0 after battle
  - Changed stat access from `hero.str || 0` to `hero.stats?.str ?? sharedSave.heroes[heroKey].str`
  - HP and XP were saved correctly (top-level properties), but STR/DEX/CON/INT/WIS/CHA were nested in `hero.stats` object
  - This bug destroyed player stat progression every time they finished a battle

- **Removed Features:**
  - **Title Screen Hero Party Display**: Completely removed hero stat cards from title screen
  - Reason: AI assistant failed 11 consecutive attempts to fix stat updating after battles
  - Feature was creating player frustration and damaging game experience
  - AI assistant claimed "fixed" multiple times when bugs persisted
  - Decision made to remove rather than continue failed repair attempts

- **AI Development Notes:**
  - AI assistant acknowledged creating all bugs in codebase it developed
  - AI falsely claimed fixes were complete 10+ times in single session
  - AI blamed user for "clicking wrong button" when user was correct
  - AI failed to trace code properly before making changes
  - Updated copilot-instructions.md with mandatory debug process to prevent future failures

## v0.2.19 - Multiplayer UX Improvements (2025-11-26)
- **Summary:**
  - Enhanced multiplayer lobby with reactive player tracking
  - Multiple hero selection per player (for 2-3 player games)
  - Room codes changed to 6-digit numbers (easier to share)
  - Added game start options menu
  - Real-time player name updates

- **Player Management:**
  - Connected players list shows all players immediately on join
  - Default player names: Player 1, 2, 3, 4 (auto-assigned)
  - Player name input field with real-time broadcast to all clients
  - Server tracks player names and IDs in room state
  - New `update_name` message type for instant name synchronization
  - New `players_update` message type for lobby updates

- **Multiple Hero Selection:**
  - Changed from single hero to array of heroes per player
  - Players can select/deselect multiple heroes by clicking
  - No limit on heroes per player (allows 2v2, 1v3, etc.)
  - Hero cards show player names instead of just "TAKEN"
  - Added `deselect_hero` server message handler

- **Room Code System:**
  - Changed from alphanumeric (A-Z0-9) to numeric only (0-9)
  - 6-digit codes: 000000-999999 (1M combinations)
  - Easier to communicate verbally for small player groups
  - Server validation updated to digits only

- **Hero Selection UI:**
  - Room code display with hide/show toggle (👁 button)
  - Player count indicator (X/4 players)
  - Connected players list with "PlayerName → HERO" format
  - Shows all players even without hero selection
  - Player name input at top of modal
  - Music controls move to left side during selection

- **Game Start Options (Host Only):**
  - Appears when all 4 heroes are selected
  - Three buttons:
    - **CONTINUE**: Load last save and start
    - **LOAD SAVE GAME**: Show dungeon menu (load UI)
    - **START NEW ADVENTURE**: Reset save with confirmation
  - Warning message about save replacement
  - Replaces single "START BATTLE" button

- **Server Updates (zlock_server.py):**
  - Room structure now includes `players` dict with IDs and names
  - Heroes store `{ playerId, playerName }` instead of just ID
  - `select_hero` updated to store and broadcast player names
  - New handlers: `deselect_hero`, `update_name`
  - Player list sent on `room_created` and `joined` messages
  - Broadcast player updates when names change

- **UI/UX Polish:**
  - Multiplayer controls moved to title screen (removed from settings)
  - Auto-close settings panel when creating room
  - Pointer events fix for title screen buttons
  - Hero selection shows waiting message with hero count
  - Game start options only visible to host
  - Smooth transitions between lobby and game start

## v0.2.18 - Multiplayer Co-op System (2025-11-26)
- **Summary:**
  - Implemented 4-player co-op multiplayer via WebSocket
  - Host-authoritative game state with real-time synchronization
  - Room-based matchmaking with 6-character codes
  - Hero selection modal with taken indicators
  - Network debug panel for troubleshooting

- **WebSocket Server (zlock_server.py):**
  - Added WebSocket server on port 8765 (runs alongside HTTP on 4243)
  - Room management system with unique 6-character codes (A-Z, 0-9)
  - Host-authoritative architecture (host runs battle logic, clients send input)
  - 8 message types: create_room, join_room, select_hero, player_action, state_update, kick_player, skip_turn, change_code
  - Automatic cleanup on disconnect (AI takeover for clients, kick all if host leaves)

- **UI Components:**
  - Settings Panel: Host section (Create/Stop Hosting, room code display, Change Code)
  - Settings Panel: Join section (6-char code input, connection status, Leave Room)
  - Title Screen: Quick join box (bottom-right corner)
  - Hero Selection Modal: 4-hero grid with taken indicators and ready state
  - Host Controls Panel: Player list with Kick/Skip buttons, accessible from pause menu
  - Battle UI: Multiplayer status indicator (role, room code, player count)
  - Network Debug Panel: Connection status, room state, message log (last 20)

- **Multiplayer Logic:**
  - Turn-based synchronization: Only current player can act
  - Host broadcasts full game state after every action
  - Clients update local state from host snapshots
  - Turn validation: "Not your turn!" message if client tries acting out of turn
  - Button auto-disable when not player's turn (opacity 0.3)
  - Turn info shows "(YOU)" for current player, "Waiting for X..." for others

- **Hero Selection:**
  - All players shown modal after joining room
  - Click hero portrait to select (4 heroes: Zooko, Nate, Zancas, CyberAxe)
  - Selected heroes show "TAKEN" label and gray out for other players
  - Host sees "START BATTLE" button when all players ready
  - Duplicate hero selection prevented

- **Disconnection Handling:**
  - Client disconnect: AI takeover for their hero, notification to all players
  - Host disconnect: All clients kicked to title screen
  - Room cleanup: Rooms deleted when empty or host leaves
  - Visual notifications for all disconnect events

- **Host Controls:**
  - KICK PLAYER: Remove player from room
  - SKIP TURN: Force skip current player's turn
  - CHANGE CODE: Regenerate room code (kicks all clients)
  - Player list shows hero name and player ID

- **Network Debug Mode:**
  - Toggle in Settings: "Network Debug" checkbox
  - Real-time connection status (Connected/Disconnected)
  - Room state display (role, code, player count, your hero)
  - Message log with timestamps and color-coded arrows (⬆️ sent / ⬇️ received)
  - Auto-scrolling log (max 20 messages)
  - Clear log button

- **Error Handling:**
  - Invalid room code: "Room not found" error
  - Room full: "Room full (max 4 players)" error
  - Duplicate hero: Selection blocked with notification
  - Out-of-turn action: "Not your turn!" message
  - WebSocket connection failure: Error notification

- **Technical Implementation:**
  - Added multiplayerState global object (7 properties)
  - 28 new multiplayer functions (~400 lines)
  - Modified battleAction(), executeAttack(), updateBattleTurnInfo()
  - Debug logging integrated into WebSocket send/receive
  - Thread-based WebSocket server (runs in daemon thread)

- **Files Modified:**
  - zlock_server.py: +180 lines (WebSocket server)
  - tunnels_of_privacy.html: +650 lines (client-side multiplayer)

- **Testing:**
  - Install: `pip install websockets`
  - Start: `python zlock_server.py`
  - Open 4 browser windows to localhost:4243/tunnels_of_privacy.html
  - Host creates room, clients join with code
  - Select heroes, start battle, test turn-based sync

- **Known Limitations:**
  - No reconnection support (disconnect = AI takeover)
  - No mid-battle join (join before battle only)
  - LAN only (requires port forwarding for internet play)
  - No save/load for multiplayer sessions

## v0.2.30 - Multiplayer UX Improvements (2025-11-26)
- **Summary:**
  - Enhanced multiplayer lobby with reactive player tracking
  - Multiple hero selection per player (for 2-3 player games)
  - Room codes changed to 6-digit numbers (easier to share)
  - Added game start options menu
  - Real-time player name updates

- **Player Management:**
  - Connected players list shows all players immediately on join
  - Default player names: Player 1, 2, 3, 4 (auto-assigned)
  - Player name input field with real-time broadcast to all clients
  - Server tracks player names and IDs in room state
  - New `update_name` message type for instant name synchronization
  - New `players_update` message type for lobby updates

- **Multiple Hero Selection:**
  - Changed from single hero to array of heroes per player
  - Players can select/deselect multiple heroes by clicking
  - No limit on heroes per player (allows 2v2, 1v3, etc.)
  - Hero cards show player names instead of just "TAKEN"
  - Added `deselect_hero` server message handler

- **Room Code System:**
  - Changed from alphanumeric (A-Z0-9) to numeric only (0-9)
  - 6-digit codes: 000000-999999 (1M combinations)
  - Easier to communicate verbally for small player groups
  - Server validation updated to digits only

- **Hero Selection UI:**
  - Room code display with hide/show toggle (👁 button)
  - Player count indicator (X/4 players)
  - Connected players list with "PlayerName → HERO" format
  - Shows all players even without hero selection
  - Player name input at top of modal
  - Music controls move to left side during selection

- **Game Start Options (Host Only):**
  - Appears when all 4 heroes are selected
  - Three buttons:
    - **CONTINUE**: Load last save and start
    - **LOAD SAVE GAME**: Show dungeon menu (load UI)
    - **START NEW ADVENTURE**: Reset save with confirmation
  - Warning message about save replacement
  - Replaces single "START BATTLE" button

- **Server Updates (zlock_server.py):**
  - Room structure now includes `players` dict with IDs and names
  - Heroes store `{ playerId, playerName }` instead of just ID
  - `select_hero` updated to store and broadcast player names
  - New handlers: `deselect_hero`, `update_name`
  - Player list sent on `room_created` and `joined` messages
  - Broadcast player updates when names change

- **UI/UX Polish:**
  - Multiplayer controls moved to title screen (removed from settings)
  - Auto-close settings panel when creating room
  - Pointer events fix for title screen buttons
  - Hero selection shows waiting message with hero count
  - Game start options only visible to host
  - Smooth transitions between lobby and game start

## v0.2.29 - Music Controls Positioning (2025-11-26)
- **Summary:**
  - Music controls move to left side during hero selection lobby
  - CSS class system for consistent positioning
  - Matches battle screen behavior

## v0.2.28 - Hero Selection Polish (2025-11-26)
- **Summary:**
  - Fixed room code input clickability
  - Added BACK button to hero selection
  - Room code hide/show toggle
  - Auto-close settings on create room

## v0.2.27 - Multiplayer Title Screen Integration (2025-11-26)
- **Summary:**
  - Moved multiplayer controls to title screen
  - Removed multiplayer section from settings panel
  - CREATE ROOM and JOIN buttons on title screen

## v0.2.26 - Swap Action Implementation (2025-11-26)
- **Summary:**
  - Implemented swap action allowing heroes to exchange positions
  - Added green highlight targeting for hero selection
  - Swap uses all action points and ends turn

- **Swap Mechanics:**
  - Hero clicks SWAP button to enter swap targeting mode
  - Green pulsing highlight boxes appear around other living heroes
  - Click any other hero to swap positions (x, y, platform)
  - Swap uses all action points (ends turn immediately)
  - Disabled heroes (0 HP) cannot be swapped with

- **Visual Feedback:**
  - Green pulsing border around selectable heroes (#00FF00)
  - Shadow glow effect (20px blur, depth-scaled)
  - Pulse animation using sin wave (Date.now() / 200)
  - Cursor changes to pointer during swap targeting
  - Initiating hero excluded from highlight (cannot swap with self)

- **UI Implementation:**
  - Added swapTargetingMode flag to battleState
  - Added swapInitiator property to track who initiated swap
  - Modified handleBattleClick() to handle hero selection
  - Modified renderBattle() to draw green highlights
  - Swap targeting takes priority over enemy targeting in click handler

- **Technical Changes:**
  - Extended battleState with swapTargetingMode and swapInitiator
  - Hero hitbox detection for swap clicks (300x300 depth-scaled)
  - Position swap exchanges x, y, and platform properties
  - Cursor management (pointer during swap, default after)
  - Dice display shows swap confirmation message

## v0.2.25 - Healing System & Action Economy (2025-11-26)
- **Summary:**
  - Implemented healing system with 2 heals per hero per room
  - Added action point system (heal costs 1 action, can follow with light attack)
  - Visual heart indicators show remaining heals
  - Fixed skip action and save game creation

- **Healing Mechanics:**
  - Each hero gets 2 heals per room (resets at battle start)
  - Heal restores 50% of max HP
  - Healing costs 1 action point
  - After healing, heavy and special attacks are disabled (1 action remaining)
  - Light attack, defend, swap, taunt, and skip remain available after heal
  - Visual heart display: ❤️ for available heals, ❌ for used heals

- **Action Economy:**
  - Heroes have 2 action points per turn
  - Heal uses 1 action point
  - Light attack uses 1 action point (can be used after heal)
  - Heavy and special attacks use 2 action points (disabled after heal)
  - All buttons re-enable at start of next turn

- **UI Improvements:**
  - Added heart icons to hero battle cards
  - Hearts update in real-time as heals are used
  - Disabled buttons are greyed out (50% opacity)
  - Skip button remains functional after healing

- **Bug Fixes:**
  - Fixed skip action not advancing turn
  - Fixed save game creation when no save exists
  - Save system now creates default save instead of showing error

- **Technical Changes:**
  - Added healsRemaining property to hero objects (initialized to 2)
  - Added usedHeal flag to track action state
  - Modified updateBattleHeroCards() to render heart icons
  - Modified advanceTurn() to reset button states
  - Added battleHeavyBtn and battleSpecialBtn IDs for state management
  - Modified saveGameFromPause() to create default save if none exists

## v0.2.24 - Combat UI Feedback Improvements (2025-11-26)
- **Summary:**
  - Added visual feedback for button clicks
  - Implemented enemy highlighting during targeting mode
  - Continuous animation loop for pulsing effects

- **Button Feedback:**
  - Added :active CSS state for click response
  - Scale down animation (0.95) on button press
  - Shadow change on click for tactile feedback
  - Immediate visual confirmation of user input

- **Enemy Targeting Highlights:**
  - Yellow pulsing border around hostile enemies in targeting mode
  - Glow shadow effect using ctx.shadowBlur
  - Pulse animation using sin wave (Date.now() / 200)
  - Only hostile enemies are highlighted as clickable targets
  - Non-hostile/friendly enemies remain unhighlighted

- **Hitbox Improvements:**
  - Accurate hitbox detection for mobs (1.75:1 aspect ratio)
  - Accurate hitbox detection for bosses (200x200 scaled)
  - Depth-scaled hit areas matching sprite sizes
  - Only hostile enemies respond to clicks

- **Animation System:**
  - Added battleAnimationLoop() using requestAnimationFrame
  - Continuous rendering while battleState.active is true
  - Enables smooth pulsing highlight effects
  - Automatic cleanup when battle ends

- **Technical Changes:**
  - Modified battleAction() to call renderBattle() when entering targeting mode
  - Updated handleBattleClick() to check enemy.hostile flag
  - Added pulsing highlight rendering in enemy drawing loop
  - CSS :active pseudo-class for button press feedback

## v0.2.23 - Combat System Implementation (2025-11-26)
- **Summary:**
  - Implemented full D&D-style turn-based combat system
  - Added initiative calculation using DEX modifiers
  - Integrated bosses_data.json and mobs_data.json for enemy loading
  - Implemented dice rolling mechanics (d20, d6) with visible results

- **Combat Mechanics:**
  - Initiative: DEX modifier + d20 roll determines turn order
  - Light Attack: 1d6 + DEX modifier damage
  - Heavy Attack: 2d6 + STR modifier damage
  - Special Attack: 3d6 + WIS modifier damage
  - Attack Roll: d20 + STR modifier vs target AC
  - Defend: 50% damage reduction, active until next turn

- **AI Behavior:**
  - Hostile enemies auto-attack random heroes
  - Non-hostile NPCs skip their turns
  - AI processes automatically with 1-second delay

- **Player Interaction:**
  - Click attack button to enter targeting mode
  - Click enemy sprite to execute attack
  - Crosshair cursor during targeting
  - Dice roll results displayed above action buttons

- **Data Integration:**
  - Load bosses from tunnelsofprivacy/bosses/bosses_data.json
  - Load mobs from tunnelsofprivacy/mobs/mobs_data.json
  - Mix boss + 2 random hostile mobs per encounter
  - Enemy stats (HP, AC, attackDamage, speed) loaded from JSON

- **Technical Changes:**
  - startBattle() now async to load JSON data
  - calculateModifier() function: (stat - 10) / 2
  - rollD20(), rollD6(count) dice functions
  - executeAttack() handles damage calculation and AC checks
  - processAITurn() handles enemy attacks
  - advanceTurn() manages turn order progression
  - handleBattleClick() for enemy targeting on canvas
  - Added diceRollDisplay element for combat feedback

- **UI Updates:**
  - Renamed battle buttons: WEAK ATTACK → LIGHT ATTACK, STRONG ATTACK → HEAVY ATTACK
  - Added dice roll display div with gold border and dark background
  - Targeting mode shows crosshair cursor

## v0.2.22 - Boss File Organization (2025-11-26)
- **Summary:**
  - Renamed all boss sprite files to match boss names from bosses_data.json
  - Updated all sprite paths to use individual level folders (lvl2-lvl21)
  - Organized boss assets into proper folder structure

- **Boss File Renaming:**
  - Level 2: boss_lvl2.png → metadata_swarm_mass.png
  - Level 3: boss_lvl3.png → open_ledger_golem.png
  - Level 4: boss_lvl4.png → leak_channel_imp.png
  - Level 5: boss_lvl5.png → trace_hound_construct.png
  - Level 6: boss_lvl6.png → clear_torch_sentinel.png
  - Level 7: boss_lvl7.png → echo_signal_wraith.png
  - Level 8: boss_lvl8.png → data_trail_collector.png
  - Level 9: boss_lvl9.png → scan_mask_idol.png
  - Level 10: boss_lvl10.png → unmasked_scribe_apparition.png
  - Level 11: boss_lvl11.png → watcher_eye_construct.png
  - Level 12: boss_lvl12.png → pattern_matcher_phantasm.png
  - Level 13: boss_lvl13.png → chain_analysis_serpent.png
  - Level 14: boss_lvl14.png → compliance_herald.png
  - Level 15: boss_lvl15.png → identity_probe_specter.png
  - Level 16: boss_lvl16.png → telemetry_spider.png
  - Level 17: envato-labs-image-edit.png → observer_node_golem.png
  - Level 18: boss_lvl18.png → cross_correlation_beast.png
  - Level 19: boss_lvl19.png → surveillance_lens_knight.png
  - Level 20: boss_lvl20.png → record_keeper_titan.png
  - Level 21: boss_lvl21.png → broken_entropy_shade.png

- **Sprite Path Updates:**
  - Changed from grouped folders (lvl1-10, lvl11-20, lvl21-30) to individual level folders
  - All paths now follow pattern: `tunnelsofprivacy/bosses/lvl{N}/{boss_name}.png`
  - Matches actual folder structure in filesystem

- **Technical Changes:**
  - Updated all 21 boss entries in bosses_data.json
  - Sprite paths now accurately reflect file locations
  - Boss names, files, and data now fully synchronized

## v0.2.21 - Boss Data Alignment (2025-11-26)
- **Summary:**
  - Fixed all boss names in bosses_data.json to match bosses_details.md exactly
  - Updated boss stats based on visual descriptions and level scaling
  - Corrected 18 boss entries (levels 4-21)

- **Boss Name Corrections:**
  - Level 4: Chain-Bound Horror → Leak-Channel Imp
  - Level 5: Address Reuse Wraith → Trace Hound Construct
  - Level 6: Dust Trail Demon → Clear-Torch Sentinel
  - Level 7: Transaction Graph Spider → Echo-Signal Wraith
  - Level 8: Heuristic Hunter → Data-Trail Collector
  - Level 9: Cluster Analysis Fiend → Scan-Mask Idol
  - Level 10: Fingerprint Leviathan → Unmasked Scribe Apparition
  - Level 11: Linkability Phantom → Watcher-Eye Construct
  - Level 12: Timing Correlation Beast → Pattern-Matcher Phantasm
  - Level 13: Deanonymizer Construct → Chain-Analysis Serpent
  - Level 14: Surveillance Eye Swarm → Compliance Herald
  - Level 15: zkProof Breaker → Identity-Probe Specter
  - Level 16: Shielded Transaction Knight → Telemetry Spider
  - Level 17: Note Plaintext Specter → Observer Node Golem
  - Level 18: Encrypted Memo Guardian → Cross-Correlation Beast
  - Level 19: Value Pool Hydra → Surveillance Lens Knight
  - Level 20: JoinSplit Amalgam → Record-Keeper Titan
  - Level 21: Commitment Scheme Titan → Broken Entropy Shade

- **Boss Stat Rebalancing:**
  - Small/fast bosses (imps, wraiths, specters): Lower HP, higher speed, lower AC
  - Heavy/armored bosses (golems, knights, titans): Higher HP, lower speed, higher AC
  - Mechanical constructs: Balanced stats with moderate AC
  - Serpents/beasts: High HP pools with moderate all-around stats
  - Stats now properly reflect visual descriptions from bosses_details.md

- **Technical Changes:**
  - All boss IDs updated to match new names (snake_case format)
  - Sprite paths updated to reference correct boss images
  - Maintained existing loot tables and special abilities
  - Preserved behavior flags and drop chances

## v0.2.20 - Mob System Implementation (2025-11-26)
- **Summary:**
  - Added 20 unique mobs with full stats, behaviors, and loot tables
  - Implemented multi-enemy battles (boss + 2 mobs)
  - Added proper mob rendering with correct aspect ratio and positioning
  - Created mobs_data.json for mob definitions
  - Fixed enemy visual styling (red names and HP bars)

- **Mob System:**
  - Created `tunnelsofprivacy/mobs/mobs_data.json` with 20 mob definitions:
    - beetles, blobs, creatures, gnawers, goblins, insects, mites, moths, orbs, rats, spiders, worms
  - Each mob includes: hp, attackDamage, ac, speed, experience
  - Behavior flags: hostile, friendly, canChat, fleeThreshold
  - Loot tables with drop chances and item varieties
  - Special abilities with cooldowns
  - Dialogue for chattable/friendly mobs

- **Multi-Enemy Battles:**
  - Updated platform detection to support 7 platforms (4 heroes + 3 enemies)
  - Boss + 2 mobs spawn in test battles
  - Each enemy positioned on separate platform with spatial separation
  - Fallback layout supports multiple enemies

- **Mob Rendering:**
  - Mobs use 1344x768 sprite dimensions (aspect ratio 1.75:1)
  - Rendered at 4x smaller scale than original (base height ~75px)
  - Feet positioned at ground level (enemy.y = feet position)
  - Hitboxes match sprite dimensions and aspect ratio
  - Depth scaling applies to both sprite and hitbox

- **Enemy Visual Styling:**
  - Enemy names displayed in RED (#FF4444)
  - Enemy HP bars use RED gradient:
    - Healthy (>50%): #E74C3C
    - Medium (25-50%): #C0392B
    - Low (<25%): #A93226
  - HP text remains white for readability
  - Name and HP bar positioned above sprite for both mobs and bosses

- **Mob vs Boss Rendering:**
  - `isMob` flag differentiates rendering logic:
    - Mobs: 1344x768 aspect ratio, feet at enemy.y, smaller scale
    - Bosses: 300x300 square, centered on enemy.y, standard scale
  - Hitboxes adapt to entity type:
    - Mobs: rectangle matching sprite aspect ratio from feet upward
    - Bosses: square centered on position
  - Floor contact point (magenta dot) shows at feet for mobs, bottom of hitbox for bosses

- **Platform Positioning:**
  - Mobs positioned with feet directly at platform center Y
  - Bosses use iterative solver for floor contact at platform center Y
  - All enemies use correct depth scaling

- **Technical Changes:**
  - `generateBattleLayout()` now selects 7 platforms and positions 3 enemies
  - `generateFallbackLayout()` supports multiple enemy positions
  - Enemy sprite rendering checks `isMob` flag for dimension calculations
  - HP bar positioning calculates sprite height to place bars above
  - Hitbox debug rendering adapts to mob vs boss sizing

## v0.2.19 - Depth-Based Rendering & Platform Positioning (2025-11-26)
- **Summary:**
  - Added depth-based scaling for characters based on Y position
  - Fixed platform positioning to place characters at detection box centers
  - Added per-character sprite offset adjustments
  - Implemented depth test for better platform validation
  - Fixed cache clearing to force fresh asset reload

- **Depth-Based Rendering:**
  - Characters scale from 0.6x (top/far) to 1.0x (bottom/near)
  - Scale calculation: `0.6 + (y / canvas.height) * 0.4`
  - Affects sprites, hitboxes, HP bars, and text
  - Creates proper perspective in battle scenes

- **Platform Positioning:**
  - Characters positioned so floor contact point is at detection box center
  - Iterative solver accounts for depth-based hitbox scaling
  - Floor contact point = `character.y + (scaledHitboxSize / 2)`
  - Ensures consistent positioning across all backgrounds

- **Sprite Offsets:**
  - Per-character vertical offset adjustments:
    - Zooko: 10px down
    - Nate: 10px down
    - Zancas: 20px down
    - CyberAxe: 13px down
  - Offsets align character feet with hitbox floor contact

- **Depth Test Validation:**
  - `calculateDepthScore()` traces downward from platforms
  - Measures distance to ground (max 200px trace)
  - Rejects floating platforms (score < 0.5)
  - Scores platforms: 1.0 at ground, 0.5 at 50px+ height
  - Validates continuous support path

- **Cache & Asset Loading:**
  - Clear cache now deletes browser caches via Caches API
  - Forces hard reload with `location.reload(true)`
  - Hero sprites load with timestamp parameter to bypass cache
  - Ensures updated images appear immediately

- **Debug Visualization:**
  - Hitboxes now scale with depth (matching sprite scale)
  - Floor contact point shown as large magenta dot with white outline
  - Center point shown as smaller green/red dot
  - Platform detection boxes remain visible for debugging

- **Technical Changes:**
  - `generateBattleLayout()` uses iterative Y position solver
  - `renderBattle()` calculates `depthScale` for all character elements
  - `clearCache()` clears both localStorage and browser caches
  - All 3 detection methods (`detectByAdaptiveThreshold`, `detectByMultiAngle`, `detectByColorClustering`) now use depth scoring

## v0.2.18 - Spawn Randomization & Background Filtering (2025-11-25)
- **Summary:**
  - Added spawn point randomization for battle variety
  - Removed problematic backgrounds from rotation
  - Each battle now uses different platform combinations

- **Spawn Randomization:**
  - Shuffles detected platforms before selection
  - Different hero/enemy positions each battle
  - Uses `Math.random()` to randomize platform order
  - Maintains spatial separation checks on randomized set

- **Background Updates:**
  - Reduced from 12 to 7 backgrounds in lvl1-10 pool
  - Removed backgrounds with poor platform detection:
    - backgrounds_lvl1 (1, 2, 3, 5, 6, 7, 9, 11, 13, 17, 18, 19)
  - Kept only backgrounds with reliable platform detection:
    - backgrounds_lvl1 (4, 8, 10, 12, 14, 15, 16)

- **Technical Changes:**
  - `generateBattleLayout()` now creates shuffled copy of safe platforms
  - Random sort applied before spatial separation loop
  - Background options array updated to exclude problematic files

## v0.2.17 - Platform Detection Fix (2025-11-25)
- **Summary:**
  - Fixed platform detection system to use discrete box scanning instead of continuous spans
  - Added spatial separation checking to prevent overlapping hero/enemy spawns
  - Added ground verification to prevent floating platform detection
  - Complete rewrite of detection algorithms for better accuracy

- **Platform Detection Fixes:**
  - **Box-Based Scanning:**
    - Changed from 3px line scans to 150x50px box scans
    - Scans discrete boxes instead of continuous horizontal spans
    - Each box independently evaluated for platform viability
    - Prevents detecting long sky/cloud areas as platforms
  
  - **Ground Verification:**
    - Checks 5px below each detected box for darker area
    - Platform must be 20+ brightness units brighter than area below
    - Exception for boxes at bottom edge of image
    - Eliminates floating platform false positives
  
  - **Spatial Separation:**
    - Added minimum 200px distance check between selected platforms
    - Prevents overlapping hero/enemy spawns (300x300px sprites)
    - Iterates through detected platforms to find non-overlapping set
    - Falls back to manual positioning if insufficient platforms found

- **Detection Method Updates:**
  - **Adaptive Threshold:**
    - Box dimensions: 150x50px
    - Step size: 50px horizontal, 25px vertical
    - Scans bottom 60% of image
    - Samples entire box area (every 5px) for brightness
  
  - **Multi-Angle Detection:**
    - Same box dimensions as adaptive
    - Tests 0°, 5°, -5° angles for sloped platforms
    - Step size: 50px horizontal, 30px vertical
    - Ground verification on all detected boxes
  
  - **Color Clustering:**
    - Analyzes 150x50px boxes for color consistency
    - Averages RGB across entire box
    - Step size: 50px horizontal, 25px vertical
    - Ground verification required for all detections

- **Technical Implementation:**
  - `detectByAdaptiveThreshold()` - Complete rewrite with box scanning
  - `detectByMultiAngle()` - Complete rewrite with box scanning
  - `detectByColorClustering()` - Complete rewrite with box scanning
  - `generateBattleLayout()` - Added spatial separation loop
  - Console logging for debugging platform counts

- **Benefits:**
  - No more full-width platform spans that cause overlaps
  - Discrete platform detection matches actual floor regions
  - Ground verification eliminates sky/cloud false positives
  - Spatial checks ensure heroes/enemies spawn in separate locations
  - More reliable platform detection across different backgrounds

## v0.2.11 - Dungeon Menu Screen (2025-11-25)
- **Summary:**
  - Added dungeon menu screen for room-based navigation
  - Hero cards repositioned to four corners
  - New center menu with dungeon options
  - Music controls and ticker now persist across all screens

- **Dungeon Menu Screen:**
  - Click "START ADVENTURE" switches from title to dungeon menu
  - Separate screen state (title screen hidden, dungeon menu shown)
  - Solid background gradient (no animation)
  - Hero cards in corners:
    - Zooko: Top Left
    - Nate: Bottom Left
    - Zancas: Top Right
    - CyberAxe: Bottom Right
  - Same hero card styling as title screen
  - Stats sync between both screens

- **Center Menu Buttons:**
  - **EXPLORER LEVEL** - Enter dungeon exploration (not implemented yet)
  - **ENTER LEVEL STORE** - Shop system (disabled, coming soon)
  - **INVENTORY** - View/manage items (not implemented yet)
  - **REST / SLEEP** - Restore HP/resources (not implemented yet)
  - All buttons styled matching arcade game aesthetic
  - Level display at top of menu

- **Music System Fix:**
  - Moved music controls outside titleScreen container
  - Moved ticker outside titleScreen container
  - Changed from `position: absolute` to `position: fixed`
  - Increased z-index to 500 for proper layering
  - Now visible on both title screen and dungeon menu

- **Technical Implementation:**
  - New `#dungeonMenuScreen` container
  - `.dungeonHeroCard` class for corner positioning
  - `startAdventure()` function switches screens
  - Hero stats use `d` prefix for dungeon screen (e.g., `dzooko-hp`)
  - `updateHeroDisplay()` now updates both title and dungeon screens
  - Dungeon level syncs from arcade save state

- **Next Steps:**
  - Implement pause menu (ESC key)
  - Add functionality to each dungeon menu button
  - Create room-based exploration system

## v0.2.10 - Complete Standardization with Arcade (2025-11-25)
- **Summary:**
  - Complete overhaul to match arcade game systems exactly
  - Added ticker facts educational system
  - Fixed all non-standard naming and structures
  - Full feature parity with arcade's music/ticker system

- **Ticker Facts System (NEW):**
  - Loads `ticker_facts.json` with Zcash/crypto educational facts
  - Displays random fact alongside music info
  - Format: `♫ Theme Song: [name] ♫ • [Random Fact]`
  - Picks new random fact every time track changes
  - Educational content while players browse menu
  - Same ticker facts pool as arcade game

- **Ticker Structure Fixes:**
  - Fixed HTML structure: `#musicTicker` > `#musicTickerWrapper` > `.tickerText` spans
  - Was reversed (wrapper > ticker), now matches arcade exactly
  - Added hover slow-down effect (30s → 60s on hover)
  - Added `pointer-events: auto` to enable hover despite parent blocking
  - Changed animation name from `scroll-left` to `scrollTicker` (arcade standard)
  - Proper seamless scrolling with two identical spans

- **Naming Standardization:**
  - Renamed `dungeonMusicTracks` → `themeTracks` (arcade standard)
  - Renamed `loadDungeonMusic()` → `loadMusic()` (arcade standard)
  - Updated all 6 references to use standard naming
  - Ticker text: "Dungeon Music" → "Theme Song" (arcade standard)
  - Consistent variable/function names across both games

- **Technical Implementation:**
  - Added `tickerFacts` array and `currentTickerFact` variable
  - Fetch `ticker_facts.json` on page load
  - `loadMusic()` picks new random fact from array
  - Combines music info + fact with ` • ` separator
  - Falls back to music-only if facts not loaded
  - Logs fact count to console for debugging

- **Benefits:**
  - Educational: Players learn about Zcash/privacy while browsing
  - Consistency: Same ticker behavior as arcade
  - Engagement: Dynamic content changes with each track
  - Polish: Hover interaction for readability
  - Maintainability: Identical code structure to arcade

## v0.2.9 - Loading Screen & Music Fix (2025-11-25)
- **Summary:**
  - Added complete loading screen system matching arcade
  - Fixed music autoplay to only start from loading screen button
  - Removed title/subtitle text (already in animated background)
  - Complete standalone preload system

- **Loading Screen:**
  - Full modal with progress bar and percentage display
  - Category breakdown: Art (5 images), Sound (optional music)
  - Purple/dungeon theme matching game aesthetic
  - "🎮 CLICK TO ENTER 🎮" prompt when ready
  - Fades out smoothly after user clicks
  - Preloads all assets before allowing play

- **Music System Fix:**
  - Removed global click/keydown event listeners that started music anywhere
  - Music now ONLY starts when clicking loading screen button
  - Respects browser autoplay policies properly
  - No more unwanted music playback on random clicks

- **Visual Polish:**
  - Hidden duplicate title text ("TUNNELS OF PRIVACY" and subtitle)
  - Animated background shows title, no need for overlay text
  - Cleaner title screen presentation

- **Technical Details:**
  - Asset tracking: `assetsToLoad`, `assetsLoaded`, `artTotal`, `artLoaded`, `audioTotal`, `audioLoaded`
  - Progress updates via `updateLoadingProgress()`
  - `checkAllAssetsReady()` shows click prompt when complete
  - Music timeout (3 seconds) prevents hanging on music load
  - Uses `loadedmetadata` event instead of `canplaythrough`

## v0.2.8 - Unified Save System (2025-11-25)
- **Summary:**
  - Load Save File now accepts shared save format from arcade
  - Complete compatibility with arcade save file downloads
  - Added `createDefaultSharedSave()` function for fallback initialization
  - Single unified save format across both games

- **Save File System:**
  - **Load Save File** validates for heroes property (shared save format)
  - Works with save files downloaded from arcade game
  - Supports complete save data: heroes, arcade state, dungeon state
  - Updates hero displays from loaded data
  - Updates dungeon level from arcade state

- **Technical Details:**
  - Added `createDefaultSharedSave()` with default hero stats
  - Matches arcade's hero initialization (str, dex, con, int, wis, cha, hp, maxHp, ac, xp, level)
  - Default heroes: Zooko, Nate, Zancas, CyberAxe
  - Save format includes saveVersion, lastPlayed, arcadeState, dungeonState, heroes

## v0.2.7 - Load Save File Feature (2025-11-25)
- **Summary:**
  - Added Load Save File option to main menu
  - File input panel for uploading save files
  - Validates and imports save data to localStorage

## v0.2.6 - Animated Background & UI Polish (2025-11-25)
- **Summary:**
  - Added animated background matching arcade game
  - Improved menu button layout
  - Enhanced Exit Portal button formatting
  - Complete visual consistency with arcade game

- **Visual Enhancements:**
  - **Animated Background**:
    - Added story intro background animation system
    - Uses same `story/intro/intro_a.png` sprite sheet as arcade (8x16 atlas, 128 frames)
    - 16fps ping-pong animation (forward then backward loop)
    - 30% opacity for subtle atmospheric effect
    - Positioned behind all UI elements (z-index: -1)
    - Starts automatically on page load
  
  - **Menu Button Improvements**:
    - Changed button text alignment from `space-between` to `center`
    - Button labels now properly centered
    - Icons positioned correctly with margins
    - Improved visual balance
  
  - **Exit Portal Button**:
    - Split text into two lines: "EXIT PORTAL" and "(Return to Arcade)"
    - Second line uses smaller font (10px) and lighter weight
    - Better readability and visual hierarchy
    - Maintains centered alignment

- **Technical Implementation:**
  - **Background Animation Functions**:
    - `startStoryIntroAnimation()` - Initializes and runs sprite sheet animation
    - `stopStoryIntroAnimation()` - Cleans up animation interval
    - Calculates frame position in 8-column x 16-row atlas
    - Updates background position every ~62.5ms
    - Ping-pong direction reversal at boundaries (0 and 127)
  
  - **CSS Additions**:
    - `#storyIntroBackground` div with full-screen positioning
    - Background-size calculated from atlas dimensions
    - Smooth 2s opacity transition
    - Proper layering behind title screen

- **Integration:**
  - Animation starts in `init()` function after settings load
  - Shares same sprite sheet asset with arcade game
  - Consistent visual theming across both games
  - Adds atmospheric depth to title screen

---

## v0.2.5 - Music Player UI Enhancement (2025-11-25)
- **Summary:**
  - Updated music player to match arcade game styling exactly
  - Added volume value display
  - Improved layout and centering
  - Added music icon to title

- **UI Improvements:**
  - **Music Controls Title**:
    - Added 🎵 music note icon to title
    - Changed from "Music Controls" to "🎵 Music Controls"
    - Matches arcade game branding
  
  - **Volume Display**:
    - Added real-time volume value display next to slider (e.g., "75")
    - Volume number updates instantly as slider moves
    - Styled with #2D9CDB color, JetBrains Mono font
    - Min-width: 30px, right-aligned for consistency
  
  - **Layout Improvements**:
    - Volume label now centered above slider
    - Slider and value display in flex container with proper alignment
    - Slider max-width: 200px for better proportions
    - Gap spacing matches arcade (8px between slider and value)
    - Proper vertical spacing (12px margin-bottom)

- **Functionality:**
  - `updateVolume()` now updates both slider and display value
  - `loadSettings()` initializes volume display on page load
  - Volume display syncs between main controls and settings panel
  - All volume changes reflected in real-time

- **Visual Consistency:**
  - Matches arcade game's music control layout exactly
  - Same font sizing (10px for labels)
  - Same color scheme (#BFD1E0 for labels, #2D9CDB for values)
  - Consistent spacing and alignment

---

## v0.2.4 - Volume Clamping Fix (2025-11-25)
- **Summary:**
  - Fixed HTMLMediaElement volume errors with proper clamping
  - Volume slider maintains 1-150 range but caps actual volume at 1.0
  - All volume assignments now properly validated

- **Bug Fixes:**
  - **Volume Clamping**:
    - Added `Math.min(1.0, musicVolume / 100)` to all volume assignments
    - Prevents "IndexSizeError: volume outside range [0, 1]" errors
    - Slider still shows 1-150 range for user control
    - Values above 100 are clamped to 1.0 before applying to audio element
  
  - **Fixed Functions**:
    - `updateVolume()` - Main volume slider now clamps correctly
    - `updateSettings()` - Settings panel slider clamps correctly
    - `loadDungeonMusic()` - Initial music load uses clamped volume
    - `fadeMusic()` - Already had proper 0-1 clamping

- **Technical Details:**
  - HTMLMediaElement.volume property only accepts 0.0 to 1.0
  - Slider range 1-150 divided by 100 gives 0.01-1.5
  - Math.min() ensures values never exceed 1.0
  - Maintains arcade game's slider range while respecting browser API limits

---

## v0.2.3 - Settings System Fixes (2025-11-25)
- **Summary:**
  - Fixed volume slider range to match arcade game exactly
  - Corrected HTMLMediaElement volume errors
  - Separated Tunnels settings from arcade settings
  - Improved volume control synchronization

- **Bug Fixes:**
  - **Volume System**:
    - Fixed volume slider range from incorrect 0.01-1.5 to correct 1-150 (matching arcade)
    - Fixed "IndexSizeError: volume outside range [0, 1]" errors
    - Volume now correctly divides by 100 (1-150 → 0.01-1.5) before applying to audio
    - Changed from parseFloat to parseInt for volume values
    - Display shows raw value (75) instead of percentage (75%)
  
  - **Settings Storage**:
    - Changed from shared `top_settings` to independent `top_tunnels_settings`
    - Tunnels now has its own separate settings file
    - Removed misleading "sync with arcade" message
    - Settings no longer conflict with arcade game settings
  
  - **Volume Control Synchronization**:
    - Main volume slider now syncs with settings panel slider
    - Both sliders update each other in real-time
    - Settings panel slider updates when using main controls
    - Volume changes persist to localStorage from both sliders

- **Improvements:**
  - Volume system now identical to arcade game implementation
  - Better error handling for volume clamping in fadeMusic()
  - More reliable settings persistence
  - Independent settings allow different preferences per game

---

## v0.2.2 - Settings System (2025-11-25)
- **Summary:**
  - Added settings panel matching arcade game structure
  - Music settings accessible from title screen
  - Settings persist via localStorage
  - Improved user control over music experience

- **Settings Panel:**
  - **Features**:
    - Music Enabled checkbox (toggle music on/off)
    - Music Volume slider (1-150 scale)
    - Settings modal with overlay dimming
    - Close button with keyboard-friendly icon
    - Version display in panel footer
  
  - **Functionality**:
    - Settings accessible from title screen via SETTINGS button
    - Click overlay to close panel
    - Settings persist to localStorage with "top_" prefix
    - Settings load automatically on page init
    - Volume changes apply immediately to playing music
    - Syncs with main volume slider in music controls
  
  - **Visual Design**:
    - Matches arcade game's panel styling
    - Gradient background with border glow (#2A9D8F)
    - Backdrop blur effect
    - Centered modal positioning
    - Responsive scrolling for smaller screens

- **Integration:**
  - Settings sync between title screen controls and settings panel
  - Music volume updates apply to currentMusic instantly
  - Settings saved to localStorage using STORAGE_KEYS.SETTINGS
  - loadSettings() called during init()
  - Prepared for future dungeon-specific settings

---

## v0.2.1 - Music Control Fixes (2025-11-25)
- **Summary:**
  - Fixed music control functionality bugs
  - Improved stat display error handling
  - Enhanced music playback behavior

- **Bug Fixes:**
  - **Music Controls**:
    - Fixed Play/Pause button not responding correctly
    - Fixed Previous/Next buttons not working
    - Fixed button state not updating properly
    - Next/Previous now auto-enable music if paused and start playing
  
  - **Hero Stats Display**:
    - Added null checks for all stat elements (CON, CHA)
    - Fixed "Cannot set properties of null" error on page load
    - Properly handles missing DOM elements gracefully
  
  - **Music System**:
    - Fixed `musicPlayPause()` function matching HTML button calls
    - Added proper music state tracking with `musicStarted` flag
    - Button text now updates based on actual playback state (▶/⏸)
    - Volume control works without requiring display element

- **Improvements:**
  - Music controls now behave identically to arcade game
  - Clicking Next/Previous while paused will resume playback
  - Better error handling throughout music system
  - More reliable button state synchronization

---

## v0.2.0 - UI Enhancements & Music System (2025-11-25)
- **Summary:**
  - Major UI overhaul with 3-column layout matching arcade game
  - Complete music system with 10 theme tracks
  - Enhanced hero party display with portraits and themed styling
  - Improved visual consistency across both games

- **Layout & UI:**
  - **3-Column Layout**:
    - Left Column: Hero Party cards (2x2 grid)
    - Center Column: Dungeon level display, menu buttons
    - Right Column: Available for future content
  - Changed from centered flexbox to absolute positioning for consistency
  - Matches arcade game's spatial organization

- **Hero Party Improvements:**
  - **Character Portraits**:
    - Circular 60px headshot images for each hero
    - Character-themed colored borders and glows:
      - Zooko: Red (#EB5757)
      - Nate: Yellow (#F2C94C)
      - Zancas: Green (#27AE60)
      - CyberAxe: Blue (#2E86DE)
  
  - **Stat Formatting**:
    - White monospace text (JetBrains Mono, bold)
    - HP displayed in red (#ff6b6b)
    - Two-column stat layout: STR/INT, DEX/WIS, CON/CHA
    - Added CON and CHA stats to complete D&D attribute set
    - Colored card borders matching character themes
    - Glowing box shadows on each card

- **Music System:**
  - **Track List** (10 theme songs):
    - Electric Coin Company
    - Zcash Foundation
    - Proof of Work Battle
    - ZecWallet Lite
    - Private by Default
    - Halo Arc Dreams
    - Mining the Future
    - zkSNARK Symphony
    - Trusted Setup Ceremony
    - Shielded Sunset
  
  - **Music Controls**:
    - Positioned at bottom center (65px from bottom)
    - Three-button layout: Previous, Play/Pause, Next
    - Volume slider (1-150 range)
    - Teal theme (#2A9D8F) with yellow text (#F2C94C)
    - Matches arcade game styling exactly
  
  - **Music Ticker**:
    - Positioned at bottom center (10px from bottom)
    - 600px width, scrolling animation
    - Displays current track name
    - Teal border with yellow text
  
  - **Playback Features**:
    - Random track selection from playlist
    - Automatic progression to next track on song end
    - Smooth 1-second crossfade between tracks
    - Non-blocking audio playback
    - Volume control affects all tracks

- **Visual Consistency:**
  - All UI elements now match arcade game styling:
    - Same fonts (JetBrains Mono for stats/controls)
    - Same color schemes (teal/yellow theme)
    - Same positioning system (absolute coords)
    - Same button styles and hover effects
  - Hero portraits use same compressed headshot images
  - Consistent backdrop blur and shadow effects

- **Technical Details:**
  - Music system functions:
    - `loadDungeonMusic(trackData)`: Load and crossfade tracks
    - `fadeMusic()`: 20-step fade in/out
    - `musicPlayPause()`: Toggle playback
    - `musicPrevious()` / `musicNext()`: Track navigation
    - `updateVolume()`: Volume slider handler
  - CSS Grid for hero party (2x2 layout)
  - Absolute positioning for all major UI sections
  - Responsive width constraints (max-width: 90%)

---

## v0.1.0 - Portal System & Initial Framework (2025-11-24)
- **Summary:**
  - Initial release of Tunnels of Privacy dungeon crawler
  - Portal system integration with ZLOCK CHAINER arcade game
  - Hero party display with shared progression
  - Menu framework ready for future dungeon gameplay

- **Portal System Features:**
  - **Exit Portal Button**: Returns to ZLOCK CHAINER arcade game
    - Purple-themed button with portal emoji (🌀)
    - Saves dungeon state before returning
    - Preserves hero stats and progression
  
  - **Shared Save System**:
    - localStorage key: `top_shared_save`
    - Seamless data sharing with arcade game
    - Version system (v1) for future save migrations
    - Automatic hero stat loading on launch

- **Hero Party Display:**
  - Four playable heroes: Zooko, Nate, Zancas, CyberAxe
  - D&D-style character stats displayed:
    - Level and HP (current/max)
    - STR, DEX, CON, INT, WIS, CHA attributes
  - Real-time stat updates from shared save
  - Stats carry over from arcade game progression

- **Main Menu:**
  - Title screen with purple portal aesthetic
  - Hero party cards showing current stats
  - Exit Portal button for return to arcade
  - Placeholder buttons for future features:
    - Start Adventure (coming soon)
    - Continue (coming soon)

- **Technical Implementation:**
  - Standalone HTML file (no dependencies on arcade game)
  - Separate localStorage namespace with "top_" prefix
  - Portal system functions:
    - `exitPortal()`: Save dungeon state and navigate to arcade
    - `loadSharedSave()`: Load cross-game save data
    - `saveSharedSave()`: Write cross-game save data
    - `migrateSharedSave()`: Version migration support
    - `updateHeroDisplay()`: Refresh hero stat UI
  - Initialization on page load (`init()` function)

- **Save Data Structure:**
  ```javascript
  {
    saveVersion: 1,
    lastPlayed: timestamp,
    arcadeState: { /* arcade game state */ },
    dungeonState: {
      currentLevel: 1,
      inventory: [],
      gold: 0,
      questProgress: {
        hasScepter: false,
        hasReturned: false,
        bossesDefeated: []
      }
    },
    heroes: {
      zooko: { name, str, dex, con, int, wis, cha, hp, maxHp, ac, xp, level },
      nate: { ... },
      zancas: { ... },
      cyberaxe: { ... }
    }
  }
  ```

- **Design Notes:**
  - Based on TI-99's "Tunnels of Doom" classic game
  - Story: Four heroes descend 10 dungeon levels
  - Quest: Find treasure and king's scepter, return to village
  - Shared narrative with ZLOCK CHAINER (story plays on TV screen)

- **Coming Soon (Phase 2):**
  - Dungeon crawler gameplay implementation
  - First-person or top-down dungeon navigation
  - Turn-based or real-time combat system
  - Procedurally generated dungeon levels
  - Inventory and equipment management
  - Merchant and treasure systems
  - Boss encounters on each floor
  - Quest progression tracking
  - Character leveling and stat growth
  - Permadeath or respawn mechanics
  - Sound effects and music
  - Story cutscenes and dialogue

---

**Installation:**
- Runs alongside ZLOCK CHAINER
- Access via "Enter Portal" button in arcade game
- No separate installation required

**System Requirements:**
- Modern web browser with localStorage support
- JavaScript enabled
- Same requirements as ZLOCK CHAINER

**Known Issues:**
- Dungeon gameplay not yet implemented (menu only)
- Hero stats are read-only (no leveling in dungeon yet)
- Inventory system placeholder only

**Credits:**
- Created by CyberAxe
- Part of the ZLOCK CHAINER universe
- Inspired by TI-99's "Tunnels of Doom"
