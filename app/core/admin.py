from django.contrib import admin
from django.apps import apps
from django.contrib.postgres.fields import JSONField
from prettyjson import PrettyJSONWidget
from core import models


# Inlines


class BusinessInline(admin.StackedInline):
    model = models.Business
    extra = 0
    formfield_overrides = {JSONField: {"widget": PrettyJSONWidget}}


class LoanInline(admin.TabularInline):
    model = models.Loan
    extra = 0
    formfield_overrides = {JSONField: {"widget": PrettyJSONWidget}}


class PersonInline(admin.StackedInline):
    model = models.Person
    extra = 0
    formfield_overrides = {JSONField: {"widget": PrettyJSONWidget}}


# Models


@admin.register(models.Account)
class AccountAdmin(admin.ModelAdmin):
    inlines = (BusinessInline, PersonInline, LoanInline)
    list_display = ("id", "status", "line_of_credit", "created_at")
    formfield_overrides = {JSONField: {"widget": PrettyJSONWidget}}


@admin.register(models.Business)
class BusinessAdmin(admin.ModelAdmin):
    list_display = ("business_id", "id", "name", "legal_name", "account", "created_at")
    formfield_overrides = {JSONField: {"widget": PrettyJSONWidget}}


@admin.register(models.Loan)
class LoanAdmin(admin.ModelAdmin):
    list_display = ("id", "account", "token", "signature", "created_at")
    formfield_overrides = {JSONField: {"widget": PrettyJSONWidget}}

    def token(self, obj):
        return obj.offer_token[:75] + (obj.offer_token[75:] and "..")


@admin.register(models.Person)
class PersonAdmin(admin.ModelAdmin):
    formfield_overrides = {JSONField: {"widget": PrettyJSONWidget}}


# Temporal tables


@admin.register(models.AccountHistory)
class AccountHistoryAdmin(admin.ModelAdmin):
    list_display = ("id", "status", "line_of_credit", "created_at")
    formfield_overrides = {JSONField: {"widget": PrettyJSONWidget}}


@admin.register(models.LoanHistory)
class LoanHistoryAdmin(admin.ModelAdmin):
    list_display = ("id", "account", "token", "signature", "created_at")
    formfield_overrides = {JSONField: {"widget": PrettyJSONWidget}}

    def token(self, obj):
        return obj.offer_token[:75] + (obj.offer_token[75:] and "..")


# Dynamically load the rest

models = apps.get_models()

for model in models:
    try:
        admin.site.register(model)
    except admin.sites.AlreadyRegistered:
        pass
