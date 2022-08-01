#!/bin/bash
mkdir -p ~/.local/bin
if [[ ! "$PATH" =~ "$HOME/.local/bin" ]]; then
    echo -e '\nexport PATH="$HOME/.local/bin:$PATH"' >> $rc
fi
