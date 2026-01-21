from django import forms
from apps.store.models import Address

class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = [
            "full_name", "phone",
            "address_line1", "address_line2",
            "city", "state", "pincode",
            "is_primary"
        ]

        widgets = {
    "full_name": forms.TextInput(attrs={
        "class": "w-full rounded-lg border border-gray-300 px-4 py-2 focus:border-yellow-500 focus:ring-2 focus:ring-yellow-200 outline-none",
        "placeholder": "e.g. Jay Shah"
    }),

    "phone": forms.TextInput(attrs={
        "class": "w-full rounded-lg border border-gray-300 px-4 py-2 focus:border-yellow-500 focus:ring-2 focus:ring-yellow-200 outline-none",
        "placeholder": "e.g. +91 9876543210"
    }),

    "address_line1": forms.TextInput(attrs={
        "class": "w-full rounded-lg border border-gray-300 px-4 py-2 focus:border-yellow-500 focus:ring-2 focus:ring-yellow-200 outline-none",
        "placeholder": "House no., Building name, Street"
    }),

    "address_line2": forms.TextInput(attrs={
        "class": "w-full rounded-lg border border-gray-300 px-4 py-2 focus:border-yellow-500 focus:ring-2 focus:ring-yellow-200 outline-none",
        "placeholder": "Landmark, Area (optional)"
    }),

    "city": forms.TextInput(attrs={
        "class": "w-full rounded-lg border border-gray-300 px-4 py-2 focus:border-yellow-500 focus:ring-2 focus:ring-yellow-200 outline-none",
        "placeholder": "e.g. Ahmedabad"
    }),

    "state": forms.TextInput(attrs={
        "class": "w-full rounded-lg border border-gray-300 px-4 py-2 focus:border-yellow-500 focus:ring-2 focus:ring-yellow-200 outline-none",
        "placeholder": "e.g. Gujarat"
    }),

    "pincode": forms.TextInput(attrs={
        "class": "w-full rounded-lg border border-gray-300 px-4 py-2 focus:border-yellow-500 focus:ring-2 focus:ring-yellow-200 outline-none",
        "placeholder": "e.g. 380015"
    }),

    "is_primary": forms.CheckboxInput(attrs={
        "class": "w-4 h-4"
    }),
}
