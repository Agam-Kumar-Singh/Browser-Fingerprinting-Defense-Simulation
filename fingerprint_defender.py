import random
import base64
import os
import string

class FingerprintDefender:
    def __init__(self):
        self.common_user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0",
            "Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1",
            "Mozilla/5.0 (Linux; Android 10; SM-G981B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.120 Mobile Safari/537.36"
        ]
        self.common_resolutions = [
            {"width": 1920, "height": 1080},
            {"width": 1366, "height": 768},
            {"width": 1536, "height": 864},
            {"width": 1440, "height": 900},
            {"width": 375, "height": 812},  # Mobile
            {"width": 414, "height": 896}   # Mobile
        ]
        self.common_timezones = [
            "America/New_York",
            "Europe/London",
            "Asia/Tokyo",
            "America/Los_Angeles",
            "Europe/Paris",
            "Asia/Shanghai"
        ]
        self.languages = ["en-US", "en-GB", "fr-FR", "de-DE", "es-ES", "ja-JP", "zh-CN", "ru-RU"]
    
    def defend(self, fingerprint):
        defended = fingerprint.copy()
        
        # Randomly select standardized attributes
        if 'browser' in defended:
            defended['browser'] = {
                'userAgent': random.choice(self.common_user_agents),
                'language': "en-US",
                'languages': ["en-US", "en"],
                'cookieEnabled': True,
                'doNotTrack': "0"
            }
        
        # Select a different standardized resolution each time
        if 'screen' in defended:
            resolution = random.choice(self.common_resolutions)
            defended['screen'] = {
                'width': resolution['width'],
                'height': resolution['height'],
                'colorDepth': 24,
                'pixelDepth': 24,
                'orientation': "landscape-primary" if resolution['width'] >= 1000 else "portrait-primary"
            }
        
        # Block advanced fingerprints
        defended['webgl'] = "blocked"
        defended['canvas'] = "blocked"
        
        # Select a different standardized timezone
        defended['timezone'] = {
            'timezone': random.choice(self.common_timezones),
            'dateOffset': -random.choice([240, 300, 360])
        }
        
        return defended
        
    def randomize(self, fingerprint):
        randomized = fingerprint.copy()

        # Generate random user agent string
        browser_name = random.choice(["Chrome", "Firefox", "Safari", "Edge"])
        os_name = random.choice(["Windows NT 10.0", "Macintosh; Intel Mac OS X 10_15_7", "Linux; Android 10", "iPhone; CPU iPhone OS 14_6"])
        version = f"{random.randint(80, 120)}.0.{random.randint(4000, 5000)}.{random.randint(100, 200)}"
        randomized['browser'] = {
            'userAgent': f"Mozilla/5.0 ({os_name}) AppleWebKit/537.36 (KHTML, like Gecko) {browser_name}/{version} Safari/537.36",
            'language': random.choice(self.languages),
            'languages': random.sample(self.languages, random.randint(1, 3)),
            'cookieEnabled': random.choice([True, False]),
            'doNotTrack': random.choice([None, "1", "0"])
        }

        # Randomize screen attributes
        is_mobile = random.choice([True, False])
        width_range = (320, 500) if is_mobile else (800, 2560)
        height_range = (568, 896) if is_mobile else (600, 1440)
        randomized['screen'] = {
            'width': random.randint(*width_range),
            'height': random.randint(*height_range),
            'colorDepth': random.choice([16, 24, 30, 32]),
            'pixelDepth': random.choice([16, 24, 30, 32]),
            'orientation': random.choice(["portrait-primary", "landscape-primary"])
        }

        # Randomize WebGL and Canvas
        randomized['webgl'] = base64.b64encode(os.urandom(8)).decode() if random.choice([True, False]) else "blocked"
        randomized['canvas'] = base64.b64encode(os.urandom(8)).decode() if random.choice([True, False]) else "blocked"

        # Random timezone
        randomized['timezone'] = {
            'timezone': random.choice(self.common_timezones + ["Australia/Sydney", "Africa/Cairo", "America/Sao_Paulo"]),
            'dateOffset': -random.randint(0, 720)
        }

        # Mark as randomized
        randomized['is_randomized'] = True
        randomized['is_mobile'] = is_mobile

        return randomized
    
    def generate_fake_fingerprint(self):
        # Create a base fingerprint and randomize it
        base_fp = {
            "screen": {"width": 1920, "height": 1080, "colorDepth": 24, "pixelDepth": 24},
            "browser": {"userAgent": "Mozilla/5.0"},
            "webgl": "NVIDIA Corporation",
            "canvas": "real_canvas_data",
            "is_fake": True
        }
        return self.randomize(base_fp)