#!/usr/bin/env python
# vi: et sw=2 fileencoding=utf-8



import json

from django.db.models import CharField, functions, Value
from django.utils.deprecation import MiddlewareMixin

from .models import UserRequest


class LoggerMiddleware(MiddlewareMixin, object):
  # pylint: disable=too-few-public-methods

  body_maksimipituus = 65536
  body_lohkokoko = 1024

  def process_request(self, request):
    # pylint: disable=no-self-use

    body = request.body[:self.body_maksimipituus].decode("ASCII", "replace")
    post = request.POST.copy()

    # suodata pois salasanat
    if 'password' in post:
      body = ''
      post['password'] = 'salasana'
    if 'password1' in post:
      body = ''
      post['password1'] = 'salasana'
    if 'password2' in post:
      body = ''
      post['password2'] = 'salasana'
    if 'salasana' in post:
      body = ''
      post['salasana'] = 'salasana'

    # luo uusi tietue
    user_request_id = UserRequest.objects.create(
      user=request.user.id if request.user.is_authenticated else None,
      path=request.get_full_path()[:UserRequest._meta.get_field('path').max_length],
      method=request.method,
      scheme=request.scheme,
      body="",
      content_length=request.META.get("CONTENT_LENGTH", ""),
      content_type=request.META.get("CONTENT_TYPE", ""),
      http_accept=request.META.get("HTTP_ACCEPT", ""),
      http_accept_encoding=request.META.get("HTTP_ACCEPT_ENCODING", ""),
      http_accept_language=request.META.get("HTTP_ACCEPT_LANGUAGE", ""),
      http_host=request.META.get("HTTP_HOST", ""),
      http_referer=request.META.get("HTTP_REFERER", ""),
      http_user_agent=request.META.get("HTTP_USER_AGENT", ""),
      remote_addr=request.META.get("REMOTE_ADDR", ""),
      remote_host=request.META.get("REMOTE_HOST", ""),
      remote_user=request.META.get("REMOTE_USER", ""),
      server_name=request.META.get("SERVER_NAME", ""),
      server_port=request.META.get("SERVER_PORT", ""),
      post_data=json.dumps(post),
      get_data=json.dumps(request.GET),
      cookies=json.dumps(request.COOKIES),
      encoding=request.encoding or "",
      is_ajax=request.is_ajax(),
    ).pk

    # lisää body pala kerrallaan
    for lohko in range(0, len(body), self.body_lohkokoko):
      UserRequest.objects.filter(
        pk=user_request_id
      ).update(
        body=functions.Concat(
          'body',
          Value(body[lohko:lohko+self.body_lohkokoko]),
          output_field=CharField(),
        ),
      )
    # def process_request

  # class LoggerMiddleware
