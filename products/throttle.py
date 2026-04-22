from rest_framework.throttling import AnonRateThrottle, UserRateThrottle

class CustomAnonRateThrottle(AnonRateThrottle):
    scope = 'twenty'  # definiert den Scope für diese Throttle-Klasse, damit die Raten aus den Einstellungen verwendet werden

class CustomUserRateThrottle(UserRateThrottle):
    scope = 'hundret'  # definiert den Scope für diese Throttle-Klasse, damit die Raten aus den Einstellungen verwendet werden