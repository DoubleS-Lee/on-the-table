from django.contrib import messages
from django.shortcuts import redirect, reverse, get_object_or_404, render
from contents import models as content_models
from django.contrib.auth.decorators import login_required
from . import forms, models
from django.views.generic import FormView


'''
def CreateReviewView(request, content_id):
    content = get_object_or_404(Content, pk=content_id)
    if request.method == 'POST':
        comment_form = forms.ReviewForm(request.POST)
        comment_form.instance.user_id = request.user.id
        comment_form.instance.content_id = content_id
        if comment_form.is_valid():
            comment = comment_form.save()
                
    comment_form = forms.ReviewForm()
    comments = content.reviews.all()

    return render(request, 'contents/content_detail.html', {'object':content, "comments":comments, "comment_form":comment_form})
'''

#이 부분 추가적으로 수정해야함
def CreateReviewView(request, content, *args, **kwargs):
            if request.method == 'POST':
                comment = models.Review()
                comment.review = request.POST['review']
                comment.content = content_models.Content.objects.get(pk=content) # id로 객체 가져오기
                comment.user = request.user
                comment.save()
                return redirect(reverse("contents:detail", kwargs={"pk": content}))
            else:
                messages.error(request, "비정상적인 접근입니다")
                return redirect('contents:detail')


@login_required
def delete_review(request, content_pk, review_pk):
    user = request.user
    try:
        review = models.Review.objects.get(pk=review_pk)
        if review.user.pk != user.pk:
            messages.error(request, "리뷰를 삭제할 수 없습니다")
        else:
            models.Review.objects.filter(pk=review_pk).delete()
            messages.success(request, "리뷰가 삭제되었습니다")
        return redirect(reverse("contents:detail", kwargs={"pk": content_pk}))
    except models.Content.DoesNotExist:
        return redirect(reverse("core:home"))

'''
@login_required
def delete_photo(request, content_pk, photo_pk):
    user = request.user
    try:
        content = models.Content.objects.get(pk=content_pk)
        if content.user.pk != user.pk:
            messages.error(request, "Cant delete that photo")
        else:
            models.Photo.objects.filter(pk=photo_pk).delete()
            messages.success(request, "Photo Deleted")
        return redirect(reverse("contents:photos", kwargs={"pk": content_pk}))
    except models.Content.DoesNotExist:
        return redirect(reverse("core:home"))
'''