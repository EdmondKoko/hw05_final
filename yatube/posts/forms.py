from django import forms

from .models import Post, Comment


class PostForm(forms.ModelForm):
    text = forms.CharField(widget=forms.Textarea,
                           required=True,
                           label='Текст поста',
                           help_text='Текст нового поста')

    class Meta:
        model = Post
        fields = ('text', 'group', 'image')
        labels = {
            'group': 'Группа',
            'image': 'Изображение',
        }
        help_texts = {
            'group': 'Группа, к которой будет относиться пост',
            'image': 'Вы можете добавить изображение к вашему посту',
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)
        labels = {
            "post": "Пост",
            "author": "Комментатор",
            "text": "Текст",
        }

        help_texts = {
            "post": "Текст поста",
            "author": "Автор комментария",
            "text": "Текст комментария",
        }
