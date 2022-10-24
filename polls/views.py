from django.shortcuts import render,render_to_response
from django.http import HttpResponse
from django.template import Context, loader
from django.template.loader import get_template
from django import template
from django.http import JsonResponse
import json
from polls.bert import run_squad
from polls.bert import mood_demo
import time
import datetime
# Create your views here.
# def loadmodel():

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

def test(request):
    print("123123")
    return HttpResponse("123123.")

def web_site(request):
    template = loader.get_template('detail.html')
    # loadmodel()
    return HttpResponse(template.render())

tokenizer,estimator = run_squad.loadModel()

def qa_web(myrequest):
    path = myrequest.get_full_path()  # 加入本行，# 扣除網域名稱的請求路徑(開頭會有一個反斜線)
    print(path)

    errors = []
    default_p = '塑化劑是一種「環境荷爾蒙」，又稱內分泌干擾物，指會干擾生物體內分泌之外因性化學物質。若長時間高劑量使用 DEHP，將導致男嬰生殖器發育不良、女童性早熟，以及成年男性精蟲減少等問題。常見塑化劑可分成八種，其中 DEHP 在人體代謝快速，大部分代謝物會於 24 到 48 小時內排出體外；DINP 則是在 72 小時內由糞便或尿液排出。因此，若非大量食用，其實並沒有立即的安全問題。'
    default_q = '若長時間使用哪一種塑化劑會使男嬰生殖器發育不良、女童性早熟，以及成年男性精蟲減少等問題。'
    if 'passage' in myrequest.POST and 'question' in myrequest.POST:
        # if 'predict' in request.POST:
        #     passage = request.POST.get('passage',default_p)
        #     question = request.POST.get('question', str(default_q))
        passage = myrequest.POST['passage']
        question = myrequest.POST['question']
        if len(passage) == 0:
            passage = default_p
        if len(question) == 0:
            question = default_q

        date_time = datetime.datetime.now()  # 擷取現在時間
        print ("pas len:", passage)
        print ("que len:", question)
        if not passage or not question:
            errors.append('* 有空白欄位，請不要留空')

        import json
        import requests
        data = {'mode':"qa",'pas': passage, 'que': question}
        r = requests.post("http://140.115.51.157:8080/polls/run_server_model", data=json.dumps(data))
        # r = requests.post("http://140.115.51.157:8080/polls/model_get_request", data=data)
        data = r.json()
        print(data['answer'])

        answer = data['answer']
        # passage = passage
        # question = question
    return render_to_response('qa_template.html', locals())

def mood_web(myrequest):
    path = myrequest.get_full_path()  # 加入本行，# 扣除網域名稱的請求路徑(開頭會有一個反斜線)
    print(path)
    default_text = "今天天氣真好！"
    if 'text_mood' in myrequest.POST:
        # if 'predict' in request.POST:
        #     passage = request.POST.get('passage',default_p)
        #     question = request.POST.get('question', str(default_q))
        text = myrequest.POST['text_mood']
        if len(text) == 0:
            text = default_text

        date_time = datetime.datetime.now()  # 擷取現在時間
        print ("pas len:", len(default_text))

        import json
        import requests
        data = {'mode':"mood",'text': text}
        r = requests.post("http://140.115.51.157:8080/polls/run_server_model", data=json.dumps(data))
        # r = requests.post("http://140.115.51.157:8080/polls/model_get_request", data=data)
        data = r.json()
        print(data['mood'])

        mood = data['mood']
        text_a = text
    return render_to_response('mood_template.html', locals())

def score_web(myrequest):
    path = myrequest.get_full_path()  # 加入本行，# 扣除網域名稱的請求路徑(開頭會有一個反斜線)
    print(path)
    default_text = "今天天氣真好！"
    if 'text_mood' in myrequest.POST:
        text = myrequest.POST['text_mood']
        if len(text) == 0:
            text = default_text

        date_time = datetime.datetime.now()  # 擷取現在時間
        print ("pas len:", len(default_text))

        import json
        import requests
        data = {'mode':"score",'text': text}
        r = requests.post("http://140.115.51.157:8080/polls/run_server_model", data=json.dumps(data))
        # r = requests.post("http://140.115.51.157:8080/polls/model_get_request", data=data)
        data = r.json()
        print(data['score'])

        score = data['score']
        text_area = text
    return render_to_response('moodscore_template.html', locals())

def get_request(request):

    data_ex1 = request.POST['passage']
    data_ex2 = request.POST.get("question", "")
    # data_ex3 = json.loads(request.body.decode('utf-8'))
    # print(json.loads(request.body.decode('utf-8')))
    print("data_ex1: ",data_ex1)
    print("data_ex2: ",data_ex2)
    start= time.time()
    answer = run_squad.answerPredict(str(data_ex1),str(data_ex2),"time",tokenizer,estimator)
    end = time.time()
    #run model
    #model.preid
    return JsonResponse({'answer':answer,'time_cost': round(end - start,3)})

mood_tokenizer,mood_estimator,processor,label_list = mood_demo.load_MoodModel()
score_tokenizer,score_estimator,score_processor,score_label_list = mood_demo.load_ScoreModel()

def sentiment_analysis_website(request):
    template = loader.get_template('mood_demo.html')
    # loadmodel()
    return HttpResponse(template.render())

def get_Mood(request):
    text_a = request.POST['text']
    print("text_a:",text_a)
    start = time.time()
    mood = mood_demo.run_class(text_a,mood_tokenizer,mood_estimator,processor,label_list)
    end = time.time()
    print("mood: ",mood)
    return JsonResponse({'mood':mood,'time_cost': round(end - start,3)})

def get_score(request):
    text_a = request.POST['text']
    print("text_a:", text_a)
    start = time.time()
    score = mood_demo.run_score(text_a, score_tokenizer, score_estimator, score_processor, score_label_list)
    end = time.time()
    print("score: ", score)
    return JsonResponse({'score': score, 'time_cost': round(end - start, 3)})

# from django.views.decorators.csrf import ensure_csrf_cookie

# @ensure_csrf_cookie
def run_server_model(request):

    # print("++++++++++++++++++++++++++++++++++++++++")
    # input()
    # print("get in model")
    path = request.get_full_path()  # 加入本行，# 扣除網域名稱的請求路徑(開頭會有一個反斜線)
    print("path:",path)
    # data = json.loads(request.body.decode('utf-8'))
    # print("load:",json.loads(request.body.decode('utf-8')))
    # if request.method == "POST":
    # if data['mode'] == "qa":
    if request.GET['mode'] == "qa":
        # default_p = '塑化劑是一種「環境荷爾蒙」，又稱內分泌干擾物，指會干擾生物體內分泌之外因性化學物質。若長時間高劑量使用 DEHP，將導致男嬰生殖器發育不良、女童性早熟，以及成年男性精蟲減少等問題。常見塑化劑可分成八種，其中 DEHP 在人體代謝快速，大部分代謝物會於 24 到 48 小時內排出體外；DINP 則是在 72 小時內由糞便或尿液排出。因此，若非大量食用，其實並沒有立即的安全問題。'
        # default_q = '若長時間使用哪一種塑化劑會使男嬰生殖器發育不良、女童性早熟，以及成年男性精蟲減少等問題。'
        passage = '新型冠狀病毒是呼吸道病毒，它主要通過人咳嗽、打噴嚏時產生的飛沫、通過唾液飛沫或鼻涕，與受感染者接觸而傳播。每人都應保持良好的呼吸衛生習慣。例如，打噴嚏或咳嗽時，用彎曲的肘部遮擋，或使用紙巾並立即將用過的紙巾丟入封閉的垃圾桶。經常用含酒精成分的免洗洗手液清潔手或者用肥皂和清水洗手也很重要。了解被感染者何時可將病毒傳給他人對控制工作非常重要。需要根據感染者的詳細醫學信息確定2019-nCoV的傳染期。根據最近的報告，2019-nCoV感染者可能在出現明顯症狀之前就具傳染性。但根據現有數據，有症狀者仍是病毒的主要傳播者。新型冠狀病毒與嚴重急性呼吸道症候群不一樣。2019-nCoV與嚴重急性呼吸綜合徵病毒（SARS-CoV）屬於同一病毒家族，但它們不是同一種病毒。冠狀病毒是在動物和人體中發現的一個大型病毒家族。一些冠狀病毒會感染人，已知可引起感冒以及中東呼吸症候群冠狀病毒（MERS）和嚴重急性呼吸道症候群冠狀病毒（SARS）等較嚴重疾病。新型冠狀病毒是以前從未在人體中發現的冠狀病毒新毒株。新型冠狀病毒現已被命名為2019-nCoV。在2019年12月中國武漢暴發疫情之前，未曾發現此病毒。新型冠狀病毒現已被命名為2019-nCoV。目前還沒有可推薦的預防或治療新型冠狀病毒的任何特效藥。但2019-nCoV感染者應該接受適當治療，以緩解和治療症狀，重症患者應該接受優化的支持性治療。正在研究一些特異治療方法，將通過臨床試驗進行測試。世衛組織正與一系列合作夥伴一道，協調新型冠狀病毒治療藥物的開發工作。為防止受到新型冠狀病毒感染，應該保持基本的手衛生和呼吸衛生習慣，堅持安全飲食，盡可能避免與任何有呼吸道疾病症狀（如咳嗽和打噴嚏）的人密切接觸。不推薦採用以下措施應對2019-nCoV，它們不能有效保護您，甚至可能會帶來害處：服用維生素C、吸煙、飲用傳統藥茶、佩戴多個口罩最大限度進行防護、在無醫囑的情況下服用抗生素等藥物，如果有發熱、咳嗽和呼吸困難等症狀，請及早就醫，以降低發生更嚴重感染的風險，並應告知醫務人員您最近的旅行史。預防措施與其他呼吸道感染相同，包括養成良好衛生習慣、勤洗手、並遵守口罩配戴三時機：「看病、陪病、探病的時候、有呼吸道症狀時、有慢性病者外出時」，並且儘量避免出入人潮擁擠、空氣不流通的公共場所，及避免接觸野生動物與禽類。與其他呼吸系統疾病一樣，感染2019-nCoV可導致輕微症狀，例如流涕、咽痛、咳嗽和發熱等。某些患者症狀可能較重，並可導致肺炎或呼吸困難。在少數情況下，此病可以致命。老年人和有基礎病症（如糖尿病和心臟病）的人似乎較易患重症。詳細調查發現，2002年中國發生了SARS-CoV從果子狸傳播至人的事件，2012年沙特阿拉伯發生了MERS-CoV從單峰駱駝傳播至人的事件。有些已知的冠狀病毒在動物中傳播，但未感染人類。隨著全球監測工作的改善，可能會發現更多的冠狀病毒。尚未查明2019-nCoV的動物來源。這並不意味著人們會從任何動物或寵物那裡感染2019-nCoV。一些最初報告的人類感染病例很可能來自中國活體動物市場中的動物。為保護自己，在活體動物市場時，應避免在未加防護情況下直接接觸活體動物以及動物觸碰過的地方。應避免食用生鮮或未煮熟的動物產品。應採用良好的食品安全措施，謹慎處理生鮮的肉、奶或動物器官，以免與生食交叉污染。是的，2019-nCoV可以在人際傳播，導致呼吸道疾病。人們通常是在住家、工作場所或醫療機構等地與感染者密切接觸後受到感染的。冠狀病毒多屬接觸或飛沫傳染，與患者共用毛巾等直接與間接接觸行為有可能碰到病毒，而手摸到沾有病毒的物品後再觸及口、鼻、眼，是有可能讓病毒進入身體而感染的。'
        # passage = data['pas']
        question = request.GET['que']
        # print ("pas len:", data['pas'])
        # print ("que len:", data['que'])
        print('GET in !!!!!!!!!!!!!!!!!!!!!!!')
        if len(passage) == 0:
            passage = default_p
        if len(question) == 0:
            question = default_q
        # answer = run_squad.answerPredict(str(passage), str(question), "time", tokenizer, estimator)
        return JsonResponse({'answer': "Hi Yang"})
        # return  HttpResponse('Hi Yang')
'''
    if data['mode'] == "mood":
        start = time.time()
        text_a = data['text']
        mood = mood_demo.run_class(text_a, mood_tokenizer, mood_estimator, processor, label_list)
        end = time.time()
        print("mood: ", mood)
        return JsonResponse({'mood': mood, 'time_cost': round(end - start, 3)})

    if data['mode'] == "score":
        start = time.time()
        text_a = data['text']
        score = mood_demo.run_score(text_a, score_tokenizer, score_estimator, score_processor, score_label_list)
        end = time.time()
        print ("text_a:",text_a)
        print("score: ", score)
        return JsonResponse({'score': score, 'time_cost': round(end - start, 3)})
'''