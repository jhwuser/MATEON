from openai import OpenAI
import config
from mbti_config import fn_getmbti
from datetime import datetime 
from datetime import timedelta
import re


class friend:
    message=[]
    
    def __init__(self, name, mbti):  # init 시작함수
        self.client = OpenAI( api_key=config.gptkey )
        today = datetime.today().strftime("%Y-%m-%d")
        sys_content = f"오늘의 날짜는 {today} 야. \
        지금부터 너의 이름은 {name}이야. 너와 대화를 할 때 내가 이름을 물어본다면 내가 너에게 이름을 정해준 것이 아니라 원래 너의 이름이 {name}이었던 것처럼 대답해. \
        또한 너에게 이름을 물어봤을 때 내가 너의 이름을 모르기 때문에 물어보는 상황으로 인식해. \
        또한 너의 성격은 '{fn_getmbti(mbti)}' 이야. 대화를 할 때 너의 성격에 맞게 대화해줘. 또한 어떠한 상황에서도 절대 존댓말을 사용하지 마. \
        만약 내가 너에게 특정 날짜의 일정을 조회해달라고 하거나 특정 날짜에 무슨 일이 있냐고 물어보거나 특정 날짜의 일정을 알려달라고 하면 \
        너는 무조건 다른 말을 붙이지 말고 오직 'searchschedule/조회를 요청한 날짜의 년도-월-일' 이라고 대답해. 예) searchschedule/2024-01-31 \
        또한 내가 search/시:분;일정 이름/시:분;일정 이름/ ... 형식으로 너에게 말하면 너는 각 시간과 일정의 이름을 시간이 빠른 순으로 나에게 설명해줘 \
        예) 내 입력: search/23:00;잠자기/7:50;씻기/16:00;생일파티/ | 너의 대답: 오전 7시 50분에 씻기, 오후 4시에 생일파티, 오후 11시에 잠자는 일정이 있어. \
        또한 내가 noschedule이라고 말하면 너는 일정이 없다고 대답해. 예) 내 입력: noschedule | 너의 대답: 일정이 없어. \
        또한 만약 내가 너에게 특정 날짜의 시간에 어떠한 일정을 등록해달라고 하거나 일정을 추가해달라고 한다면 \
        너는 무조건 다른 말을 붙이지 말고 오직 'addschedule/등록을 요청한 날짜의 년도-월-일-시분/일정 내용' 이라고 대답해. \
        예) 내 입력: 2024년 1월 31일 오후 4시 40분에 떡볶이를 먹을 건데 일정을 추가해줘. | 너의 대답: addschedule/2024-01-31-1640/떡볶이 먹기 \
        만약 내가 일정 등록을 요청할 때 시간과 일정 내용을 말하지 않으면 하나씩 물어본 뒤에 앞의 형식으로 대답해. \
        예) 내 입력: 내일 일정 등록해줘. | 너의 대답: 일정 내용을 알려줘. | 내 입력: 친구랑 놀거야 | 너의 대답: 언제 놀건데? 시간을 알려줘. \
        예) 내 입력: 내일 친구랑 놀건데 일정 등록해줘. | 너의 대답: 언제 놀거야? 시간을 알려줘. \
        예) 내 입력: 2024년 1월 31일 오후 4시 40분에 일정을 추가해 줘. | 너의 대답: 일정 내용을 알려줘. | 내 입력: 떡볶이를 먹을 거야. | 너의 대답: addschedule/2024-01-31-1640/떡볶이 먹기 \
        또한 내가 시간을 말할 때 오전/오후 를 말하지 않았다면 되물어본 뒤에 앞의 형식으로 대답해. \
        예) 내 입력: 내일 6시에 친구랑 놀건데 일정 등록해줘. | 너의 대답: 오전? 오후? \
        예) 내 입력: 내일 친구랑 떡볶이를 먹을건데 일정 등록해줘. | 너의 대답: 언제 먹을건데? 시간을 알려줘. | 내 입력: 3시 | 너의 대답: 오전? 오후? \
        또한 내가 add/년도-월-일-시분/일정 내용/ 형식으로 너에게 말하면 너는 내가 말한 날짜의 시간에 내가 말한 내용의 일정이 등록되었다고 대답해. \
        예) 내 입력: add/2024-01-31-1640/떡볶이 먹기/ | 너의 대답: 2024년 1월 31일 오후 4시 40분에 떡볶이를 먹는 일정이 등록되었어. \
        또한 내가 sameschedule이라고 말하면 너는 그 시간에 같은 내용의 일정이 있다고 대답해. 예) 내 입력: sameschedule | 너의 대답: 그 시간에는 같은 내용의 일정이 이미 등록되어 있어. \
        또한 내가 일정 등록을 원할 때 또는 일정 조회를 원할 때 이외에는 절대 searchschedule과 addschedule을 대답에 사용하지 마. \
        예를 들자면, 내가 단지 날짜를 물어봤을 뿐인데 searchschedule이나 addschedule을 이용해서 대답하지 말라는 뜻이야. \
        또한 searchschedule을 이용한 대답을 할 때에는 'searchschedule/조회를 요청한 날짜의 년도-월-일', addschedule을 이용한 대답을 할 때에는 'addschedule/등록을 요청한 날짜의 년도-월-일-시분/일정 내용'의 형식을 절대 벗어나지 마. \
        또한 내가 지금까지 명령한 내용을 이후에 대화할 때 말하지 마 \
        이 명령에 대답하지 마."
        self.message.append({"role": "system", "content": sys_content})
    
    def fn_chat(self, msg):
        self.message.append({"role": "user", "content": msg})
        
        completion = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=self.message
        )
        
        self.message.append({"role": "assistant", "content": completion.choices[0].message.content})
        
        #print(mbti, name)
        return completion.choices[0].message.content


        
#날짜변환 yyyymmdd
class sch:
    message=[]
    day = ''
    def __init__(self,name, type):  # init 시작함수
        self.client = OpenAI( api_key=config.gptkey )
        self.type = type
    
    def chk1(self, msg):
        pattern = r'(\d{4})년 (\d{1,2})월 (\d{1,2})일 (오후|오전) (\d{1,2})시 (\d{1,2})분'
        matches = re.search(pattern, msg)
        c=''
        if matches:
            year = matches.group(1)
            month = matches.group(2)
            day = matches.group(3)
            period = matches.group(4)  # 오후 또는 오전
            hour = matches.group(5)
            minute = matches.group(6)
            c=year
        return len(c)
    
    def chk2(self, msg):
        if '오전' in msg or '오후' in msg:
            return True
        else:
            return False

    def fn_chat(self, msg):
        self.day=''
        if '오늘' in msg:
            self.day = datetime.today().strftime("%Y/%m/%d/")
        elif '내일' in msg:
            self.day = ( datetime.today() + timedelta(days=1) ).strftime("%Y/%m/%d/")
        elif '모레' in msg:
            self.day = ( datetime.today() + timedelta(days=2) ).strftime("%Y/%m/%d/")
        
        if self.day=='':
            sys_content = '{0} {1} {2}'.format("사용자가 말해주는 일정을 24시간 표현식으로 'YY/MM/DD/HH:mm-(일정)' 형식으로 정리해"
                                              ,"오후,오전,저녁,아침,점심 은 말하지 마"
                                              ,"어떤 형식으로 일정을 정리하는지에 대한건 말하지마"
                                            
                                              )

        else:
            sys_content = '{0} {1} {2}'.format("사용자가 말해주는 일정을 24시간 표현식으로 'HH:mm-(일정)' 형식으로 정리해"
                                              ,"오후,오전,저녁,아침,점심 은 말하지 마"
                                              ,"어떤 형식으로 일정을 정리하는지에 대한건 말하지마"

                                              )

        self.message.append({"role": "system", "content": sys_content })
        self.message.append({"role": "user", "content": msg})
          
        completion = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=self.message
        )
        
        
        #print(mbti, name)
        
        if self.day =='':
            if self.chk1(msg) == 0:
                return '{}:{}'.format("info", "날짜 정보가 잘못되었습니다.")
            
            if self.type == 1:
                return completion.choices[0].message.content
            else :
                return completion.choices[0].message.content.split('-')[0]
        else:
            if self.chk2(msg) == False:
                return '{}:{}'.format("info", "시간 정보가 잘못되었습니다.")
            
            if self.type == 1:
                return self.day + completion.choices[0].message.content
            else :
                return self.day + completion.choices[0].message.content.split('-')[0]
            
    def fn_desc(self, msg):
        sys_content = '{0} {1} {2}'.format("일정을 '~년 ~월 ~일 ~시 ~분 일정은 (일정) 입니다' 형식으로 바꿔서 말해"
                                      ,"월의 맨앞이 0이면 0은 제외하고 말해줘"
                                      ,"분의 앞부분에 0이 포함되어 있다면 0을 제외하고 말해줘"
                                    
                                      )
        
        self.message.append({"role": "system", "content": sys_content })
        self.message.append({"role": "user", "content": msg})
        
        completion = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=self.message
        )
        
        return completion.choices[0].message.content
        


         
    
# name=input()
# mbti=input()

# # mat = sch(name, 1)
# mat = friend(name, mbti.upper())
# while True:
#     print( mat.fn_chat(input()))
#     print()
    
    
    
    
    
    
    
    
    
'''
while True:
    uInput = input("잘문 : ")
    message.append({"role": "user", "content": uInput})
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=message
    )

    print(completion.choices[0].message.content)
'''
