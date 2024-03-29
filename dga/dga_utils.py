import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import math

def percent_gas(num1, num2, num3):
    gas = [num1, num2, num3]
    count = 0
    total = sum(gas)

    for element in gas:
        pct = (element / total) * 100
        gas[count] = pct
        count = count + 1

    return gas


def dt1(ethylene, methane, acetylene):
    gas = percent_gas(ethylene, methane, acetylene)
    x = gas[0]
    y = gas[1]
    z = gas[2]

    #
    # Define the transformation matrix
    #
    A = np.array([[5, 2.5, 50], [0, 5 * np.sqrt(3) / 2, 50], [0, 0, 1]])

    #
    # Define a set of points for Duval triangle regions
    #
    p = np.array([
        [0, 0, 1],  # 0-p1
        [0, 100, 1],  # 1-p2
        [100, 0, 1],  # 2-p3
        [0, 87, 1],  # 3-p4
        [0, 96, 1],  # 4-p5
        [0, 98, 1],  # 5-p6
        [2, 98, 1],  # 6-p7
        [23, 0, 1],  # 7-p8
        [23, 64, 1],  # 8-p9
        [20, 76, 1],  # 9-p10
        [20, 80, 1],  # 10-p11
        [40, 31, 1],  # 11-p12
        [40, 47, 1],  # 12-p13
        [50, 35, 1],  # 13-p14
        [50, 46, 1],  # 14-p15
        [50, 50, 1],  # 15-p16
        [71, 0, 1],  # 16-p17
        [85, 0, 1]])  # 17-p18

    #
    # Apply the coordinates transformation to all points
    #
    v = p @ np.transpose(A)

    #
    # Set one more sample point
    #
    sample_point = np.array([x, y, 1]) @ np.transpose(A)

    #
    # Define each of the regions by the coordinates of its angle points
    #
    region_PD = v[[5, 1, 6], :]
    region_T1 = v[[4, 5, 6, 10, 9], :]
    region_T2 = v[[9, 10, 15, 14], :]
    region_T3 = v[[13, 15, 2, 17], :]
    region_D1 = v[[0, 3, 8, 7], :]
    region_D2 = v[[7, 8, 12, 11, 16], :]
    region_DT = v[[3, 4, 14, 13, 17, 16, 11, 12], :]

    #
    # Plot the results
    #
    fig, ax1 = plt.subplots()
    ax1.fill(region_PD[:, 0], region_PD[:, 1], '#c92a2a')
    ax1.fill(region_T1[:, 0], region_T1[:, 1], '#ffff80')
    ax1.fill(region_T2[:, 0], region_T2[:, 1], '#e89f9b')
    ax1.fill(region_T3[:, 0], region_T3[:, 1], '#e7c490')
    ax1.fill(region_D1[:, 0], region_D1[:, 1], '#eca9fc')
    ax1.fill(region_D2[:, 0], region_D2[:, 1], '#B8F198')
    ax1.fill(region_DT[:, 0], region_DT[:, 1], '#B45F57')
    ax1.scatter(sample_point[0], sample_point[1], marker='x', c='r', zorder=2) # type: ignore
    ax1.grid(linestyle='--', alpha=0.4, axis='both')

    #
    # Also place axes captions
    #
    label1 = np.array([45, -5, 1]) @ np.transpose(A)
    ax1.text(label1[0], label1[1], '%C2H2')
    label2 = np.array([95, -5, 1]) @ np.transpose(A)
    ax1.text(label2[0], label2[1], '0')
    label3 = np.array([5, -5, 1]) @ np.transpose(A)
    ax1.text(label3[0], label3[1], '100')
    label4 = np.array([-10, 55, 1]) @ np.transpose(A)
    ax1.text(label4[0], label4[1], '%CH4')
    label5 = np.array([-3, 5, 1]) @ np.transpose(A)
    ax1.text(label5[0], label5[1], '0')
    label6 = np.array([-7, 95, 1]) @ np.transpose(A)
    ax1.text(label6[0], label6[1], '100')
    label7 = np.array([45, 55, 1]) @ np.transpose(A)
    ax1.text(label7[0], label7[1], '%C2H4')
    label8 = np.array([5, 95, 1]) @ np.transpose(A)
    ax1.text(label8[0], label8[1], '0')
    label9 = np.array([95, 5, 1]) @ np.transpose(A)
    ax1.text(label9[0], label9[1], '100')
    label10 = np.array([-2, 100, 1]) @ np.transpose(A)
    ax1.text(label10[0], label10[1], 'PD', color='#232663')
    label11 = np.array([11, 20, 1]) @ np.transpose(A)
    ax1.text(label11[0], label11[1], 'D1', color='#232663')
    label12 = np.array([35, 20, 1]) @ np.transpose(A)
    ax1.text(label12[0], label12[1], 'D2', color='#232663')
    label12 = np.array([55, 20, 1]) @ np.transpose(A)
    ax1.text(label12[0], label12[1], 'DT', color='#232663')
    label12 = np.array([70, 20, 1]) @ np.transpose(A)
    ax1.text(label12[0], label12[1], 'T3', color='#232663')
    label13 = np.array([11, 84, 1]) @ np.transpose(A)
    ax1.text(label13[0], label13[1], 'T1', color='#232663')
    label14 = np.array([35, 60, 1]) @ np.transpose(A)
    ax1.text(label14[0], label14[1], 'T2', color='#232663')
    label15 = np.array([27, 106, 1]) @ np.transpose(A)
    # ax1.text(label15[0], label15[1], 'Fault detected: ', color='#000')
    #
    # Display fault by region
    #
    fault = None
    if x <= 2 and y >= 98:
        # label20 = np.array([33, 94, 1]) @ np.transpose(A)
        # ax1.text(label20[0], label20[1], 'PD', color='#000')
        # label21 = np.array([36, 88, 1]) @ np.transpose(A)
        # ax1.text(label21[0], label21[1], 'Partial discharges', color='#000')
        fault = "PD - Partial discharges"
    elif x <= 20 and 76 <= y <= 98 and z <= 4:
        # label20 = np.array([33, 94, 1]) @ np.transpose(A)
        # ax1.text(label20[0], label20[1], 'T1', color='#000000')
        # label21 = np.array([36, 88, 1]) @ np.transpose(A)
        # ax1.text(label21[0], label21[1], 'Thermal fault', color='#000')
        # label22 = np.array([39, 82, 1]) @ np.transpose(A)
        # ax1.text(label22[0], label22[1], 't < 300°C', color='#000')
        fault = "T1 - Thermal fault, t < 300°C"
    elif 20 <= x <= 50 and 46 <= y <= 80 and z <= 4:
        # label20 = np.array([33, 94, 1]) @ np.transpose(A)
        # ax1.text(label20[0], label20[1], 'T2', color='#000')
        # label21 = np.array([36, 88, 1]) @ np.transpose(A)
        # ax1.text(label21[0], label21[1], 'Thermal fault', color='#000')
        # label22 = np.array([39, 82, 1]) @ np.transpose(A)
        # ax1.text(label22[0], label22[1], '300°C < t < 700°C', color='#000')
        fault = "T2 - Thermal fault, 300°C < t < 700°C"
    elif x >= 50 and y <= 50 and z <= 15:
        # label20 = np.array([33, 94, 1]) @ np.transpose(A)
        # ax1.text(label20[0], label20[1], 'T3', color='#000000')
        # label21 = np.array([36, 88, 1]) @ np.transpose(A)
        # ax1.text(label21[0], label21[1], 'Thermal fault', color='#000000')
        # label22 = np.array([39, 82, 1]) @ np.transpose(A)
        # ax1.text(label22[0], label22[1], 't > 700°C', color='#000000')
        fault = "T3 - Thermal fault, t > 700°C"
    elif x <= 23 and y <= 87 and z >= 13:
        # print('D1 fault detected!')
        # label20 = np.array([33, 94, 1]) @ np.transpose(A)
        # ax1.text(label20[0], label20[1], 'D1', color='#000000')
        # label21 = np.array([36, 88, 1]) @ np.transpose(A)
        # ax1.text(label21[0], label21[1], 'Discharges of low', color='#000000')
        # label22 = np.array([39, 82, 1]) @ np.transpose(A)
        # ax1.text(label22[0], label22[1], 'energy', color='#000000')
        fault = "D1 - Discharges of low energy"
    elif 23 <= x <= 40 and y <= 64 and z >= 13 or x >= 40 and y <= 31 and 29 <= z <= 60:
        # label20 = np.array([33, 94, 1]) @ np.transpose(A)
        # ax1.text(label20[0], label20[1], 'D2', color='#000000')
        # label21 = np.array([36, 88, 1]) @ np.transpose(A)
        # ax1.text(label21[0], label21[1], 'Discharges of high', color='#000000')
        # label22 = np.array([39, 82, 1]) @ np.transpose(A)
        # ax1.text(label22[0], label22[1], 'energy', color='#000000')
        fault = "D2 - Discharges of high energy"
    else:
        # label20 = np.array([33, 94, 1]) @ np.transpose(A)
        # ax1.text(label20[0], label20[1], 'DT', color='#000000')
        # label21 = np.array([36, 88, 1]) @ np.transpose(A)
        # ax1.text(label21[0], label21[1], 'Thermal fault', color='#000000')
        # label22 = np.array([39, 82, 1]) @ np.transpose(A)
        # ax1.text(label22[0], label22[1], 'and discharges', color='#000000')
        fault = "DT - Thermal fault and discharges"
    #
    # Show the final plot
    #
    ax1.set_xlim(0, 625)
    ax1.set_ylim(0, 550)
    ax1.get_xaxis().set_visible(False)
    ax1.get_yaxis().set_visible(False)
    
    plt.savefig('dga/static/images/dt1.png')
    
    return fault


def dt4(methane, hydrogen, ethane):
    gas = percent_gas(methane, hydrogen, ethane)
    x = gas[0]
    y = gas[1]
    z = gas[2]

    #
    # Define the transformation matrix
    #
    A = np.array([[5, 2.5, 50], [0, 5 * np.sqrt(3) / 2, 50], [0, 0, 1]])

    #
    # Define a set of points for Duval triangle regions
    #
    p = np.array([
        [0, 0, 1],  # 0-p1
        [0, 100, 1],  # 1-p2
        [100, 0, 1],  # 2-p3
        [0, 9, 1],  # 3-p4
        [0, 54, 1],  # 4-p5
        [2, 97, 1],  # 5-p6
        [2, 98, 1],  # 6-p7
        [15, 84, 1],  # 7-p8
        [15, 85, 1],  # 8-p9
        [36, 40, 1],  # 9-p10
        [36, 64, 1],  # 10-p11
        [45, 9, 1],  # 11-p12
        [55, 15, 1],  # 12-p13
        [61, 9, 1],  # 13-p14
        [61, 15, 1],  # 14-p15
        [70, 0, 1]])  # 15-p16

    #
    # Apply the coordinates transformation to all points
    #
    v = p @ np.transpose(A)

    #
    # Set one more sample point
    #
    sample_point = np.array([x, y, 1]) @ np.transpose(A)

    #
    # Define each of the regions by the coordinates of its angle points
    #
    region_PD = v[[7, 5, 6, 8], :]
    region_ND = v[[3, 4, 11], :]
    region_O = v[[0, 3, 13, 15], :]
    region_C = v[[9, 10, 2, 15, 12, 14], :]
    region_S = v[[4, 1, 6, 5, 7, 8, 10, 9, 14, 12, 13, 11], :]

    #
    # Plot the results
    #
    fig, ax1 = plt.subplots()
    ax1.fill(region_PD[:, 0], region_PD[:, 1], '#c92a2a')
    ax1.fill(region_ND[:, 0], region_ND[:, 1], '#d6efec')
    ax1.fill(region_O[:, 0], region_O[:, 1], '#ffc4a9')
    ax1.fill(region_C[:, 0], region_C[:, 1], '#f3918d')
    ax1.fill(region_S[:, 0], region_S[:, 1], '#89d2ef')
    ax1.scatter(sample_point[0], sample_point[1], marker='x', c='r', zorder=2) # type: ignore
    ax1.grid(linestyle='--', alpha=0.4, axis='both')

    #
    # Also place axes captions
    #
    label1 = np.array([45, -5, 1]) @ np.transpose(A)
    ax1.text(label1[0], label1[1], '%C2H6')
    label2 = np.array([95, -5, 1]) @ np.transpose(A)
    ax1.text(label2[0], label2[1], '0')
    label3 = np.array([5, -5, 1]) @ np.transpose(A)
    ax1.text(label3[0], label3[1], '100')
    label4 = np.array([-8, 55, 1]) @ np.transpose(A)
    ax1.text(label4[0], label4[1], '%H2')
    label5 = np.array([-3, 5, 1]) @ np.transpose(A)
    ax1.text(label5[0], label5[1], '0')
    label6 = np.array([-7, 95, 1]) @ np.transpose(A)
    ax1.text(label6[0], label6[1], '100')
    label7 = np.array([45, 55, 1]) @ np.transpose(A)
    ax1.text(label7[0], label7[1], '%CH4')
    label8 = np.array([5, 95, 1]) @ np.transpose(A)
    ax1.text(label8[0], label8[1], '0')
    label9 = np.array([95, 5, 1]) @ np.transpose(A)
    ax1.text(label9[0], label9[1], '100')
    label10 = np.array([12, 88, 1]) @ np.transpose(A)
    ax1.text(label10[0], label10[1], 'PD', color='#232663')
    label11 = np.array([20, 58, 1]) @ np.transpose(A)
    ax1.text(label11[0], label11[1], 'S', color='#232663')
    label12 = np.array([32, 3, 1]) @ np.transpose(A)
    ax1.text(label12[0], label12[1], '0', color='#232663')
    label13 = np.array([79, 3, 1]) @ np.transpose(A)
    ax1.text(label13[0], label13[1], 'C', color='#232663')
    label14 = np.array([27, 106, 1]) @ np.transpose(A)
    # ax1.text(label14[0], label14[1], 'Fault detected: ', color='#000')
    #
    # Detect fault by region
    #
    fault = None
    if 2 <= x <= 15 and 84 <= y <= 98 and z <= 1:
        # label20 = np.array([33, 94, 1]) @ np.transpose(A)
        # ax1.text(label20[0], label20[1], 'PD', color='#000')
        # label21 = np.array([36, 88, 1]) @ np.transpose(A)
        # ax1.text(label21[0], label21[1], 'Partial discharges', color='#000')
        fault = "PD - Partial discharges"
    elif x <= 70 and y <= 9 and z >= 30:
        # label20 = np.array([33, 94, 1]) @ np.transpose(A)
        # ax1.text(label20[0], label20[1], 'O', color='#000000')
        # label21 = np.array([36, 88, 1]) @ np.transpose(A)
        # ax1.text(label21[0], label21[1], 'Overheating', color='#000000')
        # label22 = np.array([39, 82, 1]) @ np.transpose(A)
        # ax1.text(label22[0], label22[1], 't < 250°C', color='#000000')
        fault = "O - Overheatingm, t < 250°C"
    elif x <= 45 and 9 <= y <= 54 and z >= 46:
        # label20 = np.array([33, 94, 1]) @ np.transpose(A)
        # ax1.text(label20[0], label20[1], 'ND', color='#000000')
        # label21 = np.array([36, 88, 1]) @ np.transpose(A)
        # ax1.text(label21[0], label21[1], 'Not detected', color='#000000')
        fault = "ND - Not detected"
    elif (x >= 36 and y <= 64 and z <= 24) or (x >= 55 and y <= 15 and 24 <= z <= 30):
        # label20 = np.array([33, 94, 1]) @ np.transpose(A)
        # ax1.text(label20[0], label20[1], 'C', color='#000000')
        # label21 = np.array([36, 88, 1]) @ np.transpose(A)
        # ax1.text(label21[0], label21[1], 'Paper carbonization', color='#000000')
        # label22 = np.array([39, 82, 1]) @ np.transpose(A)
        # ax1.text(label22[0], label22[1], 't > 300°C', color='#000000')
        fault = "C - Paper carbonization, t > 300°C"
    else:
        # label20 = np.array([33, 94, 1]) @ np.transpose(A)
        # ax1.text(label20[0], label20[1], 'S', color='#000000')
        # label21 = np.array([36, 88, 1]) @ np.transpose(A)
        # ax1.text(label21[0], label21[1], 'Stray gassing of', color='#000000')
        # label22 = np.array([39, 82, 1]) @ np.transpose(A)
        # ax1.text(label22[0], label22[1], 'mineral oil', color='#000000')
        fault = "S - Stray gassing of mineral oil"
    #
    # Show the final plot
    #
    ax1.set_xlim(0, 625)
    ax1.set_ylim(0, 550)
    ax1.get_xaxis().set_visible(False)
    ax1.get_yaxis().set_visible(False)

    plt.savefig('dga/static/images/dt4.png')
    
    return fault


def dt5(ethylene, methane, ethane):
    gas = percent_gas(ethylene, methane, ethane)
    x = gas[0]
    y = gas[1]
    z = gas[2]

    #
    # Define the transformation matrix
    #
    A = np.array([[5, 2.5, 50], [0, 5 * np.sqrt(3) / 2, 50], [0, 0, 1]])

    #
    # Define a set of points for Duval triangle regions
    #
    p = np.array([
        [0, 0, 1],  # 0-p1
        [0, 100, 1],  # 1-p2
        [100, 0, 1],  # 2-p3
        [0, 46, 1],  # 3-p4
        [0, 85, 1],  # 4-p5
        [0, 98, 1],  # 5-p6
        [1, 84, 1],  # 6-p7
        [1, 97, 1],  # 7-p8
        [10, 0, 1],  # 8-p9
        [10, 36, 1],  # 9-p10
        [10, 60, 1],  # 10-p11
        [10, 75, 1],  # 11-p12
        [10, 78, 1],  # 12-p13
        [10, 90, 1],  # 13-p14
        [35, 0, 1],  # 14-p15
        [35, 35, 1],  # 15-p16
        [35, 53, 1],  # 16-p17
        [35, 65, 1],  # 17-p18
        [50, 36, 1],  # 18-p19
        [50, 38, 1],  # 19-p20
        [70, 0, 1],  # 20-p21
        [70, 16, 1]])  # 21-p22

    #
    # Apply the coordinates transformation to all points
    #
    v = p @ np.transpose(A)

    #
    # Set one more sample point
    #
    sample_point = np.array([x, y, 1]) @ np.transpose(A)

    #
    # Define each of the regions by the coordinates of its angle points
    #
    region_PD = v[[4, 5, 7, 6], :]
    region_T2 = v[[12, 13, 17, 16], :]
    region_T3 = v[[16, 17, 2, 20, 21, 18, 19], :]
    region_T3_2 = v[[14, 15, 20], :]
    region_ND = v[[8, 10, 15, 14], :]
    region_O = v[[0, 3, 9, 8], :]
    region_O_2 = v[[6, 7, 5, 1, 13, 11], :]
    region_C = v[[10, 12, 19, 18, 21, 20, ], :]
    region_S = v[[3, 4, 11, 9], :]

    #
    # Plot the results
    #
    fig, ax1 = plt.subplots()
    ax1.fill(region_PD[:, 0], region_PD[:, 1], '#c92a2a')
    ax1.fill(region_T2[:, 0], region_T2[:, 1], '#e89f9b')
    ax1.fill(region_T3[:, 0], region_T3[:, 1], '#e7c490')
    ax1.fill(region_T3_2[:, 0], region_T3_2[:, 1], '#e7c490')
    ax1.fill(region_ND[:, 0], region_ND[:, 1], '#d6efec')
    ax1.fill(region_O[:, 0], region_O[:, 1], '#ffc4a9')
    ax1.fill(region_O_2[:, 0], region_O_2[:, 1], '#ffc4a9')
    ax1.fill(region_C[:, 0], region_C[:, 1], '#f3918d')
    ax1.fill(region_S[:, 0], region_S[:, 1], '#89d2ef')
    ax1.scatter(sample_point[0], sample_point[1], marker='x', c='r', zorder=2) # type: ignore
    ax1.grid(linestyle='--', alpha=0.4, axis='both')
    #
    # Also place axes captions
    #
    label1 = np.array([45, -5, 1]) @ np.transpose(A)
    ax1.text(label1[0], label1[1], '%C2H6')
    label2 = np.array([95, -5, 1]) @ np.transpose(A)
    ax1.text(label2[0], label2[1], '0')
    label3 = np.array([5, -5, 1]) @ np.transpose(A)
    ax1.text(label3[0], label3[1], '100')
    label4 = np.array([-10, 55, 1]) @ np.transpose(A)
    ax1.text(label4[0], label4[1], '%CH4')
    label5 = np.array([-3, 5, 1]) @ np.transpose(A)
    ax1.text(label5[0], label5[1], '0')
    label6 = np.array([-7, 95, 1]) @ np.transpose(A)
    ax1.text(label6[0], label6[1], '100')
    label7 = np.array([45, 55, 1]) @ np.transpose(A)
    ax1.text(label7[0], label7[1], '%C2H4')
    label8 = np.array([5, 95, 1]) @ np.transpose(A)
    ax1.text(label8[0], label8[1], '0')
    label9 = np.array([95, 5, 1]) @ np.transpose(A)
    ax1.text(label9[0], label9[1], '100')
    label10 = np.array([-4, 88, 1]) @ np.transpose(A)
    ax1.text(label10[0], label10[1], 'PD', color='#232663')
    label11 = np.array([5, 15, 1]) @ np.transpose(A)
    ax1.text(label11[0], label11[1], 'O', color='#232663')
    label12 = np.array([5, 86, 1]) @ np.transpose(A)
    ax1.text(label12[0], label12[1], 'O', color='#232663')
    label13 = np.array([5, 60, 1]) @ np.transpose(A)
    ax1.text(label13[0], label13[1], 'S', color='#232663')
    label14 = np.array([43, 15, 1]) @ np.transpose(A)
    ax1.text(label14[0], label14[1], 'T3', color='#232663')
    label15 = np.array([75, 15, 1]) @ np.transpose(A)
    ax1.text(label15[0], label15[1], 'T3', color='#232663')
    label16 = np.array([21, 70, 1]) @ np.transpose(A)
    ax1.text(label16[0], label16[1], 'T2', color='#232663')
    label17 = np.array([35, 42, 1]) @ np.transpose(A)
    ax1.text(label17[0], label17[1], 'C', color='#232663')
    label18 = np.array([27, 106, 1]) @ np.transpose(A)
    # ax1.text(label18[0], label18[1], 'Fault detected: ', color='#000')
    #
    # Detect fault by region
    #
    fault = None
    if x <= 1 and 84 <= y <= 98 and 2 <= z <= 15:
        # label20 = np.array([33, 94, 1]) @ np.transpose(A)
        # ax1.text(label20[0], label20[1], 'PD', color='#000')
        # label21 = np.array([36, 88, 1]) @ np.transpose(A)
        # ax1.text(label21[0], label21[1], 'Partial discharges', color='#000')
        fault = "PD - Partial discharges"
    elif x <= 10 and 36 <= y <= 85 and 15 <= z <= 54:
        # label20 = np.array([33, 94, 1]) @ np.transpose(A)
        # ax1.text(label20[0], label20[1], 'S', color='#000000')
        # label21 = np.array([36, 88, 1]) @ np.transpose(A)
        # ax1.text(label21[0], label21[1], 'Stray gassing of', color='#000000')
        # label22 = np.array([39, 82, 1]) @ np.transpose(A)
        # ax1.text(label22[0], label22[1], 'mineral oil', color='#000000')
        fault = "S - Stray gassing of mineral oil"
    elif x <= 10:
        # label20 = np.array([33, 94, 1]) @ np.transpose(A)
        # ax1.text(label20[0], label20[1], 'O', color='#000000')
        # label21 = np.array([36, 88, 1]) @ np.transpose(A)
        # ax1.text(label21[0], label21[1], 'Overheating', color='#000000')
        # label22 = np.array([39, 82, 1]) @ np.transpose(A)
        # ax1.text(label22[0], label22[1], 't < 250°C', color='#000000')
        fault = "O - Overheating, t < 250°C"
    elif 10 <= x <= 35 and 53 <= y <= 90 and z <= 12:
        # label20 = np.array([33, 94, 1]) @ np.transpose(A)
        # ax1.text(label20[0], label20[1], 'T2', color='#000')
        # label21 = np.array([36, 88, 1]) @ np.transpose(A)
        # ax1.text(label21[0], label21[1], 'Thermal fault', color='#000')
        # label22 = np.array([39, 82, 1]) @ np.transpose(A)
        # ax1.text(label22[0], label22[1], '300°C < t < 700°C', color='#000')
        fault = "T2 - Thermal fault, 300°C < t < 700°C"
    elif 10 <= x <= 35 and y <= 60 and 30 <= z <= 90:
        # label20 = np.array([33, 94, 1]) @ np.transpose(A)
        # ax1.text(label20[0], label20[1], 'ND', color='#000000')
        # label21 = np.array([36, 88, 1]) @ np.transpose(A)
        # ax1.text(label21[0], label21[1], 'Not detected', color='#000000')
        fault = "ND - Not detected"
    elif (10 <= x <= 50 and 20 <= y <= 78 and 12 <= z <= 30) or (50 <= x <= 70 and y <= 36 and 14 <= z <= 30):
        # label20 = np.array([33, 94, 1]) @ np.transpose(A)
        # ax1.text(label20[0], label20[1], 'C', color='#000000')
        # label21 = np.array([36, 88, 1]) @ np.transpose(A)
        # ax1.text(label21[0], label21[1], 'Paper carbonization', color='#000000')
        # label22 = np.array([39, 82, 1]) @ np.transpose(A)
        # ax1.text(label22[0], label22[1], 't > 300°C', color='#000000')
        fault = "C - Paper carbonization, t > 300°C"
    else:
        # label20 = np.array([33, 94, 1]) @ np.transpose(A)
        # ax1.text(label20[0], label20[1], 'T3', color='#000000')
        # label21 = np.array([36, 88, 1]) @ np.transpose(A)
        # ax1.text(label21[0], label21[1], 'Thermal fault', color='#000000')
        # label22 = np.array([39, 82, 1]) @ np.transpose(A)
        # ax1.text(label22[0], label22[1], 't > 700°C', color='#000000')
        fault = "T3 - Thermal fault, t > 700°C"
    #
    # Show the final plot
    #
    ax1.set_xlim(0, 625)
    ax1.set_ylim(0, 550)
    ax1.get_xaxis().set_visible(False)
    ax1.get_yaxis().set_visible(False)

    plt.savefig('dga/static/images/dt5.png')
    
    return fault


def centroid(c2h6, h2, c2h2, c2h4, ch4):
    gas = [c2h6, h2, c2h2, c2h4, ch4]
    # print(gas)

    total = sum(gas)
    count = 0
    for i in gas:
        percentage = (i / total) * 100
        gas[count] = percentage
        count = count + 1

    xc2h6 = gas[0] * math.cos(math.radians(162))
    yc2h6 = gas[0] * math.sin(math.radians(162))

    xh2 = gas[1] * math.cos(math.radians(90))
    yh2 = gas[1] * math.sin(math.radians(90))

    xc2h2 = gas[2] * math.cos(math.radians(18))
    yc2h2 = gas[2] * math.sin(math.radians(18))

    xc2h4 = gas[3] * math.cos(math.radians(-54))
    yc2h4 = gas[3] * math.sin(math.radians(-54))

    xch4 = gas[4] * math.cos(math.radians(-126))
    ych4 = gas[4] * math.sin(math.radians(-126))

    x = [xc2h6, xh2, xc2h2, xc2h4, xch4]
    y = [yc2h6, yh2, yc2h2, yc2h4, ych4]

    a0 = x[0] * y[1] - x[1] * y[0]
    a1 = x[1] * y[2] - x[2] * y[1]
    a2 = x[2] * y[3] - x[3] * y[2]
    a3 = x[3] * y[4] - x[4] * y[3]
    a4 = x[4] * y[0] - x[0] * y[4]

    a = [a0, a1, a2, a3, a4]

    for i in a:
        count = count + i
    area = count * 0.5

    # calculate x and y coordinate
    cx = ((x[0] + x[1]) * a[0]) + ((x[1] + x[2]) * a[1]) + ((x[2] + x[3]) * a[2]) + ((x[3] + x[4]) * a[3]) + (
            (x[4] + x[0]) * a[4])
    Cx = cx * (1 / (6 * area))

    cy = ((y[0] + y[1]) * a[0]) + ((y[1] + y[2]) * a[1]) + ((y[2] + y[3]) * a[2]) + ((y[3] + y[4]) * a[3]) + (
            (y[4] + y[0]) * a[4])
    Cy = cy * (1 / (6 * area))
    # print("Cx = ", Cx)
    # print("Cx = ", Cy)

    return [Cx, Cy, 1]


def pentagon1(c2h6, h2, c2h2, c2h4, ch4):
    coordinate = centroid(c2h6, h2, c2h2, c2h4, ch4)
    print("The coordinate array pentagon 1 = ", coordinate)

    A = np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]])

    #
    # Define a set of points for Duval triangle regions
    #
    p = np.array([
        [0, 0, 1],  # center
        [0, 40, 1],  # p1
        [38, 12.4, 1],  # p2
        [23.5, -32.4, 1],  # p3
        [-23.5, -32.4, 1],  # p4
        [-38, 12.4, 1],  # p5
        [-1, 33, 1],  # p6
        [0, 33, 1],  # -7
        [-1, 24.5, 1],  # p8
        [0, 24.5, 1],  # p9
        [4, 16, 1],  # p10
        [-35, 3.1, 1],  # p11
        [0, 1.5, 1],  # p12
        [0, -3, 1],  # p13
        [-6, -4, 1],  # p14
        [32, -6.1, 1],  # p15
        [24.3, -30, 1],  # p16
        [1, -32.4, 1],  # p17
        [-22.5, -32.4, 1]])  # p18

    #
    # Apply the coordinates transformation to all points
    #
    v = p @ np.transpose(A)

    #
    # Set one more sample point
    sample_point = np.array(coordinate) @ np.transpose(A)
    #
    # Define each of the regions by the coordinates of its angle points
    #
    region_PD = v[[6, 7, 9, 8], :]
    region_T1 = v[[11, 12, 13, 14, 18, 4], :]
    region_T2 = v[[14, 17, 18], :]
    region_T3 = v[[14, 13, 16, 3, 17], :]
    region_D1 = v[[1, 2, 15, 10, 12], :]
    region_D2 = v[[10, 15, 16, 13, 12], :]
    region_S = v[[1, 7, 6, 8, 9, 12, 11, 5], :]

    #
    # Plot the results
    #
    fig, ax1 = plt.subplots()
    ax1.fill(region_PD[:, 0], region_PD[:, 1], '#c92a2a')
    ax1.fill(region_T1[:, 0], region_T1[:, 1], '#ffff80')
    ax1.fill(region_T2[:, 0], region_T2[:, 1], '#e89f9b')
    ax1.fill(region_T3[:, 0], region_T3[:, 1], '#e7c490')
    ax1.fill(region_S[:, 0], region_S[:, 1], '#89d2ef')
    ax1.fill(region_D1[:, 0], region_D1[:, 1], '#eca9fc')
    ax1.fill(region_D2[:, 0], region_D2[:, 1], '#B8F198')

    ax1.scatter(sample_point[0], sample_point[1], marker='x', c='r', zorder=2) # type: ignore
    ax1.grid(linestyle='--', alpha=0.4, axis='both')

    #
    # Also place axes captions
    #
    label1 = np.array([-2, 41, 1]) @ np.transpose(A)
    ax1.text(label1[0], label1[1], 'H2')
    label2 = np.array([-46, 12, 1]) @ np.transpose(A)
    ax1.text(label2[0], label2[1], 'C2H6')
    label3 = np.array([-28, -36, 1]) @ np.transpose(A)
    ax1.text(label3[0], label3[1], 'CH4')
    label4 = np.array([23, -36, 1]) @ np.transpose(A)
    ax1.text(label4[0], label4[1], 'C2H4')
    label5 = np.array([39, 12, 1]) @ np.transpose(A)
    ax1.text(label5[0], label5[1], 'C2H2')
    label6 = np.array([-4, 33, 1]) @ np.transpose(A)
    ax1.text(label6[0], label6[1], 'PD', color='#232663')
    label7 = np.array([16, 17, 1]) @ np.transpose(A)
    ax1.text(label7[0], label7[1], 'D1', color='#232663')
    label8 = np.array([20, -13, 1]) @ np.transpose(A)
    ax1.text(label8[0], label8[1], 'D2', color='#232663')
    label9 = np.array([9, -24, 1]) @ np.transpose(A)
    ax1.text(label9[0], label9[1], 'T3', color='#232663')
    label10 = np.array([-11, -24, 1]) @ np.transpose(A)
    ax1.text(label10[0], label10[1], 'T2', color='#232663')
    label11 = np.array([-23, -13, 1]) @ np.transpose(A)
    ax1.text(label11[0], label11[1], 'T1', color='#232663')
    label12 = np.array([-20, 17, 1]) @ np.transpose(A)
    ax1.text(label12[0], label12[1], 'S', color='#232663')
    #
    # Show the final plot
    #
    ax1.set_xlim(-50, 50)
    ax1.set_ylim(-45, 50)
    ax1.get_xaxis().set_visible(False)
    ax1.get_yaxis().set_visible(False)
    
    plt.savefig('dga/static/images/dp1.png')


def pentagon2(c2h6, h2, c2h2, c2h4, ch4):
    coordinate = centroid(c2h6, h2, c2h2, c2h4, ch4)
    print("The coordinate array pentagon 2 = ", coordinate)

    A = np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]])

    #
    # Define a set of points for Duval triangle regions
    #
    p = np.array([
        [0, 0, 1],  # center
        [0, 40, 1],  # p1
        [38, 12.4, 1],  # p2
        [23.5, -32.4, 1],  # p3
        [-23.5, -32.4, 1],  # p4
        [-38, 12.4, 1],  # p5
        [-1, 33, 1],  # p6
        [0, 33, 1],  # -7
        [-1, 24.5, 1],  # p8
        [0, 24.5, 1],  # p9
        [4, 16, 1],  # p10
        [-35, 3.1, 1],  # p11
        [0, 1.5, 1],  # p12
        [0, -3, 1],  # p13
        [-3.5, -3.5, 1],  # p14
        [32, -6.1, 1],  # p15
        [24.3, -30, 1],  # p16
        [2.5, -32.4, 1],  # p17
        [-21.5, -32.4, 1],  # p18
        [-11, -8, 1],  # p19
        [-6, -4, 1]])  # p20

    #
    # Apply the coordinates transformation to all points
    #
    v = p @ np.transpose(A)

    #
    # Set one more sample point
    sample_point = np.array(coordinate) @ np.transpose(A)

    #
    # Define each of the regions by the coordinates of its angle points
    #
    region_PD = v[[6, 7, 9, 8], :]
    region_O = v[[11, 12, 13, 14, 20, 19, 18, 4], :]
    region_C = v[[14, 17, 18, 19, 20], :]
    region_T3H = v[[14, 13, 16, 3, 17], :]
    region_D1 = v[[1, 2, 15, 10, 12], :]
    region_D2 = v[[10, 15, 16, 13, 12], :]
    region_S = v[[1, 7, 6, 8, 9, 12, 11, 5], :]

    #
    # Plot the results
    #
    fig, ax1 = plt.subplots()
    ax1.fill(region_PD[:, 0], region_PD[:, 1], '#c92a2a')
    ax1.fill(region_O[:, 0], region_O[:, 1], '#ffc4a9')
    ax1.fill(region_C[:, 0], region_C[:, 1], '#f3918d')
    ax1.fill(region_T3H[:, 0], region_T3H[:, 1], '#f6e999')
    ax1.fill(region_S[:, 0], region_S[:, 1], '#89d2ef')
    ax1.fill(region_D1[:, 0], region_D1[:, 1], '#eca9fc')
    ax1.fill(region_D2[:, 0], region_D2[:, 1], '#B8F198')

    ax1.scatter(sample_point[0], sample_point[1], marker='x', c='r', zorder=2) # type: ignore
    ax1.grid(linestyle='--', alpha=0.4, axis='both')

    #
    # Also place axes captions
    #
    label1 = np.array([-2, 41, 1]) @ np.transpose(A)
    ax1.text(label1[0], label1[1], 'H2')
    label2 = np.array([-46, 12, 1]) @ np.transpose(A)
    ax1.text(label2[0], label2[1], 'C2H6')
    label3 = np.array([-28, -36, 1]) @ np.transpose(A)
    ax1.text(label3[0], label3[1], 'CH4')
    label4 = np.array([23, -36, 1]) @ np.transpose(A)
    ax1.text(label4[0], label4[1], 'C2H4')
    label5 = np.array([39, 12, 1]) @ np.transpose(A)
    ax1.text(label5[0], label5[1], 'C2H2')
    label6 = np.array([-4, 33, 1]) @ np.transpose(A)
    ax1.text(label6[0], label6[1], 'PD', color='#232663')
    label7 = np.array([16, 17, 1]) @ np.transpose(A)
    ax1.text(label7[0], label7[1], 'D1', color='#232663')
    label8 = np.array([20, -13, 1]) @ np.transpose(A)
    ax1.text(label8[0], label8[1], 'D2', color='#232663')
    label9 = np.array([5, -24, 1]) @ np.transpose(A)
    ax1.text(label9[0], label9[1], 'T3-H', color='#232663')
    label10 = np.array([-9, -24, 1]) @ np.transpose(A)
    ax1.text(label10[0], label10[1], 'C', color='#232663')
    label11 = np.array([-23, -13, 1]) @ np.transpose(A)
    ax1.text(label11[0], label11[1], 'O', color='#232663')
    label12 = np.array([-20, 17, 1]) @ np.transpose(A)
    ax1.text(label12[0], label12[1], 'S', color='#232663')
    #
    # Show the final plot
    #
    ax1.set_xlim(-50, 50)
    ax1.set_ylim(-45, 50)
    ax1.get_xaxis().set_visible(False)
    ax1.get_yaxis().set_visible(False)
    
    plt.savefig('dga/static/images/dp2.png')