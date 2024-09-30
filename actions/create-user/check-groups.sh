#!/bin/bash

if [[ "$USER_GROUPS" == "" ]]; then
  echo ""
else
  echo "--groups $USER_GROUPS"
fi
