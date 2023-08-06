# -*- coding: utf-8 -*-
import json
import logging
from base64 import b64decode
from datetime import datetime, timedelta
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import get_user_model
from django.conf import settings
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.authentication import BaseAuthentication, get_authorization_header
from rest_framework.authentication import SessionAuthentication
from rest_framework_jwt.settings import api_settings as jwt_settings
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from .http_utils import get_account_info
from .models import TUserAccessToken, TUserExtra


jwt_decode_handler = jwt_settings.JWT_DECODE_HANDLER
jwt_get_username_from_payload = jwt_settings.JWT_PAYLOAD_GET_USERNAME_HANDLER
logger = logging.getLogger('OAuthUser')


class OAuthAccessTokenAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth_header = get_authorization_header(request)
        if auth_header in ['', b'', None]:
            return None

        auth = [str(a.decode(encoding='utf-8')) if isinstance(a, bytes) else a for a in auth_header.split(b' ')]
        if auth is None or not isinstance(auth, list) or len(auth) < 2 or 'bearer' != auth[0].lower():
            return None

        access_token = auth[1]

        dt_now = datetime.now()
        saved = TUserAccessToken.objects.filter(access_token=access_token)

        valid = saved.filter(recheck_after__lte=dt_now)
        if valid.exists():
            # 验证成功
            user = valid.first().user
            return user, access_token
        else:
            if not saved.exists():
                saved.delete()

            status, response = get_account_info(settings.OAUTH_ACCOUNT_URL, 'Bearer', access_token)
            if status != 200:
                raise AuthenticationFailed

            account_info = json.loads(response)
            username = account_info.get('username')

            user_model = get_user_model()
            try:
                user = user_model.objects.select_related('extra').get(username=username)
            except ObjectDoesNotExist:
                user = user_model.objects.create(username=username)

            remote_privileges_list = account_info.get('privileges', [])

            if not hasattr(user, 'extra'):
                TUserExtra.objects.create(
                    user=user,
                    full_name=account_info.get('full_name'),
                    phone_number=account_info.get('mobile'),
                    access_token=access_token,
                    token_type='Bearer',
                    expires_in=600,
                    remote_privileges='|'.join(remote_privileges_list))
            else:
                user.extra.full_name = account_info.get('full_name')
                user.extra.access_token = access_token
                user.extra.token_type = 'Bearer'
                user.extra.expires_in = 600
                user.extra.remote_privileges = '|'.join(remote_privileges_list)
                user.extra.save()

            TUserAccessToken.objects.create(
                access_token=access_token,
                user=user,
                recheck_after=dt_now + timedelta(minutes=10))

            return user, access_token


class CsrfExemptSessionAuthentication(SessionAuthentication):
    def enforce_csrf(self, request):
        return


class JWTAuthentication(JSONWebTokenAuthentication):
    def authenticate(self, request):
        try:
            user, jwt_value = super(JWTAuthentication, self).authenticate(request)
        except TypeError:
            return None

        payload = jwt_decode_handler(jwt_value)

        if not hasattr(user, 'extra'):
            extra = TUserExtra.objects.create(user=user)
        else:
            extra = user.extra

        extra.full_name = payload.get('nick_name')
        extra.phone_number = payload.get('mobile')
        extra.remote_privileges = '|'.join(payload.get('privileges', []))
        extra.save()

        return user, jwt_value

    def authenticate_credentials(self, payload):
        """
        Returns an active user that matches the payload's user id and email.
        """
        User = get_user_model()
        username = jwt_get_username_from_payload(payload)

        if not username:
            msg = _('Invalid payload.')
            raise AuthenticationFailed(msg)

        try:
            user = User.objects.get_by_natural_key(username)
        except User.DoesNotExist:
            user = User.objects.create(**{User.USERNAME_FIELD: username})

        if not user.is_active:
            msg = _('User account is disabled.')
            raise AuthenticationFailed(msg)

        return user
