from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .rag_engine import answer_query

@csrf_exempt
def ask_question(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            question = data.get("question")
            collection = data.get("collection")

            if not question:
                return JsonResponse({"error": "Question is required."}, status=400)
            if not collection:
                return JsonResponse({"error": "No PDF context loaded."}, status=400)

            answer, source_docs = answer_query(question, collection_name=collection)

            # Optionally extract source names if available in metadata
            sources = []
            for doc in source_docs:
                src = doc.metadata.get("source") if hasattr(doc, "metadata") else None
                if src:
                    sources.append(src)

            return JsonResponse({
                "answer": answer,
                "sources": sources
            })

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Only POST method allowed."}, status=405)
