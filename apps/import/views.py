from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from apps.base.services.excel import import_group_from_excel, import_keyword_from_excel

from .forms import ExcelFileUploadForm


def import_base_view(request, *, import_function, excel_columns: list[str], title: str):
    if request.method == "POST":
        form = ExcelFileUploadForm(excel_columns, data=request.POST, files=request.FILES)
        if form.is_valid():
            excel_file = request.FILES["excel_file"]
            customer_id = request.POST["customer"]
            is_import_to_all = request.POST.get("is_import_to_all", False)
            import_function(excel_file, is_import_to_all, customer_id)
            return redirect("import:success")
    else:
        form = ExcelFileUploadForm(excel_columns)

    return render(
        request,
        "import/import_form_template.html",
        {"form": form, "title": title},
    )


@login_required
def import_keywords_view(request):
    return import_base_view(
        request,
        import_function=import_keyword_from_excel,
        excel_columns=["Keyword", "Category"],
        title="Import keywords from excel",
    )


@login_required
def import_groups_view(request):
    return import_base_view(
        request,
        import_function=import_group_from_excel,
        excel_columns=["Group", "Category"],
        title="Import groups from excel",
    )
