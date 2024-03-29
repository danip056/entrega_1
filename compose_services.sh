#!/bin/sh

# echo "Do you want to Build the image?"
# select env in "Yes" "No"; do
#     case $env in
#         Yes ) docker-compose -f "docker-compose-bd.yml" up -d; docker-compose -f "docker-compose-worker.yml" up -d; docker-compose -f "docker-compose-web.yml" up -d; break;;
#         No ) exit;;
#         * ) echo "Please select shown options.";;
#     esac
# done

echo "Select the service you want to compose:"
select env in "All" "Web" "Worker" "File" "BD"; do
    case $env in
        All ) docker-compose -f "docker-compose-bd.yml" up -d; docker-compose -f "docker-compose-worker.yml" up -d --build; docker-compose -f "docker-compose-web.yml" up -d --build; break;;
        Web ) docker-compose -f "docker-compose-web.yml" up -d; break;;
        Worker ) docker-compose -f "docker-compose-worker.yml" up -d; break;;
        BD ) docker-compose -f "docker-compose-bd.yml" up -d; break;;
        cancel ) echo "No option was selected, exit."; exit;;
        * ) echo "Please select shown options.";;
    esac
done