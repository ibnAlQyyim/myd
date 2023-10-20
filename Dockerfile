# Use the base image
FROM modenaf360/gotty:latest
 
# Expose the desired port
EXPOSE 7860
 
# Start Gotty with the specified command
CMD ["gotty", "-r", "-w", "--port", "7860", "/bin/bash"]
