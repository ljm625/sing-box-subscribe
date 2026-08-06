import socket

# 配置
HOST = '0.0.0.0'
PORT = 6666

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind((HOST, PORT))
    print(f"UDP 服务端已启动，监听 {HOST}:{PORT}")

    expected_seq = {}
    lost_counts = {}

    while True:
        try:
            data, addr = server_socket.recvfrom(1024)
            # 接收到数据后原样发回给客户端，实现双向通路
            server_socket.sendto(data, addr)
            
            # 解析包信息进行日志统计 (若客户端发送了特定格式的数据)
            try:
                decoded_data = data.decode('utf-8')
                parts = decoded_data.split(',')
                if len(parts) >= 2:
                    seq = int(parts[0])
                    client_ip = addr[0]
                    
                    if client_ip not in expected_seq:
                        expected_seq[client_ip] = seq
                        lost_counts[client_ip] = 0
                    
                    if seq > expected_seq[client_ip]:
                        lost = seq - expected_seq[client_ip]
                        lost_counts[client_ip] += lost
                        print(f"来自 {client_ip} 的数据包断层！丢失约 {lost} 个包。累计丢包数: {lost_counts[client_ip]}")
                    
                    expected_seq[client_ip] = seq + 1
            except:
                pass
                
        except KeyboardInterrupt:
            print("\n服务端停止运行。")
            break
    server_socket.close()

if __name__ == '__main__':
    start_server()