from django import forms
from django.forms.models import modelformset_factory
from products.models import Variation,Category
class ProductFilterForm(forms.Form):
    q = forms.CharField(label='Search', required=False)
    categories_id = forms.ModelMultipleChoiceField(
    label = 'Category',
    queryset=Category.objects.all(),
    widget=forms.CheckboxSelectMultiple(),
    required=False,
    )
    max_price = forms.DecimalField(max_digits=12, decimal_places=2,required=False)
    min_price = forms.DecimalField(max_digits=12, decimal_places=2,required=False)

class VariationInventoryForm(forms.ModelForm):
    # TODO: Define other fields here
    class Meta:
        model = Variation
        fields = ['price',"sale_price","inventory"]
VariationInventoryFormset = modelformset_factory(Variation, form = VariationInventoryForm, extra = 0)
