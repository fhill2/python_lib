#!/usr/bin/sh
curl \
  -H 'Authorization: token 23af11e56abeafd1e2954ff0487f40f2df2d2656' \
  -d '{"query":"query { currentUser { username } }"}' \
  http://127.0.0.1:7080/.api/graphql
