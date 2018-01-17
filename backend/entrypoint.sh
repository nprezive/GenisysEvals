#!/bin/sh


if [ ! -f FirstRunComplete ]; then
  echo "First run. Collecting static files..."
  python manage.py collectstatic --clear --no-input
  if [ $? == 0 ]; then
    touch FirstRunComplete
  else
    echo ""
    echo "ERROR!"
    echo ""
    exit 200
  fi

  echo "Done"
else
  echo "FirstRunComplete exist not runing first run cmds"
fi

exec "$@"
