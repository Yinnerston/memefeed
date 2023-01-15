if git status --short | grep static; then
    # docker-compose -f docker-compose.prod.yml exec memefeed python manage.py collectstatic --no-input --clear
    echo "MATCH"
fi