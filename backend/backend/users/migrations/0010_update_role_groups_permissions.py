from django.db import migrations


def update_role_groups(apps, schema_editor):

    Group = apps.get_model('auth', 'Group')
    Permission = apps.get_model('auth', 'Permission')

    # Ensure permissions are created for all apps
    # This is necessary when running in tests or isolated migration environments
    from django.contrib.auth.management import create_permissions

    for app_config in apps.get_app_configs():
        app_config.models_module = True  # Ensure models are loaded
        create_permissions(app_config, verbosity=0)

    # Map group name -> list of (app_label, codename) tuples
    groups_perms = {
        'donor': [
            ('users', 'can_access_basic_info'),

            ('listings', 'add_listing'),
            ('listings', 'change_listing'),
            ('listings', 'view_listing'),
            ('listings', 'delete_listing'),

            ('chat', 'view_chatchannel'),
            ('chat', 'add_chatchannel'),

            ('reviews', 'view_review'),
        ],
        'recipient_individual': [
            ('users', 'can_access_basic_info'),

            ('listings', 'view_listing'),

            ('payments', 'add_payment'),
            ('payments', 'view_payment'),

            ('chat', 'view_chatchannel'),
            ('chat', 'add_chatchannel'),

            ('reviews', 'add_review'),
            ('reviews', 'view_review'),
        ],
        'recipient_association': [
            ('users', 'can_access_basic_info'),
            ('users', 'can_access_udruga_additional_info'),

            ('listings', 'view_listing'),

            ('campaigns', 'add_campaign'),
            ('campaigns', 'change_campaign'),
            ('campaigns', 'view_campaign'),
            ('campaigns', 'delete_campaign'),

            ('payments', 'add_payment'),
            ('payments', 'view_payment'),

            ('chat', 'view_chatchannel'),
            ('chat', 'add_chatchannel'),

            ('reviews', 'add_review'),
            ('reviews', 'view_review'),
        ],
        'recipient': [
            ('users', 'can_access_basic_info'),

            ('listings', 'view_listing'),

            ('campaigns', 'view_campaign'),

            ('payments', 'add_payment'),
            ('payments', 'view_payment'),

            ('chat', 'view_chatchannel'),
            ('chat', 'add_chatchannel'),

            ('reviews', 'add_review'),
            ('reviews', 'view_review'),
        ],
    }

    for group_name, perm_tuples in groups_perms.items():
        group, created = Group.objects.get_or_create(name=group_name)
        group.permissions.clear()

        for app_label, codename in perm_tuples:
            try:
                # Query permission directly by app_label and codename
                # This works because Django creates permissions with content_type__app_label
                perm = Permission.objects.filter(
                    content_type__app_label=app_label,
                    codename=codename
                ).first()

                if perm:
                    group.permissions.add(perm)
            except Exception as e:
                continue


def remove_role_groups(apps, schema_editor):
    """
    Reverse migration: remove all role groups.
    """
    Group = apps.get_model('auth', 'Group')
    for name in ['donor', 'recipient_individual', 'recipient_association', 'recipient']:
        try:
            group = Group.objects.get(name=name)
            group.delete()
            print(f"Deleted group '{name}'")
        except Group.DoesNotExist:
            pass


class Migration(migrations.Migration):

    dependencies = [
        # Users app - latest migration
        ('users', '0009_user_profile_image'),

        # Campaigns app - latest migration
        ('campaigns', '0003_campaign_end_date'),

        # Listings app - latest migration
        ('listings', '0005_rename_active_confirmed_donation_conversation_listing_confirmed_donation_conversation_and_more'),

        # Reviews app - latest migration
        ('reviews', '0002_review_for_listing'),

        # Chat app - latest migration
        ('chat', '0004_chatchannel_payment_request_msg_id'),

        # Payments app - latest migration
        ('payments', '0006_payment_name'),
    ]

    operations = [
        migrations.RunPython(update_role_groups, remove_role_groups),
    ]
