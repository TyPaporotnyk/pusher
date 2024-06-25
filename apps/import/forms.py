from django import forms
from django.core.validators import FileExtensionValidator

from apps.base.services.excel import get_excel_file_not_contains_columns
from apps.customers.models import Customer


class ExcelFileUploadForm(forms.Form):
    excel_file = forms.FileField(
        label="Select an Excel file", validators=[FileExtensionValidator(allowed_extensions=["xlsx", "xls"])]
    )
    customer = forms.ModelChoiceField(
        queryset=Customer.objects.all().order_by("username"), required=False, label="Customer"
    )
    is_import_to_all = forms.BooleanField(required=False, label="Import to all customers")

    def __init__(self, excel_columns: list[str], *args, **kwargs):
        super(ExcelFileUploadForm, self).__init__(*args, **kwargs)

        self.excel_columns = excel_columns

    def clean_excel_file(self):
        excel_file = self.cleaned_data.get("excel_file")

        not_contained_columns = get_excel_file_not_contains_columns(excel_file, self.excel_columns)
        if not_contained_columns:
            raise forms.ValidationError(message=f"Excel file not contained {','.join(not_contained_columns)} columns")

        return excel_file

    def clean(self):
        cleaned_data = super().clean()
        customer = cleaned_data.get("customer")
        is_import_to_all = cleaned_data.get("is_import_to_all")

        if not customer and not is_import_to_all:
            raise forms.ValidationError("You must either select a customer or choose to import to all customers.")

        return cleaned_data
