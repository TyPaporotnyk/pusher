from django.shortcuts import redirect, render

from apps.customers.forms import ExcelUploadForm
from apps.customers.use_case.excel import import_group_from_excel, import_keyword_from_excel


def import_keywords_view(request):
    if request.method == "POST":
        form = ExcelUploadForm(request.POST, request.FILES)
        if form.is_valid():
            excel_file = request.FILES["excel_file"]
            import_keyword_from_excel(
                excel_file,
            )
            return redirect("import_success")
    else:
        form = ExcelUploadForm()

    return render(
        request,
        "customers/load_model_from_file.html",
        {"form": form},
    )


def import_groups_view(request):
    if request.method == "POST":
        form = ExcelUploadForm(request.POST, request.FILES)
        if form.is_valid():
            excel_file = request.FILES["excel_file"]
            import_group_from_excel(
                excel_file,
            )
            return redirect("import_success")
    else:
        form = ExcelUploadForm()

    return render(
        request,
        "customers/load_model_from_file.html",
        {"form": form},
    )
