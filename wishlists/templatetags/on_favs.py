
from django import template
from wishlists import models as wishlist_models

register = template.Library()


@register.simple_tag(takes_context=True)
def on_favs(context, content):
    user = context.request.user
    the_list = wishlist_models.Wishlist.objects.get_or_none(
        user=user, name="My Favourites Houses"
    )
    if the_list is not None:
        return content in the_list.contents.all()
    else:
        pass