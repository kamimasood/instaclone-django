from django import forms
from .models import Post

class PostForm(forms.ModelForm):
    """Form for creating and editing posts."""
    class Meta:
        model = Post
        fields = ['image', 'video', 'caption']
        widgets = {
            'caption': forms.Textarea(attrs={'rows': 3,
                                             'placeholder': 'Write a caption...'}),
        }
