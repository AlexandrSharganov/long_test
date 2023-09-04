from rest_framework.authentication import TokenAuthentication

class CustomTokenAuthentication(TokenAuthentication):
    """Кастомный класс для замены ключевого слова Token на Bearer."""
    
    keyword = 'Bearer'