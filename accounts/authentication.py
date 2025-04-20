from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed, NotAuthenticated
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
import jwt
import logging

logger = logging.getLogger(__name__)

class CustomJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        # Authorization 헤더에서 토큰 추출
        auth_header = request.META.get('HTTP_AUTHORIZATION', '')
        logger.info(f"Authorization header: {auth_header}")
        
        if not auth_header:
            logger.warning("No Authorization header found")
            raise NotAuthenticated({
                "error": {
                    "code": "TOKEN_NOT_FOUND",
                    "message": "토큰이 없습니다."
                }
            })

        try:
            # Bearer 토큰 형식 검증
            if auth_header.startswith('Bearer '):
                token = auth_header.split('Bearer ')[1]
            else:
                auth_type, token = auth_header.split()
                if auth_type.lower() != 'bearer':
                    logger.warning(f"Invalid auth type: {auth_type}")
                    raise AuthenticationFailed({
                        "error": {
                            "code": "INVALID_TOKEN",
                            "message": "토큰이 유효하지 않습니다."
                        }
                    })

            # 토큰 검증
            validated_token = self.get_validated_token(token.encode())
            user = self.get_user(validated_token)
            
            if user is None:
                logger.warning("User not found for token")
                raise AuthenticationFailed({
                    "error": {
                        "code": "USER_NOT_FOUND",
                        "message": "토큰에 해당하는 사용자를 찾을 수 없습니다."
                    }
                })
                
            logger.info(f"Authentication successful for user: {user.username}")
            return user, validated_token

        except jwt.ExpiredSignatureError:
            logger.warning("Token expired")
            raise AuthenticationFailed({
                "error": {
                    "code": "TOKEN_EXPIRED",
                    "message": "토큰이 만료되었습니다."
                }
            })
        except (jwt.InvalidTokenError, TokenError, ValueError):
            logger.warning("Invalid token")
            raise AuthenticationFailed({
                "error": {
                    "code": "INVALID_TOKEN",
                    "message": "토큰이 유효하지 않습니다."
                }
            })
        except Exception:
            raise AuthenticationFailed({
                "error": {
                    "code": "INVALID_TOKEN",
                    "message": "토큰이 유효하지 않습니다."
                }
            })