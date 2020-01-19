# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class TblCategory(models.Model):
    code = models.CharField(primary_key=True, max_length=255)
    keyword = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tbl_category'


class TblClickHistory(models.Model):
    no = models.AutoField(primary_key=True)
    regdate = models.DateTimeField(blank=True, null=True)
    community_crawling_no = models.ForeignKey('TblCommunityCrawling', models.DO_NOTHING, db_column='community_crawling_no', blank=True, null=True)
    member_mid = models.ForeignKey('TblMember', models.DO_NOTHING, db_column='member_mid', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tbl_click_history'


class TblCommunityCrawling(models.Model):
    no = models.AutoField(primary_key=True)
    regdate = models.DateTimeField(blank=True, null=True)
    last_crawling = models.TextField()  # This field type is a guess.
    fee = models.IntegerField(blank=True, null=True)
    image = models.CharField(max_length=1000, blank=True, null=True)
    link = models.CharField(max_length=1000, blank=True, null=True)
    price = models.IntegerField(blank=True, null=True)
    title = models.CharField(max_length=255, blank=True, null=True)
    category_code = models.ForeignKey(TblCategory, models.DO_NOTHING, db_column='category_code', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tbl_community_crawling'


class TblExecuteHistory(models.Model):
    no = models.AutoField(primary_key=True)
    regdate = models.DateTimeField(blank=True, null=True)
    member_mid = models.ForeignKey('TblMember', models.DO_NOTHING, db_column='member_mid', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tbl_execute_history'


class TblInterest(models.Model):
    mid = models.ForeignKey('TblMember', models.DO_NOTHING, db_column='mid')
    keyword = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tbl_interest'


class TblLowprice(models.Model):
    lno = models.AutoField(primary_key=True)
    regdate = models.DateTimeField(blank=True, null=True)
    fee = models.IntegerField(blank=True, null=True)
    image = models.CharField(max_length=1000, blank=True, null=True)
    link = models.CharField(max_length=1000, blank=True, null=True)
    price = models.IntegerField(blank=True, null=True)
    title = models.CharField(max_length=255, blank=True, null=True)
    category_code = models.ForeignKey(TblCategory, models.DO_NOTHING, db_column='category_code', blank=True, null=True)
    pno = models.ForeignKey('TblPick', models.DO_NOTHING, db_column='pno', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tbl_lowprice'


class TblMarket(models.Model):
    mcode = models.CharField(primary_key=True, max_length=255)
    url_title = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tbl_market'


class TblMember(models.Model):
    mid = models.CharField(primary_key=True, max_length=255)
    regdate = models.DateTimeField(blank=True, null=True)
    age_group = models.CharField(max_length=255, blank=True, null=True)
    role = models.CharField(max_length=255)
    sex = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tbl_member'


class TblPick(models.Model):
    pno = models.AutoField(primary_key=True)
    regdate = models.DateTimeField(blank=True, null=True)
    fee = models.IntegerField(blank=True, null=True)
    image = models.CharField(max_length=1000, blank=True, null=True)
    link = models.CharField(max_length=1000, blank=True, null=True)
    current_price = models.IntegerField(blank=True, null=True)
    title = models.CharField(max_length=255, blank=True, null=True)
    receipt = models.TextField(blank=True, null=True)  # This field type is a guess.
    state = models.TextField(blank=True, null=True)  # This field type is a guess.
    wanted_price = models.IntegerField(blank=True, null=True)
    member_mid = models.ForeignKey(TblMember, models.DO_NOTHING, db_column='member_mid', blank=True, null=True)
    category_code = models.ForeignKey(TblCategory, models.DO_NOTHING, db_column='category_code', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tbl_pick'


class TblToken(models.Model):
    token = models.CharField(primary_key=True, max_length=255)
    mid = models.ForeignKey(TblMember, models.DO_NOTHING, db_column='mid', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tbl_token'
