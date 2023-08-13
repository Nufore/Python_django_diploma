from django import forms
from django.core.validators import validate_image_file_extension
from django.utils.translation import gettext as _
from .models import Product, ProductImages


class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = single_file_clean(data, initial)
        return result


class ProductAdminForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = (
            "title",
            "description",
            "fullDescription",
            "price",
            "count",
            "category",
            "tags",
            "freeDelivery",
            "sale",
        )

    # images = forms.FileField(
    #     widget=MultipleFileInput(attrs={"multiple": False}),
    #     label=_("Add images"),
    #     required=False,
    # )

    images = MultipleFileField(label=_("Add images"), required=False)

    def clean_images(self):
        """Make sure only images can be uploaded."""
        for upload in self.files.getlist("images"):
            validate_image_file_extension(upload)

    def save_images(self, product):
        """Process each uploaded image."""
        for upload in self.files.getlist("images"):
            image = ProductImages(product=product, image=upload)
            image.save()
