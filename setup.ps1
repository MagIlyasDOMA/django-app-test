Move-Item -Path 'app_test' -Destination '../app_test'
Move-Item -Path 'manage.py' -Destination '../'
Remove-Item -Path './' -Recurse -Force