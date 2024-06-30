from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .forms import ExcelFileUploadForm, PublicExcelFileUploadForm
from .services.data_import import (
    import_black_list_from_excel,
    import_group_from_excel,
    import_keyword_from_excel,
    import_public_black_lists_from_excel,
    import_public_groups_from_excel,
    import_public_keywords_from_excel,
)


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


@login_required
def import_black_list_view(request):
    return import_base_view(
        request,
        import_function=import_black_list_from_excel,
        excel_columns=["BlackList", "Category"],
        title="Import Black Lists from excel",
    )


def import_public_base_view(request, *, import_function, excel_columns: list[str], title: str):
    if request.method == "POST":
        form = PublicExcelFileUploadForm(excel_columns, data=request.POST, files=request.FILES)
        if form.is_valid():
            excel_file = request.FILES["excel_file"]
            import_function(excel_file)
            return redirect("import:success")
    else:
        form = PublicExcelFileUploadForm(excel_columns)

    return render(
        request,
        "import/import_form_template.html",
        {"form": form, "title": title},
    )


@login_required
def import_public_keywords_view(request):
    return import_public_base_view(
        request,
        import_function=import_public_keywords_from_excel,
        excel_columns=["Keyword"],
        title="Import public keywords from excel",
    )


@login_required
def import_public_groups_view(request):
    return import_public_base_view(
        request,
        import_function=import_public_groups_from_excel,
        excel_columns=["Group"],
        title="Import public groups from excel",
    )


@login_required
def import_public_black_list_view(request):
    return import_public_base_view(
        request,
        import_function=import_public_black_lists_from_excel,
        excel_columns=["BlackList"],
        title="Import public black Lists from excel",
    )
