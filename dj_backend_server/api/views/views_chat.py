from django.http import JsonResponse
from django.views.decorators.http import require_POST

from api.utils import get_vector_store
from api.utils.make_chain import get_qa_chain, get_condense_chain
import json
from django.views.decorators.csrf import csrf_exempt
from api.interfaces import StoreOptions

@csrf_exempt
@require_POST
def chat(request):
    body = json.loads(request.body.decode('utf-8'))
    question = body.get('question')
    history = body.get('history') or []
    namespace = body.get('namespace')
    mode = body.get('mode')
    initial_prompt = body.get('initial_prompt')

    if not question:
        return JsonResponse({'message': 'No question in the request'})

    sanitized_question = question.strip().replace('\n', ' ')

    try:
        vector_store = get_vector_store(StoreOptions(namespace=namespace))
        chain = get_qa_chain(vector_store, mode, initial_prompt)

        # use this only if constructing a qa retrieval chain
        # condense_chain = get_condense_chain(mode)
        # sanitized_question = condense_chain.predict(chat_history="\n".join(history), question=question)
        
        response = chain({"query": sanitized_question })
        r = {'text': response['result']}
        return JsonResponse(r)
    except Exception as e:
            import traceback
            print(e)
            traceback.print_exc()
            return JsonResponse({'error': str(e)})

