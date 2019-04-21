# Install Node on Raspberry
# From https://zhuanlan.zhihu.com/p/36323399
wget https://npm.taobao.org/mirrors/node/latest/node-v10.0.0-linux-armv7l.tar.xz
xz -d node-v10.0.0-linux-armv7l.tar.xz
tar -xavf node-v10.0.0-linux-armv7l.tar
# sudo rm -rf /usr/bin/node
# 如果曾经装过node
mv ./node-v10.0.0-linux-armv7l /usr/local/node
sudo ln -s /usr/local/node/bin/node /usr/bin/node
sudo ln -s /usr/local/node/bin/npm /usr/bin/npm
node --version
npm --version
