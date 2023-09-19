import subprocess

def capture(entry_url):
   cmd = ['ffmpeg', '-i', entry_url]
   process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
   stdout, stderr = process.communicate()
   error_lines = (line for line in stderr.decode().split('\n') if 'error' in line.lower())
   for line in error_lines:
      print(line)