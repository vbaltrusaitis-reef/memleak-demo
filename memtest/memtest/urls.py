# FIX 3: Don't import debug_toolbar.
import debug_toolbar
from django.urls import path
from memtest.views import memory_leak

urlpatterns = [
    path("memory_leak", memory_leak)
]
