#!/bin/bash

build_lib() {
  rm -rf BUILD
  cp -rf SRC BUILD
  (cd BUILD && ./autogen.sh && ./configure --disable-shared --disable-freetype && make)
}
GIT_URL="https://github.com/libming/libming.git"
TAG_NAME="ming-0_4_7"
RELEVANT_BINARIES="swftophp"

[ ! -e SRC ] && git clone $GIT_URL SRC
cd SRC
git checkout $TAG_NAME
cd ..

build_lib
chmod 777 BUILD/util/swftophp
cp BUILD/util/swftophp ./swftophp-4.7

