from django import forms


class SearchFoodForm(forms.Form):
    """
    model form for research of substitute from a food_name
    """

    product_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'type': 'text',
                'placeholder': 'Produit',
                'class': 'form-control js-scroll-trigger autocomplete',
                'id': 'product_name',
                'aria-describedby': 'basic-addon3',
            }
        )
    )
