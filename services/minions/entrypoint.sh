#!/bin/bash

socat -dd TCP-LISTEN:7771,reuseaddr,fork EXEC:/app/minions