'''
1.Model参数类型：
numpy.ndarray
'''

import numpy as np
import random
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

class Model(object):
    def __init__(self):
        pass

    # 标准差
    def square_accuracy(self, predictions, labels):
        accuracy = np.sqrt(np.mean(np.sum((predictions - labels)**2, 1)))
        return round(accuracy, 3)

    def ekf2d(
        self
       ,transition_states
       ,observation_states
       ,transition_func
       ,jacobF_func
       ,initial_state_covariance
       ,observation_matrices
       ,transition_covariance
       ,observation_covariance
        ):

        conv_length = len(transition_states)-1

        # 状态参数个数
        initial_state = transition_states[0]
        state_parameters_num = initial_state.shape[0]
        # 单个状态参数数组
        state_parameters = [0]*state_parameters_num
        temp = []
        for i in range(state_parameters_num):
            for v in transition_states:
                temp.append(v[i, 0])
            state_parameters[i] = temp
            temp = []

        # 获取单个观测参数
        observation_parameters_num = observation_states[0].shape[0]
        observation_parameters = [0]*observation_parameters_num
        for i in range(observation_parameters_num):
            for v in observation_states:
                temp.append(v[i, 0])
            observation_parameters[i] = temp
            temp = []

        S = [] # 融合估计位置
        X = initial_state # 初始状态
        # X = np.matrix('2; 2; 0') # 对初始状态进行验证
        S.append(X)
        P = initial_state_covariance # 状态协方差矩阵（初始状态不是非常重要，经过迭代会逼近真实状态）
        Q = transition_covariance # 状态转移协方差矩阵
        H = observation_matrices # 观测矩阵
        R = observation_covariance # 观测噪声方差

        for i in range(conv_length):
            # 状态预测
            state_values = [X[k, 0] for k in range(state_parameters_num)]
            new_state_values = transition_func(state_values)
            X_ = np.matrix([[new_state_values[k]] for k in range(state_parameters_num)])

            # 一阶线性化后的状态矩阵
            F = jacobF_func(i)
            P_ = F * P * F.T + Q
            K = P_ * H.T * np.linalg.pinv(H * P_ * H.T + R)
            Z = np.matrix([[observation_parameters[k][i+1]] for k in range(observation_parameters_num)]) # 新息
            X = X_ + K * (Z - H * X_)
            P = (np.eye(3) - K * H) * P_
            S.append(X)
        
        return S