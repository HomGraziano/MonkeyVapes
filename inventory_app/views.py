from .models import Item, Client, Order, OrderItem
from .forms import ItemForm, OrderForm, OrderItemFormSet
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.forms import modelformset_factory
from .forms import OrderItemForm

OrderItemFormSet = modelformset_factory(OrderItem, form=OrderItemForm, extra=1)

def item_list(request):
    items = Item.objects.all()
    return render(request, 'inventory_app/item_list.html', {'items': items})

def item_create(request):
    if request.method == 'POST':
        form = ItemForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Item created successfully!")
            return redirect('item_list')
    else:
        form = ItemForm()
    return render(request, 'inventory_app/item_form.html', {'form': form})

def order_create(request):
    
    items = Item.objects.all()
    if request.method == 'POST':
        form = OrderForm(request.POST)
        formset = OrderItemFormSet(request.POST, queryset=OrderItem.objects.none())

        if not form.is_valid() or not formset.is_valid():
            print("Form errors:", form.errors)
            print("Formset errors:", formset.errors)
            
        if form.is_valid() and formset.is_valid():
            client_name = form.cleaned_data['client_name'].strip()
            client, _ = Client.objects.get_or_create(name=client_name)

            # Check stock availability
            order_quantities = {}
            for item_form in formset:
                if item_form.cleaned_data and not item_form.cleaned_data.get('DELETE', False):
                    item = item_form.cleaned_data['item']
                    qty = item_form.cleaned_data['quantity']
                    order_quantities[item] = order_quantities.get(item, 0) + qty

            for item, qty in order_quantities.items():
                if item.quantity < qty:
                    messages.error(request, f"Not enough stock for '{item.name}'. Available: {item.quantity}, requested: {qty}.")
                    return render(request, 'inventory_app/order_form.html', {'form': form, 'formset': formset})

            # Create order record
            order = Order.objects.create(client=client, total_amount=0)

            # Save each order item and reduce stock
            for item_form in formset:
                if item_form.cleaned_data and not item_form.cleaned_data.get('DELETE', False):
                    order_item = item_form.save(commit=False)
                    order_item.order = order
                    order_item.save()

                    item = order_item.item
                    item.quantity -= order_item.quantity
                    item.save()
            
            total = 0
            for item_form in formset:
                    if item_form.cleaned_data:
                        qty = item_form.cleaned_data['quantity']
                        item = item_form.cleaned_data['item']
                        total += qty * item.price

            order.total_amount = total
            order.save()

            messages.success(request, "Order created successfully!")
            return redirect('order_list')

    else:
        form = OrderForm()
        formset = OrderItemFormSet(queryset=OrderItem.objects.none())

    return render(request, 'inventory_app/order_form.html', {
        'form': form,
        'formset': formset,
        'items': items,
    })


def item_edit(request, pk):
    item = get_object_or_404(Item, pk=pk)
    if request.method == 'POST':
        form = ItemForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            messages.success(request, "Item updated successfully!")
            return redirect('item_list')
    else:
        form = ItemForm(instance=item)
    return render(request, 'inventory_app/item_form.html', {'form': form})

def order_list(request):
    orders = Order.objects.all().order_by('-id')  # newest first
    return render(request, 'inventory_app/order_list.html', {'orders': orders})

def order_detail(request, pk):
    order = get_object_or_404(Order, pk=pk)
    # Prepare items with subtotal
    order_items = []
    for item in order.items.all():
        subtotal = item.quantity * item.item.price
        order_items.append({
            'item': item.item,
            'quantity': item.quantity,
            'subtotal': subtotal,
        })
    return render(request, 'inventory_app/order_detail.html', {
        'order': order,
        'order_items': order_items,
    })

def item_delete(request, pk):
    item = get_object_or_404(Item, pk=pk)
    if item.orderitem_set.exists():
        messages.error(request, "This item is used in an order and cannot be deleted.")
    else:
        item.delete()
        messages.success(request, "Item deleted.")
    return redirect('item_list')

def order_delete(request, pk):
    order = get_object_or_404(Order, pk=pk)

    # Restore inventory
    for order_item in order.items.all():
        item = order_item.item
        item.quantity += order_item.quantity
        item.save()

    # Delete order
    order.delete()
    messages.success(request, "Order deleted and inventory restored.")
    return redirect('order_list')  # Or wherever your list of orders is