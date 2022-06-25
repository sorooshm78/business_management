# Create your views here.
from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.http import HttpRequest
from django.shortcuts import render
from jalali_date import date2jalali

from record.models import Record

MONTH = [
    'فروردین',
    'اردیبهشت',
    'خرداد',
    'تیر',
    'مرداد',
    'شهریور',
    'مهر',
    'آبان',
    'آذر',
    'دی',
    'بهمن',
    'اسفند',
]


def get_name_month():
    date_number = int(get_today_date()[5:7])
    return MONTH[date_number]


def get_today_date():
    return str(date2jalali(datetime.date(datetime.now()))).replace('-', '/')


def get_month_date():
    return str(date2jalali(datetime.date(datetime.now()))).replace('-', '/')[:8]


def get_year_date():
    return str(date2jalali(datetime.date(datetime.now()))).replace('-', '/')[:5]


def get_dict_total_record(date, records):
    sum_input = 0
    sum_output = 0
    for record in records:
        if record.record_type == 'input':
            sum_input += record.price
        elif record.record_type == 'output':
            sum_output += record.price
    return {
        'date': date,
        'sum_input': sum_input,
        'sum_output': sum_output,
        'remaining': sum_input - sum_output,
    }


def get_records_by_date(request, repo_id, date):
    return Record.objects.filter(
        date__contains=date,
        repository_id=repo_id,
        repository__user_id=request.user.id
    ).order_by('date')


def get_dict_today(request, repo_id):
    date = get_today_date()
    today_records = get_records_by_date(request, repo_id, date)
    return get_dict_total_record(date, today_records)


def get_dict_month(request, repo_id):
    date = get_month_date()
    month_records = get_records_by_date(request, repo_id, date)
    return get_dict_total_record(get_name_month(), month_records)


def get_dict_year(request, repo_id):
    date = get_year_date()
    years_records = get_records_by_date(request, repo_id, date)
    return get_dict_total_record(date[:-1], years_records)


@login_required
def detail_reports_view(request: HttpRequest, repo_id):
    date = request.GET.get('date')
    records = None
    if date == 'today':
        records = get_records_by_date(request, repo_id, get_today_date())
    if date == 'month':
        records = get_records_by_date(request, repo_id, get_month_date())
    if date == 'year':
        records = get_records_by_date(request, repo_id, get_year_date())

    return render(
        request,
        'report/detail_report.html', {
            'records': records,
            'repo_id': repo_id,
        }
    )


@login_required
def report_view(request: HttpRequest, repo_id):
    return render(
        request,
        'report/report.html', {
            'repo_id': repo_id,
            'today': get_dict_today(request, repo_id),
            'month': get_dict_month(request, repo_id),
            'year': get_dict_year(request, repo_id),
        }
    )
