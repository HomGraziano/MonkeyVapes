from django import forms
from .models import Item, Order, OrderItem
from django.forms.models import inlineformset_factory

class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['name', 'quantity', 'price']  

class OrderForm(forms.Form):
    client_name = forms.CharField(label='Client Name', max_length=100)

OrderItemFormSet = inlineformset_factory(
    Order,
    OrderItem,
    fields=('item', 'quantity'),
    extra=1,
    can_delete=False
)

class OrderItemForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        fields = ['item', 'quantity']
        labels = {
            'item': 'Producto',     
            'quantity': 'Cantidad',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Build choices with data-price attribute
        items = Item.objects.all()
        choices = []
        for item in items:
            choices.append((item.pk, item.name))
        self.fields['item'].queryset = items