from django.contrib import messages
from django.shortcuts import redirect, reverse, get_object_or_404, render
from contents import models as content_models
from django.contrib.auth.decorators import login_required
from . import forms, models
from django.views.generic import FormView


#이 부분 추가적으로 수정해야함
def CreateReviewView(request, content, *args, **kwargs):
    if request.method == 'POST':
        comment = models.Review()
        comment.review = request.POST['review']
        comment.content = content_models.Content.objects.get(pk=content) # id로 객체 가져오기
        comment.user = request.user
        if len(comment.review) > 0:
            comment.save()
        else:
            messages.error(request, "댓글을 입력하고 등록 버튼을 눌러주세요")
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
            messages.error(request, "댓글을 삭제할 수 없습니다")
        else:
            models.Review.objects.filter(pk=review_pk).delete()
            messages.success(request, "댓글이 삭제되었습니다")
        return redirect(reverse("contents:detail", kwargs={"pk": content_pk}))
    except models.Review.DoesNotExist:
        return redirect(reverse("core:home"))


@login_required
def edit_review(request, content_pk, review_pk):
    comment = models.Review.objects.get(pk=review_pk)
    if request.method == 'POST':
        comment.review = request.POST['review']
        comment.content = content_models.Content.objects.get(pk=content_pk) # id로 객체 가져오기
        comment.user = request.user
       
        if len(comment.review) > 0:
            comment.save()
        else:
            messages.error(request, "댓글을 입력하고 등록 버튼을 눌러주세요")
        return redirect(reverse("contents:detail", kwargs={"pk": content_pk}))

    else:
        messages.error(request, "비정상적인 접근입니다")
        return redirect('contents:detail')
