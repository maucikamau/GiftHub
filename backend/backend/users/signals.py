"""User signals for synchronizing with StreamChat."""
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from stream_chat import StreamChat

from .models import User


@receiver(post_save, sender=User)
def sync_user_to_streamchat(sender, instance, created, **kwargs):
    """
    Automatically sync user data to StreamChat when a user is created or updated.

    Args:
        sender: The model class (User)
        instance: The actual user instance being saved
        created: Boolean indicating if this is a new user
        **kwargs: Additional keyword arguments
    """
    try:
        # Initialize StreamChat client
        client = StreamChat(
            api_key=settings.STREAM_API_KEY,
            api_secret=settings.STREAM_API_SECRET
        )

        # Prepare user data for Stream
        user_data = {
            "id": str(instance.chat_uid),
            "name": instance.username or instance.email,
            "email": instance.email,
            "internalId": instance.id,
        }

        # Add optional fields if they exist
        if instance.first_name:
            user_data["first_name"] = instance.first_name
        if instance.last_name:
            user_data["last_name"] = instance.last_name

        # Create or update user in StreamChat
        client.upsert_user(user_data)

        print(f"✅ User {instance.email} synced to StreamChat (created={created})")

    except Exception as e:
        # Log the error but don't prevent user save from completing
        print(f"❌ Error syncing user {instance.email} to StreamChat: {str(e)}")
