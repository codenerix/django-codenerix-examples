#!/bin/bash

appname="`grep "^WSGI_APPLICATION" settings.py | cut -d "'" -f 2 | cut -d "." -f 1`"
apps="`find -name "models.py" | cut -d '/' -f 2 | sort`"

NEW=""
OLD=""
for app in $apps; do
    echo "Processing ${app}..."
    NEW="$NEW $app"
    header="`grep "^from django\.contrib\ import\ admin" $app/admin.py`"
    classes="`grep "^class" $app/models.py | grep -v "META: Abstract class" | cut -d " " -f 2 | cut -d "(" -f 1`"
    registered="`grep "^admin\.site\.register" $app/admin.py | cut -d "(" -f 2 | cut -d ")" -f 1 | cut -d "," -f 1`"
    imports=""
    registers=""
    for class in $classes ; do
        # Check if the class is registered already
        found="FALSE"
        for register in $registered ; do
            if [[ "$class" == "$register" ]] ; then
                found="TRUE"
                break
            fi
        done
        # Register the class if we haven't done before
        if [[ "$found" == "FALSE" ]] ; then
            if [[ -z "$imports" ]] ; then
                imports="$class"
            else
                imports="${imports}, ${class}"
            fi
            registers="$registers\nadmin.site.register(${class})"
            echo "    > $class added"
        fi
    done
    # If we have some to register
    if [[ ! -z "$registers" ]] ; then
        echo >> ${app}/admin.py
        echo "# Automatic added by Codenerix admin.py builder" >> ${app}/admin.py
        if [[ -z "$header" ]] ; then
            echo "from django.contrib import admin" >> ${app}/admin.py
        fi
        echo "from ${appname}.${app}.models import $imports" >> ${app}/admin.py
        echo -e "$registers" >> ${app}/admin.py
    fi
done
