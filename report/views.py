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


def get_context_dictionary(records, date):
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


def get_all_records(request, repo_id):
    return Record.objects.filter(
        repository_id=repo_id,
        repository__user_id=request.user.id
    ).order_by('date')


def filter_records_by_date(records, date):
    filter_records = []
    for record in records:
        if date in record.date:
            filter_records.append(record)

    return filter_records


def get_today_context(records):
    date = get_today_date()
    today_records = filter_records_by_date(records, date)
    return get_context_dictionary(today_records, date)


def get_month_context(records):
    date = get_month_date()
    month_records = filter_records_by_date(records, date)
    return get_context_dictionary(month_records, get_name_month())


def get_year_context(records):
    date = get_year_date()
    years_records = filter_records_by_date(records, date)
    return get_context_dictionary(years_records, date[:-1])


def get_sum_price(records):
    sum = 0
    for record in records:
        sum += int(record.price)
    return sum


def filter_request_by_date(request, all_records):
    date = request.GET.get('date')
    records = None
    if date == 'today':
        records = filter_records_by_date(all_records, get_today_date())
    if date == 'month':
        records = filter_records_by_date(all_records, get_month_date())
    if date == 'year':
        records = filter_records_by_date(all_records, get_year_date())
    if date == 'total':
        records = all_records
    return records


@login_required
def detail_report_view(request: HttpRequest, repo_id):
    all_records = get_all_records(request, repo_id)

    filter_records = filter_request_by_date(request, all_records)

    return render(
        request,
        'report/detail_report.html', {
            'records': filter_records,
            'repo_id': repo_id,
            'sum_records': get_sum_price(filter_records)
        }
    )


@login_required
def report_view(request: HttpRequest, repo_id):
    records = get_all_records(request, repo_id)
    return render(
        request,
        'report/report.html', {
            'repo_id': repo_id,
            'today': get_today_context(records),
            'month': get_month_context(records),
            'year': get_year_context(records),
            'total': get_context_dictionary(get_all_records(request, repo_id), '-')
        }
    )
