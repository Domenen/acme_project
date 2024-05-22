from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect

from .models import Birthday, Congratulation
from .forms import BirthdayForm, CongratulationForm
from .utils import calculate_birthday_countdown


# def birthday(request, pk=None):
#     """Send birthday list."""
#     # Если в запросе указан pk (если получен запрос на редактирование объекта):
#     if pk is not None:
#         # Получаем объект модели или выбрасываем 404 ошибку.
#         instance = get_object_or_404(Birthday, pk=pk)
#     # Если в запросе не указан pk
#     # (если получен запрос к странице создания записи):
#     else:
#         # Связывать форму с объектом не нужно, установим значение None.
#         instance = None
#     # Передаём в форму либо данные из запроса, либо None.
#     # В случае редактирования прикрепляем объект модели.
#     form = BirthdayForm(
#         request.POST or None,
#         files=request.FILES or None,
#         instance=instance
#     )
#     # Остальной код без изменений.
#     context = {'form': form}
#     # Сохраняем данные, полученные из формы, и отправляем ответ:
#     if form.is_valid():
#         form.save()
#         birthday_countdown = calculate_birthday_countdown(
#             form.cleaned_data['birthday']
#         )
#         context.update({'birthday_countdown': birthday_countdown})
#     return render(request, 'birthday/birthday.html', context)


# def birthday_list(request):
#     """Send birthday list."""
#     # Получаем список всех объектов с сортировкой по id.
#     birthdays = Birthday.objects.order_by('id')
#     # Создаём объект пагинатора с количеством 10 записей на страницу.
#     paginator = Paginator(birthdays, 10)

#     # Получаем из запроса значение параметра page.
#     page_number = request.GET.get('page')
#     # Получаем запрошенную страницу пагинатора. 
#     # Если параметра page нет в запросе или его значение не приводится к числу,
#     # вернётся первая страница.
#     page_obj = paginator.get_page(page_number)
#     # Вместо полного списка объектов передаём в контекст 
#     # объект страницы пагинатора
#     context = {'page_obj': page_obj}
#     return render(request, 'birthday/birthday_list.html', context)


# def delete_birthday(request, pk):
#     """Delete."""
#     # Получаем объект модели или выбрасываем 404 ошибку.
#     instance = get_object_or_404(Birthday, pk=pk)
#     # В форму передаём только объект модели;
#     # передавать в форму параметры запроса не нужно.
#     form = BirthdayForm(instance=instance)
#     context = {'form': form}
#     # Если был получен POST-запрос...
#     if request.method == 'POST':
#         # ...удаляем объект:
#         instance.delete()
#         # ...и переадресовываем пользователя на страницу со списком записей.
#         return redirect('birthday:list')
#     # Если был получен GET-запрос — отображаем форму.
#     return render(request, 'birthday/birthday.html', context)


# Создаём миксин.
# class BirthdayMixin:
#     """CBV Birthday."""

#     model = Birthday
#     success_url = reverse_lazy('birthday:list')


class OnlyAuthorMixin(UserPassesTestMixin):

    def test_func(self):
        object = self.get_object()
        return object.author == self.request.user


# Наследуем класс от встроенного ListView:
class BirthdayListView(ListView):
    """CBV Birthday."""

    # Указываем модель, с которой работает CBV...
    model = Birthday
    queryset = Birthday.objects.prefetch_related(
        'tags'
    ).select_related('author')
    # ...сортировку, которая будет применена при выводе списка объектов:
    ordering = 'id'
    # ...и даже настройки пагинации:
    paginate_by = 10


class BirthdayCreateView(LoginRequiredMixin, CreateView):
    """CBV Birthday."""

    # # Указываем модель, с которой работает CBV...
    # model = Birthday
    # # Этот класс сам может создать форму на основе модели!
    # # Нет необходимости отдельно создавать форму через ModelForm.
    # # Указываем поля, которые должны быть в форме:
    # # fields = '__all__'
    # # Указываем имя формы:
    # form_class = BirthdayForm
    # # Явным образом указываем шаблон:
    # template_name = 'birthday/birthday.html'
    # # Указываем namespace:name страницы, куда будет перенаправлен пользователь
    # # после создания объекта:
    # success_url = reverse_lazy('birthday:list')
    model = Birthday
    form_class = BirthdayForm

    def form_valid(self, form):
        # Присвоить полю author объект пользователя из запроса.
        form.instance.author = self.request.user
        # Продолжить валидацию, описанную в форме.
        return super().form_valid(form)


class BirthdayUpdateView(OnlyAuthorMixin, UpdateView):
    """CBV Birthday."""

    # model = Birthday
    # form_class = BirthdayForm
    # template_name = 'birthday/birthday.html'
    # success_url = reverse_lazy('birthday:list')
    model = Birthday
    form_class = BirthdayForm

    # # Определяем метод test_func() для миксина UserPassesTestMixin:
    # def test_func(self):
    #     # Получаем текущий объект.
    #     object = self.get_object()
    #     # Метод вернёт True или False. 
    #     # Если пользователь - автор объекта, то тест будет пройден.
    #     # Если нет, то будет вызвана ошибка 403.
    #     return object.author == self.request.user


class BirthdayDeleteView(OnlyAuthorMixin, DeleteView):
    """CBV Birthday."""

    model = Birthday
    success_url = reverse_lazy('birthday:list')


class BirthdayDetailView(DetailView):
    """CBV Birthday."""

    model = Birthday

    def get_context_data(self, **kwargs):
        """Калькулятор дня рождения."""
        # Получаем словарь контекста:
        context = super().get_context_data(**kwargs)
        # Добавляем в словарь новый ключ:
        context['birthday_countdown'] = calculate_birthday_countdown(
            # Дату рождения берём из объекта в словаре context:
            self.object.birthday
        )
        # Записываем в переменную form пустой объект формы.
        context['form'] = CongratulationForm()
        # Запрашиваем все поздравления для выбранного дня рождения.
        context['congratulations'] = (
            # Дополнительно подгружаем авторов комментариев,
            # чтобы избежать множества запросов к БД.
            self.object.congratulations.select_related('author')
        )
        return context


# Будут обработаны POST-запросы только от залогиненных пользователей.
@login_required
def add_comment(request, pk):
    # Получаем объект дня рождения или выбрасываем 404 ошибку.
    birthday = get_object_or_404(Birthday, pk=pk)
    # Функция должна обрабатывать только POST-запросы.
    form = CongratulationForm(request.POST)
    if form.is_valid():
        # Создаём объект поздравления, но не сохраняем его в БД.
        congratulation = form.save(commit=False)
        # В поле author передаём объект автора поздравления.
        congratulation.author = request.user
        # В поле birthday передаём объект дня рождения.
        congratulation.birthday = birthday
        # Сохраняем объект в БД.
        congratulation.save()
    # Перенаправляем пользователя назад, на страницу дня рождения.
    return redirect('birthday:detail', pk=pk)

# ----------------------------------------------добовлять коменты через CBV
# from django.contrib.auth.mixins import LoginRequiredMixin
# from django.shortcuts import get_object_or_404
# from django.urls import reverse
# from django.views.generic import CreateView

# from .forms import CongratulationForm
# from .models import Birthday, Congratulation


# class CongratulationCreateView(LoginRequiredMixin, CreateView):
#     birthday = None
#     model = Congratulation
#     form_class = CongratulationForm

#     # Переопределяем dispatch()
#     def dispatch(self, request, *args, **kwargs):
#         self.birthday = get_object_or_404(Birthday, pk=kwargs['pk'])
#         return super().dispatch(request, *args, **kwargs)

#     # Переопределяем form_valid()
#     def form_valid(self, form):
#         form.instance.author = self.request.user
#         form.instance.birthday = self.birthday
#         return super().form_valid(form)

#     # Переопределяем get_success_url()
#     def get_success_url(self):
#         return reverse('birthday:detail', kwargs={'pk': self.birthday.pk})
# ------------------------------------------------------------------
