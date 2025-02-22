# #!/bin/bash
docker build -t blazorapp .
docker container prune -f
docker run --rm  blazorapp  
read