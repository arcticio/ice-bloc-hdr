#!/bin/bash

VERSION_FILE="version.py"

VERSION=`cat $VERSION_FILE`

length=${#VERSION} 

POS=11
OFF=1
let "LEN = $length - $POS - $OFF"

VERSION=${VERSION:$POS:$LEN}

increment_version ()
{
  declare -a part=( ${1//\./ } )
  declare    new
  declare -i carry=1

  for (( CNTR=${#part[@]}-1; CNTR>=0; CNTR-=1 )); do
    len=${#part[CNTR]}
    new=$((part[CNTR]+carry))
    [ ${#new} -gt $len ] && carry=1 || carry=0
    [ $CNTR -gt 0 ] && part[CNTR]=${new: -len} || part[CNTR]=${new}
  done

  new="${part[*]}"
  
  echo -e "VERSION = '${new// /.}'\n" > $VERSION_FILE

} 

increment_version $VERSION

echo 
echo "VERSION = ${VERSION}"
