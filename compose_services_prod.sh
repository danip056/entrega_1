#!/bin/sh

echo "Select the service you want to compose:"
select env in "Web" "Worker"; do
    case $env in
        Web ) docker compose -f "docker-compose-web-prod.yml" up -d --build; break;;
        Worker ) docker compose -f "docker-compose-worker-prod.yml" up -d --build; break;;
        cancel ) echo "No option was selected, exit."; exit;;
        * ) echo "Please select shown options.";;
    esac
done