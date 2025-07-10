# Description

Simple docker-compose file for fast deployment of working xray and easy adding new clients.

# Running

    - add address of a server to address.txt
    - preconfigure config_path/config.json for your needs
    - docker compose up -d --build
    - docker exec -it xray-app bash
    - python app.py (for generating new private and public keys)
    - python app.py -n $client_name
    - share generated link

**On first launch privateKey in config.json should not be empty.**