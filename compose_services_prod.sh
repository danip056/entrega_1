#!/bin/sh

echo "Select the service you want to compose:"
select env in "All" "Web" "Worker" "File" "BD"; do
    case $env in
        Web ) docker compose -f "docker-compose-web-prod.yml" up -d; break;;
        Worker ) docker compose -f "docker-compose-worker-prod.yml" up -d; break;;
        cancel ) echo "No option was selected, exit."; exit;;
        * ) echo "Please select shown options.";;
    esac
done