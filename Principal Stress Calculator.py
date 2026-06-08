import numpy as np
import matplotlib.pyplot as plt

plt.rcParams['font.family'] = 'Malgun Gothic'
# 그래프의 폰트를 윈도우 OS의 기본 한글 폰트인 맑은 고딕으로 변경하는 코드.
# marplotlib이 기본적으로 사용하는 DejaVu Sans는 영문 전용이라 한글문자를 인식하지 못함.
plt.rcParams['axes.unicode_minus'] = False
# 그래프에 축에 음수값이 표시될 때, 기본 유니코드 마이너스 기호 대신 
# 일반적인 키보드의 하이픈-마이너스를 사용하도록 설정


material_db = {
    "PLA": {"type": "brittle", "Tensile_Strength": 63.63},
    "ABS": {"type": "ductile", "Tensile_Strength": 43.1},
}



def stress_calculator(stress_tensor):
    principal_stresses = np.linalg.eigvalsh(stress_tensor)
    ''' 
    np.linalg.eigvalsh 는 고윳값을 계산하는 numpy의 함수이다.
    주응력은 응력텐서의 고윳값이므로 이 함수 모듈을 사용하는 것으로 주응력을 계산할 수 있다.

    주응력(principal_stresses)를 계산하는 이유는 maximum normal stress(최대 수직응력)을 계산하기 위함이다.
    응력은 좌표계마다 그 값이 달라지므로, 최대값을 구하고 이 값이 파단응력[UTS]을 넘어서면 재료의 파손(failure)가 발생한다.
    따라서 주응력을 계산하여 그 값이 재료의 파단응력[UTS]과 비교하기 위해 주응력을 계산한다.
    ''' 

    principal_stresses = np.sort(principal_stresses)[::-1]

    '''
    np.linalg.eigvalsh => 이 함수의 출력은 NumPy 배열(ndarray)라는 형태이다.
    만약 내장함수 sorted()를 사용하게 되면, 일반 파이썬 리스트로 변경된다.
    하지만, np.sort를 사용할 때에는 결과물을 계속 ndarray로 유지할 수 있다.
    추가로 파이썬 내장 함수보다 C언어 기반으로 최적화된 np.sort가 속도가 더 빠르다.
        
    일반적으로 주응력은 내림차순으로 표현한다. 따라서 np.sort에 [::-1]을 통해서
    내림차순으로 정렬한다. [descending order) sigma1 >= sigma2 >= sigma3 ]
    추가로 Ductile[연성]재료의 경우, 최대주응력보다 본미세스응력을 종종 평가기준으로 한다.
    '''

    sigma1, sigma2, sigma3 = principal_stresses # sigma1이 최대 주응력이다.
    von_mises = np.sqrt(0.5*(sigma1 - sigma2)**2+0.5*(sigma2 - sigma3)**2+0.5*(sigma3 - sigma1)**2) # 본미세스응력을 계산하는 공식이다.
    

    print('-'*30)
    print('--- 주응력 ---')
    print(f'\u03c3 [최대값] : {sigma1:.4f}')
    print(f'\u03c3 [중간값] : {sigma2:.4f}')
    print(f'\u03c3 [최소값] : {sigma3:.4f}')
    print(f'\n본미세스 응력 : {von_mises:.4f}')

    return sigma1, sigma2, sigma3, von_mises


def plot_3d_mohr_circle(sigma1, sigma2, sigma3):

    # 모어원의 중심점은 주응력의 평균으로 구할 수 있다.
    # 모어원의 반지름은 주응력 차를 절반으로 나누어 구할 수 있다.

    C1 = (sigma1 + sigma3)/2
    R1= (sigma1 - sigma3)/2
    
    C2 = (sigma1 + sigma2)/2
    R2= (sigma1 - sigma2)/2

    C3 = (sigma2 + sigma3)/2
    R3= (sigma2 - sigma3)/2

    tau_max = R1 # 최대 전단응력은 모어원에서 가장 큰 원의 반지름과 같다.

    print(f'\n최대 전단응력 : {tau_max:.4f}')
    print('-'*30)

    # 모어원 그리기

    _,ax = plt.subplots(figsize=(7,7))
    # plt.plt() 대신 ax.plot을 사용하는 이유 = OOP
    # 지금 이 명령을 통해서 Figure 객체와 axes 객체가 형성된다.
    # plt.subplots() 함수는 파이썬 내부적으로 무조건 튜플 형태의 데이터 2개 세트로 반환하도록 되어있다.
    # 따라서 Figure 객체와 axes 객체가 나오는데, 앞부분의 figure 객체는 우리가 사용하지 않으므로 변수를 생성하지 않는다.
    # Figure 객체를 이용하면 plot을 pdf나 png 형태로 저장할 수 있는 기능을 추가할 수 있다.

    theta = np.linspace(0,2*np.pi,200)

    def draw_circle(ax, center, radius, color, label):
        x = center + radius*np.cos(theta)
        y = radius*np.sin(theta)
        ax.plot(x,y,color=color,label=label,linewidth=2)
        ax.plot(center, 0, marker='+',color=color, markersize =8) # 중심표기
    

    draw_circle(ax,C1,R1,'blue','Circle 1 (\u03c31 - \u03c33)')
    draw_circle(ax,C2,R2,'green','Circle 2 (\u03c31 - \u03c33)')
    draw_circle(ax,C3,R3,'red','Circle 3 (\u03c31 - \u03c33)')


    ax.plot(sigma1,0,'ko',label='\u03c31') # ko는 검은색 원
    ax.plot(sigma2,0,'k^',label='\u03c32') # k^는 검은색 삼각형
    ax.plot(sigma3,0,'ks',label='\u03c33') # ks는 검은색 사각형  ==> 주응력들을 그래프에 표시해준다.

    ax.axhline(0,color='black',linewidth=1)
    ax.axvline(0,color='black',linewidth=1)
    # x축과 y축을 그려주는 함수 horizontal & vertical
    
    ax.set_aspect('equal','box')
    # 'equal' 설정을 통해 그래프의 x&y축이 같은 비율로 plot되게 한다.
    # 'box' 설정을 통해 그래프 테두리 박스 전체의 비율을 1:1로 고정한다. -> 가시성 향상

    ax.set_xlabel('수직응력(\u03c3)')
    ax.set_ylabel('전단응력(\u03c4)')
    ax.set_title('모어원') # x축과 y축에 label(이름)을 붙이고, 제목도 붙여준다.
    ax.margins(0.3) # 그래프 plot에 margin[여유]를 줘서 가시성을 높여준다.


    ax.grid(True, linestyle ='--',alpha=0.7)
    # 그래프에 grid (격자무늬)를 형성하여 읽기 쉽게 한다.
    # 알파값은 투명도를 의미. 0 = 완전투명, 1 = 완전 불투명, 0.7 = 70% 불투명
    ax.legend(loc='upper right')
    
    plt.tight_layout()
    # 이 기능은 그래프의 축라벨, 타이틀, 눈금 등이 잘리거나 겹치지 않도록 
    # 그래프 내부 요소들의 여백을 자동으로 최적화해주는 함수이다.

    plt.show()
    # 지금까지 메모리상에만 그려두었던 모든 그래프 그림들을 실제 모니터 화면에 팝업 창으로 띄워서 보여주는 함수이다.

def evaluate_failure(sigma1, von_mises, material_choice, safety_factor):

    if material_choice not in material_db:
        print('지원하지 않는 재료입니다.')
        return
    
    mat_info = material_db[material_choice] # 재료DB 딕셔너리에서 해당되는 재료를 꺼낸다.
    mat_type = mat_info["type"] # 꺼내진 재료의 종류를 다시 꺼낸다. -> criterion 설정을 위해서.
    UTS = mat_info["Tensile_Strength"]

    print('\n','-'*30)
    print(f'--- 파손 평가 (재료 : {material_choice}), 안전계수 : {safety_factor} ---')
    print(f'최대 주응력 (σ1): {sigma1:.2f} MPa')
    print(f'본 미세스 응력 (σ_VM): {von_mises:.2f} MPa')
    print('-'*30)

    is_safe = False

    if mat_type == "brittle":
        allowable_stress = UTS / safety_factor
        print('\n취성재료에 대해 최대 주응력 이론으로 파손을 예측합니다.')
        print(f'허용응력 (인장강도/안전계수) : {allowable_stress:.2f} MPa')

        if sigma1 <= allowable_stress:
            is_safe = True

    elif mat_type == "ductile":
        allowable_stress = UTS / safety_factor
        print('\n연성재료에 대해 본 미세스 이론으로 파손을 예측합니다.')
        print(f'허용 응력 (인장강도/ 안전계수): {allowable_stress:.2f} MPa')

        if von_mises <= allowable_stress:
            is_safe = True

    print('\n 파손 평가 결과')
    if is_safe:
        print('✅ SAFE: 현재 응력상태에서 출력물이 안전합니다.')
    else:
        print('❌ Failure: 현재 응력상태에서 출력물이 위험합니다.')
    print('-'*30)


# 파이썬 파일을 실행하면, 파이썬 내부적으로 __name__ 변수 안에 __main__이라는 값을 넣어준다.
# 파이썬 파일이 import를 통해서 불려오면 __name__ 변수 안에 main이라는 값을 넣는다.
# 따라서 지금 이 파일썬 파일이 모듈로서 불러와졌을 때, [주응력 계산함수나 모어원 그리기 함수를 사용하기 위해]
# 응력을 입력받는 과정이 실행되지 않기 위해서 if __name__ == '__main__':를 넣어준다.

if __name__ == '__main__':  
    
    print("="*40)
    print('3차원 모어원 및 파손 평가 프로그램')
    print("="*40)
    try:
        print('3차원 응력텐서를 입력하세요.')
        sigma_xx = float(input('sigma_xx [단위: MPa] : '))
        sigma_yy = float(input('sigma_yy [단위: MPa] : '))
        sigma_zz = float(input('sigma_zz [단위: MPa] : '))
        tau_xy = float(input('tau_xy [단위: MPa] : '))
        tau_xz = float(input('tau_xz [단위: MPa] : '))
        tau_yz = float(input('tau_yz [단위: MPa] : '))
        # 이미 배웠듯이, input으로 받은 자료는 string 형태이므로 연산을 위해 실수로 변환해야한다.

        
        stress_matrix = np.array([
            [sigma_xx, tau_xy, tau_xz],
            [tau_xy, sigma_yy, tau_yz],
            [tau_xz, tau_yz, sigma_zz]
        ])

        print('\n 입력된 응력텐서')
        print(stress_matrix)


        sigma1, sigma2, sigma3, von_mises = stress_calculator(stress_matrix)

        print('\n 사용할 필라멘트를 선택하세요')
        print('사용 가능한 재료: PLA, ABS')
        material_choice = input('사용할 재료를 입력하세요 (PLA 혹은 ABS): ').upper()
        
        safety_factor = float(input('안전계수를 입력하세요 (예: 2.0): '))

        evaluate_failure(sigma1, von_mises, material_choice, safety_factor)

        print('\n 모어원 그리기')

        plot_3d_mohr_circle(sigma1, sigma2, sigma3)

    except ValueError:
        print('\n Error: 올바른 숫자(또는 문자)를 입력해주세요.')
    except ImportError:
        print('\n Error: Required libraries not found. Please run:')
        print('pip install numpy matplotlib')