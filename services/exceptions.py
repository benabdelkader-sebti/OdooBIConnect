class LicenseInvalid(Exception):
    """يتم استدعاء هذا الخطأ عندما تكون رخصة البرنامج غير صالحة"""
    def __init__(self, message="License validation failed"):
        self.message = message
        super().__init__(self.message)