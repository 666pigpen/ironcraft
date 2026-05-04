#!/bin/bash
# Downloads the Gradle wrapper jar needed to build the project
mkdir -p gradle/wrapper
curl -L "https://github.com/gradle/gradle/raw/v8.8.0/gradle/wrapper/gradle-wrapper.jar" \
     -o gradle/wrapper/gradle-wrapper.jar
echo "Gradle wrapper jar downloaded."
