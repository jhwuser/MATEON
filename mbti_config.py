# mbti_dic ={}

def fn_getmbti(mbti_type):
    # mbti_dic = {name:''}
    # d=mbti_dic[name]    
    d=''
    if ('E' in mbti_type) and ('T' in mbti_type):
        d=d+',카리스마 있음, 내가 짱이다, 주장 강함, 자기 확신,'
    if ('E' in mbti_type) and ('F' in mbti_type):
        d=d+',밝고 높은 텐션, 분위기 메이커, 시끄러움,'
    if ('I' in mbti_type) and ('T' in mbti_type):
        d=d+',시니컬하고 회의주의적, 낮은 텐션, 다크함,'  
    if ('I' in mbti_type) and ('F' in mbti_type):
        d=d+',예술적, 아름다움 추구, 내적 갈등,'
    if ('N' in mbti_type) and ('T' in mbti_type):
        d=d+',지적 호기심, 어려운 문제 즐김, 물음표 살인마,'
    if ('N' in mbti_type) and ('F' in mbti_type):
        d=d+',섬세한 감수성, 생각이 많음, 순수함,'
    if ('S' in mbti_type) and ('T' in mbti_type):
        d=d+',현실주의, 자립심, 돌직구,'
    if ('S' in mbti_type) and ('F' in mbti_type):
        d=d+',융화됨, 긍정적, 우호적,'
    if ('I' in mbti_type) and ('N' in mbti_type):
        d=d+',괴짜, 망상 많이함, 속을 모름,'
    if ('E' in mbti_type) and ('N' in mbti_type):
        d=d+',또라이, 아이디어 뱅크,'
    if ('I' in mbti_type) and ('S' in mbti_type):
        d=d+',상식과 조화 중시, 차분함, 어른스러움,'
    if ('E' in mbti_type) and ('S' in mbti_type):
        d=d+',인싸, 사회생활 잘함, 붙임성 좋음,'
    if ('N' in mbti_type) and ('P' in mbti_type):
        d=d+',통제불능, ADHD, 현실 부적응,'
    if ('N' in mbti_type) and ('J' in mbti_type):
        d=d+',이상주의자, 리더형,'
    if ('S' in mbti_type) and ('P' in mbti_type):
        d=d+',자극 추구, 게으름, 오늘만 산다,'
    if ('S' in mbti_type) and ('J' in mbti_type):
        d=d+',꼼꼼함, 고집 셈, 안정 중시,'
    if ('T' in mbti_type) and ('P' in mbti_type):
        d=d+',직설적, 솔직함, 거침없음,'
    if ('T' in mbti_type) and ('J' in mbti_type):
        d=d+',칼같음, 차가움, 숨어있는 따뜻함,'
    if ('F' in mbti_type) and ('P' in mbti_type):
        d=d+',발랄함, 부드러움, 유연성,'
    if ('F' in mbti_type) and ('J' in mbti_type):
        d=d+',사려깊음, 챙겨주기, 믿음직스러움,'
    if ('E' in mbti_type) and ('P' in mbti_type):
        d=d+',개방적, 쾌활함, 자유로움, 시끄러움,'
    if ('E' in mbti_type)  and ('J' in mbti_type):
        d=d+',슈퍼 인싸, 친목 마스터, 항상 바쁜 일정,'
    if ('I' in mbti_type) and ('P' in mbti_type):
        d=d+',집순이&집돌이, 집에 가고 싶음, 연락 잘 안받음,'
    if ('I' in mbti_type) and ('J' in mbti_type):
        d=d+',혼자 하는 것을 선호, 혼자 부지런함,'
    return d



