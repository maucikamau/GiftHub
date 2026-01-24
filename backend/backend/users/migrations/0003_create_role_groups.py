from django.db import migrations


def create_role_groups(apps, schema_editor):
    Group = apps.get_model('auth', 'Group')
    Permission = apps.get_model('auth', 'Permission')

    # Map group name -> list of permission codenames to attach
    groups_perms = {
        'donor': [
            'can_access_basic_info',
            'add_listing',
            'change_listing',
            'view_listing',
            'delete_listing',
        ],
        'recipient_individual': [
            'can_access_basic_info',
            'view_listing',
        ],
        'recipient_association': [
            'can_access_basic_info',
            'can_access_udruga_additional_info',
            'view_listing',
        ],
        # keep a plain recipient group in case some users use that role
        'recipient': [],
    }

    for group_name, perm_codenames in groups_perms.items():
        group, created = Group.objects.get_or_create(name=group_name)
        for codename in perm_codenames:
            try:
                perm = Permission.objects.get(codename=codename)
            except Permission.DoesNotExist:
                # permission might not yet exist in rare ordering cases; skip safely
                print("Permission with codename", codename, "does not exist, skipping...")
                continue
            group.permissions.add(perm)


def remove_role_groups(apps, schema_editor):
    Group = apps.get_model('auth', 'Group')
    for name in ['donor', 'recipient_individual', 'recipient_association', 'recipient']:
        try:
            g = Group.objects.get(name=name)
            g.delete()
        except Exception:
            pass


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_remove_user_type_alter_user_role'),
    ]

    operations = [
        migrations.RunPython(create_role_groups, remove_role_groups),
    ]

