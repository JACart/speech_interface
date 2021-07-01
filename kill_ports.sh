#!/bin/sh -x
kill $(sudo lsof -t -i:4445)
kill $(sudo lsof -t -i:4343)