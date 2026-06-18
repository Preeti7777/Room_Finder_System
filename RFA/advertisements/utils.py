from .models import Advertisement


def get_active_ads(position, limit=None):
    ads = Advertisement.objects.filter(
        position=position,
        is_active=True
    )

    if limit:
        ads = ads[:limit]

    return ads


def get_phone_reveal_ad():
    return Advertisement.objects.filter(
        position='phone_reveal',
        ad_type='rewarded',
        is_active=True
    ).first()