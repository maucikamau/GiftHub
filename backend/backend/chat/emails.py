"""
Email utilities for chat/donation notifications.
"""
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags
import logging

logger = logging.getLogger(__name__)

def send_donation_accepted_email(chat_channel):
    """
    Send email to recipient when donor accepts their donation request.

    Args:
        chat_channel: ChatChannel instance
    """
    recipient = chat_channel.recipient
    donor = chat_channel.donor
    listing = chat_channel.listing

    subject = f'Donacija prihvaćena - {listing.title}'

    # Prepare context for template
    context = {
        'recipient_name': recipient.first_name or recipient.username,
        'donor_username': donor.username,
        'listing_title': listing.title,
        'listing_category': listing.category,
        'delivery_type_label': 'Osobno preuzimanje' if chat_channel.delivery_type == 'pickup' else 'Dostava o trošku primatelja',
        'is_pickup': chat_channel.delivery_type == 'pickup',
        'conversation_id': chat_channel.stream_channel_id,
    }

    # Render HTML template
    html_message = render_to_string('emails/donation_accepted.html', context)
    plain_message = strip_tags(html_message)

    try:
        send_mail(
            subject=subject,
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[recipient.email],
            html_message=html_message,
            fail_silently=False,
        )
        return True
    except Exception as e:
        logger.exception(e)
        print(f"Failed to send donation accepted email: {e}")
        return False


def send_donation_rejected_email(chat_channel):
    """
    Send email to recipient when donor rejects their donation request.

    Args:
        chat_channel: ChatChannel instance
    """
    recipient = chat_channel.recipient
    donor = chat_channel.donor
    listing = chat_channel.listing

    subject = f'Donacija odbijena - {listing.title}'

    # Prepare context for template
    context = {
        'recipient_name': recipient.first_name or recipient.username,
        'donor_username': donor.username,
        'listing_title': listing.title,
        'listing_category': listing.category,
        'conversation_id': chat_channel.stream_channel_id,
    }

    # Render HTML template
    html_message = render_to_string('emails/donation_rejected.html', context)
    plain_message = strip_tags(html_message)

    try:
        send_mail(
            subject=subject,
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[recipient.email],
            html_message=html_message,
            fail_silently=False,
        )
        return True
    except Exception as e:
        logger.exception(e)
        print(f"Failed to send donation rejected email: {e}")
        return False


def send_donation_request_received_email(chat_channel):
    """
    Send email to donor when they receive a new donation request.

    Args:
        chat_channel: ChatChannel instance
    """
    recipient = chat_channel.recipient
    donor = chat_channel.donor
    listing = chat_channel.listing

    subject = f'Novi zahtjev za donaciju - {listing.title}'

    # Prepare context for template
    context = {
        'donor_name': donor.first_name or donor.username,
        'recipient_username': recipient.username,
        'listing_title': listing.title,
        'listing_category': listing.category,
        'delivery_type_label': 'Osobno preuzimanje' if chat_channel.delivery_type == 'pickup' else 'Dostava o trošku primatelja',
        'conversation_id': chat_channel.stream_channel_id,
    }

    # Render HTML template
    html_message = render_to_string('emails/donation_request_received.html', context)
    plain_message = strip_tags(html_message)

    try:
        send_mail(
            subject=subject,
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[donor.email],
            html_message=html_message,
            fail_silently=False,
        )
        return True
    except Exception as e:
        logger.exception(e)

        print(f"Failed to send donation request received email: {e}")
        return False


def send_donation_cancelled_email(listing, recipient, donor, conversation_id):
    """
    Send email to donor when recipient cancels the donation.

    Args:
        listing: Listing instance
        recipient: User instance (who cancelled)
        donor: User instance (who will receive the email)
    """
    subject = f'Donacija otkazana - {listing.title}'

    # Prepare context for template
    context = {
        'donor_name': donor.first_name or donor.username,
        'recipient_username': recipient.username,
        'listing_title': listing.title,
        'listing_category': listing.category,
        'conversation_id': conversation_id,
    }

    # Render HTML template
    html_message = render_to_string('emails/donation_cancelled.html', context)
    plain_message = strip_tags(html_message)

    try:
        send_mail(
            subject=subject,
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[donor.email],
            html_message=html_message,
            fail_silently=False,
        )
        return True
    except Exception as e:
        logger.exception(e)
        print(f"Failed to send donation cancelled email: {e}")
        return False

