import subprocess

# Define the command
command = """
echo 'This sentence is spoken first. This sentence is synthesized while the first sentence is spoken.' | \
  ./piper/piper --model en_US-amy-low.onnx --output_file out.wav
"""

# Run the command in the shell
subprocess.run(command, shell=True)