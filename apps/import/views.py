from django.shortcuts import redirect, render

from .forms import ExcelFileUploadForm
from .services.excel import import_group_from_excel, import_keyword_from_excel


def import_base_view(request, *, import_function, title: str):
    if request.method == "POST":
        form = ExcelFileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            excel_file = request.FILES["excel_file"]
            import_function(
                excel_file,
            )
            return redirect("import:success")
    else:
        form = ExcelFileUploadForm()

    return render(
        request,
        "import/import_form_template.html",
        {"form": form, "title": title},
    )


def import_keywords_view(request):
    return import_base_view(
        request,
        import_function=import_keyword_from_excel,
        title="Import keywords from excel",
    )


def import_groups_view(request):
    return import_base_view(
        request,
        import_function=import_group_from_excel,
        title="Import groups from excel",
    )
