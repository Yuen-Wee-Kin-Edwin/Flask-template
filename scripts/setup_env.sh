#!/usr/bin/env bash

# Detect shell type
if [ -n "$ZSH_VERSION" ]; then
  shell="zsh"
elif [ -n "$BASH_VERSION" ]; then
  shell="bash"
else
  echo "Unsupported shell. Use Bash or Zsh." >&2
  exit 1
fi

if [ "$shell" = "zsh" ]; then
  # Define the targets and sources as two separate arrays.
  targets=(".env" ".env.production")
  sources=(".env.example" ".env.production.example")

  for i in {1..2}; do
    target="${targets[i]}"
    source="${sources[i]}"

    if [ -f "$target" ]; then
      echo "$target already exists. Skipping creation."
    else
      if [ -f "$source" ]; then
        cp "$source" "$target"
        echo "Created $target from $source."
      else
        echo "Error: $source not found. Cannot create $target." >&2
      fi
    fi
  done

elif [ "$shell" = "bash" ]; then
  # Define the targets and sources as two separate arrays.
  targets=(".env" ".env.production")
  sources=(".env.example" ".env.production.example")

  for i in "${!targets[@]}"; do
    target="${targets[$i]}"
    source="${sources[$i]}"

    if [ -f "$target" ]; then
      echo "$target already exists. Skipping creation."
    else
      if [ -f "$source" ]; then
        cp "$source" "$target"
        echo "Created $ target from $source."
      else
        echo "Error: $source not found. Cannot create $target." >&2
      fi
    fi
  done
fi
    