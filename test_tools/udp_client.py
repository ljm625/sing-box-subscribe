import time
import socks  # 导入 PySocks
import socket

# 配置测试目标
TARGET_IP = '127.0.0.1'     # 替换为实际的远程服务端公网 IP
TARGET_PORT = 6666
PACKET_COUNT = 1000        # 测试总发包数
INTERVAL = 0.001           # 发包间隔（秒）

# 配置 SOCKS5 代理服务器
PROXY_HOST = '127.0.0.1'  # 你的代理软件本地 IP
PROXY_PORT = 7890         # 你的代理软件本地端口

def start_proxy_client():
    # 创建支持 SOCKS 代理的 UDP socket
    client_socket = socks.socksocket(socket.AF_INET, socket.SOCK_DGRAM)
    
    # 设置 SOCKS5 代理（注意：必须确保你的代理服务器开启了 UDP 转发功能）
    client_socket.set_proxy(socks.SOCKS5, PROXY_HOST, PROXY_PORT)
    client_socket.settimeout(2.0)  # 设置超时时间

    received_count = 0
    total_rtt = 0.0
    max_rtt = 0.0
    min_rtt = float('inf')

    print(f"已配置代理 {PROXY_HOST}:{PROXY_PORT}")
    print(f"正在通过代理向 {TARGET_IP}:{TARGET_PORT} 发送测试包...")

    for seq in range(PACKET_COUNT):
        # 构造带有序列号和时间戳的 Payload
        message = f"{seq},{time.time()}".encode('utf-8')
        
        try:
            # 发送数据
            client_socket.sendto(message, (TARGET_IP, TARGET_PORT))
            
            # 接收回显数据
            data, server = client_socket.recvfrom(1024)
            
            # 计算往返延迟 (RTT)
            rtt = (time.time() - float(data.decode('utf-8').split(',')[1])) * 1000
            
            received_count += 1
            total_rtt += rtt
            if rtt > max_rtt: max_rtt = rtt
            if rtt < min_rtt: min_rtt = rtt

        except socket.timeout:
            print(f"包 {seq} 超时 / 丢包")
        except Exception as e:
            # 如果代理服务器未开启 UDP 转发，通常会在这里抛出 General SOCKS server failure
            print(f"包 {seq} 错误: {e}")

        time.sleep(INTERVAL)

    # 统计最终结果
    loss_rate = ((PACKET_COUNT - received_count) / PACKET_COUNT) * 100
    avg_rtt = total_rtt / received_count if received_count > 0 else 0

    print("\n" + "="*30)
    print("UDP 代理双向丢包测试结果")
    print("="*30)
    print(f"测试总数: {PACKET_COUNT} | 成功接收: {received_count}")
    print(f"通过代理丢包率: {loss_rate:.2f}%")
    if received_count > 0:
        print(f"平均 RTT : {avg_rtt:.2f} ms")
        print(f"延迟范围 : {min_rtt:.2f} ms ~ {max_rtt:.2f} ms")
    print("="*30)

    client_socket.close()

if __name__ == '__main__':
    start_proxy_client()
