# Create your views here.
import re
from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.http import HttpRequest
from django.shortcuts import render
from jalali_date import date2jalali

from category.models import Category
from record.models import Record


class TodayDate:
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

    today = str(date2jalali(datetime.date(datetime.now()))).replace('-', '/')

    @staticmethod
    def get_year():
        return TodayDate.today[:4]

    @staticmethod
    def get_month():
        return TodayDate.today[5:7]

    @staticmethod
    def get_month_name():
        month = int(TodayDate.get_month())
        return TodayDate.MONTH[month]

    @staticmethod
    def get_day():
        return TodayDate.today[8:]

    @staticmethod
    def get_today():
        return TodayDate.today


def get_context(records, display_date):
    sum_input = 0
    sum_output = 0
    for record in records:
        if record.record_type == 'input':
            sum_input += record.price
        elif record.record_type == 'output':
            sum_output += record.price
    return {
        'date': display_date,
        'sum_input': sum_input,
        'sum_output': sum_output,
        'remaining': sum_input - sum_output,
    }


def convert_date_to_regex(date):
    today = TodayDate.get_today()
    month = TodayDate.get_month()
    year = TodayDate.get_year()

    if date == 'today':
        return today
    if date == 'month':
        return f'{year}/{month}/*'
    if date == 'year':
        return f'{year}/*/*'
    if date == 'total':
        return r'.*'


def get_all_records(request, repo_id):
    return Record.objects.filter(
        repository_id=repo_id,
        repository__user_id=request.user.id
    ).order_by('date')


def filter_records_by_date(records, regex_date):
    return [record for record in records if re.search(regex_date, record.date)]


def filter_records_by_record_type(records, record_type):
    return [record for record in records if record.record_type == record_type]


def filter_records_by_cat(records, cat_id):
    return [record for record in records if record.category_id == int(cat_id)]


def get_sum_price(records):
    sum = 0
    for record in records:
        sum += int(record.price)
    return sum


@login_required
def detail_report_view(request: HttpRequest, repo_id):
    all_records = get_all_records(request, repo_id)
    categories = Category.objects.filter(
        repository_id=repo_id,
        repository__user_id=request.user.id,
    )

    date = request.GET.get('date')
    filter_records = filter_records_by_date(all_records, convert_date_to_regex(date))

    record_type = request.GET.get('record_type')
    if record_type is not None:
        filter_records = filter_records_by_record_type(filter_records, record_type)

    cat_id = request.GET.get('cat')
    if cat_id is not None:
        filter_records = filter_records_by_cat(filter_records, cat_id)

    return render(
        request,
        'report/detail_report.html', {
            'current_url': f'{request.path}?date={date}',
            'records': filter_records,
            'repo_id': repo_id,
            'categories': categories,
            'sum_records': get_sum_price(filter_records),
        }
    )


@login_required
def report_view(request: HttpRequest, repo_id):
    all_records = get_all_records(request, repo_id)
    today_record = filter_records_by_date(all_records, convert_date_to_regex('today'))
    month_record = filter_records_by_date(all_records, convert_date_to_regex('month'))
    year_record = filter_records_by_date(all_records, convert_date_to_regex('year'))

    return render(
        request,
        'report/report.html', {
            'repo_id': repo_id,
            'today': get_context(today_record, TodayDate.get_today()),
            'month': get_context(month_record, TodayDate.get_month_name()),
            'year': get_context(year_record, TodayDate.get_year()),
            'total': get_context(all_records, '-')
        }
    )
