from django import forms
from tinymce.widgets import TinyMCE
from .models import Post, Comment, Category


class TinyMCEWidget(TinyMCE):
    def use_required_attribute(self, *args):
        return False


class PostForm(forms.ModelForm):
    content = forms.CharField(
        widget=TinyMCEWidget(
            attrs={'required': False, 'cols': 20, 'rows': 10}
        )
    )

    class Meta:
        model = Post
        fields = ('title', 'overview', 'content', 'thumbnail', 'categories', 'previous_post', 'next_post')

    def __init__(self, *args, **kwargs):
        super(PostForm,self).__init__(*args, **kwargs)
        self.fields['previous_post'].empty_label = "Select Previous Post"
        self.fields['next_post'].empty_label = "Select Next Post"

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ('title',)

class CommentForm(forms.ModelForm):
    content = forms.CharField(widget=forms.Textarea(attrs={
        'class': 'form_control text-appear',
        'placeholder': 'Type your comment',
        'id': 'usercomment',
        'rows': '4',
        'cols': '90'
        }))
    class Meta:
        model = Comment
        fields = ('content',)