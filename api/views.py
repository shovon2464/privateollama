from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse
import os
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
import requests
import json



 

alpaca_prompt = """Below is an instruction that describes a task, paired with an input that provides further context. Write a response that appropriately completes the request.

### Instruction:
{}

### Input:
{}

### Response:
{}"""

class IsActiveView(APIView):
    def get(self, request):
        data = {"message": "I Am Active, I Am Private Ollama!"}
        return Response(data, status=status.HTTP_200_OK)
    
    

@method_decorator(csrf_exempt, name='dispatch')
class ClassifyNaturesView(View):
    #using privateollma
    def post(self, request):
        try:
            import torch
            from numba import cuda
            # Create your views here.
            import os
            import gc
            os.environ["CUDA_DEVICE_ORDER"]="PCI_BUS_ID"
            os.environ["CUDA_VISIBLE_DEVICES"]="1"
            from unsloth import FastLanguageModel
            max_seq_length = 9000 # Choose any! We auto support RoPE Scaling internally!
            dtype = None # None for auto detection. Float16 for Tesla T4, V100, Bfloat16 for Ampere+
            load_in_4bit = True # Use 4bit quantization to reduce memory usage. Can be False.
            model, tokenizer = FastLanguageModel.from_pretrained(
                    model_name = "natures_classify_6600l", # YOUR MODEL YOU USED FOR TRAINING
                    max_seq_length = max_seq_length,
                    dtype = dtype,
                    load_in_4bit = load_in_4bit,
                    ) 
            content = request.POST.get('document')
            instruction = "Classify the following insurance document into one of the specified categories based on its content. Return the classification as a JSON object with the type in short form. Do not include reasoning. Example output: {\n\"type\": \"PCH \"}.If the document describes a New Business then classify it to NBS. If the document describes Cancellation of policy then classify it to XLN. If the document changes the policy then classify it to PCH.  Be careful not to confuse this with NBS If the document is a reminder of an outstanding balance and time to pay, classify it as ACR. If the document describes an Endorsement then classify it to EDT. .If the document is a debit note describing a transaction then classify it to DBR.If the document describes Renewal then classify it to RWL. If the document indicates that a renewal was issued, the client is not happy, and a change is needed, classify it as RII. If the document describes reinstatement after cancellation due to non-payment, classify it as REI. Only return the classification in the specified JSON format."
            inputs = tokenizer(
            [
                alpaca_prompt.format(instruction,content,"")
            ], return_tensors = "pt").to("cuda")

            outputs = model.generate(**inputs, max_new_tokens = 64, use_cache = True)
            response = tokenizer.batch_decode(outputs)
            torch.cuda.empty_cache()
            gc.collect() 
            device = cuda.get_current_device()
            device.reset()
            response = response[0].split("###")
            response = response[3]
            start_index = response.find('{') 
            end_index = response.rfind('}')+1
            response = response[start_index:end_index]
            response = json.loads(response)
            return JsonResponse(response,safe=False)


        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
        