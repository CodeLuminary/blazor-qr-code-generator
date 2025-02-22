#!/bin/bash
dotnet run --urls="http://*:5147"  & sleep 20 && pytest e2etest/evals.py
read