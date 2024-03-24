#!/bin/bash

export AUTH0_DOMAIN='dev-tioi4bnfisc6bcli.us.auth0.com'
export ALGORITHMS="['RS256']"
export API_AUDIENCE='https://yesCompany/api'

echo 'hello world from setup.sh'
echo $AUTH0_DOMAIN
# echo ${ALGORITHMS[@]}
echo $API_AUDIENCE
echo $ALGORITHMS