from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.http import HttpResponse
import objgraph


def memory_leak(request):
    layer = get_channel_layer()

    # FIX 4: Remove the line below, don't make any call to group_send
    async_to_sync(layer.group_send)("any", {})

    growth = objgraph.growth()
    if not growth:
        return HttpResponse("NO NEW OBJECTS\n")
    if growth:
        report = "NEW OBJECTS:\nname\ttotal\tdiff\n"
        for name, total, diff in growth:
            report += f"{name}\t{total}\t+{diff}\n"
        report += "\n"
        return HttpResponse(report)