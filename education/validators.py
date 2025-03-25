from rest_framework.serializers import ValidationError


class YouTubeValidator:
    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        url = "http://www.youtube.com"
        if value.get("video_url"):
            if url not in value.get("video_url"):
                raise ValidationError("Ссылки кроме 'http://www.youtube.com' не поддерживаются.")
        return None
