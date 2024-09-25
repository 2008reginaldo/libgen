#!/bin/bash

# Define the target link and destination path
TARGET="$HOME/.local/share/sioyek/shared.db"
LINK="$HOME/Dropbox/Academico/libgen/shared.db"

# Check if the link already exists
if [ ! -L "$LINK" ]; then
    # Check if the destination file already exists
    if [ ! -e "$LINK" ]; then
        # Create the symbolic link
        ln -s "$TARGET" "$LINK"
        echo "Symbolic link created: $LINK -> $TARGET"
    else
        echo "A file already exists at the destination path: $LINK"
    fi
else
    echo "Symbolic link already exists: $LINK -> $(readlink $LINK)"
fi

