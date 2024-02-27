import pygame
import time
import cv2
import numpy as np
import matplotlib.pyplot as plt


def get_axes(joystick):
    ax0 = int(round(joystick.get_axis(0)*100))
    ax1 = int(round(-joystick.get_axis(1)*100))
    ax2 = int(round(joystick.get_axis(2)*100))
    ax3 = int(round(joystick.get_axis(3)*100))
    return ax0, ax1, ax2, ax3

def get_motor_outputs(x, y, r, a, b):
    m1 = -a*x + a*y - b*r
    m2 = -a*x - a*y - b*r
    m3 =  a*x - a*y - b*r
    m4 =  a*x + a*y - b*r
    return m1, m2, m3, m4

def motor_output_limit(m, limit):
    if m > abs(limit):
        m = limit
    elif m < -abs(limit):
        m = -limit
    return int(m)

img_blank = 255*np.ones((800, 600, 3), dtype="uint8")


# Unit Vectors
u1 = np.array((-1, -1))
u2 = np.array((-1,  1))
u3 = np.array(( 1,  1))
u4 = np.array(( 1, -1))

# reference points
pt_m1_0 = np.array((400, 100))
pt_m2_0 = np.array((200, 100))
pt_m3_0 = np.array((200, 300))
pt_m4_0 = np.array((400, 300))
pt_robo_0 = np.array((300, 200))

def main():
    # Initialize Pygame
    pygame.init()

    # Check for available joysticks
    joystick_count = pygame.joystick.get_count()
    print(f"Number of joysticks found: {joystick_count}")

    joystick = pygame.joystick.Joystick(0)
    joystick.init()

    print(f"Joystick Name: {joystick.get_name()}")
    print(f"Number of Axes: {joystick.get_numaxes()}")
    print(f"Number of Buttons: {joystick.get_numbuttons()}")

    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 0.8
    font_color = (255, 0, 0)  # BGR color (white in this case)
    font_thickness = 2

    color = (255, 0, 0)  # BGR color (green in this case)
    thickness = 2

    a = 0.5
    b = 0.5
    motor_limit = 50
    robo_gain = 0.5

    print("Press ESC to stop")

    while True:
        img = img_blank.copy()
        
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()


        # スティックの値読み取り
        ax0, ax1, ax2, ax3 = get_axes(joystick)
    
        x = ax0
        y = ax1
        r = ax2
        
        # 各モーターの出力計算
        m1, m2, m3, m4 = get_motor_outputs(x, y, r, a, b)
        
        m1 = motor_output_limit(m1, motor_limit)
        m2 = motor_output_limit(m2, motor_limit)
        m3 = motor_output_limit(m3, motor_limit)
        m4 = motor_output_limit(m4, motor_limit)
        
        pt_m1 = (m1*u1 + pt_m1_0).astype("int")
        pt_m2 = (m2*u2 + pt_m2_0).astype("int")
        pt_m3 = (m3*u3 + pt_m3_0).astype("int")
        pt_m4 = (m4*u4 + pt_m4_0).astype("int")
        
        robo_vector = (m1*u1 + m2*u2 + m3*u3 + m4*u4)
        pt_robo = pt_robo_0 + (robo_gain*robo_vector).astype("int") 
        
        # 各モーターの出力を描画
        cv2.line(img, pt_m1_0, pt_m1, color, thickness)
        cv2.line(img, pt_m2_0, pt_m2, color, thickness)
        cv2.line(img, pt_m3_0, pt_m3, color, thickness)
        cv2.line(img, pt_m4_0, pt_m4, color, thickness)
        
        cv2.circle(img, pt_m1, 10, color, -1)
        cv2.circle(img, pt_m2, 10, color, -1)
        cv2.circle(img, pt_m3, 10, color, -1)
        cv2.circle(img, pt_m4, 10, color, -1)

        cv2.putText(img, f"{m1}", pt_m1_0+np.array((-10, 40)), font, font_scale, font_color, font_thickness)
        cv2.putText(img, f"{m2}", pt_m2_0+np.array((-10, 40)), font, font_scale, font_color, font_thickness)
        cv2.putText(img, f"{m3}", pt_m3_0+np.array((-10, 40)), font, font_scale, font_color, font_thickness)
        cv2.putText(img, f"{m4}", pt_m4_0+np.array((-10, 40)), font, font_scale, font_color, font_thickness)
        
        # ロボットの移動ベクトルを描画
        cv2.line(img, pt_robo_0, pt_robo, color, thickness)
        if np.linalg.norm(robo_vector) != 0:
            cv2.circle(img, pt_robo, 10, color, -1)
        
        # ロボットの回転を計算
        r_angle = int(180*r/100)
        x_rotation = 50*np.cos(np.deg2rad(r_angle))
        y_rotation = 50*np.sin(np.deg2rad(r_angle))
        pt_robo_r = np.array((x_rotation, y_rotation)).astype("int") + pt_robo_0
        
        # ロボットの回転を描画
        cv2.ellipse(img, (300, 200), (50, 50), 0, 0, r_angle, color, thickness)
        if r_angle != 0:
            cv2.circle(img, pt_robo_r, 10, color, -1)

        # スティックの座標軸を描画
        cv2.line(img, (30, 650), (270, 650), (0,0,0), 1)
        cv2.line(img, (150, 530), (150, 770), (0,0,0), 1)
        cv2.line(img, (330, 650), (570, 650), (0,0,0), 1)
        cv2.line(img, (450, 530), (450, 770), (0,0,0), 1)    

        # スティックの読み取り値を描画
        pt_left_0 = np.array([150, 650])
        pt_left = pt_left_0 + np.array([x, -y])
        
        pt_right_0 = np.array([450, 650])
        pt_right = pt_right_0 + np.array([r, 0])
        

        cv2.line(img, pt_left_0, pt_left, color, thickness)
        cv2.circle(img, pt_left, 10, color, -1)
        
        cv2.line(img, pt_right_0, pt_right, color, thickness)
        cv2.circle(img, pt_right, 10, color, -1)

        cv2.putText(img, f"Omni Wheels", (20, 30), font, font_scale, font_color, font_thickness)  
        cv2.putText(img, f"Controller", (20, 520), font, font_scale, font_color, font_thickness)   
        cv2.putText(img, f"X {x}", (20, 790), font, font_scale, font_color, font_thickness)    
        cv2.putText(img, f"Y {y}", (170, 790), font, font_scale, font_color, font_thickness)
        cv2.putText(img, f"R {r}", (400, 790), font, font_scale, font_color, font_thickness)
        
        cv2.imshow("Omni Wheel Sim", img)
        
        # Break the loop if 'q' key is pressed
        if cv2.waitKey(10) & 0xFF == 27:
            pygame.quit()
            break
        
        
        
        #time.sleep(0.01)
    cv2.destroyAllWindows()
    pygame.quit()
    

if __name__ == '__main__':
    main()
