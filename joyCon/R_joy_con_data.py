import hid
import time
import sys
import requests

VENDOR_ID = 0x057E
L_PRODUCT_ID = 0x2006
R_PRODUCT_ID = 0x2007

L_ACCEL_OFFSET_X = 350
L_ACCEL_OFFSET_Y = 0
L_ACCEL_OFFSET_Z = 4081
R_ACCEL_OFFSET_X = 350
R_ACCEL_OFFSET_Y = 0
R_ACCEL_OFFSET_Z = -4081

SCORE_BORDER_1 = 300000
SCORE_BORDER_2 = 500000
SCORE_BORDER_3 = 800000

fileName = './R_data.txt'

MY_PRODUCT_ID = R_PRODUCT_ID

def write_output_report(joycon_device, packet_number, command, subcommand, argument):
    joycon_device.write(command
                        + packet_number.to_bytes(1, byteorder='big')
                        + b'\x00\x01\x40\x40\x00\x01\x40\x40'
                        + subcommand
                        + argument)

def is_left():
    return MY_PRODUCT_ID == L_PRODUCT_ID

def to_int16le_from_2bytes(hbytebe, lbytebe):
    uint16le = (lbytebe << 8) | hbytebe 
    int16le = uint16le if uint16le < 32768 else uint16le - 65536
    return int16le

def get_nbit_from_input_report(input_report, offset_byte, offset_bit, nbit):
    return (input_report[offset_byte] >> offset_bit) & ((1 << nbit) - 1)

def get_button_down(input_report):
    return get_nbit_from_input_report(input_report, 5, 0, 1)

def get_button_up(input_report):
    return get_nbit_from_input_report(input_report, 5, 1, 1)

def get_button_right(input_report):
    return get_nbit_from_input_report(input_report, 5, 2, 1)

def get_button_left(input_report):
    return get_nbit_from_input_report(input_report, 5, 3, 1)

def get_stick_left_horizontal(input_report):
    return get_nbit_from_input_report(input_report, 6, 0, 8) | (get_nbit_from_input_report(input_report, 7, 0, 4) << 8)

def get_stick_left_vertical(input_report):
    return get_nbit_from_input_report(input_report, 7, 4, 4) | (get_nbit_from_input_report(input_report, 8, 0, 8) << 4)

def get_stick_right_horizontal(input_report):
    return get_nbit_from_input_report(input_report, 9, 0, 8) | (get_nbit_from_input_report(input_report, 10, 0, 4) << 8)

def get_stick_right_vertical(input_report):
    return get_nbit_from_input_report(input_report, 10, 4, 4) | (get_nbit_from_input_report(input_report, 11, 0, 8) << 4)

def get_accel_x(input_report, sample_idx=0):
    if sample_idx not in [0, 1, 2]:
        raise IndexError('sample_idx should be between 0 and 2')
    return (to_int16le_from_2bytes(get_nbit_from_input_report(input_report, 13 + sample_idx * 12, 0, 8),
                                   get_nbit_from_input_report(input_report, 14 + sample_idx * 12, 0, 8))
            - (L_ACCEL_OFFSET_X if is_left() else R_ACCEL_OFFSET_X))

def get_accel_y(input_report, sample_idx=0):
    if sample_idx not in [0, 1, 2]:
        raise IndexError('sample_idx should be between 0 and 2')
    return (to_int16le_from_2bytes(get_nbit_from_input_report(input_report, 15 + sample_idx * 12, 0, 8),
                                   get_nbit_from_input_report(input_report, 16 + sample_idx * 12, 0, 8))
            - (L_ACCEL_OFFSET_Y if is_left() else R_ACCEL_OFFSET_Y))

def get_accel_z(input_report, sample_idx=0):
    if sample_idx not in [0, 1, 2]:
        raise IndexError('sample_idx should be between 0 and 2')
    return (to_int16le_from_2bytes(get_nbit_from_input_report(input_report, 17 + sample_idx * 12, 0, 8),
                                   get_nbit_from_input_report(input_report, 18 + sample_idx * 12, 0, 8))
            - (L_ACCEL_OFFSET_Z if is_left() else R_ACCEL_OFFSET_Z))

def get_gyro_x(input_report, sample_idx=0):
    if sample_idx not in [0, 1, 2]:
        raise IndexError('sample_idx should be between 0 and 2')
    return to_int16le_from_2bytes(get_nbit_from_input_report(input_report, 19 + sample_idx * 12, 0, 8),
                                  get_nbit_from_input_report(input_report, 20 + sample_idx * 12, 0, 8))

def get_gyro_y(input_report, sample_idx=0):
    if sample_idx not in [0, 1, 2]:
        raise IndexError('sample_idx should be between 0 and 2')
    return to_int16le_from_2bytes(get_nbit_from_input_report(input_report, 21 + sample_idx * 12, 0, 8),
                                  get_nbit_from_input_report(input_report, 22 + sample_idx * 12, 0, 8))

def get_gyro_z(input_report, sample_idx=0):
    if sample_idx not in [0, 1, 2]:
        raise IndexError('sample_idx should be between 0 and 2')
    return to_int16le_from_2bytes(get_nbit_from_input_report(input_report, 23 + sample_idx * 12, 0, 8),
                                  get_nbit_from_input_report(input_report, 24 + sample_idx * 12, 0, 8))

def joycon_connect(joycon_device):
    joycon_device.open(VENDOR_ID, MY_PRODUCT_ID)
    # 6軸センサーを有効化
    write_output_report(joycon_device, 0, b'\x01', b'\x40', b'\x01')
    # 設定を反映するためには時間間隔が必要
    time.sleep(0.02)
    # 60HzでJoy-Conの各データを取得するための設定
    write_output_report(joycon_device, 1, b'\x01', b'\x03', b'\x30')

def integrate_accel(joycon_device):
    base_time = time.time()
    accel = [0, 0, 0]
    while abs(time.time() - base_time) < 1.0:
        input_report = joycon_device.read(49)
        accel_x = get_accel_x(input_report)
        accel_y = get_accel_y(input_report)
        accel_z = get_accel_z(input_report)
        accel[0] += abs(accel_x)
        accel[1] += abs(accel_y)
        accel[2] += abs(accel_y)
    return accel

def calculate_score(accel_array):
    score = 0
    for accel in accel_array :
        if SCORE_BORDER_1 > accel :
            score += 0
        elif SCORE_BORDER_1 < accel < SCORE_BORDER_2 :
            score += 1
        elif SCORE_BORDER_2 < accel < SCORE_BORDER_3 :
            score += 2
        else :
            score += 3
    return score + 1

if __name__ == '__main__':
    joycon_device = hid.device()
    joycon_connect(joycon_device)
    print ('joy-con R')
    player_id = '0' if is_left() else '1'
    try:
        while True:
            accel_array = integrate_accel(joycon_device)
            print(accel_array)
            score = calculate_score(accel_array)
            print(score)
            requests.get('https://script.google.com/macros/s/AKfycbxX4kPc4r8L2wTcyQtUZJrwa_saA6kzwQ9vf9E3XxRW_e7PxOpB/exec?player='+player_id+'&text='+str(score))
    except KeyboardInterrupt:
        joycon_device.close()
        sys.exit()