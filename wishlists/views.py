from django.shortcuts import redirect, reverse
from django.views.generic import TemplateView
from contents import models as content_models
from . import models


def toggle_content(request, content_pk):
    action = request.GET.get("action", None)
    content = content_models.Content.objects.get_or_none(pk=content_pk)
    if content is not None and action is not None:
        the_list, _ = models.Wishlist.objects.get_or_create(
            user=request.user, name="My Favourites Houses"
        )
        if action == "add":
            the_list.contents.add(content)
        elif action == "remove":
            the_list.contents.remove(content)
    return redirect(reverse("contents:detail", kwargs={"pk": content_pk}))


class SeeFavsView(TemplateView):

    template_name = "wishlists/wishlist_detail.html"
