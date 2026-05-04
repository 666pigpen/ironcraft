#!/bin/sh
#
# Gradle start up script for UN*X
#
APP_NAME="Gradle"
APP_BASE_NAME=$(basename "$0")
APP_HOME=$(cd "$(dirname "$0")" && pwd -P)

MAX_FD="maximum"
warn() { echo "$*"; }
die() { echo "$*"; exit 1; }

# Determine the Java command to use
if [ -n "$JAVA_HOME" ]; then
    JAVACMD="$JAVA_HOME/bin/java"
    if [ ! -x "$JAVACMD" ]; then
        die "JAVA_HOME is set to an invalid directory: $JAVA_HOME"
    fi
else
    JAVACMD="java"
    which java >/dev/null 2>&1 || die "Java is not installed."
fi

# Determine working directory and classpath
GRADLE_USER_HOME="${GRADLE_USER_HOME:-$HOME/.gradle}"
WRAPPER_JAR="$APP_HOME/gradle/wrapper/gradle-wrapper.jar"
WRAPPER_PROPERTIES="$APP_HOME/gradle/wrapper/gradle-wrapper.properties"

exec "$JAVACMD" \
    -classpath "$WRAPPER_JAR" \
    org.gradle.wrapper.GradleWrapperMain \
    "$@"
