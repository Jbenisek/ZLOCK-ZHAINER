#!/usr/bin/env python3
"""
ZLOCK Web Server with proper MIME types for GLB files
Fixes binary file serving issues on Linux
Includes WebSocket server for multiplayer co-op
Includes OpenRouter LLM API for NPC chat
"""

import http.server
import socketserver
import mimetypes
import sys
import os
import re
import asyncio
import json
import random
import string
import time
import urllib.request
import urllib.error
import socket
from threading import Thread
from pathlib import Path

# Force IPv4 - fixes 20+ second delays on systems with broken IPv6
original_getaddrinfo = socket.getaddrinfo
def ipv4_only_getaddrinfo(host, port, family=0, type=0, proto=0, flags=0):
    return original_getaddrinfo(host, port, socket.AF_INET, type, proto, flags)
socket.getaddrinfo = ipv4_only_getaddrinfo

# API Keys - loaded from config file or prompted on startup
OPENROUTER_API_KEY = None
GROQ_API_KEY = None
LLM_ENABLED = False

# Config file path (same directory as server)
CONFIG_FILE = Path(__file__).parent / '.zlock_api_keys.json'

def load_api_keys():
    """Load API keys from config file if it exists"""
    global OPENROUTER_API_KEY, GROQ_API_KEY, LLM_ENABLED
    
    if CONFIG_FILE.exists():
        try:
            with open(CONFIG_FILE, 'r') as f:
                config = json.load(f)
                OPENROUTER_API_KEY = config.get('openrouter_api_key', '')
                GROQ_API_KEY = config.get('groq_api_key', '')
                if OPENROUTER_API_KEY or GROQ_API_KEY:
                    LLM_ENABLED = True
                    print(f"✓ Loaded API keys from {CONFIG_FILE.name}")
                    if GROQ_API_KEY:
                        print(f"  • Groq API: {GROQ_API_KEY[:20]}...")
                    if OPENROUTER_API_KEY:
                        print(f"  • OpenRouter API: {OPENROUTER_API_KEY[:20]}...")
                return True
        except Exception as e:
            print(f"⚠️ Error loading config: {e}")
    return False

def save_api_keys():
    """Save API keys to config file"""
    try:
        with open(CONFIG_FILE, 'w') as f:
            json.dump({
                'openrouter_api_key': OPENROUTER_API_KEY or '',
                'groq_api_key': GROQ_API_KEY or ''
            }, f, indent=2)
        print(f"✓ Saved API keys to {CONFIG_FILE.name}")
    except Exception as e:
        print(f"⚠️ Error saving config: {e}")

def prompt_for_api_keys():
    """Prompt user for API keys on startup"""
    global OPENROUTER_API_KEY, GROQ_API_KEY, LLM_ENABLED
    
    print("\n" + "="*60)
    print("🔑 API KEY SETUP")
    print("="*60)
    print("LLM features require API keys for Groq and/or OpenRouter.")
    print("Press Enter to skip (LLM chat will be disabled).")
    print("Keys are saved locally and won't be asked again.\n")
    
    # Groq API Key (free, fast)
    print("GROQ API Key (FREE - get one at console.groq.com):")
    groq_input = input("  > ").strip()
    if groq_input:
        GROQ_API_KEY = groq_input
        LLM_ENABLED = True
    
    # OpenRouter API Key (paid, more models)
    print("\nOpenRouter API Key (PAID - get one at openrouter.ai):")
    openrouter_input = input("  > ").strip()
    if openrouter_input:
        OPENROUTER_API_KEY = openrouter_input
        LLM_ENABLED = True
    
    # Save if any keys provided
    if LLM_ENABLED:
        save_api_keys()
        print("\n✓ LLM Chat ENABLED")
    else:
        print("\n⚠️ No API keys provided - LLM Chat DISABLED")
        print("  Heroes can still chat with each other, but NPCs won't respond.")
    
    print("="*60 + "\n")

def init_api_keys():
    """Initialize API keys - load from file or prompt"""
    if not load_api_keys():
        prompt_for_api_keys()

try:
    import websockets
except ImportError:
    print("⚠️  WARNING: 'websockets' module not installed!")
    print("Run: pip install websockets")
    print("Multiplayer features will be disabled.\n")
    websockets = None

# TTS with Piper - auto-install and setup
TTS_ENABLED = False
PIPER_VOICE_DIR = Path(__file__).parent / 'piper_voices'

# Voice pools for randomization
# Format: (language, speaker_name, quality)
# Each category has multiple voices to pick from randomly

# All available voices to download (verified working)
ALL_VOICES = [
    # British voices
    ('en_GB', 'alba', 'medium'),              # Female, sophisticated
    ('en_GB', 'jenny_dioco', 'medium'),       # Female, clear
    ('en_GB', 'cori', 'medium'),              # Female
    ('en_GB', 'alan', 'medium'),              # Male
    ('en_GB', 'northern_english_male', 'medium'),    # Male, gruff
    ('en_GB', 'aru', 'medium'),               # Male
    # American voices
    ('en_US', 'amy', 'medium'),               # Female
    ('en_US', 'kristin', 'medium'),           # Female
    ('en_US', 'hfc_female', 'medium'),        # Female
    ('en_US', 'ljspeech', 'medium'),          # Female (Linda Johnson)
    ('en_US', 'joe', 'medium'),               # Male, mature
    ('en_US', 'ryan', 'medium'),              # Male, young
    ('en_US', 'bryce', 'medium'),             # Male, deep
    ('en_US', 'hfc_male', 'medium'),          # Male
    ('en_US', 'norman', 'medium'),            # Male
    ('en_US', 'lessac', 'medium'),            # Neutral/androgynous
    ('en_US', 'kusal', 'medium'),             # Male, accented
]

# Voice pools by type - will pick randomly from these
VOICE_POOLS = {
    # Female voices
    'female_mature': [
        ('en_GB', 'alba', 'medium'),
        ('en_GB', 'jenny_dioco', 'medium'),
        ('en_US', 'hfc_female', 'medium'),
    ],
    'female_young': [
        ('en_US', 'kristin', 'medium'),
        ('en_US', 'amy', 'medium'),
        ('en_GB', 'cori', 'medium'),
        ('en_US', 'ljspeech', 'medium'),
    ],
    # Male voices  
    'male_deep': [
        ('en_US', 'bryce', 'medium'),
        ('en_GB', 'northern_english_male', 'medium'),
        ('en_US', 'norman', 'medium'),
    ],
    'male_young': [
        ('en_US', 'ryan', 'medium'),
        ('en_GB', 'aru', 'medium'),
        ('en_US', 'kusal', 'medium'),
    ],
    'male_mature': [
        ('en_US', 'joe', 'medium'),
        ('en_GB', 'alan', 'medium'),
        ('en_US', 'kusal', 'medium'),
    ],
    # Special types
    'monster': [
        ('en_US', 'hfc_male', 'medium'),
        ('en_GB', 'northern_english_male', 'medium'),
        ('en_US', 'norman', 'medium'),
    ],
    'ethereal': [
        ('en_US', 'lessac', 'medium'),
        ('en_US', 'ljspeech', 'medium'),
        ('en_GB', 'alba', 'medium'),
    ],
}

# Fixed voice assignments (not randomized)
VOICE_ASSIGNMENTS = {
    # Narrator - always British female (sexy sophisticated)
    'narrator': ('en_GB', 'alba', 'medium'),
    # Heroes - fixed voices for consistency
    'zooko': ('en_US', 'joe', 'medium'),
    'nate': ('en_US', 'ryan', 'medium'),
    'zancas': ('en_US', 'kristin', 'medium'),
    'cyberaxe': ('en_US', 'bryce', 'medium'),
    # Entity type fallbacks (if LLM doesn't specify voiceType)
    'boss': ('en_US', 'bryce', 'medium'),  # Deep male voice for bosses
    'mob': ('en_US', 'hfc_male', 'medium'),
    'captive': ('en_US', 'amy', 'medium'),
    'npc': ('en_US', 'lessac', 'medium'),
    'default': ('en_US', 'lessac', 'medium'),
}

# Speech synthesis parameters per voice type
# length_scale: <1 = faster, >1 = slower
# noise_scale: higher = more expressive/emotional variation
# noise_w_scale: phoneme duration variation (rhythm)
VOICE_PARAMS = {
    # Narrator - smooth, measured, slightly slow for clarity
    'narrator': {'length_scale': 1.2, 'noise_scale': 0.55, 'noise_w_scale': 0.75},
    
    # Heroes - each with distinct speech patterns (slowed down for clarity)
    'zooko': {'length_scale': 1.1, 'noise_scale': 0.65, 'noise_w_scale': 0.85},      # Calm, wise
    'nate': {'length_scale': 1.0, 'noise_scale': 0.75, 'noise_w_scale': 0.9},        # Quick, energetic
    'zancas': {'length_scale': 1.05, 'noise_scale': 0.7, 'noise_w_scale': 0.85},     # Confident, sharp
    'cyberaxe': {'length_scale': 1.15, 'noise_scale': 0.6, 'noise_w_scale': 0.8},    # Steady, deliberate
    
    # Voice type pools - character archetypes
    'female_mature': {'length_scale': 1.1, 'noise_scale': 0.65, 'noise_w_scale': 0.85},
    'female_young': {'length_scale': 1.02, 'noise_scale': 0.75, 'noise_w_scale': 0.9},
    'male_deep': {'length_scale': 1.05, 'noise_scale': 0.85, 'noise_w_scale': 0.95},    # Rougher, commanding
    'male_young': {'length_scale': 1.0, 'noise_scale': 0.75, 'noise_w_scale': 0.85},
    'male_mature': {'length_scale': 1.1, 'noise_scale': 0.8, 'noise_w_scale': 0.9},     # Gruff, weathered
    
    # Entity types - dramatic characterization
    'boss': {'length_scale': 1.1, 'noise_scale': 0.9, 'noise_w_scale': 1.0},        # Rough, aggressive, intimidating
    'mob': {'length_scale': 1.05, 'noise_scale': 0.7, 'noise_w_scale': 0.85},       # Generic enemy
    'monster': {'length_scale': 1.0, 'noise_scale': 1.0, 'noise_w_scale': 1.1},     # Growly, rough
    'captive': {'length_scale': 0.95, 'noise_scale': 0.85, 'noise_w_scale': 1.0},   # Nervous, shaky (still a bit fast)
    'ethereal': {'length_scale': 1.4, 'noise_scale': 0.45, 'noise_w_scale': 0.65},  # Slow, dreamy, smooth
    'npc': {'length_scale': 1.1, 'noise_scale': 0.65, 'noise_w_scale': 0.85},       # Normal
    
    # Default fallback
    'default': {'length_scale': 1.1, 'noise_scale': 0.667, 'noise_w_scale': 0.85},
}

# Cache for entity voice assignments
# Maps entity_id -> (language, speaker, quality) tuple
# This ensures the same entity always uses the same voice within a session
ENTITY_VOICE_CACHE = {}

def ensure_piper_installed():
    """Install piper-tts if not already installed"""
    global TTS_ENABLED
    
    try:
        import piper
        print("✓ piper-tts is installed")
        TTS_ENABLED = True
        return True
    except ImportError:
        print("\n📦 Installing piper-tts (first-time setup)...")
        import subprocess
        try:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'piper-tts', '-q'])
            print("✓ piper-tts installed successfully")
            TTS_ENABLED = True
            return True
        except subprocess.CalledProcessError as e:
            print(f"⚠️ Failed to install piper-tts: {e}")
            print("  TTS features will be disabled.")
            return False

def get_voice_model_path(language, speaker, quality):
    """Get path to voice model files (.onnx and .onnx.json)"""
    # Piper voice naming: en_GB-alba-medium.onnx
    model_name = f"{language}-{speaker}-{quality}"
    model_path = PIPER_VOICE_DIR / f"{model_name}.onnx"
    config_path = PIPER_VOICE_DIR / f"{model_name}.onnx.json"
    return model_path, config_path, model_name

def download_voice_model(language, speaker, quality):
    """Download voice model from HuggingFace if not present"""
    model_path, config_path, model_name = get_voice_model_path(language, speaker, quality)
    
    if model_path.exists() and config_path.exists():
        return True  # Already downloaded
    
    # Create voice directory if needed
    PIPER_VOICE_DIR.mkdir(exist_ok=True)
    
    # HuggingFace URL pattern for piper voices
    # Example: https://huggingface.co/rhasspy/piper-voices/resolve/main/en/en_GB/alba/medium/en_GB-alba-medium.onnx
    lang_region = language.split('_')[0]  # en_GB -> en
    base_url = f"https://huggingface.co/rhasspy/piper-voices/resolve/main/{lang_region}/{language}/{speaker}/{quality}"
    
    print(f"  📥 Downloading {model_name}...")
    
    try:
        # Download .onnx model
        onnx_url = f"{base_url}/{model_name}.onnx"
        urllib.request.urlretrieve(onnx_url, model_path)
        
        # Download .onnx.json config
        json_url = f"{base_url}/{model_name}.onnx.json"
        urllib.request.urlretrieve(json_url, config_path)
        
        print(f"  ✓ Downloaded {model_name}")
        return True
    except Exception as e:
        print(f"  ⚠️ Failed to download {model_name}: {e}")
        return False

def ensure_voice_models():
    """Download all required voice models"""
    if not TTS_ENABLED:
        return False
    
    print("\n🎤 Checking TTS voice models...")
    print(f"   (20 voices for variety - ~200MB total on first run)")
    
    # Download ALL voices for maximum variety
    all_success = True
    
    for language, speaker, quality in ALL_VOICES:
        model_path, config_path, model_name = get_voice_model_path(language, speaker, quality)
        
        if model_path.exists() and config_path.exists():
            print(f"  ✓ {model_name} (already downloaded)")
        else:
            if not download_voice_model(language, speaker, quality):
                all_success = False
    
    return all_success

def init_tts():
    """Initialize TTS system - install piper and download voices"""
    global TTS_ENABLED
    
    print("\n" + "="*60)
    print("🔊 TTS SETUP (Piper Neural TTS)")
    print("="*60)
    
    if ensure_piper_installed():
        ensure_voice_models()
        if TTS_ENABLED:
            print("✓ TTS system ready\n")
    else:
        print("⚠️ TTS disabled - piper-tts not available\n")

PORT = 4243
WS_PORT = 8765

# Add proper MIME types for game assets
mimetypes.add_type('model/gltf-binary', '.glb')
mimetypes.add_type('model/gltf+json', '.gltf')
mimetypes.add_type('application/json', '.json')
mimetypes.add_type('audio/mpeg', '.mp3')
mimetypes.add_type('audio/wav', '.wav')
mimetypes.add_type('audio/ogg', '.ogg')
mimetypes.add_type('video/mp4', '.mp4')
mimetypes.add_type('image/png', '.png')
mimetypes.add_type('image/jpeg', '.jpg')
mimetypes.add_type('image/jpeg', '.jpeg')

class GameHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    """Custom handler with proper binary file support"""
    
    # Increase timeout for large file transfers (videos)
    timeout = 300  # 5 minutes instead of default 60 seconds
    
    def end_headers(self):
        # Add CORS headers for cross-origin requests
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        
        # Enable aggressive caching for large static assets (models, videos, audio)
        # HTML files: no cache (for development iteration)
        if self.path.endswith('.html'):
            self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate')
        # Large binary assets: cache for 24 hours (browser stores in memory/disk)
        elif self.path.endswith(('.glb', '.gltf', '.mp4', '.mp3', '.wav', '.ogg', '.png', '.jpg', '.jpeg')):
            self.send_header('Cache-Control', 'public, max-age=86400')  # 24 hours cache
            self.send_header('Expires', 'Thu, 31 Dec 2026 23:59:59 GMT')  # Far future expiry
        else:
            self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate')
        
        super().end_headers()
    
    def guess_type(self, path):
        """Override to ensure proper binary MIME types"""
        mimetype, encoding = mimetypes.guess_type(path)
        
        # Force binary for GLB files
        if path.endswith('.glb'):
            return 'model/gltf-binary'
        # Force video/mp4 for MP4 files
        elif path.endswith('.mp4'):
            return 'video/mp4'
        
        return mimetype or 'application/octet-stream'
    
    def do_OPTIONS(self):
        """Handle CORS preflight requests"""
        self.send_response(200)
        self.end_headers()
    
    def do_POST(self):
        """Handle POST requests for chat API"""
        if self.path == '/api/chat':
            return self.handle_chat_api()
        elif self.path == '/api/generate-encounter':
            return self.handle_generate_encounter()
        elif self.path == '/api/llm-status':
            return self.handle_llm_status()
        elif self.path == '/api/tts':
            return self.handle_tts()
        elif self.path == '/api/tts-status':
            return self.handle_tts_status()
        elif self.path == '/api/tts/clear-voice-cache':
            return self.handle_clear_voice_cache()
        else:
            self.send_error(404, "Not found")
    
    def handle_clear_voice_cache(self):
        """Clear the entity voice cache (called when leaving a room)"""
        global ENTITY_VOICE_CACHE
        count = len(ENTITY_VOICE_CACHE)
        ENTITY_VOICE_CACHE = {}
        print(f"[TTS] Voice cache cleared ({count} entries)")
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps({
            'success': True,
            'cleared': count
        }).encode('utf-8'))
    
    def handle_tts_status(self):
        """Return TTS availability status"""
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps({
            'enabled': TTS_ENABLED,
            'fixedVoices': list(VOICE_ASSIGNMENTS.keys()),
            'voicePools': list(VOICE_POOLS.keys()),
            'totalVoices': len(ALL_VOICES)
        }).encode('utf-8'))
    
    def handle_tts(self):
        """Generate speech audio from text using Piper TTS"""
        if not TTS_ENABLED:
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({
                'success': False,
                'error': 'TTS disabled - piper-tts not installed',
                'ttsDisabled': True
            }).encode('utf-8'))
            return
        
        try:
            import io
            import wave
            import re
            from piper import PiperVoice
            from piper.config import SynthesisConfig
            
            # Read request body
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length)
            data = json.loads(body.decode('utf-8'))
            
            text = data.get('text', '')
            voice_type = data.get('voiceType', 'default').lower()  # narrator, hero name, boss, mob, etc.
            personality = data.get('personality', '').lower()  # emotional context from NPC
            entity_id = data.get('entityId', None)  # Unique ID to maintain voice consistency
            
            # Strip asterisk actions like *laughs menacingly* from text
            # These are roleplay actions that shouldn't be read literally
            text = re.sub(r'\*[^*]+\*', '', text).strip()
            
            # === TEXT PREPROCESSING FOR NATURAL SPEECH ===
            # Add breathing pauses and natural rhythm
            
            # Normalize multiple spaces
            text = re.sub(r'\s+', ' ', text)
            
            # Add pause after sentences (period followed by space)
            # Using comma + space creates a natural breath pause
            text = re.sub(r'\.\s+', '... ', text)
            
            # Add slight pause after exclamations and questions
            text = re.sub(r'!\s+', '!.. ', text)
            text = re.sub(r'\?\s+', '?.. ', text)
            
            # Add pause after colons (before explanations)
            text = re.sub(r':\s+', ':.. ', text)
            
            # Add micro-pause after commas if not already present
            text = re.sub(r',\s*(?!\.)', ', ', text)
            
            # Handle ellipsis - ensure proper spacing
            text = re.sub(r'\.{3,}', '... ', text)
            
            # Add pause before dramatic words (when preceded by space)
            dramatic_words = ['but', 'however', 'yet', 'now', 'then', 'suddenly', 'finally', 'alas', 'behold']
            for word in dramatic_words:
                text = re.sub(rf'\s+({word})\b', rf', \1', text, flags=re.IGNORECASE)
            
            # Clean up any double commas or spaces we created
            text = re.sub(r',\s*,', ',', text)
            text = re.sub(r'\s+', ' ', text)
            text = text.strip()
            
            if not text:
                self.send_response(400)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({
                    'success': False,
                    'error': 'No text provided (or text was all actions)'
                }).encode('utf-8'))
                return
            
            # Get voice configuration - use cached voice for entities, or pick new one
            voice_config = None
            
            # If entity has ID, check cache for consistent voice
            if entity_id and entity_id in ENTITY_VOICE_CACHE:
                voice_config = ENTITY_VOICE_CACHE[entity_id]
                print(f"[TTS] Using cached voice for entity '{entity_id}'")
            
            # No cached voice - pick one
            if voice_config is None:
                if voice_type in VOICE_POOLS:
                    # Random selection from pool for variety
                    voice_config = random.choice(VOICE_POOLS[voice_type])
                    # Cache it if entity has ID
                    if entity_id:
                        ENTITY_VOICE_CACHE[entity_id] = voice_config
                        print(f"[TTS] Assigned new voice to entity '{entity_id}': {voice_config}")
                elif voice_type in VOICE_ASSIGNMENTS:
                    voice_config = VOICE_ASSIGNMENTS[voice_type]
                else:
                    voice_config = VOICE_ASSIGNMENTS['default']
            
            language, speaker, quality = voice_config
            
            model_path, config_path, model_name = get_voice_model_path(language, speaker, quality)
            
            # Check if model exists
            if not model_path.exists():
                # Try to download it
                if not download_voice_model(language, speaker, quality):
                    self.send_response(500)
                    self.send_header('Content-Type', 'application/json')
                    self.end_headers()
                    self.wfile.write(json.dumps({
                        'success': False,
                        'error': f'Voice model {model_name} not available'
                    }).encode('utf-8'))
                    return
            
            # Generate speech
            print(f"[TTS] Generating speech for '{text[:50]}...' using {model_name} ({voice_type})")
            
            voice = PiperVoice.load(str(model_path), str(config_path))
            
            # Get voice parameters for this voice type
            params = VOICE_PARAMS.get(voice_type, VOICE_PARAMS['default']).copy()
            
            # === DYNAMIC PERSONALITY ADJUSTMENTS ===
            # Modify voice params based on emotional context from NPC personality
            if personality:
                # Aggressive/angry = faster, more expressive
                if any(word in personality for word in ['aggressive', 'angry', 'hostile', 'furious', 'rage', 'violent']):
                    params['length_scale'] = params.get('length_scale', 1.0) * 0.9
                    params['noise_scale'] = min(1.0, params.get('noise_scale', 0.667) * 1.2)
                
                # Calm/wise/thoughtful = slower, more measured
                elif any(word in personality for word in ['calm', 'wise', 'thoughtful', 'contemplative', 'serene', 'patient']):
                    params['length_scale'] = params.get('length_scale', 1.0) * 1.15
                    params['noise_scale'] = params.get('noise_scale', 0.667) * 0.85
                
                # Nervous/scared = faster, more varied rhythm
                elif any(word in personality for word in ['nervous', 'scared', 'anxious', 'fearful', 'timid', 'coward']):
                    params['length_scale'] = params.get('length_scale', 1.0) * 0.92
                    params['noise_w_scale'] = min(1.2, params.get('noise_w_scale', 0.8) * 1.15)
                
                # Cunning/sly = moderate pace, expressive
                elif any(word in personality for word in ['cunning', 'sly', 'devious', 'scheming', 'manipulative']):
                    params['length_scale'] = params.get('length_scale', 1.0) * 1.05
                    params['noise_scale'] = min(1.0, params.get('noise_scale', 0.667) * 1.1)
                
                # Sad/melancholy = slower, less expressive
                elif any(word in personality for word in ['sad', 'melancholy', 'tragic', 'mournful', 'depressed']):
                    params['length_scale'] = params.get('length_scale', 1.0) * 1.2
                    params['noise_scale'] = params.get('noise_scale', 0.667) * 0.8
                
                # Excited/energetic = faster
                elif any(word in personality for word in ['excited', 'energetic', 'manic', 'enthusiastic', 'hyper']):
                    params['length_scale'] = params.get('length_scale', 1.0) * 0.88
            
            # Create synthesis config with character-specific parameters
            syn_config = SynthesisConfig(
                length_scale=params.get('length_scale', 1.0),
                noise_scale=params.get('noise_scale', 0.667),
                noise_w_scale=params.get('noise_w_scale', 0.8)
            )
            
            # Generate audio to WAV bytes using the custom config
            audio_bytes = io.BytesIO()
            with wave.open(audio_bytes, 'wb') as wav_file:
                # Use synthesize() with config, then write to WAV
                wav_file.setnchannels(1)
                wav_file.setsampwidth(2)  # 16-bit
                wav_file.setframerate(voice.config.sample_rate)
                for audio_chunk in voice.synthesize(text, syn_config):
                    wav_file.writeframes(audio_chunk.audio_int16_bytes)
            
            audio_data = audio_bytes.getvalue()
            
            # Send WAV audio response
            self.send_response(200)
            self.send_header('Content-Type', 'audio/wav')
            self.send_header('Content-Length', str(len(audio_data)))
            self.end_headers()
            self.wfile.write(audio_data)
            
            print(f"[TTS] Generated {len(audio_data)} bytes of audio")
            
        except Exception as e:
            print(f"[TTS] Error: {e}")
            import traceback
            traceback.print_exc()
            self.send_response(500)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({
                'success': False,
                'error': str(e)
            }).encode('utf-8'))
    
    def handle_llm_status(self):
        """Return LLM availability status"""
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps({
            'enabled': LLM_ENABLED,
            'hasGroq': bool(GROQ_API_KEY),
            'hasOpenRouter': bool(OPENROUTER_API_KEY)
        }).encode('utf-8'))
    
    def handle_chat_api(self):
        """Handle chat API request - Groq (1-5) or OpenRouter (6-10)"""
        
        # Check if LLM is enabled
        if not LLM_ENABLED:
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({
                'success': False,
                'error': 'LLM disabled - no API keys configured',
                'llmDisabled': True
            }).encode('utf-8'))
            return
        
        # Models 1-5: Groq (FAST), Models 6-9: OpenRouter
        # Exception: Model 1 is OpenRouter Mistral Nemo for comparison
        MODEL_OPTIONS = {
            # OpenRouter (for comparison)
            1: ('openrouter', 'mistralai/mistral-nemo'),   # Mistral Nemo - OpenRouter
            # Groq models (fast)
            2: ('groq', 'llama-3.1-8b-instant'),           # Llama 3.1 8B - fastest
            3: ('groq', 'llama-3.3-70b-versatile'),        # Llama 3.3 70B - smartest
            4: ('groq', 'gemma2-9b-it'),                   # Gemma 2 9B
            5: ('groq', 'mixtral-8x7b-32768'),             # Mixtral 8x7B
            # OpenRouter models
            6: ('openrouter', 'meta-llama/llama-3.1-8b-instruct'),  # Llama 3.1 8B
            7: ('openrouter', 'google/gemma-2-9b-it'),     # Gemma 2 9B
            8: ('openrouter', 'qwen/qwen2.5-coder-7b-instruct'),    # Qwen 2.5 7B
            9: ('openrouter', 'sao10k/l3-lunaris-8b')      # L3 Lunaris 8B
        }
        
        # Costs per million tokens (input, output)
        MODEL_COSTS = {
            1: (0.02, 0.04),    # Mistral Nemo
            2: (0.05, 0.08),    # Llama 3.1 8B
            3: (0.59, 0.79),    # Llama 3.3 70B
            4: (0.20, 0.20),    # Gemma 2 9B
            5: (0.24, 0.24),    # Mixtral 8x7B
            6: (0.02, 0.03),    # Llama 3.1 8B
            7: (0.03, 0.09),    # Gemma 2 9B
            8: (0.03, 0.09),    # Qwen 2.5 7B
            9: (0.04, 0.05)     # L3 Lunaris 8B
        }
        
        try:
            # Read request body
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length)
            data = json.loads(body.decode('utf-8'))
            
            npc_name = data.get('npcName', 'Unknown')
            npc_backstory = data.get('backstory', '')
            npc_type = data.get('npcType', 'mob')  # mob, boss, npc
            conversation = data.get('conversation', [])  # Previous messages
            player_message = data.get('message', '')
            player_name = data.get('playerName', 'Hero')
            model_id = data.get('modelId', 1)  # Default to model 1
            rp_mode = data.get('rpMode', True)  # RP emotes vs normal speech
            
            # Get selected model (provider, model_name)
            provider, selected_model = MODEL_OPTIONS.get(model_id, MODEL_OPTIONS[1])
            print(f"[Chat API] Using {provider} model {model_id}: {selected_model} | RP Mode: {rp_mode}")
            
            import time
            timing = {}
            t_start = time.time()
            
            # Build system prompt based on RP mode
            if rp_mode:
                # Classic RPG style with emotes and dramatic speech
                system_prompt = f"""You are {npc_name}, a {npc_type} in a dungeon crawler RPG called 'Tunnels of Privacy'.

Backstory: {npc_backstory}

You are in combat with a party of heroes. Stay in character. Keep responses SHORT (1-3 sentences max). Be dramatic but concise. You can be hostile, friendly, or neutral based on your nature.

Use *emotes* to express actions like *laughs maniacally* or *snarls* or *shifts nervously*. Speak in a dramatic fantasy RPG style.

If you have nothing interesting to say or don't want to talk, respond with just: *silence* or *growls*

Do not break character. Do not mention being an AI."""
            else:
                # Modern conversational style - like talking to a person in 2025
                system_prompt = f"""You are {npc_name}, a character in a dungeon crawler game called 'Tunnels of Privacy'.

Background info: {npc_backstory}

Talk like a normal person in 2025 would - casual, direct, no medieval speech patterns. Keep it SHORT (1-3 sentences). You can be hostile, friendly, sarcastic, whatever fits your personality - just talk normally.

NO asterisk emotes like *laughs*. NO dramatic fantasy speak. Just natural conversation like you'd text someone.

Examples of good responses:
- "Nah, I'm good. You can leave now."
- "Look man, I don't want trouble. Just passing through."
- "You think you can just walk in here? That's cute."
- "Whatever. I've got better things to do than fight."

If you don't want to talk, just say something short like "..." or "Go away."

Don't mention being an AI."""
            
            # Build messages array
            messages = [{'role': 'system', 'content': system_prompt}]
            
            # Add conversation history
            for msg in conversation[-10:]:  # Last 10 messages for context
                role = 'assistant' if msg.get('isNpc') else 'user'
                messages.append({'role': role, 'content': msg.get('text', '')})
            
            # Add current message
            messages.append({'role': 'user', 'content': f"{player_name}: {player_message}"})
            
            timing['build_request'] = time.time() - t_start
            t_api_start = time.time()
            
            # Build API request
            api_request = {
                'model': selected_model,
                'messages': messages,
                'max_tokens': 150,
                'temperature': 0.8
            }
            
            # BUILD FAILOVER MODEL LIST
            # If user selected a Groq model (2-5), failover to other Groq then OpenRouter
            # If user selected OpenRouter (1, 6-9), failover to other OR then Groq
            GROQ_MODELS = [
                (2, 'groq', 'llama-3.1-8b-instant'),
                (3, 'groq', 'llama-3.3-70b-versatile'),
                (4, 'groq', 'gemma2-9b-it'),
                (5, 'groq', 'mixtral-8x7b-32768'),
            ]
            OPENROUTER_MODELS = [
                (1, 'openrouter', 'mistralai/mistral-nemo'),
                (6, 'openrouter', 'meta-llama/llama-3.1-8b-instruct'),
                (7, 'openrouter', 'google/gemma-2-9b-it'),
                (8, 'openrouter', 'qwen/qwen2.5-coder-7b-instruct'),
                (9, 'openrouter', 'sao10k/l3-lunaris-8b'),
            ]
            
            # Start with selected model, then add failovers
            if provider == 'groq':
                # Groq first (filter out current), then OpenRouter
                failover_list = [(model_id, provider, selected_model)]
                failover_list += [(mid, p, m) for mid, p, m in GROQ_MODELS if mid != model_id and GROQ_API_KEY]
                failover_list += [(mid, p, m) for mid, p, m in OPENROUTER_MODELS if OPENROUTER_API_KEY]
            else:
                # OpenRouter first (filter out current), then Groq
                failover_list = [(model_id, provider, selected_model)]
                failover_list += [(mid, p, m) for mid, p, m in OPENROUTER_MODELS if mid != model_id and OPENROUTER_API_KEY]
                failover_list += [(mid, p, m) for mid, p, m in GROQ_MODELS if GROQ_API_KEY]
            
            # FAILOVER LOGIC
            npc_response = None
            last_error = None
            actual_model_id = model_id
            models_tried = []
            
            timing['build_http'] = time.time() - t_api_start
            t_network_start = time.time()
            
            for current_model_id, current_provider, current_model in failover_list:
                models_tried.append(f"{current_provider}/{current_model}")
                api_request['model'] = current_model
                
                # Set API URL and headers
                if current_provider == 'groq':
                    api_url = 'https://api.groq.com/openai/v1/chat/completions'
                    headers = {
                        'Content-Type': 'application/json',
                        'Authorization': f'Bearer {GROQ_API_KEY}'
                    }
                else:
                    api_url = 'https://openrouter.ai/api/v1/chat/completions'
                    headers = {
                        'Content-Type': 'application/json',
                        'Authorization': f'Bearer {OPENROUTER_API_KEY}',
                        'HTTP-Referer': 'http://localhost:4243',
                        'X-Title': 'Tunnels of Privacy'
                    }
                
                req = urllib.request.Request(
                    api_url,
                    data=json.dumps(api_request).encode('utf-8'),
                    headers=headers
                )
                
                try:
                    print(f"[Chat API] Trying {current_provider}/{current_model}")
                    with urllib.request.urlopen(req, timeout=60) as response:
                        result = json.loads(response.read().decode('utf-8'))
                        npc_response = result['choices'][0]['message']['content']
                        actual_model_id = current_model_id
                        
                        # Extract token usage
                        usage = result.get('usage', {})
                        prompt_tokens = usage.get('prompt_tokens', 0)
                        completion_tokens = usage.get('completion_tokens', 0)
                        
                        print(f"[Chat API] Success with {current_provider}/{current_model}")
                        break  # Success
                        
                except urllib.error.HTTPError as http_err:
                    last_error = http_err
                    error_body = ''
                    try:
                        error_body = http_err.read().decode('utf-8')
                    except:
                        pass
                    
                    if http_err.code == 429:
                        print(f"[Chat API] Rate limited (429) on {current_provider}/{current_model}, trying next...")
                        continue  # Try next model
                    elif http_err.code == 402:
                        print(f"[Chat API] Payment required (402) on {current_provider}/{current_model}, trying next...")
                        continue
                    else:
                        print(f"[Chat API] Error ({http_err.code}) on {current_provider}/{current_model}: {error_body[:100]}")
                        continue  # Try next model
                except Exception as e:
                    last_error = e
                    print(f"[Chat API] Exception on {current_provider}/{current_model}: {str(e)[:100]}")
                    continue
            
            # Check if we got a response
            if not npc_response:
                print(f"[Chat API] All models exhausted. Tried: {', '.join(models_tried)}")
                raise last_error if last_error else Exception(f"All models failed")
            
            timing['network_wait'] = time.time() - t_network_start
            t_parse_start = time.time()
            
            # Calculate cost
            input_cost_per_m, output_cost_per_m = MODEL_COSTS.get(actual_model_id, (0, 0))
            cost = (prompt_tokens * input_cost_per_m / 1000000) + (completion_tokens * output_cost_per_m / 1000000)
            
            timing['parse_response'] = time.time() - t_parse_start
            timing['total'] = time.time() - t_start
                
            # Print timing breakdown
            print(f"[Chat API] TIMING: build_req={timing['build_request']:.3f}s | build_http={timing['build_http']:.3f}s | NETWORK={timing['network_wait']:.2f}s | parse={timing['parse_response']:.3f}s | TOTAL={timing['total']:.2f}s")
            
            # Send response
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({
                'success': True,
                'response': npc_response,
                'npcName': npc_name,
                'usage': {
                    'promptTokens': prompt_tokens,
                    'completionTokens': completion_tokens,
                    'cost': cost
                },
                'timing': {
                    'networkWait': round(timing['network_wait'], 2),
                    'total': round(timing['total'], 2)
                }
            }).encode('utf-8'))
            
        except urllib.error.HTTPError as e:
            error_body = e.read().decode('utf-8') if e.fp else str(e)
            print(f"[Chat API] OpenRouter error: {e.code} - {error_body}")
            self.send_response(500)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({
                'success': False,
                'error': f'OpenRouter API error: {e.code}'
            }).encode('utf-8'))
            
        except Exception as e:
            print(f"[Chat API] Error: {e}")
            self.send_response(500)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({
                'success': False,
                'error': str(e)
            }).encode('utf-8'))
    
    def handle_generate_encounter(self):
        """Dungeon Master LLM generates unique encounter data"""
        
        # Check if LLM is enabled
        if not LLM_ENABLED:
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({
                'success': False,
                'error': 'LLM disabled - no API keys configured',
                'llmDisabled': True
            }).encode('utf-8'))
            return
        
        try:
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length)
            data = json.loads(body.decode('utf-8'))
            
            encounter_type = data.get('type', 'boss')  # boss, mob, npc, captive
            base_data = data.get('baseData', {})  # Original JSON data as template
            room_level = data.get('roomLevel', 1)
            use_free_model = data.get('useFreeModel', True)  # Client preference
            
            # MODEL POOLS FOR FAILOVER
            # Free models (Groq) - fast, generous limits
            FREE_MODELS = [
                ('groq', 'llama-3.1-8b-instant'),      # Fastest
                ('groq', 'llama-3.3-70b-versatile'),   # Smartest
                ('groq', 'gemma2-9b-it'),              # Backup
                ('groq', 'mixtral-8x7b-32768'),        # Backup
            ]
            
            # Paid models (OpenRouter) - better quality, ordered by speed/quality
            PAID_MODELS = [
                ('openrouter', 'anthropic/claude-3-haiku'),          # Fast Claude - best balance
                ('openrouter', 'meta-llama/llama-3.1-70b-instruct'), # Smart & reasonably fast
                ('openrouter', 'google/gemma-2-9b-it'),              # Cheap backup
                ('openrouter', 'mistralai/mistral-nemo'),            # Free tier on OR (slow)
            ]
            
            # Build model list based on preference with failover
            if use_free_model:
                # Free first, then paid as fallback
                model_list = [(p, m) for p, m in FREE_MODELS if (p == 'groq' and GROQ_API_KEY) or (p == 'openrouter' and OPENROUTER_API_KEY)]
                model_list += [(p, m) for p, m in PAID_MODELS if (p == 'groq' and GROQ_API_KEY) or (p == 'openrouter' and OPENROUTER_API_KEY)]
            else:
                # Paid first, then free as fallback
                model_list = [(p, m) for p, m in PAID_MODELS if (p == 'groq' and GROQ_API_KEY) or (p == 'openrouter' and OPENROUTER_API_KEY)]
                model_list += [(p, m) for p, m in FREE_MODELS if (p == 'groq' and GROQ_API_KEY) or (p == 'openrouter' and OPENROUTER_API_KEY)]
            
            if not model_list:
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({
                    'success': False,
                    'error': 'No API keys available',
                    'llmDisabled': True
                }).encode('utf-8'))
                return
            
            # Start with first model in list
            provider, model = model_list[0]
            print(f"[DM API] Generating {encounter_type} for level {room_level} using {provider}/{model} (free={use_free_model})")
            
            # World lore for context
            world_lore = """
TUNNELS OF PRIVACY - World Lore:
The Tunnels of Privacy are ancient underground passages beneath a world where personal data has become currency. 
Privacy is a treasure, and those who steal it become corrupted monsters. The heroes (Zooko, Nate, Zancas, CyberAxe) 
fight to protect people's right to financial privacy using Zcash cryptocurrency and zero-knowledge proofs.

Enemies are often manifestations of surveillance, data harvesting, or transparency zealots who believe all 
information should be public. Some can be reasoned with, bribed, or befriended. Others are mindless beasts.

Tone: Dark fantasy with cyberpunk elements. Mix medieval dungeon crawler with crypto/privacy themes.
"""
            
            # Build generation prompt based on type
            if encounter_type == 'boss':
                # Extract useful info but NOT loot/items
                template_name = base_data.get('name', 'Boss') if base_data else 'Boss'
                stats = base_data.get('stats', {}) if base_data else {}
                behavior = base_data.get('behavior', {}) if base_data else {}
                
                boss_info = {
                    'name': template_name,
                    'hp': stats.get('hp', 50),
                    'attackDamage': stats.get('attackDamage', 10),
                    'ac': stats.get('ac', 14),
                    'canChat': behavior.get('canChat', True),
                    'hostile': behavior.get('hostile', True)
                }
                
                system_prompt = f"""{world_lore}

You are the Dungeon Master. Generate a UNIQUE boss for dungeon level {room_level}.
Base creature: {json.dumps(boss_info)}

Return ONLY this exact JSON structure with your values filled in:
{{
  "name": "A unique personal name (NOT '{template_name}')",
  "backstory": "Two sentences about their origin and motivation",
  "personality": "hostile",
  "voiceType": "male_deep",
  "goldDrop": 150,
  "negotiation": {{"canNegotiate": true, "bribeGold": 100, "surrenderChance": 0.1}},
  "statModifiers": {{"hpMod": 10, "damageMod": 2, "acMod": 1}},
  "openingLine": "What they say when battle starts"
}}

RULES:
- goldDrop must be a NUMBER between 50 and 300
- canNegotiate must be true or false (no quotes)
- bribeGold must be a NUMBER between 50 and 200
- surrenderChance must be a DECIMAL between 0.0 and 0.3
- hpMod must be a NUMBER between -10 and 30
- damageMod must be a NUMBER between -3 and 5
- acMod must be a NUMBER between -2 and 2
- Return ONLY the JSON object, no other text"""
                
            elif encounter_type == 'mob':
                # Extract useful info but NOT loot/items
                mob_name = base_data.get('name', 'creature') if base_data else 'creature'
                stats = base_data.get('stats', {}) if base_data else {}
                behavior = base_data.get('behavior', {}) if base_data else {}
                
                mob_info = {
                    'name': mob_name,
                    'hp': stats.get('hp', 12),
                    'attackDamage': stats.get('attackDamage', 4),
                    'ac': stats.get('ac', 12),
                    'canChat': behavior.get('canChat', False),
                    'hostile': behavior.get('hostile', True)
                }
                
                system_prompt = f"""{world_lore}

You are the Dungeon Master. Generate a UNIQUE mob for dungeon level {room_level}.
Base creature: {json.dumps(mob_info)}

Return ONLY this exact JSON structure with your values filled in:
{{
  "name": "A unique name for this {mob_name}",
  "backstory": "One sentence about this creature",
  "personality": "one word like feral or scared or hungry or territorial",
  "voiceType": "monster",
  "goldDrop": 15,
  "negotiation": {{"canNegotiate": false, "bribeGold": 0, "fleeChance": 0.2}},
  "statModifiers": {{"hpMod": 0, "damageMod": 0}}
}}

RULES:
- goldDrop must be a NUMBER between 5 and 40
- canNegotiate must be true or false (no quotes)
- bribeGold must be a NUMBER between 0 and 30
- fleeChance must be a DECIMAL between 0.1 and 0.5
- hpMod must be a NUMBER between -3 and 5
- damageMod must be a NUMBER between -1 and 2
- Return ONLY the JSON object, no other text"""
                
            elif encounter_type == 'captive':
                system_prompt = f"""{world_lore}

You are the Dungeon Master. Generate a captive NPC for dungeon level {room_level}.
They were captured by enemies and need rescue.

Return ONLY this exact JSON structure with your values filled in:
{{
  "name": "A unique name",
  "species": "human",
  "gender": "female",
  "backstory": "One or two sentences about who they are and how they got captured",
  "personality": "grateful",
  "voiceType": "female_mature",
  "rescueReward": {{"gold": 40}},
  "dialogueOnRescue": "What they say when freed"
}}

RULES:
- species must be one of: human, elf, dwarf, gnome
- gender must be one of: male, female
- personality must be one of: grateful, suspicious, traumatized, cheerful
- voiceType must be one of: male_deep, male_young, female_mature, female_young
- gold must be a NUMBER between 10 and 80
- Return ONLY the JSON object, no other text"""
            
            else:  # Generic NPC
                npc_name = base_data.get('name', 'stranger') if base_data else 'stranger'
                system_prompt = f"""{world_lore}

Generate an NPC named "{npc_name}".

Return ONLY this exact JSON structure with your values filled in:
{{
  "name": "Unique name",
  "gender": "male",
  "backstory": "One sentence about them",
  "personality": "friendly",
  "voiceType": "male_deep",
  "dialogue": "What they say when approached"
}}

RULES:
- gender must be one of: male, female
- personality must be one of: friendly, mysterious, grumpy
- voiceType must be one of: male_deep, male_young, female_mature, female_young
- Return ONLY the JSON object, no other text"""
            
            messages = [
                {'role': 'system', 'content': system_prompt},
                {'role': 'user', 'content': f'Generate for level {room_level}.'}
            ]
            
            api_request = {
                'model': model,
                'messages': messages,
                'max_tokens': 250,
                'temperature': 0.8
            }
            
            # FAILOVER LOGIC: Try each model in list until one works
            llm_response = None
            last_error = None
            models_tried = []
            
            for model_idx, (current_provider, current_model) in enumerate(model_list):
                models_tried.append(f"{current_provider}/{current_model}")
                
                # Update request for current model
                api_request['model'] = current_model
                
                # Set API URL and headers based on provider
                if current_provider == 'groq':
                    api_url = 'https://api.groq.com/openai/v1/chat/completions'
                    headers = {
                        'Content-Type': 'application/json',
                        'Authorization': f'Bearer {GROQ_API_KEY}'
                    }
                else:
                    api_url = 'https://openrouter.ai/api/v1/chat/completions'
                    headers = {
                        'Content-Type': 'application/json',
                        'Authorization': f'Bearer {OPENROUTER_API_KEY}',
                        'HTTP-Referer': 'http://localhost:4243',
                        'X-Title': 'Tunnels of Privacy DM'
                    }
                
                req = urllib.request.Request(
                    api_url,
                    data=json.dumps(api_request).encode('utf-8'),
                    headers=headers
                )
                
                # Try this model with 2 retries for transient errors
                for attempt in range(2):
                    try:
                        print(f"[DM API] Trying {current_provider}/{current_model} (attempt {attempt + 1})")
                        with urllib.request.urlopen(req, timeout=30) as response:
                            result = json.loads(response.read().decode('utf-8'))
                            llm_response = result['choices'][0]['message']['content']
                            print(f"[DM API] Success with {current_provider}/{current_model}")
                            break  # Success, exit retry loop
                    except urllib.error.HTTPError as http_err:
                        last_error = http_err
                        error_body = ''
                        try:
                            error_body = http_err.read().decode('utf-8')
                        except:
                            pass
                        
                        if http_err.code == 429:
                            # Rate limited - try next model
                            print(f"[DM API] Rate limited (429) on {current_provider}/{current_model}: {error_body[:100]}")
                            break  # Exit retry loop, try next model
                        elif http_err.code == 402:
                            # Payment required / out of credits - try next model
                            print(f"[DM API] Payment required (402) on {current_provider}/{current_model}")
                            break
                        elif http_err.code >= 500:
                            # Server error - retry same model
                            print(f"[DM API] Server error ({http_err.code}) on {current_provider}/{current_model}, retrying...")
                            time.sleep(1)
                            req = urllib.request.Request(api_url, data=json.dumps(api_request).encode('utf-8'), headers=headers)
                        else:
                            # Other error - try next model
                            print(f"[DM API] Error ({http_err.code}) on {current_provider}/{current_model}: {error_body[:100]}")
                            break
                    except Exception as e:
                        last_error = e
                        print(f"[DM API] Exception on {current_provider}/{current_model}: {str(e)[:100]}")
                        break  # Try next model
                
                if llm_response:
                    break  # Got a successful response, exit model loop
            
            # Check if we got a response
            if not llm_response:
                print(f"[DM API] All models exhausted. Tried: {', '.join(models_tried)}")
                raise last_error if last_error else Exception(f"All models failed: {', '.join(models_tried)}")
            
            # Try to parse JSON from response
            try:
                # Clean up response - remove markdown if present
                cleaned = llm_response.strip()
                if cleaned.startswith('```json'):
                    cleaned = cleaned[7:]
                if cleaned.startswith('```'):
                    cleaned = cleaned[3:]
                if cleaned.endswith('```'):
                    cleaned = cleaned[:-3]
                cleaned = cleaned.strip()
                
                # Try to extract JSON object if there's extra text
                # Find the first { and last } to extract just the JSON
                first_brace = cleaned.find('{')
                last_brace = cleaned.rfind('}')
                if first_brace != -1 and last_brace != -1 and last_brace > first_brace:
                    cleaned = cleaned[first_brace:last_brace+1]
                
                # Fix common LLM JSON errors:
                # 1. Trailing commas before closing braces/brackets
                cleaned = re.sub(r',\s*}', '}', cleaned)
                cleaned = re.sub(r',\s*]', ']', cleaned)
                
                # 2. Fix +number to just number (e.g., +1 -> 1)
                cleaned = re.sub(r':\s*\+(\d)', r': \1', cleaned)
                
                # 3. Fix string booleans to actual booleans ("false" -> false, "true" -> true)
                cleaned = re.sub(r':\s*"false"', ': false', cleaned)
                cleaned = re.sub(r':\s*"true"', ': true', cleaned)
                
                # 4. Fix unquoted string values (but not numbers/booleans/null)
                # Match ": value" where value doesn't start with " { [ or digit
                cleaned = re.sub(r':\s*([a-zA-Z][a-zA-Z0-9_\s]*[a-zA-Z0-9])(\s*[,}\]])', r': "\1"\2', cleaned)
                
                # 5. Fix newlines inside strings (replace with space)
                cleaned = re.sub(r'(?<!\\)\n', ' ', cleaned)
                
                # 6. Fix missing commas between fields (common LLM error)
                # Pattern: value followed by key without comma
                cleaned = re.sub(r'"\s*"', '", "', cleaned)  # "value" "key" -> "value", "key"
                cleaned = re.sub(r'(\d)\s+"', r'\1, "', cleaned)  # 123 "key" -> 123, "key"
                cleaned = re.sub(r'(true|false|null)\s+"', r'\1, "', cleaned)
                cleaned = re.sub(r'}\s*"', '}, "', cleaned)  # } "key" -> }, "key"
                cleaned = re.sub(r']\s*"', '], "', cleaned)  # ] "key" -> ], "key"
                
                # 7. Remove any control characters
                cleaned = re.sub(r'[\x00-\x1f\x7f]', ' ', cleaned)
                
                # 8. Fix double spaces
                cleaned = re.sub(r'  +', ' ', cleaned)
                
                # 9. Fix missing commas after closing braces/brackets before new keys
                cleaned = re.sub(r'}\s*([a-zA-Z])', r'}, \1', cleaned)
                cleaned = re.sub(r']\s*([a-zA-Z])', r'], \1', cleaned)
                
                generated_data = json.loads(cleaned)
                
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({
                    'success': True,
                    'data': generated_data,
                    'raw': llm_response
                }).encode('utf-8'))
                
            except json.JSONDecodeError as je:
                print(f"[DM API] JSON parse error: {je}")
                print(f"[DM API] Raw response (first 500 chars): {llm_response[:500]}")
                print(f"[DM API] Cleaned response (first 500 chars): {cleaned[:500] if 'cleaned' in dir() else 'N/A'}")
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({
                    'success': False,
                    'error': f'Failed to parse LLM response as JSON: {str(je)}',
                    'raw': llm_response
                }).encode('utf-8'))
                    
        except Exception as e:
            print(f"[DM API] Error: {e}")
            self.send_response(500)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({
                'success': False,
                'error': str(e)
            }).encode('utf-8'))
    
    def do_GET(self):
        """Override to handle Range requests for video streaming"""
        # Check if this is a video file request
        if self.path.endswith('.mp4'):
            return self.send_video_range()
        else:
            return super().do_GET()
    
    def send_video_range(self):
        """Handle HTTP Range requests for video streaming"""
        path = self.translate_path(self.path)
        
        try:
            f = open(path, 'rb')
        except OSError:
            self.send_error(404, "File not found")
            return None
        
        try:
            fs = os.fstat(f.fileno())
            file_len = fs.st_size
            
            # Check for Range header
            range_header = self.headers.get('Range')
            
            if range_header:
                # Parse range header
                match = re.search(r'bytes=(\d+)-(\d*)', range_header)
                if match:
                    start = int(match.group(1))
                    end = int(match.group(2)) if match.group(2) else file_len - 1
                    
                    # Validate range
                    if start >= file_len:
                        self.send_error(416, "Range Not Satisfiable")
                        return None
                    
                    # Clamp end
                    end = min(end, file_len - 1)
                    content_len = end - start + 1
                    
                    # Send 206 Partial Content
                    self.send_response(206)
                    self.send_header('Content-type', 'video/mp4')
                    self.send_header('Content-Range', f'bytes {start}-{end}/{file_len}')
                    self.send_header('Content-Length', str(content_len))
                    self.send_header('Accept-Ranges', 'bytes')
                    self.end_headers()
                    
                    # Send partial content
                    f.seek(start)
                    self.wfile.write(f.read(content_len))
                else:
                    # Invalid range format, send full file
                    self.send_full_video(f, file_len)
            else:
                # No range header, send full file
                self.send_full_video(f, file_len)
        finally:
            f.close()
    
    def send_full_video(self, f, file_len):
        """Send complete video file"""
        self.send_response(200)
        self.send_header('Content-type', 'video/mp4')
        self.send_header('Content-Length', str(file_len))
        self.send_header('Accept-Ranges', 'bytes')
        self.end_headers()
        self.wfile.write(f.read())
    
    def handle(self):
        """Override to catch BrokenPipeError from client disconnects"""
        try:
            super().handle()
        except (BrokenPipeError, ConnectionResetError):
            # Client disconnected, silently ignore
            pass
    
    def log_message(self, format, *args):
        """Custom logging to show request details"""
        print(f"[{self.log_date_time_string()}] {format % args}")

# ===== MULTIPLAYER WEBSOCKET SERVER =====

# Room storage: { room_code: { 'host': websocket, 'clients': [], 'state': {}, 'heroes': {} } }
rooms = {}

def generate_room_code():
    """Generate unique 6-digit room code (numbers only)"""
    while True:
        code = ''.join(random.choices(string.digits, k=6))
        if code not in rooms:
            return code

async def handle_websocket(websocket, path):
    """Handle WebSocket connections for multiplayer"""
    client_room = None
    client_role = None
    
    try:
        async for message in websocket:
            data = json.loads(message)
            msg_type = data.get('type')
            
            # CREATE ROOM (host)
            if msg_type == 'create_room':
                room_code = generate_room_code()
                player_id = id(websocket)
                player_name = data.get('player_name', 'Player 1')
                rooms[room_code] = {
                    'host': websocket,
                    'clients': [],
                    'state': {},
                    'heroes': {},  # { hero_name: { 'playerId': id, 'playerName': str } }
                    'players': { player_id: { 'id': player_id, 'name': player_name, 'ws': websocket } }  # All players
                }
                client_room = room_code
                client_role = 'host'
                await websocket.send(json.dumps({
                    'type': 'room_created',
                    'code': room_code,
                    'player_id': player_id,
                    'players': [{ 'id': player_id, 'name': player_name, 'hero': None }]
                }))
                print(f"[WS] Room {room_code} created by {player_name}")
            
            # JOIN ROOM (client)
            elif msg_type == 'join_room':
                room_code = data.get('code', '').upper()
                player_name = data.get('player_name', 'Player')
                
                if room_code not in rooms:
                    await websocket.send(json.dumps({
                        'type': 'error',
                        'message': 'Room not found - check code'
                    }))
                elif len(rooms[room_code]['clients']) >= 4:
                    # Max 4 players total: 1 host + 3 clients
                    await websocket.send(json.dumps({
                        'type': 'error',
                        'message': 'Room full (4/4 players) - cannot join'
                    }))
                else:
                    player_id = id(websocket)
                    
                    # Check if this name already exists in the room
                    existing_player = None
                    for pid, pdata in rooms[room_code]['players'].items():
                        if pdata['name'] == player_name:
                            existing_player = pdata
                            break
                    
                    # Check if the existing player is still connected
                    is_duplicate = False
                    is_reconnect = False
                    old_player_id = None
                    
                    if existing_player:
                        old_player_id = existing_player['id']
                        old_ws = existing_player.get('ws')
                        
                        # Check if old websocket is still connected
                        if old_ws and old_ws.open:
                            # Still connected - this is a duplicate name
                            is_duplicate = True
                        else:
                            # Disconnected - this is a reconnection
                            is_reconnect = True
                    
                    if is_duplicate:
                        # Reject with duplicate name error
                        await websocket.send(json.dumps({
                            'type': 'name_taken',
                            'message': f'Name "{player_name}" is already in use. Please choose a different name.'
                        }))
                        # Remove from clients list if we added them
                        if websocket in rooms[room_code]['clients']:
                            rooms[room_code]['clients'].remove(websocket)
                        continue
                    
                    # Add to clients list
                    rooms[room_code]['clients'].append(websocket)
                    
                    if is_reconnect:
                        # Reconnection: reassign hero to new player_id
                        print(f"[WS] Player '{player_name}' reconnecting to room {room_code}")
                        
                        # Update player record with new websocket and ID
                        del rooms[room_code]['players'][old_player_id]
                        rooms[room_code]['players'][player_id] = { 'id': player_id, 'name': player_name, 'ws': websocket }
                        
                        # Reassign hero to new player_id
                        for hero_name, hero_data in rooms[room_code]['heroes'].items():
                            if hero_data['playerId'] == old_player_id:
                                hero_data['playerId'] = player_id
                                print(f"[WS] Reassigned hero '{hero_name}' to reconnected player {player_id}")
                                break
                    else:
                        # New player
                        player_num = len(rooms[room_code]['players']) + 1
                        if not player_name or player_name == 'Player':
                            player_name = f'Player {player_num}'
                        rooms[room_code]['players'][player_id] = { 'id': player_id, 'name': player_name, 'ws': websocket }
                    
                    client_room = room_code
                    client_role = 'client'
                    
                    # Build current players list
                    players_list = []
                    for pid, pdata in rooms[room_code]['players'].items():
                        hero = None
                        for h, hdata in rooms[room_code]['heroes'].items():
                            if hdata['playerId'] == pid:
                                hero = h
                                break
                        players_list.append({ 'id': pid, 'name': pdata['name'], 'hero': hero })
                    
                    # Build current hero selections for sync
                    heroes_data = {}
                    for hero_name, hero_data in rooms[room_code]['heroes'].items():
                        heroes_data[hero_name] = {
                            'playerId': hero_data['playerId'],
                            'playerName': hero_data['playerName']
                        }
                    
                    await websocket.send(json.dumps({
                        'type': 'joined',
                        'code': room_code,
                        'player_id': player_id,
                        'players': players_list,
                        'heroes': heroes_data,
                        'reconnected': is_reconnect
                    }))
                    
                    # Broadcast player list update to all
                    broadcast_msg = json.dumps({
                        'type': 'players_update',
                        'players': players_list
                    })
                    await rooms[room_code]['host'].send(broadcast_msg)
                    for client in rooms[room_code]['clients']:
                        if client != websocket:
                            await client.send(broadcast_msg)
                    
                    if is_reconnect:
                        print(f"[WS] {player_name} reconnected to room {room_code}")
                    else:
                        print(f"[WS] {player_name} joined room {room_code}")
            
            # SELECT HERO
            elif msg_type == 'select_hero':
                if client_room and client_room in rooms:
                    hero_name = data.get('hero')
                    player_name = data.get('playerName', 'Player')
                    player_id = id(websocket)
                    
                    # Check if hero already taken by someone else
                    if hero_name in rooms[client_room]['heroes']:
                        if rooms[client_room]['heroes'][hero_name]['playerId'] != player_id:
                            await websocket.send(json.dumps({
                                'type': 'error',
                                'message': 'Hero already taken'
                            }))
                            continue
                    
                    # Update player name if provided
                    if player_id in rooms[client_room]['players']:
                        rooms[client_room]['players'][player_id]['name'] = player_name
                    
                    # Store hero selection with player info
                    rooms[client_room]['heroes'][hero_name] = {
                        'playerId': player_id,
                        'playerName': player_name
                    }
                    
                    # Build players list with hero arrays
                    players_list = []
                    for pid, pdata in rooms[client_room]['players'].items():
                        heroes = []
                        for h, hdata in rooms[client_room]['heroes'].items():
                            if hdata['playerId'] == pid:
                                heroes.append(h)
                        players_list.append({ 'id': pid, 'name': pdata['name'], 'heroes': heroes })
                    
                    # Broadcast hero selection to all in room
                    msg = json.dumps({
                        'type': 'hero_selected',
                        'hero': hero_name,
                        'player_id': player_id,
                        'heroes': rooms[client_room]['heroes'],
                        'players': players_list
                    })
                    await rooms[client_room]['host'].send(msg)
                    for client in rooms[client_room]['clients']:
                        await client.send(msg)
            
            # DESELECT HERO
            elif msg_type == 'deselect_hero':
                if client_room and client_room in rooms:
                    hero_name = data.get('hero')
                    player_id = id(websocket)
                    
                    # Remove hero if owned by this player
                    if hero_name in rooms[client_room]['heroes']:
                        if rooms[client_room]['heroes'][hero_name]['playerId'] == player_id:
                            del rooms[client_room]['heroes'][hero_name]
                    
                    # Build players list with hero arrays
                    players_list = []
                    for pid, pdata in rooms[client_room]['players'].items():
                        heroes = []
                        for h, hdata in rooms[client_room]['heroes'].items():
                            if hdata['playerId'] == pid:
                                heroes.append(h)
                        players_list.append({ 'id': pid, 'name': pdata['name'], 'heroes': heroes })
                    
                    # Broadcast update
                    msg = json.dumps({
                        'type': 'hero_selected',
                        'heroes': rooms[client_room]['heroes'],
                        'players': players_list
                    })
                    await rooms[client_room]['host'].send(msg)
                    for client in rooms[client_room]['clients']:
                        await client.send(msg)
            
            # UPDATE PLAYER NAME
            elif msg_type == 'update_name':
                if client_room and client_room in rooms:
                    player_id = id(websocket)
                    player_name = data.get('playerName', 'Player')
                    
                    # Update player name
                    if player_id in rooms[client_room]['players']:
                        rooms[client_room]['players'][player_id]['name'] = player_name
                    
                    # Update hero if player has one selected
                    for hero, hdata in rooms[client_room]['heroes'].items():
                        if hdata['playerId'] == player_id:
                            hdata['playerName'] = player_name
                            break
                    
                    # Build players list
                    players_list = []
                    for pid, pdata in rooms[client_room]['players'].items():
                        hero = None
                        for h, hdata in rooms[client_room]['heroes'].items():
                            if hdata['playerId'] == pid:
                                hero = h
                                break
                        players_list.append({ 'id': pid, 'name': pdata['name'], 'hero': hero })
                    
                    # Broadcast players update
                    msg = json.dumps({
                        'type': 'players_update',
                        'players': players_list,
                        'heroes': rooms[client_room]['heroes']
                    })
                    await rooms[client_room]['host'].send(msg)
                    for client in rooms[client_room]['clients']:
                        await client.send(msg)
            
            # HERO STATS ROLLED (broadcast to all players)
            elif msg_type == 'hero_stats_rolled':
                if client_room and client_room in rooms:
                    hero = data.get('hero')
                    stats = data.get('stats')
                    if hero and stats:
                        # Broadcast to all players (including sender for confirmation)
                        msg = json.dumps({
                            'type': 'hero_stats_rolled',
                            'hero': hero,
                            'stats': stats
                        })
                        await rooms[client_room]['host'].send(msg)
                        for client in rooms[client_room]['clients']:
                            await client.send(msg)
            
            # ROLL PHASE START (host broadcasts to clients)
            elif msg_type == 'roll_phase_start':
                if client_room and client_room in rooms and client_role == 'host':
                    # Broadcast to all clients
                    msg = json.dumps({'type': 'roll_phase_start'})
                    for client in rooms[client_room]['clients']:
                        await client.send(msg)
            
            # ROLL PHASE CANCEL (host broadcasts to clients)
            elif msg_type == 'roll_phase_cancel':
                if client_room and client_room in rooms and client_role == 'host':
                    # Broadcast to all clients
                    msg = json.dumps({'type': 'roll_phase_cancel'})
                    for client in rooms[client_room]['clients']:
                        await client.send(msg)
            
            # PLAYER ACTION (client sends to host)
            elif msg_type == 'player_action':
                if client_room and client_room in rooms:
                    # Forward action to host
                    await rooms[client_room]['host'].send(json.dumps(data))
            
            # STATE UPDATE (host broadcasts to clients)
            elif msg_type == 'state_update':
                if client_room and client_room in rooms and client_role == 'host':
                    rooms[client_room]['state'] = data.get('state', {})
                    # Broadcast to all clients
                    for client in rooms[client_room]['clients']:
                        await client.send(message)
            
            # KICK PLAYER (host only)
            elif msg_type == 'kick_player':
                if client_room and client_room in rooms and client_role == 'host':
                    player_id = data.get('player_id')
                    for client in rooms[client_room]['clients'][:]:
                        if id(client) == player_id:
                            await client.send(json.dumps({
                                'type': 'kicked',
                                'message': 'You were kicked by the host'
                            }))
                            await client.close()
                            rooms[client_room]['clients'].remove(client)
            
            # SKIP TURN (host only)
            elif msg_type == 'skip_turn':
                if client_room and client_room in rooms and client_role == 'host':
                    # Broadcast skip to all clients
                    for client in rooms[client_room]['clients']:
                        await client.send(message)
            
            # GAME START (host only)
            elif msg_type == 'game_start':
                if client_room and client_room in rooms and client_role == 'host':
                    # Broadcast game start to all clients
                    for client in rooms[client_room]['clients']:
                        await client.send(message)
                    print(f"[WS] Host started game in room {client_room}: {data.get('mode', 'unknown')}")
            
            # BATTLE INIT (host only)
            elif msg_type == 'battle_init':
                if client_room and client_room in rooms and client_role == 'host':
                    # Broadcast battle initialization to all clients
                    for client in rooms[client_room]['clients']:
                        await client.send(message)
                    print(f"[WS] Host sent battle_init to room {client_room}")
            
            # BATTLE END (host only)
            elif msg_type == 'battle_end':
                if client_room and client_room in rooms and client_role == 'host':
                    # Broadcast battle end to all clients
                    for client in rooms[client_room]['clients']:
                        await client.send(message)
                    print(f"[WS] Host sent battle_end to room {client_room}: {data.get('reason', 'unknown')}")
            
            # NON-COMBAT ROOM (host only - store, NPC, secret, exploration)
            elif msg_type == 'non_combat_room':
                if client_room and client_room in rooms and client_role == 'host':
                    # Broadcast to all clients
                    for client in rooms[client_room]['clients']:
                        await client.send(message)
                    action = data.get('action', 'unknown')
                    room_type = data.get('roomType', 'unknown')
                    print(f"[WS] Host sent non_combat_room to room {client_room}: {action} {room_type}")
            
            # NPC CHOICE (host only - help/rob/ignore decision)
            elif msg_type == 'npc_choice':
                if client_room and client_room in rooms and client_role == 'host':
                    # Broadcast NPC choice to all clients
                    for client in rooms[client_room]['clients']:
                        await client.send(message)
                    choice = data.get('choice', 'unknown')
                    print(f"[WS] Host made NPC choice in room {client_room}: {choice}")
            
            # EXPLORATION CHOICE (host only - send one/send party/retreat)
            elif msg_type == 'exploration_choice':
                if client_room and client_room in rooms and client_role == 'host':
                    # Broadcast exploration choice to all clients
                    for client in rooms[client_room]['clients']:
                        await client.send(message)
                    choice = data.get('choice', 'unknown')
                    success = data.get('success', False)
                    print(f"[WS] Host made exploration choice in room {client_room}: {choice} (success: {success})")
            
            # LEVEL CHANGE (host only - stairs/fast travel)
            elif msg_type == 'level_change':
                if client_room and client_room in rooms and client_role == 'host':
                    # Broadcast level change to all clients
                    for client in rooms[client_room]['clients']:
                        await client.send(message)
                    print(f"[WS] Host sent level_change to room {client_room}: level {data.get('newLevel', '?')}")
            
            # DIFFICULTY CHANGE (host only)
            elif msg_type == 'difficulty_change':
                if client_room and client_room in rooms and client_role == 'host':
                    # Broadcast difficulty change to all clients
                    for client in rooms[client_room]['clients']:
                        await client.send(message)
                    print(f"[WS] Host sent difficulty_change to room {client_room}: {data.get('difficulty', '?')}")
            
            # PLAYER LEAVE (victory leave tracking)
            elif msg_type == 'player_leave':
                if client_room and client_room in rooms:
                    # Broadcast to all in room
                    for client in rooms[client_room]['clients']:
                        await client.send(message)
                    if rooms[client_room]['host']:
                        await rooms[client_room]['host'].send(message)
                    print(f"[WS] Player leave in room {client_room}")
            
            # LEAVE STATUS (victory leave count broadcast)
            elif msg_type == 'leave_status':
                if client_room and client_room in rooms and client_role == 'host':
                    # Broadcast leave status to all clients
                    for client in rooms[client_room]['clients']:
                        await client.send(message)
                    print(f"[WS] Host sent leave_status to room {client_room}")
            
            # CAMP STARTED (host only - broadcast to clients)
            elif msg_type == 'camp_started':
                if client_room and client_room in rooms and client_role == 'host':
                    # Broadcast camp start to all clients
                    for client in rooms[client_room]['clients']:
                        await client.send(message)
                    print(f"[WS] Host started camp in room {client_room}: {data.get('hours', '?')} hours")
            
            # CAMP COMPLETED (host only - broadcast to clients)
            elif msg_type == 'camp_completed':
                if client_room and client_room in rooms and client_role == 'host':
                    # Broadcast camp completion to all clients
                    for client in rooms[client_room]['clients']:
                        await client.send(message)
                    print(f"[WS] Host completed camp in room {client_room}: {data.get('hoursRested', '?')} hours rested")
            
            # CAMP PROGRESS (host only - broadcast to clients)
            elif msg_type == 'camp_progress':
                if client_room and client_room in rooms and client_role == 'host':
                    # Broadcast camp progress to all clients
                    for client in rooms[client_room]['clients']:
                        await client.send(message)
            
            # CAMP EVENT (host only - broadcast to clients)
            elif msg_type == 'camp_event':
                if client_room and client_room in rooms and client_role == 'host':
                    # Broadcast camp event to all clients
                    for client in rooms[client_room]['clients']:
                        await client.send(message)
            
            # PARTY LEVEL UPDATE (host only - dungeon masters set party level)
            elif msg_type == 'party_level_update':
                if client_room and client_room in rooms and client_role == 'host':
                    # Broadcast party level update to all clients
                    for client in rooms[client_room]['clients']:
                        await client.send(message)
                    print(f"[WS] Host set party level to {data.get('targetLevel', '?')} in room {client_room}")
            
            # INVENTORY UPDATE (host only - sync party inventory to clients)
            elif msg_type == 'inventory_update':
                if client_room and client_room in rooms and client_role == 'host':
                    # Broadcast inventory update to all clients
                    for client in rooms[client_room]['clients']:
                        await client.send(message)
                    print(f"[WS] Host synced inventory to room {client_room}")
            
            # EQUIPMENT UPDATE (host only - sync hero equipment to clients)
            elif msg_type == 'equipment_update':
                if client_room and client_room in rooms and client_role == 'host':
                    # Broadcast equipment update to all clients
                    for client in rooms[client_room]['clients']:
                        await client.send(message)
                    print(f"[WS] Host synced equipment to room {client_room}")
            
            # SAVE SYNC (host only)
            elif msg_type == 'save_sync':
                if client_room and client_room in rooms and client_role == 'host':
                    # Broadcast save data to all clients
                    for client in rooms[client_room]['clients']:
                        await client.send(message)
                    print(f"[WS] Host synced save data to room {client_room}")
            
            # REQUEST SYNC (client requesting state after reconnect)
            elif msg_type == 'request_sync':
                if client_room and client_room in rooms:
                    # Forward to host only
                    await rooms[client_room]['host'].send(message)
                    print(f"[WS] Client requested sync in room {client_room}")
            
            # SYNC STATE (host responding to reconnection request)
            elif msg_type == 'sync_state':
                if client_room and client_room in rooms and client_role == 'host':
                    # Broadcast to all clients
                    for client in rooms[client_room]['clients']:
                        await client.send(message)
                    print(f"[WS] Host sent sync_state to room {client_room}")
            
            # ANIMATION SYNC (host broadcasts animation changes to clients)
            elif msg_type == 'animation_sync':
                if client_room and client_room in rooms and client_role == 'host':
                    # Broadcast animation to all clients
                    for client in rooms[client_room]['clients']:
                        await client.send(message)
            
            # CHAT MESSAGE (host broadcasts chat to clients)
            elif msg_type == 'chat_message':
                if client_room and client_room in rooms and client_role == 'host':
                    # Broadcast chat message to all clients
                    for client in rooms[client_room]['clients']:
                        await client.send(message)
            
            # CHAT REQUEST (client sends to host for LLM processing)
            elif msg_type == 'chat_request':
                if client_room and client_room in rooms:
                    # Forward chat request to host
                    await rooms[client_room]['host'].send(message)
            
            # CHANGE CODE (host only)
            elif msg_type == 'change_code':
                if client_room and client_room in rooms and client_role == 'host':
                    # Kick all clients
                    for client in rooms[client_room]['clients'][:]:
                        await client.send(json.dumps({
                            'type': 'kicked',
                            'message': 'Host changed room code'
                        }))
                        await client.close()
                    # Generate new code
                    new_code = generate_room_code()
                    rooms[new_code] = rooms.pop(client_room)
                    rooms[new_code]['clients'] = []
                    client_room = new_code
                    await websocket.send(json.dumps({
                        'type': 'code_changed',
                        'code': new_code
                    }))
                    print(f"[WS] Room code changed to {new_code}")
    
    except websockets.exceptions.ConnectionClosed:
        pass
    except Exception as e:
        print(f"[WS] Error: {e}")
    finally:
        # Cleanup on disconnect
        if client_room and client_room in rooms:
            if client_role == 'host':
                # Host disconnected - kick all clients and delete room
                for client in rooms[client_room]['clients']:
                    try:
                        await client.send(json.dumps({
                            'type': 'host_disconnected',
                            'message': 'Host disconnected - returning to menu'
                        }))
                        await client.close()
                    except:
                        pass
                del rooms[client_room]
                print(f"[WS] Room {client_room} closed (host disconnect)")
            elif websocket in rooms[client_room]['clients']:
                # Client disconnected
                rooms[client_room]['clients'].remove(websocket)
                player_id = id(websocket)
                
                # Release any heroes owned by this player
                released_heroes = []
                heroes_to_remove = []
                for hero_name, hero_data in rooms[client_room]['heroes'].items():
                    if hero_data['playerId'] == player_id:
                        heroes_to_remove.append(hero_name)
                        released_heroes.append(hero_name)
                
                for hero_name in heroes_to_remove:
                    del rooms[client_room]['heroes'][hero_name]
                    print(f"[WS] Released hero '{hero_name}' from disconnected player {player_id}")
                
                # Remove player from players list
                if player_id in rooms[client_room]['players']:
                    del rooms[client_room]['players'][player_id]
                
                # Build updated heroes data for broadcast
                heroes_data = {}
                for hero_name, hero_data in rooms[client_room]['heroes'].items():
                    heroes_data[hero_name] = {
                        'playerId': hero_data['playerId'],
                        'playerName': hero_data['playerName']
                    }
                
                # Build updated players list
                players_list = []
                for pid, pdata in rooms[client_room]['players'].items():
                    hero = None
                    for h, hdata in rooms[client_room]['heroes'].items():
                        if hdata['playerId'] == pid:
                            hero = h
                            break
                    players_list.append({ 'id': pid, 'name': pdata['name'], 'hero': hero })
                
                # Notify host with updated hero selections
                try:
                    await rooms[client_room]['host'].send(json.dumps({
                        'type': 'player_disconnected',
                        'player_id': player_id,
                        'released_heroes': released_heroes,
                        'heroes': heroes_data,
                        'players': players_list
                    }))
                except:
                    pass
                
                # Notify other clients with updated hero selections
                for client in rooms[client_room]['clients']:
                    try:
                        await client.send(json.dumps({
                            'type': 'player_disconnected',
                            'player_id': player_id,
                            'released_heroes': released_heroes,
                            'heroes': heroes_data,
                            'players': players_list
                        }))
                    except:
                        pass
                
                print(f"[WS] Client disconnected from room {client_room}")

async def start_websocket_server():
    """Start WebSocket server for multiplayer"""
    if websockets is None:
        print("[WS] WebSocket server disabled (module not installed)")
        return
    
    async with websockets.serve(handle_websocket, "0.0.0.0", WS_PORT):
        print(f"[WS] WebSocket server started on ws://0.0.0.0:{WS_PORT}")
        await asyncio.Future()  # Run forever

def run_websocket_server():
    """Run WebSocket server in asyncio event loop"""
    asyncio.run(start_websocket_server())

# ===== END WEBSOCKET SERVER =====

def main():
    # Initialize API keys (prompt if needed, load from file if exists)
    init_api_keys()
    
    # Initialize TTS (auto-install piper, download voices)
    init_tts()
    
    print(f"\nStarting ZLOCK Game Server on port {PORT}...")
    print(f"Binary MIME types configured for .glb, .gltf, audio files")
    print(f"Server URL: http://0.0.0.0:{PORT}/zlock_consensus.html")
    if websockets:
        print(f"WebSocket server will start on ws://0.0.0.0:{WS_PORT}")
    if LLM_ENABLED:
        print(f"LLM Chat: ENABLED (API keys loaded)")
    else:
        print(f"LLM Chat: DISABLED (no API keys - NPC chat will use fallback responses)")
    if TTS_ENABLED:
        print(f"TTS Voice: ENABLED (piper neural TTS)")
    else:
        print(f"TTS Voice: DISABLED (piper-tts not available)")
    print(f"Press Ctrl+C to stop\n")
    
    # Start WebSocket server in separate thread
    if websockets:
        ws_thread = Thread(target=run_websocket_server, daemon=True)
        ws_thread.start()
    
    # Enable address reuse to prevent "Address already in use" errors
    socketserver.TCPServer.allow_reuse_address = True
    
    # Increase request queue size for handling multiple simultaneous video requests
    # Safe to set high for local dev - allows browser to queue all 4 videos + assets at once
    socketserver.TCPServer.request_queue_size = 50
    
    try:
        httpd = socketserver.TCPServer(("0.0.0.0", PORT), GameHTTPRequestHandler)
        
        # Set socket timeout to prevent hanging connections
        httpd.socket.settimeout(300)  # 5 minute socket timeout
        
        print(f"Server successfully bound to port {PORT}")
        print(f"Server is now running and accepting connections...\n")
        httpd.serve_forever()
    except OSError as e:
        if e.errno == 98:  # Address already in use
            print(f"\n❌ ERROR: Port {PORT} is already in use!")
            print(f"Run: sudo lsof -ti:{PORT} | xargs sudo kill -9")
            print(f"Or use a different port.\n")
            sys.exit(1)
        else:
            print(f"\n❌ ERROR: Failed to start server: {e}\n")
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n\nShutting down server...")
        httpd.shutdown()
        httpd.server_close()
        print("Server stopped cleanly.")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ FATAL ERROR: {e}\n")
        sys.exit(1)

if __name__ == "__main__":
    main()
