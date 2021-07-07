#!/bin/sh -x
kill -9 $(sudo lsof -t -i:4445)
# kill -9 $(sudo lsof -t -i:4343)