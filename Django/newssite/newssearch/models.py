# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
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
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
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
    id = models.BigAutoField(primary_key=True)
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


class TbComment(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    newsid = models.ForeignKey('TbNews', models.DO_NOTHING, db_column='NewsID')  # Field name made lowercase.
    userid = models.ForeignKey('TbUser', models.DO_NOTHING, db_column='UserID')  # Field name made lowercase.
    writedat = models.DateTimeField(db_column='WritedAt', blank=True, null=True)  # Field name made lowercase.
    content = models.TextField(db_column='Content', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'tb_comment'


class TbCommentTeam4(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    newsid = models.IntegerField(db_column='NewsID')  # Field name made lowercase.
    userid = models.IntegerField(db_column='UserID')  # Field name made lowercase.
    writedat = models.DateTimeField(db_column='WritedAt', blank=True, null=True)  # Field name made lowercase.
    content = models.TextField(db_column='Content', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'tb_comment_team_4'


class TbDomain(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    name = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tb_domain'


class TbNews(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    domainid = models.ForeignKey(TbDomain, models.DO_NOTHING, db_column='DomainID')  # Field name made lowercase.
    maincategory = models.CharField(db_column='MainCategory', max_length=16, blank=True, null=True)  # Field name made lowercase.
    subcategory = models.CharField(db_column='SubCategory', max_length=16, blank=True, null=True)  # Field name made lowercase.
    writedat = models.DateTimeField(db_column='WritedAt', blank=True, null=True)  # Field name made lowercase.
    title = models.CharField(db_column='Title', max_length=128, blank=True, null=True)  # Field name made lowercase.
    content = models.TextField(db_column='Content')  # Field name made lowercase.
    url = models.CharField(db_column='URL', max_length=255, blank=True, null=True)  # Field name made lowercase.
    photourl = models.TextField(db_column='PhotoURL', blank=True, null=True)  # Field name made lowercase.
    writer = models.CharField(db_column='Writer', max_length=16, blank=True, null=True)  # Field name made lowercase.
    stickers = models.TextField(db_column='Stickers', blank=True, null=True)  # Field name made lowercase.
    press = models.CharField(db_column='Press', max_length=16, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'tb_news'


class TbNewsTeam4(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    domainid = models.IntegerField(db_column='DomainID')  # Field name made lowercase.
    maincategory = models.CharField(db_column='MainCategory', max_length=16, blank=True, null=True)  # Field name made lowercase.
    subcategory = models.CharField(db_column='SubCategory', max_length=16, blank=True, null=True)  # Field name made lowercase.
    writedat = models.DateTimeField(db_column='WritedAt', blank=True, null=True)  # Field name made lowercase.
    title = models.CharField(db_column='Title', max_length=128, blank=True, null=True)  # Field name made lowercase.
    content = models.TextField(db_column='Content')  # Field name made lowercase.
    url = models.CharField(db_column='URL', max_length=255, blank=True, null=True)  # Field name made lowercase.
    photourl = models.TextField(db_column='PhotoURL', blank=True, null=True)  # Field name made lowercase.
    writer = models.CharField(db_column='Writer', max_length=16, blank=True, null=True)  # Field name made lowercase.
    stickers = models.TextField(db_column='Stickers', blank=True, null=True)  # Field name made lowercase.
    press = models.CharField(db_column='Press', max_length=16, blank=True, null=True)  # Field name made lowercase.
    cossimilarity = models.TextField(db_column='CosSimilarity', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'tb_news_team_4'


class TbUser(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    domainid = models.ForeignKey(TbDomain, models.DO_NOTHING, db_column='DomainID', blank=True, null=True)  # Field name made lowercase.
    userid = models.CharField(db_column='UserID', max_length=16, blank=True, null=True)  # Field name made lowercase.
    username = models.CharField(db_column='UserName', max_length=32, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'tb_user'

class TbUserTeam4(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    domainid = models.IntegerField(db_column='DomainID', blank=True, null=True)  # Field name made lowercase.
    userid = models.CharField(db_column='UserID', max_length=16, blank=True, null=True)  # Field name made lowercase.
    username = models.CharField(db_column='UserName', max_length=32, blank=True, null=True)  # Field name made lowercase.
    cossimilarity = models.TextField(db_column='CosSimilarity', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'tb_user_team_4'