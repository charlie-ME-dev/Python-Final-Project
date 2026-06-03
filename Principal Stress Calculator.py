import numpy as np
import matplotlib.pyplot as plt


def plot_3d_mohr_circle(stress_tensor):

    principal_stresses = np.linalg.eigvalsh(stress_tensor)

    ''' 
    np.linalg.eigvalsh 는 고윳값을 계산하는 numpt의 함수이다.
    주응력은 응력텐서의 고윳값이므로 이 함수 모듈을 사용하는 것으로 주응력을 계산할 수 있다.

    주응력(principal_stresses)를 계산하는 이유는 maximum normal stress(최대 수직응력)을 계산하기 위함이다.
    응력은 좌표계마다 그 값이 달라지므로, 최대값을 구하고 이 값이 파단응력[UTS]을 넘어서면 재료의 파손(failure)가 발생한다.
    따라서 주응력을 계산하여 그 값이 재료의 파단응력[UTS]과 비교하기 위해 주응력을 계산한다.

    때때로 von-mises stress를 주응력 대신 사용하지만, 여기서는 주응력만을 본다.
    ''' 


    principal_stresses = np.sort(principal_stresses)[::-1]
    sigma1, sigma2, sigma3 = principal_stresses
    von_mises = np.sqrt(0.5*(sigma1 - sigma2)**2+0.5*(sigma2 - sigma3)**2+0.5*(sigma3 - sigma1)**2)

    '''
    일반적으로 주응력은 내림차순으로 표현한다. 따라서 np.sort에 [::-1]을 통해서
    내림차순으로 정렬한다. [descending order) sigma1 >= sigma2 >= sigma3 ]
    추가로 Ductile[연성]재료의 경우, 최대주응력보다 본미세스응력을 종종 평가기준으로 한다.
    '''

    # 터미널에 주응력 값을 출력한다.

    print('-'*30)
    print('--- 주응력 ---')
    print(f'\u03c3 [최대값] : {sigma1:.4f}')
    print(f'\u03c3 [중간값] : {sigma2:.4f}')
    print(f'\u03c3 [최소값] : {sigma3:.4f}')
    print(f'\n본미세스 응력 : {von_mises:.4f}')

    C1 = (sigma1 + sigma3)/2
    R1= (sigma1 - sigma3)/2
    
    C2 = (sigma1 + sigma2)/2
    R2= (sigma1 - sigma2)/2

    C3 = (sigma2 + sigma3)/2
    R3= (sigma2 - sigma3)/2

    tau_max = R1
    print(f'\n최대 전단응력 : {tau_max:.4f}')
    print('-'*30)

    # 모어원 그리기
    fig,ax = plt.subplots(figsize=(10,10))


    theta = np.linspace(0,2*np.pi,200)

    def draw_circle(ax, center, radius, color, label):
        x = center + radius*np.cos(theta)
        y = radius*np.sin(theta)
        ax.plot(x,y,color=color,label=label,linewidth=2)
        ax.plot(center, 0, marker='+',color=color, markersize =8) # 중심표기
    
    draw_circle(ax,C1,R1,'blue','Circle1 (\u03c31 - \u03c33)')
    draw_circle(ax,C2,R2,'green','Circle1 (\u03c31 - \u03c33)')
    draw_circle(ax,C3,R3,'red','Circle1 (\u03c31 - \u03c33)')

    ax.axhline(0,color='black',linewidth=1)
    ax.axvline(0,color='black',linewidth=1)
    ax.set_aspect('equal','box')
    ax.set_xlabel('수직응력(\u03c3)')
    ax.set_ylabel('전단응력(\u03c4)')
    ax.set_title('모어원')

    ax.plot([sigma1, sigma2, sigma3],[0,0,0],'ko',label='주응력')

    ax.grid(True, linestyle ='--',alpha=0.7)
    ax.legend(loc='upper right')
    
    plt.tight_layout()
    plt.show()

if __name__ == '__main__':
    print("="*40)
    print('3차원 모어원 그리기')
    print("="*40)
    print('3차원 응력텐서를 입력하세요.')
    try:
        sigma_xx = float(input('sigma_xx : '))
        sigma_yy = float(input('sigma_yy : '))
        sigma_zz = float(input('sigma_zz : '))
        tau_xy = float(input('tau_xy : '))
        tau_xz = float(input('tau_xz : '))
        tau_yz = float(input('tau_yz : '))

        stress_matrix = np.array([
            [sigma_xx, tau_xy, tau_xz],
            [tau_xy, sigma_yy, tau_yz],
            [tau_xz, tau_yz, sigma_zz]
        ])
        print('\n 입력된 응력텐서')
        print(stress_matrix)
        print('\n 계산 및 가시화')

        plot_3d_mohr_circle(stress_matrix)

    except ValueError:
        print('\n Error: Please enter valid numerical values.')
    except ImportError:
        print('\n Error: Required libraries not found. Please run:')
        print('pip install numpy matplotlib')