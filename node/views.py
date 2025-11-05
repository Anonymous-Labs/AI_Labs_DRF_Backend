from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.utils.module_loading import import_string
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

@api_view(['POST', 'PATCH'])
@permission_classes([IsAuthenticated])
def execute(request):
    payload = request.data
    class_name = payload.get('type')

    if not class_name:
        return JsonResponse({"error": "Type attribute is missing in the payload."}, status=400)

    try:
        # Dynamically import and execute the class method
        class_reference = import_string(f'node.modules.input.{class_name}')
        result = class_reference.execute(payload)
        return JsonResponse({"message": result})
    except ModuleNotFoundError:
        return JsonResponse({"error": f"Class {class_name} not found."}, status=404)
    except AttributeError:
        return JsonResponse({"error": f"Class {class_name} does not have an execute method."}, status=400)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete(request):
    payload = request.data
    class_name = payload.get('type')

    if not class_name:
        return JsonResponse({"error": "Type attribute is missing in the payload."}, status=400)

    try:
        # Dynamically import and execute the class delete method
        class_reference = import_string(f'node.modules.input.{class_name}')
        metadata = payload.get('metadata', {})
        obj_id = metadata.get('id')

        if not obj_id:
            return JsonResponse({"error": "ID is missing in the metadata."}, status=400)

        obj = get_object_or_404(class_reference, id=obj_id)
        obj.delete()
        return JsonResponse({"message": "Object deleted successfully."})
    except ModuleNotFoundError:
        return JsonResponse({"error": f"Class {class_name} not found."}, status=404)
    except AttributeError:
        return JsonResponse({"error": f"Class {class_name} does not have a delete method."}, status=400)
