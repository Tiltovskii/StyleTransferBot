import sys
import subprocess

subprocess.Popen([sys.executable, 'test_image.py', '--file', 'assets\\horse.png',
                  '--model-name', 'weights\\horse2zebra\\netG_A2B.pth'])
