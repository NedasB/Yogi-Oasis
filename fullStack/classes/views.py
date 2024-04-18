from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from .models import Lesson


def all_classes(request):
    
    lessons = Lesson.objects.all()
    query = None
    sort = None
    direction = "asc"  # Sets the default direction to ascending

    if request.GET:
        # Search query
        if 'q' in request.GET:
            query = request.GET['q']
            if not query:
                messages.error(request, "You didn't enter any search criteria!")
                return redirect(reverse('classes'))
            queries = Q(title__icontains=query) | Q(description__icontains=query) | Q(instructor_name__icontains=query)
            lessons = lessons.filter(queries)

        # Sorting
        if 'sort' in request.GET:
            sort = request.GET['sort']
            sortmap = {
                'date_asc': 'date',
                'date_desc': '-date',
                'price_asc': 'cost',
                'price_desc': '-cost',
                'capacity_asc': 'current_capacity',
                'capacity_desc': '-current_capacity',
            }
            sortkey = sortmap.get(sort, 'date')  # Default sort by date if sort parameter is not recognized
            lessons = lessons.order_by(sortkey)

    context = {
        'lessons': lessons,
        'search_term': query,
        'current_sorting': sort,
    }
    
    return render(request, 'classes/classes.html', context)


def class_detail(request, class_id):
    
    lesson = get_object_or_404(Lesson, pk=class_id)
    query = request.GET.get('q', '')  # Default to empty string if 'q' is not present

    context = {
        'lesson': lesson,
        'search_term': query,
    }
    
    return render(request, 'classes/class_detail.html', context)

