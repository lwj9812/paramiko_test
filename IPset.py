import paramiko

# SSH 연결 정보
servers = [
    {   #dns-server
        'hostname': 'hostIP',
        'username': 'hostname',
        'password': 'passwd'
    },
    {   #dhcp-server
        'hostname': 'hostIP',
        'username': 'hostname',
        'password': 'passwd'
    },
    {   #web-server
        'hostname': 'hostIP',
        'username': 'hostname',
        'password': 'passwd'
    }
]

# 변경할 네트워크 설정
new_ip_addresses = ['새로운_IP_주소_1', '새로운_IP_주소_2', '새로운_IP_주소_3']
new_subnet_mask = '255.255.255.0'
new_gateway = '새로운_게이트웨이_주소'
new_dns = '새로운_DNS_주소'

# SSH 연결 및 네트워크 설정 변경
for index, server_info in enumerate(servers):
    hostname = server_info['hostname']
    username = server_info['username']
    password = server_info['password']
    new_ip = new_ip_addresses[index]
    
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname, port=22, username=username, password=password)
    
    commands = [
        f"sudo sed -i '/^IPADDR=/d' /etc/sysconfig/network-scripts/ifcfg-enp0s3",
        f"sudo sed -i '/^NETMASK=/d' /etc/sysconfig/network-scripts/ifcfg-enp0s3",
        f"sudo sed -i '/^GATEWAY=/d' /etc/sysconfig/network-scripts/ifcfg-enp0s3",
        f"sudo sed -i '/^DNS1=/d' /etc/sysconfig/network-scripts/ifcfg-enp0s3",
        f"sudo echo 'IPADDR={new_ip}' >> /etc/sysconfig/network-scripts/ifcfg-enp0s3",
        f"sudo echo 'NETMASK={new_subnet_mask}' >> /etc/sysconfig/network-scripts/ifcfg-enp0s3",
        f"sudo echo 'GATEWAY={new_gateway}' >> /etc/sysconfig/network-scripts/ifcfg-enp0s3",
        f"sudo echo 'DNS1={new_dns}' >> /etc/sysconfig/network-scripts/ifcfg-enp0s3",
        "sudo sed -i 's/BOOTPROTO=dhcp/#BOOTPROTO=dhcp/' /etc/sysconfig/network-scripts/ifcfg-enp0s3",
        "sudo systemctl restart network"
    ]
    
    print(f"서버 {hostname}에서 네트워크 설정 변경을 시작합니다.")
    
    for command in commands:
        stdin, stdout, stderr = ssh.exec_command(command)
        output = stdout.read().decode('utf-8')
        error = stderr.read().decode('utf-8')
        if output:
            print(output)
        if error:
            print(error)
    
    print(f"서버 {hostname}의 네트워크 설정 변경이 완료되었습니다.")
    
    ssh.close()
