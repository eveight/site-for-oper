from django.shortcuts import render, redirect
from .models import HistoryGiveUser, Outlet, User, HelpTable, ForFile, Task, Refund, ForUser
from django.contrib.auth.models import Group
from django.db.models import F
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import TaskForm
import random
import datetime
from datetime import timedelta


def is_user_valid(user):
    return user.groups.filter(name__in=['Оператор', 'Администратор'])


def is_user_admin(user):
    return user.groups.filter(name='Администратор')


def outlet_update():
    available_day = [3, 4, 5]

    if datetime.date.today().day in available_day and HelpTable.objects.get(id=1).outlet_update == True:
        Outlet.objects.all().update(view=0)
        HelpTable.objects.filter(id=1).update(outlet_update=False)
    if datetime.date.today().day not in available_day:
        HelpTable.objects.filter(id=1).update(outlet_update=True)


def get_score_users():
    today_month = datetime.date.today().month

    count_users = {}

    users = User.objects.all()
    for user in users:
        obj_this_month = HistoryGiveUser.objects.filter(give_user=user.id, date_time__month=today_month).count()
        count_users[user.username] = [obj_this_month]

    return count_users


def get_choice(request):
    today_day = datetime.date.today().day
    today_month = datetime.date.today().month

    obj_this_day = HistoryGiveUser.objects.filter(give_user=request.id, date_time__day=today_day,
                                                  date_time__month=today_month)

    return obj_this_day


def get_outlet_this_day_for_admin():
    today_day = datetime.date.today().day
    today_month = datetime.date.today().month

    history_order_in_month = HistoryGiveUser.objects.filter(date_time__day=today_day,
                                                            date_time__month=today_month).order_by('-date_time')
    return history_order_in_month


def get_perms_user_for_admin():
    all_user = User.objects.all()
    user_without_perms = []

    for user in all_user:
        if user.groups.filter(name__in=['Оператор', 'Администратор']):
            pass
        else:
            user_without_perms.append(user)

    return user_without_perms


def user_no_perms(request):
    if request.method == 'POST':
        if 'user_no_perms' in request.POST:
            user = User.objects.get(id=request.POST['user_no_perms'])
            user.groups.add(Group.objects.get(name='Оператор'))
            return redirect('admin_page')


def task_for_user(request):
    today = datetime.date.today().day
    user = request.user
    task_user = Task.objects.filter(date_time__day=today, operator=user.id, status=False)
    return task_user


def task_for_admin():
    all_task = Task.objects.filter(status=False).order_by('-date_time')
    return all_task


def task_perform(request):
    today = datetime.date.today().day
    user = User.objects.get(id=request.user.id)
    task = Task.objects.filter(date_time__day=today, operator=user, status=False)
    for i in task:
        HistoryGiveUser.objects.create(give_outlet=i.outlet, give_user=i.operator)
        Task.objects.filter(date_time__day=today, outlet=i.outlet, operator=i.operator).update(status=True)
    return redirect('home')


def refund_for_user(request):
    user = User.objects.get(id=request.user.id)
    all_refund_for_user = Refund.objects.filter(status=False, user=user)
    return all_refund_for_user


def refund_for_admin():
    all_refund = Refund.objects.filter(status=False).order_by('-date')
    return all_refund


def create_refund(request):
    today = datetime.datetime.now()

    relevant_refund = Refund.objects.filter(date=today)
    if relevant_refund:
        pass
    else:
        try:
            user = ForUser.objects.filter(refund=False)[0]
            user_valid = User.objects.get(id=user.user.id)

            one_days = timedelta(1)
            valid_date = today + one_days

            Refund.objects.create(date_achieve=valid_date, user=user_valid)

            ForUser.objects.filter(id=user.id).update(refund=True)
        except IndexError:
            ForUser.objects.all().update(refund=False)
            create_refund(request)


def refund_done(request):
    if request.method == 'POST':
        if 'refund_id' in request.POST:
            Refund.objects.filter(id=request.POST['refund_id']).update(status=True)
    return redirect('home')


@login_required()
def create_task(request):
    form = TaskForm()
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            outlet_id = form.cleaned_data['outlet'].id
            Outlet.objects.filter(id=outlet_id).update(view=F('view') + 1)
            form.save()

    ctx = {
        'form': form,
        'task_admin': task_for_admin(),
    }

    return render(request, 'workspace/task_page_v1.html', ctx)


@login_required()
@user_passes_test(is_user_valid, login_url='user_invalid')
def home_space(request, error=None):
    obj_file = ForFile.objects.get(id=1)

    ctx = {
        'count_users': get_score_users(),
        'choose': get_choice(request.user),
        'get_work_error': error,
        'obj_file': obj_file,
        'task_user': task_for_user(request),
        'create_refund': create_refund(request),
        'refund_for_user': refund_for_user(request),
    }
    return render(request, 'workspace/home_v2.html', ctx)


@login_required()
@user_passes_test(is_user_valid)
def get_work(request, tt=3):
    if request.method == 'POST':
        if 'one_tt' in request.POST:
            tt = 1

        outlet_update()
        obj_user = User.objects.get(id=request.user.id)
        get_outlet = Outlet.objects.filter(view__lte=3, working=True)
        if get_outlet:
            choice = random.choices(get_outlet, k=tt)
            for i in choice:
                obj_outlet = Outlet.objects.get(id=i.pk)

                new_point = HistoryGiveUser.objects.create(give_outlet=obj_outlet, give_user=obj_user)
                new_point.save()

                Outlet.objects.filter(id=i.pk).update(view=F('view') + 1)
        else:
            return redirect('home', error='Нет доступных ТТ')
    return redirect('/home/')


@user_passes_test(is_user_admin, login_url='home')
def admin_page(request):
    user_no_perms(request)

    ctx = {
        'outlet_for_admin': get_outlet_this_day_for_admin(),
        'user_without_perms': get_perms_user_for_admin(),
        'task_admin': task_for_admin(),
        'refund_for_admin': refund_for_admin(),
    }
    return render(request, 'workspace/admin_page_v1.html', ctx)


@login_required()
def user_invalid(request):
    return render(request, 'workspace/user_invalid_v1.html')
