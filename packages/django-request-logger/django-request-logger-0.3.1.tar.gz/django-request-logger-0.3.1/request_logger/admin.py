#!/usr/bin/env python
# vi: et sw=2 fileencoding=utf-8
#============================================================================
# Request Logger
# Copyright (c) 2019 OneByte Oy (http://onebyte.fi)
#
# All rights reserved.
# Redistributions of files must retain the above copyright notice.
#
# @description [File description]
# @created     20.02.2019
# @author      Harry Karvonen <harry.karvonen@pispalanit.fi>
# @copyright   Copyright (c) OneByte Oy
# @license     All rights reserved
#============================================================================

from django.contrib import admin

from .models import UserRequest

class InputFilter(admin.SimpleListFilter):
  template = 'request_logger/admin/input_filter.html'

  def lookups(self, request, model_admin):
    # Dummy, required to show the filter.
    return ((),)

  def choices(self, changelist):
    # Grab only the "all" option.
    all_choice = next(super().choices(changelist))
    all_choice['query_parts'] = (
      (k, v)
      for k, v in changelist.get_filters_params().items()
      if k != self.parameter_name
    )
    yield all_choice

user_request_fields = (
  "user",
  "timestamp",
  "is_ajax",
  "method",
  "path",
  #"scheme",
  #"body",
  #"content_length",
  #"content_type",
  #"http_accept",
  #"http_accept_encoding",
  #"http_accept_language",
  "http_host",
  "http_referer",
  "http_user_agent",
  "remote_addr",
  #"remote_host",
  #"remote_user",
  "server_name",
  "server_port",
  #"post_data",
  #"get_data",
  #"cookies",
  #"encoding",
)

def create_filter(field_name):
  class _FieldFilter(InputFilter):
    parameter_name = field_name
    title = field_name

    def queryset(self, request, queryset):
      val = self.value()

      if not val:
        return

      search_field = self.parameter_name

      a, b = val.startswith("*"), val.endswith("*")

      if a and b:
        search_field += "__icontains"
        val = val[1:-1]
      elif a:
        search_field += "__iendswith"
        val = val[1:]
      elif b:
        search_field += "__istartswith"
        val = val[:-1]

      return queryset.filter(
        **{search_field: val}
      )

  return _FieldFilter
  # def create_filter

class UserRequestAdmin(admin.ModelAdmin):
  list_filter = tuple(create_filter(f) for f in user_request_fields)
  list_display = user_request_fields
  show_full_result_count = False

admin.site.register(UserRequest, UserRequestAdmin)
