import paramiko
from paramiko import SSHClient
from scp import SCPClient
from time import sleep

def download_data():
    ssh = SSHClient()
    ssh.load_system_host_keys()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    hotspotIP = '172.20.10.4'
    orionIP = '10.0.0.233'
    ssh.connect(hostname= hotspotIP, 
                port = '22',
                username='debian',
                password='birdsdp8')
                #pkey='load_key_if_relevant')
    sftp = ssh.open_sftp()

    # Copy audio files into Audio_Inputs
    #with SCPClient(ssh.get_transport(), sanitize=lambda x: x) as scp:
        #scp.get('/home/debian/sd_card/pics_audio/*.wav','/Users/orionmclain/BirdNET-Analyzer/Audio_Inputs')

    
    # Copy images files into Feeder_Images
    with SCPClient(ssh.get_transport(), sanitize=lambda x: x) as scp:
        scp.get('/home/debian/sd_card/pics_audio/*.png','/Users/orionmclain/BirdNET-Analyzer/Feeder_Images') 
        
    #sftp_client.close()
    scp.close()
    ssh.close()

def remoteStart():
    ssh = paramiko.SSHClient()
    ssh.load_system_host_keys()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    hotspotIP = '172.20.10.4'
    orionIP = '10.0.0.233'
    ssh.connect(orionIP, port=22, username='debian', password='birdsdp8')

    # Command to start the feeder functions remotely   -- repeat the following two lines for all needed commands
    command1 = './picture_control.sh'
    #command2 = './record.sh'

    # Execute command remotely
    stdin, stdout, stderr = ssh.exec_command(command1)
    #stdin, stdout, stderr = ssh.exec_command(command2)

    # Print output
    print(stdout.read().decode())

    # Close the SSH connection
    ssh.close()

def remoteStop():
    ssh = paramiko.SSHClient()
    ssh.load_system_host_keys()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect('172.20.10.4', port=22, username='debian', password='birdsdp8')

    # Command to stop the feeder functions remotely   -- repeat the following two lines for all needed commands
    command = ''
    # Execute command remotely
    stdin, stdout, stderr = ssh.exec_command(command)

    # Print output
    print(stdout.read().decode())

    # Close the SSH connection
    ssh.close()

def removeFiles():
    ssh = paramiko.SSHClient()
    ssh.load_system_host_keys()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    hotspotIP = '172.20.10.4'
    orionIP = '10.0.0.233'
    ssh.connect(hotspotIP, port=22, username='debian', password='birdsdp8')

    # Command to remove audio and image files  
    command = 'rm sd_card/pics_audio/*'
    # Execute command remotely
    stdin, stdout, stderr = ssh.exec_command(command)

    # Print output
    print(stdout.read().decode())

    # Close the SSH connection
    ssh.close()


if __name__ == "__main__":
    #download_data()   # 
    remoteStart()
    #removeFiles()