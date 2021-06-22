from django.db import models
from django.contrib.postgres.fields import ArrayField, DateTimeRangeField, JSONField


class Accountable(models.Model):
    description = models.TextField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    def __str__(self):
        return str(self.id)

    class Meta:
        managed = False
        db_table = "accountables"


ACCOUNT_STATUS = (
    ("pending", "pending"),
    ("under-review", "under-review"),
    ("approved", "approved"),
    ("rejected", "rejected"),
)


class AbstractAccount(models.Model):
    accountable = models.ForeignKey(Accountable, models.DO_NOTHING)
    status = models.TextField(choices=ACCOUNT_STATUS, default="pending")
    line_of_credit = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    tos_acceptance = JSONField(blank=True, null=True)
    banking = JSONField(blank=True, default=dict)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    sys_period = DateTimeRangeField(blank=True)

    def __str__(self):
        return str(self.id)

    class Meta:
        abstract = True


class Account(AbstractAccount):
    class Meta:
        managed = False
        db_table = "accounts"


class AccountHistory(AbstractAccount):
    class Meta:
        managed = False
        db_table = "accounts_history"


class Beneficiary(models.Model):
    business_id = models.TextField()
    is_default = models.BooleanField(unique=True)
    bank_code = models.TextField()
    bank_account = models.TextField()
    bank_branch = models.TextField()

    def __str__(self):
        return self.business_id

    class Meta:
        managed = False
        db_table = "beneficiaries"


class AbstractBusiness(models.Model):
    business_id = models.TextField()
    name = models.TextField()
    legal_name = models.TextField()
    address = JSONField(null=False)
    contact_info = JSONField(null=False)
    banking = JSONField(blank=True, default=dict)
    documents = JSONField(null=True)
    verification = JSONField(blank=True, null=True)
    account = models.OneToOneField(Account, models.DO_NOTHING, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    sys_period = DateTimeRangeField(blank=True)

    def __str__(self):
        return self.business_id

    class Meta:
        abstract = True


class Business(AbstractBusiness):
    class Meta:
        managed = False
        db_table = "businesses"


class BusinessHistory(AbstractBusiness):
    class Meta:
        managed = False
        db_table = "businesses_history"


class Client(models.Model):
    username = models.TextField(unique=True)
    password = models.TextField()
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    last_login = models.DateTimeField(blank=True, null=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.username)

    class Meta:
        managed = False
        db_table = "clients"


class DataBroker(models.Model):
    broker_id = models.TextField()
    broker = models.TextField()
    data = models.TextField(blank=True, null=True)  # This field type is a guess.
    created_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = "data_broker"


class Integration(models.Model):
    integration_name = models.TextField()
    event = models.TextField()
    param_name = models.TextField()
    param_value = models.TextField()
    data = JSONField(null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = "integrations"


class AbstractLoan(models.Model):
    id = models.UUIDField(primary_key=True)
    accountable = models.ForeignKey(Accountable, models.DO_NOTHING)
    offer_token = models.TextField(unique=True)
    signature = JSONField(blank=True, null=True)
    account = models.ForeignKey(Account, models.DO_NOTHING)
    created_at = models.DateTimeField()
    sys_period = DateTimeRangeField(blank=True)

    def __str__(self):
        return str(self.id)

    class Meta:
        abstract = True


class Loan(AbstractLoan):
    class Meta:
        managed = False
        db_table = "loans"


class LoanHistory(AbstractLoan):
    class Meta:
        managed = False
        db_table = "loans_history"


class Payment(models.Model):
    payment_id = models.TextField(unique=True)
    created_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = "payments"


class AbstractPerson(models.Model):
    first_name = models.TextField()
    last_name = models.TextField()
    id_number = models.TextField()
    address = JSONField()
    contact_info = JSONField()
    banking = JSONField(default=dict)
    documents = JSONField(blank=True, null=True)
    verification = JSONField(blank=True, null=True)
    marital_status = models.TextField()
    pep = models.BooleanField()
    account_opener = models.BooleanField()
    account = models.ForeignKey(Account, models.DO_NOTHING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    sys_period = DateTimeRangeField(blank=True)

    def __str__(self):
        return "{0} {1}".format(self.first_name, self.last_name)

    class Meta:
        abstract = True


class Person(AbstractPerson):
    class Meta:
        managed = False
        db_table = "persons"


class PersonsHistory(AbstractPerson):
    class Meta:
        managed = False
        db_table = "persons_history"


class AbstractRefreshToken(models.Model):
    account = models.ForeignKey(
        Account, models.DO_NOTHING, unique=True, blank=True, null=True
    )
    client = models.ForeignKey(
        Client, models.DO_NOTHING, unique=True, blank=True, null=True
    )
    token = models.TextField(unique=True)
    valid = models.BooleanField(null=True, default=True)
    exp = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    sys_period = DateTimeRangeField()

    def __str__(self):
        if self.account:
            return "{} (account)".format(self.token)
        elif self.client:
            return "{} (client)".format(self.token)
        else:
            return "{} (??)".format(self.token)

    class Meta:
        abstract = True


class RefreshToken(AbstractRefreshToken):
    class Meta:
        managed = False
        db_table = "refresh_tokens"


class RefreshTokensHistory(AbstractRefreshToken):
    class Meta:
        managed = False
        db_table = "refresh_tokens_history"


class SchemaMigration(models.Model):
    id = models.BigIntegerField(primary_key=True)
    applied = models.DateTimeField(blank=True, null=True)
    description = models.CharField(max_length=1024, blank=True, null=True)

    def __str__(self):
        return self.description

    class Meta:
        managed = False
        db_table = "schema_migrations"


class Transaction(models.Model):
    credit_to = models.ForeignKey(
        Accountable,
        models.DO_NOTHING,
        db_column="credit_to",
        related_name="accountable_credit",
    )
    debit_to = models.ForeignKey(
        Accountable,
        models.DO_NOTHING,
        db_column="debit_to",
        related_name="accountable_debit",
    )
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = False
        db_table = "transactions"


class Users(models.Model):
    username = models.TextField(unique=True, blank=True, null=True)
    password = models.TextField()
    is_active = models.BooleanField(blank=True, null=True)
    is_superuser = models.BooleanField(blank=True, null=True)
    is_staff = models.BooleanField(blank=True, null=True)
    last_login = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = "users"


class WebhookEndpoint(models.Model):
    url = models.URLField()
    status = models.TextField(default="enabled")
    events = ArrayField(models.CharField(max_length=255, blank=True))
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        managed = False
        db_table = "webhook_endpoints"
