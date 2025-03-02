from datetime import datetime
import os
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import sys

class Colors:
    """
    ANSI 顏色碼常量
    """
    HEADER = '\033[95m'      # 粉紫色
    BLUE = '\033[94m'        # 藍色
    CYAN = '\033[96m'        # 青色
    GREEN = '\033[92m'       # 綠色
    YELLOW = '\033[93m'      # 黃色
    RED = '\033[91m'         # 紅色
    BOLD = '\033[1m'         # 粗體
    UNDERLINE = '\033[4m'    # 底線
    END = '\033[0m'          # 結束顏色

def validate_date(date_str):
    """
    驗證日期格式是否正確
    
    Args:
        date_str (str): 日期字符串
        
    Returns:
        bool: 日期是否有效
    """
    try:
        datetime.strptime(date_str, '%Y%m%d')
        return True
    except ValueError:
        return False

def get_life_number_meaning(number):
    """
    獲取生命靈數的含義
    
    Args:
        number (int): 生命靈數
        
    Returns:
        str: 生命靈數的解釋
    """
    meanings = {
        1: "領導者：具有強大的創造力和獨立性，是天生的領袖。",
        2: "和平使者：具有外交手腕，善解人意，富有同情心。",
        3: "表達者：充滿創意和想像力，擅長溝通和自我表達。",
        4: "建造者：務實可靠，善於組織和規劃，注重細節。",
        5: "自由者：追求自由，喜歡冒險，適應力強。",
        6: "照顧者：富有同情心，重視家庭，具有責任感。",
        7: "思想者：具有哲學思維，喜歡研究和分析。",
        8: "實踐者：具有領導才能，重視物質成就。",
        9: "智者：富有同理心，具有理想主義特質。"
    }
    return meanings.get(number, "無效的生命靈數")

def calculate_life_number(birthdate):
    """
    計算生命靈數
    
    Args:
        birthdate (str): 出生日期，格式為 'YYYYMMDD'
        
    Returns:
        int: 生命靈數（1-9）
    """
    # 移除所有非數字字符
    numbers = ''.join(filter(str.isdigit, birthdate))
    
    # 持續加總直到得到個位數
    while len(numbers) > 1:
        total = sum(int(digit) for digit in numbers)
        numbers = str(total)
    
    return int(numbers)

def calculate_year_number(birthdate, year):
    """
    計算流年數字
    
    Args:
        birthdate (str): 出生日期，格式為 'YYYYMMDD'
        year (int): 要計算的年份
        
    Returns:
        int: 流年數字（1-9）
    """
    # 取出出生月日
    birth_month_day = birthdate[4:8]
    
    # 將年份和出生月日的數字相加
    total = sum(int(digit) for digit in str(year)) + sum(int(digit) for digit in birth_month_day)
    
    # 持續相加直到得到個位數
    while total > 9:
        total = sum(int(digit) for digit in str(total))
    
    return total

def get_year_number_meaning(number):
    """
    獲取流年數字的含義
    
    Args:
        number (int): 流年數字
        
    Returns:
        str: 流年數字的解釋
    """
    meanings = {
        1: "新的開始：這是個適合開始新計劃、展現領導力的一年。",
        2: "合作之年：重視人際關係，適合發展夥伴關係。",
        3: "創意表達：是個展現才華、擴大社交圈的好時機。",
        4: "建立基礎：需要務實工作，專注於建立穩固根基。",
        5: "改變之年：充滿變化與機會，要保持靈活。",
        6: "責任之年：家庭關係和諧，承擔責任的時期。",
        7: "內省成長：適合深度學習和靈性提升。",
        8: "豐收之年：事業發展和財運都很不錯。",
        9: "完成與放下：是個總結和轉化的年份。"
    }
    return meanings.get(number, "無效的流年數字")

def get_tarot_card(number):
    """
    獲取塔羅牌對應
    
    Args:
        number (int): 計算出的數字
        
    Returns:
        tuple: (牌名, 含義)
    """
    tarot_cards = {
        1: ("魔術師", "創造力、主動、新開始"),
        2: ("女祭司", "直覺、智慧、神秘"),
        3: ("皇后", "豐盛、創造力、母性"),
        4: ("皇帝", "權威、穩定、領導"),
        5: ("教皇", "信仰、傳統、指導"),
        6: ("戀人", "選擇、和諧、愛情"),
        7: ("戰車", "意志力、勝利、進展"),
        8: ("力量", "勇氣、耐心、內在力量"),
        9: ("隱士", "智慧、內省、指引"),
        10: ("命運之輪", "變化、機會、命運"),
        11: ("正義", "平衡、公正、真理"),
        12: ("懸吊者", "犧牲、等待、新視角"),
        13: ("死神", "結束、轉變、重生"),
        14: ("節制", "平衡、調和、耐心"),
        15: ("惡魔", "束縛、誘惑、執著"),
        16: ("高塔", "突變、覺醒、解放"),
        17: ("星星", "希望、靈感、指引"),
        18: ("月亮", "直覺、幻想、潛意識"),
        19: ("太陽", "快樂、活力、成功"),
        20: ("審判", "覺醒、重生、召喚"),
        21: ("世界", "完成、圓滿、統合"),
        22: ("愚人", "純真、冒險、自由")
    }
    return tarot_cards.get(number, ("未知", "無對應解釋"))

def calculate_life_tarot(birthdate):
    """
    計算生命塔羅牌
    
    Args:
        birthdate (str): 出生日期，格式為 'YYYYMMDD'
        
    Returns:
        int: 生命塔羅數字（1-22）
    """
    # 將出生日期所有數字相加
    total = sum(int(digit) for digit in birthdate)
    # 如果結果大於22，繼續相加直到得到1-22的數字
    while total > 22:
        total = sum(int(digit) for digit in str(total))
    return total

def calculate_soul_tarot(birthdate):
    """
    計算靈魂塔羅牌
    
    Args:
        birthdate (str): 出生日期，格式為 'YYYYMMDD'
        
    Returns:
        int: 靈魂塔羅數字（1-22）
    """
    # 只使用月份和日期進行計算
    month_day = birthdate[4:]
    total = sum(int(digit) for digit in month_day)
    while total > 22:
        total = sum(int(digit) for digit in str(total))
    return total

def calculate_year_tarot(birthdate, year):
    """
    計算指定年份的流年塔羅牌
    
    Args:
        birthdate (str): 出生日期，格式為 'YYYYMMDD'
        year (int): 要計算的年份
        
    Returns:
        int: 流年塔羅數字（1-22）
    """
    # 將出生年月日和目標年份相加
    total = sum(int(digit) for digit in birthdate) + sum(int(digit) for digit in str(year))
    while total > 22:
        total = sum(int(digit) for digit in str(total))
    return total

def calculate_talent_tarot(birthdate):
    """
    計算天賦塔羅牌
    
    Args:
        birthdate (str): 出生日期，格式為 'YYYYMMDD'
        
    Returns:
        int: 天賦塔羅數字（1-22）
    """
    # 使用年份的後兩位和日期計算
    year_last_two = birthdate[2:4]
    day = birthdate[6:8]
    total = sum(int(digit) for digit in year_last_two) + sum(int(digit) for digit in day)
    while total > 22:
        total = sum(int(digit) for digit in str(total))
    return total

def calculate_innate_tarot(birthdate):
    """
    計算先天塔羅牌（出生時的能量）
    
    Args:
        birthdate (str): 出生日期，格式為 'YYYYMMDD'
        
    Returns:
        int: 先天塔羅數字（1-22）
    """
    # 使用月份和日期的乘積
    month = int(birthdate[4:6])
    day = int(birthdate[6:8])
    total = month * day
    while total > 22:
        total = sum(int(digit) for digit in str(total))
    return total

def calculate_acquired_tarot(birthdate):
    """
    計算後天塔羅牌（人生歷程中培養的能量）
    
    Args:
        birthdate (str): 出生日期，格式為 'YYYYMMDD'
        
    Returns:
        int: 後天塔羅數字（1-22）
    """
    # 使用年份和月份的乘積
    year = int(birthdate[0:4])
    month = int(birthdate[4:6])
    total = year * month
    while total > 22:
        total = sum(int(digit) for digit in str(total))
    return total

def calculate_personality_tarot(birthdate):
    """
    計算人格塔羅牌（外在表現的性格特質）
    
    Args:
        birthdate (str): 出生日期，格式為 'YYYYMMDD'
        
    Returns:
        int: 人格塔羅數字（1-22）
    """
    # 使用年份的第一位和最後一位相加
    year = birthdate[0:4]
    total = int(year[0]) + int(year[3])
    while total > 22:
        total = sum(int(digit) for digit in str(total))
    return total

def calculate_shadow_tarot(birthdate):
    """
    計算陰影塔羅牌（潛意識中的特質）
    
    Args:
        birthdate (str): 出生日期，格式為 'YYYYMMDD'
        
    Returns:
        int: 陰影塔羅數字（1-22）
    """
    # 使用月份和年份中間兩位的乘積
    month = int(birthdate[4:6])
    year_middle = int(birthdate[1:3])
    total = month * year_middle
    while total > 22:
        total = sum(int(digit) for digit in str(total))
    return total

def calculate_ziwei_number(birthdate):
    """
    計算紫微靈動數
    
    Args:
        birthdate (str): 出生日期，格式為 'YYYYMMDD'
        
    Returns:
        tuple: (主星數, 副星數, 命宮數)
    """
    year = int(birthdate[0:4])
    month = int(birthdate[4:6])
    day = int(birthdate[6:8])
    
    # 計算主星數（年份各位相加）
    main_number = sum(int(digit) for digit in str(year))
    while main_number > 9:
        main_number = sum(int(digit) for digit in str(main_number))
    
    # 計算副星數（月日相乘後化簡）
    sub_number = month * day
    while sub_number > 9:
        sub_number = sum(int(digit) for digit in str(sub_number))
    
    # 計算命宮數（主星數+副星數）
    destiny_number = main_number + sub_number
    while destiny_number > 9:
        destiny_number = sum(int(digit) for digit in str(destiny_number))
    
    return (main_number, sub_number, destiny_number)

def get_ziwei_meaning(number):
    """
    獲取紫微數字的含義
    
    Args:
        number (int): 紫微數字
        
    Returns:
        str: 紫微數字的解釋
    """
    meanings = {
        1: "天乙星：領導力強，具有開創性思維，適合當領導者。",
        2: "天輔星：善解人意，具有外交手腕，是良好的協調者。",
        3: "天機星：聰明智慧，創意十足，擅長表達與溝通。",
        4: "天權星：穩重踏實，做事有條理，具有執行力。",
        5: "天同星：變化多端，適應力強，喜歡自由。",
        6: "天府星：富貴吉祥，心地善良，重視家庭。",
        7: "天貴星：智慧超群，有哲學思維，喜歡探索。",
        8: "天相星：財運亨通，事業有成，具有領導才能。",
        9: "天梁星：德高望重，具有理想抱負，富有同情心。"
    }
    return meanings.get(number, "無對應解釋")

def calculate_connection_numbers(birthdate):
    """
    計算生命靈數連線數
    
    Args:
        birthdate (str): 出生日期，格式為 'YYYYMMDD'
        
    Returns:
        tuple: (先天數, 生命數, 天賦數)
    """
    # 先天數：出生日期的日子化簡
    day = birthdate[6:8]
    innate = sum(int(d) for d in day)
    while innate > 9:
        innate = sum(int(d) for d in str(innate))
    
    # 生命數：月份化簡
    month = birthdate[4:6]
    life = sum(int(d) for d in month)
    while life > 9:
        life = sum(int(d) for d in str(life))
    
    # 天賦數：先天數+生命數的結果化簡
    talent = innate + life
    while talent > 9:
        talent = sum(int(d) for d in str(talent))
    
    return (innate, life, talent)

def get_connection_number_meaning(number, type_name):
    """
    獲取連線數的含義
    
    Args:
        number (int): 連線數
        type_name (str): 連線數類型
        
    Returns:
        str: 連線數的解釋
    """
    innate_meanings = {
        1: "天生的領導者，獨立自主，創新思維",
        2: "天生敏感，直覺強，善解人意",
        3: "天生具有創造力，表達能力強",
        4: "天生務實，有條理，重視細節",
        5: "天生追求自由，適應力強",
        6: "天生富有同情心，重視和諧",
        7: "天生具分析力，喜歡探索",
        8: "天生具權威感，重視成就",
        9: "天生理想主義，富有同理心"
    }
    
    life_meanings = {
        1: "人生課題在於發展獨立性和創造力",
        2: "人生課題在於學習合作與關係",
        3: "人生課題在於發展創意和表達",
        4: "人生課題在於建立穩定和秩序",
        5: "人生課題在於追求自由和改變",
        6: "人生課題在於創造和諧與平衡",
        7: "人生課題在於追求智慧和靈性",
        8: "人生課題在於掌握權力和物質",
        9: "人生課題在於服務和奉獻"
    }
    
    talent_meanings = {
        1: "具有開創和領導的天賦",
        2: "具有外交和協調的天賦",
        3: "具有創意和溝通的天賦",
        4: "具有組織和執行的天賦",
        5: "具有適應和冒險的天賦",
        6: "具有關懷和照顧的天賦",
        7: "具有思考和研究的天賦",
        8: "具有管理和成就的天賦",
        9: "具有智慧和奉獻的天賦"
    }
    
    meanings = {
        "先天數": innate_meanings,
        "生命數": life_meanings,
        "天賦數": talent_meanings
    }
    
    return meanings[type_name].get(number, "無對應解釋")

def calculate_zodiac_number(birthdate):
    """
    計算星座數
    
    Args:
        birthdate (str): 出生日期，格式為 'YYYYMMDD'
        
    Returns:
        tuple: (星座數, 星座名稱)
    """
    month = int(birthdate[4:6])
    day = int(birthdate[6:8])
    
    zodiac_dates = [
        ((3, 21), (4, 19), "白羊座", 1),
        ((4, 20), (5, 20), "金牛座", 2),
        ((5, 21), (6, 21), "雙子座", 3),
        ((6, 22), (7, 22), "巨蟹座", 4),
        ((7, 23), (8, 22), "獅子座", 5),
        ((8, 23), (9, 22), "處女座", 6),
        ((9, 23), (10, 23), "天秤座", 7),
        ((10, 24), (11, 22), "天蠍座", 8),
        ((11, 23), (12, 21), "射手座", 9),
        ((12, 22), (1, 19), "魔羯座", 1),
        ((1, 20), (2, 18), "水瓶座", 2),
        ((2, 19), (3, 20), "雙魚座", 3)
    ]
    
    for (start_m, start_d), (end_m, end_d), name, number in zodiac_dates:
        if (month == start_m and day >= start_d) or (month == end_m and day <= end_d):
            return (number, name)
    
    return (0, "未知星座")

def get_zodiac_meaning(number):
    """
    獲取星座數的含義
    
    Args:
        number (int): 星座數
        
    Returns:
        str: 星座數的解釋
    """
    meanings = {
        1: "開創性格：具有領導力、創新精神和冒險精神",
        2: "固定性格：穩重、堅持、重視物質和安全感",
        3: "變動性格：靈活多變、適應力強、思維活躍",
        4: "情感性格：敏感、富同情心、重視家庭",
        5: "表現性格：熱情、創意、追求關注",
        6: "分析性格：理性、完美主義、注重細節",
        7: "和諧性格：追求平衡、重視關係、具外交手腕",
        8: "神秘性格：洞察力強、意志堅定、重視權力",
        9: "理想性格：樂觀、追求自由、具哲學思維"
    }
    return meanings.get(number, "無對應解釋")

def calculate_life_grid(birthdate):
    """
    計算生命靈數九宮格
    
    Args:
        birthdate (str): 出生日期，格式為 'YYYYMMDD'
        
    Returns:
        dict: 九宮格各位置的數字
    """
    grid = {
        '思想': [],  # 頭部 - 思維模式
        '精神': [],  # 精神層面
        '愛情': [],  # 感情世界
        '健康': [],  # 身體狀況
        '意志': [],  # 意志力量
        '直覺': [],  # 直覺能力
        '物質': [],  # 物質基礎
        '才能': [],  # 天賦才能
        '智慧': []   # 智慧程度
    }
    
    # 收集所有出現的數字
    for digit in birthdate:
        num = int(digit)
        if num == 0:
            continue
        if num == 1: grid['思想'].append(num)
        elif num == 2: grid['精神'].append(num)
        elif num == 3: grid['愛情'].append(num)
        elif num == 4: grid['健康'].append(num)
        elif num == 5: grid['意志'].append(num)
        elif num == 6: grid['直覺'].append(num)
        elif num == 7: grid['物質'].append(num)
        elif num == 8: grid['才能'].append(num)
        elif num == 9: grid['智慧'].append(num)
    
    return grid

def analyze_life_grid(grid):
    """
    分析九宮格的數字連線
    
    Args:
        grid (dict): 九宮格數字分布
        
    Returns:
        tuple: (強項列表, 弱項列表, 連線分析)
    """
    strengths = []
    weaknesses = []
    connections = []
    
    # 分析數字出現次數
    for position, numbers in grid.items():
        count = len(numbers)
        if count >= 2:
            strengths.append(f"{position}({count}次): 在{position}方面特別突出")
        elif count == 0:
            weaknesses.append(f"{position}: 需要在{position}方面多加努力")
    
    # 分析數字連線
    # 思想-意志-智慧 連線
    if grid['思想'] and grid['意志'] and grid['智慧']:
        connections.append("思想-意志-智慧連線：具有強大的思考能力和決策力")
    
    # 精神-意志-直覺 連線
    if grid['精神'] and grid['意志'] and grid['直覺']:
        connections.append("精神-意志-直覺連線：直覺敏銳，精神意志力強")
    
    # 愛情-意志-物質 連線
    if grid['愛情'] and grid['意志'] and grid['物質']:
        connections.append("愛情-意志-物質連線：感情和物質生活平衡")
    
    # 思想-精神-愛情 連線
    if grid['思想'] and grid['精神'] and grid['愛情']:
        connections.append("思想-精神-愛情連線：感情生活理性且富有靈性")
    
    # 健康-意志-才能 連線
    if grid['健康'] and grid['意志'] and grid['才能']:
        connections.append("健康-意志-才能連線：具有充沛精力發展才能")
    
    return strengths, weaknesses, connections

def show_calculation_methods():
    """
    顯示所有數字的計算方法說明
    """
    c = Colors()  # 創建顏色對象以簡化使用
    
    print(f"\n{c.BOLD}" + "="*70 + f"{c.END}")
    print(f"{c.HEADER}計算方法詳細說明{c.END}")
    print(f"{c.BOLD}" + "="*70 + f"{c.END}")
    
    print(f"\n{c.BOLD}【基礎計算】{c.END}")
    print(f"{c.BLUE}1. 生命靈數：{c.END}")
    print(f"{c.CYAN}   計算方法：{c.END}將出生年月日的所有數字相加，重複相加直到得到個位數")
    print(f"{c.GREEN}   驗證範例：{c.END}")
    print("   出生日期：19900101")
    print(f"{c.YELLOW}   計算過程：{c.END}1+9+9+0+0+1+0+1 = 21")
    print("             2+1 = 3")
    print(f"{c.RED}   結果：{c.END}生命靈數為 3")
    
    print(f"\n{c.BOLD}【紫微靈動數】{c.END}")
    print(f"{c.BLUE}1. 主星數：{c.END}")
    print(f"{c.CYAN}   計算方法：{c.END}將出生年份的數字相加直到得到個位數")
    print(f"{c.GREEN}   驗證範例：{c.END}")
    print("   出生年份：1990")
    print(f"{c.YELLOW}   計算過程：{c.END}1+9+9+0 = 19")
    print("             1+9 = 10")
    print("             1+0 = 1")
    print(f"{c.RED}   結果：{c.END}主星數為 1")
    
    print(f"\n{c.BLUE}2. 副星數：{c.END}")
    print(f"{c.CYAN}   計算方法：{c.END}將出生月份和日期相乘後化簡至個位數")
    print(f"{c.GREEN}   驗證範例：{c.END}")
    print("   出生月日：0101（1月1日）")
    print(f"{c.YELLOW}   計算過程：{c.END}1 × 1 = 1")
    print(f"{c.RED}   結果：{c.END}副星數為 1")
    
    print(f"\n{c.BLUE}3. 命宮數：{c.END}")
    print(f"{c.CYAN}   計算方法：{c.END}主星數加副星數後化簡至個位數")
    print(f"{c.GREEN}   驗證範例：{c.END}")
    print(f"{c.YELLOW}   計算過程：{c.END}1 + 1 = 2")
    print(f"{c.RED}   結果：{c.END}命宮數為 2")
    
    print(f"\n{c.BOLD}【塔羅牌計算】{c.END}")
    print(f"{c.CYAN}所有塔羅牌數字需要化簡至1-22之間{c.END}")
    print(f"{c.BLUE}1. 生命塔羅：{c.END}")
    print(f"{c.CYAN}   計算方法：{c.END}出生年月日所有數字相加")
    print(f"{c.GREEN}   驗證範例：{c.END}19900101")
    print(f"{c.YELLOW}   計算過程：{c.END}1+9+9+0+0+1+0+1 = 21")
    print(f"{c.RED}   結果：{c.END}生命塔羅為 21 號牌（世界）")
    
    print(f"\n{c.BLUE}2. 靈魂塔羅：{c.END}")
    print(f"{c.CYAN}   計算方法：{c.END}只計算月份和日期的數字總和")
    print(f"{c.GREEN}   驗證範例：{c.END}19900101 中的 0101")
    print(f"{c.YELLOW}   計算過程：{c.END}0+1+0+1 = 2")
    print(f"{c.RED}   結果：{c.END}靈魂塔羅為 2 號牌（女祭司）")
    
    print(f"\n{c.BLUE}3. 天賦塔羅：{c.END}")
    print(f"{c.CYAN}   計算方法：{c.END}年份後兩位加上日期的數字總和")
    print(f"{c.GREEN}   驗證範例：{c.END}1990年01月01日")
    print(f"{c.YELLOW}   計算過程：{c.END}9+0+0+1 = 10")
    print(f"{c.RED}   結果：{c.END}天賦塔羅為 10 號牌（命運之輪）")
    
    print(f"\n{c.BOLD}【流年計算】{c.END}")
    print(f"{c.BLUE}1. 流年數字：{c.END}")
    print(f"{c.CYAN}   計算方法：{c.END}將目標年份數字與出生月日相加，化簡至個位數")
    print(f"{c.GREEN}   驗證範例：{c.END}")
    print("   出生日期：19790619")
    print(f"{c.YELLOW}   目標年份：{c.END}2025")
    print(f"{c.YELLOW}   計算過程：{c.END}2+0+2+5+0+6+1+9 = 25")
    print("             2+5 = 7")
    print(f"{c.RED}   結果：{c.END}2025年的流年數字為 7")
    
    print(f"\n{c.BLUE}2. 流年塔羅：{c.END}")
    print(f"{c.CYAN}   計算方法：{c.END}將完整出生年月日和目標年份的數字相加後化簡至22以內")
    print(f"{c.GREEN}   驗證範例：{c.END}")
    print("   出生日期：19790619")
    print(f"{c.YELLOW}   目標年份：{c.END}2025")
    print(f"{c.YELLOW}   計算過程：{c.END}1+9+7+9+0+6+1+9+2+0+2+5 = 51")
    print("             5+1 = 6")
    print(f"{c.RED}   結果：{c.END}2025年的流年塔羅為 6 號牌（戀人）")
    
    print(f"\n{c.BOLD}註：{c.END}")
    print(f"{c.CYAN}1.「化簡至個位數」{c.END}指重複將數字相加直到得到1-9的數字")
    print(f"{c.CYAN}2.「化簡至22以內」{c.END}指重複將數字相加直到得到1-22的數字")
    print(f"{c.CYAN}3. 所有計算過程中的數字都是按照順序逐位相加{c.END}")
    print(f"{c.BOLD}" + "="*70 + f"{c.END}")
    input(f"\n{c.YELLOW}按Enter鍵繼續...{c.END}")

def supports_color():
    """
    檢查當前環境是否支持顏色顯示
    """
    import platform
    
    plat = platform.system().lower()
    supported_platform = plat != 'windows' or 'ANSICON' in os.environ
    
    is_a_tty = hasattr(sys.stdout, 'isatty') and sys.stdout.isatty()
    
    return supported_platform and is_a_tty

class LifeNumberCalculatorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("生命靈數計算器")
        self.root.geometry("1200x800")  # 加大視窗尺寸
        
        # 設置主題顏色和字體
        self.style = ttk.Style()
        self.style.configure("TFrame", background="#f0f0f0")
        self.style.configure("TLabel", background="#f0f0f0", font=('微軟正黑體', 14))
        self.style.configure("TButton", font=('微軟正黑體', 14))
        
        # 創建主框架
        self.main_frame = ttk.Frame(self.root, padding="20")  # 增加padding
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 輸入區域
        self.input_frame = ttk.Frame(self.main_frame)
        self.input_frame.grid(row=0, column=0, pady=20)
        
        ttk.Label(self.input_frame, text="請輸入出生日期（YYYYMMDD）：").grid(row=0, column=0, padx=10)
        self.date_entry = ttk.Entry(self.input_frame, width=20, font=('微軟正黑體', 14))
        self.date_entry.grid(row=0, column=1, padx=10)
        
        ttk.Button(self.input_frame, text="計算", command=self.calculate).grid(row=0, column=2, padx=10)
        
        # 結果顯示區域
        self.result_frame = ttk.Frame(self.main_frame)
        self.result_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 使用 Notebook 創建標籤頁
        self.notebook = ttk.Notebook(self.result_frame)
        self.notebook.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 各個標籤頁
        self.life_number_tab = ttk.Frame(self.notebook)
        self.ziwei_tab = ttk.Frame(self.notebook)
        self.tarot_tab = ttk.Frame(self.notebook)
        self.grid_tab = ttk.Frame(self.notebook)
        
        self.notebook.add(self.life_number_tab, text="生命靈數與連線數")
        self.notebook.add(self.ziwei_tab, text="紫微靈動數")
        self.notebook.add(self.tarot_tab, text="塔羅牌")
        self.notebook.add(self.grid_tab, text="九宮格")
        
        # 在生命靈數標籤頁中創建兩個子框架
        self.life_frame = ttk.Frame(self.life_number_tab)
        self.life_frame.grid(row=0, column=0, padx=10, pady=10, sticky='nsew')
        
        # 設置文本顯示區域的字體和樣式
        text_font = ('微軟正黑體', 14)
        text_width = 60
        text_height = 30
        
        # 創建生命靈數顯示區域
        self.life_text = scrolledtext.ScrolledText(self.life_frame, 
            width=text_width, height=text_height, font=text_font)
        self.life_text.grid(row=0, column=0, padx=5, pady=5)
        
        # 設置標籤文字顏色
        self.life_text.tag_configure("title", foreground="#9932CC", font=('微軟正黑體', 16, 'bold'))  # 紫色
        self.life_text.tag_configure("subtitle", foreground="#4169E1", font=('微軟正黑體', 14, 'bold'))  # 皇家藍
        self.life_text.tag_configure("process", foreground="white", background="#2F4F4F")  # 白色字體，深灰背景
        self.life_text.tag_configure("result", foreground="#FF4500", font=('微軟正黑體', 14, 'bold'))  # 橙紅色
        self.life_text.tag_configure("meaning", foreground="#CD853F", font=('微軟正黑體', 14))  # 秘魯色
        self.life_text.tag_configure("connection", foreground="#20B2AA", font=('微軟正黑體', 14, 'bold'))  # 淺海藍
        
        # 添加紫微靈動數和塔羅牌的顯示區域
        self.ziwei_text = scrolledtext.ScrolledText(self.ziwei_tab, 
            width=text_width, height=text_height, font=text_font)
        self.ziwei_text.grid(row=0, column=0, padx=5, pady=5)
        
        self.tarot_text = scrolledtext.ScrolledText(self.tarot_tab, 
            width=text_width, height=text_height, font=text_font)
        self.tarot_text.grid(row=0, column=0, padx=5, pady=5)
        
        # 為紫微靈動數和塔羅牌的顯示區域設置相同的顏色
        for text_widget in [self.ziwei_text, self.tarot_text]:
            text_widget.tag_configure("title", foreground="#9932CC", font=('微軟正黑體', 16, 'bold'))
            text_widget.tag_configure("subtitle", foreground="#4169E1", font=('微軟正黑體', 14, 'bold'))
            text_widget.tag_configure("process", foreground="white", background="#2F4F4F")
            text_widget.tag_configure("result", foreground="#FF4500", font=('微軟正黑體', 14, 'bold'))
            text_widget.tag_configure("meaning", foreground="#CD853F", font=('微軟正黑體', 14))
        
        # 設置文本區域的背景顏色
        for text_widget in [self.life_text, self.ziwei_text, self.tarot_text]:
            text_widget.configure(bg='#1E1E1E')  # 深色背景
            text_widget.configure(fg='white')     # 默認白色文字
    
        # 九宮格標籤頁的設置
        self.grid_frame = ttk.Frame(self.grid_tab)
        self.grid_frame.grid(row=0, column=0, padx=10, pady=10, sticky='nsew')
        
        # 九宮格畫布
        self.grid_canvas = tk.Canvas(self.grid_frame, width=500, height=500, 
            bg='#1E1E1E', highlightthickness=2)
        self.grid_canvas.grid(row=0, column=0, padx=10, pady=10)
        
        # 九宮格解釋文本區域
        self.grid_text = scrolledtext.ScrolledText(self.grid_frame, 
            width=40, height=30, font=('微軟正黑體', 14))
        self.grid_text.grid(row=0, column=1, padx=10, pady=10)
        
        # 設置九宮格文本區域的顏色和標籤
        self.grid_text.configure(bg='#1E1E1E', fg='white')
        self.grid_text.tag_configure("title", foreground="#9932CC", font=('微軟正黑體', 16, 'bold'))
        self.grid_text.tag_configure("subtitle", foreground="#4169E1", font=('微軟正黑體', 14, 'bold'))
        self.grid_text.tag_configure("process", foreground="white", background="#2F4F4F")
        self.grid_text.tag_configure("result", foreground="#FF4500", font=('微軟正黑體', 14, 'bold'))
        self.grid_text.tag_configure("meaning", foreground="#CD853F", font=('微軟正黑體', 14))
    
    def draw_grid(self, grid_data):
        """繪製九宮格"""
        self.grid_canvas.delete("all")
        cell_size = 150
        start_x = 25
        start_y = 25
        
        # 繪製格子
        for i in range(4):
            self.grid_canvas.create_line(start_x, start_y + i*cell_size, 
                start_x + 3*cell_size, start_y + i*cell_size, 
                fill='white', width=2)
            self.grid_canvas.create_line(start_x + i*cell_size, start_y, 
                start_x + i*cell_size, start_y + 3*cell_size, 
                fill='white', width=2)
        
        # 填充數字
        positions = [
            ('思想', 0, 0), ('精神', 1, 0), ('愛情', 2, 0),
            ('健康', 0, 1), ('意志', 1, 1), ('直覺', 2, 1),
            ('物質', 0, 2), ('才能', 1, 2), ('智慧', 2, 2)
        ]
        
        for pos, x, y in positions:
            numbers = grid_data[pos]
            count = len(numbers)
            text = f"{pos}\n{count}次\n{numbers if count > 0 else '空'}"
            self.grid_canvas.create_text(
                start_x + x*cell_size + cell_size/2,
                start_y + y*cell_size + cell_size/2,
                text=text,
                font=('微軟正黑體', 14, 'bold'),
                fill='white',
                justify=tk.CENTER
            )
    
    def calculate(self):
        """執行計算並顯示結果"""
        birthdate = self.date_entry.get()
        
        if not validate_date(birthdate):
            tk.messagebox.showerror("錯誤", "請輸入有效的日期！")
            return
            
        # 清空所有文本區域
        self.life_text.delete(1.0, tk.END)
        self.ziwei_text.delete(1.0, tk.END)
        self.tarot_text.delete(1.0, tk.END)
        
        # 計算各項數值
        life_number = calculate_life_number(birthdate)
        life_meaning = get_life_number_meaning(life_number)
        
        # 計算生命塔羅
        life_tarot_number = calculate_life_tarot(birthdate)
        life_tarot_card, life_tarot_meaning = get_tarot_card(life_tarot_number)
        
        # 計算靈魂塔羅
        soul_tarot_number = calculate_soul_tarot(birthdate)
        soul_tarot_card, soul_tarot_meaning = get_tarot_card(soul_tarot_number)
        
        # 計算天賦塔羅
        talent_tarot_number = calculate_talent_tarot(birthdate)
        talent_tarot_card, talent_tarot_meaning = get_tarot_card(talent_tarot_number)
        
        # 計算先天和後天塔羅
        innate_tarot_number = calculate_innate_tarot(birthdate)
        innate_tarot_card, innate_tarot_meaning = get_tarot_card(innate_tarot_number)
        
        acquired_tarot_number = calculate_acquired_tarot(birthdate)
        acquired_tarot_card, acquired_tarot_meaning = get_tarot_card(acquired_tarot_number)
        
        # 計算人格和陰影塔羅
        personality_tarot_number = calculate_personality_tarot(birthdate)
        personality_tarot_card, personality_tarot_meaning = get_tarot_card(personality_tarot_number)
        
        shadow_tarot_number = calculate_shadow_tarot(birthdate)
        shadow_tarot_card, shadow_tarot_meaning = get_tarot_card(shadow_tarot_number)
        
        # 計算今年的流年數字
        current_year = datetime.now().year
        year_number = calculate_year_number(birthdate, current_year)
        year_meaning = get_year_number_meaning(year_number)
        
        # 計算明年的流年數字
        next_year = current_year + 1
        next_year_number = calculate_year_number(birthdate, next_year)
        next_year_meaning = get_year_number_meaning(next_year_number)
        
        # 計算今年和明年的流年塔羅
        current_year_tarot = calculate_year_tarot(birthdate, current_year)
        current_year_tarot_card, current_year_tarot_meaning = get_tarot_card(current_year_tarot)
        
        next_year_tarot = calculate_year_tarot(birthdate, next_year)
        next_year_tarot_card, next_year_tarot_meaning = get_tarot_card(next_year_tarot)
        
        # 計算紫微靈動數
        main_number, sub_number, destiny_number = calculate_ziwei_number(birthdate)
        main_meaning = get_ziwei_meaning(main_number)
        sub_meaning = get_ziwei_meaning(sub_number)
        destiny_meaning = get_ziwei_meaning(destiny_number)
        
        # 計算連線數
        innate_num, life_num, talent_num = calculate_connection_numbers(birthdate)
        innate_meaning = get_connection_number_meaning(innate_num, "先天數")
        life_meaning_conn = get_connection_number_meaning(life_num, "生命數")
        talent_meaning_conn = get_connection_number_meaning(talent_num, "天賦數")
        
        # 計算星座數
        zodiac_number, zodiac_name = calculate_zodiac_number(birthdate)
        zodiac_meaning = get_zodiac_meaning(zodiac_number)
        
        # 更新生命靈數和連線數顯示
        self.life_text.delete(1.0, tk.END)
        
        # 生命靈數部分
        self.life_text.insert(tk.END, "【生命靈數計算】\n\n", "title")
        self.life_text.insert(tk.END, "◆ 計算方式\n", "subtitle")
        self.life_text.insert(tk.END, "將出生年月日的所有數字相加，若大於9則繼續相加直到得到個位數\n\n", "process")
        
        self.life_text.insert(tk.END, f"出生日期：{birthdate}\n", "process")
        digits = '+'.join(birthdate)
        total = sum(int(d) for d in birthdate)
        self.life_text.insert(tk.END, f"第一步：{digits} = {total}\n", "process")
        if total > 9:
            life_number = sum(int(d) for d in str(total))
            self.life_text.insert(tk.END, f"第二步：{'+'.join(str(total))} = {life_number}\n", "process")
        
        self.life_text.insert(tk.END, f"\n結果：生命靈數為 {life_number}\n", "result")
        self.life_text.insert(tk.END, f"含義：{life_meaning}\n\n", "meaning")
        
        # 流年數部分
        self.life_text.insert(tk.END, "【流年數計算】\n", "title")
        self.life_text.insert(tk.END, "◆ 計算方式\n", "subtitle")
        self.life_text.insert(tk.END, "當年年份數字與出生月日相加，若大於9則繼續相加\n\n", "process")
        
        self.life_text.insert(tk.END, f"當前年份：{current_year}\n", "process")
        self.life_text.insert(tk.END, f"結果：流年數為 {year_number}\n", "result")
        self.life_text.insert(tk.END, f"含義：{year_meaning}\n\n", "meaning")
        
        # 連線數部分
        self.life_text.insert(tk.END, "\n【生命靈數連線數】\n\n", "title")
        
        # 先天數
        self.life_text.insert(tk.END, "1. 先天數\n", "connection")
        self.life_text.insert(tk.END, "◆ 計算方式：出生日期中的「日」的數字相加\n", "subtitle")
        self.life_text.insert(tk.END, f"計算過程：{birthdate[6:8]} → {'+'.join(birthdate[6:8])} = {innate_num}\n", "process")
        self.life_text.insert(tk.END, f"含義：{innate_meaning}\n\n", "meaning")
        
        # 生命數
        self.life_text.insert(tk.END, "2. 生命數\n", "connection")
        self.life_text.insert(tk.END, "◆ 計算方式：出生日期中的「月份」數字相加\n", "subtitle")
        self.life_text.insert(tk.END, f"計算過程：{birthdate[4:6]} → {'+'.join(birthdate[4:6])} = {life_num}\n", "process")
        self.life_text.insert(tk.END, f"含義：{life_meaning_conn}\n\n", "meaning")
        
        # 天賦數
        self.life_text.insert(tk.END, "3. 天賦數\n", "connection")
        self.life_text.insert(tk.END, "◆ 計算方式：先天數與生命數相加\n", "subtitle")
        self.life_text.insert(tk.END, f"計算過程：{innate_num} + {life_num} = {talent_num}\n", "process")
        self.life_text.insert(tk.END, f"含義：{talent_meaning_conn}\n\n", "meaning")
        
        # 星座數
        self.life_text.insert(tk.END, "4. 星座數\n", "connection")
        self.life_text.insert(tk.END, f"星座：{zodiac_name}（{zodiac_number}）\n", "process")
        self.life_text.insert(tk.END, f"含義：{zodiac_meaning}\n\n", "meaning")
        
        # 紫微靈動數顯示
        self.ziwei_text.insert(tk.END, "【紫微靈動數計算】\n\n", "title")
        
        # 主星數
        self.ziwei_text.insert(tk.END, "1. 主星數\n", "subtitle")
        self.ziwei_text.insert(tk.END, "◆ 計算方式：年份數字相加化簡\n", "process")
        self.ziwei_text.insert(tk.END, f"年份：{birthdate[0:4]}\n", "process")
        year_digits = '+'.join(birthdate[0:4])
        self.ziwei_text.insert(tk.END, f"計算過程：{year_digits} = {main_number}\n", "process")
        self.ziwei_text.insert(tk.END, f"結果：主星數為 {main_number}\n", "result")
        self.ziwei_text.insert(tk.END, f"含義：{main_meaning}\n\n", "meaning")
        
        # 副星數
        self.ziwei_text.insert(tk.END, "2. 副星數\n", "subtitle")
        self.ziwei_text.insert(tk.END, "◆ 計算方式：月份與日期相乘後化簡\n", "process")
        self.ziwei_text.insert(tk.END, f"月份：{birthdate[4:6]}\n日期：{birthdate[6:8]}\n", "process")
        self.ziwei_text.insert(tk.END, f"計算過程：{birthdate[4:6]} × {birthdate[6:8]} = {sub_number}\n", "process")
        self.ziwei_text.insert(tk.END, f"結果：副星數為 {sub_number}\n", "result")
        self.ziwei_text.insert(tk.END, f"含義：{sub_meaning}\n\n", "meaning")
        
        # 命宮數
        self.ziwei_text.insert(tk.END, "3. 命宮數\n", "subtitle")
        self.ziwei_text.insert(tk.END, "◆ 計算方式：主星數與副星數相加\n", "process")
        self.ziwei_text.insert(tk.END, f"計算過程：{main_number} + {sub_number} = {destiny_number}\n", "process")
        self.ziwei_text.insert(tk.END, f"結果：命宮數為 {destiny_number}\n", "result")
        self.ziwei_text.insert(tk.END, f"含義：{destiny_meaning}\n\n", "meaning")
        
        # 塔羅牌顯示
        self.tarot_text.insert(tk.END, "【塔羅牌計算】\n\n", "title")
        
        # 生命塔羅
        self.tarot_text.insert(tk.END, "1. 生命塔羅\n", "subtitle")
        self.tarot_text.insert(tk.END, "◆ 計算方式：出生年月日所有數字相加\n", "process")
        self.tarot_text.insert(tk.END, f"計算過程：{'+'.join(birthdate)} = {life_tarot_number}\n", "process")
        self.tarot_text.insert(tk.END, f"結果：{life_tarot_card}（{life_tarot_number}號牌）\n", "result")
        self.tarot_text.insert(tk.END, f"含義：{life_tarot_meaning}\n\n", "meaning")
        
        # 靈魂塔羅
        self.tarot_text.insert(tk.END, "2. 靈魂塔羅\n", "subtitle")
        self.tarot_text.insert(tk.END, "◆ 計算方式：月份和日期數字相加\n", "process")
        self.tarot_text.insert(tk.END, f"計算過程：{'+'.join(birthdate[4:8])} = {soul_tarot_number}\n", "process")
        self.tarot_text.insert(tk.END, f"結果：{soul_tarot_card}（{soul_tarot_number}號牌）\n", "result")
        self.tarot_text.insert(tk.END, f"含義：{soul_tarot_meaning}\n\n", "meaning")
        
        # 天賦塔羅
        self.tarot_text.insert(tk.END, "3. 天賦塔羅\n", "subtitle")
        self.tarot_text.insert(tk.END, "◆ 計算方式：年份後兩位加上日期的數字相加\n", "process")
        self.tarot_text.insert(tk.END, f"年份後兩位：{birthdate[2:4]}\n日期：{birthdate[6:8]}\n", "process")
        self.tarot_text.insert(tk.END, f"計算過程：{'+'.join(birthdate[2:4])}+{'+'.join(birthdate[6:8])} = {talent_tarot_number}\n", "process")
        self.tarot_text.insert(tk.END, f"結果：{talent_tarot_card}（{talent_tarot_number}號牌）\n", "result")
        self.tarot_text.insert(tk.END, f"含義：{talent_tarot_meaning}\n\n", "meaning")
        
        # 先天塔羅
        self.tarot_text.insert(tk.END, "4. 先天塔羅\n", "subtitle")
        self.tarot_text.insert(tk.END, "◆ 計算方式：月份與日期相乘後化簡\n", "process")
        month = int(birthdate[4:6])
        day = int(birthdate[6:8])
        product = month * day
        self.tarot_text.insert(tk.END, f"計算過程：{month} × {day} = {product}\n", "process")
        if product > 22:
            self.tarot_text.insert(tk.END, f"化簡：{'+'.join(str(product))} = {innate_tarot_number}\n", "process")
        self.tarot_text.insert(tk.END, f"結果：{innate_tarot_card}（{innate_tarot_number}號牌）\n", "result")
        self.tarot_text.insert(tk.END, f"含義：{innate_tarot_meaning}\n\n", "meaning")
        
        # 後天塔羅
        self.tarot_text.insert(tk.END, "5. 後天塔羅\n", "subtitle")
        self.tarot_text.insert(tk.END, "◆ 計算方式：年份與月份相乘後化簡\n", "process")
        year = int(birthdate[0:4])
        product = year * month
        self.tarot_text.insert(tk.END, f"計算過程：{year} × {month} = {product}\n", "process")
        if product > 22:
            self.tarot_text.insert(tk.END, f"化簡：{'+'.join(str(product))} = {acquired_tarot_number}\n", "process")
        self.tarot_text.insert(tk.END, f"結果：{acquired_tarot_card}（{acquired_tarot_number}號牌）\n", "result")
        self.tarot_text.insert(tk.END, f"含義：{acquired_tarot_meaning}\n\n", "meaning")
        
        # 人格塔羅
        self.tarot_text.insert(tk.END, "6. 人格塔羅\n", "subtitle")
        self.tarot_text.insert(tk.END, "◆ 計算方式：年份的第一位和最後一位相加\n", "process")
        first_digit = birthdate[0]
        last_digit = birthdate[3]
        self.tarot_text.insert(tk.END, f"年份第一位：{first_digit}\n年份最後一位：{last_digit}\n", "process")
        self.tarot_text.insert(tk.END, f"計算過程：{first_digit} + {last_digit} = {personality_tarot_number}\n", "process")
        self.tarot_text.insert(tk.END, f"結果：{personality_tarot_card}（{personality_tarot_number}號牌）\n", "result")
        self.tarot_text.insert(tk.END, f"含義：{personality_tarot_meaning}\n\n", "meaning")
        
        # 陰影塔羅
        self.tarot_text.insert(tk.END, "7. 陰影塔羅\n", "subtitle")
        self.tarot_text.insert(tk.END, "◆ 計算方式：月份與年份中間兩位相乘後化簡\n", "process")
        year_middle = int(birthdate[1:3])
        product = month * year_middle
        self.tarot_text.insert(tk.END, f"月份：{month}\n年份中間兩位：{year_middle}\n", "process")
        self.tarot_text.insert(tk.END, f"計算過程：{month} × {year_middle} = {product}\n", "process")
        if product > 22:
            self.tarot_text.insert(tk.END, f"化簡：{'+'.join(str(product))} = {shadow_tarot_number}\n", "process")
        self.tarot_text.insert(tk.END, f"結果：{shadow_tarot_card}（{shadow_tarot_number}號牌）\n", "result")
        self.tarot_text.insert(tk.END, f"含義：{shadow_tarot_meaning}\n\n", "meaning")
        
        # 在塔羅牌顯示區域添加配牌說明
        self.tarot_text.insert(tk.END, "【塔羅牌配牌解讀】\n\n", "title")
        
        # 主要配牌組合
        self.tarot_text.insert(tk.END, "◆ 生命塔羅 + 靈魂塔羅\n", "subtitle")
        self.tarot_text.insert(tk.END, f"組合：{life_tarot_card} + {soul_tarot_card}\n", "process")
        self.tarot_text.insert(tk.END, "代表：顯示您目前生命歷程中的主要課題和靈魂學習\n\n", "meaning")
        
        # 天賦配牌組合
        self.tarot_text.insert(tk.END, "◆ 天賦塔羅 + 先天塔羅\n", "subtitle")
        self.tarot_text.insert(tk.END, f"組合：{talent_tarot_card} + {innate_tarot_card}\n", "process")
        self.tarot_text.insert(tk.END, "代表：展現您與生俱來的能力和潛在天賦\n\n", "meaning")
        
        # 成長配牌組合
        self.tarot_text.insert(tk.END, "◆ 後天塔羅 + 人格塔羅\n", "subtitle")
        self.tarot_text.insert(tk.END, f"組合：{acquired_tarot_card} + {personality_tarot_card}\n", "process")
        self.tarot_text.insert(tk.END, "代表：顯示您在成長過程中發展出的特質\n\n", "meaning")
        
        # 整體發展方向
        self.tarot_text.insert(tk.END, "◆ 生命方向配牌\n", "subtitle")
        self.tarot_text.insert(tk.END, "生命塔羅 → 靈魂塔羅 → 天賦塔羅\n", "process")
        self.tarot_text.insert(tk.END, f"{life_tarot_card} → {soul_tarot_card} → {talent_tarot_card}\n", "process")
        self.tarot_text.insert(tk.END, "代表：顯示您的生命發展軌跡和方向\n\n", "meaning")
        
        # 內在成長配牌
        self.tarot_text.insert(tk.END, "◆ 內在成長配牌\n", "subtitle")
        self.tarot_text.insert(tk.END, "先天塔羅 → 後天塔羅 → 人格塔羅\n", "process")
        self.tarot_text.insert(tk.END, f"{innate_tarot_card} → {acquired_tarot_card} → {personality_tarot_card}\n", "process")
        self.tarot_text.insert(tk.END, "代表：展現您的個人成長和轉變過程\n\n", "meaning")
        
        # 陰影整合配牌
        self.tarot_text.insert(tk.END, "◆ 陰影整合配牌\n", "subtitle")
        self.tarot_text.insert(tk.END, "人格塔羅 → 陰影塔羅 → 靈魂塔羅\n", "process")
        self.tarot_text.insert(tk.END, f"{personality_tarot_card} → {shadow_tarot_card} → {soul_tarot_card}\n", "process")
        self.tarot_text.insert(tk.END, "代表：顯示您需要整合的陰影面向和靈性成長\n\n", "meaning")
        
        # 配牌解讀說明
        self.tarot_text.insert(tk.END, "\n【配牌解讀說明】\n", "title")
        self.tarot_text.insert(tk.END, "1. 牌與牌之間的關係顯示了能量的流動方向\n", "process")
        self.tarot_text.insert(tk.END, "2. 相鄰牌號的差異表示了轉變的難易程度\n", "process")
        self.tarot_text.insert(tk.END, "3. 重複出現的牌號代表了特別需要關注的面向\n", "process")
        self.tarot_text.insert(tk.END, "4. 大阿爾卡納牌號的總和反映了整體能量強度\n", "process")
        
        # 特殊牌號組合解釋
        if life_tarot_number == soul_tarot_number:
            self.tarot_text.insert(tk.END, "\n★ 生命塔羅與靈魂塔羅相同：表示生命目標與靈魂使命高度一致\n", "result")
        if talent_tarot_number == innate_tarot_number:
            self.tarot_text.insert(tk.END, "★ 天賦塔羅與先天塔羅相同：表示天賦能力已充分展現\n", "result")
        if acquired_tarot_number == personality_tarot_number:
            self.tarot_text.insert(tk.END, "★ 後天塔羅與人格塔羅相同：表示個性特質已充分發展\n", "result")
    
        # 在計算方法中添加九宮格的計算和顯示
        grid = calculate_life_grid(birthdate)
        strengths, weaknesses, connections = analyze_life_grid(grid)
        
        # 繪製九宮格
        self.draw_grid(grid)
        
        # 顯示九宮格分析
        self.grid_text.delete(1.0, tk.END)
        self.grid_text.insert(tk.END, "【生命靈數九宮格分析】\n\n", "title")
        
        # 顯示強項分析
        self.grid_text.insert(tk.END, "◆ 強項分析\n", "subtitle")
        if strengths:
            for strength in strengths:
                self.grid_text.insert(tk.END, f"• {strength}\n", "result")
        else:
            self.grid_text.insert(tk.END, "數字分布較為平均\n", "process")
        
        # 顯示弱項分析
        self.grid_text.insert(tk.END, "\n◆ 弱項分析\n", "subtitle")
        if weaknesses:
            for weakness in weaknesses:
                self.grid_text.insert(tk.END, f"• {weakness}\n", "process")
        else:
            self.grid_text.insert(tk.END, "無明顯弱項\n", "process")
        
        # 顯示數字連線分析
        self.grid_text.insert(tk.END, "\n◆ 數字連線分析\n", "subtitle")
        if connections:
            for connection in connections:
                self.grid_text.insert(tk.END, f"• {connection}\n", "meaning")
        else:
            self.grid_text.insert(tk.END, "無特殊數字連線\n", "process")
        
        # 九宮格解讀說明
        self.grid_text.insert(tk.END, "\n【九宮格解讀說明】\n", "title")
        self.grid_text.insert(tk.END, "1. 數字重複出現代表該領域能量強\n", "process")
        self.grid_text.insert(tk.END, "2. 空缺的宮位需要多加發展\n", "process")
        self.grid_text.insert(tk.END, "3. 連線表示能量的流動方向\n", "process")
        self.grid_text.insert(tk.END, "4. 對角線連線具有特殊意義\n", "process")

def main():
    root = tk.Tk()
    app = LifeNumberCalculatorGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main() 